"""postair_closing — la clôture de la conférence (décision NG, planche anim1
2026-09-03 : « un module de clôture dans lequel je mettrai le slide [DLH]
ainsi que d'autres »).

v1 : slide-titre + la slide DLH (diaporama ``st_slideshow``) + Next deck.
NG y ajoutera ses slides de clôture — la liste ci-dessous est la seule
source de l'ordre.
"""

import setup  # noqa: F401  — MUST run first (sys.path: module dir + shared-blocks)

import tomllib
from pathlib import Path

import blocks
from custom.refs import config as refs_config
from custom.refs import sources as bib_sources
from postair_lang import current_lang
import streamlit as st
from postair_display import SCALE, postair_profiles
import streamtex as stx
import streamtex.styles as sts
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

# Static resolution: module first, shared assets (mascots) second.
stx.set_static_sources([
    str(_MODULE_DIR / "static"),
    str(_MODULE_DIR.parent / "shared-blocks" / "static"),
])

# Les médias sont SERVIS, jamais inlinés (règle du dépôt).
stx.configure_image_path("app/static/media")

st.set_page_config(
    page_title="AI DAY — Closing",
    page_icon="🏁",
    layout="wide",
    initial_sidebar_state="collapsed",  # NG 2026-09-03 : lancement panneau FERMÉ (la projection dispose de toute la largeur)
)

sts.theme = dark

set_presentation_config(PresentationConfig(
    title="AI DAY — Closing",
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
    # Auditorium rule: a slide must fill the screen — 0 = the slide title
    # sits flush at the top (needs streamtex >= 0.7.22).
    scroll_offset=0,
)

# Export PDF : même calibrage que les autres decks (paysage A4, marges
# minces, print_background pour le thème sombre). ⚠ le diaporama n'y montre
# que sa première image (limite CSS assumée, planche anim1).
PDF = PdfConfig(
    format="A4",
    landscape=True,
    margin_top="6mm", margin_bottom="6mm",
    margin_left="6mm", margin_right="6mm",
    print_background=True,
    content_width=100,
    theme_bg="#1A1A2E", theme_text="#F2EEE6",
)

# Reading order IS this list — it is the single source of truth for the deck.
# Les trois slides de clôture (loop, next, thanks) viennent de
# postair_guidelines (déménagement tâche 5, 2026-09-03) — la clôture du JOUR
# vit ici, pas dans le dernier deck de contenu.
st_book(
    [
        blocks.bck_closing_title,    # C1 · Closing — take the method home
        blocks.bck_close_loop,       # C2 · the four things they now have
        blocks.bck_closing_dlh,      # C3 · Digital Learning Hub (diaporama)
        blocks.bck_close_next,       # C4 · the QR to the hub, what stays online
        blocks.bck_close_thanks,     # C5 · mascot family photo, applause
        blocks.bck_next_module,      # chaîne du jour — boucle vers le suivant
    ],
    toc_config=toc,
    marker_config=marker_config,
    # La bibliographie se charge PAR ``st_book``, jamais avant lui : il vide
    # le registre au début de sa construction (règle bib canonique, CLAUDE.md).
    bib_sources=bib_sources(),
    bib_config=refs_config(),   # locale = langue projetée (0.7.26)
    # La langue projetée, passée à chaque build(lang) — plan-i18n D2.
    block_kwargs={"lang": current_lang()},
    paginate=True,
    view_modes=[ViewMode.PAGINATED],
    banner=BannerConfig.hidden(),
    page_width=100,
    zoom=100,
    presentation_profiles=postair_profiles(),
    scale=SCALE,  # base amphi 30pt (postair_display)
    doc_version=_doc_version,
    pdf_config=PDF,
)
