"""The answering screens — progress (05) and send (06), as the room sees them.

Two sub-slides, one real mobile capture each (Q14 layout: capture left,
useful messages right). Shown while the how-to is still fresh: what the
screen shows, the gesture to make, the trap to avoid — nothing the tooltip
already says better.

SPEAKER NOTES:
Thirty seconds each. On the progress screen, say out loud that there is no
timer — the room needs to hear it once. On the send screen, the one message
that matters: nothing leaves the phone before that tap, and after it the
record is anonymous. Then move on; these screens explain themselves.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from streamtex import *


def build():
    st_marker("While you answer")
    screen_slide(
        ["While you ", (s.project.titles.keyword, "answer")],
        "05-progression",
        "Mobile screen of the survey at the halfway mark: progress bar and "
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
        zoomImage=160,
        zoomText=130,
        device="mobile",
        landscape=False,
        crop=(0, 0, 5, 0),
    )
    st_slide_break(marker_label="Sending your answers",
                   config=SlideBreakConfig(mode=SlideBreakMode.MARKER_ONLY))
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
    )
