"""The group comparison — écran 29-diapo-groupes.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_admin (diaporama /present, Q15)) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from postair_lang import T, TF
from streamtex import *


_MARKER = {"en": "The group comparison", "fr": "La comparaison par groupe"}
_TITLE = {"en": ("The ", (s.project.titles.keyword, "group"), " comparison"), "fr": ("Les ", (s.project.titles.keyword, "groupes"), " comparés")}
_MESSAGES = [
    ({"en": "Groups, side by side", "fr": "Les groupes, côte à côte"},
     {"en": ("The same aggregates split by group, when the campaign defines "
             "groups."), "fr": "Les mêmes agrégats, ventilés par groupe, quand la campagne définit des groupes."}),
    ({"en": "Absence is normal here", "fr": "Ici, l'absence est normale"},
     {"en": ("A room without declared groups shows no comparison — the "
             "section stays away cleanly, it is not a failure."), "fr": "Une salle sans groupes déclarés n'affiche aucune comparaison — la section s'efface proprement, ce n'est pas une panne."}),
]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    screen_slide(
        TF(_TITLE, lang),
        '29-diapo-groupes',
        "Desktop view of the /present full-screen slideshow: The group comparison, dark theme",
        [(T(h, lang), T(d, lang)) for h, d in _MESSAGES],
        device="desktop", landscape=True,
        lang=lang
    )
