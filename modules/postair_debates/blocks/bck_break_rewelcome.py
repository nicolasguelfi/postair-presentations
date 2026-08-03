"""Re-welcome — what the second half holds, in three cards.

Reads the post-break sessions from the agenda rather than restating them, so
the slide cannot drift from the programme. Medio comes back on stage: the
moderator opened the morning, the moderator restarts it.

SPEAKER NOTES:
One minute, energy up. People come back scattered and half of them are still
in the corridor — do not start the content here. Name the three sessions, say
that the first one answers the question everybody actually has ("how does
this thing work?"), and hand over.
"""
# @guideline: postair-minimal

# ``from streamtex import *`` shadows the builtin ``list`` with the st_list
# module: annotations must stay unevaluated.
from __future__ import annotations

from custom.styles import Styles as s
from postair_data import mascot
from postair_event import AGENDA
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

_PROMISE = {
    "Introduction to AI & Generative AI": "understand",
    "Using Mistral models & agents to study": "practice",
    "The UL AI guidelines": "the rules of the game",
}


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    session = s.project.body.body + s.center_txt + s.bold
    promise = s.project.titles.subtitle + s.center_txt
    duration = s.project.body.caption + s.center_txt
    mascot_name = s.project.body.mascot_name


bs = BlockStyles


def _second_half() -> list[tuple[str, str]]:
    """Sessions after the break, in agenda order — closing excluded."""
    seen_break = False
    out = []
    for session, duration, kind in AGENDA:
        if kind == "break":
            seen_break = True
            continue
        if seen_break and session in _PROMISE:
            out.append((session, duration))
    return out


def build():
    st_marker("Part two")
    medio = mascot("Medio")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "Part two — ", (s.project.titles.keyword, "how it works"),
                         ", and what you may do with it",
                         tag=t.div, toc_lvl="+1", label="Part two")
            with g.cell():
                st_info_tooltip(
                    title="The second half",
                    entries=[
                        ("Understand", "What a large language model is doing when it answers: "
                         "prediction, not knowledge — and why that explains both the usefulness "
                         "and the confident mistakes."),
                        ("Practice", "A revision agent built live with Mistral, including the "
                         "anti-patterns: the agent that flatters, the one that invents sources, "
                         "the one that does the work you needed to do yourself."),
                        ("The rules", "The university's AI charter: permitted by default, the "
                         "syllabus prevails, disclose your use, three risk levels, ten red lines "
                         "— and the test that decides the rest: can you defend it out loud?"),
                        ("Same posture, new light", "Everything in the second half connects back "
                         "to the nine axes you answered on this morning."),
                    ],
                )
        st_space("v", "1vh")
        # ONE flat grid — the moderator is a cell like the others, never a
        # column holding a second responsive grid.
        second = _second_half()
        with st_grid(cols=s.project.grids.balanced(1 + len(second)), gap="1.2vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_top) as g:
            with g.cell():
                st_image(s.project.cards.media_center, width="min(16vw, 34vh)",
                         uri=medio["image"],
                         alt=f"{medio['name']}, the moderator mascot, restarting the session")
                st_write(bs.mascot_name, medio["name"], tag=t.div)
            for session, duration in second:
                with g.cell(), st_block(s.project.cards.blue):
                    st_write(bs.promise, _PROMISE[session], tag=t.div)
                    st_write(bs.session, session, tag=t.div)
                    st_write(bs.duration, duration, tag=t.div)
