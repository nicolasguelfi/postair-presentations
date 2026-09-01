"""BACKUP · Moral Machine — 40 millions de décisions, et le contrepoint.

Annexe backup (planche drafts2 ``backsoc=moralmachine``, NG 2026-09-01) : le
matériel signature des formations AISE pour la question récurrente « et la
voiture autonome, elle choisit qui ? ». Le graphe des préférences par pays
est réutilisé tel quel (copyright NG levé 2026-09-01 ; visuel dérivé de
l'expérience MIT, crédité par la clé ``awad2018-moralmachine`` VISIBLE). La
chute est le contrepoint réglementaire : la commission d'éthique allemande
INTERDIT précisément ce que la foule préfère (règle 9 — aucune distinction
par caractéristiques personnelles), clé ``bmvi2017-ethics``.

Frontière inter-decks (con documenté de la planche) : l'axe éthique des
debates traite les dilemmes en discussion ; ce backup ne fait que RÉPONDRE à
une question de salle avec deux faits sourcés — pas un exposé.

SPEAKER NOTES:
Only if asked about autonomous vehicles or « who does the AI choose? ».
Three findings, one breath each: spare humans over animals, spare the young,
spare the many. Then the twist that makes the room think: the only official
ethics rules in force (Germany, 2017) FORBID choosing by age or gender —
what the crowd wants is what the law prohibits. Ethics is not a poll.
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
    finding = s.project.body.bullet + s.center_txt + s.bold
    punch = s.project.titles.subtitle + s.project.colors.amber + s.center_txt
    cite = s.project.body.caption + s.center_txt


bs = BlockStyles

#: Réglages datés (2026-09-01) ; ratio mesuré Pillow sur le fichier versionné.
TUNING = {"chart_vh": 34, "chart_ratio": 2.648}

_MARKER = {"en": "Moral Machine"}
_TITLE = {"en": ("40 million ", (s.project.titles.keyword, "moral decisions"))}
_CHART = "images/trainings/moralmachine_prefs.png"
_ALT = ("Moral Machine country-level preferences chart: sparing the young, "
        "by country, France at one extreme")
_FINDINGS = {"en": "spare humans · spare the YOUNG · spare the many"}
_PUNCH = {"en": ("the German ethics rules FORBID exactly that",
                 "no distinction by age, gender, constitution — rule 9")}
_CITE_STUDY = ["awad2018-moralmachine"]
_CITE_RULES = ["bmvi2017-ethics"]

_TIP_TITLE = {"en": "The experiment, precisely"}
_TOOLTIP = [
    ({"en": "Moral Machine"},
     {"en": ("An MIT online experiment: dilemmas of an autonomous car that "
             "must crash — 40 million decisions from 233 countries and "
             "territories (published 2018).")}),
    ({"en": "The three global preferences"},
     {"en": ("Spare humans over animals, spare the young over the old, spare "
             "more lives over fewer — with marked cultural variations "
             "between country clusters.")}),
    ({"en": "The counterpoint"},
     {"en": ("Germany's ethics commission (2017), the only official rules of "
             "that era: technology must PREVENT dilemmas (rule 5), and any "
             "distinction on personal features — age, gender, constitution — "
             "is strictly prohibited (rule 9).")}),
    ({"en": "The lesson"},
     {"en": ("What crowds prefer and what ethics commissions allow can point "
             "in opposite directions — « ethics by poll » is not ethics. The "
             "debates session digs deeper this afternoon.")}),
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
        with st_zoom(120):
            st_write(bs.finding, T(_FINDINGS, lang), " ",
                     citation(*_CITE_STUDY), tag=t.div)
        st_space("v", "2vh")
        with st_block(s.project.containers.media_stage(
                TUNING["chart_ratio"], TUNING["chart_vh"])):
            st_image(s.project.cards.media_center, uri=_CHART, alt=_ALT)
        st_space("v", "3vh")
        with st_zoom(130):
            for line in T(_PUNCH, lang):
                st_write(bs.punch, line, tag=t.div)
            st_write(bs.cite, citation(*_CITE_RULES), tag=t.div)
