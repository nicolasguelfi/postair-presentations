"""Openness (pôle décélérateur) — vote du pôle, la réponse de qui ne se prononce pas.

Slide GÉNÉRIQUE (gabarit ``vote_abstain_slide``), doublée par pôle (NG 2026-08-23) :
le bloc n'apporte que le marqueur unique du pôle voté.
"""
# @guideline: postair-minimal

from custom.axis_slides import vote_abstain_slide


def build():
    vote_abstain_slide("OPE", "decel")
