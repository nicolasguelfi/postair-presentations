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
from streamtex import *


def build(lang: str = "en", **_):
    st_marker("Age requirement")
    screen_slide(
        ["The ", (s.project.titles.keyword, "age"), " requirement"],
        "02-eligibilite",
        "Mobile screen of the survey age requirement: two declarations, 18 or "
        "older and under 18, dark theme",
        [
            ("A simple declaration",
             "Two statements, pick the one that applies to you today — no "
             "birthdate, no proof, nothing stored about your age beyond the "
             "category."),
            ("Under 18? You still play",
             "Full survey, personal radar, archetypes, figures — the whole "
             "experience, nothing less."),
            ("The one difference",
             "Only the answers of people aged 18 or over are recorded for "
             "research — an under-18 record is simply not counted in the "
             "study."),
        ],
        toc_label="Age requirement",
        tooltip=("Why this gate",
                 [("Research ethics", "The survey is an academic research "
                   "instrument: minors' answers are excluded from the study "
                   "by design, without excluding minors from the game."),
                  ("Declarative by choice", "No identity check — the gate "
                   "relies on an honest declaration, consistent with a fully "
                   "anonymous survey: verifying an age would require knowing "
                   "who you are.")]),
        zoomImage=210,
        zoomText=120,
        device="mobile",
        landscape=False,
        crop=(0, 0, 30, 0),
    )
