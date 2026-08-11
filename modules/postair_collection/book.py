"""postair_collection — le livre des modules de l'AI Day.

Un hub d'une page, sur le modèle de ``stx_manuals_collection`` (streamtex-docs) :
une carte par module déployé, lue depuis ``collection.toml``. Ajouter un module
= une section dans le toml, rien ici.
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
    BannerConfig,
    NumberingMode,
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
st_book(
    [
        blocks.bck_home,
    ],
    toc_config=toc,
    paginate=False,
    view_modes=[ViewMode.CONTINUOUS],
    banner=BannerConfig.hidden(),
    page_width=100,
    zoom=100,
    doc_version=_doc_version,
)
