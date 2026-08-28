"""The nearest figures — écran 13-res-figures.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_explore) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from streamtex import *


def build():
    st_marker('The nearest figures')
    screen_slide(
        ["The ", (s.project.titles.keyword, "nearest"), " figures"],
        "13-res-figures",
        "Mobile screen of the report's nearest great figures section, dark theme",
        [
            ("Figures in your company",
             "The great figures closest to your posture — scored by the same "
             "instrument you just answered."),
            ("The trap: reading it as a twin",
             "Nearness measures answers, not lives — an invitation to read the "
             "figure, never an identity."),
        ],
        zoomImage=175,
        zoomText=150,
        device="mobile",
        landscape=False,
        crop=(0, 0, 65, 0),
    )
