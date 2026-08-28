"""L'assemblage d'un lot (recette R7) — verdicts des lentilles → lot final.

Lit ``<lot>.fr.json`` et les verdicts ``<lot>.v3a.json`` / ``.v3b.json`` /
``.v3c.json`` (chacun : liste de ``{id, verdict, issue, fix}``). Applique
les FIX uniques ; quand plusieurs lentilles proposent des ``fix`` DIFFÉRENTS
pour une même entrée, la priorité est **faits (v3b) > terminologie (v3a) >
amphi (v3c)** et le conflit est listé — l'assembleur humain ou agent tranche
si nécessaire. Écrit ``<lot>.final.json`` et imprime le journal.

Usage::

    uv run python _project/tools/i18n_assemble.py _project/i18n/postair_opening/lot-1
    uv run python _project/tools/i18n_lots.py --inject _project/i18n/postair_opening/lot-1.final.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

_PRIORITY = ("v3b", "v3a", "v3c")
_NBSP = "\u00a0"


def frtypo(text: str) -> str:
    """Les insécables du français, posées mécaniquement (les lentilles les oublient)."""
    import re
    text = re.sub(r"(?<=\S) ([:;?!%»])", _NBSP + r"\1", text)
    text = re.sub(r"(?<=\S)([:;?!%»])", lambda m: m.group(1) if m.group(1) in ";" and False else m.group(0), text)
    text = re.sub(r"« (?=\S)", "«" + _NBSP, text)
    # « 92% » → « 92 % »
    text = re.sub(r"(?<=\d)%", _NBSP + "%", text)
    return text


def _typo_value(v):
    if isinstance(v, str):
        return frtypo(v)
    if isinstance(v, list):
        return [{k: (frtypo(x) if isinstance(x, str) else x) for k, x in f.items()} for f in v]
    return v


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 1
    stem = Path(sys.argv[1])
    lot = json.loads(Path(f"{stem}.fr.json").read_text(encoding="utf-8"))
    verdicts: dict[str, dict[str, dict]] = {}
    for lens in _PRIORITY:
        p = Path(f"{stem}.{lens}.json")
        if not p.exists():
            print(f"  ? {p.name} absent — lentille sautée")
            continue
        for v in json.loads(p.read_text(encoding="utf-8")):
            verdicts.setdefault(v["id"], {})[lens] = v
    applied = conflicts = 0
    for e in lot:
        vs = verdicts.get(e["id"], {})
        fixes = [(lens, v["fix"]) for lens, v in vs.items()
                 if v.get("verdict") == "FIX" and v.get("fix") not in (None, [])]
        if not fixes:
            continue
        distinct = {json.dumps(f, ensure_ascii=False, sort_keys=True) for _l, f in fixes}
        chosen_lens, chosen = next((l, f) for l, f in fixes)   # ordre = priorité
        if len(distinct) > 1:
            conflicts += 1
            print(f"  ! conflit {e['id']} — retenu {chosen_lens}")
            for lens, f in fixes:
                print(f"      {lens}: {vs[lens].get('issue', '')[:80]} → {json.dumps(f, ensure_ascii=False)[:90]}")
        else:
            print(f"  ~ {e['id']} [{'+'.join(l for l, _f in fixes)}] {vs[chosen_lens].get('issue', '')[:90]}")
        e["fr_v1"] = e["fr"]
        e["fr"] = chosen
        applied += 1
    for e in lot:
        e["fr"] = _typo_value(e["fr"])
    Path(f"{stem}.final.json").write_text(json.dumps(lot, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n{len(lot)} entrées · {applied} correction(s) appliquée(s) · {conflicts} conflit(s) → {stem}.final.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
