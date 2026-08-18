"""Access to the SHARED session facts — only what several slides project.

Règle NG 2026-08-18 (« le fait vit dans son bloc ») : un fait qui ne sert
qu'une slide est inliné en constantes dans son bloc. ``static/data/facts.json``
ne garde donc que le PARTAGÉ — aujourd'hui la seule section ``ai_act``,
consommée par les deux slides AI Act (U9 et U9b) : ce qui sert plusieurs
slides vit dans ``custom/``. Le contenu reste hand-curated, vérifié à la
source, et porte ses clés de citation ; une correction d'un fait partagé se
fait dans le JSON, jamais dans une slide.

**Les références ne sont PAS ici.** Une source porte des clés de citation ; la
phrase bibliographique est dérivée de ``static/data/references.bib`` par
``custom.refs``. Deux fichiers, deux rôles : celui-ci dit ce qu'on affirme,
l'autre dit d'où ça vient — et l'appareil critique n'existe qu'une fois.

Language follows the ecosystem convention: every translatable leaf is an
object keyed by language code, and ``metadata.languages`` says which codes the
file actually carries. ``text()`` falls back to the default language rather
than leaving a hole on a projected screen.
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
            f"{_FACTS.name} is missing — the session has no content without "
            f"it, and nothing may be typed into a block instead.")
    return json.loads(_FACTS.read_text(encoding="utf-8"))


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


def section(name: str):
    """One top-level section of the manifest — loud when it is missing."""
    data = manifest().get(name)
    if data is None:
        raise KeyError(
            f"facts.json has no section {name!r} — the slide that asked has "
            f"no content, and nothing may be typed into a block instead.")
    return data


def citekeys(node: dict) -> list[str]:
    """The citation keys of a sourced node (empty list when unsourced)."""
    return list((node.get("source") or {}).get("citekeys") or [])
