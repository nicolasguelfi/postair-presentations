"""The room's radar — écran 23-diapo-radar.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_admin (diaporama /present, Q15)) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from streamtex import *


def build():
    st_marker("The room's radar")
    screen_slide(
        ["The room's ", (s.project.titles.keyword, "radar")],
        '23-diapo-radar',
        "Desktop view of the /present full-screen slideshow: The room's radar, dark theme",
        [
            ('The average shape of the room',
             'Every answer in the room, averaged into one nine-axis profile.'),
            ('What to comment',
             'The most marked axis, the most ambivalent axis, the dominant archetype — three things, then stop.'),
        ],
        device="desktop", landscape=True,
    )
