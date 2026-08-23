"""Geler le catalogue des captures d'écran du parcours SUMVADIS.

Le deck « The SUMVADIS Tool » (``modules/postair_survey``) projette les écrans
réels de l'application — jamais des maquettes. Comme pour ``postair_debates``,
rien n'est écrit à la main : cet outil lit le registre des médias du dépôt
sumvadis (``packages/core/assets/media-registry.jsonl``, journal en ajout
seul, DD-47) et gèle la sélection dans

    modules/postair_survey/static/data/captures-catalogue.json

Les octets, eux, ne sont jamais versionnés : ``sync_media.py`` les matérialise
au build sous ``modules/postair_survey/static/media/captures/``, comme les
mascottes et les figures. Ce qui est versionné est la DÉSIGNATION des médias.

Politique de gel (décision D, NG 2026-08-21 — la MATRICE COMPLÈTE) :

- langues : ``en``, ``fr``, ``de`` — tout ce que le registre publie ;
- facettes : les quatre (``mobile``/``desktop`` × ``sombre``/``clair``) pour
  CHAQUE écran — le choix de ce qui est projeté descend dans la slide
  (``capture(slug, device=…, theme=…, lang=…)``), plus dans la politique ;
- ``17-res-page-entiere`` : EXCLU, inchangé (6,1 Mo par variante, page
  défilante illisible projetée — l'embarquer douze fois serait du lest pur) ;
- le DÉFAUT de ``capture()`` reste ``mobile · sombre · en`` (Q14) : élargir le
  gel ne change pas ce que les slides existantes projettent.

Coût assumé (NG 2026-08-21) : ~12 variantes × ~29 écrans ≈ 350 fichiers,
de l'ordre de 150-200 Mo matérialisés dans CHAQUE image de service — contre
14 Mo avant. En échange : n'importe quelle facette/langue se demande dans une
slide sans regel ni campagne.

**Règle I3 (sumvadis design/11, lot L5)** : un artefact GELÉ ne porte JAMAIS
d'adresse de concept ``/c/…``. Seules les adresses de VERSION ``/v/…`` du
registre entrent dans le gel — immuables, donc « fichier présent = à jour »
reste vrai par construction. Une adresse non-``/v/`` est un refus bruyant,
jamais un repli.

Le nom local porte l'horodatage PAR (slug, langue, facette) :
``<slug>__<lang>__<facette>__<horodatage>.png`` — un regel change le nom, et
``sync_media.py`` n'a donc jamais à revalider quoi que ce soit.

Chemins de machine : ``survey-captures.config.local.json`` (gitignoré ;
copier ``survey-captures.config.example.json``). Une seule clé est lue,
``sumvadis``. Le registre est en LECTURE SEULE : on n'écrit jamais en amont.

Usage
-----
    uv run python _project/tools/build_survey_captures.py               # gèle le catalogue
    uv run python _project/tools/build_survey_captures.py --work-order  # constat, stdout seul
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

_TOOLS = Path(__file__).parent
_REPO = _TOOLS.parent.parent
_OUT = _REPO / "modules" / "postair_survey" / "static" / "data" / "captures-catalogue.json"

#: Le registre des médias du dépôt sumvadis — journal en ajout seul (DD-47) :
#: l'état courant se calcule en REJOUANT le fichier, la dernière ligne gagne.
_REGISTRY = "packages/core/assets/media-registry.jsonl"
_DOMAINE = "parcours"
_ID_PREFIX = "postair"

# ── Politique de gel (décision D, NG 2026-08-21 — matrice complète) ─────────
LANGS = ("en", "fr", "de")
THEMES = ("sombre", "clair")
DEVICES = ("mobile", "desktop")
EXCLUDE = ("17-res-page-entiere",)
#: Écrans de régie et de diaporama attendus de la campagne sumvadis ss12
#: (chantier 3b + Q15). Rapportés « prévus, non publiés » tant qu'absents du
#: registre ; le jour où ils y entrent, la politique desktop ci-dessus les
#: gèle sans rien changer ici (les slugs diaporama 23+ s'ajouteront seuls).
PLANNED_SLUGS = ("20-admin-console", "21-admin-salle", "22-admin-projection")

#: Chemins sumvadis dont l'état non committé serait photographié par le gel.
_GATE_PATHS = ["packages/e2e", "packages/core/assets"]


def load_config() -> dict[str, str]:
    local = _TOOLS / "survey-captures.config.local.json"
    if not local.exists():
        raise SystemExit(f"missing {local} — copy survey-captures.config.example.json and fill it in")
    return json.loads(local.read_text(encoding="utf-8"))


def warn_if_dirty(root: str) -> None:
    """Say so when the freeze would photograph work in progress.

    Même arbitrage que ``build_debates_content.py`` : les sessions de campagne
    régénèrent le registre bien avant de committer — refuser rendrait le
    contrôle avant/après inutilisable. On avertit, bruyamment, et l'auteur
    décide. Le gel silencieux est la panne à prévenir, pas l'arbre sale.
    """
    try:
        r = subprocess.run(["git", "-C", root, "status", "--porcelain", "--"] + _GATE_PATHS,
                           capture_output=True, text=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return                       # not a git tree here: nothing to assert
    dirty = [ln for ln in r.stdout.splitlines() if ln.strip()]
    if not dirty:
        return
    print(f"! sumvadis has {len(dirty)} uncommitted change(s) on {'/'.join(_GATE_PATHS)} — "
          "this freeze photographs work in progress:", file=sys.stderr)
    for line in dirty[:10]:
        print(f"    {line}", file=sys.stderr)
    if len(dirty) > 10:
        print(f"    … and {len(dirty) - 10} more", file=sys.stderr)


def wanted_facettes(slug: str) -> tuple[str, ...]:
    """Les facettes de la MATRICE DE BASE — celles dont l'absence est signalée.

    Matrice complète (décision D, NG 2026-08-21) : les quatre facettes
    appareil × thème pour chaque écran. Depuis le 2026-08-23, le gel prend en
    plus TOUT ce que le registre publie au-delà (ex. les pleines pages
    ``capture-mobile-complet-*``) — opportuniste : gelé si présent, jamais
    « attendu manquant ». Cette fonction ne sert donc plus qu'au constat des
    trous de la matrice de base.
    """
    if slug in EXCLUDE:
        return ()
    return tuple(f"capture-{device}-{theme}"
                 for device in DEVICES for theme in THEMES)


def load_registry(root: Path) -> dict[tuple[str, str, str], dict]:
    """(slug, lang, facette) → dernière entrée ``version`` du domaine parcours.

    Rejeu du journal, dans l'ordre du fichier : une ligne ``version`` remplace
    la précédente pour le même triplet, une ligne ``retire`` retire l'id du
    service (toutes facettes), une ``version`` postérieure le rétablit.
    """
    path = root / _REGISTRY
    if not path.exists():
        raise SystemExit(f"registre introuvable : {path}")
    latest: dict[tuple[str, str, str], dict] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        raw = raw.strip()
        if not raw or raw.startswith("#"):
            continue
        e = json.loads(raw)
        kind = e.get("kind")
        if kind == "retire":
            parts = (e.get("id") or "").split("__")
            if len(parts) == 3 and parts[0] == _ID_PREFIX:
                _, slug, lang = parts
                for key in [k for k in latest if k[0] == slug and k[1] == lang]:
                    del latest[key]
            continue
        if kind != "version" or e.get("domaine") != _DOMAINE:
            continue
        parts = e["id"].split("__")
        if len(parts) != 3 or parts[0] != _ID_PREFIX:
            continue
        _, slug, lang = parts
        latest[(slug, lang, e["facette"])] = e
    return latest


def select(latest: dict[tuple[str, str, str], dict]) -> dict:
    """Applique la politique de gel au registre rejoué.

    Renvoie ``captures`` (les entrées gelables), ``missing`` (attendues par la
    politique mais absentes du registre, écrans prévus exclus), ``planned``
    (les écrans de régie/diaporama pas encore publiés) et ``non_v`` (adresses
    violant la règle I3 — le compteur doit rester à 0).
    """
    published = sorted({slug for (slug, _l, _f) in latest})
    captures, missing, non_v = [], [], []
    for slug in published:
        base = wanted_facettes(slug)
        if not base:          # écran exclu (17-res-page-entiere)
            continue
        # La matrice de base, PLUS toute facette publiée au-delà (gel
        # opportuniste, 2026-08-23) — l'absence n'est signalée que pour la base.
        extra = sorted({(f, l) for (s2, l, f) in latest
                        if s2 == slug and f not in base})
        for facette, lang in ([(f, l) for f in base for l in LANGS] + extra):
            entry = latest.get((slug, lang, facette))
            if entry is None:
                missing.append(f"{slug} · {lang} · {facette}")
                continue
            url = entry.get("version_url") or ""
            if "/v/" not in url:
                non_v.append(f"{slug} · {lang} · {facette} — {url or 'sans adresse'}")
                continue
            stamp = entry["horodatage"]
            captures.append({
                "slug": slug, "lang": lang, "facette": facette,
                "horodatage": stamp,
                # Le nom local porte l'horodatage PAR (slug, lang, facette) :
                # un regel change le nom, « fichier présent = à jour » reste
                # vrai par construction côté sync_media.
                "file": f"{slug}__{lang}__{facette}__{stamp}.png",
                "url": url,
                "sha256": entry.get("sha256"),
            })
    planned = [s for s in PLANNED_SLUGS if s not in published]
    return {"captures": captures, "missing": missing, "planned": planned, "non_v": non_v}


def freeze(selection: dict) -> None:
    _OUT.parent.mkdir(parents=True, exist_ok=True)
    _OUT.write_text(json.dumps({
        "_doc": "GÉNÉRÉ par _project/tools/build_survey_captures.py depuis le registre des "
                "médias du dépôt sumvadis (packages/core/assets/media-registry.jsonl). Ne pas "
                "éditer à la main : régénérer. Adresses de VERSION /v/ uniquement (règle I3) ; "
                "les octets sont matérialisés au build par sync_media.py et jamais versionnés.",
        "source": f"sumvadis {_REGISTRY}",
        "domaine": _DOMAINE,
        "policy": {
            "langs": list(LANGS),
            "themes": list(THEMES),
            "devices": list(DEVICES),
            "matrix": "complète (décision D, NG 2026-08-21) — le choix de "
                      "projection descend dans la slide",
            "exclude": list(EXCLUDE),
            "planned": list(PLANNED_SLUGS),
        },
        "captures": selection["captures"],
        "planned_unpublished": selection["planned"],
    }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def work_order(selection: dict) -> str:
    """L'état du gel face au registre, sur stdout — ne modifie rien.

    Même contrat que ``build_debates_content.py --work-order`` : tout ce qui
    est listé ici existe déjà en amont, une copie committée ne ferait que
    dupliquer le registre. Ce qui est local — ce que CE deck projette — se
    recalcule à la demande, par la même règle que le gel.
    """
    frozen = {}
    if _OUT.exists():
        data = json.loads(_OUT.read_text(encoding="utf-8"))
        frozen = {(c["slug"], c["lang"], c["facette"]): c for c in data.get("captures", [])}
    fresh = {(c["slug"], c["lang"], c["facette"]): c for c in selection["captures"]}

    stale = [f"{k[0]} · {k[1]} · {k[2]} — gelé {frozen[k]['horodatage']}, "
             f"registre {fresh[k]['horodatage']}"
             for k in sorted(frozen.keys() & fresh.keys())
             if frozen[k]["horodatage"] != fresh[k]["horodatage"]]
    to_add = sorted(fresh.keys() - frozen.keys())
    to_drop = sorted(frozen.keys() - fresh.keys())

    out = ["# Captures du parcours — état du gel",
           "",
           "> Sortie de `build_survey_captures.py --work-order`. **Éphémère par",
           "> construction** : la vérité est le registre sumvadis, cette liste ne fait",
           "> que le comparer au catalogue gelé du module. Rien n'est modifié.",
           "",
           f"- {len(fresh)} capture(s) attendue(s) par la politique, "
           f"{len(frozen)} gelée(s) dans {_OUT.name}"]
    if not _OUT.exists():
        out.append(f"- **catalogue absent** ({_OUT.relative_to(_REPO)}) — lancer le gel")
    for line in stale:
        out.append(f"- gel PÉRIMÉ : {line}")
    for k in to_add:
        out.append(f"- à geler (absent du catalogue) : {k[0]} · {k[1]} · {k[2]}")
    for k in to_drop:
        out.append(f"- gelé mais plus sélectionné : {k[0]} · {k[1]} · {k[2]}")
    for line in selection["missing"]:
        out.append(f"- ATTENDUE MANQUANTE au registre : {line} — publier l'écran dans "
                   f"sumvadis (parcours_publier.py), jamais contourner ici")
    for slug in selection["planned"]:
        out.append(f"- prévu, non publié : {slug} (campagne sumvadis ss12 — chantier 3b/Q15)")
    out += ["",
            f"**{len(stale) + len(to_add) + len(to_drop)} écart(s) de gel · "
            f"{len(selection['missing'])} attendue(s) manquante(s) · "
            f"{len(selection['non_v'])} adresse(s) non-/v/ (doit rester 0).**"]
    for line in selection["non_v"]:
        out.append(f"- RÈGLE I3 VIOLÉE : {line}")
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--work-order", action="store_true",
                    help="constat gel/registre sur stdout — ne modifie rien")
    args = ap.parse_args()

    root = load_config()["sumvadis"]
    warn_if_dirty(root)
    selection = select(load_registry(Path(root)))

    if args.work_order:
        print(work_order(selection))
        return

    if selection["non_v"]:
        for line in selection["non_v"]:
            print(f"  ! règle I3 : {line}", file=sys.stderr)
        raise SystemExit(f"{len(selection['non_v'])} adresse(s) non-/v/ dans la sélection — "
                         "un gel ne porte JAMAIS d'adresse /c/ (règle I3). Rien n'a été écrit.")

    freeze(selection)
    print(f"wrote {_OUT.relative_to(_REPO)} — {len(selection['captures'])} capture(s), "
          f"{len(selection['missing'])} attendue(s) manquante(s), "
          f"{len(selection['planned'])} écran(s) prévu(s) non publié(s)")
    for line in selection["missing"]:
        print(f"  ! manquante au registre : {line}")
    for slug in selection["planned"]:
        print(f"  · prévu, non publié : {slug}")


if __name__ == "__main__":
    main()
