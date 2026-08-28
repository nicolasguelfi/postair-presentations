"""postair_collection — le livre des modules de l'AI Day.

Un hub d'une page, sur le modèle de ``stx_manuals_collection`` (streamtex-docs) :
une carte par module déployé, lue depuis ``collection.toml``. Ajouter un module
= une section dans le toml, rien ici.
"""

import setup  # noqa: F401  — MUST run first (sys.path: module dir + shared-blocks)

import tomllib
from pathlib import Path

import blocks
from postair_lang import current_lang
import streamlit as st
import streamtex as stx
import streamtex.styles as sts
from custom.themes import dark
from streamtex import (
    BannerConfig,
    NumberingMode,
    PdfConfig,
    PresentationConfig,
    TOCConfig,
    ViewMode,
    set_presentation_config,
    st_book,
)

_MODULE_DIR = Path(__file__).parent
if not (_MODULE_DIR / "static").exists():
    _MODULE_DIR = Path.cwd()

try:
    _doc_version = tomllib.loads(
        (_MODULE_DIR.parent.parent / "pyproject.toml").read_text(encoding="utf-8")
    ).get("project", {}).get("version", "?")
except OSError:
    _doc_version = "?"

stx.set_static_sources([
    str(_MODULE_DIR / "static"),
    str(_MODULE_DIR.parent / "shared-blocks" / "static"),
])
stx.configure_image_path("app/static/media")

st.set_page_config(
    page_title="AI DAY — Presentations",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

sts.theme = dark

set_presentation_config(PresentationConfig(
    title="AI DAY — The presentations",
    aspect_ratio="16/9",
    footer=True,
    center_content=False,
    enforce_ratio=False,
    hide_streamlit_header=False,
))

toc = TOCConfig(numbering=NumberingMode.SIDEBAR_ONLY, toc_position=None, search=False)

# Une seule page, pas de pagination : c'est un hub, pas un deck.
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
        blocks.bck_home,
    ],
    toc_config=toc,
    # La langue projetée, passée à chaque build(lang) — plan-i18n D2.
    block_kwargs={"lang": current_lang()},
    paginate=False,
    view_modes=[ViewMode.CONTINUOUS],
    banner=BannerConfig.hidden(),
    page_width=100,
    zoom=100,
    doc_version=_doc_version,
    pdf_config=PDF,
)
