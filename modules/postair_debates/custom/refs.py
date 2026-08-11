"""Les références du document — mécanisme BibTeX natif, sur le gel du tuyau.

Règle bib canonique (CLAUDE.md, 2026-08-11) : la slide porte le **code** de
citation dans son texte visible — « (Chowdhury, 2026) », carte complète au
survol — et la phrase bibliographique n'est imprimée que sur la page
References. Pattern de référence : le deck DCS et ``stx_manual_advanced``.

Ici, contrairement à ``postair_opening``, le ``.bib`` n'est pas écrit à la
main : ``static/data/references.bib`` est **GELÉ** par
``_project/tools/build_debates_content.py`` depuis les ``.bib`` du hub
``ai-social-profiles``, limité aux clés que ``content.json`` cite réellement.
Même contrat que le manifeste : ne jamais l'éditer, régénérer. Le hub est la
vérité — une correction bibliographique se fait là-bas et arrive par regel.

Deux régimes cohabitent, par construction du tuyau :

- les **arguments** portent une clé éditoriale (``citekey``) : code natif,
  carte au survol, entrée gelée dans le ``.bib`` ;
- les **citations de figures** n'ont pas encore de clé promue par le hub
  (leurs ``citekeys`` de registre sont heuristiques, non projetables) : la
  chaîne de référence vérifiée reste affichée telle quelle, et
  ``citation_or`` fait le repli sans que les blocs aient à choisir.

Les blocs n'importent jamais ``streamtex.bib`` directement — ils demandent ici
``citation(...)`` ou ``citation_or(...)``.
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

BIB = Path(__file__).parent.parent / "static" / "data" / "references.bib"

#: Style d'affichage : auteur-année, lisible à voix haute depuis la scène.
#: Tri par auteur — le document est paginé, seul ce tri donne deux fois la
#: même page de références (voir le même choix dans postair_opening).
#:
#: Calibrage projection de la carte au survol, repris du deck DCS : le défaut
#: de la librairie (420 px, corps ~12 px) est illisible en amphithéâtre. La
#: carte est ``position:fixed``, donc insensible au zoom des slides.
CONFIG = BibConfig(
    format=BibFormat.APA,
    citation_style=CitationStyle.AUTHOR_YEAR,
    sort_by="author",
    hover_enabled=True,
    locale="en",
    cite_color="#aab2c0",          # code discret dans le texte, gris-bleu clair
    card_width="780px",
    card_font_scale=2.0,
    card_css="#stx-bib-card{max-height:70vh;overflow-y:auto;}",
)


def sources() -> list[str]:
    """Le gel bibliographique du document, pour ``st_book(bib_sources=…)``.

    Volontairement bruyant si le fichier manque : il est généré avec
    ``content.json`` par le même outil — son absence signifie un gel
    incomplet, pas un document sans références. ``st_book`` avale les erreurs
    de chargement en un simple avertissement de journal — on vérifie donc ici.
    """
    if not BIB.exists():
        raise FileNotFoundError(
            f"{BIB.name} est absent — il se GÉNÈRE avec content.json : "
            f"uv run python _project/tools/build_debates_content.py")
    return [str(BIB)]


def _registry(keys):
    """Le registre, garanti peuplé — quel que soit le chemin d'exécution.

    Trois chemins font tourner ces blocs et ne se ressemblent pas :
    l'application (``st_book`` VIDE le registre au début de sa construction),
    ``stx export html`` (qui n'appelle pas ``st_book`` du tout et AVALE
    l'exception d'un bloc en le sautant en silence), et les tests. Le registre
    est donc rempli à la demande, idempotent — le même piège, documenté et
    constaté en exécution, que dans ``postair_opening/custom/refs.py``.
    """
    registry = get_bib_registry()
    if all(registry.get(key) is not None for key in keys):
        return registry
    if not BIB.exists():
        raise FileNotFoundError(
            f"{BIB.name} est absent — il se GÉNÈRE avec content.json : "
            f"uv run python _project/tools/build_debates_content.py")
    set_bib_config(CONFIG)
    registry.register_many(load_bib(str(BIB)))
    return registry


def known(*keys: str) -> bool:
    """Vrai si TOUTES les clés sont dans le gel — sans lever, pour le repli.

    Passe les clés à ``_registry`` : c'est ce qui déclenche le chargement du
    gel quand le registre est encore vide (chemin export, premier bloc). Un
    tuple vide court-circuiterait le chargement et répondrait faux pour des
    clés pourtant gelées — constaté sur l'export du 2026-08-11.
    """
    if not keys or not BIB.exists():
        return False
    registry = _registry(keys)
    return all(registry.get(key) is not None for key in keys)


def citation(*keys: str, prefix: str = "", suffix: str = "") -> str:
    """Le code de citation visible — carte complète au survol. Bruyant."""
    registry = _registry(keys)
    for key in keys:
        if registry.get(key) is None:
            raise KeyError(
                f"clé de citation inconnue : {key!r} — elle doit être gelée "
                f"dans {BIB.name} par build_debates_content.py, jamais "
                f"remplacée par un texte écrit à la main.")
    return cite(*keys, prefix=prefix, suffix=suffix)


def citation_or(fallback: str | None, *keys: str) -> str | None:
    """Le code cite() si les clés sont gelées, sinon le repli du manifeste.

    C'est le seul endroit où le choix code-ou-chaîne se prend : les cartes
    l'appellent sans savoir si le hub a déjà promu la clé. Le jour où une
    citation de figure reçoit sa clé, son code apparaît ici sans qu'un bloc
    change.
    """
    if keys and known(*keys):
        return cite(*keys)
    return fallback


def all_entries() -> int:
    """Peuple le registre avec TOUT le gel et rend le nombre d'entrées.

    La page de références liste toutes les entrées, pas seulement celles que
    la séance a ouvertes : le document est paginé, donc ``get_cited_entries``
    ne voit que la slide courante — le choix déterministe est le même que
    dans ``postair_opening``.
    """
    registry = get_bib_registry()
    set_bib_config(CONFIG)
    registry.register_many(load_bib(str(BIB)))
    return len(registry)
