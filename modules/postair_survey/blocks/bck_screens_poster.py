"""Poster: the screens part opens on ONE real screen — the personal radar.

TOC anchor of Part 2 (« The screens »). One full-frame mobile capture of
``09-res-radar`` — the screen the whole survey exists to produce — and
nothing else. Every capture in this part is the REAL application, frozen from
the sumvadis media registry (``build_survey_captures.py``), never a mock-up;
mobile facet by decision Q14 (NG 2026-08-14): the deck projects what the room
holds in hand.

SPEAKER NOTES:
One sentence, then silence: "this is where you are going — YOUR posture, on
your phone, in about twenty minutes." Do not explain the radar here; the
reading lesson comes later in this part. Let the room recognise a phone
screen, not a slide.
"""
# @guideline: postair-minimal

from custom.captures import capture
from custom.styles import Styles as s
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    caption = s.project.body.mascot_name + s.center_txt


bs = BlockStyles

#: Plein cadre pour une capture PORTRAIT : la hauteur borne, pas la largeur.
_POSTER_WIDTH = "min(30vw, 34vh)"


def build():
    st_marker("The screens — poster")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "The ", (s.project.titles.keyword, "screens"),
                         tag=t.div, toc_lvl="1", label="The screens")
            with g.cell():
                st_info_tooltip(
                    title="This part",
                    entries=[
                        ("Real screens", "Every capture in this part is the real application, "
                         "photographed by the sumvadis capture pipeline — never a mock-up, "
                         "never retouched."),
                        ("Why phone screens", "The room answers on phones, so the deck shows "
                         "the mobile screens — what you will actually hold in hand."),
                        ("Operator screens", "The régie pages (admin console, live view, "
                         "projection) are desktop screens; they join this part once their "
                         "captures are published."),
                    ],
                )
        st_space("v", "1vh")
        st_image(s.project.cards.media_center, width=_POSTER_WIDTH,
                 uri=capture("09-res-radar"),
                 alt="Mobile screen of the survey report: the personal nine-axis "
                     "posture radar, dark theme")
        st_write(bs.caption, "where you are going — your radar, on your phone",
                 tag=t.div)
