"""Meet the mascots 2/2 — la même scène, la DROITE se lance (Bici, objets).

Page jumelle de ``bck_video_mascots`` : mêmes deux vidéos, seule la vidéo
active change — arriver ici par la flèche droite lance Bici avec le son.
Aucun contenu propre : tout vit dans ``custom/media_duo.py``.
"""
# @guideline: postair-minimal

from custom.media_duo import MASCOTS_TITLE, mascot_duo, media_duo_slide
from postair_lang import T, TF


_MARKER = {"en": "Mascot videos · 2"}


def build(lang: str = "en", **_):
    media_duo_slide(
        TF(MASCOTS_TITLE, lang),
        mascot_duo(lang), "right",
        marker=T(_MARKER, lang),
        stage_vh=70,
        lang=lang,
    )
