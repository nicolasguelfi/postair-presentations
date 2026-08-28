"""Meet the mascots 1/2 — le duo vidéo, la GAUCHE se lance (Pathos, animaux).

Première des deux pages jumelles du duo mascottes (gabarit
``custom/media_duo.py``, NG 2026-08-22) : Pathos (Emotion, famille animaux) à
gauche, Bici (Prudence, famille objets) à droite. Sur cette page la vidéo de
GAUCHE démarre avec le son ; la flèche droite passe à la page jumelle où la
DROITE démarre. Le choix des deux mascottes vit dans ``mascot_duo(lang)``.

SPEAKER NOTES:
Let Pathos play — twenty seconds, do not talk over it. One sentence before:
every mascot of the app has its own presentation clip, this is what you will
find behind each character. Then arrow right: Bici answers, at its own pace.
"""
# @guideline: postair-minimal

from custom.media_duo import MASCOTS_TITLE, mascot_duo, media_duo_slide
from postair_i18n import ui
from postair_lang import T, TF


_MARKER = {"en": "Mascot videos"}
_TIP_TITLE = {"en": "The mascot clips"}
#: La première tête vient du lexique (``in_the_app``, partagée avec les vidéos
#: de figures) ; les deux autres sont propres à cette slide.
_TIP = [
    {"en": ("Every one of the 36 mascots carries a short presentation clip — "
            "open any character to play it.")},
    ({"en": "Two families"},
     {"en": ("Each pole is carried by an animal AND an object; here, the most "
             "playful of each family.")}),
    ({"en": "Production"},
     {"en": ("Made in house, entirely with generative AI, from the definitions "
             "of the nine axes.")}),
]


def build(lang: str = "en", **_):
    media_duo_slide(
        TF(MASCOTS_TITLE, lang),
        mascot_duo(lang), "left",
        marker=T(_MARKER, lang),
        toc_label=T(_MARKER, lang),
        tooltip=(T(_TIP_TITLE, lang),
                 [(ui("in_the_app", lang), T(_TIP[0], lang)),
                  (T(_TIP[1][0], lang), T(_TIP[1][1], lang)),
                  (T(_TIP[2][0], lang), T(_TIP[2][1], lang))]),
        stage_vh=70,
        lang=lang,
    )
