"""Freedom (pôle décélérateur) — vote du pôle, les trois réponses EN DÉFAVEUR.

Slide GÉNÉRIQUE (gabarit ``vote_oppose_slide``), doublée par pôle (NG 2026-08-23) :
le bloc n'apporte que le marqueur unique du pôle voté.
"""
# @guideline: postair-minimal

from custom.axis_slides import vote_oppose_slide


def build():
    vote_oppose_slide("CON", "decel")
