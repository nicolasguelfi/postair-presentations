"""Vote — les trois réponses EN DÉFAVEUR (intensité croissante).

Bloc GÉNÉRIQUE, listé dix-huit fois dans le book (une occurrence par pôle,
NG 2026-08-24) : l'ancre de marqueur embarque l'index du registre, un
libellé répété ne collisionne pas ; le marqueur est CACHÉ pour que la barre
latérale ne liste que les slides porteuses. Si un jour il faut des ancres
nommées par pôle, envelopper dans une fabrique paramétrable — pas répliquer.
"""
# @guideline: postair-minimal

from custom.axis_slides import vote_oppose_slide


def build():
    vote_oppose_slide()
