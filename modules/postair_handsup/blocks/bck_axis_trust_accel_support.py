"""Trust (pôle accélérateur) — vote du pôle, les trois réponses EN FAVEUR.

Slide GÉNÉRIQUE (gabarit ``vote_support_slide``), doublée par pôle (NG 2026-08-23) :
le bloc n'apporte que le marqueur unique du pôle voté.
"""
# @guideline: postair-minimal

from custom.axis_slides import vote_support_slide


def build():
    vote_support_slide("TRU", "accel")
