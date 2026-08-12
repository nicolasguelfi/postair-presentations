"""Closing — and now? (C2).

The QR to the hub of the day's presentations, giant, with the four « what
stays with you » lines. URLs and contacts in the tooltip. Data-driven from
``custom.facts`` (section ``next``).

SPEAKER NOTES:
Two minutes. Leave the QR on screen long enough for the slow phones. Say the
one that matters most: your survey result stays at /r/<your code>, anonymous,
yours — and postures move, retake it at the end of the year.
"""
# @guideline: postair-minimal

from custom.facts import section, text
from custom.styles import Styles as s
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    item = s.project.body.bullet + s.center_txt
    url = s.project.titles.subtitle + s.project.colors.keyword + s.center_txt + s.bold


bs = BlockStyles


def build():
    st_marker("And now?")
    data = section("next")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "And ", (s.project.titles.keyword, "now"), "?",
                         tag=t.div, toc_lvl="+1", label="And now?")
            with g.cell():
                st_info_tooltip(
                    title="Everything that stays online",
                    entries=[
                        ("The hub", "postair-collection.streamtex.org — the four decks "
                         "of the day, one card each."),
                        ("Your result", "app.sumvadis.ai/r/<your code> — anonymous, "
                         "computed on your device, kept for you."),
                        ("Contacts", text(data["contacts"])),
                    ],
                )
        st_space("v", "1.5vh")
        # breakpoint : sous 520 px, le QR passe au-dessus de la liste.
        with st_grid(cols="55% 45%", breakpoint="520px",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                # QR versionné (static/images/qr/), généré vers le hub collection.
                st_image(s.project.cards.media_center, width="18vw",
                         uri="images/qr/qr_hub_collection.png",
                         alt="QR code to postair-collection.streamtex.org, the hub of "
                             "the day's presentations")
                st_write(bs.url, text(data["hub_url"]), tag=t.div)
            with g.cell():
                for item in data["items"]:
                    st_write(bs.item, "▸ ", text(item), tag=t.div)
                    st_space("v", "1vh")
