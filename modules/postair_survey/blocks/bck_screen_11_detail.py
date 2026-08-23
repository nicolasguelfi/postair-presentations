"""Explore — every answer, kept — écran 11-res-detail.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_explore) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from streamtex import *


def build():
    st_marker('Explore your report')
    screen_slide(
        [(s.project.titles.keyword, "Explore"), " — every answer, kept"],
        "11-res-detail",
        "Mobile screen of the report's per-answer detail, grouped by axis, "
        "dark theme",
        [
            ("Statement by statement",
             "All your answers, grouped by axis — the raw material behind "
             "the radar."),
            ("The gesture: open one axis",
             "See which statements pulled you toward a pole; the surprises "
             "are usually here."),
        ],
        toc_label="Explore your report",
        tooltip=("The exploration screens",
                 [("Below the radar", "Per-answer detail, nearest profiles, contrasted "
                   "figures, campaign examples — four ways to interrogate one result."),
                  ("Then the room", "The last screen of this sequence compares you with "
                   "the room's averages — the bridge to the projection.")]),
        zoomImage=150,
        zoomText=170,
    )
