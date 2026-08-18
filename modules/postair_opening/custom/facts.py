"""Le contenu PARTAGÉ par plusieurs slides — et lui seul.

Règle NG (2026-08-18) : un fait qui ne sert qu'UNE slide vit dans le bloc de
cette slide, en constantes structurées (headline / detail / caveat /
citekeys) ; voir les séries ``bck_already_*`` et ``bck_faculty_*``. Ne reste
ici que ce que plusieurs slides projettent à l'identique — aujourd'hui la
seule réserve « no faculty data », affichée en clair sur les trois slides
facultés.

**Les références ne sont PAS ici.** Une source porte des clés de citation ; la
phrase bibliographique est dérivée de ``static/data/references.bib`` par
``custom.refs``. Clé inconnue = erreur bruyante.

Language follows the ecosystem convention: every translatable leaf is an object
keyed by language code, and ``metadata.languages`` says which codes the file
actually carries. ``text()`` falls back to the default language rather than
leaving a hole on a projected screen.
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
            f"{_FACTS.name} is missing — the faculty slides have no shared "
            f"reserve without it, and nothing may be typed in its place.")
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


def no_faculty_data() -> dict:
    """The reserve sentence, shown on the slide and never softened.

    No survey measures generative-AI adoption faculty by faculty at this
    university. The slide says so where the audience can read it, because the
    people whose faculties are named will be in the room.
    """
    return manifest()["no_faculty_data"]
