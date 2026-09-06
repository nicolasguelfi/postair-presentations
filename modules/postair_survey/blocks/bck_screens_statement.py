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
from postair_i18n import screen, ui
from postair_lang import T, TF
from streamtex import *
from streamtex.styles import Style


_MARKER = {"en": "A statement", "fr": "Un énoncé"}
#: « une aide » ET le libellé cité dans le VIOLET du bouton d'aide de
#: l'application (NG 2026-09-06) — la couleur renvoie au lien
#: « C’est-à-dire ? » de la capture. Ce libellé est CITÉ du gel des écrans
#: (DD-113, ``screen``), jamais recopié : le titre se construit donc par
#: langue, dans ``_title``.
_HELP = Style("color: #8782FF; font-weight: 700;", "pa_title_help_purple")
_TITLE = {"en": ("A statement, ", (s.project.titles.keyword, "six levels"), ", ",
                 (_HELP, "“{hint}”"), " for ", (_HELP, "help")),
          "fr": ("Un énoncé, ", (s.project.titles.keyword, "six niveaux"), ", ",
                 (_HELP, "«{nb}{hint}{nb}»"), " pour ", (_HELP, "une aide"))}
_MESSAGES = [
    ({"en": "No right answer", "fr": "Pas de bonne réponse"},
     {"en": ("A portrait, not a test — nothing is scored as correct, and "
             "nobody sees your individual answers."), "fr": "Un portrait, pas un test — rien n'est noté comme juste, et personne ne voit vos réponses individuelles."}),
    ({"en": "Answer for YOURSELF", "fr": "Répondez pour VOUS"},
     {"en": ("Not for the image you would like to give — the result is only "
             "useful if it is yours."), "fr": "Pas pour l'image que vous aimeriez donner — le résultat n'est utile que s'il est le vôtre."}),
    ({"en": "“{no_opinion}” ≠ a middle answer", "fr": "«{nb}{no_opinion}{nb}» ≠ le milieu"},
     {"en": ("A separate button OUTSIDE the six levels — excluded from your "
             "scores, never counted as halfway."), "fr": "Un bouton à part, HORS des six niveaux — exclu de vos scores, jamais compté comme un milieu."}),
]
_TIP_TITLE = {"en": "Six levels, no middle", "fr": "Six niveaux, pas de milieu"}
_TIP = [
    ({"en": "A gentle forced choice", "fr": "Un choix forcé, en douceur"},
     {"en": ("The middle of a scale attracts non-answers. If you truly have "
             "no opinion, use the dedicated button — it is excluded from your "
             "scores."), "fr": "Le milieu d'une échelle attire les non-réponses. Si vous n'avez vraiment pas d'opinion, utilisez le bouton dédié — il est exclu de vos scores."}),
    ({"en": "Why that matters", "fr": "Pourquoi ça compte"},
     {"en": ("A middle answer would be counted as a position halfway between "
             "the poles; '{no_opinion}' is counted as nothing at all. Confusing "
             "them is the one mistake that distorts a profile."), "fr": "Une réponse du milieu compterait comme une position à mi-chemin entre les pôles{nb}; «{nb}{no_opinion}{nb}» ne compte pour rien du tout. Les confondre est la seule erreur qui déforme un profil."}),
]
#: La tête « Help per question » vient du lexique (partagée avec la slide de
#: l'instrument).
_TIP_HELP = {"en": ("Every statement has a help button: clarification, anchors "
                    "and two concrete examples."), "fr": "Chaque énoncé a un bouton d'aide : clarification, repères et deux exemples concrets."}


def _cite(text: str, lang: str) -> str:
    """Les boutons « Sans opinion » et « C’est-à-dire ? » sont CITÉS tels que
    l'application les nomme (gel sumvadis, DD-113) — jamais recopiés dans
    la feuille."""
    return text.format(no_opinion=screen("04-question", "action", lang),
                       hint=screen("04-question", "hint", lang), nb="\u00a0")


def _title(lang: str) -> tuple:
    """Les fragments du titre, le libellé du bouton d'aide résolu par langue."""
    return tuple((frag[0], _cite(frag[1], lang)) if isinstance(frag, tuple)
                 else _cite(frag, lang) for frag in TF(_TITLE, lang))


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    screen_slide(
        _title(lang),
        "04-question",
        "Desktop screen of the survey journey: one statement with its six "
        "agreement levels and the help button, dark theme",
        [(_cite(T(h, lang), lang), _cite(T(d, lang), lang)) for h, d in _MESSAGES],
        toc_label=T(_MARKER, lang),
        tooltip=(T(_TIP_TITLE, lang),
                 [*[(_cite(T(h, lang), lang), _cite(T(d, lang), lang)) for h, d in _TIP],
                  (ui("help_per_question", lang), T(_TIP_HELP, lang))]),
        # Desktop PAYSAGE (NG 2026-08-21) : capture pleine scène en haut,
        # les trois règles en ligne dessous — permis par le gel matrice
        # complète (décision D). L'alerte « 1 octet » du 2026-08-21 était
        # un incident transitoire du service média, résolu côté sumvadis.
        device="mobile-complet",
        landscape=False,
        zoomImage=140,
        zoomText=130,
        crop=(18, 0, 13, 0),
        # Cartes à demi-rembourrage vertical (NG 202r6-09-06, capture FR).
        card_padding="1vh 1.5vw",
        lang=lang
    )
