"""Meet the figures 1/2 — le duo vidéo, la GAUCHE se lance (Platon).

Première des deux pages jumelles du duo figures (gabarit
``custom/media_duo.py``, NG 2026-08-22) : Platon à gauche, Ada Lovelace à
droite — un homme, une femme, connus de l'assemblée (Socrate n'est pas au
gel des 51 figures ; Platon est son plus proche voisin, NG 2026-08-22).
Vidéos EMBARQUÉES comme les clips mascottes (matérialisées par sync_media,
exception assumée pour ces deux seules figures — « tout doit marcher tout
de suite »). Le choix des deux figures vit dans ``figure_duo()``.

SPEAKER NOTES:
Same gesture as the mascots: let Platon speak, then arrow right for Ada
Lovelace. One sentence: every great figure's page carries its presentation
video — same instrument, same nine axes, and this afternoon they argue.
"""
# @guideline: postair-minimal

from custom.media_duo import FIGURES_TITLE, figure_duo, media_duo_slide
from postair_i18n import ui
from postair_lang import T, TF


_MARKER = {"en": "Figure videos", "fr": "Vidéos des figures"}
_TIP_TITLE = {"en": "The figure videos", "fr": "Vidéos des figures"}
_TIP = [
    ({"en": "In the app", "fr": "Dans l'application"},
     {"en": ("Every great figure's page carries a short presentation video — "
             "click the portrait to play it."), "fr": "Chaque page de grande figure a sa courte vidéo de présentation — cliquez sur le portrait pour la lancer."}),
    ({"en": "Same instrument", "fr": "Le même instrument"},
     {"en": ("The figures are scored on the same 54 statements you answered, "
             "from documented positions in their work."), "fr": "Les figures sont évaluées sur les 54 mêmes énoncés que vous, d'après des positions documentées dans leur œuvre."}),
    ({"en": "AI-made, sourced", "fr": "Faites par IA, sourcées"},
     {"en": ("The videos are generative productions grounded in each figure's "
             "dossier — arguments to debate, never facts about a person."), "fr": "Les vidéos sont des productions génératives ancrées dans le dossier de chaque figure — des arguments à débattre, jamais des faits sur une personne."}),
]


_MARKER = {"en": "Figure videos", "fr": "Vidéos des figures"}
_TIP_TITLE = {"en": "The figure videos", "fr": "Vidéos des figures"}
#: Les deux premières têtes viennent du lexique (``in_the_app`` et
#: ``same_instrument``, partagées avec d'autres slides) ; la troisième est
#: propre à cette slide.
_TIP_IN_APP = {"en": ("Every great figure's page carries a short presentation "
                      "video — click the portrait to play it."), "fr": "Chaque page de grande figure a sa courte vidéo de présentation — cliquez sur le portrait pour la lancer."}
_TIP_SAME = {"en": ("The figures are scored on the same 54 statements you "
                    "answered, from documented positions in their work."), "fr": "Les figures sont évaluées sur les 54 mêmes énoncés que vous, d'après des positions documentées dans leur œuvre."}
_TIP_AI = ({"en": "AI-made, sourced", "fr": "Faites par IA, sourcées"},
           {"en": ("The videos are generative productions grounded in each "
                   "figure's dossier — arguments to debate, never facts about "
                   "a person."), "fr": "Les vidéos sont des productions génératives ancrées dans le dossier de chaque figure — des arguments à débattre, jamais des faits sur une personne."})


def build(lang: str = "en", **_):
    media_duo_slide(
        TF(FIGURES_TITLE, lang),
        figure_duo(lang), "left",
        marker=T(_MARKER, lang),
        toc_label=T(_MARKER, lang),
        tooltip=(T(_TIP_TITLE, lang),
                 [(ui("in_the_app", lang), T(_TIP_IN_APP, lang)),
                  (ui("same_instrument", lang), T(_TIP_SAME, lang)),
                  (T(_TIP_AI[0], lang), T(_TIP_AI[1], lang))]),
        stage_vh=70,
        lang=lang,
    )
