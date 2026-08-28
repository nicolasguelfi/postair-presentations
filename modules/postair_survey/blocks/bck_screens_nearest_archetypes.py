"""The nearest archetypes — écran 12-res-profils.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_explore) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from postair_lang import T, TF
from streamtex import *


_MARKER = {"en": "The nearest archetypes"}
_TITLE = {"en": ("The ", (s.project.titles.keyword, "nearest"), " archetypes")}
_MESSAGES = [
    ({"en": "Profiles like yours"},
     {"en": "The archetypes closest to your posture — company, not a verdict."}),
    ({"en": "The trap: reading it as a box"},
     {"en": ("You are near an archetype, never inside one; the distance is "
             "part of the information.")}),
]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    screen_slide(
        TF(_TITLE, lang),
        "12-res-profils",
        "Mobile screen of the report's nearest profiles section, dark theme",
        [(T(h, lang), T(d, lang)) for h, d in _MESSAGES],
        zoomImage=160,
        zoomText=140,
        device="mobile",
        landscape=False,
        crop=(0, 0, 27, 0),
        lang=lang
    )
