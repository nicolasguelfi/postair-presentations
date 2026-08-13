"""La marque de transparence IA — transcription du mécanisme sumvadis (DD-35).

La référence unique de la convention est ``apps/web/src/components/AiMark.tsx``
du dépôt sumvadis (gate e2e ``ai-mark.spec.ts``) : pastille « ✦ AI », texte
blanc sur gris ``zinc-500`` à 35 % d'alpha (directive d'auteur 2026-07-30 —
discret, vraie transparence), bas-droite du média, clics traversants. C'est la
divulgation visible exigée par l'art. 50 de l'AI Act, en vigueur pendant
l'AI Day ; le pendant lisible par machine (C2PA/XMP) voyage DANS le fichier,
posé par le pipeline de publication de la fabrique — jamais ici.

Règle d'auteur reprise telle quelle : la marque est une SUPERPOSITION, jamais
incrustée dans le média — les pixels restent intacts, et la pastille est
pilotée par le drapeau de données (``ai_generated`` des manifestes et
sidecars), donc impossible à oublier sur un nouvel asset.

Deux écarts assumés avec la fiche web, imposés par le support :

- la taille est à l'échelle d'un amphithéâtre (``clamp`` sur la largeur de
  fenêtre), pas les 9 px d'un écran de téléphone ;
- ``st_write`` ne pose pas d'attribut ``aria-label`` : le texte de la pastille
  EST la divulgation lisible.
"""

from __future__ import annotations

from contextlib import contextmanager

from streamtex import st_block, st_write
from streamtex.enums import Tags as t
from streamtex.styles import Style

#: Le conteneur marqué épouse son média. ``fit`` : largeur au contenu (média à
#: largeur explicite, ex. un portrait en ``min(38vw, 66vh)``) ; sinon pleine
#: largeur de la cellule (média en ``width="100%"`` — le cas ``hero_split``).
_WRAP_FIT = Style(
    "position: relative; width: fit-content; max-width: 100%; "
    "margin-left: auto; margin-right: auto;",
    "pa_ai_marked",
)
_WRAP_FILL = Style(
    "position: relative; width: 100%;",
    "pa_ai_marked",
)

#: La pastille DD-35 : zinc-500 (113,113,122) à 0.35 — la convention que le
#: gate sumvadis vérifie au pixel près ; ne pas « améliorer » ces valeurs.
_CHIP_CSS = (
    "position: absolute; right: 0.6em; z-index: 10; "
    "pointer-events: none; background: rgba(113, 113, 122, 0.35); "
    "color: #FFFFFF; border-radius: 999px; padding: 0.1em 0.7em; "
    "font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; "
    "font-size: clamp(11px, 1.05vw, 22px); line-height: 1.7;"
)
_CHIP_BOTTOM = Style(_CHIP_CSS + " bottom: 0.6em;", "pa_ai_mark")
#: Haut-droite UNIQUEMENT quand le bord bas appartient aux contrôles vidéo
#: natifs — même réserve que le composant sumvadis.
_CHIP_TOP = Style(_CHIP_CSS + " top: 0.6em;", "pa_ai_mark")


@contextmanager
def ai_marked(marked: bool = True, label: str = "AI", fit: bool = True,
              top: bool = False):
    """Enveloppe le rendu d'un média et y superpose la pastille « ✦ AI ».

    :param marked: le drapeau de données du média (``ai_generated``). Faux =
        aucun conteneur ajouté — le passage du drapeau est systématique, c'est
        lui qui décide, jamais le bloc.
    :param label: libellé de la pastille (« AI » ; « IA »/« KI » si un deck
        traduit venait à exister — mêmes libellés que l'i18n sumvadis).
    :param fit: épouser la largeur du média (défaut) ou remplir la cellule
        (média rendu en ``width="100%"``).
    :param top: pastille en HAUT-droite — seulement quand le bord bas porte
        les contrôles vidéo natifs.
    """
    if not marked:
        yield
        return
    with st_block(_WRAP_FIT if fit else _WRAP_FILL):
        yield
        st_write(_CHIP_TOP if top else _CHIP_BOTTOM, f"✦ {label}", tag=t.div)
