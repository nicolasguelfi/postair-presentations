"""Survey results (image left, big buttons right).

Each big button opens the results dashboard of one day's campaign
(app.sumvadis.ai/present/<code>: room radar, modal posture per axis,
archetype distribution, per-question detail) in a new tab.

SPEAKER NOTES:
The reveal, and the longest single moment of the sequence — about ten
minutes. Open the results page of the day and comment three things, in this
order: the most marked axis, the most ambivalent axis, the dominant
archetype. Compare the room with a great historical figure — it always gets
a laugh, and it plants the debate that follows. Keep the per-question detail
open at the end: it is where the divisive questions come from.
If the network fails, the rehearsal screenshots are the fallback; announce
them as such rather than pretending they are live.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from custom.visuals import is_synthetic
from postair_event import DAYS, present_url
from postair_i18n import ui
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.ai_mark import dd35_overlay


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    button = s.project.ds.buttons.action_amber
    day = s.project.ds.buttons.action_day


bs = BlockStyles

#: Les libellés de jour (``DAYS``) restent hors feuille.
_MARKER = {"en": "Survey results"}
_TITLE = {"en": ("The ", (s.project.titles.keyword, "results"), " of this room")}
_LABEL = {"en": "Results"}
_BUTTON = {"en": "Open the results"}
_TIP_TITLE = {"en": "Reading the dashboard"}
#: Têtes « Room radar », « Per-question detail », « What to comment »,
#: « Fallback » : lexique (partagées avec la slide des résultats de la salle).
_TIP_RADAR = {"en": ("The average profile of the cohort on the nine axes, "
                     "with optional overlays: nearest archetype, nearest great figure.")}
_TIP_POSTURES = ({"en": "Postures per axis"},
                 {"en": ("The modal posture and its share (e.g. 'AMB 42%'): "
                         "directional, ambivalent, balanced or detached.")})
_TIP_ARCHETYPES = ({"en": "Archetypes"},
                   {"en": "Distribution of the six archetypes across the room."})
_TIP_DETAIL = {"en": ("Expandable answer distribution for each of the "
                      "54 statements — the source for picking the debate questions.")}
_TIP_PRIVACY = ({"en": "Privacy"},
                {"en": ("Only aggregates are shown (minimum 5 answers); the page "
                        "refreshes every 4 seconds and can export a room report.")})
_TIP_CAUTION = ({"en": "Caution"},
                {"en": ("The page has no authentication — do not share its URL "
                        "before the session.")})
# Repris de bck_results_room, écartée du parcours le 2026-08-24 (elle ouvrait
# les MÊMES /present/<code>) : ces deux conseils n'existaient que là.
_TIP_COMMENT = {"en": ("Three things, in this order: the most marked axis, "
                       "the most ambivalent axis, the dominant archetype. Resist the urge to "
                       "comment all nine — the room stops listening after three.")}
_TIP_FALLBACK = {"en": ("If the network fails, use the rehearsal screenshots and say "
                        "clearly that they are from the rehearsal, not from this room.")}


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="+1", label=T(_LABEL, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[
                        (ui("room_radar", lang), T(_TIP_RADAR, lang)),
                        (T(_TIP_POSTURES[0], lang), T(_TIP_POSTURES[1], lang)),
                        (T(_TIP_ARCHETYPES[0], lang), T(_TIP_ARCHETYPES[1], lang)),
                        (ui("per_question_detail", lang), T(_TIP_DETAIL, lang)),
                        (T(_TIP_PRIVACY[0], lang), T(_TIP_PRIVACY[1], lang)),
                        (T(_TIP_CAUTION[0], lang), T(_TIP_CAUTION[1], lang)),
                        (ui("what_to_comment", lang), T(_TIP_COMMENT, lang)),
                        (ui("fallback", lang), T(_TIP_FALLBACK, lang)),
                    ],
                )
        st_space("v", "1vh")
        with st_grid(cols="55% 45%", gap="1.5vw",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_image(s.project.cards.media_center, width="100%", editable=True, name="survey_results_reveal",
                         alt="Papercut theatre curtain opening on a bright stage revealing a "
                             "large colorful paper radar chart under spotlights and confetti",
                    overlay=dd35_overlay(is_synthetic("survey_results_reveal")))
            with g.cell():
                for label, code in DAYS:
                    # La date passe à la ligne, en dessous de l'action : c'est
                    # l'action qu'on lit, c'est la date qu'on vérifie.
                    st_write(bs.button, T(_BUTTON, lang), (bs.day, label),
                             tag=t.div, link=present_url(code), no_link_decor=True)
