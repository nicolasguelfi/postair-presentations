"""Affichage POSTAIR — l'échelle amphi/mobile partagée par tous les books.

Constat NG (2026-08-12, captures iPhone) : les books calibrent le texte pour
l'amphithéâtre (``base_pt_desktop=30``, ×1,67 du défaut) mais les facteurs de
rétrécissement tablette/mobile de la librairie restaient ceux d'un document
18pt — titres à ~75 px CSS sur téléphone, pendant que les images (%/vw)
suivaient l'écran.

La réponse est à DEUX étages, et celui-ci n'est que le premier :

1. ``SCALE`` (ici) — facteurs par palier de la librairie (``@media``
   1024/480 px), ramenés à 0,70/0,55.
2. Les **plafonds ``vw``** posés sur les jetons de texte du design system
   (``postair_dark``, NG 2026-08-12) — c'est EUX qui rendent le texte
   proportionnel en continu à la largeur : ``min(7vw, calc(...))`` sur un
   titre ne mord qu'en dessous de ~1400 px et laisse la projection intacte.

Un dispositif de profils auto-zoom (zoom 60 appliqué par détection d'appareil)
a été essayé le même jour et RETIRÉ : le zoom CSS se cumulait avec les
plafonds (double rétrécissement), son rendu est peu fiable sur iOS, et le
sélecteur de la sidebar affichait « Défaut » alors que les valeurs étaient
déjà appliquées — trois confusions pour zéro gain une fois les plafonds posés.
"""

from __future__ import annotations

from streamtex import (
    PageLayout,
    PresentationProfile,
    ScaleConfig,
    SlideBreakDisplayConfig,
    SlideBreakMode,
)
from streamtex.presentation_profile import ViewMode as _ProfileViewMode

#: L'échelle des decks : base amphi 30pt (projection intacte), rétrécissements
#: par palier renforcés — le lissage continu vient des plafonds vw du DS.
SCALE = ScaleConfig(base_pt_desktop=30, tablet_scale=0.70, mobile_scale=0.55)

# ── Le profil d'écran (planche ecran2, NG 2026-09-02) ───────────────────────
#: Les DEUX résolutions de référence du calibrage (règle R-écran de la
#: design-guideline) : le projecteur des séances, et l'écran du portable de
#: l'orateur (mesuré, pas supposé). Toute taille se juge à ces références —
#: la porte ``check_projection.py`` y rend les exports.
PROJECTION_REF = (1920, 1080)
LAPTOP_REF = (1728, 1117)

#: Les RACCOURCIS DE ZOOM du panneau latéral, partagés par les 7 decks
#: paginés (``st_book(presentation_profiles=postair_profiles())``) — le hub
#: ``collection`` (continu) n'en reçoit pas : un profil paginé le
#: basculerait. Le profil actif au démarrage reste « Default », construit
#: par la librairie depuis les réglages du book : le rendu au démarrage ne
#: bouge pas d'un pixel — Default EST le mode de calage et de séance.
#:
#: Renommage NG (2026-09-02) : d'abord livrés « Laptop »/« Salle étroite »,
#: ces profils promettaient un remède de salle qu'ils ne rendent pas — le
#: deck étant entièrement relatif à la fenêtre (vh/vw + plafonds), un zoom
#: CSS rétrécit AUSSI ce qui s'adapte déjà (capture NG : contenu réduit +
#: bande morte ; même mécanique que le double rétrécissement du 2026-08-12).
#: Ils s'assument désormais pour ce qu'ils sont : deux préréglages de zoom
#: nommés, plus rapides que le champ Zoom % manuel, utiles à l'occasion.
#: Une salle en résolution moindre se traite par la porte de projection
#: (``--resolutions``) et le design system, jamais par ces zooms. Les
#: coupures reflètent le réglage commun des 7 books (FULL, 30 vh) pour
#: qu'un changement de profil ne change QUE le zoom.
def postair_profiles() -> list[PresentationProfile]:
    """Les raccourcis de zoom — une liste NEUVE par appel (objets mutables)."""
    _breaks = lambda: SlideBreakDisplayConfig(  # noqa: E731 — fabrique locale
        enabled=True, mode=SlideBreakMode.FULL, before=0, after=30)
    return [
        PresentationProfile(
            name="Zoom 90 %",
            mode=_ProfileViewMode.PAGINATED,
            layout=PageLayout(width=100, zoom=90),
            breaks=_breaks(),
        ),
        PresentationProfile(
            name="Zoom 80 %",
            mode=_ProfileViewMode.PAGINATED,
            layout=PageLayout(width=100, zoom=80),
            breaks=_breaks(),
        ),
    ]
