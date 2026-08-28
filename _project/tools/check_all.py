"""LA porte d'avant-répétition — tous les contrôles du dépôt, une commande.

Réunit les filets existants et les règles vérifiables de la guideline
(consolidation P3, NG 2026-08-23). Chaque porte a une raison d'être née d'un
incident réel ; aucune n'est décorative.

Usage::

    uv run python _project/tools/check_all.py            # tout (exports compris, ~minutes)
    uv run python _project/tools/check_all.py --fast     # sans la porte des exports

Portes, dans l'ordre :

1. **noms** — aucun chiffre dans un nom de bloc (règle du book : l'ordre
   change tout le temps) ; aucun bloc orphelin (un bloc exclu se COMMENTE
   dans le book, il y reste donc cité — un bloc jamais cité est un oubli).
2. **blocs** — ``check_blocks_build.py`` : build() réel de chaque bloc
   (filet R14 et consorts).
3. **médias** — ``sync_media.py --check`` : 0 média manquant.
4. **gel studio** — ``check_shared_freeze.py`` (dégrade proprement sans
   configuration de machine).
5. **gel captures** — ``build_survey_captures.py --work-order`` : 0 écart de
   gel, 0 adresse non-/v/ ; les « attendues manquantes » de la matrice de
   base sont un avertissement (dette connue : la console admin sans ``de``).
6. **gel débats** — ``build_debates_content.py --work-order`` : 0 sans
   référence imprimable, 0 problème de gel .bib (les compteurs du milieu
   sont une dette connue → avertissement). Sauté sans configuration hub.
7. **exports** — ``check_export_media.py`` : src présents + marque DD-35
   (sauté avec ``--fast`` : c'est la porte lente, elle régénère les exports).
8. **i18n** — ``check_i18n.py`` : l'anglais projeté n'a pas bougé
   (``--regress``, sauté avec ``--fast``) et les modules sortis de
   ``I18N_PENDING`` n'ont ni littéral nu ni feuille sans ``fr`` ; les modules
   encore en attente ne donnent qu'un avertissement (plan-i18n, 2026-08-28).

Ne modifie rien. Code de sortie 0 = tout est vert ; 1 = au moins une porte
rouge. Les avertissements n'affectent pas le code de sortie.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

_TOOLS = Path(__file__).parent
_REPO = _TOOLS.parent.parent
_MODULES = _REPO / "modules"

_GREEN, _RED, _YELLOW, _DIM, _OFF = "\033[32m", "\033[31m", "\033[33m", "\033[2m", "\033[0m"

results: list[tuple[str, str, str]] = []   # (porte, état, détail)


def _record(gate: str, ok: bool, detail: str = "", warn: bool = False) -> None:
    state = "WARN" if warn else ("OK" if ok else "FAIL")
    colour = _YELLOW if warn else (_GREEN if ok else _RED)
    print(f"{colour}{state:4s}{_OFF} {gate}" + (f" — {detail}" if detail else ""))
    results.append((gate, state, detail))


def _run(cmd: list[str]) -> tuple[int, str]:
    proc = subprocess.run(cmd, cwd=_REPO, capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


# ── 1. noms ──────────────────────────────────────────────────────────────────

def gate_names() -> None:
    numbered, orphans = [], []
    for module in sorted(_MODULES.iterdir()):
        blocks_dir = module / "blocks"
        book = module / "book.py"
        if not blocks_dir.is_dir() or not book.exists():
            continue
        book_text = book.read_text(encoding="utf-8")
        for p in sorted(blocks_dir.glob("bck_*.py")):
            if re.search(r"\d", p.stem):
                numbered.append(f"{module.name}/{p.name}")
            if p.stem not in book_text:
                orphans.append(f"{module.name}/{p.name}")
    ok = not numbered and not orphans
    detail = "; ".join(
        (["chiffres dans un nom : " + ", ".join(numbered)] if numbered else [])
        + (["bloc jamais cité par son book : " + ", ".join(orphans)] if orphans else []))
    _record("noms de blocs (pas de chiffre, pas d'orphelin)", ok, detail)


# ── 2-4. les filets existants, tels quels ────────────────────────────────────

def gate_blocks() -> None:
    code, out = _run([sys.executable, str(_TOOLS / "check_blocks_build.py")])
    fails = [line.strip() for line in out.splitlines() if "FAIL" in line]
    _record("build de chaque bloc (check_blocks_build)", code == 0,
            fails[0] if fails else "")


def gate_media() -> None:
    code, out = _run([sys.executable, str(_TOOLS / "sync_media.py"), "--check"])
    missing = [line.strip() for line in out.splitlines() if "manque " in line]
    _record("médias matérialisés (sync_media --check)", code == 0,
            f"{len(missing)} manquant(s)" if missing else "")


def gate_shared_freeze() -> None:
    code, out = _run([sys.executable, str(_TOOLS / "check_shared_freeze.py")])
    degraded = "non comparés" in out
    _record("gel du studio (check_shared_freeze)", code == 0,
            "config machine absente — contrôle partiel" if degraded else "",
            warn=(code == 0 and degraded))


# ── 5. gel des captures ─────────────────────────────────────────────────────

def gate_captures() -> None:
    if not (_TOOLS / "survey-captures.config.local.json").exists():
        _record("gel des captures (work-order)", True,
                "config machine absente — sauté", warn=True)
        return
    code, out = _run([sys.executable, str(_TOOLS / "build_survey_captures.py"),
                      "--work-order"])
    m = re.search(r"\*\*(\d+) écart\(s\) de gel · (\d+) attendue\(s\) "
                  r"manquante\(s\) · (\d+) adresse\(s\) non-/v/", out)
    if code != 0 or not m:
        _record("gel des captures (work-order)", False, "sortie illisible")
        return
    stale, missing, non_v = map(int, m.groups())
    if stale or non_v:
        _record("gel des captures (work-order)", False,
                f"{stale} écart(s) de gel, {non_v} non-/v/ — regeler puis sync")
    else:
        _record("gel des captures (work-order)", True,
                f"{missing} attendue(s) manquante(s) au registre (dette connue)"
                if missing else "", warn=bool(missing))


# ── 6. gel des débats ───────────────────────────────────────────────────────

def gate_debates() -> None:
    if not (_TOOLS / "debates-hub.config.local.json").exists():
        _record("gel des débats (work-order)", True,
                "config hub absente — sauté", warn=True)
        return
    code, out = _run([sys.executable, str(_TOOLS / "build_debates_content.py"),
                      "--work-order"])
    m = re.search(r"\*\*(\d+) sans référence imprimable · (\d+) sans traduction "
                  r"française · (\d+) citations sans clé BibTeX[^·]*· "
                  r"(\d+) problème\(s\) de gel \.bib", out)
    if code != 0 or not m:
        _record("gel des débats (work-order)", False, "sortie illisible")
        return
    no_ref, no_fr, no_key, bib = map(int, m.groups())
    if no_ref or bib:
        _record("gel des débats (work-order)", False,
                f"{no_ref} sans référence imprimable, {bib} problème(s) .bib")
    else:
        debt = no_fr + no_key
        _record("gel des débats (work-order)", True,
                f"dette connue : {no_fr} sans fr, {no_key} sans clé promue"
                if debt else "", warn=bool(debt))


# ── 6bis. gel de l'instrument (deck à main levée) ───────────────────────────

def gate_handsup() -> None:
    if not (_TOOLS / "debates-hub.config.local.json").exists():
        _record("gel de l'instrument (handsup work-order)", True,
                "config hub absente — sauté", warn=True)
        return
    code, out = _run([sys.executable, str(_TOOLS / "build_handsup_content.py"),
                      "--work-order"])
    m = re.search(r"\*\*(\d+) divergence\(s\) de gel · (\d+) synthèse\(s\) "
                  r"en attente amont", out)
    if code != 0 or not m:
        _record("gel de l'instrument (handsup work-order)", False, "sortie illisible")
        return
    diverged, missing = map(int, m.groups())
    if diverged:
        # ROUGE, pas warn : l'exigence du deck de secours est « aucune
        # divergence possible » (plan v2) — le remède est un regel.
        _record("gel de l'instrument (handsup work-order)", False,
                "le gel diverge du questionnaire du hub — régénérer")
    else:
        _record("gel de l'instrument (handsup work-order)", True,
                f"{missing} synthèse(s) en attente amont (ticket v1.10.0)"
                if missing else "", warn=bool(missing))


# ── 7. exports ──────────────────────────────────────────────────────────────

def gate_exports() -> None:
    code, out = _run([sys.executable, str(_TOOLS / "check_export_media.py")])
    last = next((line.strip() for line in reversed(out.splitlines()) if line.strip()), "")
    _record("exports (src présents + marque DD-35)", code == 0,
            "" if code == 0 else last)


# ── 8. i18n ─────────────────────────────────────────────────────────────────

def gate_i18n(fast: bool) -> None:
    cmd = [sys.executable, str(_TOOLS / "check_i18n.py"),
           "--inventory" if fast else "--report"]
    code, out = _run(cmd)
    if fast:
        # Inventaire seul : jamais rouge, il compte ce qui reste à migrer.
        counts = re.findall(r"(\d+) littéral\(aux\) nu\(s\), (\d+) feuille", out)
        bare = sum(int(a) for a, _b in counts)
        missing = sum(int(b) for _a, b in counts)
        _record("i18n (inventaire ; régression sautée --fast)", True,
                f"{bare} littéral(aux) nu(s), {missing} feuille(s) sans fr",
                warn=bool(bare or missing))
        return
    m = re.search(r"\*\*(\d+) littéral\(aux\) nu\(s\) · (\d+) feuille\(s\) sans fr · "
                  r"(\d+) régression\(s\) EN · (\d+) exigé\(s\) manquant\(s\)\*\*", out)
    if not m:
        _record("i18n (régression EN + parité)", False, "sortie illisible")
        return
    bare, missing, regress, required = map(int, m.groups())
    if regress or required:
        _record("i18n (régression EN + parité)", False,
                f"{regress} régression(s) EN, {required} exigé(s) manquant(s)")
    else:
        _record("i18n (régression EN + parité)", True,
                f"{bare} littéral(aux) nu(s), {missing} feuille(s) sans fr (modules en attente)"
                if bare or missing else "", warn=bool(bare or missing))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--fast", action="store_true",
                    help="sauter la porte des exports (la plus lente)")
    args = ap.parse_args()

    gate_names()
    gate_blocks()
    gate_media()
    gate_shared_freeze()
    gate_captures()
    gate_debates()
    gate_handsup()
    if args.fast:
        _record("exports (src présents + marque DD-35)", True,
                "sauté (--fast)", warn=True)
    else:
        gate_exports()
    gate_i18n(args.fast)

    fails = [g for g, s, _d in results if s == "FAIL"]
    warns = [g for g, s, _d in results if s == "WARN"]
    print()
    if fails:
        print(f"{_RED}ROUGE{_OFF} — {len(fails)} porte(s) : {', '.join(fails)}")
        return 1
    note = f" ({len(warns)} avertissement(s))" if warns else ""
    print(f"{_GREEN}VERT{_OFF} — toutes les portes passent{note}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
