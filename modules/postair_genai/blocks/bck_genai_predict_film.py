"""The film — the prediction mechanism, animated (after the Predict reveal).

Insertion NG (2026-09-01) : juste après la révélation des probabilités de
« Luxembourg is a ____ », le film ``transformers-01.mp4`` (1920×1080, ~3'15)
prend TOUTE la fenêtre — le pattern « film plein écran » d'opening
(``bck_wait_loop``) : ``media_fullscreen`` + ``media_stage(ratio, 100)``, le
média grandit jusqu'à toucher un bord de la fenêtre et suit ses DEUX
dimensions (règle R4d), l'indication de lecture se pose en surimpression pour
ne lui reprendre aucune hauteur.

Retouche NG (2026-09-02) : ``autoplay=True, loop=False`` — le film part à
l'arrivée sur la slide (le Chrome de projection autorise l'autoplay sonore),
et il ne porte PAS de pastille DD-35 : c'est une PRODUCTION D'AUTEUR (montage
ScreenFlow de NG, sources hors dépôt), pas un média généré — une marque à
tort diluerait le sens de DD-35 autant qu'une marque manquante. Le « défaut
sûr = marqué » de la première version était un contresens : cette convention
vaut pour la médiathèque d'images MANAGÉES (sidecar), pas pour un film
authored.

Le fichier est VERSIONNÉ dans ``static/video/`` (décision NG 2026-09-01,
QCM) : exception assumée du dépôt — un média produit pour ces présentations,
hors CDN et hors catalogue, comme les illustrations. 36 Mo en git plutôt
qu'une campagne de publication à sept jours de l'AI Day ; le build CI l'a
d'office.

SPEAKER NOTES:
The film starts as the slide appears — arrive on it only when the room has
read the 78 % bar. Three minutes and a quarter: decide beforehand whether
you let it run whole or pause after the first sequence and tell the rest.
Sound ON. Bridge back: « that machinery, multiplied by scale, is the next
slide ».
"""
# @guideline: postair-minimal

from pathlib import Path

from custom.styles import Styles as s
from postair_lang import T
from streamtex import *
from streamtex.enums import Tags as t

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
            st_video(str(_FILM), autoplay=True, loop=False)
        with st_block(s.project.containers.media_hint_overlay):
            st_write(bs.hint, T(_HINT, lang), tag=t.div)
