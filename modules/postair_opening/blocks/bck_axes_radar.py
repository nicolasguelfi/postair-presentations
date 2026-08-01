"""The question of the day: what is YOUR posture facing AI?

SPEAKER NOTES:
This is the pivot of the morning: we stop talking about "AI in general" and
start talking about YOU. Show the empty radar: nine fundamental questions,
nine axes, and a big question mark in the centre — because nobody can answer
for you. Announce the three registers (Knowing, Acting, Becoming) that the
next three slides unfold. Mention that the survey is anonymous and grounded
in a published scientific model.
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
    st_marker("Your posture?")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "What is ", (s.project.titles.keyword, "your posture"),
                         " facing AI?", tag=t.div, toc_lvl="1", label="Your posture?")
            with g.cell():
                st_info_tooltip(
                    title="The POSTAIR model",
                    entries=[
                        ("A posture", "Your personal position facing the AI revolution — not "
                                      "'for or against', but where you stand on nine fundamental "
                                      "tensions. There is no right answer."),
                        ("Nine axes", "Grouped in three registers: KNOWING (how I judge — trust, "
                                      "optimism, rationality), ACTING (how I deploy — speed, "
                                      "openness, freedom/control), BECOMING (what results — "
                                      "centralisation, altruism, transhumanism)."),
                        ("Scientific basis", "The instrument derives from the research article "
                                             "'Understanding human postures in front of the AI "
                                             "revolution' (N. Guelfi, University of Luxembourg)."),
                        ("Anonymous", "The survey you are about to take is fully anonymous: your "
                                      "result is computed on YOUR device; only anonymous averages "
                                      "reach the room screen."),
                    ],
                )
        st_space("v", "1vh")
        # Radar as large as the remaining viewport allows (16:10 SVG).
        with st_grid(cols="1fr 78% 1fr", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_space("h", "0.5vw")
            with g.cell():
                st_image(s.project.cards.media_center, width="100%", uri="images/postair_radar_question.svg",
                         alt="Empty nine-axis POSTAIR radar chart with a large question mark "
                             "in the centre — axes: Trust, Optimism, Rationality, Speed, "
                             "Openness, Freedom/Control, Centralisation, Altruism, Transhumanism")
            with g.cell():
                st_space("h", "0.5vw")
