"""postair_waves — the seventeen waves of revolutions (a navigable bank).

Eighth document of the POSTAIR set. See _project/plans/plan-postair_waves.md.

Reading order: the promise, the frame (Kuhn/Perez, the substitution protocol),
the three grids at a glance — then the seventeen waves, one visible stop each,
their depth (the validated quadriptych, the figures with their CDN video
player, the lesson) behind hidden markers. Like debates, this is a bank, not a
talk: the speaker opens two or three waves and leaves the rest closed — which
is why search and the sidebar matter more than the reading order.
"""

import setup  # noqa: F401  — MUST run first (sys.path: module dir + shared-blocks)

import tomllib
from pathlib import Path

import blocks
from postair_lang import current_lang
import streamlit as st
from postair_display import SCALE
import streamtex as stx
import streamtex.styles as sts
from custom.refs import CONFIG as BIB_CONFIG
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

# Static resolution: module first (the content manifest, the wave images),
# shared assets (mascots) second.
stx.set_static_sources([
    str(_MODULE_DIR / "static"),
    str(_MODULE_DIR.parent / "shared-blocks" / "static"),
])

# Les médias sont SERVIS, jamais inlinés (même règle et même raison que dans
# les autres books : `st_image` encoderait en base64 tout fichier trouvé sur
# disque). Matérialisation : `_project/tools/sync_media.py`.
stx.configure_image_path("app/static/media")

st.set_page_config(
    page_title="AI DAY — The seventeen waves",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="auto",
)

sts.theme = dark

set_presentation_config(PresentationConfig(
    title="AI DAY — The seventeen waves",
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

# Même régime de navigation que debates : le deck est une banque, l'orateur y
# cherche une vague par son nom pendant que la salle attend.
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
    # Auditorium rule (streamtex >= 0.7.22): sub-slides are reached by
    # scrolling — the default 80 px offset would push them out of the viewport.
    scroll_offset=0,
)

# Export PDF — même choix que les autres books du jeu : paysage A4, marges
# minces, `print_background` (sans lui Chromium imprime un fond blanc).
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
        blocks.bck_welcome_title,       # the promise: 16 crises overcome, 1 open
        blocks.bck_intro_approche,      # Kuhn · Perez · every stance has an ancestor
        blocks.bck_intro_substitution,  # same 54 questions, the era's term
        # ── The illustrated gallery — clickable object cards (2×2) ──
        # ⚠ MIROIR : _WAVE_PAGE_FIRST (custom/render.py) = l'index de page du
        # premier bloc de vague ci-dessous. Toute insertion avant les vagues
        # doit le mettre à jour.
        blocks.bck_waves_grid_origins,      # writing → the press (1-4)
        blocks.bck_waves_grid_machines,     # telescope → vaccine (5-8)
        blocks.bck_waves_grid_power,        # dynamo → atom (9-12)
        blocks.bck_waves_grid_information,  # computer → Web (13-16)
        blocks.bck_waves_grid_ai,           # the 17th, alone and large
        # ── The chronological walk — one stop per wave ──────────────
        # Chaque bloc = le quadriptyque VALIDÉ (25-26/08/2026) + les figures
        # au portrait-lecteur (vidéos au CDN) + la leçon, en marqueurs cachés.
        blocks.bck_wave_writing,
        blocks.bck_wave_printing_china,
        blocks.bck_wave_medieval_crafts,
        blocks.bck_wave_printing_press,
        blocks.bck_wave_new_science,
        blocks.bck_wave_industrialisation,
        blocks.bck_wave_rail_telegraph,
        blocks.bck_wave_germ_theory,
        blocks.bck_wave_electricity,
        blocks.bck_wave_motor_aviation,
        blocks.bck_wave_mass_media,
        blocks.bck_wave_atom,
        blocks.bck_wave_computer_cybernetics,
        blocks.bck_wave_synthetic_chemistry,
        blocks.bck_wave_genetic_engineering,
        blocks.bck_wave_internet_web,
        blocks.bck_wave_ai,             # ends on the half-written whiteboard
        # ── Closing ─────────────────────────────────────────────────
        blocks.bck_wrapup,              # 16 opened · 16 overcome · the 17th is yours
        blocks.bck_next_module,         # chaîne du jour — gros bouton
        blocks.bck_references,          # never presented; opened when challenged
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
    scale=SCALE,  # base amphi 30pt (postair_display)
    doc_version=_doc_version,
    pdf_config=PDF,
    # La bibliographie se charge PAR ``st_book``, jamais avant lui. Le .bib
    # est GELÉ par build_waves_content.py — même contrat que content.json.
    bib_sources=bib_sources(),
    bib_config=BIB_CONFIG,
)
