"""Debate wrap-up — the whole cast, and the permission to change your mind.

The eighteen pole mascots are read from the frozen cast manifest and laid out
in ONE flat responsive grid: the full company on stage at the end of the act.
No plate image is needed — the grid is the plate, and it stays true when the
cast changes.

SPEAKER NOTES:
Two minutes to close. The room has just failed to agree, and some of them
will read that as the session having gone badly. Say the opposite, plainly:
on questions like these, a cohort that agreed would be a cohort that had not
thought. Then give them the two things they can take away — their posture is
a snapshot and it will move, and they can retake the survey later with the
same code to see how far. That lands better than any conclusion.
"""
# @guideline: postair-minimal

# ``from streamtex import *`` shadows the builtin ``list`` with the st_list
# module: annotations must stay unevaluated.
from __future__ import annotations

from custom.styles import Styles as s
from postair_data import REGISTERS, register_axes
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    lead = s.project.body.bullet + s.center_txt
    mascot_name = s.project.body.mascot_name


bs = BlockStyles


def _all_poles() -> list[dict]:
    """The eighteen pole mascots, in register order, accelerator first."""
    return [axis[kind]
            for name, _sub, _n in REGISTERS
            for axis in register_axes(name)
            for kind in ("accel", "decel")]


def build():
    st_marker("No consensus")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "No consensus — and that is ",
                         (s.project.titles.keyword, "normal"),
                         tag=t.div, toc_lvl="+1", label="No consensus")
            with g.cell():
                st_info_tooltip(
                    title="After today",
                    entries=[
                        ("A posture is a snapshot", "It is where you stand today, with what you "
                         "know today. The instrument measures a position, not a personality — "
                         "and positions move, especially in a first year."),
                        ("Retake it later", "The same survey can be retaken at the end of the "
                         "year with the same code. Comparing the two is the interesting part; "
                         "most people are surprised by which axis moved."),
                        ("Disagreement is the material", "Every one of these eighteen postures "
                         "has been held, argued and written down by someone whose name is in the "
                         "history of technology. None of them is a mistake."),
                        ("Where to go next", "The afternoon sessions take the same questions to "
                         "practice: how generative AI actually works, how to use it for study, "
                         "and what the university's rules say."),
                    ],
                )
        st_space("v", "1vh")
        st_write(bs.lead, "Your posture today is ", (s.project.titles.keyword, "a snapshot"),
                 " — retake it at the end of the year", tag=t.div)
        st_space("v", "1.5vh")
        # ONE flat grid, the full company: eighteen cells, wrapping naturally.
        with st_grid(cols="repeat(auto-fit, minmax(min(140px, 45vw), 1fr))", gap="0.6vw",
                     cell_styles=s.project.containers.grid_cell_top) as g:
            for pole in _all_poles():
                with g.cell():
                    st_image(s.project.cards.media_center, width="min(8vw, 15vh)",
                             uri=pole["image"],
                             alt=f"{pole['mascot']}, mascot of the {pole['label']} posture")
                    st_write(bs.mascot_name, pole["mascot"], tag=t.div)
