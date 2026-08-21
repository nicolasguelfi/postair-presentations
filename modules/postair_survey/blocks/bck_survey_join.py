"""Join the survey — one slide, and a day chosen live by the speaker.

Data-driven from postair_event.py (three daily sumvadis campaigns).

ONE slide, not one per day (NG 2026-08-03). Three sub-slides put the three
access codes one arrow-key apart from each other: a student on Monday only had
to press the right arrow to read Tuesday's code, and a code seen by a room that
must not use it is a code that can pollute another day's campaign. The day is
therefore chosen by the speaker, in the subtitle, and only the chosen day is on
screen.

The selector opens on ``Survey Date``, which shows the SHAPE of the slide — the
frame where the QR will be, a code masked behind question marks — and nothing
usable. That state is not a placeholder waiting to be replaced: it is the state
the slide is in while the speaker explains what is about to happen, and the one
it should be left in whenever the deck is open outside a session.

The last selector entry, ``Custom code…`` (NG 2026-08-21), opens a free field:
the speaker types ANY campaign code — one created that very morning — and the
slide shows it exactly like a declared day, QR included. The QR is **generated
locally** (segno, pure Python, cached in the temp directory): no network call
during the session, nothing written under ``static/``. A non-alphanumeric
entry keeps the slide masked — the code goes into a URL and a filename.
Limite assumée : dans l'export HTML statique, la slide est figée à l'état
masqué (les widgets ne vivent que dans le mode Streamlit de l'orateur).

SPEAKER NOTES:
The critical moment — keep the slide up until the counter stabilises. Pick the
day in the selector BEFORE you turn to the room; the slide shows nothing usable
until you do. For an ad-hoc campaign, pick « Custom code… » and type the code —
the QR appears as you type; check it on YOUR phone before sending the room to
it. Scan the QR or type the short URL, then the code of the day. Anonymous,
20-40 minutes, phone OR laptop. No device? Pair up. If the venue wifi
struggles, switch to 4G.
"""
# @guideline: postair-minimal

import tempfile
from pathlib import Path

import segno
from custom.styles import Styles as s
from postair_event import DAYS, NO_DAY, join_url
from shared_widgets import st_info_tooltip, st_stage_code_input, st_stage_selector
from streamtex import *
from streamtex.enums import Tags as t

#: Clé de widget STABLE — une clé engendrée changerait à chaque rerun et
#: remettrait le sélecteur à zéro sous la main de l'orateur.
_SELECTOR_KEY = "survey_join_day"
_CODE_KEY = "survey_join_custom_code"

#: L'entrée du sélecteur qui ouvre la saisie libre (NG 2026-08-21) : une
#: campagne créée le matin même se projette sans regel — le QR se GÉNÈRE
#: localement (segno, pur Python), aucun appel réseau pendant la séance.
CUSTOM_DAY = "Custom code…"

#: Les QR générés vivent hors de l'arbre (répertoire temporaire) : rien ne
#: s'écrit sous static/, le conteneur reste byte-identique à son image.
_QR_CACHE = Path(tempfile.gettempdir()) / "postair-qr"

#: Le QR est 20 % plus grand qu'à la conception (NG 2026-08-03) : c'est lui que
#: 1500 téléphones visent, et depuis le dernier rang.
_QR_WIDTH = "min(36vw, 62.4vh)"

#: L'URL est affichée avec sa barre oblique finale : sans elle, le code tapé
#: juste après se colle au chemin et la page ne s'ouvre pas.
_JOIN_URL_SHOWN = "https://app.sumvadis.ai/s/"


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    day = s.project.titles.subtitle + s.center_txt
    url = s.project.ds.stage.url_big
    code = s.project.ds.stage.code_giant
    code_masked = s.project.ds.stage.code_masked
    hint = s.project.body.body + s.center_txt


bs = BlockStyles


