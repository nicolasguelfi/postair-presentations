"""Centralisation (pôle accélérateur) — la slide du pôle : sa synthèse, seule et en grand.

Vote PAR PÔLE (NG 2026-08-23) : chaque pôle ouvre sa séquence de vote.
Bloc MINCE sur ``pole_synthesis_slide`` — textes du gel, rien à la main.

RÉGLAGE PAR SLIDE (NG 2026-08-24) : ``zoomTitle`` / ``zoomPole`` /
``zoomCell`` se passent ici ; sans eux, la table ``_ZOOMS`` du gabarit fait
foi pour les dix-huit pôles.
"""
# @guideline: postair-minimal

from custom.axis_slides import pole_synthesis_slide


def build(lang: str = "en", **_):
    pole_synthesis_slide("CEN", "accel", lang=lang)
