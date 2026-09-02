"""La porte i18n — l'anglais ne bouge pas, le français ne manque pas.

Chantier EN/FR (plan-i18n, NG 2026-08-28). Cinq contrôles, aucun ne modifie
le dépôt (sauf ``--baseline``, qui écrit la référence LOCALE non versionnée) :

- ``--baseline [modules]`` — fige l'export EN de chaque module dans
  ``_project/i18n/baseline/<module>.json`` : marqueurs, entrées TOC, texte
  par marqueur, médias. C'est la photographie de « ce qui est projeté
  aujourd'hui ». À refaire seulement quand l'EN d'un module évolue de façon
  voulue (lot 2 : au tag ``en-final/<module>``).
- ``--regress [modules]`` — exporte ``STX_LANG=en`` et compare à la baseline.
  Toute différence = ROUGE : le chantier i18n ne doit changer AUCUN octet de
  ce que l'anglais projette (doctrine « l'anglais ne bouge pas »).
- ``--inventory [modules]`` — les littéraux anglais NUS (chaînes passées
  directement à ``st_write``/``st_marker``/``st_info_tooltip``/
  ``st_slide_break``/``label=``/``toc_label=``, ou constantes ``str`` de
  module qu'ils consomment) et les feuilles ``{"en": …}`` sans ``fr``. C'est
  le work-order des migrateurs et des traducteurs.
- ``--parity [modules]`` — chaque feuille porte toutes les LANGS, non vides,
  ``fr != en`` sauf liste blanche (``_project/i18n/whitelist.txt``) ; si
  l'export FR est demandé (``--with-export``), même nombre de marqueurs et
  mêmes médias qu'en EN.
- ``--words [modules]`` — puces FR de plus de 8 mots quand l'EN en a 8 ou
  moins (règle R3) : avertissement, jamais rouge.
- ``--drift <ref> [modules]`` — feuilles dont l'EN a changé depuis ``<ref>``
  (git) sans que le FR bouge : le filet contre le glissement futur.

``--report`` imprime la ligne de synthèse lue par ``check_all.py`` :
``**N littéral(s) nu(s) · N feuille(s) sans fr · N régression(s)**``.

Sévérité pendant le chantier : ``--regress`` est ROUGE dès le socle ;
inventaire et parité sont des avertissements tant que le module figure dans
``I18N_PENDING`` (vidé module par module au tag ``i18n/<module>-done``).

Exception assumée : un littéral qui est une DONNÉE citée verbatim dans
toutes les langues (règle R-case — ex. la fausse référence Varghese de
genai) se marque ``i18n: verbatim`` dans un commentaire sur sa ligne ou la
ligne au-dessus — l'inventaire le saute. Le marqueur est un engagement
d'auteur, pas un échappatoire : il dit « ceci ne se traduit pas », il ne
blanchit jamais un oubli.

Usage::

    uv run python _project/tools/check_i18n.py --baseline
    uv run python _project/tools/check_i18n.py --regress postair_opening
    uv run python _project/tools/check_i18n.py --inventory postair_survey
    uv run python _project/tools/check_i18n.py --report            # pour check_all
"""

from __future__ import annotations

import argparse
import ast
import json
from functools import lru_cache
import os
import re
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path

_TOOLS = Path(__file__).parent
_REPO = _TOOLS.parent.parent
_MODULES_DIR = _REPO / "modules"
_BASELINE_DIR = _REPO / "_project" / "i18n" / "baseline"
_WHITELIST = _REPO / "_project" / "i18n" / "whitelist.txt"

LANGS = ("en", "fr")

#: Modules dont la traduction n'est pas encore exigée : inventaire et parité y
#: sont des avertissements. Un module en sort au tag ``i18n/<module>-done``.
I18N_PENDING = {
    # lot 1 : opening, waves, handsup, survey sortis le 2026-08-29 (tags i18n/<module>-done)
    # lot 2 : debates sorti le 2026-08-30 (tag i18n/postair_debates-done) ;
    # lot 3 : genai sorti le 2026-09-03 (relecture NG planche prep1, tag
    # i18n/postair_genai-done — l'exception Varghese porte « i18n: verbatim ») ;
    # les autres quand leur anglais sera fini (tag en-final/<module>)
    "postair_guidelines", "postair_collection",
}

