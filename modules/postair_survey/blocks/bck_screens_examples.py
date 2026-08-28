"""The campaign's examples — écran 15-res-exemples.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_explore) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from postair_lang import T, TF
from streamtex import *


_MARKER = {"en": "The campaign's examples"}
_TITLE = {"en": ("The campaign's ", (s.project.titles.keyword, "examples"))}
_MESSAGES = [
    ({"en": "Beyond this room"},
     {"en": ("Example profiles published with the campaign — postures to "
             "compare with, before the room's own averages exist.")}),
    ({"en": "The gesture: browse later"},
     {"en": ("Nothing here expires; the report keeps its examples after the "
             "session.")}),
]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    screen_slide(
        TF(_TITLE, lang),
        "15-res-exemples",
        "Mobile screen of the report's campaign examples section, dark theme",
        [(T(h, lang), T(d, lang)) for h, d in _MESSAGES],
        zoomImage=190,
        zoomText=140,
        device="mobile",
        landscape=False,
        lang=lang
    )
