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
from postair_lang import current_lang
import streamlit as st
from postair_display import SCALE
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
# (questionnaire v1.10.0 du hub) : VOTE PAR PÔLE — chaque pôle a sa
# slide de synthèse puis les TROIS MÊMES blocs de vote génériques
# (bck_vote_*, marqueurs cachés — une slide répétée = un bloc, listé N fois).
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
        blocks.bck_title,             # titre PAPERCUT + sélecteur de langue + ancrage
        # blocks.bck_axis_trust_questions,  # exclu (NG 2026-08-24) — les 6 énoncés, à décommenter au besoin
        blocks.bck_axis_trust_accel_synthesis,
        blocks.bck_vote_support,
        blocks.bck_vote_oppose,
        blocks.bck_vote_abstain,
        blocks.bck_axis_trust_decel_synthesis,
        blocks.bck_vote_support,
        blocks.bck_vote_oppose,
        blocks.bck_vote_abstain,
        # blocks.bck_axis_optimism_questions,  # exclu (NG 2026-08-24) — les 6 énoncés, à décommenter au besoin
        blocks.bck_axis_optimism_accel_synthesis,
        blocks.bck_vote_support,
        blocks.bck_vote_oppose,
        blocks.bck_vote_abstain,
        blocks.bck_axis_optimism_decel_synthesis,
        blocks.bck_vote_support,
        blocks.bck_vote_oppose,
        blocks.bck_vote_abstain,
        # blocks.bck_axis_rationality_questions,  # exclu (NG 2026-08-24) — les 6 énoncés, à décommenter au besoin
        blocks.bck_axis_rationality_accel_synthesis,
        blocks.bck_vote_support,
        blocks.bck_vote_oppose,
        blocks.bck_vote_abstain,
        blocks.bck_axis_rationality_decel_synthesis,
        blocks.bck_vote_support,
        blocks.bck_vote_oppose,
        blocks.bck_vote_abstain,
        # blocks.bck_axis_speed_questions,  # exclu (NG 2026-08-24) — les 6 énoncés, à décommenter au besoin
        blocks.bck_axis_speed_accel_synthesis,
        blocks.bck_vote_support,
        blocks.bck_vote_oppose,
        blocks.bck_vote_abstain,
        blocks.bck_axis_speed_decel_synthesis,
        blocks.bck_vote_support,
        blocks.bck_vote_oppose,
        blocks.bck_vote_abstain,
        # blocks.bck_axis_openness_questions,  # exclu (NG 2026-08-24) — les 6 énoncés, à décommenter au besoin
        blocks.bck_axis_openness_accel_synthesis,
        blocks.bck_vote_support,
        blocks.bck_vote_oppose,
        blocks.bck_vote_abstain,
        blocks.bck_axis_openness_decel_synthesis,
        blocks.bck_vote_support,
        blocks.bck_vote_oppose,
        blocks.bck_vote_abstain,
        # blocks.bck_axis_freedom_questions,  # exclu (NG 2026-08-24) — les 6 énoncés, à décommenter au besoin
        blocks.bck_axis_freedom_accel_synthesis,
        blocks.bck_vote_support,
        blocks.bck_vote_oppose,
        blocks.bck_vote_abstain,
        blocks.bck_axis_freedom_decel_synthesis,
        blocks.bck_vote_support,
        blocks.bck_vote_oppose,
        blocks.bck_vote_abstain,
        # blocks.bck_axis_centralisation_questions,  # exclu (NG 2026-08-24) — les 6 énoncés, à décommenter au besoin
        blocks.bck_axis_centralisation_accel_synthesis,
        blocks.bck_vote_support,
        blocks.bck_vote_oppose,
        blocks.bck_vote_abstain,
        blocks.bck_axis_centralisation_decel_synthesis,
        blocks.bck_vote_support,
        blocks.bck_vote_oppose,
        blocks.bck_vote_abstain,
        # blocks.bck_axis_individualism_questions,  # exclu (NG 2026-08-24) — les 6 énoncés, à décommenter au besoin
        blocks.bck_axis_individualism_accel_synthesis,
        blocks.bck_vote_support,
        blocks.bck_vote_oppose,
        blocks.bck_vote_abstain,
        blocks.bck_axis_individualism_decel_synthesis,
        blocks.bck_vote_support,
        blocks.bck_vote_oppose,
        blocks.bck_vote_abstain,
        # blocks.bck_axis_transhumanism_questions,  # exclu (NG 2026-08-24) — les 6 énoncés, à décommenter au besoin
        blocks.bck_axis_transhumanism_accel_synthesis,
        blocks.bck_vote_support,
        blocks.bck_vote_oppose,
        blocks.bck_vote_abstain,
        blocks.bck_axis_transhumanism_decel_synthesis,
        blocks.bck_vote_support,
        blocks.bck_vote_oppose,
        blocks.bck_vote_abstain,
        blocks.bck_next_module,       # chaîne du jour — gros bouton vers le deck suivant
        # ── Appendix ────────────────────────────────────────────────
        blocks.bck_refs_bibliography,  # never presented; opened when a claim is challenged
    ],
    toc_config=toc,
    marker_config=marker_config,
    # La bibliographie se charge PAR ``st_book``, jamais avant lui (règle NG
    # 2026-08-03) : il vide le registre au début de sa construction.
    bib_sources=bib_sources(),
    bib_config=refs_config(),   # locale = langue projetée (0.7.26)
    # La langue projetée, passée à chaque build(lang) — plan-i18n D2.
    block_kwargs={"lang": current_lang()},
    paginate=True,
    view_modes=[ViewMode.PAGINATED],
    banner=BannerConfig.hidden(),
    page_width=100,
    zoom=100,
    scale=SCALE,  # base amphi 30pt + rétrécissements mobiles (postair_display)
    doc_version=_doc_version,
    pdf_config=PDF,
)
