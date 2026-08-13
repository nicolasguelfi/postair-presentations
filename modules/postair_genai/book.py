"""postair_genai — AI Day afternoon opener (Introduction to AI & Generative AI, 30').

Sixth document of the POSTAIR set, first slot after the break. See
_project/plans/plan-postair_genai.md — the plan ↔ block mapping is one to one
(G1…G12), plus the References appendix.
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
    page_title="AI DAY — GenAI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="auto",
)

sts.theme = dark

set_presentation_config(PresentationConfig(
    title="AI DAY — Introduction to AI & Generative AI",
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
        blocks.bck_genai_title,          # G1  · hero + the promise
        blocks.bck_genai_pocket,         # G2  · you have used AI for years
        blocks.bck_genai_timeline,       # G3  · seventy years in one frieze
        blocks.bck_genai_prediction,     # G4  · THE pedagogical slide: predict
        blocks.bck_genai_scale,          # G5  · data + compute + energy, emergence
        blocks.bck_genai_capabilities,   # G6  · seven capabilities, agents in amber
        blocks.bck_genai_augment_medical,   # G6b · augmentation: 85 % vs 20 %
        blocks.bck_genai_augment_twist,     # G6c · the tool alone is not enough
        blocks.bck_genai_augment_justice,   # G6d · justice 1/2 : the case file
        blocks.bck_genai_augment_justice_lab,  # G6e · justice 2/2 : in the lab
        blocks.bck_genai_hallucinations,  # G7 · the fabricated case, projected
        # G8, découpé en quatre (NG 2026-08-11) : un message fort, une image
        # forte, un texte en gros — jamais quatre revers sur une slide.
        blocks.bck_genai_limit_bias,     # G8a · bias in, bias out
        blocks.bck_genai_limit_control,  # G8b · who controls the models
        blocks.bck_genai_limit_data,     # G8c · your data is the raw material
        blocks.bck_genai_limit_brain,    # G8d · the brain is a muscle
        # G9, découpé en deux : le tuteur généreux, puis l'examen humain.
        blocks.bck_genai_studies_tutor,  # G9a · the tireless tutor
        blocks.bck_genai_studies_exam,   # G9b · the exam stays human
        blocks.bck_genai_careers,        # G10 · transformation, not disappearance
        blocks.bck_genai_future_pm,      # G10b · project manager of your assistants
        blocks.bck_genai_actor,          # G11 · the loop back to the posture
        blocks.bck_genai_takeaways,      # G12 · four cards to photograph
        blocks.bck_refs_bibliography,    # never presented; opened when challenged
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
