"""Why look back — the theoretical frame of the deck, in three cards.

Kuhn reads a scientific revolution as paradigm → anomaly → crisis → new
paradigm; Perez shows the great technological surges repeating their social
pattern; and the POSTAIR report documents that every stance of today's AI
debate has a documented ancestor. The quadriptych of every wave in this deck
IS that cycle, made visible.

SPEAKER NOTES:
One sentence per card: revolutions follow a cycle (Kuhn) ; the cycle repeats
across surges (Perez) ; so the sixteen crossed waves are DATA about ours.
Then the substitution slide explains how the comparison is made rigorous.
"""
# @guideline: postair-minimal

from custom.refs import citation
from custom.styles import Styles as s
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    head = s.project.body.pole_label_accel_compact
    body = s.project.body.mascot_name


bs = BlockStyles

_CARDS = [
    ("A cycle", "paradigm → anomaly → CRISIS → new paradigm", "kuhn1962",
     "Kuhn, The Structure of Scientific Revolutions (1962): resistances, "
     "conversions and generation effects are part of every paradigm shift."),
    ("A repetition", "great surges repeat their social pattern", "perez2002",
     "Perez, Technological Revolutions and Financial Capital (2002): each "
     "surge brings the same sequence of irruption, frenzy, crisis and "
     "deployment."),
    ("An inheritance", "every AI stance has an ancestor", None,
     "The POSTAIR report documents it figure by figure: today's enthusiasts, "
     "sceptics and regulators all have documented ancestors in the sixteen "
     "previous waves."),
]


def build():
    st_marker("Why look back")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "Why look ", (s.project.titles.keyword, "back"),
                         tag=t.div, toc_lvl="1", label="Why look back")
            with g.cell():
                st_info_tooltip(title="The frame, in full sentences",
                                entries=[(head, full)
                                         for head, _, _, full in _CARDS])
        st_space("v", s.project.spacing.title_gap)
        with st_grid(cols=s.project.grids.balanced(len(_CARDS)), gap="1.5vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_top) as g:
            for head, tele, key, _ in _CARDS:
                with g.cell(), st_block(s.project.cards.blue):
                    st_write(bs.head, head, tag=t.div)
                    st_write(bs.body, tele, tag=t.div)
                    if key:
                        st_write(bs.body, citation(key), tag=t.div)
