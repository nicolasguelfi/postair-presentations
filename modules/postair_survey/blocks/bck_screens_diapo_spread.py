"""The room's spread — écran 24-diapo-etendue.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_admin (diaporama /present, Q15)) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from postair_lang import T, TF
from streamtex import *


_MARKER = {"en": "The room's spread", "fr": "L'étendue de la salle"}
_TITLE = {"en": ("The room's ", (s.project.titles.keyword, "spread")), "fr": ("La salle, son ", (s.project.titles.keyword, "étendue"))}
_MESSAGES = [
    ({"en": "Beyond the average", "fr": "Au-delà de la moyenne"},
     {"en": ("The interquartile band shows where the middle half of the room "
             "actually stands, axis by axis."), "fr": "La bande interquartile montre où se situe vraiment la moitié centrale de la salle, axe par axe."}),
    ({"en": "Narrow is agreement, wide is a debate", "fr": "Étroite, un accord ; large, un débat"},
     {"en": ("Dispersion made visible — this view announces where the "
             "afternoon will be lively."), "fr": "La dispersion rendue visible — cette vue annonce où l'après-midi sera animé."}),
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
