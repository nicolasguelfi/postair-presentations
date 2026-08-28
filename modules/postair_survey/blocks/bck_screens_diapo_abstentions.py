"""Where the room abstains — écran 28-diapo-abstentions.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_admin (diaporama /present, Q15)) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from postair_lang import T, TF
from streamtex import *


_MARKER = {"en": "Where the room abstains"}
_TITLE = {"en": ("Where the room ", (s.project.titles.keyword, "abstains"))}
_MESSAGES = [
    ({"en": "The 'no opinion' map"},
     {"en": ("Where the room chose not to answer — counted apart, never as a "
             "middle answer.")}),
    ({"en": "An abstention is information"},
     {"en": ("It names the questions this room does not yet feel equipped "
             "to answer — worth one comment, not a judgement.")}),
]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    screen_slide(
        TF(_TITLE, lang),
        '28-diapo-abstentions',
        "Desktop view of the /present full-screen slideshow: Where the room abstains, dark theme",
        [(T(h, lang), T(d, lang)) for h, d in _MESSAGES],
        device="desktop", landscape=True,
        lang=lang
    )
