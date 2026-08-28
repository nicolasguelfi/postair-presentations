"""Meet the figures 2/2 — la même scène, la DROITE se lance (Ada Lovelace).

Page jumelle de ``bck_video_figures`` : mêmes deux vidéos, seule la vidéo
active change — arriver ici par la flèche droite lance Ada Lovelace avec le
son. Aucun contenu propre : tout vit dans ``custom/media_duo.py``.
"""
# @guideline: postair-minimal

from custom.media_duo import FIGURES_TITLE, figure_duo, media_duo_slide
from postair_lang import T, TF


_MARKER = {"en": "Figure videos · 2", "fr": "Vidéos des figures · 2"}


def build(lang: str = "en", **_):
    media_duo_slide(
        TF(FIGURES_TITLE, lang),
        figure_duo(lang), "right",
        marker=T(_MARKER, lang),
        stage_vh=70,
        lang=lang,
    )
