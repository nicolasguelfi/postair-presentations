"""What it gets wrong — who controls the models? (G8b). Série « the other side ».

Composition de série (ex-gabarit ``limit_slide``, NG 2026-08-11) : UNE image
papier découpé dominante à gauche (``hero_split``), UN message en gros, UNE
ligne punch. Les 4 blocs ``bck_genai_limit_*`` partagent cette composition :
toute évolution s'y réplique à la main.

Le FAIT vit ici (règle NG 2026-08-18) : label, message, punch et detail
s'éditent dans ce bloc. Cette slide est la seule de la série sans citation —
un constat de structure de marché, pas une mesure publiée.

SPEAKER NOTES:
One minute. A handful of companies train the frontier models — then plant the
teaser: what Europe builds itself is a sovereignty question, and the next
session is built on a European model.
"""
# @guideline: postair-minimal

from postair_i18n import ui
from postair_lang import T
from shared_widgets import st_info_tooltip
from streamtex import st_block, st_grid, st_marker, st_space, st_write, st_zoom
from streamtex.enums import Tags as t

from custom.prompts import AI_PREFIX, AI_SUFFIX_LANDSCAPE
from custom.styles import Styles as s
from custom.visuals import staged_hero_image
from postair_pack.components.hero_split import hero_split


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    message = s.project.titles.subtitle + s.center_txt
    punch = s.project.body.body + s.project.colors.amber + s.center_txt + s.bold


bs = BlockStyles

# ── Le revers ───────────────────────────────────────────────────────────────
_MARKER = {"en": "Control"}
_ICON = "🏛️"
_LABEL = {"en": "Who controls the models?"}
_MESSAGE = {"en": "Frontier models\n=\na handful of companies"}
_PUNCH = {"en": "EU sovereignty → Mistral"}
_DETAIL = {"en": ("A handful of companies train the frontier models. What Europe "
                  "builds itself is a sovereignty question — the Mistral session is "
                  "part of the answer.")}

# ── L'image papercut ────────────────────────────────────────────────────────
_IMAGE = "genai_control"
_FALLBACK = "images/genai_control_fallback.svg"
_ALT = ("Papercut giant hands holding amber orbs above a small crowd of "
        "paper silhouettes")
_SCENE = ("Three enormous paper hands rising from the bottom of the frame, "
          "each holding a glowing warm amber paper orb high above a small "
          "crowd of tiny abstract paper silhouettes watching from below.")


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    prompt = AI_PREFIX + _SCENE + AI_SUFFIX_LANDSCAPE
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, _ICON, " ",
                         (s.project.titles.keyword, T(_LABEL, lang)),
                         tag=t.div, toc_lvl="+1", label=T(_LABEL, lang))
            with g.cell():
                st_info_tooltip(title=T(_LABEL, lang),
                                entries=[(ui("documented_note", lang),
                                          T(_DETAIL, lang))])
        st_space("v", s.project.spacing.title_gap)
        # Gabarit par défaut (NG 2026-08-13) : image carrée à gauche ~50 %,
        # message + punch empilés à droite — plus rien sous le pli.
        with hero_split(s, image=lambda: staged_hero_image(
                _IMAGE, prompt, _FALLBACK, alt_ready=_ALT, alt_fallback=_ALT,
                variant="sq")):
            with st_zoom(150):
                st_write(bs.message, T(_MESSAGE, lang), tag=t.div)
                st_space("v", "1vh")
                st_write(bs.punch, T(_PUNCH, lang), tag=t.div)
