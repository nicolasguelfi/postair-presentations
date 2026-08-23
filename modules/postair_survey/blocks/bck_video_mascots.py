"""Meet the mascots 1/2 — le duo vidéo, la GAUCHE se lance (Pathos, animaux).

Première des deux pages jumelles du duo mascottes (gabarit
``custom/media_duo.py``, NG 2026-08-22) : Pathos (Emotion, famille animaux) à
gauche, Bici (Prudence, famille objets) à droite. Sur cette page la vidéo de
GAUCHE démarre avec le son ; la flèche droite passe à la page jumelle où la
DROITE démarre. Le choix des deux mascottes vit dans ``mascot_duo()``.

SPEAKER NOTES:
Let Pathos play — twenty seconds, do not talk over it. One sentence before:
every mascot of the app has its own presentation clip, this is what you will
find behind each character. Then arrow right: Bici answers, at its own pace.
"""
# @guideline: postair-minimal

from custom.media_duo import mascot_duo, media_duo_slide
from custom.styles import Styles as s


def build():
    media_duo_slide(
        ["Every mascot has its ", (s.project.titles.keyword, "own video")],
        mascot_duo(), "left",
        marker="Mascot videos",
        toc_label="Mascot videos",
        tooltip=("The mascot clips",
                 [("In the app", "Every one of the 36 mascots carries a short "
                   "presentation clip — open any character to play it."),
                  ("Two families", "Each pole is carried by an animal AND an "
                   "object; here, the most playful of each family."),
                  ("Production", "Made in house, entirely with generative AI, "
                   "from the definitions of the nine axes.")]),
        stage_vh=70,
    )
