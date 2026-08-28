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


_MARKER = {"en": "The great figures", "fr": "Les grandes figures"}
_TITLE = {"en": ("The great figures — the ", (s.project.titles.keyword, "explorer")), "fr": ("Les grandes figures — l'", (s.project.titles.keyword, "explorateur"))}
_MESSAGES = [
    ({"en": "Beyond your report", "fr": "Au-delà du rapport"},
     {"en": ("The explorer opens the whole gallery: archetypes and great "
             "figures, scored by the same engine that just scored you."), "fr": "L'explorateur ouvre toute la galerie : archétypes et grandes figures, évalués par le même moteur qui vient de vous évaluer."}),
    ({"en": "The gesture: pick one", "fr": "Le geste : en choisir une"},
     {"en": ("Choose a figure and see where it stands on the nine axes — then "
             "find your own distance to it."), "fr": "Choisissez une figure et voyez où elle se situe sur les neuf axes — puis mesurez la distance qui vous en sépare."}),
]
_TIP_TITLE = {"en": "The figures pages", "fr": "Les pages des figures"}
#: La première tête vient du lexique (``same_instrument``, partagée avec les
#: vidéos de figures).
_TIP_SAME = {"en": ("Every figure is scored on the same 54 statements you "
                    "answered, from documented positions in their work."), "fr": "Chaque figure est évaluée sur les 54 mêmes énoncés que vous, d'après des positions documentées dans son œuvre."}
_TIP_DOORWAY = ({"en": "Doorway to the debates", "fr": "Porte d'entrée vers les débats"},
                {"en": ("The afternoon's debate deck draws its figures, quotes "
                        "and references from these same dossiers."), "fr": "Le deck de débat de l'après-midi tire ses figures, ses citations et ses références de ces mêmes dossiers."})


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
