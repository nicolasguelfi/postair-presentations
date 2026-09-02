"""Title — Study Smarter: your course agent (M1, recadré v0.2 « Mistral & co. »).

One dominant hero image, a title, a promise: a method, a demo, and the
mistakes to avoid — whatever YOUR tool. Everything else (session plan,
prerequisites, the published step-by-step) lives in the tooltip.

Le FAIT vit ici (règle NG 2026-08-18) : titre, promesse et plan de session
s'éditent dans ce bloc. Aucune affirmation sourcée sur cette slide.

SPEAKER NOTES:
One minute. The promise, slowly: in twenty minutes you leave with a METHOD to
build a revision agent for ONE of your courses — shown on Mistral, working
with whatever tool you already use. Announce the two live demos and the four
mistakes: this session shows the failures, not just the recipe.
"""
# @guideline: postair-minimal

from custom.prompts import AI_PREFIX, AI_SUFFIX_LANDSCAPE
from custom.styles import Styles as s
from custom.visuals import staged_hero_image
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    subtitle = s.project.titles.subtitle + s.project.colors.amber + s.center_txt


bs = BlockStyles

#: Scène durcie (contrôle visuel 2026-09-02) : la 1re génération rendait
#: l'étudiant figuratif (peau, oreille, profil) — la silhouette est exigée
#: PLATE, monochrome sombre, strictement de dos.
_HERO_PROMPT = (
    AI_PREFIX
    + "A student at a paper desk, rendered ONLY as a flat single-colour dark "
      "navy paper silhouette seen strictly from behind — no skin, no ear, no "
      "profile, no facial features. On the desk: a small stack of colourful "
      "paper books, an open paper notebook, and a glowing warm amber paper "
      "orb standing on the desk like a friendly companion, radiating thin "
      "luminous rays over the notebook."
    + AI_SUFFIX_LANDSCAPE
)

_MARKER = {"en": "Mistral & co.", "fr": "Mistral & co."}
_TOC_LABEL = {"en": "Study Smarter", "fr": "Réviser plus malin"}
_TITLE = {"en": ("Study Smarter: your ", (s.project.titles.keyword, "course agent")), "fr": ("Réviser plus malin : votre ", (s.project.titles.keyword, "agent de cours"))}
_SUBTITLE = {"en": "a method · a demo — whatever YOUR tool", "fr": "une méthode · une démo — quel que soit VOTRE outil"}
_TIP_TITLE = {"en": "This session", "fr": "Cette séance"}
_TIP = [
    ({"en": "The plan", "fr": "Le plan"},
     {"en": ("Why the method beats the tool, the goal (an agent for ONE "
             "course), four steps, two live demos in Mistral's Le Chat, four "
             "fatal mistakes — each one DEMONSTRATED — and the good "
             "practices to take home."), "fr": "Pourquoi la méthode prime sur l’outil, l’objectif (un agent pour UN cours), quatre étapes, deux démos en direct dans Le Chat de Mistral, quatre erreurs fatales — chacune DÉMONTRÉE — et les bonnes pratiques à emporter."}),
    ({"en": "Prerequisites", "fr": "Prérequis"},
     {"en": ("None today — watch. To redo everything at home: a free Mistral "
             "account (or your own tool: the four steps transpose as they "
             "are)."), "fr": "Aucun aujourd’hui — regardez. Pour tout refaire chez vous : un compte Mistral gratuit (ou votre propre outil : les quatre étapes se transposent telles quelles)."}),
    ({"en": "The written step-by-step", "fr": "Le pas-à-pas écrit"},
     {"en": ("A complete written walkthrough of this session is published "
             "after the AI Day — no need to take notes, photograph the "
             "method slide."), "fr": "Un pas-à-pas écrit complet de cette séance est publié après l’AI Day — inutile de prendre des notes, photographiez la slide de la méthode."}),
]

# ── La main de l'artiste (pattern TUNING) ───────────────────────────────────
#: ``hero_vh`` = budget hauteur de l'image héro (staged_hero_image, R4d).
TUNING = {
    "hero_vh": 60,
}


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="1", label=T(_TOC_LABEL, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(T(h, lang), T(d, lang)) for h, d in _TIP],
                )
        
        st_space("v", "3vh")
        st_write(bs.subtitle, T(_SUBTITLE, lang), tag=t.div)
        st_space("v", "3vh")
        
        staged_hero_image(
            "mistral_hero", _HERO_PROMPT, "images/mistral_hero_fallback.svg",
            alt_ready=("Papercut student at a desk with a book stack, an amber orb "
                       "standing on the desk radiating over an open notebook"),
            alt_fallback=("Papercut desk, student silhouette from behind, amber "
                          "agent orb on the desk between the books"),
            stage_vh=TUNING["hero_vh"],
        )
