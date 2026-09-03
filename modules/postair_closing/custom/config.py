"""Runtime flags du module — coquille de COMPAT vers la vérité unique.

La définition vit dans ``shared-blocks/postair_env.py`` (décision NG,
planche editable ``verite=p1``, 2026-09-02) : le ``.env`` LOCAL du module
règle les modes de lancement, jamais une variable globale machine. Cette
coquille garde les imports existants (``from custom.config import
IS_EDITABLE``) et disparaîtra au geste de capitalisation P5.
"""

from pathlib import Path

from postair_env import module_flags

IS_EDITABLE, IS_EXPORTABLE = module_flags(Path(__file__).parent.parent)
