"""Access to the frozen debate manifest — the only content source of this deck.

``static/data/content.json`` is produced by ``_project/tools/build_debates_content.py``
from the four upstream sources (the debate deck, the figure profiles, the quote
ledger with its editorial layer, the media manifest). No figure name, quotation,
reference or argument is ever typed into a block: a block asks this module for a
pole and renders what it gets.

Language follows the ecosystem convention: every translatable leaf is an object
keyed by language code, and ``metadata.languages`` says which codes the manifest
actually carries. ``text()`` falls back to the default language rather than
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
            f"`uv run python _project/tools/build_debates_content.py`")
    return json.loads(_MANIFEST.read_text(encoding="utf-8"))


def default_language() -> str:
    return manifest().get("metadata", {}).get("default_language", "en")


def languages() -> list[str]:
    return manifest().get("metadata", {}).get("languages", ["en"])


def text(node, lang: str | None = None) -> str:
    """One translatable leaf, in ``lang``, falling back to the default language."""
    if node is None:
        return ""
    if isinstance(node, str):
        return node
    lang = lang or default_language()
    return node.get(lang) or node.get(default_language()) or ""


def corpus_figures() -> int:
    """La taille du corpus étudié (nombre de figures profilées au hub) —
    gelée par l'outil (v2) pour que la slide « pôle sans champion » n'écrive
    jamais un effectif à la main (R-facts)."""
    return int(manifest().get("corpus_figures", 0))


@lru_cache(maxsize=1)
def poles() -> list[dict]:
    return manifest()["poles"]


@lru_cache(maxsize=32)
def axis_poles(axis: str) -> list[dict]:
    """The two poles of one axis, accelerator first.

    The display order is the sumvadis convention already used by the opening
    deck; the ``effect`` field of the instrument decides which side that is,
    so the two axes whose accelerator sits on the left are handled without a
    special case here.
    """
    both = [p for p in poles() if p["axis"] == axis]
    return sorted(both, key=lambda p: p["effect"] != "accelerator")


@lru_cache(maxsize=1)
def axes() -> list[str]:
    """Axis ids in the order the manifest lays them out (the three registers)."""
    seen = []
    for p in poles():
        if p["axis"] not in seen:
            seen.append(p["axis"])
    return seen


def warnings_for(axis: str) -> list[str]:
    """Generator warnings concerning this axis — rendered, never hidden.

    The Individualism pole has no champion in the corpus and the selector had
    to relax its threshold; the slide says so itself rather than presenting
    three lukewarm figures as advocates.
    """
    return [w for w in manifest().get("warnings", []) if w.startswith(f"{axis}/")]
