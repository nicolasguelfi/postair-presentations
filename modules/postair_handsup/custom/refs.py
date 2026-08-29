"""Les références du document — mécanisme BibTeX, et rien d'autre.

Règle NG (2026-08-03, précisée 2026-08-11) : **toute** référence d'une
présentation passe par le mécanisme BibTeX de streamtex, dans sa forme comme
dans sa provenance. Les données ne portent que des **clés de citation** ; la
slide porte le **code** de citation dans son texte visible — « (Guelfi, 2025) »,
carte complète au survol — et la phrase bibliographique n'est imprimée qu'à un
seul endroit : la page References. Jamais dans une slide, jamais dans un panneau
tooltip (un ``cite()`` dans un panneau de survol serait un hover-dans-hover,
fragile en projection). Pattern canonique : le deck DCS et le manuel
``stx_manual_advanced`` — voir la section références du CLAUDE.md du dépôt.

Ce qu'on y gagne, concrètement : une correction se fait en un seul endroit ; la
même entrée sert la carte au survol, le code en ligne et la page de références ;
et une clé inconnue se voit tout de suite au lieu de passer pour une référence
plausible.

Les blocs n'importent jamais ``streamtex.bib`` directement — ils demandent ici
``citation(...)``.
"""

from __future__ import annotations

from dataclasses import replace
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

from postair_lang import current_lang
from postair_pack.design_systems.postair_dark import (
    CITE_CODE_BLOCK_CSS,
    CITE_CODE_CSS,
)

BIB = Path(__file__).parent.parent / "static" / "data" / "references.bib"

#: Style d'affichage : auteur-année, lisible à voix haute depuis la scène.
#:
#: Tri par auteur, et surtout PAS par ordre de citation : le document est
#: paginé, donc une seule slide s'exécute à la fois. L'ordre de citation
#: dépendrait alors de ce que l'orateur a ouvert avant, et la page de
#: références changerait d'ordre d'une séance à l'autre. Le tri alphabétique
#: est le seul qui donne deux fois la même page.
#: Calibrage projection de la carte au survol (API BibConfig ≥ 0.7.20), repris
#: du deck DCS : le défaut de la librairie (420 px, corps ~12 px) est illisible
#: en amphithéâtre. La carte est ``position:fixed``, donc insensible au zoom
#: des slides — ces tailles sont littérales à l'écran.
_BASE = BibConfig(
    format=BibFormat.APA,
    citation_style=CitationStyle.AUTHOR_YEAR,
    sort_by="author",
    hover_enabled=True,
    locale="en",   # remplacée par la langue projetée dans config() — voir ci-dessous
    # Pas de cite_color : le LOOK du code (plus petit, italique, gris muted)
    # vit dans CITE_CODE_CSS du design system, inliné par ``citation()`` —
    # une couleur posée ici par le scaffold reprendrait la main sur le
    # libellé en mode application, et l'export ne la verrait jamais.
    card_width="780px",
    card_font_scale=2.0,
    card_css="#stx-bib-card{max-height:70vh;overflow-y:auto;}",
)


def config() -> BibConfig:
    """La configuration bib DE CE RUN — sa ``locale`` suit la langue projetée.

    Une constante de module ne suffit pas : le processus Streamlit sert
    ``?lang=en`` et ``?lang=fr`` tour à tour et n'importe ce module qu'une
    fois. Depuis streamtex 0.7.26 la locale est lue par tous les formateurs
    (« Vaswani et Shazeer », « Dans … », « p. », « n° » en français).
    """
    return replace(_BASE, locale=current_lang())


def sources() -> list[str]:
    """Les sources bibliographiques du document, pour ``st_book(bib_sources=…)``.

    Volontairement bruyant si le fichier manque : sans bibliographie, les
    infobulles des deux slides de cadrage n'auraient plus une seule source, et
    une slide de chiffres sans ses sources n'a rien à faire devant un
    amphithéâtre. ``st_book`` avale les erreurs de chargement en un simple
    avertissement de journal — on vérifie donc ici, où ça s'arrête.
    """
    if not BIB.exists():
        raise FileNotFoundError(
            f"{BIB.name} est absent — les références du document en sortent "
            f"toutes, et rien ne doit être réécrit à la main à la place.")
    return [str(BIB)]


def _registry(keys):
    """Le registre, garanti peuplé — quel que soit le chemin d'exécution.

    Trois chemins font tourner ces blocs, et ils ne se ressemblent pas :

    - l'application Streamlit passe par ``st_book``, qui **vide** le registre
      au début de sa construction avant de le remplir depuis ``bib_sources`` ;
    - ``stx export html`` n'appelle pas ``st_book`` du tout : il exécute les
      blocs directement, sans jamais charger de bibliographie ;
    - un test importe parfois un bloc seul.

    Un chargement fait une seule fois, à un seul endroit, se fait donc écraser
    ou manquer selon le chemin — et l'export, qui **avale** l'exception d'un
    bloc en le sautant en silence, produirait un document amputé de ses trois
    slides sourcées sans que rien ne le dise. Le registre est donc rempli à la
    demande, et le réenregistrement est idempotent : le remplir deux fois ne
    coûte rien, ne pas le remplir coûte trois slides.

    Constaté en exécution le 2026-08-03, après une correction qui marchait à
    l'export et cassait dans l'application.
    """
    registry = get_bib_registry()
    if all(registry.get(key) is not None for key in keys):
        return registry
    if not BIB.exists():
        raise FileNotFoundError(
            f"{BIB.name} est absent — les références du document en sortent "
            f"toutes, et rien ne doit être réécrit à la main à la place.")
    set_bib_config(config())
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
    """Le code de citation visible — « (Liang et al., 2023) », carte au survol.

    C'est la SEULE forme qu'une slide a le droit de porter : le code dans le
    texte, la référence complète dans la carte et sur la page References. La
    phrase formatée n'existe plus qu'à un endroit, ``st_bibliography``.
    """
    registry = _registry(keys)
    for key in keys:
        if registry.get(key) is None:
            raise KeyError(
                f"clé de citation inconnue : {key!r} — elle doit exister dans "
                f"{BIB.name}, jamais être remplacée par un texte écrit à la main.")
    return _wrap(cite(*keys, prefix=prefix, suffix=suffix), inline)


def all_entries() -> int:
    """Peuple le registre avec TOUT le ``.bib`` et rend le nombre d'entrées.

    La page de références liste toutes les entrées, pas seulement celles que la
    séance a ouvertes : le document est paginé, donc les slides que l'orateur
    n'a pas atteintes n'ont jamais tourné, et une liste « citées seulement »
    se réduirait à ce qui a été cliqué ce matin-là.
    """
    registry = get_bib_registry()
    set_bib_config(config())
    registry.register_many(load_bib(str(BIB)))
    return len(registry)
