"""Collection home — the AI Day presentations, one card per module.

Cards are generated from ``collection.toml`` (modèle : stx_manuals_collection
de streamtex-docs) : adding a module never touches this block. URLs come from
the toml, overridable per deployment by ``STX_URL_<KEY>`` env vars. Each card
opens the deck in ONE language per button (NG 2026-08-29): the language
travels in the address (``?lang=``), nothing is remembered anywhere.

House visual line: postair_dark (navy canvas, blue framing cards, ONE amber
accent) — this hub is read on a laptop by the speaker and the team, but it
keeps the family's face.
"""
# @guideline: postair-minimal

import os
import tomllib
from pathlib import Path

from custom.styles import Styles as s
from postair_chain import leaf
from postair_lang import LANGS, NAMES, T, with_lang
from streamtex import *
from streamtex.enums import Tags as t

_TOML_PATH = Path(__file__).parent.parent / "collection.toml"
with open(_TOML_PATH, "rb") as _f:
    _CONFIG = tomllib.load(_f)

_CARDS_PER_ROW = _CONFIG.get("collection", {}).get("cards_per_row", 3)

_PROJECTS = []
for _key, _data in sorted(_CONFIG.get("projects", {}).items(),
                          key=lambda item: item[1].get("order", 0)):
    env_key = "STX_URL_" + _key.upper().replace("-", "_")
    _PROJECTS.append({
        "key": _key,
        "title": leaf(_data.get("title", _key)),
        "description": leaf(_data.get("description", "")),
        "emoji": _data.get("emoji", "📄"),
        "button_label": leaf(_data.get("button_label", "Open")),
        "url": os.environ.get(env_key, _data.get("project_url", "#")),
    })


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    subtitle = s.project.titles.subtitle + s.center_txt
    emoji = s.project.titles.subtitle + s.center_txt
    card_title = s.project.body.bullet + s.center_txt + s.bold
    card_desc = s.project.body.caption + s.center_txt
    footer = s.project.body.caption + s.center_txt
    # DEUX boutons par carte, un par langue (NG 2026-08-29) : la langue vit
    # dans l'adresse du deck ouvert. L'anglais garde l'accent ambre (langue
    # par défaut du jour), le français prend le bleu de cadrage — un seul
    # accent focal par carte, règle R5.
    #: Libellé = le NOM DE LA LANGUE seul, en gros (NG 2026-09-02) — le
    #: « Open/Ouvrir · » est tombé, la langue est toute l'information.
    _button = (
        "display:block;box-sizing:border-box;padding:1.2vh 1vw;flex:1 1 0;"
        "text-align:center;border-radius:0.8vh;text-decoration:none;font-weight:700;"
        "font-size:clamp(15px, 1.2vw, 24px);"
    )
    button_css = {
        "en": _button + "background:#F39C12;color:#1A1A2E;",
        "fr": _button + "background:#3A6EA5;color:#F2EEE6;",
    }
    buttons_row = "display:flex;gap:0.8vw;width:100%;"


bs = BlockStyles


def _card(project: dict, lang: str) -> None:
    # Compact (NG 2026-08-13) : emoji EN LIGNE avec le titre — quatre cartes
    # 2×2 tiennent dans un écran laptop sans coupe.
    with st_block(s.project.cards.blue):
        st_write(bs.card_title, project["emoji"], "  ", T(project["title"], lang), tag=t.div)
        st_space("v", "0.6vh")
        st_write(bs.card_desc, T(project["description"], lang), tag=t.div)
        st_space("v", "1vh")
        # Un bouton par langue, libellé = le NOM de la langue seul
        # (« English », « Français » — NG 2026-09-02) ; le lien porte
        # ``?lang=``. Le ``button_label`` du toml n'est plus affiché.
        links = "".join(
            f'<a href="{with_lang(project["url"], code)}" target="_blank" rel="noopener" '
            f'style="{bs.button_css[code]}">{NAMES[code]}</a>'
            for code in LANGS)
        st_html(f'<div style="{bs.buttons_row}">{links}</div>')


def build(lang: str = "en", **_):
    st_marker("AI Day")
    meta = _CONFIG.get("collection", {})
    with st_block(s.project.containers.page_fill_top):
        st_write(bs.title, "AI DAY — the ", (s.project.titles.keyword, "presentations"),
                 tag=t.div, toc_lvl="1", label="AI Day")
        st_space("v", "0.5vh")
        st_write(bs.subtitle, T(leaf(meta.get("description", "")), lang), tag=t.div)
        st_space("v", "2vh")
        # UNE grille équilibrée (NG 2026-08-13) : quatre cartes = 2×2, sans
        # rangée orpheline pleine largeur ni carte coupée en bas d'écran.
        with st_grid(cols=s.project.grids.balanced(len(_PROJECTS)), gap="1.5vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_top) as g:
            for project in _PROJECTS:
                with g.cell():
                    _card(project, lang)
        st_space("v", "3vh")
        # « Mistral joins the day it exists » est tombé le 2026-09-02 : le
        # module postair_mistral existe et porte sa carte ci-dessus.
        st_write(bs.footer,
                 "one service per deck · this hub only links", tag=t.div)
