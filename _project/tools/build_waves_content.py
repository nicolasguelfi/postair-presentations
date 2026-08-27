#!/usr/bin/env python3
"""Gèle le manifeste du deck des vagues depuis le registre du hub.

Jumeau (minimal, lot L1) de ``build_debates_content.py`` — mêmes contrats :

- **Le hub est la vérité.** Source unique de ce gel :
  ``ai-social-profiles/great-figures/figures.json`` (le registre ``waves`` et
  les 55 figures). Une correction se fait LÀ-BAS et arrive par régénération ;
  rien n'est jamais écrit dans le hub depuis ici.
- **Le gel est un artefact GÉNÉRÉ** : ``modules/postair_waves/static/data/
  content.json`` ne s'édite jamais à la main. Règle I3 : aucune adresse
  ``/c/…`` n'y entre (aucune ici : le lot L1 ne gèle pas encore de médias).
- **Chemins de machine** : le même ``debates-hub.config.local.json`` que
  l'outil debates (clé ``hub`` — un seul hub, une seule config par poste).
- L'outil **avertit** quand l'arbre du hub est sale sur ``great-figures/``
  (un gel silencieux est le mode de défaillance à prévenir, pas un arbre sale).

Depuis le lot L3, le gel joint aussi ``great-figures/media-manifest.json`` —
le même régime que debates : **portrait et poster en URI locales**
(``figures/<nom-cdn>``, matérialisées par ``sync_media.py`` depuis les champs
``*_cdn``), **vidéo en URL CDN absolue jamais matérialisée** (streaming à la
demande, ``preload="none"``), et une figure ne porte un lecteur que si portrait
ET vidéo ont ``clearance.channel == "public-ok"`` (gandhi et hawking restent en
nom seul). Il gèle enfin ``references.bib`` : les clés du cadre théorique
(kuhn1962, perez2002), extraites verbatim du ``references.bib`` racine du hub.
Lot L6 (campagne hub) : couche éditoriale ``ai_lesson``, phrases trilingues.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

_TOOLS = Path(__file__).parent
_ROOT = _TOOLS.parent.parent
_DATA = _ROOT / "modules" / "postair_waves" / "static" / "data"
_OUT = _DATA / "content.json"
_OUT_BIB = _DATA / "references.bib"

#: Le cadre théorique de l'intro — des clés du ``references.bib`` racine du
#: hub, copiées VERBATIM dans le gel (jamais réécrites ici).
_BIB_KEYS = ["kuhn1962", "perez2002"]

#: La figure emblématique de chaque vague — recopiée du hub
#: (``great-figures/tools/report_data.py``, relevé du 2026-08-25). Le hub reste
#: la vérité : le gel VÉRIFIE que chaque emblème appartient bien aux figures de
#: sa vague et échoue bruyamment sinon — une divergence se corrige en recopiant
#: la table du hub, jamais en inventant ici.
_EMBLEMS = {
    "writing": "platon", "printing-china": "shen-kuo",
    "medieval-crafts": "ibn-khaldun", "printing-press": "luther",
    "new-science": "galilee", "industrialisation": "marx",
    "rail-telegraph": "thoreau", "germ-theory": "pasteur",
    "electricity": "tesla", "motor-aviation": "saint-exupery",
    "mass-media": "orwell", "atom": "einstein",
    "computer-cybernetics": "turing", "synthetic-chemistry": "carson",
    "genetic-engineering": "berg", "internet-web": "berners-lee",
    "ai": "hinton",
}

_EXPECTED_WAVES = 17
_EXPECTED_FIGURES = 55


def load_config() -> dict[str, str]:
    local = _TOOLS / "debates-hub.config.local.json"
    if not local.exists():
        raise SystemExit(
            f"missing {local} — copy debates-hub.config.example.json and fill it in")
    return json.loads(local.read_text(encoding="utf-8"))


def warn_if_hub_dirty(hub_root: str) -> None:
    """Même garde-fou que build_debates_content : avertir, jamais refuser."""
    try:
        r = subprocess.run(
            ["git", "-C", hub_root, "status", "--porcelain", "--", "great-figures"],
            capture_output=True, text=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return                       # not a git tree here: nothing to assert
    dirty = [ln for ln in r.stdout.splitlines() if ln.strip()]
    if not dirty:
        return
    print(f"! hub has {len(dirty)} uncommitted change(s) on great-figures — "
          "this build freezes work in progress:", file=sys.stderr)
    for line in dirty[:10]:
        print(f"    {line}", file=sys.stderr)
    if len(dirty) > 10:
        print(f"    … and {len(dirty) - 10} more", file=sys.stderr)


def _hub_commit(hub_root: str) -> str:
    try:
        r = subprocess.run(["git", "-C", hub_root, "rev-parse", "--short", "HEAD"],
                           capture_output=True, text=True, check=True)
        return r.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return "?"


def _videos_by_lang(assets: list[dict]) -> dict[str, dict]:
    """Les vidéos de présentation projetables, PAR LANGUE (en/fr/de).

    La langue vit dans le NOM du fichier source (``…__talk__en.mp4``), pas
    dans un champ — convention de la fabrique. 52 figures portent les trois
    langues ; saint-exupery n'a pas de DE — le gel reflète ce qui existe,
    jamais plus (les drapeaux de la slide suivent, retour NG 2026-08-27).
    """
    out: dict[str, dict] = {}
    for v in assets:
        if (v.get("role") != "video"
                or v.get("clearance", {}).get("channel") != "public-ok"):
            continue
        src = v.get("source") or ""
        for lang in ("en", "fr", "de"):
            if f"__{lang}" in src and lang not in out:
                out[lang] = v
    return out


def _figure_media(entry: dict | None) -> dict | None:
    """Le bloc média d'une figure — ``None`` si le lecteur est impossible.

    Une figure n'apparaît avec un lecteur que si elle porte un portrait ET une
    vidéo, chacun ``public-ok`` (CLAUDE.md — un portrait seul ne suffit pas).
    ``portrait``/``poster`` sont les URI locales que ``sync_media.py``
    matérialise depuis ``*_cdn`` ; ``video`` reste une URL CDN absolue.
    """
    if not entry:
        return None
    assets = entry.get("assets", [])
    portrait = next((a for a in assets
                     if a.get("role") == "portrait"
                     and a.get("clearance", {}).get("channel") == "public-ok"),
                    None)
    videos = _videos_by_lang(assets)
    if not portrait or not videos:
        return None
    portrait_cdn = portrait["renditions"]["web-512"]
    first = next(iter(videos.values()))
    poster_cdn = first.get("poster")
    media = {
        "portrait": "figures/" + portrait_cdn.rsplit("/", 1)[-1],
        "portrait_cdn": portrait_cdn,
        "portrait_ai": bool(portrait.get("ai_generated")),
        "videos": {lang: v["url"] for lang, v in videos.items()},
        "video_ai": any(bool(v.get("ai_generated")) for v in videos.values()),
    }
    if poster_cdn:
        media["poster"] = "figures/" + poster_cdn.rsplit("/", 1)[-1]
        media["poster_cdn"] = poster_cdn
    return media


def _freeze_bib(hub: str) -> int:
    """Copie VERBATIM les entrées ``_BIB_KEYS`` du references.bib du hub."""
    text = (Path(hub) / "references.bib").read_text(encoding="utf-8")
    chunks = []
    for key in _BIB_KEYS:
        m = re.search(r"@\w+\{" + re.escape(key) + r"\s*,", text)
        if not m:
            raise SystemExit(f"bib key {key!r} not found in the hub's "
                             f"references.bib — fix the key list, never the hub")
        depth, i = 0, m.start()
        while i < len(text):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    break
            i += 1
        chunks.append(text[m.start():i + 1])
    _OUT_BIB.write_text(
        "% GÉNÉRÉ par _project/tools/build_waves_content.py — ne pas éditer :\n"
        "% régénérer. Entrées copiées verbatim du references.bib du hub.\n\n"
        + "\n\n".join(chunks) + "\n", encoding="utf-8")
    return len(chunks)


def build() -> dict:
    hub = load_config()["hub"]
    warn_if_hub_dirty(hub)
    registry = json.loads(
        (Path(hub) / "great-figures" / "figures.json").read_text(encoding="utf-8"))
    media_manifest = json.loads(
        (Path(hub) / "great-figures" / "media-manifest.json")
        .read_text(encoding="utf-8"))["figures"]

    raw_waves = registry["waves"]
    raw_figures = registry["figures"]
    if len(raw_waves) != _EXPECTED_WAVES:
        raise SystemExit(f"hub registry has {len(raw_waves)} waves, "
                         f"expected {_EXPECTED_WAVES} — refusing a partial freeze")
    if len(raw_figures) != _EXPECTED_FIGURES:
        raise SystemExit(f"hub registry has {len(raw_figures)} figures, "
                         f"expected {_EXPECTED_FIGURES} — refusing a partial freeze")

    by_wave: dict[str, list[dict]] = {w["id"]: [] for w in raw_waves}
    for f in raw_figures:
        if f["wave"] not in by_wave:
            raise SystemExit(f"figure {f['id']!r} points at unknown wave "
                             f"{f['wave']!r} — fix the HUB, never this freeze")
        by_wave[f["wave"]].append({
            "id": f["id"], "name": f["name"], "dates": f.get("dates"),
            "origin": f.get("origin"), "stance": f.get("stance"),
            "stance_class": f.get("stance_class"), "tier": f.get("tier"),
            "media": _figure_media(media_manifest.get(f["id"])),
        })

    waves = []
    for w in sorted(raw_waves, key=lambda w: w["order"]):
        emblem = _EMBLEMS.get(w["id"])
        figure_ids = [f["id"] for f in by_wave[w["id"]]]
        if emblem not in figure_ids:
            raise SystemExit(
                f"emblem {emblem!r} is not among the figures of wave "
                f"{w['id']!r} ({figure_ids}) — the _EMBLEMS table has drifted "
                f"from the hub's report_data.py: recopy it from the hub.")
        waves.append({
            "id": w["id"], "code": w["code"], "order": w["order"],
            "period": w["period"], "name": w["name"],
            "substitution": w.get("substitution"),
            "emblem": emblem,
            "figures": sorted(by_wave[w["id"]], key=lambda f: f["id"]),
        })

    return {
        "metadata": {
            "_doc": "GÉNÉRÉ par _project/tools/build_waves_content.py — ne "
                    "jamais éditer : régénérer. Le hub est la vérité.",
            "generated_by": "build_waves_content.py (lot L1)",
            "hub_commit": _hub_commit(hub),
            "languages": ["en", "fr"],
            "default_language": "en",
        },
        "waves": waves,
    }


def main() -> None:
    manifest = build()
    _OUT.parent.mkdir(parents=True, exist_ok=True)
    _OUT.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")
    n_bib = _freeze_bib(load_config()["hub"])
    n_fig = sum(len(w["figures"]) for w in manifest["waves"])
    n_med = sum(1 for w in manifest["waves"] for f in w["figures"] if f["media"])
    silent = [f["id"] for w in manifest["waves"] for f in w["figures"]
              if not f["media"]]
    print(f"{_OUT.relative_to(_ROOT)}  —  {len(manifest['waves'])} waves, "
          f"{n_fig} figures ({n_med} with player, sans lecteur: "
          f"{', '.join(silent) or 'aucune'})  (hub "
          f"{manifest['metadata']['hub_commit']})")
    print(f"{_OUT_BIB.relative_to(_ROOT)}  —  {n_bib} entrées gelées")


if __name__ == "__main__":
    main()
