"""The room's spread — écran 24-diapo-etendue.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_admin (diaporama /present, Q15)) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from postair_lang import T, TF
from streamtex import *


_MARKER = {"en": "The room's spread"}
_TITLE = {"en": ("The room's ", (s.project.titles.keyword, "spread"))}
_MESSAGES = [
    ({"en": "Beyond the average"},
     {"en": ("The interquartile band shows where the middle half of the room "
             "actually stands, axis by axis.")}),
    ({"en": "Narrow is agreement, wide is a debate"},
     {"en": ("Dispersion made visible — this view announces where the "
             "afternoon will be lively.")}),
]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    screen_slide(
        TF(_TITLE, lang),
        '24-diapo-etendue',
        "Desktop view of the /present full-screen slideshow: The room's spread, dark theme",
        [(T(h, lang), T(d, lang)) for h, d in _MESSAGES],
        device="desktop", landscape=True,
        lang=lang
    )
