"""Wrap-up — sixteen crises overcome, the seventeenth being written.

The deck's thesis said back to the room, and the bridge to the live survey:
the recomposed world of the AI wave is deliberately unfinished — the
half-written whiteboard, the marker waiting for a hand. The next thing the
room does is pick that marker up: the survey measures their posture.

SPEAKER NOTES:
Close on the numbers, slowly: sixteen crises opened, sixteen overcome. Then
the last line, looking at the room: « the seventeenth is yours ». Move
straight to the survey deck.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from postair_lang import T, TF
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    giant = s.project.body.bullet_giant + s.center_txt
    line = s.project.body.bullet + s.center_txt


bs = BlockStyles

_MARKER = {"en": "Sixteen and one", "fr": "Seize et une"}
_TITLE = {"en": ("Sixteen crises ", (s.project.titles.keyword, "overcome")), "fr": ("Seize crises ", (s.project.titles.keyword, "surmontées"))}
_GIANT = {"en": "16 opened · 16 overcome", "fr": "16 ouvertes · 16 surmontées"}
_LINE = {"en": "rules, uses, postures — every time", "fr": "règles, usages, postures — à chaque fois"}
_YOURS = {"en": ("the seventeenth is ", (s.project.colors.amber, "yours"),
                 " — the survey measures your posture next"), "fr": ("la dix-septième est ", (s.project.colors.amber, "la vôtre"), " — le sondage mesure maintenant votre posture")}


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_center):
        st_write(bs.title, *TF(_TITLE, lang),
                 tag=t.div, toc_lvl="1", label=T(_MARKER, lang))
        st_space("v", s.project.spacing.title_gap)
        st_write(bs.giant, T(_GIANT, lang), tag=t.div)
        st_write(bs.line, T(_LINE, lang), tag=t.div)
        st_space("v", "4vh")
        st_write(bs.line, *TF(_YOURS, lang), tag=t.div)
