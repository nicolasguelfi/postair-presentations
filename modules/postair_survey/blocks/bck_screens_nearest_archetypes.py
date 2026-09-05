"""The nearest archetypes — écran 12-res-profils.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_explore) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from postair_lang import T, TF
from streamtex import *


_MARKER = {"en": "The nearest archetypes", "fr": "Archétypes les plus proches"}
_TITLE = {"en": ("The ", (s.project.titles.keyword, "nearest"), " archetypes"), "fr": ("Vos ", (s.project.titles.keyword, "plus proches"), " archétypes")}
_MESSAGES = [
    ({"en": "Profiles like yours", "fr": "Profils comme le vôtre"},
     {"en": "The archetypes closest to your posture — company, not a verdict.", "fr": "Les archétypes les plus proches de votre posture — des compagnons, pas un verdict."}),
    ({"en": "The trap: reading it as a box", "fr": "Le piège : y voir une case"},
     {"en": ("You are near an archetype, never inside one; the distance is "
             "part of the information."), "fr": "Vous êtes près d'un archétype, jamais dedans ; la distance fait partie de l'information."}),
]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    screen_slide(
        TF(_TITLE, lang),
        "12-res-profils",
        "Mobile screen of the report's nearest profiles section, dark theme",
        [(T(h, lang), T(d, lang)) for h, d in _MESSAGES],
        zoomImage=200,
        zoomText=140,
        device="mobile",
        landscape=False,
        crop=(0, 0, 53, 0),
        lang=lang
    )
