"""The twist — the tool alone is not enough (G6c, augmentation 2/3).

La slide-pivot de la vision collaboration (NG 2026-08-13) : le même essai
randomisé qui donne 92 % à l'IA seule ne donne que 76 % au médecin ÉQUIPÉ
de l'IA — deux points de mieux que sans elle. Trois cartes, trois nombres,
et le message que toute la journée porte : travailler AVEC s'apprend.

SPEAKER NOTES:
Ninety seconds. Reveal the three numbers left to right and pause after the
third: the room expects 92, sees 76. That gap IS the lecture: access to the
tool is not the skill — piloting it is. This is the strongest argument for
why they are in this amphitheatre at all. Bridge: "and that is a general
truth, not a medical one — watch the judges."
"""
# @guideline: postair-minimal

from custom.facts import citekeys, section, text
from custom.prompts import AI_PREFIX, AI_SUFFIX_LANDSCAPE
from custom.refs import citation
from custom.styles import Styles as s
from custom.visuals import hero_image
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    number = s.project.body.name_double + s.center_txt
    number_amber = s.project.body.name_double + s.project.colors.amber + s.center_txt
    who = s.project.body.body + s.center_txt
    message = s.project.titles.subtitle + s.center_txt
    loyalty = s.project.body.caption + s.center_txt


bs = BlockStyles

_CARD_TONES = {"amber": s.project.cards.amber, "blue": s.project.cards.blue,
               "teal": s.project.cards.teal}

_HERO_PROMPT = (
    AI_PREFIX
    + "One abstract paper human silhouette seen from behind, studying a "
      "large paper chart of colourful cut-out bars pinned on a paper easel; "
      "beside the silhouette, at shoulder height, floats a glowing warm "
      "amber paper orb — a plain sphere with no body, no limbs and no face, "
      "also turned toward the chart. Exactly one orb in the image."
    + AI_SUFFIX_LANDSCAPE
)


def build():
    st_marker("The twist")
    fact = next(a for a in section("augment") if a["id"] == "twist")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "The twist: the tool ",
                         (s.project.titles.keyword, "alone"), " is not enough",
                         tag=t.div, toc_lvl="+1", label="The twist")
            with g.cell():
                st_info_tooltip(title=text(fact["label"]),
                                entries=[("Verified at the source",
                                          text(fact["detail"]))])
        st_space("v", "1vh")
        hero_image(
            "genai_twist", _HERO_PROMPT, "images/genai_twist_fallback.svg",
            alt_ready=("Papercut silhouette and amber orb side by side, studying the "
                       "same paper chart on an easel"),
            alt_fallback=("Papercut silhouette and amber orb studying the same paper "
                          "chart together"),
            width="46%",
        )
        st_space("v", "1.5vh")
        with st_grid(cols=s.project.grids.balanced(len(fact["bars"])), gap="1.5vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for bar in fact["bars"]:
                with g.cell(), st_block(_CARD_TONES[bar["tone"]]):
                    st_write(bs.number_amber if bar["tone"] == "amber" else bs.number,
                             text(bar["value"]), tag=t.div)
                    st_write(bs.who, text(bar["who"]), tag=t.div)
        st_space("v", "1.5vh")
        st_write(bs.message, text(fact["message"]), " ",
                 citation(*citekeys(fact)), tag=t.div)
        st_space("v", "0.5vh")
        st_write(bs.loyalty, text(fact["loyalty"]), tag=t.div)
