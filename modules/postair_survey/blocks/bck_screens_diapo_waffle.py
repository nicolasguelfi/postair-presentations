"""The archetype waffle — écran 26-diapo-gaufre.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_admin (diaporama /present, Q15)) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from postair_lang import T, TF
from streamtex import *


_MARKER = {"en": "The archetype waffle", "fr": "La gaufre des archétypes"}
_TITLE = {"en": ("The archetype ", (s.project.titles.keyword, "waffle")), "fr": ("Les archétypes en ", (s.project.titles.keyword, "gaufre"))}
_MESSAGES = [
    ({"en": "Each dot is one of you", "fr": "Chaque point est l'un d'entre vous"},
     {"en": ("Every anonymous answer takes its place in an archetype — the "
             "room, person by person, name by nobody."), "fr": "Chaque réponse anonyme prend sa place dans un archétype — la salle, personne par personne, sans nommer personne."}),
    ({"en": "Six archetypes at a glance", "fr": "Six archétypes d'un coup d'œil"},
     {"en": ("The distribution of the six archetypes across the room, in one "
             "figure."), "fr": "La répartition des six archétypes dans la salle, en une seule image."}),
]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    screen_slide(
        TF(_TITLE, lang),
        '26-diapo-gaufre',
        "Desktop view of the /present full-screen slideshow: The archetype waffle, dark theme",
        [(T(h, lang), T(d, lang)) for h, d in _MESSAGES],
        device="desktop", landscape=True,
        lang=lang
    )
