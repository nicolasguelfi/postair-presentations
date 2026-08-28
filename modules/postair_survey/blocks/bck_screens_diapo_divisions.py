"""What divides the room — écran 27-diapo-divisions.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_admin (diaporama /present, Q15)) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.

SPEAKER NOTES:
Slow down on this view: it is the menu of the afternoon's debates.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from streamtex import *


def build(lang: str = "en", **_):
    st_marker('What divides the room')
    screen_slide(
        ["What ", (s.project.titles.keyword, "divides"), " the room"],
        '27-diapo-divisions',
        "Desktop view of the /present full-screen slideshow: What divides the room, dark theme",
        [
            ('The most divisive statements',
             'Ranked by how strongly the room splits on them.'),
            ('The menu of the debates',
             "This view IS the shortlist: the afternoon's arguments start from these lines."),
        ],
        device="desktop", landscape=True,
    )
