"""Where the room abstains — écran 28-diapo-abstentions.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_admin (diaporama /present, Q15)) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from streamtex import *


def build():
    st_marker('Where the room abstains')
    screen_slide(
        ["Where the room ", (s.project.titles.keyword, "abstains")],
        '28-diapo-abstentions',
        "Desktop view of the /present full-screen slideshow: Where the room abstains, dark theme",
        [
            ("The 'no opinion' map",
             'Where the room chose not to answer — counted apart, never as a middle answer.'),
            ('An abstention is information',
             'It names the questions this room does not yet feel equipped '
             'to answer — worth one comment, not a judgement.'),
        ],
        device="desktop", landscape=True,
    )
