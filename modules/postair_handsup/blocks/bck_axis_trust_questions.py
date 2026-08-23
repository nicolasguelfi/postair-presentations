"""Trust — les 3 énoncés de chaque pôle (gabarit ``questions_slide``).

Bloc MINCE : il nomme un code d'instrument et un gabarit, rien d'autre — les
textes viennent du gel, la mise en page de ``custom/axis_slides.py``. Un axe
= trois blocs (questions, synthèse, vote) : ordonner ou exclure se règle
ligne par ligne dans le book.
"""
# @guideline: postair-minimal

from custom.axis_slides import questions_slide


def build():
    questions_slide("TRU")
