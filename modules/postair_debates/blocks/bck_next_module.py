"""Fin de deck — le gros bouton vers le module suivant (chaîne du jour).

Générique : la slide est rendue par ``postair_chain.build_next_module_slide``.
L'ordre des modules et les URLs viennent de la source unique
``postair_collection/collection.toml`` (surcharge ``STX_URL_<KEY>`` en
déploiement) — le hub et ce bouton ne peuvent pas diverger. Après le dernier
module de l'ordre du jour, la boucle revient au premier.

SPEAKER NOTES:
Rien à dire — un clic sur le bouton et le deck suivant s'ouvre dans le même
onglet. La slide reste à l'écran pendant la transition de séance.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from postair_chain import build_next_module_slide


def build(lang: str = "en", **_):
    # Clé EXPLICITE : le répertoire de travail dépend du lanceur
    # (run-postair lance depuis la racine, le conteneur depuis le
    # module) — constaté le 2026-08-19, gel de l'overlay au chargement.
    build_next_module_slide(s, current="debates")
