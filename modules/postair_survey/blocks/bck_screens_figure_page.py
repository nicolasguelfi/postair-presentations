"""A figure's page — écran 19-fiche-figure.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_figures) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from postair_lang import T, TF
from streamtex import *


_MARKER = {"en": "A figure's page", "fr": "La page d'une figure"}
_TITLE = {"en": ("A ", (s.project.titles.keyword, "figure's"), " page"), "fr": ("Une ", (s.project.titles.keyword, "figure"), ", sa page")}
_MESSAGES = [
    ({"en": "One figure, one dossier", "fr": "Une figure, un dossier"},
     {"en": ("Portrait, posture on the nine axes, and verbatim quotes with "
             "their references."), "fr": "Portrait, posture sur les neuf axes, et citations verbatim avec leurs références."}),
    ({"en": "A smile, not a verdict", "fr": "Un clin d'œil, pas un verdict"},
     {"en": ("The engine reads public work, not private minds — take the page "
             "as an argument to debate, never as a fact about a person."), "fr": "Le moteur lit une œuvre publique, pas des pensées privées — prenez la page comme un argument à débattre, jamais comme un fait sur une personne."}),
]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    screen_slide(
        TF(_TITLE, lang),
        "19-fiche-figure",
        "Mobile screen of one great figure's page: portrait, posture and "
        "sourced quotes, dark theme",
        [(T(h, lang), T(d, lang)) for h, d in _MESSAGES],
        lang=lang
    )
