"""The nearest figures — écran 13-res-figures.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_explore) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from postair_lang import T, TF
from streamtex import *


_MARKER = {"en": "The nearest figures"}
_TITLE = {"en": ("The ", (s.project.titles.keyword, "nearest"), " figures")}
_MESSAGES = [
    ({"en": "Figures in your company"},
     {"en": ("The great figures closest to your posture — scored by the same "
             "instrument you just answered.")}),
    ({"en": "The trap: reading it as a twin"},
     {"en": ("Nearness measures answers, not lives — an invitation to read the "
             "figure, never an identity.")}),
]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    screen_slide(
        TF(_TITLE, lang),
        "13-res-figures",
        "Mobile screen of the report's nearest great figures section, dark theme",
        [(T(h, lang), T(d, lang)) for h, d in _MESSAGES],
        zoomImage=175,
        zoomText=150,
        device="mobile",
        landscape=False,
        crop=(0, 0, 65, 0),
        lang=lang
    )
