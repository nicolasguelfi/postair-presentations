"""While you answer — écran 05-progression.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_answering) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.

SPEAKER NOTES:
Say out loud that there is no timer — the room needs to hear it once.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from streamtex import *


def build(lang: str = "en", **_):
    st_marker('While you answer')
    screen_slide(
        ["While you ", (s.project.titles.keyword, "answer")],
        "05-progression",
        "Full mobile page of the survey at the halfway mark: progress bar and "
        "the current statement, dark theme",
        [
            ("Your progress, always on screen",
             "The bar counts the statements you have answered — here, the halfway mark."),
            ("Pause when you need to",
             "You can stop and resume on your device; the survey waits for you."),
            ("The trap: chasing the bar",
             "There is no timer and no prize for speed — a rushed answer is the only "
             "wrong answer this instrument knows."),
        ],
        toc_label="While you answer",
        tooltip=("These screens",
                 [("Real captures", "The actual application, mobile facet, dark theme — "
                   "frozen from the sumvadis media registry, never redrawn."),
                  ("Median duration", "20-40 minutes measured; the progress bar is there "
                   "so nobody has to guess.")]),
        # PLEINE PAGE mobile (facette « complet ») : 1170×2949, la barre de
        # progression EST dans l'image. crop=(haut, droite, bas, gauche).
        zoomImage=130,
        zoomText=120,
        device="mobile-complet",
        landscape=False,
        crop=(0, 0, 15, 0),
        lang=lang
    )

