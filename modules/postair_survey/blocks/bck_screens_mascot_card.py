"""The mascot card — écran 08-res-carte.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_personal) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from postair_lang import T, TF
from streamtex import *


_MARKER = {"en": "The mascot card", "fr": "La carte mascotte"}
_TITLE = {"en": ("The ", (s.project.titles.keyword, "mascot"), " card"), "fr": ("La carte ", (s.project.titles.keyword, "mascotte"), "")}
_MESSAGES = [
    ({"en": "Your postures, carried by mascots", "fr": "Vos postures, portées par des mascottes"},
     {"en": ("The cast you met in this deck — each card shows the pole your "
             "answers lean toward on one axis."), "fr": "La troupe croisée dans ce deck — chaque carte montre le pôle vers lequel vos réponses penchent sur un axe."}),
    ({"en": "Why mascots", "fr": "Pourquoi des mascottes"},
     {"en": ("A figure holds a posture so a person does not have to: opinions "
             "stay depersonalised, here and in the debates."), "fr": "Un personnage porte la posture, pas une personne : les opinions restent dépersonnalisées, ici comme dans les débats."}),
]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    screen_slide(
        TF(_TITLE, lang),
        "08-res-carte",
        "Mobile screen of the report's mascot card: the mascots carrying the "
        "reader's postures, dark theme",
        [(T(h, lang), T(d, lang)) for h, d in _MESSAGES],
        device="desktop",
        landscape=False,
        zoomImage=100,
        zoomText=120,
        lang=lang
    )
