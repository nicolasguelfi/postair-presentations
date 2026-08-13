"""How we debate — the three rules, with the moderator between two poles.

Opens the discussion sequence. The questions are not chosen by the speaker:
they come out of what this room answered, which is the whole point and the
reason the survey came first.

SPEAKER NOTES:
Three minutes. Insist on one thing above all: nobody defends a position in
their own name. The mascots carry the postures, so a student can argue for
prudence without being labelled a pessimist for the rest of the year — that
is what makes a room of this size willing to speak at all. Give the three
rules plainly, promise the microphone will come to them, and move on.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from postair_data import mascot
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.ai_mark import ai_marked

_RULES = [
    ("Your questions", "the ones where this room splits"),
    ("Two minutes", "one question, one round"),
    # « both sides speak before anyone counts » disait la même chose en une
    # tournure qu'il fallait relire deux fois. Ce qu'elle voulait dire : sur
    # chaque question on entend un argument pour, puis un contre, et le vote à
    # main levée vient seulement après — jamais avant.
    ("For, against, hands", "one argument each way, then the vote"),
]

# The moderator flanked by an opposed pair — the visual grammar of a debate.
_STAGE = ("Libero", "Medio", "Guardo")


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    rule = s.project.body.bullet + s.center_txt + s.bold
    detail = s.project.body.caption + s.center_txt
    mascot_name = s.project.body.mascot_name


bs = BlockStyles


def build():
    st_marker("How we debate")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "Let's ", (s.project.titles.keyword, "debate"),
                         tag=t.div, toc_lvl="1", label="How we debate")
            with g.cell():
                st_info_tooltip(
                    title="How the questions are chosen",
                    entries=[
                        ("Not by the speaker", "The debate questions come from your own answers: "
                         "the selection ranks the statements by disagreement, by engagement and "
                         "by response rate, and keeps the most divisive ones, at most two per "
                         "axis so the debate does not collapse onto a single theme."),
                        ("Two minutes each", "One statement, one argument for, one argument "
                         "against, one show of hands. Short rounds keep a large room awake."),
                        ("Nobody speaks in their own name", "The mascots carry the postures. You "
                         "argue for prudence, not as a prudent person — which is what makes it "
                         "possible to change your mind in public."),
                        ("Microphones", "Roaming microphones; wait for one before speaking, so "
                         "the whole amphitheatre hears you and not just your row."),
                        ("Respect", "Attack the position, never the person holding it. Every "
                         "posture in this instrument is defensible, and each one has been held "
                         "by someone whose name you know."),
                    ],
                )
        st_space("v", "1vh")
        # ONE flat grid: pole · moderator · pole.
        with st_grid(cols="1fr 1.2fr 1fr", gap="1vw",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for name in _STAGE:
                m = mascot(name)
                with g.cell():
                    with ai_marked():
                        st_image(s.project.cards.media_center,
                                 width="min(20vw, 40vh)" if name == "Medio" else "min(14vw, 30vh)",
                                 uri=m["image"],
                                 alt=f"{m['name']}, mascot of the {m['pole'] or 'moderator'} posture")
                    st_write(bs.mascot_name, m["name"], tag=t.div)
        st_space("v", "2vh")
        with st_grid(cols=s.project.grids.balanced(len(_RULES)), gap="1.5vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for rule, detail in _RULES:
                with g.cell(), st_block(s.project.cards.coral):
                    st_write(bs.rule, rule, tag=t.div)
                    st_write(bs.detail, detail, tag=t.div)
