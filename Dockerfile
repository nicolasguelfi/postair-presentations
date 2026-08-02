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
# The two moderator mascots have no CDN entry at all and are the one exception:
# they are copied from the studio, so a CI build leaves them missing. Debt to be
# cleared by publishing them — see the note handed to the studio session.
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

# Pre-warm the page cache for every module so the first visitor loads instantly.
RUN for dir in modules/postair_*/; do \
        echo "Warming up cache for $dir ..." && \
        (cd "$dir" && uv run stx cache warmup .) || true; \
    done

# Pre-generate static HTML for every module (served by Nginx on /html/).
RUN for dir in modules/postair_*/; do \
        echo "Exporting HTML for $dir ..." && \
        (cd "$dir" && uv run stx export html --output /app/static-html/ .) || true; \
    done

# STX_SERVE_MODE controls which services start (set at runtime by Coolify)
ENV STX_SERVE_MODE="dual"

EXPOSE 80 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health 2>/dev/null \
    || curl -fsL http://localhost:80/html/ -o /dev/null

ENTRYPOINT ["/app/entrypoint.sh"]
