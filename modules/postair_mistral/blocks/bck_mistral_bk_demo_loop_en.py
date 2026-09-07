"""Réserve — le parcours de la démo en boucle, captures EN (plan B réseau).

Demande NG (2026-09-07) : deux diaporamas automatiques en annexe backup, un
par série de captures — celui-ci projette TOUJOURS la série EN, quelle que
soit la langue du deck (l'orateur choisit sa réserve). Il remplace le
secours Vibe du 2026-09-03 et ses captures temporaires. Les images sont
celles du bloc pas à pas du flux (``bck_mistral_demo_steps``) :
``static/images/slideshows/demo-use/en/``, 4 s par capture, fondu CSS,
``durations.json`` optionnel.

SPEAKER NOTES:
Only if the live demo fails and the room needs the path without you pressing
keys: narrate over the loop, one sentence per screen. For a manual walk,
prefer the « Demo: steps » slide in the flow.
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

#: La série projetée par CE bloc — fixe, indépendante de la langue du deck.
_SERIES = "en"
_MARKER = {"en": "Backup: demo loop (EN)", "fr": "Secours : démo en boucle (EN)"}
_TITLE = {"en": ("Demo backup — ", (s.project.titles.keyword, "English captures")),
          "fr": ("Secours démo — ", (s.project.titles.keyword, "captures anglaises"))}
_LINE = {"en": "the demo path, four seconds a frame — for the day the network fails",
         "fr": "le parcours de la démo, quatre secondes par image — pour le jour où le réseau tombe"}

# ── La main de l'artiste ────────────────────────────────────────────────────
TUNING = {"dwell_s": 4, "stage_vh": 66}


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        with st_zoom(140):
            st_write(bs.title, *TF(_TITLE, lang),
                     tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
        st_space("v", "1.5vh")
        st_write(bs.line, T(_LINE, lang), tag=t.div)
        st_space("v", "3vh")
        st_slideshow(f"images/slideshows/demo-use/{_SERIES}",
                     dwell_s=TUNING["dwell_s"], stage_vh=TUNING["stage_vh"],
                     alt=f"Mistral demo walkthrough ({_SERIES})")
