"""Survey results (image left, big buttons right).

Each big button opens the results dashboard of one day's campaign
(app.sumvadis.ai/present/<code>: room radar, modal posture per axis,
archetype distribution, per-question detail) in a new tab.

SPEAKER NOTES:
The reveal. Open the results page of the day and comment three things:
the most marked axis, the most ambivalent axis, the dominant archetype.
Compare the room with a great figure for a smile. Then use the
per-question detail to pick the debate questions.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from custom.visuals import is_synthetic
from postair_event import DAYS, present_url
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.ai_mark import ai_marked


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    button = s.project.ds.buttons.action_amber
    day = s.project.ds.buttons.action_day


bs = BlockStyles


def build():
    st_marker("Survey results")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "The ", (s.project.titles.keyword, "results"),
                         " of this room", tag=t.div, toc_lvl="+1", label="Results")
            with g.cell():
                st_info_tooltip(
                    title="Reading the dashboard",
                    entries=[
                        ("Room radar", "The average profile of the cohort on the nine axes, "
                         "with optional overlays: nearest archetype, nearest great figure."),
                        ("Postures per axis", "The modal posture and its share (e.g. 'AMB 42%'): "
                         "directional, ambivalent, balanced or detached."),
                        ("Archetypes", "Distribution of the six archetypes across the room."),
                        ("Per-question detail", "Expandable answer distribution for each of the "
                         "54 statements — the source for picking the debate questions."),
                        ("Privacy", "Only aggregates are shown (minimum 5 answers); the page "
                         "refreshes every 4 seconds and can export a room report."),
                        ("Caution", "The page has no authentication — do not share its URL "
                         "before the session."),
                    ],
                )
        st_space("v", "1vh")
        with st_grid(cols="55% 45%", gap="1.5vw",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                with ai_marked(is_synthetic("survey_results_reveal"), fit=False):
                    st_image(s.project.cards.media_center, width="100%", editable=False, name="survey_results_reveal",
                             alt="Papercut theatre curtain opening on a bright stage revealing a "
                                 "large colorful paper radar chart under spotlights and confetti")
            with g.cell():
                for label, code in DAYS:
                    # La date passe à la ligne, en dessous de l'action : c'est
                    # l'action qu'on lit, c'est la date qu'on vérifie.
                    st_write(bs.button, "Open the results", (bs.day, label),
                             tag=t.div, link=present_url(code), no_link_decor=True)
