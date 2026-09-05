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
from custom.visuals import is_synthetic
from postair_event import DAYS, live_url
from postair_i18n import ui
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.ai_mark import dd35_overlay


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    button = s.project.ds.buttons.action_big
    day = s.project.ds.buttons.action_day


bs = BlockStyles

#: Les libellés de jour (``DAYS``) restent hors feuille.
_MARKER = {"en": "Live monitoring", "fr": "Suivi en direct"}
_TITLE = {"en": ((s.project.titles.keyword, "Live"), " — the room is answering"), "fr": ((s.project.titles.keyword, "En direct"), " — la salle répond")}
_BUTTON = {"en": "Open live monitoring", "fr": "Ouvrir le suivi en direct"}
#: Le titre du tooltip (« Operator checklist ») vient du lexique.
_TIP = [
    ({"en": "The counter", "fr": "Le compteur"},
     {"en": ("The live page shows the number of submitted answers, "
             "refreshed every 2 seconds, plus the session timer."), "fr": "La page en direct affiche le nombre de réponses envoyées, rafraîchi toutes les 2 secondes, plus le chronomètre de la séance."}),
    ({"en": "First reflex: PAUSE", "fr": "Premier réflexe : PAUSE"},
     {"en": ("Any incident → pause the campaign from the "
             "admin console, then diagnose. Resuming is instant."), "fr": "Tout incident → mettez la campagne en pause depuis la console d'administration, puis diagnostiquez. La reprise est instantanée."}),
    ({"en": "Anti-bot", "fr": "Anti-bot"},
     {"en": ("If more than ~5% of submissions fail in the first two "
             "minutes, toggle the Turnstile shield from the admin console."), "fr": "Si plus de ~5 % des envois échouent dans les deux premières minutes, basculez le bouclier Turnstile depuis la console d'administration."}),
    ({"en": "Steering", "fr": "Pilotage"},
     {"en": ("Campaigns are managed in the sumvadis admin console "
             "(operator key): pause / resume / close / reopen per day."), "fr": "Les campagnes se pilotent dans la console d'administration sumvadis (clé opérateur) : pause / reprise / clôture / réouverture, par jour."}),
]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with st_zoom(150), g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=ui("operator_checklist", lang),
                    entries=[(T(h, lang), T(d, lang)) for h, d in _TIP],
                )
        st_space("v",s.project.spacing.title_gap)
        with st_grid(cols="55% 45%", gap="1.5vw",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_image(s.project.cards.media_center, width="100%", editable=True, name="survey_live_room",
                         alt="Papercut amphitheatre: rows of paper silhouettes holding glowing "
                             "phones like lanterns while answering the survey",
                    overlay=dd35_overlay(is_synthetic("survey_live_room")))
            with g.cell():
                for label, code in DAYS:
                    # La date passe à la ligne, en dessous de l'action : c'est
                    # l'action qu'on lit, c'est la date qu'on vérifie.
                    st_write(bs.button, T(_BUTTON, lang), (bs.day, label),
                             tag=t.div, link=live_url(code), no_link_decor=True)
