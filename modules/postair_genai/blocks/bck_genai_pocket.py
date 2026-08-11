"""Already in your pocket (G2) — you have been using AI for years.

One dominant image (a smartphone orbited by five everyday AIs) and five short
cards. Data-driven from ``custom.facts``: the block renders, it does not know
a single example. The classic-vs-generative distinction lives in the tooltip.

SPEAKER NOTES:
Two minutes. Start from lived experience, never from theory: everyone in the
room used at least three of these five today. Land the distinction once —
classic AI picks among existing things, generative AI writes the next thing —
it is the hinge of the whole session.
"""
# @guideline: postair-minimal

from custom.facts import section, text
from custom.prompts import AI_PREFIX, AI_SUFFIX_LANDSCAPE
from custom.styles import Styles as s
from custom.visuals import hero_image
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    icon = s.project.titles.subtitle + s.center_txt
    label = s.project.body.caption + s.center_txt + s.bold


bs = BlockStyles

_POCKET_PROMPT = (
    AI_PREFIX
    + "A large paper smartphone standing upright at the centre, its screen a "
      "warm amber paper glow, with five small colourful paper satellites "
      "orbiting around it on visible paper orbit rings: a tiny camera, a "
      "speech bubble, a globe, a film strip and a keyboard, all cut from "
      "bright cardstock."
    + AI_SUFFIX_LANDSCAPE
)


def build():
    st_marker("In your pocket")
    data = section("pocket")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "Already in ", (s.project.titles.keyword, "your pocket"),
                         tag=t.div, toc_lvl="+1", label="In your pocket")
            with g.cell():
                st_info_tooltip(
                    title="Two kinds of AI",
                    entries=[
                        ("Classic AI", text(data["distinction"]["classic"])),
                        ("Generative AI", text(data["distinction"]["generative"])),
                        *[(f"{item['icon']} {text(item['label'])}", text(item["detail"]))
                          for item in data["items"]],
                    ],
                )
        st_space("v", "1vh")
        hero_image(
            "genai_pocket", _POCKET_PROMPT, "images/genai_pocket_fallback.svg",
            alt_ready=("Papercut smartphone with an amber glowing screen, five paper "
                       "satellites orbiting it: camera, speech bubble, globe, film "
                       "strip, keyboard"),
            alt_fallback=("Stylised smartphone with amber orb screen, five orbiting "
                          "icons: keyboard, camera, film, globe, chat"),
            width="62%",
        )
        st_space("v", "1.5vh")
        # Cinq étiquettes, un mot chacune — la salle lit l'image, pas un texte.
        with st_grid(cols=s.project.grids.balanced(len(data["items"])), gap="1vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_top) as g:
            for item in data["items"]:
                with g.cell(), st_block(s.project.cards.blue):
                    st_write(bs.icon, item["icon"], tag=t.div)
                    st_write(bs.label, text(item["label"]), tag=t.div)
