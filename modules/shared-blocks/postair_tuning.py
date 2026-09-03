"""st_tuning — la résolution de réglages à trois étages (chparam2, NG 2026-09-03).

Décision NG (planche chparam2, ``api=a1 prec=p1 ou=o1`` amendé) : UNE commande
qui résout un dict de réglages depuis trois étages, du plus froid au plus
chaud —

1. **defaults** : les valeurs sûres, écrites dans le BLOC de la slide — elles
   définissent les clés ET les types attendus (le schéma) ;
2. **local** : les surcharges du bloc (la main de l'auteur) — comme les
   ``bck_*`` sont rechargés à chaud par le registre ET comptés dans le hash
   du cache de pages, éditer ce dict est pris AU PROCHAIN RERUN, sans tuer
   les processus (c'est l'amendement o1 : « la configuration dans le bloc ») ;
3. **json_path** : un JSON optionnel, résolu par les static sources du book
   (jamais ``Path.cwd`` — la leçon du diaporama) et RELU à chaque appel —
   l'étage de la répétition et de la séance : éditer le fichier + la touche
   R de Streamlit suffisent.

Précédence : ``defaults ← local ← json`` (le json gagne — c'est l'étage qu'on
édite à chaud). Panne = RÉTROGRADER d'un étage, jamais casser une slide en
séance : fichier absent = silence normal ; json illisible = étage ignoré ;
clé inconnue ou type incompatible = cette clé ignorée. Les avertissements
sont BRUYANTS en mode éditeur (``STX_EDITABLE``) et vont à la console sinon.

⚠ PÉRIMÈTRE (clarification NG, critique) : cette commande sert les SLIDES DE
CHRONOMÈTRE (opening ×3, démo genai). Les autres ``TUNING`` du dépôt
(matrices, images, colonnes, diaporamas…) ne migrent PAS dessus — toute
extension est une décision NG explicite, jamais une généralisation.

⚠ Module PARTAGÉ (shared-blocks) : une édition ICI exige un redémarrage —
mais c'est tout l'intérêt : après elle, l'itération vit dans le bloc (chaud)
et dans le json (chaud).
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import streamlit as st


def _warn(msg: str) -> None:
    """Bruyant en mode éditeur, console seulement en séance (prec=p1)."""
    if os.environ.get("STX_EDITABLE", "").strip().lower() in ("1", "true", "yes"):
        st.warning(f"st_tuning : {msg}")
    else:
        print(f"[st_tuning] {msg}")


def _compatible(default_value, value) -> bool:
    """Le type de ``value`` est-il acceptable pour cette clé du schéma ?"""
    if default_value is None:
        return True                      # None au schéma = type libre
    if isinstance(default_value, bool):  # bool AVANT int (sous-classe)
        return isinstance(value, bool)
    if isinstance(default_value, (int, float)):
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if isinstance(default_value, tuple):
        return isinstance(value, (list, tuple))  # le json dit [1, 3]
    return isinstance(value, type(default_value))


def _overlay(base: dict, layer: dict, origin: str, defaults: dict) -> None:
    """Superpose ``layer`` sur ``base``, clé par clé, schéma en garde-fou."""
    for k, v in layer.items():
        if k not in defaults:
            _warn(f"{origin} : clé inconnue {k!r} ignorée "
                  f"(schéma : {', '.join(sorted(defaults))})")
            continue
        if not _compatible(defaults[k], v):
            _warn(f"{origin} : {k!r} de type {type(v).__name__} incompatible "
                  f"avec le défaut {type(defaults[k]).__name__} — clé ignorée")
            continue
        if isinstance(defaults[k], tuple) and isinstance(v, list):
            v = tuple(v)                 # le json ne connaît pas les tuples
        base[k] = v


def st_tuning(defaults: dict, local: dict | None = None,
              json_path: str | None = None) -> dict:
    """Le dict de réglages RÉSOLU : ``defaults ← local ← json``.

    À appeler DANS ``build()`` pour que l'étage json soit relu à chaque
    affichage. ``json_path`` est relatif aux static sources du book
    (p.ex. ``"data/timers-part1.json"``) ; fichier absent = silence.
    """
    out = dict(defaults)
    if local:
        _overlay(out, local, "dict local", defaults)
    if json_path:
        from streamtex import get_static_sources
        path = next((c for c in (Path(src) / json_path
                                 for src in get_static_sources())
                     if c.is_file()), None)
        if path is not None:
            try:
                layer = json.loads(path.read_text(encoding="utf-8"))
                if not isinstance(layer, dict):
                    raise ValueError(f"racine {type(layer).__name__}, "
                                     f"objet attendu")
                _overlay(out, layer, path.name, defaults)
            except (OSError, ValueError) as e:
                _warn(f"{json_path} illisible ({e}) — étage json ignoré, "
                      f"les défauts/local jouent")
    return out
