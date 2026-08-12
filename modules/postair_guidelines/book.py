"""postair_guidelines — the last two slots of the AI Day (UL guidelines 15' + Closing 5').

Seventh document of the POSTAIR set. See _project/plans/plan-postair_guidelines.md —
the plan ↔ block mapping is one to one (U1…U8, C1…C3), plus the References appendix.
Registre : descriptif et opérationnel — on explique les règles du document officiel
(I²TL v1.0, 2026-02-16), on ne les commente pas.
"""

import setup  # noqa: F401  — MUST run first (sys.path: module dir + shared-blocks)

import tomllib
from pathlib import Path

import blocks
import streamlit as st
from postair_display import SCALE
import streamtex as stx
import streamtex.styles as sts
from custom.refs import CONFIG as BIB_CONFIG
from custom.refs import sources as bib_sources
from custom.themes import dark
from streamtex import (
    AIImageConfig,
    BannerConfig,
    MarkerConfig,
    NumberingMode,
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
    initial_sidebar_state="auto",
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
        blocks.bck_close_loop,         # C1 · the four things they now have
        blocks.bck_close_next,         # C2 · the QR to the hub, what stays online
        blocks.bck_close_thanks,       # C3 · mascot family photo, applause
        blocks.bck_refs_bibliography,  # never presented; opened when challenged
    ],
    toc_config=toc,
    marker_config=marker_config,
    # La bibliographie se charge PAR ``st_book``, jamais avant lui : il vide
    # le registre au début de sa construction (règle bib canonique, CLAUDE.md).
    bib_sources=bib_sources(),
    bib_config=BIB_CONFIG,
    paginate=True,
    view_modes=[ViewMode.PAGINATED],
    banner=BannerConfig.hidden(),
    page_width=100,
    zoom=100,
    # Auditorium base: 30pt body base ⇒ bullets ≈60pt, slide titles ≈80pt.
    scale=SCALE,  # base amphi 30pt + rétrécissements mobiles renforcés (postair_display)
    doc_version=_doc_version,
)