#: Les appels dont les chaînes sont projetées.
_TEXT_CALLS = {"st_write", "st_marker", "st_info_tooltip", "st_slide_break",
               "st_hover_tooltip"}
#: Les mots-clés dont la valeur est projetée (dans tout appel).
_TEXT_KWARGS = {"label", "toc_label", "marker_label", "title", "caption",
                "hint", "entries", "placeholder", "button_label"}
#: Les mots-clés jamais projetés (chemins, clés, styles).
_SKIP_KWARGS = {"tag", "key", "link", "uri", "name", "alt", "alt_ready",
                "alt_fallback", "toc_lvl", "cols", "gap", "width", "height",
                "cell_styles", "grid_style", "style", "overlay", "prompt",
                "device", "theme", "lang", "facette", "slug", "variant",
                "ratio", "error", "scale", "border", "format_func"}
#: Les fonctions d'enveloppe qui rendent une chaîne « traduite ».
_TRANSLATORS = {"T", "TF", "text", "term", "ui"}

_GREEN, _RED, _YELLOW, _OFF = "\033[32m", "\033[31m", "\033[33m", "\033[0m"


def _modules(wanted: list[str]) -> list[str]:
    if wanted:
        return wanted
    return sorted(p.name for p in _MODULES_DIR.iterdir()
                  if p.name.startswith("postair_") and (p / "book.py").exists())


# ── Export et photographie ──────────────────────────────────────────────────

