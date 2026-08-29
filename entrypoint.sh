#!/bin/bash
# StreamTeX container entrypoint — supports three serve modes:
#   dual           (default) Nginx + Streamlit — static fallback on error
#   static-only    Nginx only — no Streamlit, minimal resources
#   streamlit-only Streamlit only — legacy behaviour (no Nginx)
#
# Env vars:
#   FOLDER          module to serve (e.g. modules/postair_opening)
#   STX_SERVE_MODE  dual | static-only | streamlit-only (default: dual)

set -e

FOLDER="${FOLDER:-modules/postair_opening}"
MODE="${STX_SERVE_MODE:-dual}"

cd /app/${FOLDER}

# --- Always: refresh cache and generate static HTML ---

echo "[entrypoint] Mode: ${MODE} | Folder: ${FOLDER}"

# Clear stale caches
rm -rf .stx_cache .streamlit/cache

# Re-warm the page cache (for Streamlit fast first load) — ONCE PER LANGUAGE:
# since streamtex 0.7.26 the paginated cache is keyed by block_kwargs, so
# {"lang": "fr"} owns its own TOC/markers/page titles (page_cache-<fp8>.json,
# EN and FR coexist). A deck opened with ?lang=fr after an EN-only warmup
# would otherwise build its cache on the first visitor.
if [ "$MODE" != "static-only" ]; then
    for lang in en fr; do
        echo "[entrypoint] Warming up page cache (${lang})..."
        STX_LANG=$lang uv run stx cache warmup . 2>/dev/null || true
    done
fi

# Generate static HTML exports — clean first to remove stale exports from other
# FOLDERs. ONE EXPORT PER LANGUAGE (plan-i18n D3, 2026-08-28) : the public reads
# /html/<lang>/ ; a widget never survives an export, so the language is the
# STX_LANG build parameter read by postair_lang — and, since streamtex 0.7.26,
# by `stx export html` itself for the <html lang> attribute (no rewrite needed).
rm -rf /app/static-html/*
BASE_NAME=$(basename "${FOLDER}")
TARGET="${BASE_NAME}/${BASE_NAME}.html"
for lang in en fr; do
    echo "[entrypoint] Generating static HTML (${lang})..."
    STX_LANG=$lang uv run stx export html --output /app/static-html/${lang}/ . 2>/dev/null || true
    if [ -f "/app/static-html/${lang}/${TARGET}" ]; then
        echo "[entrypoint] Static HTML: /html/${lang}/ → ${lang}/${TARGET}"
    else
        echo "[entrypoint] Warning: expected ${lang}/${TARGET} not found, using fallback"
    fi
done
# Nginx snippets: 302 redirects from /html/ (English) and /html/<lang>/ to the
# exported file. Nginx includes these before starting (see nginx.conf).
echo "return 302 /html/en/${TARGET};" > /app/static-html/.nginx-redirect.conf
echo "return 302 /html/en/${TARGET};" > /app/static-html/.nginx-redirect-en.conf
echo "return 302 /html/fr/${TARGET};" > /app/static-html/.nginx-redirect-fr.conf

# Nginx snippet: serve /app/static/ from THIS module's static folder, on disk.
# The deck references its media by URL (/app/static/media/...) rather than
# inlining them in base64. Serving them here, and not by proxying Streamlit,
# keeps the images visible in static-only mode — and keeps the container
# independent of the CDN once the image is built.
echo "alias /app/${FOLDER}/static/;" > /app/static-html/.nginx-media.conf

# --- Start services based on mode ---

case "$MODE" in
    static-only)
        echo "[entrypoint] Starting Nginx (static-only)..."
        exec nginx -g "daemon off;"
        ;;
    streamlit-only)
        echo "[entrypoint] Starting Streamlit (no Nginx)..."
        exec uv run streamlit run book.py \
            --server.port=8501 --server.address=0.0.0.0
        ;;
    dual|*)
        echo "[entrypoint] Starting Nginx + Streamlit (dual mode)..."
        # Nginx in background, Streamlit as PID 1 (receives signals)
        nginx
        exec uv run streamlit run book.py \
            --server.port=8501 --server.address=0.0.0.0
        ;;
esac
