"""Provenance — said once, for the whole document, on its own slide.

Until 2026-08-11 every figure card repeated two caption lines: « reconstructed
profile — commits its author, not the figure » and, for living people,
« video: a presentation of this living person, not their own words ». Decision
NG (2026-08-11): the cards stop carrying them — fifty-four repetitions turn an
honesty clause into wallpaper — and the clause is stated ONCE here, early,
where it frames everything that follows.

SPEAKER NOTES:
Project it once, before opening the first axis, and say it in one breath: the
postures are our reconstruction from primary sources — they commit us, never
the figures; and no living person is ever made to speak by generative AI —
their video is somebody presenting them. Then move on. If a card is challenged
later, come back here rather than improvising the answer.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from streamtex import *
from streamtex.enums import Tags as t

_CLAUSES = [
    ("Reconstructed postures",
     "Each figure's position on an axis is a reconstruction from primary "
     "sources — it commits its author, never the figure."),
    ("Living people",
     "No living person is made to speak by generative AI. Their video is a "
     "presentation of them, by the author, in the author's own name."),
    ("Sourced quotations",
     "Every quotation is verbatim and verified; its citation code opens the "
     "full reference, and the References page closes the document."),
]


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    lead = s.project.titles.subtitle + s.center_txt
    clause = s.project.body.bullet + s.center_txt + s.bold
    detail = s.project.body.caption + s.center_txt


bs = BlockStyles


def build():
    st_marker("Provenance")
    with st_block(s.project.containers.page_fill_top):
        st_write(bs.title, "What these cards ", (s.project.titles.keyword, "are"),
                 " — and are not", tag=t.div, toc_lvl="1", label="Provenance")
        st_space("v", "1vh")
        st_write(bs.lead, "three rules, valid for every slide of this document",
                 tag=t.div)
        st_space("v", "2.5vh")
        with st_grid(cols=s.project.grids.balanced(len(_CLAUSES)), gap="1.5vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for clause, detail in _CLAUSES:
                with g.cell(), st_block(s.project.cards.blue):
                    st_write(bs.clause, clause, tag=t.div)
                    st_write(bs.detail, detail, tag=t.div)
