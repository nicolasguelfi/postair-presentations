"""Your radar — écran 09-res-radar.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_personal) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from postair_lang import T, TF
from streamtex import *


_MARKER = {"en": "Your radar"}
_TITLE = {"en": ("Your ", (s.project.titles.keyword, "radar"))}
_MESSAGES = [
    ({"en": "Nine axes, one shape"},
     {"en": ("Your position between the two poles of each axis — the whole "
             "survey in one figure.")}),
    ({"en": "How to read it"},
     {"en": ("The centre is one pole, not 'no opinion'; distance is a "
             "position, not a score. No shape is better than another.")}),
    ({"en": "The trap: comparing sizes"},
     {"en": ("A small shape is not a small personality — remember the reading "
             "lesson from a few slides ago.")}),
]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    screen_slide(
        TF(_TITLE, lang),
        "09-res-radar",
        "Mobile screen of the personal nine-axis posture radar, dark theme",
        [(T(h, lang), T(d, lang)) for h, d in _MESSAGES],
        zoomImage=190,
        zoomText=140,
        lang=lang
    )
