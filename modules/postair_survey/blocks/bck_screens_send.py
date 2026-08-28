"""Sending your answers — écran 06-envoi.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_answering) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.

SPEAKER NOTES:
The one message that matters: nothing leaves the phone before that
tap, and after it the record is anonymous.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from streamtex import *


def build():
    st_marker('Sending your answers')
    screen_slide(
        ["Sending your ", (s.project.titles.keyword, "answers")],
        "06-envoi",
        "Mobile screen of the survey send step: the summary before submitting "
        "the answers, dark theme",
        [
            ("The last screen before your report",
             "It appears once the statements are answered — nothing has left your "
             "phone yet."),
            ("One tap, one record",
             "Send once: the server receives a single anonymous record, and your "
             "personal report is computed on YOUR device."),
            ("The trap: walking away",
             "Answers that are never sent never reach the room's averages — finish "
             "the gesture before you pocket the phone."),
        ],
        zoomImage=190,
        zoomText=120,
        crop = (0, 0, 13, 0),
    )
