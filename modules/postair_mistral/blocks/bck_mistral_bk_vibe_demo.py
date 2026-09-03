"""Réserve — « Demo backup : Vibe en images » (le plan B réseau des démos).

Décision NG (planche anim1, vibe=p1, 2026-09-03) : si le réseau de l'amphi
tombe pendant les démos M5/M6, cette slide rejoue le parcours dans Vibe en
captures qui défilent (``st_slideshow``, 4 s chacune, boucle). Les images
vivent dans ``static/images/slideshows/vibe-demo/`` — déposer un fichier
suffit (tuyau=p1), ``durations.json`` optionnel (api=a2).

⚠ VERSIONS TEMPORAIRES (dites par NG) : les captures actuelles montrent son
espace personnel (« Bienvenue, Nicolas », projet « Salvator », favoris) et
l'interface en FRANÇAIS — à REFAIRE en répétition sur le compte de démo,
en remplaçant simplement les fichiers du dossier.

SPEAKER NOTES:
Only if the live demo fails. Narrate over the loop: welcome screen, the
agent, the sources, a prompt, the answer with its section citation — the
same story as the live run, four seconds a frame. The interface is French
on these captures; say it and move on.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from postair_lang import T, TF
from postair_slideshow import st_slideshow
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    line = s.project.body.caption + s.center_txt


bs = BlockStyles

_MARKER = {"en": "bk · Demo images", "fr": "bk · Démo en images"}
_TITLE = {"en": ("Demo backup — ", (s.project.titles.keyword, "Vibe in pictures")), "fr": ("Secours démo — ", (s.project.titles.keyword, "Vibe en images"))}
_LINE = {"en": "the live run, four seconds a frame — for the day the network fails", "fr": "le parcours de la démo, quatre secondes par image — pour le jour où le réseau tombe"}

# ── La main de l'artiste ────────────────────────────────────────────────────
TUNING = {
    "dwell_s": 4,
    "stage_vh": 66,
}


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        with st_zoom(140):
            st_write(bs.title, *TF(_TITLE, lang),
                     tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
        st_space("v", "1.5vh")
        st_write(bs.line, T(_LINE, lang), tag=t.div)
        st_space("v", "3vh")
        st_slideshow("images/slideshows/vibe-demo",
                     dwell_s=TUNING["dwell_s"], stage_vh=TUNING["stage_vh"],
                     alt="Mistral Vibe demo walkthrough")
