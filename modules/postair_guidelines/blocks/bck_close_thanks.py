"""Closing — thank you! (C3).

The family photo: the eighteen bestiary mascots of the nine axes plus the two
moderators, in one festive grid under the closing line. High energy, applause
slide — the credits live in the tooltip. Mascots are asked by the frozen cast
manifest (``postair_data``), never by file.

SPEAKER NOTES:
One minute, all energy. Read the line — « Welcome to the University of
Luxembourg — make AI yours » — open your arms, let the room applaud the
mascots. Logistics of what follows (break, rooms) is said here if needed.
"""
# @guideline: postair-minimal

from custom.facts import section, text
from custom.styles import Styles as s
from postair_data import axes, mascot
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.ai_mark import dd35_overlay


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    big = s.project.titles.subtitle + s.project.colors.amber + s.center_txt + s.bold
    confetti = s.project.titles.subtitle + s.center_txt
    name = s.project.body.mascot_name + s.center_txt


bs = BlockStyles


def build():
    st_marker("Thank you!")
    data = section("thanks")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, (s.project.titles.keyword, "Thank you"), "!",
                         tag=t.div, toc_lvl="+1", label="Thank you!")
            with g.cell():
                st_info_tooltip(
                    title="Credits",
                    entries=[
                        ("The day", text(data["credits"])),
                        ("The mascots", "38 characters, 100 % generative AI, designed "
                         "in the mascoties studio — each carries one pole of one axis."),
                    ],
                )
        st_space("v", "1vh")
        st_write(bs.confetti, "🎉 🎊 🎉", tag=t.div)
        st_space("v", "0.5vh")
        # La photo de famille : 9 axes × 2 pôles (bestiaire) + les 2 modérateurs.
        family = axes("animals")
        crew = [family[n][side]for n in sorted(family) for side in ("accel", "decel")]
        crew += [{"mascot": m["name"], "image": m["image"]}
                 for m in (mascot("Medio"), mascot("Voxo"))]
        with st_grid(cols=10, gap="0.5vw",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for member in crew:
                with g.cell():
                    st_image(s.project.cards.media_center, width="6vw",
                             uri=member["image"],
                             alt=f"Mascot {member['mascot']}",
                             overlay=dd35_overlay())
                    st_write(bs.name, member["mascot"], tag=t.div)
        st_space("v", "2vh")
        st_write(bs.big, text(data["big"]), tag=t.div)