class _Snapshot(HTMLParser):
    """Texte par section de marqueur, entrées TOC, médias — hors chrome."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.markers: list[str] = []
        self.toc: list[str] = []
        self.media: list[str] = []
        self.texts: dict[str, list[str]] = {"__before__": []}
        self._current = "__before__"
        self._skip_depth = 0
        self._in_nav = 0
        self._in_toc_entry = False
        self._stack: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self._stack.append(tag)
        if tag in ("script", "style"):
            self._skip_depth += 1
        if tag == "nav":
            self._in_nav += 1
        if self._in_nav and "stx-toc-entry" in a.get("class", ""):
            self._in_toc_entry = True
        mid = a.get("id", "")
        if mid.startswith("stx-marker-") and mid != "stx-marker-nav" \
                and "data-marker-index" in a:
            self.markers.append(mid)
            self._current = mid
            self.texts[mid] = []
        if tag in ("img", "video", "source", "audio"):
            src = a.get("src") or ""
            if src and not re.match(r"^(https?:|data:|blob:)", src) and not self._in_nav:
                self.media.append(src)

    def handle_endtag(self, tag):
        if self._stack:
            self._stack.pop()
        if tag in ("script", "style") and self._skip_depth:
            self._skip_depth -= 1
        if tag == "nav" and self._in_nav:
            self._in_nav -= 1
        if tag == "div" and self._in_toc_entry:
            self._in_toc_entry = False

    def handle_data(self, data):
        if self._skip_depth:
            return
        t = " ".join(data.split())
        if not t:
            return
        if self._in_nav:
            if self._in_toc_entry:
                self.toc.append(t)
            return
        self.texts[self._current].append(t)


def _export(module: str, lang: str, out_dir: Path) -> Path:
    env = dict(os.environ, STX_EDITABLE="false", STX_LANG=lang)
    r = subprocess.run(["uv", "run", "stx", "export", "html",
                        f"modules/{module}", "-o", str(out_dir),
                        "--asset-mode", "external"],
                       cwd=_REPO, capture_output=True, text=True, env=env)
    if r.returncode != 0:
        raise RuntimeError(f"{module}/{lang}: export en échec — {r.stderr.strip()[-400:]}")
    htmls = list(out_dir.rglob("*.html"))
    if not htmls:
        raise RuntimeError(f"{module}/{lang}: aucun HTML exporté")
    return htmls[0]


def snapshot(module: str, lang: str = "en") -> dict:
    with tempfile.TemporaryDirectory(prefix=f"stx-i18n-{module}-{lang}-") as tmp:
        html = _export(module, lang, Path(tmp))
        p = _Snapshot()
        p.feed(html.read_text(encoding="utf-8"))
    return {
        "module": module, "lang": lang,
        "markers": p.markers,
        "toc": p.toc,
        "media": sorted(set(p.media)),
        "text": {k: " ".join(v) for k, v in p.texts.items()},
    }


def _diff_snapshots(ref: dict, cur: dict) -> list[str]:
    out: list[str] = []
    if ref["markers"] != cur["markers"]:
        a, b = set(ref["markers"]), set(cur["markers"])
        out.append(f"marqueurs : {len(ref['markers'])} → {len(cur['markers'])}"
                   + (f" ; disparus {sorted(a - b)[:5]}" if a - b else "")
                   + (f" ; apparus {sorted(b - a)[:5]}" if b - a else ""))
    if ref["toc"] != cur["toc"]:
        out.append(f"TOC : {[x for x in ref['toc'] if x not in cur['toc']][:5]} → "
                   f"{[x for x in cur['toc'] if x not in ref['toc']][:5]}")
    if ref["media"] != cur["media"]:
        a, b = set(ref["media"]), set(cur["media"])
        out.append(f"médias : -{len(a - b)} +{len(b - a)}")
    for k, v in ref["text"].items():
        w = cur["text"].get(k)
        if w is None:
            continue
        if v != w:
            # Premier point de divergence, pour lire vite.
            i = next((i for i, (x, y) in enumerate(zip(v, w)) if x != y), min(len(v), len(w)))
            out.append(f"texte [{k}] diverge à {i} : « …{v[max(0, i-30):i+50]} » ≠ "
                       f"« …{w[max(0, i-30):i+50]} »")
    return out


# ── Inventaire AST ──────────────────────────────────────────────────────────

def _py_files(module: str) -> list[Path]:
    root = _MODULES_DIR / module
    files = sorted((root / "blocks").glob("bck_*.py")) if (root / "blocks").is_dir() else []
    files += sorted((root / "custom").glob("*.py")) if (root / "custom").is_dir() else []
    return files


def _call_name(node: ast.AST) -> str:
    f = node.func if isinstance(node, ast.Call) else None
    if isinstance(f, ast.Name):
        return f.id
    if isinstance(f, ast.Attribute):
        return f.attr
    return ""


def _is_text(s: str) -> bool:
    if s.startswith(("http://", "https://", "app/static/", "images/")):
        return False   # une URL ou un chemin : projeté tel quel, pas traduit
    return len(s) >= 2 and any(c.isalpha() for c in s) and s.strip() not in {
        "v", "h", "div", "span", "p", "en", "fr", "de"}


class _Inventory(ast.NodeVisitor):
    """Chaînes nues, feuilles, dans un fichier."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.const_str: dict[str, ast.AST] = {}      # NAME -> valeur (module)
        self.leaves: list[tuple[int, dict]] = []      # (ligne, {lang: str})
        self.bare: list[tuple[int, str]] = []         # (ligne, extrait)
        self._parents: list[ast.AST] = []

    # feuilles : tout dict littéral avec une clé "en"
    def visit_Dict(self, node: ast.Dict):
        keys = [k.value for k in node.keys if isinstance(k, ast.Constant)]
        if "en" in keys:
            leaf = {}
            for k, v in zip(node.keys, node.values):
                if isinstance(k, ast.Constant) and isinstance(k.value, str):
                    leaf[k.value] = _flatten(v)
            self.leaves.append((node.lineno, leaf))
            return   # ne pas redescendre : les chaînes dedans sont traduites
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign):
        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) \
                and not self._parents:
            self.const_str[node.targets[0].id] = node.value
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self._parents.append(node)
        self.generic_visit(node)
        self._parents.pop()

    # Les attributs de classe (BlockStyles.x = style) ne sont pas des
    # constantes de module : sans ceci, une variable locale du même nom
    # passait pour une constante de texte (faux positif vécu sur waves).
    visit_ClassDef = visit_FunctionDef

    def visit_Call(self, node: ast.Call):
        name = _call_name(node)
        if name in _TRANSLATORS:
            return   # T(...) : traduit par construction
        check_pos = name in _TEXT_CALLS
        for i, a in enumerate(node.args):
            if check_pos and not (name == "st_write" and i == 0):
                self._scan(a)
            else:
                self.visit(a)
        for kw in node.keywords:
            if kw.arg in _TEXT_KWARGS or (check_pos and kw.arg not in _SKIP_KWARGS):
                self._scan(kw.value)
            elif kw.arg in _SKIP_KWARGS:
                continue
            else:
                self.visit(kw.value)

    def _scan(self, node: ast.AST) -> None:
        """Une valeur projetée : chaîne nue ? constante nue ? feuille ?"""
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if _is_text(node.value):
                self.bare.append((node.lineno, node.value[:60]))
        elif isinstance(node, ast.JoinedStr):
            self.bare.append((node.lineno, "f-string à examiner"))
        elif isinstance(node, (ast.Tuple, ast.List)):
            for e in node.elts:
                self._scan(e)
        elif isinstance(node, ast.Name) and node.id in self.const_str:
            val = self.const_str[node.id]
            if isinstance(val, ast.Dict):
                self.visit(val)
            else:
                self._scan_const(node.id, val)
        elif isinstance(node, ast.Call):
            self.visit(node)
        elif isinstance(node, ast.Dict):
            self.visit(node)
        else:
            self.generic_visit(node)

    def _scan_const(self, name: str, val: ast.AST) -> None:
        if isinstance(val, ast.Constant) and isinstance(val.value, str):
            if _is_text(val.value):
                self.bare.append((val.lineno, f"{name} = {val.value[:50]!r}"))
        elif isinstance(val, (ast.Tuple, ast.List)):
            for e in val.elts:
                if isinstance(e, ast.Dict):
                    self.visit(e)
                else:
                    self._scan_const(name, e)
        elif isinstance(val, ast.BinOp):
            self.bare.append((val.lineno, f"{name} = concaténation à examiner"))


