# POSTAIR presentations — Deployment (Hetzner / Coolify)

Same mechanics as `streamtex-docs` / `ai4se6d`: **one Docker image** built from
this repo, **one Coolify service per module**, each selecting its module via the
`FOLDER` env var. Serve mode `dual` = Nginx (`/html/` static export + fallback)
+ Streamlit proxied on `/`.

## Infrastructure

- Server: Hetzner `streamtex-prod` (cax21, fsn1) — `138.199.148.59`
- Coolify: `https://coolify.streamtex.org` — project **postair** (`h13ylxrgkghvllh9znzzu1fk`)
- DNS: wildcard `*.streamtex.org` (Cloudflare, SSL full strict)
- State: `.stx-deploy.json` (versioned, no secrets) · secrets in `.stx-deploy.env` (gitignored)

## Services

| Service | UUID | Domain | FOLDER |
|---|---|---|---|
| postair-opening | `f12d9utrj67uqwjqune5t4ip` | postair-opening.streamtex.org | `modules/postair_opening` |

Runtime env per app: `FOLDER`, `STX_SERVE_MODE` (dual).

## Deploy / update

Push to `main` then trigger via API:

```bash
TOKEN=$(grep '^COOLIFY_API_TOKEN=' .stx-deploy.env | cut -d= -f2-)
URL=$(grep '^COOLIFY_URL=' .stx-deploy.env | cut -d= -f2-)
curl -s "$URL/api/v1/deploy?uuid=<APP_UUID>" -H "Authorization: Bearer $TOKEN"
```

(A GitHub Actions workflow à la ai4se6d can be added once several modules exist —
remember the cax21 rule: max 4 concurrent builds, 300 s between batches.)

## Adding a module

1. Create `modules/postair_<name>/` (book.py, setup.py, blocks/, custom/, static/).
2. The Dockerfile warms up and exports every `modules/postair_*/` automatically.
3. Create the Coolify app (POST `/api/v1/applications/public`, project/server uuids
   from `.stx-deploy.json`), set `domains`, env `FOLDER`, deploy, record in
   `.stx-deploy.json`.

## Notes

- streamlit pinned `<1.58` until streamtex ≥ 0.7.21 is on PyPI (widget-key fix f512d3f).
- No TeXLive in the image (no st_tikz in these decks) — keeps it light.
- Public URL for students = the static export `/html/` (nginx); the Streamlit mode
  is for the presenter (≈10-15 concurrent sessions per container).
