"""Le gabarit par défaut des slides POSTAIR — image à gauche, contenu à droite.

Règle NG (2026-08-13) : la composition par défaut d'une slide de contenu est
l'image CARRÉE à gauche sur ~50 % de la largeur, et la zone de droite pour le
texte ou les grilles, en télégraphique. Ce composant EST cette règle :

- grille responsive « 2 colonnes → 1 colonne » par le mécanisme maison
  (plancher px dans un ``minmax`` : sous ~720 px la grille retombe à une
  colonne, l'image repasse AU-DESSUS du texte — ordre du DOM) ;
- la colonne droite est le BUDGET de la slide : ``column_stack_centered``
  répartit ses éléments sur la hauteur disponible, rien ne passe sous le pli ;
- ``zoom`` (NG 2026-08-13) : chaque colonne est enveloppée dans ``st_zoom``
  pour l'ajustement local proportionnel — pour AJUSTER une slide dense d'un
  cran (90, 85), jamais pour rattraper une composition ratée.

Usage type dans un bloc::

    with hero_split(s, image=lambda: hero_image("genai_twist", _HERO_PROMPT,
                                                fallback, alt, alt,
                                                variant="sq")) as right:
        st_write(...)   # la colonne de droite

Le paramètre ``ratio`` règle le plancher de la colonne (48 % ≈ moitié/moitié ;
40 % donne une image plus large que le texte).
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Callable

from streamtex import st_block, st_grid, st_zoom


@contextmanager
def hero_split(styles, image: Callable[[], None], ratio: int = 44,
               gap: str = "2vw", zoom: int = 100, image_zoom: int = 100):
    """Image à gauche, contenu à droite ; empilement sous ~720 px.

    :param styles: la façade ``Styles`` du module (``s`` dans les blocs).
    :param image: rendu de la colonne image (typiquement un ``hero_image``).
    :param ratio: plancher en % d'une colonne — 44 laisse tenir exactement
        deux colonnes (2 × 44 + gouttière < 100), jamais trois.
    :param zoom: facteur ``st_zoom`` de la colonne de CONTENU (100 = neutre).
    :param image_zoom: facteur ``st_zoom`` de la colonne image.
    """
    ds = styles.project
    cols = f"repeat(auto-fit, minmax(max(340px, {ratio}%), 1fr))"
    with st_grid(cols=cols, gap=gap,
                 cell_styles=ds.containers.grid_cell_centered) as g:
        with g.cell():
            with st_zoom(image_zoom):
                image()
        with g.cell():
            with st_zoom(zoom), st_block(ds.containers.column_stack_centered):
                yield
