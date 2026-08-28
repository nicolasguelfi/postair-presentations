"""Trust — les 3 énoncés de chaque pôle (gabarit ``questions_slide``).

Bloc MINCE : il nomme un code d'instrument et un gabarit, rien d'autre — les
textes viennent du gel, la mise en page de ``custom/axis_slides.py``.

RÉGLAGE PAR SLIDE (NG 2026-08-24) : ``zoomTitle`` / ``zoomPole`` /
``zoomCell`` se passent ici ; sans eux, la table ``_ZOOMS`` du gabarit fait
foi pour les neuf axes. Ne jamais envelopper l'appel dans un ``st_zoom`` :
il emporterait le titre, et les colonnes étant en % leur boîte ne
grandirait pas — le texte passerait sous le pli (règle R-zoom).
"""
# @guideline: postair-minimal

from custom.axis_slides import questions_slide


def build():
    questions_slide("TRU", zoomCell=170)
