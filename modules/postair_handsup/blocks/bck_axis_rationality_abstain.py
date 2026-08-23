"""Rationality — vote, la réponse de qui ne se prononce pas.

Slide GÉNÉRIQUE (gabarit ``vote_abstain_slide``) : son contenu ne dépend pas de
l'axe — le bloc n'apporte que le marqueur unique, réinséré pour chaque axe.
"""
# @guideline: postair-minimal

from custom.axis_slides import vote_abstain_slide


def build():
    vote_abstain_slide("Rationality")
