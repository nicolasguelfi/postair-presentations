#!/usr/bin/env python3
"""Tests de la règle ``curated`` de build_debates_content (2026-08-30).

Deux volets :

1. **unitaire, sans le hub** : ``curated_match`` apparie par égalité stricte
   d'abord, par inclusion ensuite (fragment ⊂ phrase entière, dans n'importe
   quelle langue de l'éditorial), et refuse les fragments trop courts ;
2. **intégration, avec le hub** (sauté si la config locale manque) : les cinq
   originaux français du corpus (Saint-Simon, Hugo, Pasteur, Saint-Exupéry,
   Duhamel) doivent sortir appariés à l'éditorial — ``curated`` vrai, ``fr``
   non nul, ``en`` en anglais — quel que soit le régime d'appariement.

Usage : ``uv run python _project/tools/test_build_debates_content.py``
(exit 1 au premier échec).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import build_debates_content as b  # noqa: E402

FRENCH_ORIGINALS = ("saint-simon", "hugo", "pasteur", "saint-exupery", "duhamel")


def test_exact_wins() -> None:
    q1 = {"text": {"en": "A", "fr": "Souvenez-vous que dans les champs de l'observation le hasard ne favorise que les esprits préparés."}}
    q2 = {"text": {"en": "B", "fr": "dans les champs de l'observation le hasard ne favorise que les esprits préparés."}}
    cands = [(t, q) for q in (q1, q2) for t in q["text"].values()]
    m, how = b.curated_match("dans les champs de l'observation le hasard ne favorise que les esprits préparés.", cands)
    assert (m, how) == (q2, "exact"), (m, how)


def test_inclusion_fragment_in_sentence() -> None:
    q = {"text": {"en": "Remember that in the fields of observation chance favors only the prepared mind.",
                  "fr": "Souvenez-vous que dans les champs de l'observation le hasard ne favorise que les esprits préparés."}}
    cands = [(t, q) for t in q["text"].values()]
    m, how = b.curated_match("dans les champs de l'observation le hasard ne favorise que les esprits préparés.", cands)
    assert (m, how) == (q, "inclusion"), (m, how)
    # Dans l'autre sens (le registre porte la phrase entière + une incise, l'éditorial
    # la phrase nue) : apparié aussi — par « exact » quand les 60 premiers caractères
    # normalisés coïncident (clé-préfixe de ``_norm``, comportement historique), par
    # inclusion sinon. Ce qui compte : la citation est retrouvée.
    m, how = b.curated_match("Souvenez-vous que dans les champs de l'observation le hasard ne favorise que les esprits préparés, dit-il.", cands)
    assert m == q and how in ("exact", "inclusion"), (m, how)
    # un membre du MILIEU de phrase (≥ 40 caractères utiles) : seule l'inclusion le retrouve
    m, how = b.curated_match("champs de l'observation le hasard ne favorise que les esprits préparés", cands)
    assert (m, how) == (q, "inclusion"), (m, how)


def test_short_fragment_never_matches_by_inclusion() -> None:
    q = {"text": {"en": "Chance favors only the prepared mind, and that is all.", "fr": "Le hasard ne favorise que les esprits préparés, et c'est tout."}}
    cands = [(t, q) for t in q["text"].values()]
    m, how = b.curated_match("esprits préparés", cands)
    assert (m, how) == (None, None), (m, how)


def test_no_match() -> None:
    q = {"text": {"en": "Something else entirely about steam engines and their boilers.", "fr": "Tout autre chose."}}
    m, how = b.curated_match("dans les champs de l'observation le hasard ne favorise que les esprits préparés.", [(t, q) for t in q["text"].values()])
    assert (m, how) == (None, None), (m, how)


def test_french_originals_with_hub() -> None:
    try:
        hub = b.load_config()["hub"]
    except Exception:
        print("  (hub non configuré : test d'intégration sauté)")
        return
    data = b.build(b.Hub(hub))
    seen = {}
    for pole in data["poles"]:
        for f in pole["figures"]:
            if f["id"] in FRENCH_ORIGINALS:
                seen[f["id"]] = f["quote"]
    assert seen, "aucun original français projeté ?"
    for fid, q in sorted(seen.items()):
        assert q["curated"], f"{fid}: non apparié à l'éditorial ({q['en'][:50]!r})"
        assert q.get("fr"), f"{fid}: fr vide"
        assert not q["en"].startswith(("dans ", "Souvenez", "La ", "Le ", "Enfin")), f"{fid}: en = du français {q['en'][:40]!r}"
        print(f"  {fid}: apparié ({q.get('curated_by')}) — en={q['en'][:40]!r}")


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            print(name); fn()
    print("OK")
