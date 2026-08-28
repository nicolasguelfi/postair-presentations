"""You and the room — écran 10-res-salle.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_explore) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.

SPEAKER NOTES:
Slow down here: this comparison is the bridge to the projection
moment.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from streamtex import *


def build(lang: str = "en", **_):
    st_marker('You and the room')
    screen_slide(
        ["You and the ", (s.project.titles.keyword, "room")],
        "10-res-salle",
        "Mobile screen comparing the personal radar with the room's averages, "
        "dark theme",
        [
            ("Your shape against the room's",
             "Your radar overlaid on the room's averages — the moment a personal "
             "result becomes a conversation."),
            ("Minimum five answers",
             "Room aggregates appear only once at least five records are in; "
             "before that, the section waits."),
            ("What comes next",
             "This same comparison, projected wall-size for everyone — the next "
             "slides open it."),
        ],
        zoomImage=190,
        zoomText=140,
        device="mobile",
        landscape=False,
        lang=lang
    )
