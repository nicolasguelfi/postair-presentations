"""Your report — the header — écran 07-res-entete.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_personal) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.

SPEAKER NOTES:
The sentence that must land: the report is computed on the device
and belongs to nobody else.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from postair_i18n import ui
from postair_lang import T, TF
from streamtex import *


_MARKER = {"en": "Your report", "fr": "Votre rapport"}
_TITLE = {"en": ("Your ", (s.project.titles.keyword, "report"), " — the header"), "fr": ("Votre ", (s.project.titles.keyword, "rapport"), " — l'en-tête")}
_MESSAGES = [
    ({"en": "Yours, computed on your device", "fr": "Le vôtre, calculé sur votre appareil"},
     {"en": "The moment you send, the report opens — the server never sees it.", "fr": "Dès l'envoi, le rapport s'ouvre — le serveur ne le voit jamais."}),
    ({"en": "A portrait, not a grade", "fr": "Un portrait, pas une note"},
     {"en": ("Nothing on this page is a score; there is no result to be proud "
             "or ashamed of."), "fr": "Rien sur cette page n'est une note ; aucun résultat dont se vanter ou rougir."}),
    ({"en": "The gesture: scroll", "fr": "Le geste : faire défiler"},
     {"en": "Everything the next slides show lives further down this same page.", "fr": "Tout ce qu'affichent les slides suivantes est plus bas, sur cette même page."}),
]
_TIP_TITLE = {"en": "The personal report", "fr": "Le rapport personnel"}
#: La première tête vient du lexique (``anonymous_by_design``).
_TIP_ANON = {"en": ("Your answers stay on your device; only one anonymous "
                    "record reaches the room's aggregates."), "fr": "Vos réponses restent sur votre appareil ; un seul enregistrement anonyme rejoint les agrégats de la salle."}
_TIP_BELOW = ({"en": "Everything below", "fr": "Tout ce qui suit"},
              {"en": ("Mascot card, radar, per-answer detail, nearest profiles, "
                      "great figures — one scrolling page."), "fr": "Carte mascotte, radar, détail par réponse, profils les plus proches, grandes figures — une seule page à faire défiler."})


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    screen_slide(
        TF(_TITLE, lang),
        "07-res-entete",
        "Mobile screen of the top of the personal survey report, dark theme",
        [(T(h, lang), T(d, lang)) for h, d in _MESSAGES],
        toc_label=T(_MARKER, lang),
        tooltip=(T(_TIP_TITLE, lang),
                 [(ui("anonymous_by_design", lang), T(_TIP_ANON, lang)),
                  (T(_TIP_BELOW[0], lang), T(_TIP_BELOW[1], lang))]),
        zoomImage=150,
        zoomText=110,
        lang=lang
    )
