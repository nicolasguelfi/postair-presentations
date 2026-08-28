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
from postair_lang import T, TF
from streamtex import *


_MARKER = {"en": "Your code"}
_TITLE = {"en": ("Your ", (s.project.titles.keyword, "code"), " — keep it")}
_MESSAGES = [
    ({"en": "The only way back"},
     {"en": ("The personal code at the end of the report reopens your result "
             "at app.sumvadis.ai/r — screenshot it now.")}),
    ({"en": "No account, no recovery"},
     {"en": ("Anonymous means exactly this: no email, no login — lose the code "
             "and nobody can find your report again.")}),
    ({"en": "Share on your terms"},
     {"en": ("Download or share the report if you wish; nothing is published "
             "by default.")}),
]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    screen_slide(
        TF(_TITLE, lang),
        "16-res-code-partage",
        "Mobile screen of the end of the report: personal retrieval code, "
        "share and download actions, dark theme",
        [(T(h, lang), T(d, lang)) for h, d in _MESSAGES],
        zoomImage=200,
        zoomText=140,
        lang=lang
    )
