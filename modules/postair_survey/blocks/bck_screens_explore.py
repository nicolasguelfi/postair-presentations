"""Exploring the report — detail (11), profiles (12), contrast (14),
examples (15), and you against the room (10).

Five sub-slides for the exploratory screens of the personal report (Q14
layout: real mobile capture left, useful messages right). ``10-res-salle``
closes the sequence by design: it is the screen that turns a personal result
into the room's conversation, and it hands over to the results slides that
follow.

SPEAKER NOTES:
Keep a brisk pace — four screens at ~30 seconds, then slow down on the last
one (you and the room): that comparison is the bridge to the projection
moment. If time is short, name the four exploration screens on their first
slide and jump straight to 'You and the room'.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from streamtex import *


def build():
    st_marker("Explore your report")
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
    )
    st_slide_break(marker_label="The nearest profiles",
                   config=SlideBreakConfig(mode=SlideBreakMode.MARKER_ONLY))
    screen_slide(
        ["The ", (s.project.titles.keyword, "nearest"), " profiles"],
        "12-res-profils",
        "Mobile screen of the report's nearest profiles section, dark theme",
        [
            ("Profiles like yours",
             "The archetypes closest to your posture — company, not a verdict."),
            ("The trap: reading it as a box",
             "You are near an archetype, never inside one; the distance is part "
             "of the information."),
        ],
    )
    st_slide_break(marker_label="The contrasted figures",
                   config=SlideBreakConfig(mode=SlideBreakMode.MARKER_ONLY))
    screen_slide(
        ["The ", (s.project.titles.keyword, "contrasted"), " figures"],
        "14-res-contraste",
        "Mobile screen of the report's contrasted figures section, dark theme",
        [
            ("Your opposites, on purpose",
             "Figures whose posture contrasts most with yours."),
            ("Why read them",
             "The shortest way to understand the other pole of an axis is a "
             "figure who stands on it — this is where the debates start."),
        ],
    )
    st_slide_break(marker_label="The campaign's examples",
                   config=SlideBreakConfig(mode=SlideBreakMode.MARKER_ONLY))
    screen_slide(
        ["The campaign's ", (s.project.titles.keyword, "examples")],
        "15-res-exemples",
        "Mobile screen of the report's campaign examples section, dark theme",
        [
            ("Beyond this room",
             "Example profiles published with the campaign — postures to compare "
             "with, before the room's own averages exist."),
            ("The gesture: browse later",
             "Nothing here expires; the report keeps its examples after the "
             "session."),
        ],
    )
    st_slide_break(marker_label="You and the room",
                   config=SlideBreakConfig(mode=SlideBreakMode.MARKER_ONLY))
    screen_slide(
        ["You and the ", (s.project.titles.keyword, "room")],
        "10-res-salle",
        "Mobile screen comparing the personal radar with the room's averages, "
        "dark theme",
        [
            ("Your shape against the room's",
             "Your radar overlaid on the room's averages — the moment a personal "
             "result becomes a conversation."),
            ("Minimum five answers",
             "Room aggregates appear only once at least five records are in; "
             "before that, the section waits."),
            ("What comes next",
             "This same comparison, projected wall-size for everyone — the next "
             "slides open it."),
        ],
    )
