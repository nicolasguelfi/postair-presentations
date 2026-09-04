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

from streamtex import MediaOverlay, st_block, st_write
from streamtex.enums import Tags as t
from streamtex.styles import Style

#: La convention DD-35 à l'échelle amphi, passée au slot natif de ``st_image``
#: (0.7.23). Le libellé et la géométrie de coin viennent de ``MediaOverlay`` ;
#: ce CSS surcharge le style par défaut de la librairie en cascade.
DD35_CSS = (
    "background: rgba(113, 113, 122, 0.35); color: #FFFFFF; "
    "border-radius: 999px; padding: 0.1em 0.7em; font-weight: 700; "
    "text-transform: uppercase; letter-spacing: 0.08em; "
    "font-size: clamp(11px, 1.05vw, 22px); line-height: 1.7;"
)


def dd35_overlay(marked: bool = True, label: str = "AI",
                 position: str = "bottom-right",
                 scale: float = 1.0) -> MediaOverlay | None:
    """Le ``MediaOverlay`` DD-35 pour ``st_image(overlay=…)`` — ``None`` sinon.

    Le drapeau de données décide (``ai_generated``/``is_synthetic``), jamais le
    bloc. Depuis la 0.7.23 la pastille est rendue DANS la boîte de l'image
    (zoom d'éditeur compris, barre « Edit Image » exclue) : plus aucun calcul
    de décalage ni de variante haute côté consommateur. L'ancre est TOUJOURS
    le coin de la boîte de l'image (bas-droite par défaut).

    :param scale: facteur de taille de la pastille (NG 2026-09-04) — la base
        ``clamp`` est calibrée pour un hero d'amphi ; sur un petit média
        (mascotte à 6vw…) elle mange l'image : ``scale=0.6`` la ramène à
        l'échelle. Ne touche que la TAILLE — couleurs et alpha restent la
        convention DD-35 vérifiée par le gate sumvadis.
    """
    if not marked:
        return None
    css = DD35_CSS
    if scale != 1.0:
        css = css.replace(
            "font-size: clamp(11px, 1.05vw, 22px);",
            f"font-size: calc(clamp(11px, 1.05vw, 22px) * {scale});")
    return MediaOverlay(text=f"✦ {label}", position=position, css=css,
                        aria_label="AI-generated media (art. 50 EU AI Act "
                                   "disclosure)")

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
              top: bool = False, media_width: str | None = None):
    """Enveloppe le rendu d'un média et y superpose la pastille « ✦ AI ».

    Depuis streamtex 0.7.23, réservé aux VIDÉOS (``st.video`` est une iframe,
    le slot natif ne la couvre pas — phase 2 du plan) : toute IMAGE passe par
    ``st_image(overlay=dd35_overlay(...))``.

    :param marked: le drapeau de données du média (``ai_generated``). Faux =
        aucun conteneur ajouté — le passage du drapeau est systématique, c'est
        lui qui décide, jamais le bloc.
    :param label: libellé de la pastille (« AI » ; « IA »/« KI » si un deck
        traduit venait à exister — mêmes libellés que l'i18n sumvadis).
    :param fit: épouser la largeur du média (défaut) ou remplir la cellule
        (média rendu en ``width="100%"``).
    :param top: pastille en HAUT-droite — seulement quand le bord bas porte
        les contrôles vidéo natifs.
    :param media_width: largeur CSS du média AFFICHÉ quand elle diffère de
        celle du conteneur (``display_zoom`` d'un sidecar → ``"80%"``, ou la
        largeur passée au bloc). ``st_image`` calcule sa réduction PAR RAPPORT
        au conteneur : rétrécir le conteneur la doublerait — on décale donc la
        pastille de la marge, jamais le conteneur (constaté 2026-08-13 sur la
        roue des axes, pastille posée hors de l'image réduite à 80 %).
    """
    if not marked:
        yield
        return
    chip = _CHIP_TOP if top else _CHIP_BOTTOM
    if media_width:
        # Média centré dans le conteneur : la marge de droite vaut la moitié
        # de la différence des largeurs.
        chip = Style(
            str(chip).replace(
                "right: 0.6em;",
                f"right: calc((100% - {media_width}) / 2 + 0.6em);"),
            chip.style_id,
        )
    # Géométrie constatée (2026-08-13) : ``st_block`` rend un div de hauteur
    # NULLE placé APRÈS son contenu — la pastille « bas » flotte donc au-dessus
    # de la ligne qui suit le média, pile sur son coin inférieur. Pour ``top``
    # (mode éditeur : la barre « Edit Image » s'intercale sous l'image),
    # l'ancre s'émet AVANT le média : la pastille descend de 0.6em sous cette
    # ligne et se pose sur le coin SUPÉRIEUR de l'image, au-dessus de la barre.
    if top:
        with st_block(_WRAP_FIT if fit else _WRAP_FILL):
            st_write(chip, f"✦ {label}", tag=t.div)
        yield
    else:
        with st_block(_WRAP_FIT if fit else _WRAP_FILL):
            yield
            st_write(chip, f"✦ {label}", tag=t.div)
