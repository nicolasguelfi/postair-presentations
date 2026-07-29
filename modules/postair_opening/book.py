"""postair_opening — AI Day opening deck (Welcome · Survey · Results · Discussion · Break).

Pilot module of the POSTAIR presentation set. See _project/plans/plan-postair_opening.md.
"""

import setup  # noqa: F401  — MUST run first (sys.path: module dir + shared-blocks)

import tomllib
from pathlib import Path

import blocks
import streamlit as st
import streamtex as stx
import streamtex.styles as sts
from custom.themes import dark
from streamtex import (
    AIImageConfig,
    BannerConfig,
    MarkerConfig,
    NumberingMode,
    PresentationConfig,
    ScaleConfig,
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

st.set_page_config(
    page_title="AI DAY — Opening",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="auto",
)

sts.theme = dark

set_presentation_config(PresentationConfig(
    title="AI DAY — Facing the AI Revolution",
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
)

st_book(
    [
        # ── W — Welcome ─────────────────────────────────────────────
        blocks.bck_wait_loop,        # W00 waiting loop (video, no info)
        blocks.bck_welcome_title,    # W01 title + Medio + hero
        blocks.bck_axes_radar,       # W05a big radar with "?"
        blocks.bck_axes_registers,   # W05b-d Knowing / Acting / Becoming (3 slides)
        # (prototype scope — W02/W03/W04/W06, S, R, D, B blocks follow after design GATE)
    ],
    toc_config=toc,
    marker_config=marker_config,
    paginate=True,
    view_modes=[ViewMode.PAGINATED],
    banner=BannerConfig.hidden(),
    page_width=100,
    zoom=100,
    # Auditorium base: 30pt body base ⇒ bullets ≈60pt, slide titles ≈80pt,
    # heroes ≈120pt (all DS tokens follow via var(--stx-scale-K)).
    scale=ScaleConfig(base_pt_desktop=30),
    doc_version=_doc_version,
)
