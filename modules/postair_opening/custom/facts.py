"""Access to the framing facts — the only content source of the two scoping slides.

``static/data/facts.json`` is hand-curated rather than generated: every figure
was verified at its own source, carries its date, its population, its citation
keys and its counterpoint. No number, claim or reference is ever typed into
a block — a block asks this module for a figure and renders what it gets. A
correction is made in the JSON, never in a slide.

**Les références ne sont PAS ici.** Une source porte des clés de citation ; la
phrase bibliographique est dérivée de ``static/data/references.bib`` par
``custom.refs``. Deux fichiers, deux rôles : celui-ci dit ce qu'on affirme,
l'autre dit d'où ça vient — et l'appareil critique n'existe qu'une fois.

Language follows the ecosystem convention: every translatable leaf is an object
keyed by language code, and ``metadata.languages`` says which codes the file
actually carries. ``text()`` falls back to the default language rather than
leaving a hole on a projected screen.

Two levels of wording live side by side, because an auditorium and a tooltip do
not read the same way: ``headline`` / ``short`` / ``attribution`` are the few
words that go on a card, the long leaves are the full sourced statement that
goes in the tooltip. Both come from the data, so neither can drift from the
other.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

_FACTS = Path(__file__).parent.parent / "static" / "data" / "facts.json"


@lru_cache(maxsize=1)
def manifest() -> dict:
    if not _FACTS.exists():
        raise FileNotFoundError(
            f"{_FACTS.name} is missing — the scoping slides have no content "
            f"without it, and nothing may be typed into a block instead.")
    return json.loads(_FACTS.read_text(encoding="utf-8"))


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


@lru_cache(maxsize=1)
def figures() -> list[dict]:
    """The figures the deck projects, in the order the manifest asks for.

    ``metadata.display_order`` is what the slide shows; the array may hold more
    than the deck uses. A figure named in the order but absent from the array is
    a curation error and raises here rather than rendering an empty card.
    """
    by_id = {f["id"]: f for f in manifest()["figures"]}
    order = manifest()["metadata"].get("display_order") or list(by_id)
    missing = [fid for fid in order if fid not in by_id]
    if missing:
        raise KeyError(f"display_order names unknown figures: {', '.join(missing)}")
    return [by_id[fid] for fid in order]


@lru_cache(maxsize=8)
def framing(framing_id: str) -> dict:
    """One qualitative sourced statement.

    These are claims that carry no population — a publication year has no
    sample — and are therefore deliberately kept out of ``figures``.
    """
    for entry in manifest().get("framing", []):
        if entry["id"] == framing_id:
            return entry
    raise KeyError(f"unknown framing statement: {framing_id}")


@lru_cache(maxsize=1)
def disciplines() -> list[dict]:
    return manifest()["disciplines"]


def no_faculty_data() -> dict:
    """The reserve sentence, shown on the slide and never softened.

    No survey measures generative-AI adoption faculty by faculty at this
    university. The slide says so where the audience can read it, because the
    people whose faculties are named will be in the room.
    """
    return manifest()["no_faculty_data"]


def sources(entry: dict) -> list[dict]:
    """Every source object attached to a figure or framing statement.

    A counterpoint carries its own source; a framing statement carries several.
    Callers use this to build a tooltip that credits all of them, so a claim can
    never appear on screen with its rebuttal uncredited.
    """
    found = []
    if entry.get("source"):
        found.append(entry["source"])
    for key in ("counterpoint", "caveat"):
        node = entry.get(key)
        if isinstance(node, dict) and node.get("source"):
            found.append(node["source"])
    found.extend(entry.get("sources", []))
    return [s for s in found if s.get("citekeys")]


def citekeys(entry: dict) -> list[str]:
    """Toutes les clés de citation d'une entrée, sans doublon, dans l'ordre.

    Une entrée cite sa propre source, celle de son contrepoint, et le cas
    échéant les travaux qui la confirment (``also``). C'est ce que la référence
    imprimée doit couvrir : un chiffre projeté sans la publication qui le
    conteste serait un chiffre arrangé.
    """
    keys: list[str] = []
    for source in sources(entry):
        keys.extend(source["citekeys"])
    keys.extend(entry.get("also", []))
    return list(dict.fromkeys(keys))
