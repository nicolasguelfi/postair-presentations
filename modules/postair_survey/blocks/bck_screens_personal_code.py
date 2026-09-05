"""Your code — keep it — écran 16-res-code-partage.

Un écran = un bloc (NG 2026-08-23, découpage de bck_screens_personal) : l'ordre du deck,
l'inclusion et l'exclusion se règlent par une ligne du book.

SPEAKER NOTES:
Say « screenshot your code » out loud — the single most useful
instruction of the morning.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from postair_lang import T, TF
from streamtex import *


_MARKER = {"en": "Your code", "fr": "Votre code"}
_TITLE = {"en": ("Your ", (s.project.titles.keyword, "code"), " — keep it"), "fr": ("Votre ", (s.project.titles.keyword, "code"), " — gardez-le")}
_MESSAGES = [
    ({"en": "The only way back", "fr": "Le seul chemin de retour"},
     {"en": ("The personal code at the end of the report reopens your result "
             "at app.sumvadis.ai/r — screenshot it now."), "fr": "Le code personnel en fin de rapport rouvre votre résultat sur app.sumvadis.ai/r — faites-en une capture d'écran maintenant."}),
    ({"en": "No account, no recovery", "fr": "Ni compte, ni récupération"},
     {"en": ("Anonymous means exactly this: no email, no login — lose the code "
             "and nobody can find your report again."), "fr": "Anonyme veut dire exactement cela : ni e-mail, ni identifiant — perdez le code et personne ne retrouvera votre rapport."}),
    ({"en": "Share on your terms", "fr": "Partagez à vos conditions"},
     {"en": ("Download or share the report if you wish; nothing is published "
             "by default."), "fr": "Téléchargez ou partagez le rapport si vous voulez ; rien n'est publié par défaut."}),
]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    screen_slide(
        TF(_TITLE, lang),
        "16-res-code-partage",
        "Mobile screen of the end of the report: personal retrieval code, "
        "share and download actions, dark theme",
        [(T(h, lang), T(d, lang)) for h, d in _MESSAGES],
        zoomImage=200,
        zoomText=130,
        lang=lang
    )
