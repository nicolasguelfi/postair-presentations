"""Meet the mascots 2/2 — la même scène, la DROITE se lance (Bici, objets).

Page jumelle de ``bck_video_mascots`` : mêmes deux vidéos, seule la vidéo
active change — arriver ici par la flèche droite lance Bici avec le son.
Aucun contenu propre : tout vit dans ``custom/media_duo.py``.
"""
# @guideline: postair-minimal

from custom.media_duo import mascot_duo, media_duo_slide
from custom.styles import Styles as s


def build(lang: str = "en", **_):
    media_duo_slide(
        ["Every mascot has its ", (s.project.titles.keyword, "own video")],
        mascot_duo(), "right",
        marker="Mascot videos · 2",
        stage_vh=70,
    )
