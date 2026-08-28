"""The mascot card — écran 08-res-carte.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_personal) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from streamtex import *


def build(lang: str = "en", **_):
    st_marker('The mascot card')
    screen_slide(
        ["The ", (s.project.titles.keyword, "mascot"), " card"],
        "08-res-carte",
        "Mobile screen of the report's mascot card: the mascots carrying the "
        "reader's postures, dark theme",
        [
            ("Your postures, carried by mascots",
             "The cast you met in this deck — each card shows the pole your answers "
             "lean toward on one axis."),
            ("Why mascots",
             "A figure holds a posture so a person does not have to: opinions stay "
             "depersonalised, here and in the debates."),
        ],
        device="desktop",
        landscape=False,
        zoomImage=100,
        zoomText=120,
        lang=lang
    )
