"""postair_debates — the debates of the nine axes (a navigable bank, not a talk).

Fifth document of the POSTAIR set. See _project/plans/plan-postair_debates.md.

The reading order below is a shelf order, not a narrative: the speaker opens
the two or three axes the survey results showed as divisive and leaves the
rest closed. That is why navigation — markers and the searchable table of
contents — matters more here than in any other document of the set.
"""

import setup  # noqa: F401  — MUST run first (sys.path: module dir + shared-blocks)

import tomllib
from pathlib import Path

import blocks
from postair_lang import current_lang
import streamlit as st
from postair_display import SCALE, postair_profiles
import streamtex as stx
import streamtex.styles as sts
from custom.refs import config as refs_config
from custom.refs import sources as bib_sources
from custom.themes import dark
from streamtex import (
    BannerConfig,
    MarkerConfig,
    NumberingMode,
    PdfConfig,
    PresentationConfig,
    SlideBreakConfig,
    SlideBreakMode,
    TOCConfig,
    ViewMode,
    set_presentation_config,
    set_slide_break_config,
    st_book,
)

_MODULE_DIR = Path(__file__).parent
if not (_MODULE_DIR / "static").exists():
    # Test harnesses (streamlit AppTest) execute the script with a temporary
    # __file__ — fall back to the working directory, which IS the module dir.
    _MODULE_DIR = Path.cwd()

try:
    _doc_version = tomllib.loads(
        (_MODULE_DIR.parent.parent / "pyproject.toml").read_text(encoding="utf-8")
    ).get("project", {}).get("version", "?")
except OSError:
    _doc_version = "?"

# Static resolution: module first (the content manifest, the portraits),
# shared assets (mascots) second.
stx.set_static_sources([
    str(_MODULE_DIR / "static"),
    str(_MODULE_DIR.parent / "shared-blocks" / "static"),
])

# Les médias sont SERVIS, jamais inlinés. `st_image` encode en base64 tout
# fichier qu'il trouve sur le disque : les 54 portraits pèseraient ~23 Mo de
# base64 dans la page, contre 2,7 Ko en URL. Les octets vivent donc sous
# `static/media/`, que les sources statiques ci-dessus ne sondent pas — l'URI
# retombe ici et sort en URL relative, servie par le service statique de
# Streamlit (`/app/static/media/…`), donc par le conteneur lui-même.
# Matérialisation : `_project/tools/sync_media.py`.
stx.configure_image_path("app/static/media")

st.set_page_config(
    page_title="AI DAY — The debates",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="auto",
)

sts.theme = dark

set_presentation_config(PresentationConfig(
    title="AI DAY — The debates of the nine axes",
    aspect_ratio="16/9",
    footer=True,
    center_content=False,
    enforce_ratio=False,
    hide_streamlit_header=False,  # keep the sidebar toggle reachable
))

set_slide_break_config(SlideBreakConfig(
    mode=SlideBreakMode.FULL,
    space="30vh",
))

# Search matters more here than anywhere else: the speaker looks for an axis
# by name, on stage, while the room waits.
toc = TOCConfig(
    numbering=NumberingMode.SIDEBAR_ONLY,
    toc_position=None,
    sidebar_max_level=2,
    search=True,
)

marker_config = MarkerConfig(
    auto_marker_on_toc=None,
    next_keys=["PageDown", "ArrowRight"],
    prev_keys=["PageUp", "ArrowLeft"],
    draggable=True,
    collapsible=True,
    # Auditorium rule: a slide must fill the screen. Every sub-slide after the
    # first of a block is reached by scrolling, and there are six of them per
    # axis here — the default 80 px offset would push each one out of the
    # viewport at the bottom. Needs streamtex >= 0.7.22.
    scroll_offset=0,
)

