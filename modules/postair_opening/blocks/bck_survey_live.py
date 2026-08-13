"""Live monitoring during the answering phase (image left, big buttons right).

Each big button opens the live monitoring page of one day's campaign
(app.sumvadis.ai/live/<code>: real-time counter, session timer) in a new tab.
The presenter clicks the button of the current day.

SPEAKER NOTES:
While the room answers (≈18'), project the live counter. Walk the aisles,
answer raised hands. Announce "5 minutes left", then close. If anything
goes wrong: PAUSE the campaign first (admin console), diagnose after.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from custom.visuals import is_synthetic, managed_media_width
from postair_event import DAYS, live_url
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.ai_mark import ai_marked


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    button = s.project.ds.buttons.action_big
    day = s.project.ds.buttons.action_day


bs = BlockStyles


def build():
    st_marker("Live monitoring")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, (s.project.titles.keyword, "Live"), " — the room is answering",
                         tag=t.div, toc_lvl="+1", label="Live monitoring")
            with g.cell():
                st_info_tooltip(
                    title="Operator checklist",
                    entries=[
                        ("The counter", "The live page shows the number of submitted answers, "
                         "refreshed every 2 seconds, plus the session timer."),
                        ("First reflex: PAUSE", "Any incident → pause the campaign from the "
                         "admin console, then diagnose. Resuming is instant."),
                        ("Anti-bot", "If more than ~5% of submissions fail in the first two "
                         "minutes, toggle the Turnstile shield from the admin console."),
                        ("Steering", "Campaigns are managed in the sumvadis admin console "
                         "(operator key): pause / resume / close / reopen per day."),
                    ],
                )
        st_space("v", "1vh")
        with st_grid(cols="55% 45%", gap="1.5vw",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                with ai_marked(is_synthetic("survey_live_room"), fit=False,
                               media_width=managed_media_width("survey_live_room")):
                    st_image(s.project.cards.media_center, width="100%", editable=False, name="survey_live_room",
                             alt="Papercut amphitheatre: rows of paper silhouettes holding glowing "
                                 "phones like lanterns while answering the survey")
            with g.cell():
                for label, code in DAYS:
                    # La date passe à la ligne, en dessous de l'action : c'est
                    # l'action qu'on lit, c'est la date qu'on vérifie.
                    st_write(bs.button, "Open live monitoring", (bs.day, label),
                             tag=t.div, link=live_url(code), no_link_decor=True)
