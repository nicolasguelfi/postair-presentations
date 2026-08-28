"""The room's spread — écran 24-diapo-etendue.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_admin (diaporama /present, Q15)) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from streamtex import *


def build(lang: str = "en", **_):
    st_marker("The room's spread")
    screen_slide(
        ["The room's ", (s.project.titles.keyword, "spread")],
        '24-diapo-etendue',
        "Desktop view of the /present full-screen slideshow: The room's spread, dark theme",
        [
            ('Beyond the average',
             'The interquartile band shows where the middle half of the room actually stands, axis by axis.'),
            ('Narrow is agreement, wide is a debate',
             'Dispersion made visible — this view announces where the afternoon will be lively.'),
        ],
        device="desktop", landscape=True,
    )
