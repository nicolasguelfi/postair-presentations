"""Gel du glossaire POSTAIR — le vocabulaire bilingue canonique vient du hub.

``questionnaire/TRANSLATION-DE-GLOSSARY.json`` du hub ``ai-social-profiles``
(101 entrées ``{key, en, fr, de, note}``, validées V4 par l'auteur le
2026-08-09) est LA référence des termes : axes, pôles et abréviations,
archétypes, registres, échelle, « posture »… Ce dépôt le gèle dans
``modules/shared-blocks/static/data/glossary.json`` — même contrat que les
autres gels : jamais édité à la main, régénéré ; le hub est la vérité et une
correction se fait là-bas.

Consommé par ``postair_i18n.term(key, lang)`` (les blocs) et par la lentille
« terminologie » de la recette de traduction (plan-i18n §4, R6).

Usage::

    uv run python _project/tools/build_glossary_content.py               # regel
    uv run python _project/tools/build_glossary_content.py --work-order  # constat, sans écrire
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

_TOOLS = Path(__file__).parent
_REPO = _TOOLS.parent.parent
_CONFIG = _TOOLS / "debates-hub.config.local.json"
_FREEZE = _REPO / "modules" / "shared-blocks" / "static" / "data" / "glossary.json"
_SOURCE = Path("questionnaire") / "TRANSLATION-DE-GLOSSARY.json"


def _hub() -> Path:
    if not _CONFIG.exists():
        raise SystemExit(
            f"config machine absente : {_CONFIG.name} — copier "
            f"debates-hub.config.example.json et renseigner la clé `hub`.")
    hub = Path(json.loads(_CONFIG.read_text(encoding="utf-8"))["hub"])
    if not (hub / _SOURCE).exists():
        raise SystemExit(f"glossaire introuvable : {hub / _SOURCE}")
    return hub


def _hub_commit(hub: Path) -> str:
    proc = subprocess.run(["git", "-C", str(hub), "rev-parse", "--short", "HEAD"],
                          capture_output=True, text=True)
    return proc.stdout.strip() if proc.returncode == 0 else "?"


def _build(hub: Path) -> dict:
    entries = json.loads((hub / _SOURCE).read_text(encoding="utf-8"))
    terms = {}
    for e in entries:
        key = e["key"]
        if key in terms:
            raise SystemExit(f"clé dupliquée dans le glossaire du hub : {key}")
        if not e.get("en") or not e.get("fr"):
            raise SystemExit(f"entrée sans en/fr dans le glossaire du hub : {key}")
        terms[key] = {"en": e["en"], "fr": e["fr"], **({"de": e["de"]} if e.get("de") else {})}
    return {
        "metadata": {
            "_doc": "GÉNÉRÉ par _project/tools/build_glossary_content.py — ne jamais "
                    "éditer : régénérer. Le hub est la vérité.",
            "source": _SOURCE.as_posix(),
            "hub_commit": _hub_commit(hub),
            "languages": ["en", "fr", "de"],
            "default_language": "en",
            "entries": len(terms),
        },
        "terms": terms,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--work-order", action="store_true", help="constat sans écrire")
    args = ap.parse_args()
    hub = _hub()
    fresh = _build(hub)
    if args.work_order:
        if not _FREEZE.exists():
            print("**gel absent** — régénérer.")
            return 0
        frozen = json.loads(_FREEZE.read_text(encoding="utf-8"))
        changed = [k for k, v in fresh["terms"].items() if frozen["terms"].get(k) != v]
        gone = [k for k in frozen["terms"] if k not in fresh["terms"]]
        print(f"**{len(changed)} entrée(s) modifiée(s) · {len(gone)} disparue(s) · "
              f"{len(fresh['terms'])} au hub ({fresh['metadata']['hub_commit']})**")
        for k in (changed + gone)[:20]:
            print(f"  ~ {k}")
        return 0
    _FREEZE.parent.mkdir(parents=True, exist_ok=True)
    _FREEZE.write_text(json.dumps(fresh, ensure_ascii=False, indent=1) + "\n",
                       encoding="utf-8")
    print(f"gel écrit : {_FREEZE.relative_to(_REPO)} — {len(fresh['terms'])} entrées, "
          f"hub {fresh['metadata']['hub_commit']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
