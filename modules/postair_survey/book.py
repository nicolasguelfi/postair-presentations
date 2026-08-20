"""postair_survey — AI Day SUMVADIS tool deck (Getting started · The screens).

Né du chantier ss12 (NG 2026-08-14) : les parties Axes / Survey / Results du
deck d'ouverture deviennent ce document autonome, augmenté des captures
d'écran RÉELLES du parcours participant (catalogue gelé par
_project/tools/build_survey_captures.py, facette mobile — décision Q14 : le
deck projette ce que la salle tient en main).
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
# fichier qu'il trouve sur le disque : mascottes et captures d'écran pèseraient
# des Mo de base64 dans la page, renvoyés à chaque rerun. Les octets vivent
# donc sous `static/media/`, que les sources statiques ci-dessus ne sondent
# pas — l'URI retombe ici et sort en URL relative, servie par le service
# statique de Streamlit (`/app/static/media/…`), donc par le conteneur.
# Matérialisation : `_project/tools/sync_media.py`.
stx.configure_image_path("app/static/media")

st.set_page_config(
    page_title="AI DAY — The SUMVADIS Tool",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="auto",
)

sts.theme = dark

set_presentation_config(PresentationConfig(
    title="The SUMVADIS Tool — measure your posture",
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
# iteration, block names do not.
st_book(
    [
        # ── Part 0 · Contexts (NG 2026-08-20) — un cadre d'usage par slide ──
        blocks.bck_context_welcome_week,  # cadre académique : logo uni.lu + le contrat
        blocks.bck_context_generic,       # tous les autres cadres : wordmark sumvadis
        # ── Part 1 · Getting started ────────────────────────────────
        blocks.bck_axes_radar,        # the fairground wheel — TOC anchor « Getting started »
        blocks.bck_axes_registers,    # the nine axes, register by register
        blocks.bck_survey_poster,     # the survey part opens on one image
        blocks.bck_survey_instrument,  # 3 questions × 18 postures — l'idée de l'instrument
        blocks.bck_screens_first,     # captures 01, 02 — code of the day, welcome
        blocks.bck_screens_consent,   # capture 03 — consent, nothing personal
        blocks.bck_screens_statement,  # capture 04 — a statement, six levels + les 3 règles
        blocks.bck_survey_troubleshooting,  # before you start
        blocks.bck_survey_join,       # QR + code of the day
        # ── Part 2 · The screens ────────────────────────────────────
        blocks.bck_screens_poster,    # TOC anchor « The screens » — the personal radar, full frame
        blocks.bck_survey_live,       # live monitoring while the room answers
        blocks.bck_screens_answering,  # captures 05, 06 — progress and send
        blocks.bck_results_archetypes,  # the six archetypes
        blocks.bck_results_radar_howto,  # how to read a posture radar
        blocks.bck_screens_personal,  # captures 07, 08, 09, 16 — the personal report
        blocks.bck_screens_explore,   # captures 11, 12, 14, 15, 10 — exploring the report
        blocks.bck_screens_figures,   # captures 18, 19 — the great figures pages
        blocks.bck_survey_results,    # open the room's results (operator buttons)
        blocks.bck_results_room,      # the room's results — commentary
        blocks.bck_screens_admin,     # régie (20-22) + les 7 vues du diaporama /present
        #                             # (Q15) — captures desktop gelées le 2026-08-14
        blocks.bck_results_meaning,   # what the results say about us
        blocks.bck_next_module,       # chaîne du jour — gros bouton vers le deck suivant
        # ── Appendix ────────────────────────────────────────────────
        blocks.bck_refs_bibliography,  # never presented; opened when a claim is challenged
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
