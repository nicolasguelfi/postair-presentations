"""You and the room — écran 10-res-salle.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_explore) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.

SPEAKER NOTES:
Slow down here: this comparison is the bridge to the projection
moment.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from postair_lang import T, TF
from streamtex import *


_MARKER = {"en": "You and the room", "fr": "Vous et la salle"}
_TITLE = {"en": ("You and the ", (s.project.titles.keyword, "room")), "fr": ("Vous et la ", (s.project.titles.keyword, "salle"))}
_MESSAGES = [
    ({"en": "Your shape against the room's", "fr": "Votre forme face à la salle"},
     {"en": ("Your radar overlaid on the room's averages — the moment a "
             "personal result becomes a conversation."), "fr": "Votre radar superposé aux moyennes de la salle — le moment où un résultat personnel devient une conversation."}),
    ({"en": "Minimum five answers", "fr": "Cinq enregistrements minimum"},
     {"en": ("Room aggregates appear only once at least five records are in; "
             "before that, the section waits."), "fr": "Les agrégats de la salle n'apparaissent qu'à partir de cinq enregistrements ; avant, la section attend."}),
    ({"en": "What comes next", "fr": "La suite"},
     {"en": ("This same comparison, projected wall-size for everyone — the "
             "next slides open it."), "fr": "Cette même comparaison, projetée grand écran pour tous — les slides suivantes l'ouvrent."}),
]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    screen_slide(
        TF(_TITLE, lang),
        "10-res-salle",
        "Mobile screen comparing the personal radar with the room's averages, "
        "dark theme",
        [(T(h, lang), T(d, lang)) for h, d in _MESSAGES],
        zoomImage=190,
        zoomText=140,
        device="mobile",
        landscape=False,
        lang=lang
    )
