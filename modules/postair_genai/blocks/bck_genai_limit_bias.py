"""What it gets wrong — bias (G8a). Série « the other side ».

Composition de série (ex-gabarit ``limit_slide``, NG 2026-08-11) : UNE image
papier découpé dominante à gauche (``hero_split``), UN message en gros, UNE
ligne de preuve sourcée (code de citation visible). Les 4 blocs
``bck_genai_limit_*`` partagent cette composition : toute évolution s'y
réplique à la main.

Le FAIT vit ici (règle NG 2026-08-18) : label, message, punch, detail et
choix des citekeys s'éditent dans ce bloc. La phrase bibliographique reste
dérivée de ``references.bib`` par ``citation()`` — clé inconnue = erreur
bruyante.

SPEAKER NOTES:
One minute. Say the two numbers of the amber line slowly — 34.7 % against
under 1 % — and name the cause: the training data's imbalance, industrialised.
Hover the citation code if challenged.
"""
# @guideline: postair-minimal

from postair_i18n import ui
from postair_lang import T
from shared_widgets import st_info_tooltip
from streamtex import st_block, st_grid, st_marker, st_space, st_write
from streamtex.enums import Tags as t

from custom.prompts import AI_PREFIX, AI_SUFFIX_LANDSCAPE
from custom.refs import citation
from custom.styles import Styles as s
from custom.visuals import staged_hero_image
from postair_pack.components.hero_split import hero_split


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    message = s.project.titles.subtitle + s.center_txt
    punch = s.project.body.body + s.project.colors.amber + s.center_txt + s.bold


bs = BlockStyles

# ── Le revers ───────────────────────────────────────────────────────────────
_MARKER = {"en": "Bias"}
_ICON = "⚖️"
_LABEL = {"en": "Bias in, bias out"}
_MESSAGE = {"en": "Our biases in → industrialised out"}
_PUNCH = {"en": "34.7 % error · darker-skinned women — under 1 % · lighter-skinned men"}
_DETAIL = {"en": ("Commercial face classifiers erred up to 34.7 % on darker-skinned "
                  "women against under 1 % on lighter-skinned men — the training "
                  "data's imbalance, industrialised.")}
_CITEKEYS = ["buolamwini2018-gendershades", "bender2021-parrots"]

# ── L'image papercut ────────────────────────────────────────────────────────
_IMAGE = "genai_bias"
_FALLBACK = "images/genai_mirror_fallback.svg"
_ALT = ("Papercut tilted balance scale, one pan loaded with amber spheres, "
        "a warped paper mirror behind")
_SCENE = ("A large paper balance scale, clearly tilted: one pan low, loaded "
          "with many warm amber paper spheres, the other pan high with a "
          "single small teal sphere. Behind it, a slightly warped paper "
          "mirror leaning against the luminous sky, reflecting the scene "
          "imperfectly.")


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
            st_write(bs.message, T(_MESSAGE, lang), tag=t.div)
            st_space("v", "1vh")
            st_write(bs.punch, T(_PUNCH, lang), " ", citation(*_CITEKEYS), tag=t.div)
