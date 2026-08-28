"""Your code — keep it — écran 16-res-code-partage.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_personal) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.

SPEAKER NOTES:
Say « screenshot your code » out loud — the single most useful
instruction of the morning.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from streamtex import *


def build(lang: str = "en", **_):
    st_marker('Your code')
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
