"""postair_guidelines — the last two slots of the AI Day (UL guidelines 15'+3' AI Act + Closing 5').

Seventh document of the POSTAIR set. See _project/plans/plan-postair_guidelines.md —
the plan ↔ block mapping is one to one (U1…U8, C1…C3), plus the References appendix.
Registre : descriptif et opérationnel — on explique les règles du document officiel
(I²TL v1.0, 2026-02-16), on ne les commente pas.
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
    AIImageConfig,
    BannerConfig,
    MarkerConfig,
    NumberingMode,
    PdfConfig,
    PresentationConfig,
    SlideBreakConfig,
    SlideBreakMode,
    TOCConfig,
    ViewMode,
    set_ai_image_config,
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

# Les médias sont SERVIS, jamais inlinés (règle du dépôt) : les octets de
# mascottes vivent sous `static/media/`, matérialisés par sync_media.py, et
# sortent en URL relative servie par le conteneur.
stx.configure_image_path("app/static/media")

st.set_page_config(
    page_title="AI DAY — Guidelines",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed",  # NG 2026-09-03 : lancement panneau FERMÉ (la projection dispose de toute la largeur)
)

sts.theme = dark

set_presentation_config(PresentationConfig(
    title="AI DAY — The UL AI Guidelines",
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

set_ai_image_config(AIImageConfig(
    provider="openai",
    default_size="1536x1024",
    output_dir="static/images/ai",
    auto_generate=False,
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

# Reading order IS this list — it is the single source of truth for the deck.
# No slide numbers anywhere in the code: numbering shifts on every design
# iteration, block names do not.
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
        blocks.bck_guide_title,        # U1 · the official document, sealed
        blocks.bck_guide_default,      # U2 · by default: permitted — THE rule
        blocks.bck_guide_disclosure,   # U3 · say it: five elements
        blocks.bck_guide_risk,         # U4 · the three levels (the ONLY tricolour)
        blocks.bck_guide_redlines,     # U5 · the red lines, with Guardo
        blocks.bck_guide_tools,        # U6 · the UL bubble vs the open cloud
        blocks.bck_guide_suspicion,    # U7 · balanced scale — detection is not proof
        blocks.bck_guide_checklist,    # U8 · the final test, verbatim
        blocks.bck_guide_aiact,        # U9a · the AI Act — the law and its calendar
        blocks.bck_guide_aiact_you,    # U9b · the AI Act — you, concretely
        blocks.bck_close_loop,         # C1 · the four things they now have
        blocks.bck_close_next,         # C2 · the QR to the hub, what stays online
        blocks.bck_close_thanks,       # C3 · mascot family photo, applause
        blocks.bck_next_module,       # chaîne du jour — gros bouton vers le deck suivant
        blocks.bck_refs_bibliography,  # never presented; opened when challenged
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
    # Auditorium base: 30pt body base ⇒ bullets ≈60pt, slide titles ≈80pt.
    # Raccourcis de zoom du panneau (NG 2026-09-02) : « Default »
    # reste actif au démarrage (rendu inchangé) ; Zoom 90 %/80 % =
    # préréglages nommés — jamais un remède de salle (postair_display).
    presentation_profiles=postair_profiles(),
    scale=SCALE,  # base amphi 30pt + rétrécissements mobiles renforcés (postair_display)
    doc_version=_doc_version,
    pdf_config=PDF,
)
