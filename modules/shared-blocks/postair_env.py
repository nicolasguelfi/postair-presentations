"""Les drapeaux de lancement d'un module — la vérité UNIQUE.

Décision NG (planche editable ``verite=p1``, 2026-09-02) : la tuyauterie
``IS_EDITABLE``/``IS_EXPORTABLE`` était dupliquée dans 7 ``custom/config.py``
identiques (héritage du commit fondateur, répliqué avec tout ``custom/``) —
elle vit désormais ICI, et les ``config.py`` de module sont des coquilles
d'une ligne (compat des imports ``from custom.config import IS_EDITABLE``),
à résorber au geste de capitalisation P5.

Règle NG (même ligne, ``regle=p3`` commentée) : les modes de lancement se
règlent par le **``.env`` LOCAL du module** — gitignoré, machine-local,
copiable poste par poste — **jamais par une variable d'environnement globale
à la machine**. Le chargement fait ``os.environ.setdefault`` : une variable
déjà posée par le processus appelant garde la main — c'est ainsi que les
outils (``check_i18n``, ``check_export_media``, ``check_projection``)
forcent ``STX_EDITABLE=false`` pour qu'aucune UI d'édition ne fuie dans un
export, quel que soit le ``.env`` du module.

Sémantique STRICTEMENT identique à l'ancienne (aucun changement de
comportement) : mêmes clés, même précédence, mêmes défauts.
"""

from __future__ import annotations

import os
from pathlib import Path


def _load_env(env_file: Path) -> None:
    """Charge un ``.env`` en ``setdefault`` — l'extérieur garde la main."""
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())


def module_flags(module_dir: Path) -> tuple[bool, bool]:
    """``(IS_EDITABLE, IS_EXPORTABLE)`` du module — après son ``.env`` local."""
    _load_env(Path(module_dir) / ".env")
    return (
        os.environ.get("STX_EDITABLE", "false").lower() == "true",
        os.environ.get("STX_EXPORT", "false").lower() == "true",
    )
