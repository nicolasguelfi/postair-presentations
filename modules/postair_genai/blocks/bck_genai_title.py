"""Title — Introduction to AI & Generative AI (G1).

One dominant hero image, a title, a promise: seventy years in thirty minutes.
Everything else — what the session covers, what it deliberately leaves out —
lives in the tooltip, not on the screen.

SPEAKER NOTES:
One minute. Welcome the room back from the break, give the promise (« in
thirty minutes you will know what this thing in your pocket actually is »),
and say what this session is NOT: no mathematics, no training details — where
to learn those at UL is in the info panel.
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

_HERO_PROMPT = (
    AI_PREFIX
    + "A glowing warm amber paper sun at the centre of a constellation: paper "
      "stars and small teal paper orbs linked by thin luminous threads across "
      "a deep navy paper sky, like a mind made of light. Below, a small crowd "
      "of abstract paper silhouettes seen from behind, looking up."
    + AI_SUFFIX_LANDSCAPE
)

# ── Les feuilles {en} du bloc (structure i18n, lot C genaipat 2026-09-01) ────
_MARKER = {"en": "GenAI"}
_TOC_LABEL = {"en": "GenAI intro"}
_TITLE = {"en": ("Introduction to AI & ", (s.project.titles.keyword, "Generative AI"))}
_SUBTITLE = {"en": "70 years in 30 minutes"}
_TIP_TITLE = {"en": "This session"}
_TIP = [
    ({"en": "The promise"},
     {"en": ("In thirty minutes: where this technology comes "
             "from, how it actually works, what it can do, what it gets "
             "wrong, and what that changes for your studies and careers.")}),
    ({"en": "What we will NOT cover"},
     {"en": ("The mathematics, and how training "
             "works in detail. Both are taught at UL — computer science "
             "courses, and the university's AI learning resources.")}),
    ({"en": "How it connects"},
     {"en": ("The morning gave you the nine axes and your "
             "own posture. This afternoon gives you the technology those "
             "postures are ABOUT — then Mistral hands-on, then the rules.")}),
]

# ── La main de l'artiste (pattern TUNING debates, revue genaipat 2026-09-01) ─
#: ``hero_vh`` = budget hauteur de l'image héro (staged_hero_image, R4d) —
#: remplace l'ancien ``width="82%"``, inerte au zoom (R-zoom) et borné par la
#: seule largeur : titre ≈13vh + écart 7vh + image + sous-titre ≈9vh ≈ une
#: fenêtre. À confirmer à la repasse visuelle NG.
TUNING = {
    "hero_vh": 62,
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
        st_space("v", s.project.spacing.title_gap)
        staged_hero_image(
            "genai_hero", _HERO_PROMPT, "images/genai_hero_fallback.svg",
            alt_ready=("Papercut constellation: an amber paper sun linked to stars by "
                       "luminous threads, small paper silhouettes watching from below"),
            alt_fallback=("Amber orb at the centre of a blue constellation on navy, "
                          "abstract silhouettes watching"),
            stage_vh=TUNING["hero_vh"],
        )
        st_space("v", "1vh")
        st_write(bs.subtitle, T(_SUBTITLE, lang), tag=t.div)
