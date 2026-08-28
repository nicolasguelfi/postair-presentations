"""Rationality — les 3 énoncés de chaque pôle (gabarit ``questions_slide``).

Bloc MINCE : il nomme un code d'instrument et un gabarit, rien d'autre — les
textes viennent du gel, la mise en page de ``custom/axis_slides.py``. Un axe
= trois blocs (questions, synthèse, vote) : ordonner ou exclure se règle
ligne par ligne dans le book.

RÉGLAGE PAR SLIDE (NG 2026-08-24) : ``zoomTitle`` / ``zoomPole`` /
``zoomCell`` se passent ici ; sans eux, la table ``_ZOOMS`` du gabarit fait
foi pour les neuf axes. Ne jamais envelopper l'appel dans un ``st_zoom``.
"""
# @guideline: postair-minimal

from custom.axis_slides import questions_slide


def build(lang: str = "en", **_):
    questions_slide("RAT")
