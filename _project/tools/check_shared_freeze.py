#!/usr/bin/env python3
"""Le gel du studio mascoties est-il encore fidèle à sa source ?

``modules/shared-blocks/static/_SHARED/mascots/`` est une **copie gelée** de la
source de vérité du studio (``mascoties/shared/``) : trois manifestes JSON, les 36
webp des mascottes, quelques clips. C'est un cinquième tuyau de l'écosystème, et le
seul qui n'ait aucun outil : la copie a été faite à la main, donc rien ne dit qu'elle
soit encore à jour.

Ce script ne copie rien et ne corrige rien — il **constate**. Trois familles :

  · **manifestes** (``i18n.json``, ``cast_final.json``, ``profiles_fr.json``) :
    doivent être byte-identiques. Une divergence est un défaut : le deck afficherait
    d'autres noms que l'application.
  · **webp** : la comparaison d'octets ne suffit pas et serait trompeuse — le studio
    re-signe ses images (C2PA), ce qui change les octets sans changer l'image. Ce qui
    compte est la **signature** : une image d'IA servie sans divulgation lisible par
    machine est le défaut trouvé au CDN le 2026-08-01. On rapporte donc les deux :
    l'écart d'octets, et l'état de signature de chaque côté.
  · **clips** : on signale ceux dont aucune source n'est retrouvée côté studio —
    un média orphelin ne peut être ni re-généré ni ré-autorisé.

Usage (depuis la racine du dépôt) :

    uv run python _project/tools/check_shared_freeze.py
    uv run python _project/tools/check_shared_freeze.py --quiet   # code de retour seul

Sortie 0 = gel fidèle · 1 = divergence à traiter. Le chemin du studio se lit dans
``debates-hub.config.local.json`` (clé ``studio``) ; sans elle, seul le contrôle de
signature de la copie est exécuté.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
_REPO = _TOOLS.parent.parent
FREEZE = _REPO / "modules" / "shared-blocks" / "static" / "_SHARED" / "mascots"

#: Manifeste gelé -> son chemin relatif dans ``mascoties/shared/``.
MANIFESTS = {
    "i18n.json": "cartes/i18n.json",
    "cast_final.json": "cast/cast_final.json",
    "profiles_fr.json": "cast/profiles_fr.json",
}
WEBP_SRC = "cartes/web"
#: Marqueur d'un conteneur JUMBF — l'enveloppe d'une assertion C2PA.
C2PA_MARK = b"jumb"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def signed(p: Path) -> bool:
    return C2PA_MARK in p.read_bytes()


def studio_root() -> Path | None:
    cfg = _TOOLS / "debates-hub.config.local.json"
    if not cfg.is_file():
        return None
    raw = json.loads(cfg.read_text(encoding="utf-8")).get("studio")
    if not raw:
        return None
    p = Path(raw)
    return p if p.is_dir() else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()
    say = (lambda *a: None) if args.quiet else print

    if not FREEZE.is_dir():
        print(f"REFUS: gel introuvable — {FREEZE}", file=sys.stderr)
        return 2
    studio = studio_root()
    defauts: list[str] = []

    # --- manifestes -------------------------------------------------------
    if studio:
        for name, rel in MANIFESTS.items():
            a, b = FREEZE / name, studio / "shared" / rel
            if not a.is_file():
                defauts.append(f"manifeste absent du gel: {name}")
            elif not b.is_file():
                defauts.append(f"source studio introuvable: shared/{rel}")
            elif sha(a) != sha(b):
                defauts.append(f"manifeste DIVERGENT: {name} != shared/{rel}")
            else:
                say(f"OK  {name} identique à shared/{rel}")
    else:
        say("(clé `studio` absente de la configuration — manifestes non comparés)")

    # --- webp -------------------------------------------------------------
    webp = sorted((FREEZE / "web").glob("*.webp")) if (FREEZE / "web").is_dir() else []
    nus = [p for p in webp if not signed(p)]
    say(f"\nwebp du gel : {len(webp)} — signés C2PA : {len(webp) - len(nus)}/{len(webp)}")
    if studio and webp:
        src = studio / "shared" / WEBP_SRC
        src_signes = sum(1 for p in src.glob("*.webp") if signed(p))
        ecarts = sum(1 for p in webp
                     if (src / p.name).is_file() and sha(p) != sha(src / p.name))
        say(f"webp du studio : signés C2PA {src_signes}/{len(list(src.glob('*.webp')))}"
            f" — octets différents du gel : {ecarts}")
        if nus and src_signes:
            defauts.append(
                f"{len(nus)} webp du gel sans signature C2PA alors que le studio en "
                f"signe {src_signes} — la copie est antérieure au re-signage")
    elif nus:
        defauts.append(f"{len(nus)} webp du gel sans signature C2PA")

    # --- clips ------------------------------------------------------------
    vids = sorted((FREEZE / "videos").glob("*")) if (FREEZE / "videos").is_dir() else []
    if studio and vids:
        noms = {p.name for p in (studio / "shared").rglob("*.mp4")}
        orphelins = [p.name for p in vids if p.name not in noms]
        say(f"\nclips du gel : {len(vids)} — sans source retrouvée au studio : "
            f"{len(orphelins)}")
        if orphelins:
            defauts.append("clips orphelins (aucune source au studio): "
                           + ", ".join(sorted(orphelins)))

    if defauts:
        print("\nDIVERGENCES :", file=sys.stderr)
        for d in defauts:
            print(f"  · {d}", file=sys.stderr)
        return 1
    say("\nOK: le gel est fidèle à la source du studio.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
