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

# Les médias sont SERVIS, jamais inlinés. `st_image` encode en base64 tout
# fichier qu'il trouve sur le disque : la planche des 36 mascottes pèserait
# ~2,1 Mo de base64 dans la page, renvoyés à chaque rerun. Les octets vivent
# donc sous `static/media/`, que les sources statiques ci-dessus ne sondent
# pas — l'URI retombe ici et sort en URL relative, servie par le service
# statique de Streamlit (`/app/static/media/…`), donc par le conteneur.
# Matérialisation : `_project/tools/sync_media.py`.
stx.configure_image_path("app/static/media")

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
    # Auditorium rule: a slide must fill the screen. The library parks a
    # marker 80 px below the top by default (room for a header), which
    # pushed every section reached by scrolling — i.e. every sub-slide
    # after the first of a block — out of the viewport at the bottom.
    # 0 = the slide title sits flush at the top. Needs streamtex >= 0.7.22.
    scroll_offset=0,
)

# Reading order IS this list — it is the single source of truth for the deck.
# No slide numbers anywhere in the code: numbering shifts on every design
# iteration, block names do not. The plan ↔ block mapping lives in
# _project/plans/plan-postair_opening.md.
st_book(
    [
        # ── Welcome ─────────────────────────────────────────────────
        blocks.bck_wait_loop,         # looping video, no information revealed
        blocks.bck_welcome_title,     # title + Medio + hero image
        blocks.bck_welcome_agenda,    # the nine sessions, break accented
        blocks.bck_axes_radar,        # empty radar, "?" at the centre
        blocks.bck_axes_registers,    # Knowing / Acting / Becoming (3 sub-slides)
        blocks.bck_axes_company,      # both mascot families, film when it exists
        # ── Survey ──────────────────────────────────────────────────
        blocks.bck_survey_poster,     # opens the survey part, one full-frame image
        blocks.bck_survey_howto,      # how to answer — deliberately before the join
        blocks.bck_survey_join,       # QR + giant code, one sub-slide per day
        blocks.bck_survey_live,       # operator button → live monitoring
        blocks.bck_survey_results,    # operator button → results presentation
        # ── Results ─────────────────────────────────────────────────
        blocks.bck_results_radar_howto,  # example radar + the four posture codes
        blocks.bck_results_archetypes,   # six reference points, not six boxes
        blocks.bck_results_room,      # operator button → the room's own results
        blocks.bck_results_meaning,   # a cohort is not a bloc
        # ── Discussion ──────────────────────────────────────────────
        blocks.bck_disc_method,       # the three rules of the debate
        blocks.bck_disc_debates_link,  # hand-over to the debates deck
        blocks.bck_disc_wrapup,       # no consensus, and that is normal
        # ── Break ───────────────────────────────────────────────────
        blocks.bck_break_countdown,   # live countdown + the whole company
        blocks.bck_break_rewelcome,   # what the second half holds
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
