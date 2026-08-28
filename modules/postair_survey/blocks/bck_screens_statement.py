"""The statement screen (04) — six levels, help, and the three rules.

Slide Q14 (NG 2026-08-20) : la capture RÉELLE d'un énoncé à gauche, et à
droite les messages à la place de l'ancienne légende. Les trois propriétés
cruciales de l'ancienne slide « How to answer » (supprimée le même jour)
vivent DÉSORMAIS ICI, face à l'écran qu'elles gouvernent : no right answer,
answer for yourself, « no opinion » n'est pas un milieu.

SPEAKER NOTES:
One minute, calm and clear. Read the last card slowly: « no opinion » is NOT
a middle answer — it is the one thing people get wrong, and the one that
distorts a profile. No right answer, no image to polish: answer for
yourself. Some statements feel « reversed » — that is intentional
(acquiescence control), read carefully.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from postair_i18n import ui
from postair_lang import T, TF
from streamtex import *


_MARKER = {"en": "A statement"}
_TITLE = {"en": ("A statement, ", (s.project.titles.keyword, "six levels"), ", help")}
_MESSAGES = [
    ({"en": "No right answer"},
     {"en": ("A portrait, not a test — nothing is scored as correct, and "
             "nobody sees your individual answers.")}),
    ({"en": "Answer for YOURSELF"},
     {"en": ("Not for the image you would like to give — the result is only "
             "useful if it is yours.")}),
    ({"en": "“No opinion” ≠ a middle answer"},
     {"en": ("A separate button OUTSIDE the six levels — excluded from your "
             "scores, never counted as halfway.")}),
]
_TIP_TITLE = {"en": "Six levels, no middle"}
_TIP = [
    ({"en": "A gentle forced choice"},
     {"en": ("The middle of a scale attracts non-answers. If you truly have "
             "no opinion, use the dedicated button — it is excluded from your "
             "scores.")}),
    ({"en": "Why that matters"},
     {"en": ("A middle answer would be counted as a position halfway between "
             "the poles; 'no opinion' is counted as nothing at all. Confusing "
             "them is the one mistake that distorts a profile.")}),
]
#: La tête « Help per question » vient du lexique (partagée avec la slide de
#: l'instrument).
_TIP_HELP = {"en": ("Every statement has a help button: clarification, anchors "
                    "and two concrete examples.")}


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    screen_slide(
        TF(_TITLE, lang),
        "04-question",
        "Desktop screen of the survey journey: one statement with its six "
        "agreement levels and the help button, dark theme",
        [(T(h, lang), T(d, lang)) for h, d in _MESSAGES],
        toc_label=T(_MARKER, lang),
        tooltip=(T(_TIP_TITLE, lang),
                 [*[(T(h, lang), T(d, lang)) for h, d in _TIP],
                  (ui("help_per_question", lang), T(_TIP_HELP, lang))]),
        # Desktop PAYSAGE (NG 2026-08-21) : capture pleine scène en haut,
        # les trois règles en ligne dessous — permis par le gel matrice
        # complète (décision D). L'alerte « 1 octet » du 2026-08-21 était
        # un incident transitoire du service média, résolu côté sumvadis.
        device="mobile-complet",
        landscape=False,
        zoomImage=130,
        zoomText=120,
        crop=(0, 0, 15, 0),
        lang=lang 
    )
