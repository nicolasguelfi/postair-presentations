"""Contrôle de FORME d'un lot traduit (avant les relectures V2/V3).

Ne juge pas le sens — c'est le travail des agents. Vérifie ce qu'une machine
vérifie mieux qu'un relecteur : ``fr`` présent partout, motif des fragments
identique à l'EN, chiffres/années/pourcentages/sigles conservés, placeholders
``{…}`` conservés, R3 (≤ 8 mots FR quand l'EN en a ≤ 8), longueur ≤ +25 %
sur les textes courts, espaces insécables devant ``: ; ? ! %`` et dans « »,
et l'usage du glossaire pour les termes canoniques présents dans l'EN.

Usage::

    uv run python _project/tools/i18n_lot_check.py _project/i18n/postair_opening/lot-1.fr.json
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_REPO = Path(__file__).parent.parent.parent
_GLOSSARY = _REPO / "modules" / "shared-blocks" / "static" / "data" / "glossary.json"
_NUM = re.compile(r"\d+(?:[.,]\d+)?")
_PLACEHOLDER = re.compile(r"\{[a-z_]+\}")


def _flat(kind, v) -> str:
    if kind == "fragments":
        return "".join(f.get("text", f.get("kw", "")) for f in v)
    return v if isinstance(v, str) else ""


def check(lot: list[dict]) -> list[str]:
    terms = json.loads(_GLOSSARY.read_text(encoding="utf-8"))["terms"]
    canon = {v["en"].lower(): v["fr"] for k, v in terms.items()
             if k.startswith(("archetype.", "axis.", "pole.")) and k.endswith(".name")}
    problems = []
    for e in lot:
        i, en, fr = e["id"], e["en"], e.get("fr")
        if fr in (None, "", []):
            problems.append(f"{i}: fr manquant"); continue
        if e["kind"] == "fragments":
            if not isinstance(fr, list) or len(fr) != len(en):
                problems.append(f"{i}: {len(en)} fragments attendus"); continue
            for a, b in zip(en, fr):
                if ("kw" in a) != ("kw" in b):
                    problems.append(f"{i}: motif texte/kw différent"); break
        fe, ff = _flat(e["kind"], en), _flat(e["kind"], fr)
        if not isinstance(ff, str):
            problems.append(f"{i}: fr invalide"); continue
        if not ff.strip():
            continue   # suffixe vide voulu — la parité l'exige en liste blanche
        ne, nf = set(_NUM.findall(fe)), set(_NUM.findall(ff))
        if ne - nf:
            problems.append(f"{i}: nombres perdus {sorted(ne - nf)} — {ff[:50]!r}")
        pe, pf = set(_PLACEHOLDER.findall(fe)), set(_PLACEHOLDER.findall(ff))
        if pe != pf:
            problems.append(f"{i}: placeholders {sorted(pe)} ≠ {sorted(pf)}")
        we, wf = len(fe.split()), len(ff.split())
        if we <= 8 and wf > 8:
            problems.append(f"{i}: R3 — fr {wf} mots pour en {we} : {ff[:60]!r}")
        if we <= 12 and wf > we * 1.25 + 1 and fe != ff:
            problems.append(f"{i}: longueur +{round(100 * (wf / max(we, 1) - 1))} % ({we}→{wf} mots)")
        for m in re.finditer(r"\S [:;?!»]", ff):
            problems.append(f"{i}: espace sécable avant « {m.group()[-1]} » — {ff[max(0, m.start()-15):m.end()+5]!r}")
            break
        if "« " in ff and " " not in ff:
            problems.append(f"{i}: guillemets « » sans insécable")
        if re.search(r"\d %", ff) and not re.search(r"\d %", ff):
            problems.append(f"{i}: espace sécable avant %")
        low = fe.lower()
        for en_term, fr_term in canon.items():
            if re.search(rf"\b{re.escape(en_term)}\b", low) and fr_term.lower() not in ff.lower():
                problems.append(f"{i}: terme canonique « {en_term} » → attendu « {fr_term} » — {ff[:60]!r}")
    return problems


def main() -> int:
    rc = 0
    for arg in sys.argv[1:]:
        lot = json.loads(Path(arg).read_text(encoding="utf-8"))
        probs = check(lot)
        print(f"{arg}: {len(lot)} entrées, {len(probs)} problème(s)")
        for p in probs:
            print(f"  ~ {p}")
        rc |= 1 if any(("fr manquant" in p or "fragments" in p or "motif" in p or "perdus" in p or "placeholders" in p) for p in probs) else 0
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
