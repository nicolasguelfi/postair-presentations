"""Optimism — la synthèse de chaque pôle (gabarit ``synthetic_slide``).

Bloc MINCE : un énoncé unique par pôle, venu du champ ``synthesis`` du
questionnaire du hub (v1.10.0, commit 6af6a825) via le gel — validé un à un
par l'auteur en amont, jamais écrit ici.
"""
# @guideline: postair-minimal

from custom.axis_slides import synthetic_slide


def build():
    synthetic_slide("OPT")