def _generated_qr(code: str) -> str:
    """Le chemin ABSOLU du QR généré pour *code* — fabriqué au premier passage.

    Même contenu que les QR gelés (l'URL de campagne ``join_url``), mêmes
    couleurs sombre-sur-blanc avec zone de silence : ce qui change est la
    provenance, pas la scannabilité. Le fichier est mis en cache par code —
    ``st_image`` inline le PNG (moins d'un Ko) en base64, comme tout chemin
    absolu.
    """
    target = _QR_CACHE / f"qr_join_{code}.png"
    if not target.exists():
        _QR_CACHE.mkdir(parents=True, exist_ok=True)
        segno.make(join_url(code), error="m").save(str(target), scale=20, border=2)
    return str(target)


def build():
    st_marker("Join the survey")
    codes = dict(DAYS)
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "Your turn — ", (s.project.titles.keyword, "join the survey"),
                         tag=t.div, toc_lvl="+1", label="Join the survey")
                # Le sélecteur EST le sous-titre : c'est la seule chose qui
                # change d'une séance à l'autre, et la seule à ne pas figer.
                # « Custom code… » ouvre la saisie libre : une campagne créée
                # le matin même se projette sans toucher au code.
                chosen = st_stage_selector([NO_DAY] + [label for label, _c in DAYS]
                                           + [CUSTOM_DAY],
                                           key=_SELECTOR_KEY)
                custom = ""
                if chosen == CUSTOM_DAY:
                    custom = st_stage_code_input(key=_CODE_KEY,
                                                 placeholder="campaign code")
                    # Le code entre dans une URL et un nom de fichier : tout
                    # sauf alphanumérique reste à l'état masqué.
                    if custom and not custom.isalnum():
                        custom = ""
            with g.cell():
                st_info_tooltip(
                    title="Anonymous by design",
                    entries=[
                        ("Your result is yours", "Your personal radar is computed ON your "
                         "device; the server only receives one anonymous record."),
                        ("GDPR", "No account, no email, no tracking; data stays in the EU. "
                         "Only room-level averages are ever projected (minimum 5 answers)."),
                        ("One code per day", "Each session has its own campaign and its own "
                         "code. The slide shows only the day the speaker has selected — the "
                         "other codes are never on screen."),
                        ("No device?", "Pair up with a neighbour — one answer per person "
                         "though: your posture, not a committee's."),
                        ("Network", "If the venue wifi is slow, switch your phone to 4G."),
                        ("Keep your code", "At the end the app gives you a personal code to "
                         "retrieve your result later at app.sumvadis.ai/r."),
                    ],
                )
        # Un espace franc sous la date : il sépare ce que l'orateur manœuvre de
        # ce que la salle doit lire.
        st_space("v", "4vh")
        # Le code projeté : celui du jour choisi (QR gelé) ou celui saisi
        # (QR généré). Vide = état masqué — la slide s'explique sans rien
        # livrer, exactement comme avant la sélection.
        code = codes.get(chosen, custom if chosen == CUSTOM_DAY else "")
        with st_grid(cols="45% 55%", gap="1vw",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                if not code:
                    # La PLACE du QR, aux dimensions du vrai : passer d'un état
                    # à l'autre ne fait pas sauter la mise en page.
                    with st_block(s.project.ds.stage.qr_placeholder):
                        st_write(bs.day, "QR code", tag=t.div)
                else:
                    st_image(s.project.cards.media_center, width=_QR_WIDTH,
                             uri=(f"images/qr/qr_join_{code}.png"
                                  if chosen != CUSTOM_DAY else _generated_qr(code)),
                             alt=f"QR code opening the survey at "
                                 f"app.sumvadis.ai/s/{code}")
            with g.cell():
                if not code:
                    st_write(bs.url, _JOIN_URL_SHOWN, tag=t.div)
                    st_write(bs.code_masked, "??????", tag=t.div)
                else:
                    st_write(bs.url, _JOIN_URL_SHOWN, tag=t.div,
                             link=join_url(code), no_link_decor=True)
                    st_write(bs.code, code, tag=t.div)
                st_write(bs.hint, (s.project.titles.keyword, "anonymous"),
                         "  ·  20-40 min  ·  phone or laptop", tag=t.div)