def _flatten(node: ast.AST) -> str:
    """Le texte d'une valeur de feuille (str, tuple de fragments…)."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, (ast.Tuple, ast.List)):
        return "".join(_flatten(e) for e in node.elts)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return _flatten(node.left) + _flatten(node.right)
    return ""


def inventory(module: str) -> tuple[list[str], list[str]]:
    """(littéraux nus, feuilles sans fr) — lignes lisibles."""
    bare, missing = [], []
    for path in _py_files(module):
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
        inv = _Inventory(path)
        inv.visit(tree)
        rel = path.relative_to(_MODULES_DIR).as_posix()
        src_lines = source.splitlines()
        for line, s in inv.bare:
            # Donnée citée verbatim (marqueur ``i18n: verbatim`` sur la ligne
            # ou celle du dessus) : assumée, jamais comptée.
            context = " ".join(src_lines[max(line - 2, 0):line])
            if "i18n: verbatim" in context:
                continue
            bare.append(f"{rel}:{line}: {s}")
        for line, leaf in inv.leaves:
            for lang in LANGS:
                if leaf.get(lang) is None:
                    missing.append(f"{rel}:{line}: sans {lang} — {leaf.get('en', '')[:50]!r}")
    return bare, missing


# ── Parité, mots, dérive ────────────────────────────────────────────────────

def _leaves(path: Path, source: str | None = None) -> list[tuple[int, dict]]:
    tree = ast.parse(source if source is not None else path.read_text(encoding="utf-8"))
    inv = _Inventory(path)
    inv.visit(tree)
    return inv.leaves


def _whitelist() -> set[str]:
    if not _WHITELIST.exists():
        return set()
    return {l.strip() for l in _WHITELIST.read_text(encoding="utf-8").splitlines()
            if l.strip() and not l.startswith("#")}


_SCREENS_FREEZE = _REPO / "modules" / "shared-blocks" / "static" / "data" / "screens.json"


def _ui_norm(t: str) -> str:
    return "".join(c for c in t.lower().replace("\u00a0", " ") if c.isalnum() or c == " ").strip()


@lru_cache(maxsize=1)
def _ui_vocabulary() -> dict[str, tuple[str, str]]:
    """{forme normalisée → (id.role.lang, libellé exact)} des intitulés de
    l'application (gel sumvadis, DD-113) — titres et actions seulement."""
    if not _SCREENS_FREEZE.exists():
        return {}
    data = json.loads(_SCREENS_FREEZE.read_text(encoding="utf-8"))["screens"]
    out = {}
    for sid, roles in data.items():
        for role in ("title", "action"):
            for lang, text in roles.get(role, {}).items():
                if lang in LANGS and len(_ui_norm(text)) >= 8:
                    out.setdefault(_ui_norm(text), (f"{sid}.{role}.{lang}", text))
    return out


