"""Your radar — écran 09-res-radar.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_personal) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from streamtex import *


def build():
    st_marker('Your radar')
    screen_slide(
        ["Your ", (s.project.titles.keyword, "radar")],
        "09-res-radar",
        "Mobile screen of the personal nine-axis posture radar, dark theme",
        [
            ("Nine axes, one shape",
             "Your position between the two poles of each axis — the whole survey "
             "in one figure."),
            ("How to read it",
             "The centre is one pole, not 'no opinion'; distance is a position, "
             "not a score. No shape is better than another."),
            ("The trap: comparing sizes",
             "A small shape is not a small personality — remember the reading "
             "lesson from a few slides ago."),
        ],
        zoomImage=190,
        zoomText=140,
    )
