"""The detail per question — écran 25-diapo-details.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_admin (diaporama /present, Q15)) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from streamtex import *


def build(lang: str = "en", **_):
    st_marker('The detail per question')
    screen_slide(
        ["The ", (s.project.titles.keyword, "detail"), " per question"],
        '25-diapo-details',
        "Desktop view of the /present full-screen slideshow: The detail per question, dark theme",
        [
            ('Statement by statement',
             'The answer distribution of each of the 54 statements.'),
            ('Where the debate questions come from',
             'Pick the statements where the room splits, not the ones where it agrees.'),
        ],
        device="desktop", landscape=True,
        lang=lang
    )
