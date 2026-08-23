"""postair_handsup — AI Day rescue deck (the survey, by show of hands).

Né du plan-postair_handsup v2 (NG 2026-08-23) : si le système sumvadis tombe
en séance, le sondage se fait quand même — axe par axe, à main levée. Un axe
= trois pages : les 3 énoncés de chaque pôle, la synthèse de chaque pôle,
la slide de vote (l'échelle, identique pour les neuf axes).

Tous les textes viennent du gel ``static/data/content.json``, généré par
``_project/tools/build_handsup_content.py`` depuis le questionnaire du hub
``ai-social-profiles`` — rien n'est écrit à la main, une correction arrive
par régénération.
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

# Static resolution: module first, shared assets second.
stx.set_static_sources([
    str(_MODULE_DIR / "static"),
    str(_MODULE_DIR.parent / "shared-blocks" / "static"),
])

# Les médias sont SERVIS, jamais inlinés (règle du dépôt) — ce deck n'a que
# ses illustrations versionnées, mais le chemin reste configuré pour que
# toute image managée sorte en URL relative, jamais en base64.
stx.configure_image_path("app/static/media")

st.set_page_config(
    page_title="AI DAY — By Show of Hands",
    page_icon="🙋",
    layout="wide",
    initial_sidebar_state="auto",
)

sts.theme = dark

set_presentation_config(PresentationConfig(
    title="The survey, by show of hands",
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
    # Auditorium rule: a slide must fill the screen (scroll_offset=0, ≥ 0.7.22).
    scroll_offset=0,
)

# Reading order IS this list. Un axe = trois lignes, dans l'ordre HORAIRE du
# radar (champ `order` du questionnaire) : les énoncés, la synthèse
# (questionnaire v1.10.0 du hub), puis les trois volets de vote
# GÉNÉRIQUES (support / oppose / abstain — mêmes slides pour chaque axe).
st_book(
    [
        blocks.bck_title,             # titre PAPERCUT + sélecteur de langue + ancrage
        blocks.bck_axis_trust_questions,
        blocks.bck_axis_trust_synthetic,
        blocks.bck_axis_trust_support,
        blocks.bck_axis_trust_oppose,
        blocks.bck_axis_trust_abstain,
        blocks.bck_axis_optimism_questions,
        blocks.bck_axis_optimism_synthetic,
        blocks.bck_axis_optimism_support,
        blocks.bck_axis_optimism_oppose,
        blocks.bck_axis_optimism_abstain,
        blocks.bck_axis_rationality_questions,
        blocks.bck_axis_rationality_synthetic,
        blocks.bck_axis_rationality_support,
        blocks.bck_axis_rationality_oppose,
        blocks.bck_axis_rationality_abstain,
        blocks.bck_axis_speed_questions,
        blocks.bck_axis_speed_synthetic,
        blocks.bck_axis_speed_support,
        blocks.bck_axis_speed_oppose,
        blocks.bck_axis_speed_abstain,
        blocks.bck_axis_openness_questions,
        blocks.bck_axis_openness_synthetic,
        blocks.bck_axis_openness_support,
        blocks.bck_axis_openness_oppose,
        blocks.bck_axis_openness_abstain,
        blocks.bck_axis_freedom_questions,
        blocks.bck_axis_freedom_synthetic,
        blocks.bck_axis_freedom_support,
        blocks.bck_axis_freedom_oppose,
        blocks.bck_axis_freedom_abstain,
        blocks.bck_axis_centralisation_questions,
        blocks.bck_axis_centralisation_synthetic,
        blocks.bck_axis_centralisation_support,
        blocks.bck_axis_centralisation_oppose,
        blocks.bck_axis_centralisation_abstain,
        blocks.bck_axis_individualism_questions,
        blocks.bck_axis_individualism_synthetic,
        blocks.bck_axis_individualism_support,
        blocks.bck_axis_individualism_oppose,
        blocks.bck_axis_individualism_abstain,
        blocks.bck_axis_transhumanism_questions,
        blocks.bck_axis_transhumanism_synthetic,
        blocks.bck_axis_transhumanism_support,
        blocks.bck_axis_transhumanism_oppose,
        blocks.bck_axis_transhumanism_abstain,
        blocks.bck_next_module,       # chaîne du jour — gros bouton vers le deck suivant
        # ── Appendix ────────────────────────────────────────────────
        blocks.bck_refs_bibliography,  # never presented; opened when a claim is challenged
    ],
    toc_config=toc,
    marker_config=marker_config,
    # La bibliographie se charge PAR ``st_book``, jamais avant lui (règle NG
    # 2026-08-03) : il vide le registre au début de sa construction.
    bib_sources=bib_sources(),
    bib_config=BIB_CONFIG,
    paginate=True,
    view_modes=[ViewMode.PAGINATED],
    banner=BannerConfig.hidden(),
    page_width=100,
    zoom=100,
    scale=SCALE,  # base amphi 30pt + rétrécissements mobiles (postair_display)
    doc_version=_doc_version,
)
