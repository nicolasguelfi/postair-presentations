"""postair_mistral — Study Smarter: your course agent (Mistral & co., 20').

Seventh document of the POSTAIR set, between the GenAI intro and the UL
guidelines (official agenda: « Using models & agents to study »). See
_project/plans/plan-postair_mistral.md — the plan ↔ block mapping is one to
one (M1…M11), plus the two backups (ragm7, podcast) and the References
appendix.
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
    page_title="AI DAY — Mistral & co.",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",  # NG 2026-09-03 : lancement panneau FERMÉ (la projection dispose de toute la largeur)
)

sts.theme = dark

set_presentation_config(PresentationConfig(
    title="AI DAY — Study Smarter: your course agent",
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
# Export PDF : même calibrage que le deck genai (paysage A4, marges minces,
# print_background pour le thème sombre).
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
        blocks.bck_mistral_title,          # M1  · Study Smarter: your course agent
        blocks.bck_mistral_your_tool,      # M2  · la démo est sur Mistral, la méthode est à vous
        blocks.bck_mistral_goal,           # M3  · un agent pour UN cours (schéma)
        blocks.bck_mistral_method,         # M4  · la méthode en 5 étapes — LA slide à photographier
        blocks.bck_mistral_demo_build,     # M5  · démo A : construire l'agent (live)
        blocks.bck_mistral_demo_use,       # M6  · démo B : l'agent au travail (live)
        blocks.bck_mistral_agent_doors,    # M6b · les trois portes — ouvrir SES agents
        blocks.bck_mistral_services_map,   # SV1 · la carte des services (synthèse en flux)
        blocks.bck_mistral_err_sources,    # M7  · erreur 1 — sans sources, il invente ton cours
        blocks.bck_mistral_err_delegate,   # M8  · erreur 2 — tout déléguer, tu n'apprends rien
        blocks.bck_mistral_err_trust,      # M9  · erreur 3 — croire sans vérifier (cadrage)
        blocks.bck_mistral_err_data,       # M10 · erreur 4 — données perso & matériel protégé
        blocks.bck_mistral_recap,          # M11 · récap méthode + « keep your prompt history »
        blocks.bck_next_module,            # chaîne du jour — gros bouton vers le deck suivant
        # ── Annexe BACKUP (pattern genai) : jamais présentée, accessible en
        # 2 s par la barre latérale pendant les questions. ──────────────────
        blocks.bck_mistral_backup_divider, # seuil « — Backup — »
        blocks.bck_mistral_bk_rag,         # bk · le POURQUOI derrière l'erreur 1 (ragm7)
        blocks.bck_mistral_bk_podcast,     # bk · d'autres outils, même méthode (podcast)
        blocks.bck_mistral_bk_services_create,   # SV2 · créer TON agent (matrice)
        blocks.bck_mistral_bk_services_feed,     # SV3 · le nourrir de ton cours (matrice)
        blocks.bck_mistral_bk_services_voice,    # SV4 · lui parler (matrice voix)
        blocks.bck_mistral_bk_services_students, # SV5 · offres étudiantes (Luxembourg)
        blocks.bck_refs_bibliography,      # never presented; opened when challenged
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
    presentation_profiles=postair_profiles(),
    scale=SCALE,  # base amphi 30pt + rétrécissements mobiles renforcés (postair_display)
    doc_version=_doc_version,
    pdf_config=PDF,
)
