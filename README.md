# POSTAIR presentations — AI Day (University of Luxembourg)

StreamTeX presentation set for the **AI Day** conference (Welcome Week 2026,
3 hours, 1500 first-year students): postures facing the AI revolution
(POSTAIR survey), introduction to generative AI, studying with Mistral
agents, and the UL AI guidelines.

## Structure

- `postair_pack/` — local design pack: `postair_dark` design system (navy
  canvas + papercut graphic line + Pixar mascots), slide components
  (`axis_stack`), kit `postair-slides`.
- `modules/postair_opening/` — pilot deck: Welcome · Survey · Results ·
  Discussion · Break (110').
- `modules/shared-blocks/` — mascot assets (36 WebP + videos), POSTAIR data
  loader, palette widgets.
- `Dockerfile` / `entrypoint.sh` / `nginx.conf` — dual-mode deployment
  (see `DEPLOY.md`).

## Run locally

```bash
uv sync
cd modules/postair_opening && uv run streamlit run book.py
# open http://127.0.0.1:8501 — navigate with PageDown/PageUp
```

## Deployed

- https://postair-opening.streamtex.org (Streamlit + static fallback on `/html/`)

Mascots and generated images are 100 % AI-generated (mascoties studio /
gpt-image-1). Survey engine: [sumvadis](https://app.sumvadis.ai).
