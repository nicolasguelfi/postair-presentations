"""Hand-over to the debates deck — mascot left, one big button right.

The debate material lives in a single place: the ``postair_debates`` document,
which holds, for each of the eighteen poles, what it claims, three historical
figures who defended it, and three sourced contemporary arguments. This slide
is the door to it, built on the same operator motif as the sumvadis relays.

SPEAKER NOTES:
Switching tabs is a stage gesture — rehearse it, and keep the fallback screen
ready. Do not open the debates deck at the first pole and read it through: it
is a bank, not a talk. Open only the two or three axes the results page showed
as divisive, and let the room argue. Fifteen minutes go fast; two axes done
properly beat five rushed.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from postair_data import mascot
from postair_event import DEBATES_URL
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.ai_mark import dd35_overlay


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    button = s.project.ds.buttons.action_amber_giant
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
                        ("It is a bank, not a talk", "Eighteen poles are prepared; you will open "
                         "two or three. Pick them from the divisive axes shown on the results "
                         "page — never open them in order from the first."),
                        ("What each pole offers", "What the pole claims and its three survey "
                         "statements; three historical figures who defended it, with a portrait, "
                         "a sourced quotation and a presentation video; three sourced "
                         "contemporary arguments; then the two poles face to face."),
                        ("Both sides, always", "The material is symmetrical. Never open one pole "
                         "without its opposite — the room must hear the two best cases, not the "
                         "one the speaker prefers."),
                        ("Rules of speech", "Roaming microphones, two minutes per question, one "
                         "argument for and one against before the show of hands. Nobody defends "
                         "a position in their own name: the mascots carry the postures."),
                        ("Provenance", "The historical profiles are a reconstruction from primary "
                         "sources; they commit their author, never the figure. For living people "
                         "the video is not the figure speaking but a presentation of them."),
                    ],
                )
        # Un franc espace sous le titre (NG 2026-08-03) : la slide ne porte plus
        # qu'un bouton, et un bouton collé à son titre se lit comme une note de
        # bas de page.
        st_space("v", "6vh")
        # La ligne annonçait un nombre de postures à défendre. Elle est retirée :
        # personne ne sait encore combien d'axes la salle aura le temps de
        # traiter, et une promesse chiffrée qu'on ne tient pas s'entend.
        with st_grid(cols="45% 55%", gap="1.5vw",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_image(s.project.cards.media_center, width="min(22vw, 46vh)",
                         uri=voxo["image"],
                         alt=f"{voxo['name']}, the moderator mascot, opening the floor to debate",
                         overlay=dd35_overlay())
                st_write(bs.mascot_name, voxo["name"], tag=t.div)
            with g.cell():
                st_write(bs.button, "Open the debates", tag=t.div,
                         link=DEBATES_URL, no_link_decor=True)
