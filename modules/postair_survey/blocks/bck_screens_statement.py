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
from streamtex import *


def build(lang: str = "en", **_):
    st_marker("A statement")
    screen_slide(
        ["A statement, ", (s.project.titles.keyword, "six levels"), ", help"],
        "04-question",
        "Desktop screen of the survey journey: one statement with its six "
        "agreement levels and the help button, dark theme",
        [
            ("No right answer",
            "A portrait, not a test — nothing is scored as correct, and "
            "nobody sees your individual answers."),
            ("Answer for YOURSELF",
            "Not for the image you would like to give — the result is only "
            "useful if it is yours."),
            ("“No opinion” ≠ a middle answer",
            "A separate button OUTSIDE the six levels — excluded from your "
            "scores, never counted as halfway."),
        ],
        toc_label="A statement",
        tooltip=("Six levels, no middle",
                [("A gentle forced choice", "The middle of a scale attracts "
                "non-answers. If you truly have no opinion, use the "
                "dedicated button — it is excluded from your scores."),
                ("Why that matters", "A middle answer would be counted as a "
                "position halfway between the poles; 'no opinion' is "
                "counted as nothing at all. Confusing them is the one "
                "mistake that distorts a profile."),
                ("Help per question", "Every statement has a help button: "
                "clarification, anchors and two concrete examples.")]),
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
