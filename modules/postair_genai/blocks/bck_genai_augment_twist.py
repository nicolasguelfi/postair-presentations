"""The twist — the tool alone is not enough (G6c, augmentation 2/3).

La slide-pivot de la vision collaboration (NG 2026-08-13) : le même essai
randomisé qui donne 92 % à l'IA seule ne donne que 76 % au médecin ÉQUIPÉ
de l'IA — deux points de mieux que sans elle. Trois cartes, trois nombres,
et le message que toute la journée porte : travailler AVEC s'apprend.

Le FAIT vit ici (règle NG 2026-08-18) : les trois nombres, la ligne de
loyauté et le choix des citekeys s'éditent dans ce bloc. La phrase
bibliographique reste dérivée de ``references.bib`` par
``citation()``/``cite`` — clé inconnue = erreur bruyante.

SPEAKER NOTES:
Ninety seconds. Reveal the three numbers left to right and pause after the
third: the room expects 92, sees 76. That gap IS the lecture: access to the
tool is not the skill — piloting it is. This is the strongest argument for
why they are in this amphitheatre at all. Bridge: "and that is a general
truth, not a medical one — watch the judges."
"""
# @guideline: postair-minimal

from custom.prompts import AI_PREFIX, AI_SUFFIX_LANDSCAPE
from custom.refs import citation
from custom.styles import Styles as s
from custom.visuals import staged_hero_image
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.hero_split import hero_split


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    number = s.project.body.name_double + s.center_txt
    number_amber = s.project.body.name_double + s.project.colors.amber + s.center_txt
    who = s.project.body.body + s.center_txt
    message = s.project.body.bullet + s.project.colors.primary + s.center_txt
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

# ── Le fait (ex-entrée « twist » de la section augment) ─────────────────────
#: Jamais projeté, gardé pour la vérifiabilité — l'identifiant d'origine de
#: l'entrée : twist ; son pictogramme d'origine : 🤝.
_LABEL = "The twist: the tool alone is not enough"
_BARS = [
    {"who": "AI alone", "value": "92 %", "tone": "amber"},
    {"who": "Physician alone", "value": "74 %", "tone": "blue"},
    {"who": "Physician + AI", "value": "76 %", "tone": "teal"},
]
_MESSAGE = "Same tool · same doctors · +2 points → collaborating is LEARNED"
_LOYALTY = ("Randomized clinical trial · 50 physicians with their usual "
            "tools · peer-reviewed, 2024")
_DETAIL = ("In a randomized clinical trial, GPT-4 alone scored a median 92 % "
           "on diagnostic reasoning across six complex clinical vignettes; "
           "50 physicians using their conventional resources scored 74 % — "
           "and the physicians GIVEN GPT-4 scored only 76 %. Handing over "
           "the tool changed almost nothing: knowing how to work with it is "
           "a skill in itself, which is exactly what these study years are "
           "for.")
_CITEKEYS = ["goh2024llm"]


def build(lang: str = "en", **_):
    st_marker("The twist")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "The ", (s.project.titles.keyword, "twist"),
                         tag=t.div, toc_lvl="+1", label="The twist")
            with g.cell():
                st_info_tooltip(title=_LABEL,
                                entries=[("Verified at the source",
                                          _DETAIL)])
        st_space("v", s.project.spacing.title_gap)
        with hero_split(s, image=lambda: staged_hero_image(
                "genai_twist", _HERO_PROMPT, "images/genai_twist_fallback.svg",
                alt_ready=("Papercut silhouette and amber orb side by side, studying "
                           "the same paper chart on an easel"),
                alt_fallback=("Papercut silhouette and amber orb studying the same "
                              "paper chart together"),
                variant="sq")):
            for bar in _BARS:
                with st_block(_CARD_TONES[bar["tone"]]):
                    st_write(bs.number_amber if bar["tone"] == "amber" else bs.number,
                             bar["value"], tag=t.div)
                    st_write(bs.who, bar["who"], tag=t.div)
            st_space("v", "0.5vh")
            st_write(bs.message, _MESSAGE, " ",
                     citation(*_CITEKEYS), tag=t.div)
            st_write(bs.loyalty, _LOYALTY, tag=t.div)
