"""postair_opening — AI Day opening deck (Welcome · Survey · Results · Discussion · Break).

Pilot module of the POSTAIR presentation set. See _project/plans/plan-postair_opening.md.
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
        blocks.bck_wait_loop,         # looping video, full window, no information
        blocks.bck_welcome_title,     # title + Medio + hero image
        blocks.bck_faculty_fstm,      # AI in FSTM — 1 faculté = 1 slide (NG 2026-08-13)
        blocks.bck_faculty_fdef,      # AI in FDEF
        blocks.bck_faculty_fhse,      # AI in FHSE + la réserve d'honnêteté
        blocks.bck_already_usage,     # 94 % — un chiffre = une slide
        blocks.bck_already_productivity,  # −40 % temps · +18 % qualité
        blocks.bck_already_detectors,  # 61 % non-natifs lus « IA »
        blocks.bck_already_skills,    # 68 % « vital » + la ligne long-wave
        blocks.bck_welcome_agenda,    # before the break, the break, after it
        blocks.bck_axes_radar,        # the fairground wheel: which postures will you win
        blocks.bck_axes_registers,    # Knowing / Acting / Becoming (3 sub-slides)
        blocks.bck_axes_company,      # the nine axes again, in the objects family
        # ── Survey ──────────────────────────────────────────────────
        # Reading a radar and the six archetypes now come BEFORE the survey
        # (NG 2026-08-03): the room understands what it is about to receive
        # while it answers, and whoever finishes early has the archetype
        # descriptions to read instead of a neighbour to talk to.
        blocks.bck_survey_poster,     # opens the survey part, one full-frame image
        blocks.bck_survey_howto,      # how to answer — five properties, nothing else
        blocks.bck_results_archetypes,   # six reference archetypes, not six boxes
        blocks.bck_results_radar_howto,  # example radar + the four posture codes
        blocks.bck_survey_troubleshooting,  # what to do when something goes wrong
        blocks.bck_survey_join,       # QR + giant code, the day chosen by the speaker
        blocks.bck_survey_live,       # operator button → live monitoring
        blocks.bck_survey_results,    # operator button → results presentation
        # ── Results ─────────────────────────────────────────────────
        blocks.bck_results_room,      # operator button → the room's own results
        blocks.bck_results_meaning,   # a cohort is not a bloc
        # ── Discussion ──────────────────────────────────────────────
        blocks.bck_disc_method,       # the three rules of the debate
        blocks.bck_disc_debates_link,  # hand-over to the debates deck, which closes the morning
        # ── Appendix ────────────────────────────────────────────────
        blocks.bck_refs_bibliography,  # never presented; opened when a figure is challenged
    ],
    toc_config=toc,
    marker_config=marker_config,
    # La bibliographie se charge PAR ``st_book``, jamais avant lui : il vide le
    # registre au début de sa construction, et tout ce qui aurait été chargé
    # plus tôt disparaîtrait sans un mot — chaque référence deviendrait alors
    # une clé inconnue. Règle NG (2026-08-03) : toute référence d'une
    # présentation passe par le mécanisme BibTeX.
    bib_sources=bib_sources(),
    bib_config=BIB_CONFIG,
    paginate=True,
    view_modes=[ViewMode.PAGINATED],
    banner=BannerConfig.hidden(),
    page_width=100,
    zoom=100,
    # Auditorium base: 30pt body base ⇒ bullets ≈60pt, slide titles ≈80pt,
    # heroes ≈120pt (all DS tokens follow via var(--stx-scale-K)).
    scale=SCALE,  # base amphi 30pt + rétrécissements mobiles renforcés (postair_display)
    doc_version=_doc_version,
)
