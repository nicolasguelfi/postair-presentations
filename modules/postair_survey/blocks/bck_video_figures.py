"""Meet the figures 1/2 — le duo vidéo, la GAUCHE se lance (Platon).

Première des deux pages jumelles du duo figures (gabarit
``custom/media_duo.py``, NG 2026-08-22) : Platon à gauche, Ada Lovelace à
droite — un homme, une femme, connus de l'assemblée (Socrate n'est pas au
gel des 51 figures ; Platon est son plus proche voisin, NG 2026-08-22). Vidéos de présentation servies depuis le CDN (doctrine du
dépôt : les masters de figures ne s'embarquent pas — ces slides sont
précisément leurs deux ou trois ouvertures de la séance). Le choix des deux
figures vit dans ``figure_duo()``.

SPEAKER NOTES:
Same gesture as the mascots: let Platon speak, then arrow right for Ada
Lovelace. One sentence: every great figure's page carries its presentation
video — same instrument, same nine axes, and this afternoon they argue.
"""
# @guideline: postair-minimal

from custom.media_duo import figure_duo, media_duo_slide
from custom.styles import Styles as s


def build():
    media_duo_slide(
        ["Every figure has its ", (s.project.titles.keyword, "own video")],
        figure_duo(), "left",
        marker="Figure videos",
        toc_label="Figure videos",
        tooltip=("The figure videos",
                 [("In the app", "Every great figure's page carries a short "
                   "presentation video — click the portrait to play it."),
                  ("Same instrument", "The figures are scored on the same 54 "
                   "statements you answered, from documented positions in "
                   "their work."),
                  ("AI-made, sourced", "The videos are generative productions "
                   "grounded in each figure's dossier — arguments to debate, "
                   "never facts about a person.")]),
    )