# Reading order IS this list. No slide numbers anywhere in the code: blocks are
# named after their axis, which is stable. The plan ↔ block mapping lives in
# _project/plans/plan-postair_debates.md.
# Export PDF (NG 2026-08-24) — le format proposé dans le panneau
# « Download as… » de la barre latérale. Paysage A4 : les slides sont
# conçues en 16/9, un portrait les rétrécirait de moitié. Marges minces et
# `print_background` pour garder les cartes colorées et les lavis du thème
# sombre — sans lui, Chromium imprime un fond blanc et les textes clairs
# deviennent illisibles. Le format n'apparaît QUE si playwright et son
# Chromium sont présents (`_is_pdf_available`) : `uv run playwright install
# chromium` en local, couche dédiée dans le Dockerfile pour le conteneur.
PDF = PdfConfig(
    format="A4",
    landscape=True,
    margin_top="6mm", margin_bottom="6mm",
    margin_left="6mm", margin_right="6mm",
    print_background=True,
    content_width=100,
    theme_bg="#1A1A2E", theme_text="#F2EEE6",
)

st_book(
    [
        # Intro en 4 temps (NG 2026-08-14, ss12-restructure) : les deux slides
        # « discussion » d'opening vivent désormais là où le débat se joue —
        # même mouvement que bck_disc_wrapup (NG 2026-08-03).
        blocks.bck_disc_method,            # 1. let's debate — the rules, for the room
        blocks.bck_disc_debates_link,      # 2. next, hands on — the process, remis (NG 2026-08-31)
        #blocks.bck_debate_method,          # a bank, not a talk — how it is used, for the speaker
        #blocks.bck_provenance,             # 3. three rules of provenance, said once
        blocks.bck_disc_results,           # open /present — where does this room split? (NG 2026-08-30)
        # ── Knowing ─────────────────────────────────────────────────
        blocks.bck_axis_trust,
        blocks.bck_axis_optimism,
        blocks.bck_axis_rationality,
        # ── Acting ──────────────────────────────────────────────────
        blocks.bck_axis_speed,
        blocks.bck_axis_openness,
        blocks.bck_axis_control,
        # ── Becoming ────────────────────────────────────────────────
        blocks.bck_axis_centralisation,
        blocks.bck_axis_altruism,
        blocks.bck_axis_transhumanism,
        blocks.bck_debate_wrapup,          # thank you — every view heard, all of them in society
        # ── Closing the morning ─────────────────────────────────────
        # Moved here from the opening deck (NG 2026-08-03). The speaker is in
        # this document when the debate ends, and closing the morning from the
        # other tab meant switching back for three slides — a stage gesture
        # with nothing behind it. The morning now ends where it is being run.
        #blocks.bck_disc_wrapup,            # no consensus, and that is normal
        blocks.bck_break_countdown,        # live countdown + the whole company
        blocks.bck_break_rewelcome,        # what the second half holds
        blocks.bck_next_module,       # chaîne du jour — gros bouton vers le deck suivant
        blocks.bck_references,             # never presented; opened when challenged
    ],
    toc_config=toc,
    marker_config=marker_config,
    # La langue projetée, passée à chaque build(lang) — plan-i18n D2.
    block_kwargs={"lang": current_lang()},
    paginate=True,
    view_modes=[ViewMode.PAGINATED],
    banner=BannerConfig.hidden(),
    page_width=100,
    zoom=100,
    # Auditorium base: 30pt body base ⇒ bullets ≈60pt, slide titles ≈80pt.
    # Profils de secours de salle (planche ecran2 profils=p1, NG
    # 2026-09-02) : « Default » reste actif au démarrage (rendu
    # inchangé) ; Laptop/Salle étroite = zoom global en un geste.
    presentation_profiles=postair_profiles(),
    scale=SCALE,  # base amphi 30pt + rétrécissements mobiles renforcés (postair_display)
    doc_version=_doc_version,
    pdf_config=PDF,
    # La bibliographie se charge PAR ``st_book``, jamais avant lui : il vide le
    # registre au début de sa construction. Le .bib est GELÉ par
    # build_debates_content.py — même contrat que content.json.
    bib_sources=bib_sources(),
    bib_config=refs_config(),   # locale = langue projetée (0.7.26)
)
