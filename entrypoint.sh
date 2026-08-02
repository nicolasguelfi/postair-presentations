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

# Re-warm the page cache (for Streamlit fast first load)
if [ "$MODE" != "static-only" ]; then
    echo "[entrypoint] Warming up page cache..."
    uv run stx cache warmup . 2>/dev/null || true
fi

# Generate static HTML export — clean first to remove stale exports from other FOLDERs
rm -rf /app/static-html/*
echo "[entrypoint] Generating static HTML..."
uv run stx export html --output /app/static-html/ . 2>/dev/null || true

# Derive base_name: the export CLI uses the full basename of FOLDER
BASE_NAME=$(basename "${FOLDER}")
TARGET="${BASE_NAME}/${BASE_NAME}.html"

if [ -f "/app/static-html/${TARGET}" ]; then
    echo "[entrypoint] Static HTML: /html/ → ${TARGET}"
else
    echo "[entrypoint] Warning: expected ${TARGET} not found, using fallback"
fi
# Nginx snippet: 302 redirect from /html/ to the correct exported file.
# Nginx includes this before starting (see nginx.conf location = /html/).
echo "return 302 /html/${TARGET};" > /app/static-html/.nginx-redirect.conf

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
