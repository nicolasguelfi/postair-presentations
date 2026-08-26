"""Access to the frozen waves manifest — the only content source of this deck.

``static/data/content.json`` is produced by ``_project/tools/build_waves_content.py``
from the hub registry (``great-figures/figures.json``): the seventeen waves, their
figures, their substitution terms, their emblem. No wave name, period, figure name
or substitution term is ever typed into a block: a block asks this module for a
wave and renders what it gets. The hub is the truth — a correction happens there
and arrives here by regeneration (CLAUDE.md, « Le tuyau amont »).

Language follows the ecosystem convention: every translatable leaf is an object
keyed by language code. ``text()`` falls back to the default language rather than
showing an empty slide — a missing translation is an upstream fix, never a hole
on a projected screen.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

_MANIFEST = Path(__file__).parent.parent / "static" / "data" / "content.json"


@lru_cache(maxsize=1)
def manifest() -> dict:
    if not _MANIFEST.exists():
        raise FileNotFoundError(
            f"{_MANIFEST.name} is missing — regenerate it with "
            f"`uv run python _project/tools/build_waves_content.py`")
    return json.loads(_MANIFEST.read_text(encoding="utf-8"))


def default_language() -> str:
    return manifest().get("metadata", {}).get("default_language", "en")


def text(node, lang: str | None = None) -> str:
    """One translatable leaf, in ``lang``, falling back to the default language."""
    if node is None:
        return ""
    if isinstance(node, str):
        return node
    lang = lang or default_language()
    return node.get(lang) or node.get(default_language()) or ""


@lru_cache(maxsize=1)
def waves() -> list[dict]:
    """The seventeen waves, in chronological order (the ``order`` field)."""
    return sorted(manifest()["waves"], key=lambda w: w["order"])


@lru_cache(maxsize=32)
def wave(wave_id: str) -> dict:
    for w in waves():
        if w["id"] == wave_id:
            return w
    raise KeyError(
        f"unknown wave {wave_id!r} — the deck only knows the seventeen ids of "
        f"the frozen manifest, never a hand-typed one.")


def wave_span(first: int, last: int) -> list[dict]:
    """The waves whose ``order`` falls in [first, last] — for the three grids."""
    return [w for w in waves() if first <= w["order"] <= last]


_STORY = Path(__file__).parent.parent / "static" / "data" / "waves-story.json"


@lru_cache(maxsize=1)
def story() -> dict:
    """Le RÉCIT du deck — données éditoriales locales (voir l'en-tête du JSON).

    Les phrases FR sont validées par l'auteur (planches des 25-26/08/2026) ;
    les EN sont des traductions de travail. Destination : le hub (campagne
    ``ai_lesson``) — ce fichier migrera et sera alors gelé par l'outil.
    """
    return json.loads(_STORY.read_text(encoding="utf-8"))


ETAGES = ("objet", "avant", "crise", "recompose")


def etage_label(etage: str, lang: str | None = None) -> str:
    return text(story()["etages"][etage], lang)


def phrase(wave_id: str, etage: str, lang: str | None = None) -> str:
    return text(story()["waves"][wave_id]["phrases"][etage], lang)


def echo(wave_id: str, lang: str | None = None) -> str:
    """L'écho IA de la vague — le point SPÉCIFIQUE transposable (retour NG
    2026-08-26), affiché dans la cellule ambre de la leçon."""
    return text(story()["waves"][wave_id]["echo"], lang)


def image_uri(wave_id: str, etage: str) -> str:
    """L'URI (sous ``static/``) de l'image validée d'un étage du quadriptyque."""
    return f"images/waves/v{wave(wave_id)['order']:02d}-{etage}.webp"


_IMAGES = Path(__file__).parent.parent / "static" / "data" / "waves-images.json"


@lru_cache(maxsize=1)
def images_manifest() -> dict:
    """La PROVENANCE des images du quadriptyque (proposition A, 2026-08-26) —
    le pendant versionné des sidecars managés : moteur, master, retouches,
    et le drapeau ``ai`` qui pilote la pastille DD-35."""
    return json.loads(_IMAGES.read_text(encoding="utf-8"))["images"]


def image_ai(wave_id: str, etage: str) -> bool:
    """Le drapeau de données DD-35 d'une image — bruyant si elle n'est pas
    au manifeste de provenance : une image sans provenance ne se projette pas."""
    key = f"v{wave(wave_id)['order']:02d}-{etage}"
    entry = images_manifest().get(key)
    if entry is None:
        raise KeyError(
            f"image {key!r} absente de waves-images.json — toute image du "
            f"quadriptyque doit porter sa provenance avant d'être projetée.")
    return bool(entry.get("ai", True))
