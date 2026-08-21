"""The personal report — header (07), mascot card (08), radar (09), code (16).

Four sub-slides walking the room through the report they are about to
receive, in the order the report itself shows them (Q14 layout: real mobile
capture left, useful messages right). The radar screen returns here on
purpose after the poster: this time the room learns to read it.

SPEAKER NOTES:
About three minutes for the four screens. The two sentences that must land:
the report is computed on the device and belongs to nobody else; and the
personal code at the end is the ONLY way back to it — say "screenshot your
code" out loud, it is the single most useful instruction of the morning.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from streamtex import *


def build():
    st_marker("Your report")
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
    st_slide_break(marker_label="The mascot card",
                   config=SlideBreakConfig(mode=SlideBreakMode.MARKER_ONLY))
    screen_slide(
        ["The ", (s.project.titles.keyword, "mascot"), " card"],
        "08-res-carte",
        "Mobile screen of the report's mascot card: the mascots carrying the "
        "reader's postures, dark theme",
        [
            ("Your postures, carried by mascots",
             "The cast you met in this deck — each card shows the pole your answers "
             "lean toward on one axis."),
            ("Why mascots",
             "A figure holds a posture so a person does not have to: opinions stay "
             "depersonalised, here and in the debates."),
        ],
        device="desktop",
        landscape=False,
        zoomImage=250,
        zoomText=120,
    )
    st_slide_break(marker_label="Your radar",
                   config=SlideBreakConfig(mode=SlideBreakMode.MARKER_ONLY))
    screen_slide(
        ["Your ", (s.project.titles.keyword, "radar")],
        "09-res-radar",
        "Mobile screen of the personal nine-axis posture radar, dark theme",
        [
            ("Nine axes, one shape",
             "Your position between the two poles of each axis — the whole survey "
             "in one figure."),
            ("How to read it",
             "The centre is one pole, not 'no opinion'; distance is a position, "
             "not a score. No shape is better than another."),
            ("The trap: comparing sizes",
             "A small shape is not a small personality — remember the reading "
             "lesson from a few slides ago."),
        ],
        zoomImage=190,
        zoomText=140,
    )
    st_slide_break(marker_label="Your code",
                   config=SlideBreakConfig(mode=SlideBreakMode.MARKER_ONLY))
    screen_slide(
        ["Your ", (s.project.titles.keyword, "code"), " — keep it"],
        "16-res-code-partage",
        "Mobile screen of the end of the report: personal retrieval code, "
        "share and download actions, dark theme",
        [
            ("The only way back",
             "The personal code at the end of the report reopens your result at "
             "app.sumvadis.ai/r — screenshot it now."),
            ("No account, no recovery",
             "Anonymous means exactly this: no email, no login — lose the code "
             "and nobody can find your report again."),
            ("Share on your terms",
             "Download or share the report if you wish; nothing is published "
             "by default."),
        ],
        zoomImage=200,
        zoomText=140,
    )
