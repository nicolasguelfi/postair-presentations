"""The contrasted figures — écran 14-res-contraste.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_explore) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from postair_lang import T, TF
from streamtex import *


_MARKER = {"en": "The contrasted figures", "fr": "Les figures contrastées"}
_TITLE = {"en": ("The ", (s.project.titles.keyword, "contrasted"), " figures"), "fr": ("Les figures ", (s.project.titles.keyword, "en contraste"), " avec vous")}
_MESSAGES = [
    ({"en": "Your opposites, on purpose", "fr": "Vos contraires, à dessein"},
     {"en": "Figures whose posture contrasts most with yours.", "fr": "Les figures dont la posture contraste le plus avec la vôtre."}),
    ({"en": "Why read them", "fr": "Pourquoi les lire"},
     {"en": ("The shortest way to understand the other pole of an axis is a "
             "figure who stands on it — this is where the debates start."), "fr": "Le plus court chemin pour comprendre l'autre pôle d'un axe, c'est une figure qui s'y tient — c'est là que les débats commencent."}),
]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    screen_slide(
        TF(_TITLE, lang),
        "14-res-contraste",
        "Mobile screen of the report's contrasted figures section, dark theme",
        [(T(h, lang), T(d, lang)) for h, d in _MESSAGES],
        zoomImage=165,
        zoomText=140,
        device="mobile",
        landscape=False,
        crop=(0, 0, 46, 0),
        lang=lang
    )
