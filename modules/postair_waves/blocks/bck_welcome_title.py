"""The seventeen waves — title slide of the deck.

The thesis in one screen: sixteen technological revolutions came before this
one; each opened a crisis, and each crisis was overcome. Watching how humanity
crossed them is the shortest way to understand how to cross the wave of AI —
which is what the whole POSTAIR study instruments.

SPEAKER NOTES:
Say the promise, not the plan: « every revolution in this deck opened a crisis
— and every one of them was overcome. The seventeenth is ours. » Then move to
the approach slide. Do not enumerate the waves here: the three grids do it.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from postair_lang import T, TF
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    hero = s.project.titles.hero + s.center_txt
    line = s.project.body.bullet + s.center_txt


bs = BlockStyles

_MARKER = {"en": "The seventeen waves"}
_TITLE = {"en": ("The seventeen ", (s.project.titles.keyword, "waves"))}
_LINE_1 = {"en": ("16 revolutions ", (s.project.colors.keyword, "crossed"),
                  " · 1 being crossed")}
_LINE_2 = {"en": ("every crisis ", (s.project.colors.amber, "opened"),
                  " — every crisis overcome")}


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_center):
        st_write(bs.hero, *TF(_TITLE, lang),
                 tag=t.div, toc_lvl="1", label=T(_MARKER, lang))
        st_space("v", s.project.spacing.title_gap)
        st_write(bs.line, *TF(_LINE_1, lang), tag=t.div)
        st_write(bs.line, *TF(_LINE_2, lang), tag=t.div)
