"""Already in your pocket (G2) — you have been using AI for years.

Recomposition NG (2026-08-13, gabarit par défaut) : l'image CARRÉE à gauche
sur ~50 %, les cinq étiquettes empilées à droite — l'ancienne grille 3+2 sous
l'image coupait sa seconde rangée au pli. La distinction classique/génératif
ferme la colonne en télégraphique ; le détail vit dans l'infobulle.

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

from postair_pack.components.hero_split import hero_split


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    label = s.project.body.bullet + s.center_txt
    distinction = s.project.body.body + s.project.colors.keyword + s.center_txt


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
        st_space("v", s.project.spacing.title_gap)
        with hero_split(s, image=lambda: hero_image(
                "genai_pocket", _POCKET_PROMPT, "images/genai_pocket_fallback.svg",
                alt_ready=("Papercut smartphone with an amber glowing screen, five "
                           "paper satellites orbiting it: camera, speech bubble, "
                           "globe, film strip, keyboard"),
                alt_fallback=("Stylised smartphone with amber orb screen, five "
                              "orbiting icons: keyboard, camera, film, globe, chat"),
                variant="sq")):
            # Cinq étiquettes, un mot chacune — la salle lit l'image, pas un texte.
            for item in data["items"]:
                with st_block(s.project.cards.blue):
                    st_write(bs.label, item["icon"], "  ",
                             text(item["label"]), tag=t.div)
            st_space("v", "0.5vh")
            st_write(bs.distinction, text(data["distinction"]["classic"]), tag=t.div)
            st_write(bs.distinction, text(data["distinction"]["generative"]), tag=t.div)
