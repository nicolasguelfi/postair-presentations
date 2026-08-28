"""The great figures — the explorer — écran 18-explorateur.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_figures) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from postair_i18n import ui
from postair_lang import T, TF
from streamtex import *


_MARKER = {"en": "The great figures"}
_TITLE = {"en": ("The great figures — the ", (s.project.titles.keyword, "explorer"))}
_MESSAGES = [
    ({"en": "Beyond your report"},
     {"en": ("The explorer opens the whole gallery: archetypes and great "
             "figures, scored by the same engine that just scored you.")}),
    ({"en": "The gesture: pick one"},
     {"en": ("Choose a figure and see where it stands on the nine axes — then "
             "find your own distance to it.")}),
]
_TIP_TITLE = {"en": "The figures pages"}
#: La première tête vient du lexique (``same_instrument``, partagée avec les
#: vidéos de figures).
_TIP_SAME = {"en": ("Every figure is scored on the same 54 statements you "
                    "answered, from documented positions in their work.")}
_TIP_DOORWAY = ({"en": "Doorway to the debates"},
                {"en": ("The afternoon's debate deck draws its figures, quotes "
                        "and references from these same dossiers.")})


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    screen_slide(
        TF(_TITLE, lang),
        "18-explorateur",
        "Mobile screen of the archetype and great figures explorer, dark theme",
        [(T(h, lang), T(d, lang)) for h, d in _MESSAGES],
        toc_label=T(_MARKER, lang),
        tooltip=(T(_TIP_TITLE, lang),
                 [(ui("same_instrument", lang), T(_TIP_SAME, lang)),
                  (T(_TIP_DOORWAY[0], lang), T(_TIP_DOORWAY[1], lang))]),
        # La capture 18 est une page DÉFILANTE entière (1134×8796) — on ne
        # garde que le premier écran. crop=(haut, droite, bas, gauche).
        crop=(0, 0, 67, 0),
        zoomImage=100,
        zoomText=100,
        lang=lang
    )
