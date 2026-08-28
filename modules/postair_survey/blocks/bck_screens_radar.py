"""Your radar — écran 09-res-radar.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_personal) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from postair_lang import T, TF
from streamtex import *


_MARKER = {"en": "Your radar", "fr": "Votre radar"}
_TITLE = {"en": ("Your ", (s.project.titles.keyword, "radar")), "fr": ("Votre ", (s.project.titles.keyword, "radar"))}
_MESSAGES = [
    ({"en": "Nine axes, one shape", "fr": "Neuf axes, une forme"},
     {"en": ("Your position between the two poles of each axis — the whole "
             "survey in one figure."), "fr": "Votre position entre les deux pôles de chaque axe — tout le sondage en une seule image."}),
    ({"en": "How to read it", "fr": "Comment le lire"},
     {"en": ("The centre is one pole, not 'no opinion'; distance is a "
             "position, not a score. No shape is better than another."), "fr": "Le centre est un pôle, pas « Sans opinion » ; la distance est une position, pas un score. Aucune forme ne vaut mieux qu'une autre."}),
    ({"en": "The trap: comparing sizes", "fr": "Le piège : comparer les tailles"},
     {"en": ("A small shape is not a small personality — remember the reading "
             "lesson from a few slides ago."), "fr": "Une petite forme n'est pas une petite personnalité — rappelez-vous la leçon de lecture, quelques slides plus tôt."}),
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
