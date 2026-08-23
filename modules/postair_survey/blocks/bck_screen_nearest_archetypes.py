"""The nearest archetypes — écran 12-res-profils.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_explore) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from streamtex import *


def build():
    st_marker('The nearest archetypes')
    screen_slide(
        ["The ", (s.project.titles.keyword, "nearest"), " archetypes"],
        "12-res-profils",
        "Mobile screen of the report's nearest profiles section, dark theme",
        [
            ("Profiles like yours",
             "The archetypes closest to your posture — company, not a verdict."),
            ("The trap: reading it as a box",
             "You are near an archetype, never inside one; the distance is part "
             "of the information."),
        ],
        zoomImage=160,
        zoomText=140,
        device="mobile",
        landscape=False,
        crop=(0, 0, 27, 0),
    )
