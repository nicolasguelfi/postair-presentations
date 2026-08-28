"""The great figures — the explorer — écran 18-explorateur.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_figures) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from streamtex import *


def build(lang: str = "en", **_):
    st_marker('The great figures')
    screen_slide(
        ["The great figures — the ", (s.project.titles.keyword, "explorer")],
        "18-explorateur",
        "Mobile screen of the archetype and great figures explorer, dark theme",
        [
            ("Beyond your report",
             "The explorer opens the whole gallery: archetypes and great "
             "figures, scored by the same engine that just scored you."),
            ("The gesture: pick one",
             "Choose a figure and see where it stands on the nine axes — then "
             "find your own distance to it."),
        ],
        toc_label="The great figures",
        tooltip=("The figures pages",
                 [("Same instrument", "Every figure is scored on the same 54 statements "
                   "you answered, from documented positions in their work."),
                  ("Doorway to the debates", "The afternoon's debate deck draws its "
                   "figures, quotes and references from these same dossiers.")]),
        # La capture 18 est une page DÉFILANTE entière (1134×8796) — on ne
        # garde que le premier écran. crop=(haut, droite, bas, gauche).
        crop=(0, 0, 67, 0),
        zoomImage=100,
        zoomText=100,
    )
