"""Poster: the survey part opens with one single full-frame image.

SPEAKER NOTES:
No speech needed — let the image land. One sentence to pivot: "Time to answer
the question of the day: we measure YOUR postures, live, all together."
Nothing on this slide reveals the mechanics; the how-to comes next.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt


bs = BlockStyles


def build():
    st_marker("The Survey — poster")
    with st_block(s.project.containers.page_fill_center):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "The ", (s.project.titles.keyword, "Survey"),
                         tag=t.div, toc_lvl="1", label="The Survey")
            with g.cell():
                st_info_tooltip(
                    title="Next 30 minutes",
                    entries=[
                        ("Now", "You answer the POSTAIR survey on your phone or laptop — "
                                "anonymous, 15-20 minutes."),
                        ("Then", "We project the live results of THIS room and discover the "
                                 "cohort's postures together."),
                        ("Finally", "We debate the most divisive questions of your cohort."),
                    ],
                )
        st_image(s.project.cards.media_center, width="86%",
                 editable=False, name="survey_poster",
                 alt="Papercut poster: a giant nine-spoke paper radar with a huge question "
                     "mark at its centre, surrounded by a cheerful crowd of paper silhouettes")
