"""Your radar — écran 09-res-radar.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_personal) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from postair_i18n import screen
from postair_lang import T, TF
from streamtex import *


_MARKER = {"en": "Your radar", "fr": "Votre radar"}
_TITLE = {"en": ("Your ", (s.project.titles.keyword, "radar")), "fr": ("Votre ", (s.project.titles.keyword, "radar"))}
_MESSAGES = [
    ({"en": "Nine axes, one shape", "fr": "Neuf axes, une forme"},
     {"en": ("Your position between the two poles of each axis — the whole "
             "survey in one figure."), "fr": "Votre position entre les deux pôles de chaque axe — tout le sondage en une seule image."}),
    ({"en": "How to read it", "fr": "Comment le lire"},
     {"en": ("The centre is one pole, not '{no_opinion}'; distance is a "
             "position, not a score. No shape is better than another."), "fr": "Le centre est un pôle, pas «{nb}{no_opinion}{nb}»{nb}; la distance est une position, pas un score. Aucune forme ne vaut mieux qu'une autre."}),
    ({"en": "The trap: comparing sizes", "fr": "Le piège : comparer les tailles"},
     {"en": ("A small shape is not a small personality — remember the reading "
             "lesson from a few slides ago."), "fr": "Une petite forme n'est pas une petite personnalité — rappelez-vous la leçon de lecture, quelques slides plus tôt."}),
]


def _cite(text: str, lang: str) -> str:
    """Le bouton « Sans opinion » est CITÉ tel que l'application le nomme (gel sumvadis, DD-113)."""
    return text.format(no_opinion=screen("04-question", "action", lang), nb="\u00a0")


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    screen_slide(
        TF(_TITLE, lang),
        "09-res-radar",
        "Mobile screen of the personal nine-axis posture radar, dark theme",
        [(_cite(T(h, lang), lang), _cite(T(d, lang), lang)) for h, d in _MESSAGES],
        zoomImage=180,
        zoomText=130,
        lang=lang
    )
