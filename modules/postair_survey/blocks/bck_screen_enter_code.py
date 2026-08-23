"""The first screens — enter the code (01), seule en scène.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_first) : l'ordre
du deck, l'inclusion et l'exclusion se règlent par une ligne du book. Cette
slide porte l'ancre TOC « The first screens » du groupe ; capture centrée
avec sa légende, comme dans l'ancienne paire.
"""
# @guideline: postair-minimal

from custom.captures import capture
from custom.styles import Styles as s
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    caption = s.project.body.caption + s.center_txt


bs = BlockStyles

_WIDTH = "min(24vw, 42vh)"


def build():
    st_marker("The code screen")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "The first screens — ",
                         (s.project.titles.keyword, "the code"),
                         tag=t.div, toc_lvl="+1", label="The first screens")
            with g.cell():
                st_space("h", "0.5vw")
        st_space("v", "1vh")
        with st_zoom(110):
            st_image(s.project.cards.media_center, width=_WIDTH,
                     uri=capture("01-saisie-code"),
                     alt="Mobile screen of the survey journey: enter the code "
                         "of the day")
            st_write(bs.caption, "1 · enter the code of the day", tag=t.div)
