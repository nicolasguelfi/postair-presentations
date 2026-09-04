"""La slide DLH (C2) — le Digital Learning Hub, en images qui défilent.

Demande NG (planche anim1, 2026-09-03) : « juste un titre, un sous-titre, et
en dessous en grand une image animée » — les captures du site DLH défilent
4 s chacune, en boucle (``st_slideshow``, fondu CSS pur). Les images vivent
dans ``static/images/slideshows/dlh/`` : déposer un fichier suffit, il est
pris au prochain affichage (tuyau=p1) ; ``durations.json`` optionnel pour
allonger une capture (api=a2).

Le DLH est une structure GOUVERNEMENTALE luxembourgeoise : des formations en
présentiel à très bas prix, réductions étudiantes, et un catalogue qui couvre
l'intelligence artificielle. Versions temporaires des captures (NG) — à
remplacer par les définitives en déposant simplement les fichiers.

SPEAKER NOTES:
The bridge out of the day: you leave with a method — here is where you keep
building it. The Digital Learning Hub is government-backed, in-person,
genuinely cheap, with student discounts, and its catalogue covers AI. I teach
there too — come and say hello. (Le rôle de formateur se dit À L'ORAL —
décision de sobriété, reco p1 de la planche anim1 conservée.)
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from postair_lang import T, TF
from postair_slideshow import st_slideshow
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    subtitle = s.project.titles.subtitle + s.center_txt


bs = BlockStyles

_MARKER = {"en": "Digital Learning Hub", "fr": "Digital Learning Hub"}
_TITLE = {"en": ((s.project.titles.keyword, "Digital Learning Hub"),), "fr": ((s.project.titles.keyword, "Digital Learning Hub"),)}
_SUBTITLE = {"en": "state-backed courses on AI — student prices", "fr": "des formations IA publiques — à prix étudiant"}

# ── La main de l'artiste ────────────────────────────────────────────────────
TUNING = {
    "dwell_s": 4,       # secondes par capture (surcharge : durations.json)
    "stage_vh": 62,     # la scène du diaporama — LE levier de taille (R4d)
}


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        with st_zoom(120):
            st_write(bs.title, *TF(_TITLE, lang),
                     tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
        with st_zoom(100):
            st_write(bs.subtitle, T(_SUBTITLE, lang), tag=t.div)
        st_space("v", "1vh")
        with st_zoom(120):
            st_slideshow("images/slideshows/dlh",
                     dwell_s=TUNING["dwell_s"], stage_vh=TUNING["stage_vh"],
                     alt="Digital Learning Hub website")
