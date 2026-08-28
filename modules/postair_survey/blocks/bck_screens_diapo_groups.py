"""The group comparison — écran 29-diapo-groupes.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_admin (diaporama /present, Q15)) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from postair_lang import T, TF
from streamtex import *


_MARKER = {"en": "The group comparison"}
_TITLE = {"en": ("The ", (s.project.titles.keyword, "group"), " comparison")}
_MESSAGES = [
    ({"en": "Groups, side by side"},
     {"en": ("The same aggregates split by group, when the campaign defines "
             "groups.")}),
    ({"en": "Absence is normal here"},
     {"en": ("A room without declared groups shows no comparison — the "
             "section stays away cleanly, it is not a failure.")}),
]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    screen_slide(
        TF(_TITLE, lang),
        '29-diapo-groupes',
        "Desktop view of the /present full-screen slideshow: The group comparison, dark theme",
        [(T(h, lang), T(d, lang)) for h, d in _MESSAGES],
        device="desktop", landscape=True,
        lang=lang
    )
