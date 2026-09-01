"""BACKUP · Compute bill — la facture d'entraînement, en profondeur de G5.

Annexe backup (planche drafts2 ``backtech=compute``, NG 2026-09-01) : les
réponses toutes prêtes aux questions coût/énergie qui suivent Scale. Le
visuel est le graphe Our World in Data ANNOTÉ des formations AISE
(réutilisation autorisée 2026-09-01 ; OWID est CC-BY, crédité au panneau).

Réconciliation avec G5 (obligation de la planche) : G5 projette la PENTE
(×2,4/an, Cottier 2024) ; ce backup projette des POINTS de cette même pente
(GPT-3 ~5 M$, GPT-4 estimé ~100 M$) — mêmes ordres de grandeur, jamais deux
vérités concurrentes. Les nombres annotés sont des ordres de grandeur
d'enseignement, assumés comme tels au panneau.

SPEAKER NOTES:
Only if asked about cost or energy. Read the two annotated points, then the
teaching image: training GPT-4 took the equivalent of six billion years of
one human computing by hand. If pressed on energy: the gauge on the Scale
slide (IEA 2025) is the sourced number — data centres ≈ 1.5 % of world
electricity, possibly ×2 by 2030.
"""
# @guideline: postair-minimal

from custom.refs import citation
from custom.styles import Styles as s
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    punch = s.project.titles.subtitle + s.project.colors.amber + s.center_txt
    cite = s.project.body.caption + s.center_txt


bs = BlockStyles

#: Réglages datés (2026-09-01) ; ratio mesuré Pillow sur le fichier versionné.
TUNING = {"chart_vh": 56, "chart_ratio": 1.636}

_MARKER = {"en": "Compute bill"}
_TITLE = {"en": ("The ", (s.project.titles.keyword, "training bill"))}
_CHART = "images/trainings/compute_owid.png"
_ALT = ("Our World in Data chart of training compute, annotated: GPT-3 about "
        "5 million dollars, GPT-4 about 100 million")
_PUNCH = {"en": ("GPT-3 ≈ 5 M$ · GPT-4 ≈ 100 M$ (est.)",)}
_CITEKEYS = ["cottier2024-costs"]

_TIP_TITLE = {"en": "The orders of magnitude"}
_TOOLTIP = [
    ({"en": "The chart"},
     {"en": ("Computation used to train notable AI systems (Our World in "
             "Data, CC-BY), annotated for the AISE trainings — log scale: "
             "every gridline is ×10.")}),
    ({"en": "The teaching image"},
     {"en": ("GPT-4's training compute (~10²⁵ FLOP) is on the order of six "
             "billion years of one human calculating by hand — an order of "
             "magnitude, not an accounting line.")}),
    ({"en": "Reconciliation with Scale"},
     {"en": ("The Scale slide projects the SLOPE (×2.4 per year since 2016, "
             "sourced); this chart shows two POINTS on that slope. Same "
             "story, one truth.")}),
    ({"en": "Energy"},
     {"en": ("The sourced number lives on the Scale slide (IEA 2025): data "
             "centres ≈ 1.5 % of world electricity in 2024, possibly more "
             "than double by 2030 — AI as the main driver.")}),
]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(T(h, lang), T(d, lang)) for h, d in _TOOLTIP],
                )
        st_space("v", s.project.spacing.title_gap)
        with st_block(s.project.containers.media_stage(
                TUNING["chart_ratio"], TUNING["chart_vh"])):
            st_image(s.project.cards.media_center, uri=_CHART, alt=_ALT)
        st_space("v", "2vh")
        with st_zoom(130):
            for line in T(_PUNCH, lang):
                st_write(bs.punch, line, tag=t.div)
            st_write(bs.cite, citation(*_CITEKEYS), tag=t.div)
