"""The age requirement screen (02-eligibilite) — les catégories mineures.

Slide Q14 (NG 2026-08-23), entre le consentement (03) et l'énoncé (04) dans
l'ordre du deck : la capture RÉELLE de la porte d'âge, et à droite ce qu'elle
change — rien pour l'expérience, tout pour l'enregistrement recherche. Le
texte des cartes reprend l'écran lui-même (« Only the answers of people aged
18 or over are recorded for research ») : deux déclarations, pas de date de
naissance, pas de preuve.

SPEAKER NOTES:
Thirty seconds, and say it warmly: under-18s are welcome — full survey, full
personal radar, nothing less. The only difference is invisible to them:
their record is not counted in the research study. One honest declaration,
no birthdate, no proof — pick the statement that applies today.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from postair_lang import T, TF
from streamtex import *


_MARKER = {"en": "Age requirement", "fr": "Condition d'âge"}
_TITLE = {"en": ("The ", (s.project.titles.keyword, "age"), " requirement"), "fr": ("La condition d'", (s.project.titles.keyword, "âge"), "")}
_MESSAGES = [
    ({"en": "A simple declaration", "fr": "Une simple déclaration"},
     {"en": ("Two statements, pick the one that applies to you today — no "
             "birthdate, no proof, nothing stored about your age beyond the "
             "category."), "fr": "Deux déclarations, choisissez celle qui vous correspond aujourd'hui — pas de date de naissance, pas de justificatif, rien de conservé sur votre âge, sauf la catégorie."}),
    ({"en": "Under 18? You still play", "fr": "Moins de 18 ans ? Vous jouez"},
     {"en": ("Full survey, personal radar, archetypes, figures — the whole "
             "experience, nothing less."), "fr": "Sondage complet, radar personnel, archétypes, figures — toute l'expérience, rien de moins."}),
    ({"en": "The one difference", "fr": "La seule différence"},
     {"en": ("Only the answers of people aged 18 or over are recorded for "
             "research — an under-18 record is simply not counted in the "
             "study."), "fr": "Seules les réponses des 18 ans et plus sont enregistrées pour la recherche — l'enregistrement d'une personne mineure n'est simplement pas compté dans l'étude."}),
]
_TIP_TITLE = {"en": "Why this gate", "fr": "Pourquoi ce seuil"}
_TIP = [
    ({"en": "Research ethics", "fr": "Éthique de recherche"},
     {"en": ("The survey is an academic research instrument: minors' answers "
             "are excluded from the study by design, without excluding minors "
             "from the game."), "fr": "Le sondage est un instrument de recherche universitaire : les réponses des personnes mineures sont exclues de l'étude par conception, sans les exclure du jeu."}),
    ({"en": "Declarative by choice", "fr": "Déclaratif par choix"},
     {"en": ("No identity check — the gate relies on an honest declaration, "
             "consistent with a fully anonymous survey: verifying an age would "
             "require knowing who you are."), "fr": "Aucune vérification d'identité — le seuil repose sur une déclaration sur l'honneur, cohérente avec un sondage totalement anonyme : vérifier un âge exigerait de savoir qui vous êtes."}),
]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    screen_slide(
        TF(_TITLE, lang),
        "02-eligibilite",
        "Mobile screen of the survey age requirement: two declarations, 18 or "
        "older and under 18, dark theme",
        [(T(h, lang), T(d, lang)) for h, d in _MESSAGES],
        toc_label=T(_MARKER, lang),
        tooltip=(T(_TIP_TITLE, lang), [(T(h, lang), T(d, lang)) for h, d in _TIP]),
        zoomImage=210,
        zoomText=120,
        device="mobile",
        landscape=False,
        crop=(0, 0, 30, 0),
        lang=lang
    )
