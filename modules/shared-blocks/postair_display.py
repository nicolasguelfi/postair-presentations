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

from streamtex import ScaleConfig

#: L'échelle des decks : base amphi 30pt (projection intacte), rétrécissements
#: par palier renforcés — le lissage continu vient des plafonds vw du DS.
SCALE = ScaleConfig(base_pt_desktop=30, tablet_scale=0.70, mobile_scale=0.55)
