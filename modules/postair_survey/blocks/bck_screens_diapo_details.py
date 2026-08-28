"""The detail per question — écran 25-diapo-details.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_admin (diaporama /present, Q15)) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from postair_i18n import ui
from postair_lang import T, TF
from streamtex import *


_MARKER = {"en": "The detail per question", "fr": "Le détail par question"}
_TITLE = {"en": ("The ", (s.project.titles.keyword, "detail"), " per question"), "fr": ("Le ", (s.project.titles.keyword, "détail"), " par question")}
#: La première tête vient du lexique (``statement_by_statement``).
_MSG_STATEMENT = {"en": "The answer distribution of each of the 54 statements.", "fr": "La distribution des réponses à chacun des 54 énoncés."}
_MSG_DEBATE = ({"en": "Where the debate questions come from", "fr": "D'où viennent les questions des débats"},
               {"en": ("Pick the statements where the room splits, not the ones "
                       "where it agrees."), "fr": "Retenez les énoncés qui divisent la salle, pas ceux qui la rassemblent."})


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    screen_slide(
        TF(_TITLE, lang),
        '25-diapo-details',
        "Desktop view of the /present full-screen slideshow: The detail per question, dark theme",
        [
            (ui("statement_by_statement", lang), T(_MSG_STATEMENT, lang)),
            (T(_MSG_DEBATE[0], lang), T(_MSG_DEBATE[1], lang)),
        ],
        device="desktop", landscape=True,
        lang=lang
    )
