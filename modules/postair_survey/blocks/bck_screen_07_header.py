"""Your report — the header — écran 07-res-entete.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_personal) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.

SPEAKER NOTES:
The sentence that must land: the report is computed on the device
and belongs to nobody else.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from streamtex import *


def build():
    st_marker('Your report')
    screen_slide(
        ["Your ", (s.project.titles.keyword, "report"), " — the header"],
        "07-res-entete",
        "Mobile screen of the top of the personal survey report, dark theme",
        [
            ("Yours, computed on your device",
             "The moment you send, the report opens — the server never sees it."),
            ("A portrait, not a grade",
             "Nothing on this page is a score; there is no result to be proud or "
             "ashamed of."),
            ("The gesture: scroll",
             "Everything the next slides show lives further down this same page."),
        ],
        toc_label="Your report",
        tooltip=("The personal report",
                 [("Anonymous by design", "Your answers stay on your device; only one "
                   "anonymous record reaches the room's aggregates."),
                  ("Everything below", "Mascot card, radar, per-answer detail, nearest "
                   "profiles, great figures — one scrolling page.")]),
        zoomImage=150,
        zoomText=110,
    )
