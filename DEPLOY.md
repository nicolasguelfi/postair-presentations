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
| postair-survey | `mcgto0uw68er5cmcy61z5853` | postair-survey.streamtex.org | `modules/postair_survey` |
| postair-debates | `o655voa4o0r1gw9k1lhkujtg` | postair-debates.streamtex.org | `modules/postair_debates` |
| postair-genai | `ki72ol1fqgno2g1rpi0t2m7o` | postair-genai.streamtex.org | `modules/postair_genai` |
| postair-collection | `g5hnjmauge8443965yywvijs` | postair-collection.streamtex.org | `modules/postair_collection` |
| postair-guidelines | `cx1yh8ef3kyg1uf50m1w0wmi` | postair-guidelines.streamtex.org | `modules/postair_guidelines` |
| postair-handsup | `kjl03arps9ma13llrbtx8403` | postair-handsup.streamtex.org | `modules/postair_handsup` |

Runtime env per app: `FOLDER`, `STX_SERVE_MODE` (dual).

### Export PDF — LOCAL seulement (décision NG 2026-08-24)

Le bouton PDF du panneau « Download as… » exige playwright **et** son
Chromium. Les deux restent sur le poste de l'orateur : `playwright` vit dans
le groupe `dev` de `pyproject.toml`, que le `uv sync --no-dev` du Dockerfile
ignore, et aucune couche navigateur n'entre dans l'image. Les decks en ligne
gardent leur export HTML statique sous `/html/`.

Ce que coûterait l'activation en production, si la question revient :
environ **+350 à 450 Mo par image** (Chromium ~190 Mo + bibliothèques
système de la base slim), sur des images déjà à ~600 Mo — à peser contre
l'historique du serveur de build (`exit 255` en août sur builds parallèles).
Le geste serait d'ajouter après les dépendances :

```dockerfile
RUN uv sync --group dev && uv run playwright install --with-deps chromium
```

Sans playwright, rien ne casse : `PdfConfig` reste importable et
`_is_pdf_available()` renvoie simplement `False` — le format n'est pas
proposé (vérifié).

## Deploy / update — `main` IS production

**Pushing to `main` deploys automatically** via
`.github/workflows/hetzner-deploy.yml`: it waits for the required streamtex
version on PyPI (`.stx-version`), detects which modules changed, and triggers
only the affected Coolify services (all of them when a shared file changes).
Builds go in batches of 4 with a 300 s pause — the cax21 freezes beyond that.

Required GitHub secret: `COOLIFY_API_TOKEN` (already set).

**Working rule**: develop and validate locally, commit on a work branch, and
merge/push to `main` only when the version should go live.

```bash
# local validation before any push to main
uv run --with ruff ruff check postair_pack modules
cd modules/postair_opening && uv run streamlit run book.py
```

Manual deploy (bypass, e.g. redeploy without a code change): Actions tab →
"Deploy to Hetzner" → Run workflow, or directly:

```bash
TOKEN=$(grep '^COOLIFY_API_TOKEN=' .stx-deploy.env | cut -d= -f2-)
URL=$(grep '^COOLIFY_URL=' .stx-deploy.env | cut -d= -f2-)
curl -s "$URL/api/v1/deploy?uuid=<APP_UUID>" -H "Authorization: Bearer $TOKEN"
```

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
