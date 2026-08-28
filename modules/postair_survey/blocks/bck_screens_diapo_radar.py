"""The room's radar — écran 23-diapo-radar.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_admin (diaporama /present, Q15)) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from postair_i18n import ui
from postair_lang import T, TF
from streamtex import *


_MARKER = {"en": "The room's radar"}
_TITLE = {"en": ("The room's ", (s.project.titles.keyword, "radar"))}
_MSG_SHAPE = ({"en": "The average shape of the room"},
              {"en": ("Every answer in the room, averaged into one nine-axis "
                      "profile.")})
#: La tête « What to comment » vient du lexique (partagée avec les slides de
#: résultats).
_MSG_COMMENT = {"en": ("The most marked axis, the most ambivalent axis, the "
                       "dominant archetype — three things, then stop.")}


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    screen_slide(
        TF(_TITLE, lang),
        '23-diapo-radar',
        "Desktop view of the /present full-screen slideshow: The room's radar, dark theme",
        [
            (T(_MSG_SHAPE[0], lang), T(_MSG_SHAPE[1], lang)),
            (ui("what_to_comment", lang), T(_MSG_COMMENT, lang)),
        ],
        device="desktop", landscape=True,
        lang=lang
    )
