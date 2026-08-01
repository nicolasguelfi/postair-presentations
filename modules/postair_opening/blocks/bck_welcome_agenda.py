"""Agenda of the day — the nine sessions as one flat timeline.

Data-driven from ``custom.event.AGENDA``: the block renders, it does not know
the programme. Colour follows the ``kind`` of each session — a session is
framing blue, the discussion is coral (human/debate), the break is the single
amber focal accent of the slide, and it carries Lento, the prudence mascot,
because the break is the moment the room slows down.

SPEAKER NOTES:
Two minutes, no more. Say where we are (first session), point at the break so
nobody worries about it for the next two hours, and give the participation
instruction: phone OR laptop, your choice — keep one within reach, we will
need it very soon. Mention the exits and the toilets while the slide is up:
it is the only moment of the day where logistics are the subject.
"""
# @guideline: postair-minimal

from custom.event import AGENDA
from custom.styles import Styles as s
from postair_data import mascot
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

_CARD = {"stage": s.project.cards.blue,
         "debate": s.project.cards.coral,
         "break": s.project.cards.amber}

_DURATION = {"stage": s.project.colors.primary,
             "debate": s.project.colors.coral,
             "break": s.project.colors.amber}


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    session = s.project.body.body + s.center_txt + s.bold
    duration = s.project.titles.subtitle + s.center_txt + s.bold
    mascot_name = s.project.body.mascot_name


bs = BlockStyles


def build():
    st_marker("Agenda")
    lento = mascot("Lento")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "Our ", (s.project.titles.keyword, "three hours"),
                         " together", tag=t.div, toc_lvl="+1", label="Agenda")
            with g.cell():
                st_info_tooltip(
                    title="How the day runs",
                    entries=[
                        ("Two parts", "Five sessions before the break — welcome, survey, "
                         "results, discussion — then four after: generative AI, Mistral "
                         "agents, the university guidelines, and the closing."),
                        ("What you need", "A phone OR a laptop, your choice. Keep one within "
                         "reach: the survey starts in a few minutes and runs on it."),
                        ("The survey", "Thirty minutes, anonymous, fifty-four statements. "
                         "Your answers drive the two sessions that follow — the results and "
                         "the debate are built live from what this room answers."),
                        ("The break", "Twenty minutes, in the middle. The screen will show a "
                         "countdown, so you always know how long is left."),
                        ("Logistics", "Exits at the back and on both sides; toilets in the "
                         "corridor behind the amphitheatre. No need to ask — just go."),
                    ],
                )
        st_space("v", "2vh")
        # ONE flat responsive grid: nine cells side by side on the projector,
        # wrapping on a narrow window. No nested grid — the mascot lives inside
        # its own cell, not in a sub-grid.
        with st_grid(cols="repeat(auto-fit, minmax(min(200px, 80vw), 1fr))", gap="1vw",
                     cell_styles=s.project.containers.grid_cell_top) as g:
            for session, duration, kind in AGENDA:
                with g.cell(), st_block(_CARD[kind]):
                    st_write(bs.duration + _DURATION[kind], duration, tag=t.div)
                    st_write(bs.session, session, tag=t.div)
                    if kind == "break":
                        st_image(s.project.cards.media_center, width="70%",
                                 uri=lento["image"],
                                 alt=f"{lento['name']}, the prudence mascot of the speed axis")
                        st_write(bs.mascot_name, lento["name"], tag=t.div)
