"""Sending your answers — écran 06-envoi.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_answering) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.

SPEAKER NOTES:
The one message that matters: nothing leaves the phone before that
tap, and after it the record is anonymous.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from postair_lang import T, TF
from streamtex import *


_MARKER = {"en": "Sending your answers"}
_TITLE = {"en": ("Sending your ", (s.project.titles.keyword, "answers"))}
_MESSAGES = [
    ({"en": "The last screen before your report"},
     {"en": ("It appears once the statements are answered — nothing has left "
             "your phone yet.")}),
    ({"en": "One tap, one record"},
     {"en": ("Send once: the server receives a single anonymous record, and "
             "your personal report is computed on YOUR device.")}),
    ({"en": "The trap: walking away"},
     {"en": ("Answers that are never sent never reach the room's averages — "
             "finish the gesture before you pocket the phone.")}),
]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    screen_slide(
        TF(_TITLE, lang),
        "06-envoi",
        "Mobile screen of the survey send step: the summary before submitting "
        "the answers, dark theme",
        [(T(h, lang), T(d, lang)) for h, d in _MESSAGES],
        zoomImage=190,
        zoomText=120,
        crop = (0, 0, 13, 0),
        lang=lang
    )
