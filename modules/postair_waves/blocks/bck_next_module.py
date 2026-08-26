"""Fin de deck — le gros bouton vers le module suivant (chaîne du jour).

Générique : la slide est rendue par ``postair_chain.build_next_module_slide``.
L'ordre des modules et les URLs viennent de la source unique
``postair_collection/collection.toml``.

SPEAKER NOTES:
Rien à dire — un clic sur le bouton et le deck suivant s'ouvre dans le même
onglet.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from postair_chain import build_next_module_slide


def build():
    # Clé EXPLICITE, jamais déduite du répertoire courant (PLAYBOOK §2).
    build_next_module_slide(s, current="waves")