def ui_drift(module: str) -> list[str]:
    """Les feuilles qui RECOPIENT un intitulé de l'application au lieu de le
    citer par ``screen()`` — à un caractère de ponctuation ou de casse près.
    Avertissement, pas erreur : un titre de diapo peut légitimement
    ressembler au titre de l'écran (règle de partage DD-113)."""
    vocab = _ui_vocabulary()
    if not vocab:
        return []
    out = []
    for path in _py_files(module):
        rel = path.relative_to(_MODULES_DIR).as_posix()
        for line, leaf in _leaves(path):
            for lang, text in leaf.items():
                if not isinstance(text, str):
                    continue
                hit = vocab.get(_ui_norm(text))
                if hit and hit[0].endswith("." + lang):
                    same = " (identique)" if text == hit[1] else f" ≠ {hit[1]!r}"
                    out.append(f"{rel}:{line}: {lang} recopie {hit[0]}{same} — passer par screen() ?")
    return out


def parity(module: str) -> list[str]:
    wl = _whitelist()
    out = []
    for path in _py_files(module):
        rel = path.relative_to(_MODULES_DIR).as_posix()
        for line, leaf in _leaves(path):
            en = leaf.get("en", "")
            for lang in LANGS:
                if lang == "en":
                    continue
                v = leaf.get(lang)
                if v is None or (not v.strip() and en.strip() not in wl):
                    # Une chaîne vide n'est admise que pour une feuille en
                    # liste blanche (suffixe de gabarit sans équivalent FR).
                    out.append(f"{rel}:{line}: sans {lang} — {en[:50]!r}")
                elif v.strip() == en.strip() and en.strip() not in wl:
                    out.append(f"{rel}:{line}: {lang} identique à en — {en[:50]!r}")
    return out


def words(module: str) -> list[str]:
    out = []
    for path in _py_files(module):
        rel = path.relative_to(_MODULES_DIR).as_posix()
        for line, leaf in _leaves(path):
            en, fr = leaf.get("en", ""), leaf.get("fr", "")
            ne, nf = len(en.split()), len(fr.split())
            if en and fr and ne <= 8 and nf > 8:
                out.append(f"{rel}:{line}: fr {nf} mots (en {ne}) — {fr[:60]!r}")
    return out


def drift(module: str, ref: str) -> list[str]:
    out = []
    for path in _py_files(module):
        rel_repo = path.relative_to(_REPO).as_posix()
        r = subprocess.run(["git", "show", f"{ref}:{rel_repo}"], cwd=_REPO,
                           capture_output=True, text=True)
        if r.returncode != 0:
            continue
        old = {leaf.get("fr", ""): leaf.get("en", "")
               for _l, leaf in _leaves(path, r.stdout) if leaf.get("fr")}
        for line, leaf in _leaves(path):
            fr, en = leaf.get("fr", ""), leaf.get("en", "")
            if fr and fr in old and old[fr] != en:
                out.append(f"{path.relative_to(_MODULES_DIR).as_posix()}:{line}: "
                           f"en modifié, fr inchangé — {fr[:50]!r}")
    return out


# ── Commandes ───────────────────────────────────────────────────────────────

