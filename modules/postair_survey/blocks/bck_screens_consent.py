"""The consent screen (03) — nothing personal, and it is written on screen.

Slide Q14 (NG 2026-08-20) : la capture RÉELLE du consentement à gauche, et à
droite les messages utiles à la place de l'ancienne légende — ce que l'écran
demande, ce qu'il ne demande PAS, et ce que « anonyme » veut dire ici.
Remplace, avec ``bck_screens_statement``, l'ancienne paire « The first
screens · 3-4 » du bloc « How to answer » (supprimé le même jour).

SPEAKER NOTES:
Thirty seconds. Say out loud that nothing on this screen identifies anyone —
the room heard it on the context slide, it must SEE it once on the real
screen. Consent is a tap, stopping is allowed at any time.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from postair_i18n import ui
from postair_lang import T, TF
from streamtex import *


_MARKER = {"en": "Consent", "fr": "Consentement"}
_TITLE = {"en": ("Consent — ", (s.project.titles.keyword, "nothing personal")), "fr": ("Consentement — ", (s.project.titles.keyword, "rien de personnel"))}
_MESSAGES = [
    ({"en": "Nothing personal is asked", "fr": "Rien de personnel n'est demandé"},
     {"en": ("No name, no email, no account — nothing on this screen can "
             "identify you."), "fr": "Ni nom, ni e-mail, ni compte — rien sur cet écran ne peut vous identifier."}),
    ({"en": "Your explicit consent", "fr": "Votre consentement explicite"},
     {"en": ("The survey starts only after you accept — participation is "
             "voluntary, and you can stop at any time."), "fr": "Le sondage ne démarre qu'après votre accord — la participation est volontaire, et vous pouvez arrêter à tout moment."}),
    ({"en": "Anonymous by construction", "fr": "Anonyme par construction"},
     {"en": ("Your report is computed on YOUR device; only anonymous answers "
             "reach the room's averages."), "fr": "Votre rapport est calculé sur VOTRE appareil ; seules des réponses anonymes rejoignent les moyennes de la salle."}),
]
_TIP_TITLE = {"en": "This screen", "fr": "Cet écran"}
_TIP_CAPTURE = ({"en": "Real capture", "fr": "Capture réelle"},
                {"en": ("The actual application, mobile facet, dark theme — "
                        "frozen from the sumvadis media registry, never "
                        "redrawn."), "fr": "La vraie application, facette mobile, thème sombre — gelée depuis le registre média de sumvadis, jamais redessinée."})
#: La tête « Under 18 » vient du lexique (partagée avec la slide Welcome Week).
_TIP_UNDER_18 = {"en": ("You can play and see your own results — your record is "
                        "simply excluded from the research analysis."), "fr": "Vous pouvez jouer et voir vos propres résultats — votre enregistrement est simplement exclu de l'analyse de recherche."}


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_zoom(130):
        screen_slide(
            TF(_TITLE, lang),
            "03-consentement",
            "Mobile screen of the survey journey: the consent step, dark theme",
            [(T(h, lang), T(d, lang)) for h, d in _MESSAGES],
            toc_label=T(_MARKER, lang),
            tooltip=(T(_TIP_TITLE, lang),
                     [(T(_TIP_CAPTURE[0], lang), T(_TIP_CAPTURE[1], lang)),
                      (ui("under_18", lang), T(_TIP_UNDER_18, lang))]),
            zoomImage=100,
            zoomText=90,
            device="mobile-complet",
            landscape=False,
            crop=(0, 0, 5, 0),
            lang=lang
        )
