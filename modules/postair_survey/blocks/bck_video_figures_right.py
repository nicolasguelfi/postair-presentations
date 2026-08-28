"""Meet the figures 2/2 — la même scène, la DROITE se lance (Ada Lovelace).

Page jumelle de ``bck_video_figures`` : mêmes deux vidéos, seule la vidéo
active change — arriver ici par la flèche droite lance Ada Lovelace avec le
son. Aucun contenu propre : tout vit dans ``custom/media_duo.py``.
"""
# @guideline: postair-minimal

from custom.media_duo import figure_duo, media_duo_slide
from custom.styles import Styles as s


def build(lang: str = "en", **_):
    media_duo_slide(
        ["Every figure has its ", (s.project.titles.keyword, "own video")],
        figure_duo(), "right",
        marker="Figure videos · 2",
        stage_vh=70,
    )
