"""Open the room's results — the door to /present, just before the pivot.

Added on NG's request (2026-08-30): the debates deck must let the speaker
open the results dashboard of the day WITHOUT leaving for the survey deck —
the divisive axes are read there, and the debate that follows starts from
them. Copy of the survey deck's ``bck_survey_results`` (composition, texts
and image), decided over a shared block: the deck stays autonomous, and the
room recognises the curtain it saw half an hour earlier.

Each big button opens the results dashboard of one day's campaign
(app.sumvadis.ai/present/<code>) in a new tab — links, no widget, so the
slide survives the static export (R-live).

The curtain is the same managed illustration as in the survey deck, copied
with its sidecar under ``static/images/managed/`` (the repo's assumed
exception: illustrations produced for these presentations are versioned and
never go to the CDN). The AI mark is decided by the sidecar, never by hand.

SPEAKER NOTES:
Thirty seconds, no more — the results were commented in the previous deck.
Open the day's page, go straight to « What divides the room », and read the
two or three axes you are about to open, out loud. Then turn the page: the
pivot names the rules for taking the floor, and the first axis begins.
If the network fails, the rehearsal screenshots of the survey deck are the
fallback; announce them as such rather than pretending they are live.
"""
# @guideline: postair-minimal

import json
from pathlib import Path

from custom.styles import Styles as s
from postair_event import DAYS, present_url
from postair_i18n import ui
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.ai_mark import dd35_overlay

_MANAGED = Path(__file__).parent.parent / "static" / "images" / "managed"
#: Le rideau papercut — copie de l'image managée de survey, avec son sidecar.
_CURTAIN = "images/managed/survey_results_reveal.webp"


def _is_synthetic(name: str) -> bool:
    """Le drapeau du sidecar de l'image — la donnée décide ; sans sidecar,
    marquer est le défaut sûr (l'absence de marque doit se mériter)."""
    sidecar = _MANAGED / f"{name}.json"
    try:
        return json.loads(sidecar.read_text(encoding="utf-8")).get("source_type") == "ai_generated"
    except (OSError, ValueError):
        return True


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    button = s.project.ds.buttons.action_amber
    day = s.project.ds.buttons.action_day


bs = BlockStyles

# ── Le texte projeté (règle R-i18n) — feuilles reprises de bck_survey_results.
#: Les libellés de jour (``DAYS``) restent hors feuille.
_MARKER = {"en": "The results", "fr": "Les résultats"}
_TITLE = {"en": ("Where does ", (s.project.titles.keyword, "this room"), " split?"), "fr": ("Où ", (s.project.titles.keyword, "cette salle"), " se divise-t-elle ?")}
_LABEL = {"en": "Results", "fr": "Résultats"}
_BUTTON = {"en": "Open the results", "fr": "Ouvrir les résultats"}
_TIP_TITLE = {"en": "Reading the dashboard", "fr": "Lire le tableau de bord"}
_TIP_RADAR = {"en": ("The average profile of the cohort on the nine axes, "
                     "with optional overlays: nearest archetype, nearest great figure."), "fr": "Le profil moyen de la cohorte sur les neuf axes, avec des calques optionnels : archétype le plus proche, grande figure la plus proche."}
_TIP_POSTURES = ({"en": "Postures per axis", "fr": "Postures par axe"},
                 {"en": ("The modal posture and its share (e.g. 'AMB 42%'): "
                         "directional, ambivalent, balanced or detached."), "fr": "La posture modale et sa part (p. ex. « AMB 42 % ») : tranchée, ambivalente, équilibrée ou détachée."})
_TIP_ARCHETYPES = ({"en": "Archetypes", "fr": "Archétypes"},
                   {"en": "Distribution of the six archetypes across the room.", "fr": "Répartition des six archétypes dans la salle."})
_TIP_DETAIL = {"en": ("Expandable answer distribution for each of the "
                      "54 statements — the source for picking the debate questions."), "fr": "Distribution des réponses, dépliable, pour chacun des 54 énoncés — la source pour choisir les questions du débat."}
_TIP_DIVIDES = ({"en": "What divides the room", "fr": "Ce qui divise la salle"},
                {"en": ("The slideshow view that ranks the most divisive statements — "
                        "this view IS the menu of the debates: read the two or three "
                        "axes you will open from it."), "fr": "La vue du diaporama qui classe les énoncés les plus clivants — cette vue EST le menu des débats : lisez-y les deux ou trois axes que vous allez ouvrir."})
_TIP_PRIVACY = ({"en": "Privacy", "fr": "Vie privée"},
                {"en": ("Only aggregates are shown (minimum 5 answers); the page "
                        "refreshes every 4 seconds and can export a room report."), "fr": "Seuls des agrégats sont affichés (minimum 5 réponses) ; la page se rafraîchit toutes les 4 secondes et peut exporter un rapport de la salle."})
_TIP_CAUTION = ({"en": "Caution", "fr": "Attention"},
                {"en": ("The page has no authentication — do not share its URL "
                        "before the session."), "fr": "La page n'a aucune authentification — ne partagez pas son URL avant la séance."})
_TIP_FALLBACK = {"en": ("If the network fails, use the rehearsal screenshots of the survey "
                        "deck and say clearly that they are from the rehearsal, not from this room."), "fr": "Si le réseau tombe, utilisez les captures de la répétition du deck du sondage et dites clairement qu'elles viennent de la répétition, pas de cette salle."}


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
                        (T(_TIP_DIVIDES[0], lang), T(_TIP_DIVIDES[1], lang)),
                        (T(_TIP_PRIVACY[0], lang), T(_TIP_PRIVACY[1], lang)),
                        (T(_TIP_CAUTION[0], lang), T(_TIP_CAUTION[1], lang)),
                        (ui("fallback", lang), T(_TIP_FALLBACK, lang)),
                    ],
                )
        st_space("v", "1vh")
        with st_grid(cols="55% 45%", gap="1.5vw",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_image(s.project.cards.media_center, width="100%", uri=_CURTAIN,
                         alt="Papercut theatre curtain opening on a bright stage revealing a "
                             "large colorful paper radar chart under spotlights and confetti",
                         overlay=dd35_overlay(_is_synthetic("survey_results_reveal")))
            with g.cell():
                for label, code in DAYS:
                    # La date passe à la ligne, en dessous de l'action : c'est
                    # l'action qu'on lit, c'est la date qu'on vérifie.
                    st_write(bs.button, T(_BUTTON, lang), (bs.day, label),
                             tag=t.div, link=present_url(code), no_link_decor=True)
