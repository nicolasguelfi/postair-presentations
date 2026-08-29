FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHERUSAGESTATS=false \
    UV_LINK_MODE=copy

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl nginx-light \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Cache-bust: Coolify passes SOURCE_COMMIT automatically.
ARG SOURCE_COMMIT=unknown

# Install dependencies.
# postair_pack is a LOCAL pack resolved via [tool.uv.sources] (path) — it is
# copied before uv sync, so sources stay ENABLED (unlike ai4se6d, which used
# --no-sources: our only source entry is the in-repo pack, streamtex itself
# comes from PyPI). --upgrade-package streamtex still forces latest PyPI.
COPY .stx-version pyproject.toml uv.lock ./
COPY postair_pack/ ./postair_pack/
RUN uv sync --no-dev --upgrade-package streamtex && \
    uv pip install rich jinja2

# Pas de Chromium ici (décision NG 2026-08-24) : l'export PDF est une
# fonction de l'ORATEUR, en local. `uv sync --no-dev` ci-dessus laisse donc
# playwright (groupe `dev` de pyproject.toml) hors de l'image — ~400 Mo
# épargnés par service. Les decks en ligne gardent leur export HTML statique
# sous `/html/`. Pour l'activer un jour : voir DEPLOY.md.

# Fail the build if the installed streamtex version is older than required.
RUN REQUIRED=$(cat .stx-version | tr -d '[:space:]') && \
    INSTALLED=$(uv run python -c "from importlib.metadata import version; print(version('streamtex'))") && \
    echo "streamtex: required >= ${REQUIRED}, installed ${INSTALLED}" && \
    uv run python -c "import sys; \
r = tuple(int(x) for x in '${REQUIRED}'.split('.')); \
i = tuple(int(x) for x in '${INSTALLED}'.split('.')); \
sys.exit(1) if i < r else sys.exit(0)" || \
    { echo "ERROR: streamtex ${INSTALLED} < ${REQUIRED} — aborting build"; exit 1; }

# Copy all modules (shared-blocks included)
COPY modules/ ./modules/

# Materialise the media INSIDE the image, from the upstream catalogues.
#
# The container must be complete and autonomous: during the session it makes no
# call to the CDN. But none of these bytes live in git — they arrive here by the
# tool, and reload by emptying the folder. The URLs are content-addressed, so a
# file that is present IS up to date: no revalidation, no staleness.
#
# Images only (~39 MB): the 51 presentation videos weigh 12 MB each, are opened
# two or three times in a session, and would add 612 MB to the image for a
# momentary interaction. They stay streamed from the CDN.
#
# The catalogue it reads is the FROZEN one, committed with the modules — a few
# kilobytes of content-addressed URLs. That is what makes this step work in CI:
# the build has no access to the private upstream repos, only to the network.
# Regenerate it on the author's machine with `sync_media.py --freeze`.
#
# The two moderator mascots come from the CDN like the rest since catalogue
# v2.2.0 (crew section, 2026-08-02) — the old "no CDN entry" exception is gone;
# a CI build materialises all 38 mascots from media-catalogue.json.
COPY _project/tools/ ./_project/tools/
RUN uv run python _project/tools/sync_media.py

# Nginx configuration for dual-mode (Streamlit + static HTML)
COPY nginx.conf /etc/nginx/nginx.conf

# Entrypoint script (supports dual / static-only / streamlit-only modes)
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# FOLDER is set at runtime by Coolify env var
ENV FOLDER="modules/postair_opening"

# Default nginx redirect snippet (entrypoint regenerates at runtime)
RUN mkdir -p /app/static-html && \
    echo 'return 302 /html/;' > /app/static-html/.nginx-redirect.conf

# Pre-warm the page cache for every module so the first visitor loads instantly
# — ONCE PER LANGUAGE: since streamtex 0.7.26 the paginated cache is keyed by
# block_kwargs ({"lang": …} gets its own TOC/markers, page_cache-<fp8>.json).
RUN for dir in modules/postair_*/; do \
        for lang in en fr; do \
            echo "Warming up cache ($lang) for $dir ..." && \
            (cd "$dir" && STX_LANG=$lang uv run stx cache warmup .) || true; \
        done; \
    done

# Pre-generate static HTML for every module, ONE EXPORT PER LANGUAGE
# (plan-i18n D3, 2026-08-28) : /html/en/ and /html/fr/ — the public reads
# the static export, and a Streamlit widget never survives an export, so the
# language must be a build parameter (STX_LANG, read by postair_lang and, since
# streamtex 0.7.26, by the exporter itself for <html lang>).
RUN for dir in modules/postair_*/; do \
        for lang in en fr; do \
            echo "Exporting HTML ($lang) for $dir ..." && \
            (cd "$dir" && STX_LANG=$lang uv run stx export html --output /app/static-html/$lang/ .) || true; \
        done; \
    done

# STX_SERVE_MODE controls which services start (set at runtime by Coolify)
ENV STX_SERVE_MODE="dual"

EXPOSE 80 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health 2>/dev/null \
    || curl -fsL http://localhost:80/html/ -o /dev/null

ENTRYPOINT ["/app/entrypoint.sh"]
