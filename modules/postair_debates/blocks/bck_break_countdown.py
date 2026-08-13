"""Break screen — a live countdown and the company waiting on stage.

The break duration comes from the agenda, not from a constant typed here: if
the programme changes, the screen follows. The countdown starts when the
slide is shown, so it is right whenever the presenter actually reaches it.

SPEAKER NOTES:
Say the time out loud as well as showing it — half the room is already
standing and looking at the person next to them, not at the screen. Point at
the countdown once so people know where to look from the corridor, and say
what comes back after: generative AI, how it actually works. Then stop
talking; the screen does the rest.
"""
# @guideline: postair-minimal

# ``from streamtex import *`` shadows the builtin ``list`` with the st_list
# module: annotations must stay unevaluated.
from __future__ import annotations

from custom.styles import Styles as s
from postair_data import REGISTERS, register_axes
from postair_event import AGENDA
from shared_widgets import st_countdown, st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.ai_mark import ai_marked


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    mascot_name = s.project.body.mascot_name


bs = BlockStyles


def _break_minutes() -> int:
    """The break duration, read from the agenda (e.g. \"20'\" → 20)."""
    for _session, duration, kind in AGENDA:
        if kind == "break":
            return int("".join(c for c in duration if c.isdigit()))
    raise LookupError("the agenda declares no break")


def _company() -> list[dict]:
    """Every pole mascot — the full company, waiting for the second half."""
    return [axis[kind]
            for name, _sub, _n in REGISTERS
            for axis in register_axes(name)
            for kind in ("accel", "decel")]


def build():
    st_marker("Break")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, (s.project.titles.keyword, "Break"),
                         tag=t.div, toc_lvl="1", label="Break")
            with g.cell():
                st_info_tooltip(
                    title="After the break",
                    entries=[
                        ("Introduction to AI & Generative AI", "How a large language model "
                         "actually works, what it can and cannot do, and why it makes things up "
                         "with such confidence."),
                        ("Using Mistral models & agents to study", "Building a revision agent "
                         "step by step — including the mistakes that make one useless."),
                        ("The UL AI guidelines", "The university's rules: permitted by default, "
                         "the syllabus prevails, disclose your use, three levels of risk, ten red "
                         "lines, and the one test that settles the rest."),
                        ("Keep your device", "The second half is lighter on the phone, but keep "
                         "it within reach anyway."),
                    ],
                )
        st_countdown(_break_minutes())
        st_space("v", "1vh")
        # ONE flat grid — the company on stage while the room is out.
        company = _company()
        with st_grid(cols=s.project.grids.balanced(len(company)), gap="0.5vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for pole in company:
                with g.cell():
                    with ai_marked():
                        st_image(s.project.cards.media_center, width="min(6.5vw, 12vh)",
                                 uri=pole["image"],
                                 alt=f"{pole['mascot']}, mascot of the {pole['label']} posture")
                    st_write(bs.mascot_name, pole["mascot"], tag=t.div)
