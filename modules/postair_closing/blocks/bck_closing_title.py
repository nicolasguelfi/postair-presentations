"""La slide-titre de la clôture (C1) — la conférence se referme.

v1 volontairement sobre : le module est né pour accueillir les slides de
clôture de NG (planche anim1, 2026-09-03) — cette slide pose le seuil, le
reste viendra de sa main.

SPEAKER NOTES:
One breath. The day is done — what follows are the take-home slides: keep
learning (Digital Learning Hub), and whatever NG adds here.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from postair_lang import T, TF
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    subtitle = s.project.titles.subtitle + s.center_txt


bs = BlockStyles

_MARKER = {"en": "Closing", "fr": "Clôture"}
_TITLE = {"en": ("AI DAY — ", (s.project.titles.keyword, "Closing")), "fr": ("AI DAY — ", (s.project.titles.keyword, "Clôture"))}
_SUBTITLE = {"en": "take the method home — and keep learning", "fr": "emportez la méthode — et continuez d'apprendre"}


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        st_space("v", "20vh")
        with st_zoom(250):
            st_write(bs.title, *TF(_TITLE, lang),
                     tag=t.div, toc_lvl="1", label=T(_MARKER, lang))
        st_space("v", "6vh")
        with st_zoom(160):
            st_write(bs.subtitle, T(_SUBTITLE, lang), tag=t.div)
