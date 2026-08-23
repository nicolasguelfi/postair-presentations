"""Trust — vote, les trois réponses EN DÉFAVEUR (intensité croissante).

Slide GÉNÉRIQUE (gabarit ``vote_oppose_slide``) : son contenu ne dépend pas de
l'axe — le bloc n'apporte que le marqueur unique, réinséré pour chaque axe.
"""
# @guideline: postair-minimal

from custom.axis_slides import vote_oppose_slide


def build():
    vote_oppose_slide("Trust")
