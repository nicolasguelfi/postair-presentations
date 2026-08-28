"""While you answer — écran 05-progression.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_answering) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.

SPEAKER NOTES:
Say out loud that there is no timer — the room needs to hear it once.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from postair_lang import T, TF
from streamtex import *


_MARKER = {"en": "While you answer", "fr": "Pendant que vous répondez"}
_TITLE = {"en": ("While you ", (s.project.titles.keyword, "answer")), "fr": ("Pendant que vous ", (s.project.titles.keyword, "répondez"))}
_MESSAGES = [
    ({"en": "Your progress, always on screen", "fr": "Votre progression, toujours à l'écran"},
     {"en": ("The bar counts the statements you have answered — here, the "
             "halfway mark."), "fr": "La barre compte les énoncés auxquels vous avez répondu — ici, la moitié du parcours."}),
    ({"en": "Pause when you need to", "fr": "Faites une pause si besoin"},
     {"en": "You can stop and resume on your device; the survey waits for you.", "fr": "Vous pouvez arrêter et reprendre sur votre appareil ; le sondage vous attend."}),
    ({"en": "The trap: chasing the bar", "fr": "Le piège : courir après la barre"},
     {"en": ("There is no timer and no prize for speed — a rushed answer is "
             "the only wrong answer this instrument knows."), "fr": "Pas de chrono, pas de prime à la vitesse — une réponse bâclée est la seule mauvaise réponse que connaît cet instrument."}),
]
_TIP_TITLE = {"en": "These screens", "fr": "Ces écrans"}
_TIP = [
    ({"en": "Real captures", "fr": "Captures réelles"},
     {"en": ("The actual application, mobile facet, dark theme — frozen from "
             "the sumvadis media registry, never redrawn."), "fr": "La vraie application, facette mobile, thème sombre — gelée depuis le registre média de sumvadis, jamais redessinée."}),
    ({"en": "Median duration", "fr": "Durée médiane"},
     {"en": ("20-40 minutes measured; the progress bar is there so nobody "
             "has to guess."), "fr": "20-40 minutes mesurées ; la barre de progression est là pour que personne n'ait à deviner."}),
]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    screen_slide(
        TF(_TITLE, lang),
        "05-progression",
        "Full mobile page of the survey at the halfway mark: progress bar and "
        "the current statement, dark theme",
        [(T(h, lang), T(d, lang)) for h, d in _MESSAGES],
        toc_label=T(_MARKER, lang),
        tooltip=(T(_TIP_TITLE, lang), [(T(h, lang), T(d, lang)) for h, d in _TIP]),
        # PLEINE PAGE mobile (facette « complet ») : 1170×2949, la barre de
        # progression EST dans l'image. crop=(haut, droite, bas, gauche).
        zoomImage=130,
        zoomText=120,
        device="mobile-complet",
        landscape=False,
        crop=(0, 0, 15, 0),
        lang=lang
    )
