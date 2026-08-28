"""Wrap-up — sixteen crises overcome, the seventeenth being written.

The deck's thesis said back to the room, and the bridge to the live survey:
the recomposed world of the AI wave is deliberately unfinished — the
half-written whiteboard, the marker waiting for a hand. The next thing the
room does is pick that marker up: the survey measures their posture.

SPEAKER NOTES:
Close on the numbers, slowly: sixteen crises opened, sixteen overcome. Then
the last line, looking at the room: « the seventeenth is yours ». Move
straight to the survey deck.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    giant = s.project.body.bullet_giant + s.center_txt
    line = s.project.body.bullet + s.center_txt


bs = BlockStyles


def build(lang: str = "en", **_):
    st_marker("Sixteen and one")
    with st_block(s.project.containers.page_fill_center):
        st_write(bs.title, "Sixteen crises ", (s.project.titles.keyword, "overcome"),
                 tag=t.div, toc_lvl="1", label="Sixteen and one")
        st_space("v", s.project.spacing.title_gap)
        st_write(bs.giant, "16 opened · 16 overcome", tag=t.div)
        st_write(bs.line, "rules, uses, postures — every time", tag=t.div)
        st_space("v", "4vh")
        st_write(bs.line, "the seventeenth is ",
                 (s.project.colors.amber, "yours"),
                 " — the survey measures your posture next", tag=t.div)
