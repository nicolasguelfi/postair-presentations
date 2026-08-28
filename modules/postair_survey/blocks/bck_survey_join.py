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
from postair_i18n import ui
from postair_lang import T, TF
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

# ── Le texte projeté (règle R-i18n) — le sélecteur de jour (NO_DAY, DAYS,
# CUSTOM_DAY) et l'URL affichée restent tels quels.
_MARKER = {"en": "Join the survey", "fr": "Rejoindre le sondage"}
_TITLE = {"en": ("Your turn — ", (s.project.titles.keyword, "join the survey")), "fr": ("À vous — ", (s.project.titles.keyword, "rejoignez le sondage"))}
_CODE_PLACEHOLDER = {"en": "campaign code", "fr": "code de campagne"}
_QR_PLACEHOLDER = {"en": "QR code", "fr": "code QR"}
#: Le titre du tooltip (« Anonymous by design ») vient du lexique.
_HINT = {"en": ((s.project.titles.keyword, "anonymous"),
                "  ·  20-40 min  ·  phone or laptop"), "fr": ((s.project.titles.keyword, "anonyme"), "  ·  20-40 min  ·  téléphone ou ordinateur")}
_TIP = [
    ({"en": "Your result is yours", "fr": "Votre résultat est à vous"},
     {"en": ("Your personal radar is computed ON your "
             "device; the server only receives one anonymous record."), "fr": "Votre radar personnel est calculé SUR votre appareil ; le serveur ne reçoit qu'un seul enregistrement anonyme."}),
    ({"en": "GDPR", "fr": "RGPD"},
     {"en": ("No account, no email, no tracking; data stays in the EU. "
             "Only room-level averages are ever projected (minimum 5 answers)."), "fr": "Pas de compte, pas d'e-mail, pas de traçage ; les données restent dans l'UE. On ne projette jamais que des moyennes de la salle (minimum 5 réponses)."}),
    ({"en": "One code per day", "fr": "Un code par jour"},
     {"en": ("Each session has its own campaign and its own "
             "code. The slide shows only the day the speaker has selected — the "
             "other codes are never on screen."), "fr": "Chaque séance a sa propre campagne et son propre code. La slide n'affiche que le jour choisi par l'orateur — les autres codes ne sont jamais à l'écran."}),
    ({"en": "No device?", "fr": "Pas d'appareil ?"},
     {"en": ("Pair up with a neighbour — one answer per person "
             "though: your posture, not a committee's."), "fr": "Mettez-vous à deux avec la personne d'à côté — mais une réponse par personne : votre posture, pas celle d'un comité."}),
    ({"en": "Network", "fr": "Réseau"},
     {"en": "If the venue wifi is slow, switch your phone to 4G.", "fr": "Si le wifi de la salle est lent, passez votre téléphone en 4G."}),
    ({"en": "Keep your code", "fr": "Gardez votre code"},
     {"en": ("At the end the app gives you a personal code to "
             "retrieve your result later at app.sumvadis.ai/r."), "fr": "À la fin, l'application vous donne un code personnel pour retrouver votre résultat plus tard sur app.sumvadis.ai/r."}),
]


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


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    codes = dict(DAYS)
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                with st_zoom(150):
                    st_write(bs.title, *TF(_TITLE, lang),
                            tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
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
                                                 placeholder=T(_CODE_PLACEHOLDER, lang))
                    # Le code entre dans une URL et un nom de fichier : tout
                    # sauf alphanumérique reste à l'état masqué.
                    if custom and not custom.isalnum():
                        custom = ""
            with g.cell():
                st_info_tooltip(
                    title=ui("anonymous_by_design", lang),
                    entries=[(T(h, lang), T(d, lang)) for h, d in _TIP],
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
                        st_write(bs.day, T(_QR_PLACEHOLDER, lang), tag=t.div)
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
                st_write(bs.hint, *TF(_HINT, lang), tag=t.div)
