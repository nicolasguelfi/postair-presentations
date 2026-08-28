"""What divides the room — écran 27-diapo-divisions.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_admin (diaporama /present, Q15)) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.

SPEAKER NOTES:
Slow down on this view: it is the menu of the afternoon's debates.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from postair_lang import T, TF
from streamtex import *


_MARKER = {"en": "What divides the room", "fr": "Ce qui divise la salle"}
_TITLE = {"en": ("What ", (s.project.titles.keyword, "divides"), " the room"), "fr": ("Ce qui ", (s.project.titles.keyword, "divise"), " la salle")}
_MESSAGES = [
    ({"en": "The most divisive statements", "fr": "Les énoncés les plus clivants"},
     {"en": "Ranked by how strongly the room splits on them.", "fr": "Classés par l'ampleur du clivage dans la salle."}),
    ({"en": "The menu of the debates", "fr": "Le menu des débats"},
     {"en": ("This view IS the shortlist: the afternoon's arguments start from "
             "these lines."), "fr": "Cette vue EST la sélection : les débats de l'après-midi partent de ces lignes."}),
]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    screen_slide(
        TF(_TITLE, lang),
        '27-diapo-divisions',
        "Desktop view of the /present full-screen slideshow: What divides the room, dark theme",
        [(T(h, lang), T(d, lang)) for h, d in _MESSAGES],
        device="desktop", landscape=True,
        lang=lang
    )
