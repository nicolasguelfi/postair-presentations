"""Justice 1/2 — the case file (G6d, augmentation 3/4).

Découpage NG (2026-08-13, 1 idée = 1 slide) : l'ancienne slide justice
empilait cinq couches de texte et en noyait deux sous le pli. Celle-ci ne
porte plus QUE le résultat Kleinberg : le chiffre, sa lecture télégraphique,
le code de citation — plus la ligne-anecdote en caption AVEC son code (revue
genaipat 2026-09-01 : la clé de l'essai était orpheline, sa phrase vivait en
prose dans l'infobulle — R-bib veut le code visible, jamais la phrase). Le
laboratoire et le garde-fou ont LEUR slide (``bck_genai_augment_justice_lab``).
Gabarit par défaut : image carrée à gauche, contenu à droite.

Exception à la règle « le fait vit dans son bloc » (NG 2026-08-18) : l'entrée
``augment``/``justice`` est PARTAGÉE par les 2 slides justice et reste servie
par ``custom.facts`` — ce qui sert plusieurs slides vit dans ``custom/``. La
phrase bibliographique reste dérivée de ``references.bib`` par
``citation()``/``cite`` — clé inconnue = erreur bruyante.

SPEAKER NOTES:
Ninety seconds. Say the word « simulation » out loud — nobody replaced a
judge; the algorithm predicts the risk the law asks the judge to assess, and
does it better. Bridge: "prediction is one thing — now watch a model JUDGE."
"""
# @guideline: postair-minimal

from custom.facts import citekeys, section, text
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
    headline = s.project.body.name_double + s.project.colors.amber + s.center_txt
    sub = s.project.body.bullet + s.center_txt
    anecdote = s.project.body.caption + s.center_txt


bs = BlockStyles

_HERO_PROMPT = (
    AI_PREFIX
    + "A large paper balance scale standing level: one pan holds a tall neat "
      "stack of paper case files in coral, turquoise and lilac cardstock, "
      "the other pan holds a single glowing warm amber paper orb; behind the "
      "scale a paper courthouse facade with simple cut-out columns. No human "
      "figures, no other sun or orb — the orb on the pan is the only one."
    + AI_SUFFIX_LANDSCAPE
)


def build(lang: str = "en", **_):
    st_marker("Justice")
    fact = next(a for a in section("augment") if a["id"] == "justice")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "Justice — the ",
                         (s.project.titles.keyword, "case file"),
                         tag=t.div, toc_lvl="+1", label="Justice")
            with g.cell():
                st_info_tooltip(title=text(fact["label"]),
                                entries=[("Verified at the source",
                                          text(fact["detail"]))])
        st_space("v", s.project.spacing.title_gap)
        with hero_split(s, image=lambda: staged_hero_image(
                "genai_justice", _HERO_PROMPT, "images/genai_justice_fallback.svg",
                alt_ready=("Papercut balance scale: a stack of paper case files on "
                           "one pan, a glowing amber orb on the other, courthouse "
                           "behind"),
                alt_fallback=("Papercut balance scale weighing paper case files "
                              "against an amber orb"),
                variant="sq")):
            st_write(bs.headline, text(fact["headline"]), tag=t.div)
            st_space("v", "1vh")
            st_write(bs.sub, text(fact["headline_sub"]), " ",
                     citation(*citekeys(fact)), tag=t.div)
            st_space("v", "1vh")
            st_write(bs.anecdote, text(fact["anecdote"]), " ",
                     citation(*fact["anecdote_source"]["citekeys"]), tag=t.div)
