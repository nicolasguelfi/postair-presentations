"""The archetype waffle — écran 26-diapo-gaufre.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_admin (diaporama /present, Q15)) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from streamtex import *


def build(lang: str = "en", **_):
    st_marker('The archetype waffle')
    screen_slide(
        ["The archetype ", (s.project.titles.keyword, "waffle")],
        '26-diapo-gaufre',
        "Desktop view of the /present full-screen slideshow: The archetype waffle, dark theme",
        [
            ('Each dot is one of you',
             'Every anonymous answer takes its place in an archetype — the room, person by person, name by nobody.'),
            ('Six archetypes at a glance',
             'The distribution of the six archetypes across the room, in one figure.'),
        ],
        device="desktop", landscape=True,
        lang=lang
    )
