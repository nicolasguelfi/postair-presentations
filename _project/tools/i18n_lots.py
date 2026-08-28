"""Les lots de traduction — extraire les feuilles sans ``fr``, réinjecter le ``fr``.

Recette R3→R7 du plan-i18n (2026-08-28). Une feuille est un dict littéral
``{"en": …}`` dans un bloc ou un gabarit ; ce module la retrouve par l'AST,
l'exporte en JSON pour les agents (traducteur V1, rétro-traducteur V2,
lentilles V3) et réécrit le fichier source avec la clé ``"fr"`` ajoutée —
par position exacte (``end_lineno``/``end_col_offset``), sans reformater le
reste. Le code n'est jamais généré : seule la clé ``"fr"`` est insérée.

Formes de valeur :

- chaîne : ``{"en": "text"}`` → ``fr`` = chaîne ;
- fragments ``st_write`` : ``{"en": ("Already here — ", (KW, "usage"))}`` →
  ``fr`` = liste de fragments ``[{"text": "…"}, {"kw": "…"}]`` où ``kw``
  reprend l'expression de style du fragment EN de MÊME rang (elle est copiée
  telle quelle du source) ; le nombre et le motif des fragments doivent être
  identiques à l'EN ;
- concaténation implicite (``"a" "b"``) ou explicite (``"a" + "b"``) :
  aplatie en une chaîne à l'extraction, ``fr`` = chaîne.

Usage::

    uv run python _project/tools/i18n_lots.py --extract postair_opening -o lot.json
    uv run python _project/tools/i18n_lots.py --inject lot.fr.json
"""

from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path

_TOOLS = Path(__file__).parent
_REPO = _TOOLS.parent.parent
_MODULES_DIR = _REPO / "modules"


def _py_files(module: str) -> list[Path]:
    root = _MODULES_DIR / module
    files = sorted((root / "blocks").glob("bck_*.py")) if (root / "blocks").is_dir() else []
    files += sorted((root / "custom").glob("*.py")) if (root / "custom").is_dir() else []
    return files