def cmd_baseline(modules: list[str]) -> int:
    _BASELINE_DIR.mkdir(parents=True, exist_ok=True)
    for m in modules:
        snap = snapshot(m, "en")
        (_BASELINE_DIR / f"{m}.json").write_text(
            json.dumps(snap, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  ✓ {m}: {len(snap['markers'])} marqueurs, {len(snap['toc'])} entrées TOC, "
              f"{len(snap['media'])} médias — baseline écrite")
    return 0


def cmd_regress(modules: list[str]) -> tuple[int, int]:
    failed = 0
    for m in modules:
        ref_path = _BASELINE_DIR / f"{m}.json"
        if not ref_path.exists():
            print(f"  {_YELLOW}?{_OFF} {m}: pas de baseline — `--baseline {m}` d'abord")
            continue
        ref = json.loads(ref_path.read_text(encoding="utf-8"))
        try:
            cur = snapshot(m, "en")
        except RuntimeError as e:
            print(f"  {_RED}!{_OFF} {e}")
            failed += 1
            continue
        diffs = _diff_snapshots(ref, cur)
        if diffs:
            failed += 1
            print(f"  {_RED}!{_OFF} {m}: l'export EN diverge de la baseline")
            for d in diffs[:12]:
                print(f"      {d}")
        else:
            print(f"  {_GREEN}✓{_OFF} {m}: export EN identique à la baseline")
    return failed, len(modules)


def cmd_inventory(modules: list[str], verbose: bool) -> tuple[int, int]:
    tb = tm = 0
    for m in modules:
        bare, missing = inventory(m)
        tb += len(bare)
        tm += len(missing)
        print(f"  {m}: {len(bare)} littéral(aux) nu(s), {len(missing)} feuille(s) incomplète(s)")
        if verbose:
            for b in bare:
                print(f"      nu   {b}")
            for x in missing:
                print(f"      sans {x}")
    return tb, tm


def cmd_parity(modules: list[str], with_export: bool, verbose: bool) -> int:
    total = 0
    for m in modules:
        probs = parity(m)
        if with_export:
            try:
                en, fr = snapshot(m, "en"), snapshot(m, "fr")
                if len(en["markers"]) != len(fr["markers"]):
                    probs.append(f"export : {len(en['markers'])} marqueurs en, "
                                 f"{len(fr['markers'])} fr")
                # Les médias par langue (clips, captures, vidéos) diffèrent
                # légitimement : c'est le NOMBRE qui doit être égal.
                if len(en["media"]) != len(fr["media"]):
                    probs.append(f"export : {len(en['media'])} médias en, "
                                 f"{len(fr['media'])} fr")
            except RuntimeError as e:
                probs.append(str(e))
        total += len(probs)
        state = f"{_GREEN}✓{_OFF}" if not probs else f"{_RED}!{_OFF}"
        drifts = ui_drift(m)
        print(f"  {state} {m}: {len(probs)} problème(s) de parité"
              + (f" · {len(drifts)} recopie(s) d'intitulé d'application (avertissement)" if drifts else ""))
        if verbose:
            for p in probs:
                print(f"      {p}")
            for d in drifts:
                print(f"      ~ {d}")
    return total


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("modules", nargs="*")
    ap.add_argument("--baseline", action="store_true")
    ap.add_argument("--regress", action="store_true")
    ap.add_argument("--inventory", action="store_true")
    ap.add_argument("--parity", action="store_true")
    ap.add_argument("--with-export", action="store_true",
                    help="parité : comparer aussi les exports en et fr")
    ap.add_argument("--words", action="store_true")
    ap.add_argument("--drift", metavar="REF")
    ap.add_argument("--report", action="store_true",
                    help="inventaire + régression, ligne de synthèse pour check_all")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()
    modules = _modules(args.modules)
    rc = 0

    if args.baseline:
        return cmd_baseline(modules)
    if args.regress:
        failed, _n = cmd_regress(modules)
        rc |= 1 if failed else 0
    if args.inventory:
        cmd_inventory(modules, args.verbose)
    if args.parity:
        n = cmd_parity(modules, args.with_export, args.verbose)
        rc |= 1 if any(m not in I18N_PENDING for m in modules) and n else 0
    if args.words:
        for m in modules:
            for w in words(m):
                print(f"  ~ {w}")
    if args.drift:
        for m in modules:
            for d in drift(m, args.drift):
                print(f"  ~ {d}")
    if args.report:
        tb, tm = cmd_inventory(modules, False)
        failed, _n = cmd_regress(modules)
        # Les modules encore en attente ne rendent pas la porte rouge.
        strict = [m for m in modules if m not in I18N_PENDING]
        sb = sm = 0
        for m in strict:
            b, mm = inventory(m)
            sb += len(b)
            sm += len(mm)
        print(f"\n**{tb} littéral(aux) nu(s) · {tm} feuille(s) sans fr · "
              f"{failed} régression(s) EN · {sb + sm} exigé(s) manquant(s)**")
        rc |= 1 if failed or sb or sm else 0
    return rc


if __name__ == "__main__":
    sys.exit(main())
