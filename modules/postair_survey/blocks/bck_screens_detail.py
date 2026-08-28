"""Explore — every answer, kept — écran 11-res-detail.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_explore) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from postair_i18n import ui
from postair_lang import T, TF
from streamtex import *


_MARKER = {"en": "Explore your report"}
_TITLE = {"en": ((s.project.titles.keyword, "Explore"), " — every answer, kept")}
#: La première tête vient du lexique (``statement_by_statement``, partagée
#: avec le détail par question du diaporama).
_MSG_STATEMENT = {"en": ("All your answers, grouped by axis — the raw material "
                         "behind the radar.")}
_MSG_GESTURE = ({"en": "The gesture: open one axis"},
                {"en": ("See which statements pulled you toward a pole; the "
                        "surprises are usually here.")})
_TIP_TITLE = {"en": "The exploration screens"}
_TIP = [
    ({"en": "Below the radar"},
     {"en": ("Per-answer detail, nearest profiles, contrasted figures, "
             "campaign examples — four ways to interrogate one result.")}),
    ({"en": "Then the room"},
     {"en": ("The last screen of this sequence compares you with the room's "
             "averages — the bridge to the projection.")}),
]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    screen_slide(
        TF(_TITLE, lang),
        "11-res-detail",
        "Mobile screen of the report's per-answer detail, grouped by axis, "
        "dark theme",
        [
            (ui("statement_by_statement", lang), T(_MSG_STATEMENT, lang)),
            (T(_MSG_GESTURE[0], lang), T(_MSG_GESTURE[1], lang)),
        ],
        toc_label=T(_MARKER, lang),
        tooltip=(T(_TIP_TITLE, lang), [(T(h, lang), T(d, lang)) for h, d in _TIP]),
        zoomImage=150,
        zoomText=170,
        lang=lang
    )
