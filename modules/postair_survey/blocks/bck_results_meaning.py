"""What the results say about us — two opposite mascots, one flat grid.

The point of the slide is that a cohort is not a bloc: both poles of every
axis are held by real people in this room, and that is precisely what makes
the next twenty minutes worth having. The two mascots are read from the cast
by name, so the slide stays true if the cast is reordered.

SPEAKER NOTES:
Two minutes, and they matter. The room has just seen its averages; the risk
is that everyone concludes "so we all think the same". Say the opposite: an
average is a summary, not a portrait. On every axis, this room holds both
poles — some of you are Rapo, some are Lento, and neither is the correct
answer. That disagreement is not a problem to be fixed before the group work
starts: it is the reason the group work will be any good. Then hand over to
the debate.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from postair_data import mascot
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.ai_mark import dd35_overlay

# One axis, its two poles: the clearest possible illustration that both sides
# live in the same room. Read by name — never by position in the cast.
_FACE_OFF = ("Rapo", "Lento")


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    pole = s.project.body.pole_label
    mascot_name = s.project.body.mascot_name
    lead = s.project.body.bullet + s.center_txt
    versus = s.project.titles.register_title + s.center_txt


bs = BlockStyles


def build():
    st_marker("What it says about us")
    left, right = (mascot(n) for n in _FACE_OFF)
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "A cohort is ", (s.project.titles.keyword, "not a bloc"),
                         tag=t.div, toc_lvl="+1", label="What it says about us")
            with g.cell():
                st_info_tooltip(
                    title="Reading a room, not a person",
                    entries=[
                        ("Averages hide diversity", "A cohort at fifty on an axis can be made of "
                         "people all sitting at fifty — or of two halves at zero and a hundred. "
                         "The distribution, not the average, is the interesting object."),
                        ("Both poles are here", "On every one of the nine axes, this room holds "
                         "both sides. That is the normal state of any large group, and it is "
                         "what the next twenty minutes are for."),
                        ("Why it is useful", "Your degree programmes put you in teams. A team "
                         "where everyone shares one posture is fast and blind; a team that holds "
                         "several is slower and much harder to fool."),
                        ("Not a judgement", "No pole is the right answer. The instrument measures "
                         "positions, it does not grade them."),
                    ],
                )
        st_space("v", s.project.spacing.title_gap)
        st_write(bs.lead, "both poles · every axis · ",
                 (s.project.titles.keyword, "in this room"), tag=t.div)
        st_space("v", "2vh")
        # ONE flat grid: mascot · versus · mascot.
        with st_grid(cols="1fr 0.5fr 1fr", gap="1vw",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for side in (left, None, right):
                with g.cell():
                    if side is None:
                        st_write(bs.versus, "vs", tag=t.div)
                        continue
                    with st_block(s.project.cards.pole_cell):
                        st_write(bs.pole, side["pole"], tag=t.div)
                        st_image(s.project.cards.media_center, width="min(16vw, 34vh)",
                                 uri=side["image"],
                                 alt=f"{side['name']}, mascot of the {side['pole']} posture",
                                 overlay=dd35_overlay())
                        st_write(bs.mascot_name, side["name"], tag=t.div)
