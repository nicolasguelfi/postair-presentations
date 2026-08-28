"""A figure's page — écran 19-fiche-figure.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_figures) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from streamtex import *


def build(lang: str = "en", **_):
    st_marker("A figure's page")
    screen_slide(
        ["A ", (s.project.titles.keyword, "figure's"), " page"],
        "19-fiche-figure",
        "Mobile screen of one great figure's page: portrait, posture and "
        "sourced quotes, dark theme",
        [
            ("One figure, one dossier",
             "Portrait, posture on the nine axes, and verbatim quotes with "
             "their references."),
            ("A smile, not a verdict",
             "The engine reads public work, not private minds — take the page "
             "as an argument to debate, never as a fact about a person."),
        ],
    )
