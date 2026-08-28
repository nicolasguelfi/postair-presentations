"""Poster: the survey part opens with one single full-frame image.

SPEAKER NOTES:
No speech needed — let the image land. One sentence to pivot: "Time to answer
the question of the day: we measure YOUR postures, live, all together."
Nothing on this slide reveals the mechanics; the how-to comes next.
"""
# @guideline: postair-minimal

from custom.config import IS_EDITABLE
from custom.styles import Styles as s
from custom.visuals import is_synthetic
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.ai_mark import dd35_overlay


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt


bs = BlockStyles

_MARKER = {"en": "The Survey — poster", "fr": "Le Sondage — affiche"}
_TITLE = {"en": ("The ", (s.project.titles.keyword, "Survey")), "fr": ("Le ", (s.project.titles.keyword, "Sondage"))}
_LABEL = {"en": "The Survey", "fr": "Le Sondage"}
_TIP_TITLE = {"en": "Next 30 minutes", "fr": "Les 30 prochaines minutes"}
_TIP = [
    ({"en": "Now", "fr": "Maintenant"},
     {"en": ("You answer the POSTAIR survey on your phone or laptop — "
             "anonymous, 15-20 minutes."), "fr": "Vous répondez au sondage POSTAIR sur votre téléphone ou votre ordinateur — anonyme, 15-20 minutes."}),
    ({"en": "Then", "fr": "Ensuite"},
     {"en": ("We project the live results of THIS room and discover the "
             "cohort's postures together."), "fr": "Nous projetons les résultats en direct de CETTE salle et découvrons ensemble les postures de la cohorte."}),
    ({"en": "Finally", "fr": "Enfin"},
     {"en": "We debate the most divisive questions of your cohort.", "fr": "Nous débattons des questions les plus clivantes de votre cohorte."}),
]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_center):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                # Rétrogradé "+1" (ss12) : la partie 1 est ancrée par
                # bck_axes_radar (« Getting started »), le poster n'ouvre
                # plus une partie à lui seul.
                with st_zoom(160):
                    st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="+1", label=T(_LABEL, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(T(h, lang), T(d, lang)) for h, d in _TIP],
                )
        st_space("v", "5vh")
        st_image(s.project.cards.media_center, width="66%",
            editable=IS_EDITABLE, name="survey_poster",
            alt="Papercut poster: a giant nine-spoke paper radar with a huge question "
                "mark at its centre, surrounded by a cheerful crowd of paper silhouettes",
            overlay=dd35_overlay(is_synthetic("survey_poster")))
