"""Access to the SHARED session facts — what several slides project.

Règle NG 2026-08-18 : « le fait vit dans son bloc ». Tout contenu qui ne sert
qu'une slide est inliné en constantes dans son bloc ``bck_mistral_*`` ; ce qui
sert PLUSIEURS slides vit dans ``static/data/facts.json``. Deux partagés ici :

- ``method`` : les 5 étapes de la méthode — projetées par
  ``bck_mistral_method`` ET ``bck_mistral_recap`` (le rappel de fin ne peut
  pas diverger de la slide qu'il rappelle) ;
- ``charter`` : ce que la charte UL dit des outils, de la délégation et des
  données — cité par les infobulles de PLUSIEURS slides (ton outil, tout
  déléguer, données perso, récap). La session guidelines qui suit est la
  vérité pédagogique ; ici on ne fait qu'ancrer chaque avertissement.

The JSON stays hand-curated: every claim verified at its source, carrying its
citation keys. A correction to a shared fact is made in the JSON, never in a
slide.

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


def fact(section_name: str, fact_id: str) -> dict:
    """One shared fact by id — loud when it is missing (jamais de repli muet)."""
    for item in section(section_name):
        if item.get("id") == fact_id:
            return item
    raise KeyError(
        f"facts.json section {section_name!r} has no fact {fact_id!r} — the "
        f"slide that asked has no content, and nothing may be typed into a "
        f"block instead.")


def citekeys(node: dict) -> list[str]:
    """The citation keys of a sourced node (empty list when unsourced)."""
    return list((node.get("source") or {}).get("citekeys") or [])
