"""The Results — le poster qui ouvre la séquence des écrans de résultats.

Remplace l'ancien ``bck_screens_poster`` (capture du radar) par UNE image
générée dans la ligne graphique PAPERCUT (NG 2026-08-23) : la slide n'a que
le titre et l'illustration — l'ancre TOC de la partie, et un battement
visuel avant la série d'écrans du rapport participant.

Tant que ``results_poster`` n'existe pas dans l'historique managé, la slide
montre le radar vide (même règle que la roue : une slide qui attend une
image affiche un trou, jamais). L'image se génère depuis le panneau
d'édition (``editable`` en local) ; ``st_image`` préfère de lui-même la
version managée dès qu'elle est là.

SPEAKER NOTES:
One sentence, then silence: "this is where you are going — YOUR results, on
your phone, in about twenty minutes." The screens themselves follow, one by
one; nothing to explain on this slide.
"""
# @guideline: postair-minimal

from pathlib import Path

from custom.config import IS_EDITABLE
from custom.prompts import AI_PREFIX, AI_SUFFIX_LANDSCAPE
from custom.styles import Styles as s
from custom.visuals import is_synthetic
from postair_pack.components.ai_mark import dd35_overlay
from streamtex import *
from streamtex.enums import Tags as t

#: Le nom managé du poster, et l'endroit où l'éditeur l'enregistre.
_POSTER = "results_poster"
_MANAGED = Path(__file__).parent.parent / "static" / "images" / "managed"

#: Le repli tant que l'illustration n'est pas générée : le radar vide.
_FALLBACK = "images/postair_radar_question.svg"

POSTER_PROMPT = (
    AI_PREFIX
    + "A giant paper-cut smartphone standing upright like a joyful monument "
      "at the centre of a fairground, its screen showing a bright nine-spoke "
      "paper radar chart with a coloured shape pinned inside it. A cheerful "
      "crowd of abstract paper silhouettes gathers around, many holding up "
      "their own small paper phones with tiny radar shapes on them, paper "
      "confetti drifting in the air. A warm amber paper sun glows above the "
      "scene."
    + AI_SUFFIX_LANDSCAPE
)


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt


bs = BlockStyles


def build(lang: str = "en", **_):
    st_marker("The Results — poster")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                with st_zoom(150):
                    st_write(bs.title, "The ", (s.project.titles.keyword, "Results"),
                         tag=t.div, toc_lvl="1", label="The Results")
            with g.cell():
                st_space("h", "0.5vw")
        st_space("v", "1vh")
        ready = (_MANAGED / f"{_POSTER}.webp").exists()
        st_image(s.project.cards.media_center, width="80%",
                 uri="" if ready else _FALLBACK,
                 alt=("Papercut poster: a giant paper smartphone showing a "
                      "nine-spoke radar chart, surrounded by a cheerful crowd "
                      "of paper silhouettes holding their own phones") if ready
                 else ("Empty nine-axis POSTAIR radar chart with a large "
                       "question mark in the centre"),
                 editable=IS_EDITABLE, name=_POSTER,
                 prompt=POSTER_PROMPT, provider="openai", ai_size="1536x1024",
                 overlay=dd35_overlay(ready and is_synthetic(_POSTER)))
