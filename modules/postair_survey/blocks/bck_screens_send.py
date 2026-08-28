"""Sending your answers — écran 06-envoi.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_answering) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.

SPEAKER NOTES:
The one message that matters: nothing leaves the phone before that
tap, and after it the record is anonymous.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from postair_lang import T, TF
from streamtex import *


_MARKER = {"en": "Sending your answers", "fr": "Envoyer vos réponses"}
_TITLE = {"en": ("Sending your ", (s.project.titles.keyword, "answers")), "fr": ("Envoyer vos ", (s.project.titles.keyword, "réponses"))}
_MESSAGES = [
    ({"en": "The last screen before your report", "fr": "Le dernier écran avant votre rapport"},
     {"en": ("It appears once the statements are answered — nothing has left "
             "your phone yet."), "fr": "Il apparaît quand tous les énoncés ont une réponse — rien n'a encore quitté votre téléphone."}),
    ({"en": "One tap, one record", "fr": "Un geste, un enregistrement"},
     {"en": ("Send once: the server receives a single anonymous record, and "
             "your personal report is computed on YOUR device."), "fr": "Envoyez une fois : le serveur reçoit un seul enregistrement anonyme, et votre rapport personnel est calculé sur VOTRE appareil."}),
    ({"en": "The trap: walking away", "fr": "Le piège : s'en aller"},
     {"en": ("Answers that are never sent never reach the room's averages — "
             "finish the gesture before you pocket the phone."), "fr": "Des réponses jamais envoyées ne rejoignent jamais les moyennes de la salle — finissez le geste avant de ranger le téléphone."}),
]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    screen_slide(
        TF(_TITLE, lang),
        "06-envoi",
        "Mobile screen of the survey send step: the summary before submitting "
        "the answers, dark theme",
        [(T(h, lang), T(d, lang)) for h, d in _MESSAGES],
        zoomImage=190,
        zoomText=120,
        crop = (0, 0, 13, 0),
        lang=lang
    )
