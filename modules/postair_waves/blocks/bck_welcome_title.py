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
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    hero = s.project.titles.hero + s.center_txt
    line = s.project.body.bullet + s.center_txt


bs = BlockStyles


def build():
    st_marker("The seventeen waves")
    with st_block(s.project.containers.page_fill_center):
        st_write(bs.hero, "The seventeen ", (s.project.titles.keyword, "waves"),
                 tag=t.div, toc_lvl="1", label="The seventeen waves")
        st_space("v", s.project.spacing.title_gap)
        st_write(bs.line, "16 revolutions ",
                 (s.project.colors.keyword, "crossed"),
                 " · 1 being crossed", tag=t.div)
        st_write(bs.line, "every crisis ", (s.project.colors.amber, "opened"),
                 " — every crisis overcome", tag=t.div)
