"""The great figures — the explorer (18) and one figure's page (19).

Two sub-slides closing the screens tour (Q14 layout: real mobile capture
left, useful messages right). These pages are the doorway to the debates
deck: the same figures, the same engine, the same sourced quotes.

SPEAKER NOTES:
One minute for both. The point to make: the figures are scored by the SAME
instrument the room just answered — that is why comparing yourself with
Cleopatra is a smile AND a legitimate reading. Close with the hand-over:
"this afternoon, these figures argue — and you pick sides."
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from streamtex import *


def build():
    st_marker("The great figures")
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
    )
    st_slide_break(marker_label="A figure's page",
                   config=SlideBreakConfig(mode=SlideBreakMode.MARKER_ONLY))
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
