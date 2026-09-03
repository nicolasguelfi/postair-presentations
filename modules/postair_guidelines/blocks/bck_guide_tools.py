"""The tools UL gives you (U6).

One dominant papercut image — the protected M365 bubble versus the open
cloud — and the three lines that matter: Copilot with the UL account is the
supported choice, UniGPT is staff-only for now, free public tools pay
themselves with your data. Equity rules in the tooltip.

Le FAIT vit ici (règle NG 2026-08-18) : les trois lignes outils, les règles
d'équité et le choix des citekeys s'éditent dans ce bloc. La phrase
bibliographique reste dérivée de ``references.bib`` par ``citation()`` — clé
inconnue = erreur bruyante.

Conversion R-i18n (2026-09-03) : chaque texte projeté est une feuille
``{"en", "fr"}`` résolue par ``T``/``TF``.

SPEAKER NOTES:
Two minutes. The image carries the model: inside the bubble, your data stays
UL's; outside, it is the product. Say the equity rule out loud — if a course
requires AI, a free path must exist; premium subscriptions must not buy
grades — it concerns every wallet in the room.
"""
# @guideline: postair-minimal

from custom.prompts import AI_PREFIX, AI_SUFFIX_LANDSCAPE
from custom.refs import citation
from custom.styles import Styles as s
from custom.visuals import hero_image
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    line = s.project.body.bullet + s.center_txt
    accent = s.project.body.bullet + s.project.colors.amber + s.center_txt + s.bold
    cite = s.project.body.caption + s.center_txt


bs = BlockStyles

# ── Le fait : les outils soutenus par l'UL (guidelines, section 3, p.5) ─────
_SUPPORTED = {"en": ("Copilot + UL account = THE supported choice · your "
                     "data stays in UL's M365"),
              "fr": ("Copilot + compte UL = LE choix soutenu · vos données "
                     "restent dans le M365 de l’UL")}
_UNIGPT = {"en": "UniGPT (internal, secure) · staff first",
           "fr": "UniGPT (interne, sécurisé) · le personnel d’abord"}
_OUTSIDE = {"en": "Outside → paid with your data · personal / sensitive = NEVER",
            "fr": "Dehors → payé avec vos données · personnel / sensible = JAMAIS"}
_EQUITY = [
    {"en": "Course REQUIRES AI → a free path must exist",
     "fr": "Un cours EXIGE l’IA → une voie gratuite doit exister"},
    {"en": "Conscientious objection → CAR committee",
     "fr": "Objection de conscience → comité CAR"},
]
_CITEKEYS = ["i2tl2026-guidelines"]

_MARKER = {"en": "UL tools", "fr": "Outils UL"}
_TITLE = {"en": ("The tools ", (s.project.titles.keyword, "UL gives you")),
          "fr": ("Les outils ", (s.project.titles.keyword,
                                 "que l’UL vous donne"))}
_TIP_TITLE = {"en": "Supported tools (guidelines, section 3, p.5)",
              "fr": "Outils soutenus (lignes directrices, section 3, p.5)"}
_LBL_COPILOT = {"en": "Microsoft Copilot (UL account)",
                "fr": "Microsoft Copilot (compte UL)"}
_LBL_PUBLIC = {"en": "Public tools", "fr": "Outils publics"}
_LBL_EQUITY = {"en": "Equity", "fr": "Équité"}
_ACCENT = {"en": "Copilot with your UL account — the supported choice",
           "fr": "Copilot avec votre compte UL — le choix soutenu"}
_LINE = {"en": ("Inside the bubble your data stays UL's · outside, it is "
                "the product "),
         "fr": ("Dans la bulle, vos données restent à l’UL · dehors, elles "
                "sont le produit ")}
#: Jamais projeté, gardé pour la vérifiabilité (entrée « big » de l'ancien
#: facts.json) : « The tools UL gives you ».

_BUBBLE_PROMPT = (
    AI_PREFIX
    + "A large transparent paper bubble dome sheltering a small papercut "
      "campus with a glowing warm amber paper orb inside it, cosy and safe. "
      "Outside the bubble, an open paper sky with scattered clouds and small "
      "paper documents flying away in the wind toward the horizon."
    + AI_SUFFIX_LANDSCAPE
)


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[
                        (T(_LBL_COPILOT, lang), T(_SUPPORTED, lang)),
                        ("UniGPT", T(_UNIGPT, lang)),  # i18n: verbatim
                        (T(_LBL_PUBLIC, lang), T(_OUTSIDE, lang)),
                        *[(T(_LBL_EQUITY, lang), T(e, lang)) for e in _EQUITY],
                    ],
                )
        st_space("v", s.project.spacing.title_gap)
        hero_image(
            "guide_bubble", _BUBBLE_PROMPT, "images/guide_bubble_fallback.svg",
            alt_ready=("Papercut protected bubble sheltering a small campus and an "
                       "amber orb, open windy sky with flying documents outside"),
            alt_fallback=("Papercut bubble protecting a campus, documents flying away "
                          "outside"),
            width="58%",
        )
        st_space("v", "1.5vh")
        st_write(bs.accent, T(_ACCENT, lang), tag=t.div)
        st_write(bs.line, T(_LINE, lang), citation(*_CITEKEYS), tag=t.div)
