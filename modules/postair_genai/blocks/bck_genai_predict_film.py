"""The film — the prediction mechanism, animated (after the Predict reveal).

Insertion NG (2026-09-01) : juste après la révélation des probabilités de
« Luxembourg is a ____ », le film ``transformers-01.mp4`` (1920×1080, ~3'15)
prend TOUTE la fenêtre — le pattern « film plein écran » d'opening
(``bck_wait_loop``) : ``media_fullscreen`` + ``media_stage(ratio, 100)``, le
média grandit jusqu'à toucher un bord de la fenêtre et suit ses DEUX
dimensions (règle R4d), l'indication de lecture se pose en surimpression pour
ne lui reprendre aucune hauteur.

Contrairement à l'écran d'attente, PAS d'autoplay ni de boucle : le film se
lance d'un geste de l'orateur (règle R7 — l'autoplay avec son est de toute
façon bloqué hors du Chrome de projection), au moment choisi du récit.

Le fichier est VERSIONNÉ dans ``static/video/`` (décision NG 2026-09-01,
QCM) : exception assumée du dépôt — un média produit pour ces présentations,
hors CDN et hors catalogue, comme les illustrations. 36 Mo en git plutôt
qu'une campagne de publication à sept jours de l'AI Day ; le build CI l'a
d'office. La pastille DD-35 est posée par défaut sûr (provenance non
déclarée — l'absence de marque doit se mériter par la donnée).

SPEAKER NOTES:
Launch it yourself, when the room has read the 78 % bar — the film shows the
machinery behind that bar. Three minutes and a quarter: decide beforehand
whether you play it whole or stop after the first sequence and tell the rest.
Sound ON. Bridge back: « that machinery, multiplied by scale, is the next
slide ».
"""
# @guideline: postair-minimal

from pathlib import Path

from custom.styles import Styles as s
from postair_lang import T
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.ai_mark import ai_marked

#: Mesuré sur le fichier (ffprobe) : 1920×1080.
_FILM_RATIO = 16 / 9

#: Résolu depuis le fichier, jamais du répertoire courant (piège du lanceur).
_FILM = Path(__file__).parent.parent / "static" / "video" / "transformers-01.mp4"


class BlockStyles:
    hint = s.project.body.caption + s.center_txt


bs = BlockStyles

_MARKER = {"en": "The film"}
_HINT = {"en": "▶ play · sound on"}


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.media_fullscreen):
        # La scène est bornée par TOUTE la hauteur de fenêtre ; le film la remplit.
        with st_block(s.project.containers.media_stage(_FILM_RATIO, 100)):
            with ai_marked(fit=False, top=True):
                st_video(str(_FILM))
        with st_block(s.project.containers.media_hint_overlay):
            st_write(bs.hint, T(_HINT, lang), tag=t.div)
