"""Now, let's argue — the pivot into the first axis.

Moved here from the opening deck (NG 2026-08-14, ss12-restructure) — the same
movement as bck_disc_wrapup (NG 2026-08-03). In opening this slide was a door
to another document, mascot left and one big button right; now that it LIVES
in the debates deck there is no tab to switch to and no button to press: Voxo
opens the debate, and the next page IS the first axis. What survives is the
promise — two or three axes, the ones where this room splits — and the two
tooltip entries the earlier intro slides do not already carry.

SPEAKER NOTES:
Ten seconds — this slide is a hinge, not a stop. The results page told you
where the room splits; name the two or three axes you will open, out loud,
so the room knows the plan. Then turn the page: the first axis begins. Do
not read the bank in order — two axes done properly beat five rushed.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from postair_data import mascot
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.ai_mark import dd35_overlay


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    lead = s.project.titles.subtitle + s.center_txt
    mascot_name = s.project.body.mascot_name


bs = BlockStyles


def build():
    st_marker("The debates")
    voxo = mascot("Voxo")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "Now, let's ", (s.project.titles.keyword, "argue"),
                         tag=t.div, toc_lvl="+1", label="The debates")
            with g.cell():
                st_info_tooltip(
                    title="Navigating the debates bank",
                    entries=[
                        ("What each pole offers", "What the pole claims and its three survey "
                         "statements; three historical figures who defended it, with a portrait, "
                         "a sourced quotation and a presentation video; three sourced "
                         "contemporary arguments; then the two poles face to face."),
                        ("Both sides, always", "The material is symmetrical. Never open one pole "
                         "without its opposite — the room must hear the two best cases, not the "
                         "one the speaker prefers."),
                    ],
                )
        # Un franc espace sous le titre (NG 2026-08-03) : la slide ne porte
        # qu'une promesse, et une promesse collée à son titre se lit comme une
        # note de bas de page.
        st_space("v", s.project.spacing.title_gap)
        with st_grid(cols="45% 55%", gap="1.5vw",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_image(s.project.cards.media_center, width="min(22vw, 46vh)",
                         uri=voxo["image"],
                         alt=f"{voxo['name']}, the moderator mascot, opening the floor to debate",
                         overlay=dd35_overlay())
                st_write(bs.mascot_name, voxo["name"], tag=t.div)
            with g.cell():
                st_write(bs.lead, "Two or three axes — the ones where ",
                         (s.project.titles.keyword, "this room"), " splits", tag=t.div)
