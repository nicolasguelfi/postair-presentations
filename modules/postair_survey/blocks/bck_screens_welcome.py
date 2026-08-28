"""The first screens — the campaign welcome (02), seule en scène.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_first) : capture
centrée avec sa légende, comme dans l'ancienne paire. L'ancre TOC du groupe
vit sur la slide du code (bck_screens_enter_code).
"""
# @guideline: postair-minimal

from custom.captures import capture
from custom.styles import Styles as s
from postair_i18n import ui
from postair_lang import T
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    caption = s.project.body.caption + s.center_txt


bs = BlockStyles

_WIDTH = "min(24vw, 42vh)"

_MARKER = {"en": "The welcome screen", "fr": "L'écran d'accueil"}
#: Le début du titre (« The first screens — ») vient du lexique : il ouvre
#: aussi la slide du code.
_KEYWORD = {"en": "welcome", "fr": "l'accueil"}
_CAPTION = {"en": "2 · the campaign welcomes you", "fr": "2 · la campagne vous accueille"}


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, ui("first_screens_dash", lang),
                         (s.project.titles.keyword, T(_KEYWORD, lang)), tag=t.div)
            with g.cell():
                st_space("h", "0.5vw")
        st_space("v", "1vh")
        with st_zoom(250):
            st_image(s.project.cards.media_center, width=_WIDTH,
                     uri=capture("02-accueil-campagne", device="desktop", lang=lang),
                     alt="Mobile screen of the survey journey: the campaign "
                         "welcomes you")
            st_write(bs.caption, T(_CAPTION, lang), tag=t.div)
