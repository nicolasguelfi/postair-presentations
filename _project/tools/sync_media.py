#!/usr/bin/env python3
"""Matérialiser dans chaque module les médias servis par le CDN.

Le conteneur doit être **complet et autonome** : pendant la séance, aucun appel
au CDN. Mais rien de tout cela ne vit dans git — les octets arrivent ici par cet
outil, depuis les catalogues amont, et se rechargent en vidant le dossier.

    modules/<module>/static/media/
        mascots/<nom>.webp     ← catalogue du studio (cartes-design.json)
        clips/<axe>-<lg>.mp4   ← même catalogue, clé `video` (série « Postures »)
        figures/<sha>.<ext>    ← content.json (portraits + posters des figures)
        illustrations/…        ← VERSIONNÉ, produit pour ces présentations,
                                  jamais au CDN (décision NG 2026-08-01)

**Le rechargement est trivial, et c'est le CDN qui l'offre** : les objets sont
content-adressés — l'URL porte le hash (``…/82db7a5c.webp``). Un fichier local
qui porte ce nom *est* à jour, par construction. La synchro se réduit donc à
« si le fichier du catalogue est absent, le télécharger » : ni revalidation, ni
date, ni invalidation de cache. Recharger tout = supprimer le dossier.

Pourquoi des fichiers et pas les URL du CDN directement : ``st_image`` encode en
base64 tout fichier local, mais laisse passer une URL. Servis par le service
statique de Streamlit (``/app/static/media/…``), ces fichiers sont référencés par
une URL relative — pages légères ET conteneur autonome. Voir ``configure_image_path``
dans le ``book.py`` de chaque module.

Usage (depuis la racine du dépôt) :

    uv run python _project/tools/sync_media.py            # télécharge ce qui manque
    uv run python _project/tools/sync_media.py --check    # constate, n'écrit rien
    uv run python _project/tools/sync_media.py --force    # re-télécharge tout

Sortie 0 = tout est là · 1 = il manque des médias (avec ``--check``).
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

_TOOLS = Path(__file__).parent
_REPO = _TOOLS.parent.parent
_MODULES = _REPO / "modules"

#: Les modules qui affichent des mascottes. Un module qui n'en affiche pas ne
#: paie pas le poids : la synchro est par module, pas globale.
MASCOT_MODULES = ["postair_opening", "postair_debates"]
#: Les modules qui affichent des figures (portraits + posters).
FIGURE_MODULES = ["postair_debates"]
#: Les modules qui projettent un clip de mascotte.
#:
#: On matérialise TOUS les clips du catalogue, pas seulement celui qui est à
#: l'écran aujourd'hui : l'outil ne connaît pas le contenu des slides, et le
#: jour où le deck change de clip, rien ici ne doit bouger. Le coût est modeste
#: — renditions légères, quelques dizaines de Mo — et il achète l'essentiel :
#: l'écran d'attente tourne **vingt minutes devant la salle qui se remplit**,
#: c'est le pire moment possible pour dépendre du réseau.
CLIP_MODULES = ["postair_opening"]

_TIMEOUT = 30


def load_config() -> dict[str, str]:
    local = _TOOLS / "debates-hub.config.local.json"
    if not local.exists():
        raise SystemExit(f"manque {local} — copier debates-hub.config.example.json")
    return json.loads(local.read_text(encoding="utf-8"))


#: Le catalogue gelé — quelques Ko d'URL, VERSIONNÉ. Sans lui, le build Coolify
#: ne pourrait rien matérialiser : il tourne en CI, sans accès aux dépôts privés
#: où vivent les catalogues. Même principe que `content.json` pour le hub : ce
#: qui est versionné est la DÉSIGNATION des médias, jamais les médias.
_FROZEN = _REPO / "modules" / "shared-blocks" / "static" / "_SHARED" / "media-catalogue.json"


def mascot_catalogue(studio: str | None) -> list[tuple[str, str]]:
    """(nom de fichier, URL) des 36 mascottes.

    Lit le catalogue gelé s'il existe — le cas en CI et au build. Le studio, qui
    est la source de vérité de ce qu'il produit, n'est lu que pour REGELER, sur
    la machine de l'auteur (``--freeze``).
    """
    if _FROZEN.exists():
        frozen = json.loads(_FROZEN.read_text(encoding="utf-8"))
        return [(e["file"], e["url"]) for e in frozen["mascots"]]
    if not studio:
        raise SystemExit(f"ni catalogue gelé ({_FROZEN.name}) ni chemin `studio` — rien à lire")
    return _read_studio(studio)


def _studio_design(studio: str) -> dict:
    path = Path(studio) / "shared" / "cartes" / "cartes-design.json"
    if not path.exists():
        raise SystemExit(f"catalogue du studio introuvable : {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _catalogued(design: dict):
    """(clé, entrée) de tous les médias du catalogue : les axes, puis la troupe.

    ``crew`` est une section **sœur** de ``assets``, jamais comptée dedans — le
    contrat amont dit « 36 assets », et les modérateurs s'ajoutent à côté. Les
    deux sections ont exactement la même forme ; ce dépôt consomme des médias et
    n'a pas à distinguer les rôles, donc un seul traitement pour les deux.
    """
    for section in ("assets", "crew"):
        yield from (design.get(section) or {}).items()


def _read_studio(studio: str) -> list[tuple[str, str]]:
    out = []
    for key, entry in _catalogued(_studio_design(studio)):
        url = entry.get("url")
        if not url:
            raise SystemExit(f"asset sans URL dans le catalogue du studio : {key}")
        out.append((f"{key}.webp", url))
    return out


def clip_catalogue(studio: str | None) -> list[tuple[str, str]]:
    """(nom de fichier, URL) des clips « Postures ».

    Même règle que les mascottes : le gel d'abord, le studio seulement pour
    regeler. Un catalogue gelé antérieur à ce chantier ne porte pas de clé
    ``clips`` — on rend alors une liste vide plutôt que d'échouer, et
    ``--freeze`` la remplira.
    """
    if _FROZEN.exists():
        frozen = json.loads(_FROZEN.read_text(encoding="utf-8"))
        return [(e["file"], e["url"]) for e in frozen.get("clips", [])]
    if not studio:
        raise SystemExit(f"ni catalogue gelé ({_FROZEN.name}) ni chemin `studio` — rien à lire")
    return _read_studio_clips(studio)


def _read_studio_clips(studio: str) -> list[tuple[str, str]]:
    """Les clips publiés par `commercials`, déclarés dans le catalogue du studio.

    Chaque asset porte un objet ``video`` indexé par langue. Le nom local est
    dérivé de la clé d'axe et de la langue — JAMAIS du nom content-adressé du
    CDN, qui change à chaque republication et rendrait le deck faux en silence.
    """
    out = []
    for key, entry in _catalogued(_studio_design(studio)):
        for lang, url in sorted((entry.get("video") or {}).items()):
            out.append((f"{key}-{lang}.mp4", url))
    return out


def freeze(studio: str) -> None:
    """Regeler le catalogue depuis le studio. À lancer sur la machine de l'auteur."""
    entries = _read_studio(studio)
    clips = _read_studio_clips(studio)
    design = _studio_design(studio)
    _FROZEN.parent.mkdir(parents=True, exist_ok=True)
    _FROZEN.write_text(json.dumps({
        "_doc": "GÉNÉRÉ par _project/tools/sync_media.py --freeze depuis "
                "mascoties/shared/cartes/cartes-design.json. Ne pas éditer à la main. "
                "Ce fichier ne contient que des URL content-adressées : les octets, eux, "
                "sont matérialisés au build et ne sont jamais versionnés.",
        "source": "mascoties/shared/cartes/cartes-design.json",
        "design_version": design.get("version"),
        "mascots": [{"file": f, "url": u} for f, u in entries],
        "clips": [{"file": f, "url": u} for f, u in clips],
    }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"  catalogue gelé : {len(entries)} mascottes, {len(clips)} clips "
          f"→ {_FROZEN.relative_to(_REPO)}")


def figure_catalogue(module: str) -> list[tuple[str, str]]:
    """(nom de fichier, URL) des portraits et posters, depuis le manifeste gelé.

    Les vidéos restent au CDN : 51 masters de 12 Mo, ouverts deux ou trois fois
    dans la séance. Les embarquer coûterait 612 Mo pour une interaction ponctuelle,
    alors que les images sont à l'écran en permanence.
    """
    manifest = _MODULES / module / "static" / "data" / "content.json"
    if not manifest.exists():
        return []
    data = json.loads(manifest.read_text(encoding="utf-8"))
    seen: dict[str, str] = {}
    for pole in data["poles"]:
        for fig in pole["figures"]:
            media = fig.get("media") or {}
            # `portrait` / `poster` sont les URI LOCALES que la slide demande ;
            # `*_cdn` est la provenance, donc ce qu'il faut télécharger.
            for role in ("portrait_cdn", "poster_cdn"):
                url = media.get(role)
                if url:
                    seen[url.rsplit("/", 1)[-1]] = url
    return sorted(seen.items())


def _wrong_type(name: str, payload: bytes) -> str | None:
    """Le contenu a-t-il la tête de ce que son nom annonce ?

    Sur un réseau à portail captif, la page de connexion est renvoyée **avec un
    code 200**. Sans ce contrôle elle serait écrite sous un nom de média, le
    ``--check`` la compterait comme présente, et la slide afficherait une image
    cassée le jour même.
    """
    head = payload[:16]
    if name.endswith(".webp") and not (head[:4] == b"RIFF" and head[8:12] == b"WEBP"):
        return "ce n'est pas un WebP"
    if name.endswith(".mp4") and b"ftyp" not in head:
        return "ce n'est pas un MP4"
    return None


def fetch(url: str, target: Path) -> int:
    """Télécharger une ressource distante dans un fichier LOCAL.

    Lecture seule côté serveur : un GET, rien d'autre. Ce dépôt ne écrit jamais
    au CDN — ``target`` est un chemin sous ``modules/<module>/static/media/``.

    Trois garde-fous, tous ici et donc tous **au build** : aucun n'ajoute quoi
    que ce soit pendant la séance, où le CDN n'est jamais contacté. Aucun ne
    peut se déclencher sur un fichier correct ; ils ne font que déplacer la
    panne du pire moment (l'amphi) au moins cher (le build, où il suffit de
    relancer).
    """
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        with urllib.request.urlopen(url, timeout=_TIMEOUT) as r:
            payload = r.read()
            announced = r.headers.get("content-length")
    except (urllib.error.URLError, OSError) as e:
        raise SystemExit(f"échec du téléchargement de {url} : {e}") from e

    # Le réseau peut couper sans lever d'erreur : `read()` rend alors moins
    # d'octets qu'annoncé, et le fichier serait écrit entier mais tronqué.
    if announced and announced.isdigit() and int(announced) != len(payload):
        raise SystemExit(f"téléchargement tronqué : {url} — {len(payload)} octets reçus, "
                         f"{announced} annoncés. Rien n'a été écrit ; relancer.")

    wrong = _wrong_type(target.name, payload)
    if wrong:
        raise SystemExit(f"contenu inattendu pour {url} — {wrong} ({len(payload)} octets). "
                         "Un portail captif ou un proxy a sans doute répondu à la place "
                         "du CDN. Rien n'a été écrit.")

    # Écriture atomique : le nom final n'apparaît qu'une fois les octets
    # complets sur le disque. Sinon un build interrompu laisserait un fichier
    # partiel que le `--check` suivant compterait comme PRÉSENT — le conteneur
    # se déclarerait complet en embarquant un média cassé.
    tmp = target.with_name(target.name + ".part")
    tmp.write_bytes(payload)
    tmp.replace(target)
    return len(payload)


def sync(module: str, kind: str, entries: list[tuple[str, str]],
         check: bool, force: bool) -> tuple[int, int, int]:
    """Renvoie (présents, manquants, octets écrits)."""
    root = _MODULES / module / "static" / "media" / kind
    present = missing = written = 0
    for name, url in entries:
        target = root / name
        if target.exists() and not force:
            present += 1
            continue
        missing += 1
        if check:
            print(f"    manque {kind}/{name}")
            continue
        written += fetch(url, target)
    return present, missing, written


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true",
                    help="constater sans écrire ; sortie 1 s'il manque des médias")
    ap.add_argument("--force", action="store_true",
                    help="re-télécharger même ce qui est déjà là")
    ap.add_argument("--freeze", action="store_true",
                    help="regeler le catalogue depuis le studio (machine de l'auteur)")
    args = ap.parse_args()

    # En CI il n'y a ni configuration de machine ni dépôt privé : seul le
    # catalogue gelé est lisible, et il suffit.
    cfg = load_config() if (_TOOLS / "debates-hub.config.local.json").exists() else {}
    studio = cfg.get("studio")

    if args.freeze:
        if not studio:
            raise SystemExit("`--freeze` demande la clé `studio` dans la configuration locale")
        freeze(studio)
        return

    total_missing = total_written = 0
    mascots = mascot_catalogue(studio)
    for module in MASCOT_MODULES:
        p, m, w = sync(module, "mascots", mascots, args.check, args.force)
        total_missing += m
        total_written += w
        print(f"  {module}/mascots   : {p} présents, {m} manquants")
    clips = clip_catalogue(studio)
    for module in CLIP_MODULES:
        p, m, w = sync(module, "clips", clips, args.check, args.force)
        total_missing += m
        total_written += w
        print(f"  {module}/clips     : {p} présents, {m} manquants")
    for module in FIGURE_MODULES:
        figures = figure_catalogue(module)
        p, m, w = sync(module, "figures", figures, args.check, args.force)
        total_missing += m
        total_written += w
        print(f"  {module}/figures   : {p} présents, {m} manquants")

    if args.check:
        print(f"=> {total_missing} média(s) manquant(s)")
        sys.exit(1 if total_missing else 0)
    print(f"=> {total_written / 1024 / 1024:.1f} Mo écrits")


if __name__ == "__main__":
    main()
