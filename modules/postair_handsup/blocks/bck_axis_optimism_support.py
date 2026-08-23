"""Optimism — vote, les trois réponses EN FAVEUR (intensité décroissante).

Slide GÉNÉRIQUE (gabarit ``vote_support_slide``) : son contenu ne dépend pas de
l'axe — le bloc n'apporte que le marqueur unique, réinséré pour chaque axe.
"""
# @guideline: postair-minimal

from custom.axis_slides import vote_support_slide


def build():
    vote_support_slide("Optimism")
