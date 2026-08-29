"""Gel du vocabulaire des ÉCRANS — les intitulés de l'application viennent de sumvadis.

Septième tuyau sumvadis → présentations (DD-113, option O2, 2026-08-29) :
``packages/core/assets/ecrans/vocabulaire.json`` du dépôt ``sumvadis`` (GÉNÉRÉ
là-bas par ``pnpm vocabulaire:ecrans`` depuis ``screens.ts`` + ``i18n.ts`` ; 33
écrans — les identifiants du registre des captures — avec ``title`` /
``action`` / ``hint`` en en/fr/de ; fichier de dépôt lu PAR CHEMIN, jamais servi
par le CDN). Ce dépôt le gèle dans ``modules/shared-blocks/static/data/screens.json``
— même contrat que le glossaire : jamais édité à la main, régénéré ; un libellé
faux ou manquant se corrige DANS sumvadis, puis se regèle ici.

Consommé par ``postair_i18n.screen(id, role, lang)`` : ce qu'une slide CITE de
l'interface (le nom d'un bouton, le titre d'un écran que le participant verra
sur son téléphone) passe par là ; ce que le deck dit avec ses mots reste une
feuille du bloc (règle R-i18n).

Usage::

    uv run python _project/tools/build_screens_vocabulary.py               # regel
    uv run python _project/tools/build_screens_vocabulary.py --work-order  # constat, sans écrire
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

_TOOLS = Path(__file__).parent
_REPO = _TOOLS.parent.parent
_CONFIG = _TOOLS / "survey-captures.config.local.json"
_FREEZE = _REPO / "modules" / "shared-blocks" / "static" / "data" / "screens.json"
_SOURCE = Path("packages") / "core" / "assets" / "ecrans" / "vocabulaire.json"
ROLES = ("title", "action", "hint")


def _sumvadis() -> Path:
    if not _CONFIG.exists():
        raise SystemExit(
            f"config machine absente : {_CONFIG.name} — copier "
            f"survey-captures.config.example.json et renseigner la clé `sumvadis`.")
    root = Path(json.loads(_CONFIG.read_text(encoding="utf-8"))["sumvadis"])
    if not (root / _SOURCE).exists():
        raise SystemExit(f"vocabulaire introuvable : {root / _SOURCE}")
    return root


def _commit(root: Path) -> str:
    proc = subprocess.run(["git", "-C", str(root), "rev-parse", "--short", "HEAD"],
                          capture_output=True, text=True)
    return proc.stdout.strip() if proc.returncode == 0 else "?"


def _build(root: Path) -> dict:
    src = json.loads((root / _SOURCE).read_text(encoding="utf-8"))
    screens = {}
    for s in src["screens"]:
        sid = s["id"]
        if sid in screens:
            raise SystemExit(f"écran dupliqué dans le vocabulaire sumvadis : {sid}")
        entry = {}
        for role in ROLES:
            node = s.get(role)
            if not node:
                continue
            if not node.get("en") or not node.get("fr"):
                raise SystemExit(f"{sid}.{role} sans en/fr dans le vocabulaire sumvadis")
            entry[role] = {"key": node.get("key"),
                           **{l: node[l] for l in ("en", "fr", "de") if node.get(l)}}
        if "title" not in entry:
            raise SystemExit(f"{sid} sans title dans le vocabulaire sumvadis")
        screens[sid] = entry
    return {
        "metadata": {
            "_doc": "GÉNÉRÉ par _project/tools/build_screens_vocabulary.py — ne jamais "
                    "éditer : régénérer. sumvadis est la vérité (DD-113).",
            "source": _SOURCE.as_posix(),
            "source_version": src.get("version"),
            "source_sha256": src.get("sha256"),
            "sumvadis_commit": _commit(root),
            "languages": src.get("langs", ["en", "fr", "de"]),
            "default_language": "en",
            "screens": len(screens),
        },
        "screens": screens,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--work-order", action="store_true", help="constat sans écrire")
    args = ap.parse_args()
    root = _sumvadis()
    fresh = _build(root)
    if args.work_order:
        if not _FREEZE.exists():
            print("**gel absent** — régénérer.")
            return 1
        frozen = json.loads(_FREEZE.read_text(encoding="utf-8"))
        changed = [k for k, v in fresh["screens"].items() if frozen["screens"].get(k) != v]
        gone = [k for k in frozen["screens"] if k not in fresh["screens"]]
        print(f"**{len(changed)} écran(s) modifié(s) · {len(gone)} disparu(s) · "
              f"{len(fresh['screens'])} chez sumvadis ({fresh['metadata']['sumvadis_commit']}, "
              f"v{fresh['metadata']['source_version']})**")
        for k in (changed + gone)[:20]:
            print(f"  ~ {k}")
        return 1 if (changed or gone) else 0
    _FREEZE.parent.mkdir(parents=True, exist_ok=True)
    _FREEZE.write_text(json.dumps(fresh, ensure_ascii=False, indent=1) + "\n",
                       encoding="utf-8")
    print(f"gel écrit : {_FREEZE.relative_to(_REPO)} — {len(fresh['screens'])} écrans, "
          f"sumvadis {fresh['metadata']['sumvadis_commit']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
