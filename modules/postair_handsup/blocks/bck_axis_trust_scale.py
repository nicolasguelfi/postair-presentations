"""Trust — la slide de vote (gabarit ``scale_slide``).

Même contenu pour les neuf axes — seuls le titre et le marqueur portent
l'axe : neuf blocs minces plutôt qu'un bloc listé neuf fois, qui casserait
marqueurs et TOC.
"""
# @guideline: postair-minimal

from custom.axis_slides import scale_slide


def build():
    scale_slide("TRU")
