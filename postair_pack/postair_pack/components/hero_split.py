"""Le gabarit par défaut des slides POSTAIR — image à gauche, contenu à droite.

Règle NG (2026-08-13) : la composition par défaut d'une slide de contenu est
l'image CARRÉE à gauche sur ~50 % de la largeur, et la zone de droite pour le
texte ou les grilles, en télégraphique. Ce composant EST cette règle.

Contrat de réglage (NG 2026-08-13) : le gabarit est le schéma COMMUN, mais
chaque paramètre a une valeur par défaut et se règle SLIDE PAR SLIDE, à
l'appel, dans le bloc — jamais par une configuration centrale, jamais en
relançant un script : éditer la ligne, enregistrer, Streamlit ré-exécute.

- ``ratio`` est la part de largeur de l'IMAGE, réellement asymétrique :
  ``40`` → image 40 %, contenu 60 %. Sous ~720 px les deux colonnes
  retombent en une (repli flex : l'image repasse AU-DESSUS du texte, ordre
  du DOM) ;
- l'image se dimensionne PAR SA CELLULE (``width="100%"`` chez l'appelant,
  le défaut de ``hero_image``) : changer ``ratio`` suffit, rien d'autre à
  toucher ; la forme (1:1, 3:2, 2:3) se choisit par ``variant`` de
  ``hero_image`` — les trois orientations existent déjà en médiathèque ;
- la colonne droite est le BUDGET de la slide : ``column_stack_centered``
  répartit ses éléments sur la hauteur disponible, rien ne passe sous le
  pli ; ``zoom``/``image_zoom`` ajustent chaque colonne d'un cran (90, 85),
  jamais pour rattraper une composition ratée ;
- ``marked`` pose la marque de transparence IA (DD-35, voir ``ai_mark``)
  sur le conteneur du média — à passer depuis le DRAPEAU de données
  (``ai_generated``), jamais en dur.

Usage type dans un bloc::

    with hero_split(s, ratio=40, image=lambda: hero_image("genai_twist",
                                                          _PROMPT, fallback,
                                                          alt, alt,
                                                          variant="sq")):
        st_write(...)   # la colonne de droite
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Callable

from streamtex import st_block, st_grid, st_zoom

from postair_pack.components.ai_mark import ai_marked


@contextmanager
def hero_split(styles, image: Callable[[], None], ratio: int = 50,
               gap: str = "2vw", zoom: int = 100, image_zoom: int = 100,
               marked: bool = False, mark_label: str = "AI"):
    """Image à gauche sur ``ratio`` %, contenu à droite ; une colonne sous 720 px.

    :param styles: la façade ``Styles`` du module (``s`` dans les blocs).
    :param image: rendu de la colonne image (typiquement un ``hero_image``).
    :param ratio: part de largeur de l'image, en % (50 = moitié/moitié,
        40 = image plus étroite que le texte). Toujours réglable par slide.
    :param zoom: facteur ``st_zoom`` de la colonne de CONTENU (100 = neutre).
    :param image_zoom: facteur ``st_zoom`` de la colonne image.
    :param marked: drapeau ``ai_generated`` du média — pose la pastille DD-35.
    :param mark_label: libellé de la pastille (voir ``ai_mark``).
    """
    ds = styles.project
    # Deux pistes asymétriques exactes (fr) ; le repli mobile est le
    # mécanisme NATIF de la grille (``breakpoint`` : une seule colonne sous
    # le seuil, l'image repasse AU-DESSUS du texte — ordre du DOM). Les
    # styles de cellule doivent passer par ``st_grid`` : un ``st_block``
    # imbriqué n'est PAS l'item de grille (chaque enfant est enveloppé dans
    # un ``.stx-el``), constaté le 2026-08-13 en croyant piloter du flex.
    cols = f"minmax(0, {ratio}fr) minmax(0, {100 - ratio}fr)"
    with st_grid(cols=cols, gap=gap, breakpoint="720px",
                 cell_styles=ds.containers.grid_cell_centered) as g:
        with g.cell():
            with st_zoom(image_zoom), ai_marked(marked, mark_label, fit=False):
                image()
        with g.cell():
            with st_zoom(zoom), st_block(ds.containers.column_stack_centered):
                yield