def _str_of(node: ast.AST) -> str | None:
    """Le texte d'une expression-chaîne (constante, concaténation), sinon None."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        a, b = _str_of(node.left), _str_of(node.right)
        if a is not None and b is not None:
            return a + b
    return None


def _fragments(node: ast.AST, src: str) -> list[dict] | None:
    """Une séquence de fragments st_write → [{"text"} | {"kw", "style"}]."""
    if not isinstance(node, (ast.Tuple, ast.List)):
        return None
    out = []
    for e in node.elts:
        s = _str_of(e)
        if s is not None:
            out.append({"text": s})
        elif isinstance(e, ast.Tuple) and len(e.elts) == 2 and _str_of(e.elts[1]) is not None:
            out.append({"kw": _str_of(e.elts[1]), "style": ast.get_source_segment(src, e.elts[0])})
        else:
            return None
    return out


class _Leaves(ast.NodeVisitor):
    def __init__(self, src: str):
        self.src = src
        self.found: list[dict] = []

    def visit_Dict(self, node: ast.Dict):
        keys = {k.value: v for k, v in zip(node.keys, node.values)
                if isinstance(k, ast.Constant) and isinstance(k.value, str)}
        if "en" in keys:
            en = keys["en"]
            entry = {"line": node.lineno, "col": node.col_offset,
                     "end_line": node.end_lineno,
                     "end_col": node.end_col_offset, "has_fr": "fr" in keys}
            s = _str_of(en)
            if s is not None:
                entry.update(kind="text", en=s)
            else:
                fr = _fragments(en, self.src)
                if fr is None:
                    entry.update(kind="unsupported", en=ast.get_source_segment(self.src, en))
                else:
                    entry.update(kind="fragments", en=fr)
            self.found.append(entry)
            return
        self.generic_visit(node)


def extract(module: str, only_missing: bool = True) -> list[dict]:
    lots = []
    for path in _py_files(module):
        src = path.read_text(encoding="utf-8")
        v = _Leaves(src)
        v.visit(ast.parse(src))
        rel = path.relative_to(_REPO).as_posix()
        for i, e in enumerate(v.found):
            if only_missing and e["has_fr"]:
                continue
            lots.append({"id": f"{rel}:{e['line']}:{e['col']}", "file": rel,
                         "line": e["line"], "col": e["col"],
                         "kind": e["kind"], "en": e["en"], "fr": None,
                         "context": _context(src, e["line"])})
    return lots


def _context(src: str, line: int, width: int = 2) -> str:
    lines = src.splitlines()
    lo, hi = max(0, line - 1 - width), min(len(lines), line + width)
    return "\n".join(lines[lo:hi])


def _py_str(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def _render_fr(kind: str, en, fr) -> str:
    if kind == "text":
        if not isinstance(fr, str):
            raise ValueError("fr doit être une chaîne")
        return _py_str(fr)
    if kind == "fragments":
        if not isinstance(fr, list) or len(fr) != len(en):
            raise ValueError(f"fr doit avoir {len(en)} fragments, même motif que en")
        parts = []
        for e, f in zip(en, fr):
            if "kw" in e:
                if "kw" not in f:
                    raise ValueError("fragment stylé attendu (clé 'kw')")
                parts.append(f"({e['style']}, {_py_str(f['kw'])})")
            else:
                if "text" not in f:
                    raise ValueError("fragment texte attendu (clé 'text')")
                parts.append(_py_str(f["text"]))
        return "(" + ", ".join(parts) + ("," if len(parts) == 1 else "") + ")"
    raise ValueError(f"forme non injectable : {kind}")


def inject(lot: list[dict]) -> dict[str, int]:
    """Insère ``"fr"`` dans chaque feuille du lot ; retourne {fichier: n}."""
    by_file: dict[str, list[dict]] = {}
    for e in lot:
        if e.get("fr") is None or e.get("fr") == []:
            continue   # une chaîne vide est une valeur voulue : injectée
        by_file.setdefault(e["file"], []).append(e)
    done: dict[str, int] = {}
    for rel, entries in by_file.items():
        path = _REPO / rel
        src = path.read_text(encoding="utf-8")
        lines = src.splitlines(keepends=True)
        # Retrouver les feuilles ACTUELLES par ligne de début (le fichier a pu
        # bouger depuis l'extraction : on refuse si la ligne ne porte plus la
        # même feuille EN).
        v = _Leaves(src)
        v.visit(ast.parse(src))
        current = {(f["line"], f["col"]): f for f in v.found}
        # Injection de bas en haut et de droite à gauche pour ne pas décaler
        # les positions encore à traiter.
        for e in sorted(entries, key=lambda x: (-x["line"], -x["col"])):
            cur = current.get((e["line"], e["col"]))
            if cur is None or cur["en"] != e["en"]:
                raise SystemExit(f"{e['id']}: la feuille a changé depuis l'extraction — réextraire")
            if cur["has_fr"]:
                raise SystemExit(f"{e['id']}: porte déjà un fr")
            rendered = _render_fr(cur["kind"], cur["en"], e["fr"])
            # Les offsets de l'AST sont en OCTETS utf-8 : convertir en index
            # de caractères sur la ligne (un « — » compte trois octets).
            li = cur["end_line"] - 1
            line = lines[li]
            col = len(line.encode("utf-8")[:cur["end_col"] - 1].decode("utf-8"))
            assert line[col] == "}", (e["id"], line)
            before = line[:col].rstrip()
            sep = "" if before.endswith(",") else ","
            lines[li] = f'{before}{sep} "fr": {rendered}{line[col:]}'
            done[rel] = done.get(rel, 0) + 1
        path.write_text("".join(lines), encoding="utf-8")
    return done


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--extract", metavar="MODULE")
    ap.add_argument("--all", action="store_true", help="extraire aussi les feuilles déjà traduites")
    ap.add_argument("-o", "--out")
    ap.add_argument("--inject", metavar="LOT_JSON")
    args = ap.parse_args()
    if args.extract:
        lot = extract(args.extract, only_missing=not args.all)
        text = json.dumps(lot, ensure_ascii=False, indent=1)
        if args.out:
            Path(args.out).write_text(text, encoding="utf-8")
            kinds = {}
            for e in lot:
                kinds[e["kind"]] = kinds.get(e["kind"], 0) + 1
            print(f"{len(lot)} feuille(s) → {args.out} {kinds}")
        else:
            print(text)
        return 0
    if args.inject:
        lot = json.loads(Path(args.inject).read_text(encoding="utf-8"))
        done = inject(lot)
        for rel, n in done.items():
            print(f"  {n:3d} fr injecté(s) → {rel}")
        print(f"total : {sum(done.values())}")
        return 0
    ap.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
