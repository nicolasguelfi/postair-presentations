"""The group comparison — écran 29-diapo-groupes.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_admin (diaporama /present, Q15)) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from streamtex import *


def build():
    st_marker('The group comparison')
    screen_slide(
        ["The ", (s.project.titles.keyword, "group"), " comparison"],
        '29-diapo-groupes',
        "Desktop view of the /present full-screen slideshow: The group comparison, dark theme",
        [
            ('Groups, side by side',
             'The same aggregates split by group, when the campaign defines groups.'),
            ('Absence is normal here',
             'A room without declared groups shows no comparison — the '
             'section stays away cleanly, it is not a failure.'),
        ],
        device="desktop", landscape=True,
    )
