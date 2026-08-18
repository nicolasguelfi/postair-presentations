"""Exécute le ``build()`` de chaque bloc, module par module — le filet R14.

Pourquoi cet outil (incident du 2026-08-18) : ``py_compile`` ne voit pas les
erreurs d'exécution. ``from streamtex import *`` masque le builtin ``list``
(le module ``streamtex/list.py`` de ``st_list``) : un ``list(...)`` dans un
bloc compile parfaitement et lève ``TypeError: 'module' object is not
callable`` au premier build de page — devant la salle si personne n'a projeté
la slide entre-temps. Ce script attrape cette famille entière d'erreurs en
construisant réellement chaque bloc, en mode bare Streamlit.

Usage::

    uv run python _project/tools/check_blocks_build.py            # tous les modules
    uv run python _project/tools/check_blocks_build.py postair_genai [...]

Chaque module tourne dans un SOUS-PROCESSUS séparé (cwd = le module) : les
paquets ``custom`` et ``blocks`` portent le même nom d'un module à l'autre et
entreraient en collision dans un seul interpréteur. Le registre TOC est
réinitialisé avant chaque bloc, comme ``st_book`` le fait à chaque page.

L'outil ne modifie rien. Code de sortie : 0 si tous les blocs construisent,
1 sinon — utilisable en contrôle d'avant-répétition comme en CI locale.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent.parent
_MODULES_DIR = _ROOT / "modules"

#: Le script exécuté DANS chaque module (cwd = le module, venv du projet).
_CHILD = r"""
import importlib, pathlib, sys
sys.path.insert(0, '.')
import setup  # noqa: F401 — sys.path du module (shared-blocks, packs)
from streamtex.toc import reset_toc_registry

fails = 0
for p in sorted(pathlib.Path('blocks').glob('bck_*.py')):
    name = p.stem
    try:
        reset_toc_registry()
        importlib.import_module(f'blocks.{name}').build()
        print(f'OK    {name}')
    except Exception as e:  # noqa: BLE001 — tout échec de build est un échec
        fails += 1
        print(f'FAIL  {name}: {type(e).__name__}: {e}')
sys.exit(1 if fails else 0)
"""


def check_module(module_dir: Path) -> bool:
    """Construit tous les blocs d'un module ; True si tout passe."""
    print(f"===== {module_dir.name} =====")
    proc = subprocess.run(
        [sys.executable, "-c", _CHILD],
        cwd=module_dir, capture_output=True, text=True,
    )
    # Le mode bare de Streamlit émet des avertissements sans intérêt ici.
    for line in proc.stdout.splitlines():
        if line.startswith(("OK", "FAIL")):
            print(f"  {line}")
    if proc.returncode != 0 and "FAIL" not in proc.stdout:
        # Échec avant la boucle (setup, import module) : montrer la cause.
        print(proc.stderr.strip().splitlines()[-1] if proc.stderr else "?")
    return proc.returncode == 0


def main() -> int:
    wanted = sys.argv[1:]
    modules = [
        d for d in sorted(_MODULES_DIR.iterdir())
        if (d / "blocks").is_dir() and (d / "setup.py").exists()
        and (not wanted or d.name in wanted)
    ]
    if not modules:
        print(f"aucun module à contrôler (demandés : {wanted})")
        return 1
    broken = [d.name for d in modules if not check_module(d)]
    if broken:
        print(f"\nÉCHEC — blocs cassés dans : {', '.join(broken)}")
        return 1
    print(f"\nOK — tous les blocs de {len(modules)} module(s) construisent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
