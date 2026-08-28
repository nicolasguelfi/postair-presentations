"""Agenda of the day — before the break, the break, after the break.

Data-driven from ``postair_event.AGENDA``: the block renders, it does not know
the programme. Colour follows the ``kind`` of each session — a session is
framing blue, the discussion is coral (human/debate), the break is the single
amber focal accent of the slide, and it carries Lento, the prudence mascot,
because the break is the moment the room slows down.

Three columns (NG 2026-08-03), and the shape carries the meaning: everything
before the break on the left, the break alone in the middle, everything after
on the right. Nine cards in a row said "nine equal things"; this says "two
halves and a pause", which is how the room will actually live the morning —
and it buys each card three times the width, so the wording and the timing can
be read from the back.

The split is read from the data, never counted by hand: the break is the entry
whose ``kind`` is ``break``. Move it in ``postair_event.py`` and the columns
follow.

SPEAKER NOTES:
Two minutes, no more. Say where we are (first session), point at the break so
nobody worries about it for the next two hours, and give the participation
instruction: phone OR laptop, your choice — keep one within reach, we will
need it very soon. Mention the exits and the toilets while the slide is up:
it is the only moment of the day where logistics are the subject.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from postair_data import mascot
from postair_event import AGENDA
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.ai_mark import dd35_overlay

_CARD = {"stage": s.project.cards.blue,
         "debate": s.project.cards.coral,
         "break": s.project.cards.amber}

_DURATION = {"stage": s.project.colors.primary,
             "debate": s.project.colors.coral,
             "break": s.project.colors.amber}


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    session = s.project.body.session_name
    duration = s.project.titles.duration
    mascot_name = s.project.body.mascot_name


bs = BlockStyles


def _columns():
    """The agenda as three columns: before the break, the break, after it."""
    kinds = [kind for _s, _d, kind in AGENDA]
    pause = kinds.index("break")
    return [AGENDA[:pause], AGENDA[pause:pause + 1], AGENDA[pause + 1:]]


def build(lang: str = "en", **_):
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
                        ("Two parts", "Four sessions before the break — welcome, survey, "
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
        st_space("v", "3vh")
        # Three columns, each a flat stack — no nested grid. The floors are in
        # percent so three columns hold on a projector and collapse to one on a
        # narrow window, without a hard-coded breakpoint.

        # Trois pistes en fractions : avant 40 · pause 20 · après 40.
        _COLS = "minmax(0, 32fr) minmax(0, 26fr) minmax(0, 42fr)"

        with st_grid(cols=_COLS, gap="1.2vw", breakpoint="720px",
                    grid_style=s.project.grids.stretch,
                    cell_styles=s.project.containers.grid_cell_stretch) as g:

            for column in _columns():
                alone = len(column) == 1
                stack = (s.project.containers.column_stack_centered if alone
                         else s.project.containers.column_stack)
                with g.cell(), st_block(stack):
                    for session, duration, kind in column:
                        with st_block(_CARD[kind]):
                            with st_zoom(120):
                                st_write(bs.duration + _DURATION[kind], duration, tag=t.div)
                                st_write(bs.session, session, tag=t.div)
                            if kind == "break":
                                st_image(s.project.cards.media_center, width="55%",
                                         uri=lento["image"],
                                         alt=f"{lento['name']}, the prudence mascot "
                                             "of the speed axis",
                                         overlay=dd35_overlay())
                                st_write(bs.mascot_name, lento["name"], tag=t.div)
