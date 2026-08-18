"""Les références du document — mécanisme BibTeX, et rien d'autre.

Règle bib canonique (CLAUDE.md, 2026-08-11) : les données ne portent que des
**clés de citation** ; la slide porte le **code** de citation dans son texte
visible — « (Turing, 1950) », carte complète au survol — et la phrase
bibliographique n'est imprimée qu'à un seul endroit : la page References.
Jamais dans une slide, jamais dans un panneau tooltip (hover-dans-hover).
Pattern canonique : le deck DCS et ``stx_manual_advanced``.

Copie conforme de ``postair_opening/custom/refs.py`` — même registre à la
demande, mêmes erreurs bruyantes, même calibrage projection de la carte.

Les blocs n'importent jamais ``streamtex.bib`` directement — ils demandent ici
``citation(...)``.
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

#: Style d'affichage : auteur-année, lisible à voix haute depuis la scène.
#: Tri par auteur — le document est paginé, seul ce tri donne deux fois la
#: même page de références. Calibrage projection de la carte au survol repris
#: du deck DCS (le défaut librairie, 420 px / corps ~12 px, est illisible en
#: amphithéâtre ; la carte est ``position:fixed``, insensible au zoom).
CONFIG = BibConfig(
    format=BibFormat.APA,
    citation_style=CitationStyle.AUTHOR_YEAR,
    sort_by="author",
    hover_enabled=True,
    locale="en",
    # Pas de cite_color : le LOOK du code (plus petit, italique, gris muted)
    # vit dans CITE_CODE_CSS du design system, inliné par ``citation()`` —
    # une couleur posée ici par le scaffold reprendrait la main sur le
    # libellé en mode application, et l'export ne la verrait jamais.
    card_width="780px",
    card_font_scale=2.0,
    card_css="#stx-bib-card{max-height:70vh;overflow-y:auto;}",
)


def sources() -> list[str]:
    """Les sources bibliographiques du document, pour ``st_book(bib_sources=…)``."""
    if not BIB.exists():
        raise FileNotFoundError(
            f"{BIB.name} est absent — les références du document en sortent "
            f"toutes, et rien ne doit être réécrit à la main à la place.")
    return [str(BIB)]


def _registry(keys):
    """Le registre, garanti peuplé — quel que soit le chemin d'exécution.

    Trois chemins font tourner ces blocs et ne se ressemblent pas :
    l'application (``st_book`` VIDE le registre au début de sa construction),
    ``stx export html`` (qui n'appelle pas ``st_book`` du tout et AVALE
    l'exception d'un bloc en le sautant en silence), et les tests. Le registre
    est donc rempli à la demande, idempotent — piège documenté et constaté en
    exécution dans ``postair_opening/custom/refs.py`` le 2026-08-03.
    """
    registry = get_bib_registry()
    if all(registry.get(key) is not None for key in keys):
        return registry
    if not BIB.exists():
        raise FileNotFoundError(
            f"{BIB.name} est absent — les références du document en sortent "
            f"toutes, et rien ne doit être réécrit à la main à la place.")
    set_bib_config(CONFIG)
    registry.register_many(load_bib(str(BIB)))
    return registry


def _wrap(code: str, inline: bool) -> str:
    """Le fragment ``cite()`` habillé du style collection (règle NG 2026-08-15).

    Style INLINÉ, pas injecté : il doit suivre le fragment dans l'application
    ET dans l'export HTML statique (qui ne reçoit pas le scaffold bib), et
    couvrir les parenthèses, que ``.stx-cite`` n'enveloppe pas. Par défaut le
    code passe À LA LIGNE (fin de phrase/paragraphe) ; ``inline=True`` est
    l'exception assumée par le bloc, quand la coupure créerait une ambiguïté.
    """
    css = CITE_CODE_CSS if inline else CITE_CODE_BLOCK_CSS
    return f'<span style="{css}">{code}</span>'


def citation(*keys: str, prefix: str = "", suffix: str = "",
             inline: bool = False) -> str:
    """Le code de citation visible — carte complète au survol. Bruyant."""
    registry = _registry(keys)
    for key in keys:
        if registry.get(key) is None:
            raise KeyError(
                f"clé de citation inconnue : {key!r} — elle doit exister dans "
                f"{BIB.name}, jamais être remplacée par un texte écrit à la main.")
    return _wrap(cite(*keys, prefix=prefix, suffix=suffix), inline)


def all_entries() -> int:
    """Peuple le registre avec TOUT le ``.bib`` et rend le nombre d'entrées.

    La page de références liste toutes les entrées, pas seulement celles que
    la séance a ouvertes : le document est paginé, donc ``get_cited_entries``
    ne voit que la slide courante.
    """
    registry = get_bib_registry()
    set_bib_config(CONFIG)
    registry.register_many(load_bib(str(BIB)))
    return len(registry)
