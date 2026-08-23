"""Gèle l'instrument POSTAIR pour le deck de secours « à main levée ».

Décision NG 2026-08-23 (plan-postair_handsup v2) : le deck projette les 54
énoncés, les synthèses par pôle et l'échelle de réponse — et n'écrit AUCUNE
de ces chaînes à la main. La vérité est le hub ``ai-social-profiles``
(``questionnaire/questionnaire.json``, cf. ECOSYSTEM.md) ; la copie sumvadis
n'est qu'un sync verbatim. Cet outil extrait les trois langues et gèle
``modules/postair_handsup/static/data/content.json`` — même contrat que le
gel des débats : ne jamais l'éditer à la main, régénérer.

Usage::

    uv run python _project/tools/build_handsup_content.py               # regel
    uv run python _project/tools/build_handsup_content.py --work-order  # constat, n'écrit rien

Chemin du hub : ``debates-hub.config.local.json`` (clé ``hub`` — la config
machine EXISTANTE du gel des débats, aucune nouvelle config).

Le ``--work-order`` compare le gel au hub et imprime une ligne de bilan que
``check_all`` parse : **toute divergence est un ROUGE** (l'exigence du deck
de secours est « aucune divergence possible », pas « divergence signalée ») ;
les synthèses absentes de l'amont sont un avertissement « attente amont »
tant que le questionnaire n'a pas livré son champ ``synthesis`` (v1.10.0).

Structure du gel — pensée pour les gabarits, pas pour la fidélité au schéma
amont : par axe (ordre horaire du radar = champ ``order``), les pôles sont
rangés ``accel``/``decel`` (par ``effect``), chaque énoncé est affecté à son
pôle par sa polarité (+1 = ``pole_right`` de l'instrument), et l'échelle est
pré-découpée pour la slide de vote : ``agree`` en intensité décroissante,
``disagree`` en intensité croissante, ``no_opinion`` à part.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

_TOOLS = Path(__file__).parent
_REPO = _TOOLS.parent.parent
_CONFIG = _TOOLS / "debates-hub.config.local.json"
_FREEZE = _REPO / "modules" / "postair_handsup" / "static" / "data" / "content.json"

_LANGS = ["en", "fr", "de"]
_SCALE_REF = "agreement-0-5"


def _hub() -> Path:
    if not _CONFIG.exists():
        raise SystemExit(
            f"config machine absente : {_CONFIG.name} — copier "
            f"debates-hub.config.example.json et renseigner la clé `hub`.")
    hub = Path(json.loads(_CONFIG.read_text(encoding="utf-8"))["hub"])
    q = hub / "questionnaire" / "questionnaire.json"
    if not q.exists():
        raise SystemExit(f"questionnaire introuvable : {q}")
    return hub


def _warn_if_dirty(hub: Path) -> None:
    """Même politesse que le gel des débats : avertir, ne pas échouer."""
    proc = subprocess.run(
        ["git", "-C", str(hub), "status", "--porcelain", "--", "questionnaire/"],
        capture_output=True, text=True)
    if proc.returncode == 0 and proc.stdout.strip():
        print("⚠ l'arbre du hub est sale sur questionnaire/ — le gel "
              "photographierait un travail en cours.")


def _texts(node: dict) -> dict:
    """Les trois langues d'un champ amont — clé manquante = erreur bruyante."""
    return {lang: node[lang] for lang in _LANGS}


def _build(hub: Path) -> dict:
    src = json.loads((hub / "questionnaire" / "questionnaire.json")
                     .read_text(encoding="utf-8"))
    scale = src["scales"][_SCALE_REF]
    labels = scale["labels"]  # index 0 (Strongly disagree) → 5 (Strongly agree)
    by_level = [{lang: labels[lang][i] for lang in _LANGS} for i in range(6)]

    axes = []
    for ax in sorted(src["axes"], key=lambda a: a["order"]):
        poles = {}
        for side in ("pole_left", "pole_right"):
            pole = ax[side]
            polarity = 1 if side == "pole_right" else -1
            statements = [
                {"id": q["id"], "text": _texts(q["text"])}
                for q in ax["questions"] if q["polarity"] == polarity
            ]
            if len(statements) != 3:
                raise SystemExit(
                    f"axe {ax['code']} : {len(statements)} énoncé(s) vers "
                    f"{side} — l'instrument en promet exactement 3.")
            key = "accel" if pole["effect"] == "accelerator" else "decel"
            poles[key] = {
                "label": _texts(pole),
                # v1.9.x n'a pas encore le champ — null tant que l'amont
                # (session ai-social-profiles) n'a pas livré la v1.10.0.
                "synthesis": _texts(pole["synthesis"]) if "synthesis" in pole else None,
                "statements": statements,
            }
        if set(poles) != {"accel", "decel"}:
            raise SystemExit(f"axe {ax['code']} : pôles accel/decel introuvables")
        axes.append({
            "code": ax["code"], "order": ax["order"],
            "name": _texts(ax["name"]), **poles,
        })

    return {
        "_generated_by": "_project/tools/build_handsup_content.py — ne pas éditer, régénérer",
        "questionnaire_version": src["metadata"]["version"],
        "questionnaire_date": src["metadata"]["date"],
        "languages": _LANGS,
        "scale": {
            # Slide de vote : pour, en intensité DÉCROISSANTE…
            "agree": [by_level[5], by_level[4], by_level[3]],
            # …contre, en intensité CROISSANTE, puis « No opinion » à part.
            "disagree": [by_level[2], by_level[1], by_level[0]],
            "no_opinion": _texts(scale["no_answer"]["label"]),
        },
        "axes": axes,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--work-order", action="store_true",
                    help="constat gel vs hub, n'écrit rien")
    args = ap.parse_args()

    hub = _hub()
    _warn_if_dirty(hub)
    fresh = _build(hub)
    missing = sum(1 for ax in fresh["axes"] for k in ("accel", "decel")
                  if ax[k]["synthesis"] is None)

    if args.work_order:
        if not _FREEZE.exists():
            print("le gel n'existe pas encore — lancer sans --work-order.")
            print(f"**1 divergence(s) de gel · {missing} synthèse(s) en attente amont** "
                  f"(hub v{fresh['questionnaire_version']})")
            return 0
        frozen = json.loads(_FREEZE.read_text(encoding="utf-8"))
        diverged = 0 if frozen == fresh else 1
        state = ("le gel est identique au hub" if not diverged else
                 f"le gel (v{frozen.get('questionnaire_version', '?')}) diverge "
                 f"du hub (v{fresh['questionnaire_version']}) — régénérer")
        print(state + f" ; synthèses absentes de l'amont : {missing}/18.")
        print(f"**{diverged} divergence(s) de gel · {missing} synthèse(s) en attente amont** "
              f"(hub v{fresh['questionnaire_version']})")
        return 0

    _FREEZE.parent.mkdir(parents=True, exist_ok=True)
    _FREEZE.write_text(json.dumps(fresh, ensure_ascii=False, indent=2) + "\n",
                       encoding="utf-8")
    print(f"gelé : {_FREEZE.relative_to(_REPO)} "
          f"(questionnaire v{fresh['questionnaire_version']}, "
          f"{len(fresh['axes'])} axes, synthèses manquantes : {missing}/18)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
