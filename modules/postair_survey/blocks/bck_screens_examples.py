"""The campaign's examples — écran 15-res-exemples.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_explore) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from streamtex import *


def build():
    st_marker("The campaign's examples")
    screen_slide(
        ["The campaign's ", (s.project.titles.keyword, "examples")],
        "15-res-exemples",
        "Mobile screen of the report's campaign examples section, dark theme",
        [
            ("Beyond this room",
             "Example profiles published with the campaign — postures to compare "
             "with, before the room's own averages exist."),
            ("The gesture: browse later",
             "Nothing here expires; the report keeps its examples after the "
             "session."),
        ],
        zoomImage=190,
        zoomText=140,
        device="mobile",
        landscape=False,
    )
