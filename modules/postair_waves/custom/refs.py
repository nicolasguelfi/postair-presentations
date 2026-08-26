"""Les références du document — mécanisme BibTeX natif, sur le gel du tuyau.

Règle bib canonique (CLAUDE.md, 2026-08-11) : la slide porte le **code** de
citation dans son texte visible, carte complète au survol, et la phrase
bibliographique n'est imprimée que sur la page References.

Le ``.bib`` n'est pas écrit à la main : ``static/data/references.bib`` est
**GELÉ** par ``_project/tools/build_waves_content.py`` — les entrées du cadre
théorique (kuhn1962, perez2002) copiées verbatim depuis le ``references.bib``
racine du hub. Même contrat que ``content.json`` : ne jamais l'éditer,
régénérer. Les blocs n'importent jamais ``streamtex.bib`` directement — ils
demandent ici ``citation(...)``.
"""

from __future__ import annotations

from pathlib import Path

from streamtex import (
    BibConfig,
    BibFormat,
    CitationStyle,
    cite,
    get_bib_registry,
    load_bib,
    set_bib_config,
)

from postair_pack.design_systems.postair_dark import (
    CITE_CODE_BLOCK_CSS,
    CITE_CODE_CSS,
)

BIB = Path(__file__).parent.parent / "static" / "data" / "references.bib"

#: Calibrage projection de la carte au survol — le même que les autres decks
#: (le défaut 420 px / corps 12 px est illisible en amphithéâtre).
CONFIG = BibConfig(
    format=BibFormat.APA,
    citation_style=CitationStyle.AUTHOR_YEAR,
    sort_by="author",
    hover_enabled=True,
    locale="en",
    card_width="780px",
    card_font_scale=2.0,
    card_css="#stx-bib-card{max-height:70vh;overflow-y:auto;}",
)


def sources() -> list[str]:
    """Le gel bibliographique, pour ``st_book(bib_sources=…)`` — bruyant."""
    if not BIB.exists():
        raise FileNotFoundError(
            f"{BIB.name} est absent — il se GÉNÈRE avec content.json : "
            f"uv run python _project/tools/build_waves_content.py")
    return [str(BIB)]


def _registry(keys):
    """Le registre, garanti peuplé — application, export et tests confondus.

    Même piège documenté que dans debates/opening : ``st_book`` vide le
    registre au début de sa construction et l'export n'appelle pas
    ``st_book`` du tout — le registre se remplit donc à la demande.
    """
    registry = get_bib_registry()
    if all(registry.get(key) is not None for key in keys):
        return registry
    if not BIB.exists():
        raise FileNotFoundError(
            f"{BIB.name} est absent — il se GÉNÈRE avec content.json : "
            f"uv run python _project/tools/build_waves_content.py")
    set_bib_config(CONFIG)
    registry.register_many(load_bib(str(BIB)))
    return registry


def _wrap(code: str, inline: bool) -> str:
    """Le fragment ``cite()`` habillé du style collection (règle NG 2026-08-15)."""
    css = CITE_CODE_CSS if inline else CITE_CODE_BLOCK_CSS
    return f'<span style="{css}">{code}</span>'


def citation(*keys: str, prefix: str = "", suffix: str = "",
             inline: bool = False) -> str:
    """Le code de citation visible — carte complète au survol. Bruyant."""
    registry = _registry(keys)
    for key in keys:
        if registry.get(key) is None:
            raise KeyError(
                f"clé de citation inconnue : {key!r} — elle doit être gelée "
                f"dans {BIB.name} par build_waves_content.py, jamais "
                f"remplacée par un texte écrit à la main.")
    return _wrap(cite(*keys, prefix=prefix, suffix=suffix), inline)


def all_entries() -> int:
    """Peuple le registre avec TOUT le gel — la page References liste tout
    (deck paginé : ``get_cited_entries`` ne voit que la slide courante)."""
    registry = get_bib_registry()
    set_bib_config(CONFIG)
    registry.register_many(load_bib(str(BIB)))
    return len(registry)
