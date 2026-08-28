"""The tools UL gives you (U6).

One dominant papercut image — the protected M365 bubble versus the open
cloud — and the three lines that matter: Copilot with the UL account is the
supported choice, UniGPT is staff-only for now, free public tools pay
themselves with your data. Equity rules in the tooltip.

Le FAIT vit ici (règle NG 2026-08-18) : les trois lignes outils, les règles
d'équité et le choix des citekeys s'éditent dans ce bloc. La phrase
bibliographique reste dérivée de ``references.bib`` par ``citation()`` — clé
inconnue = erreur bruyante.

SPEAKER NOTES:
Two minutes. The image carries the model: inside the bubble, your data stays
UL's; outside, it is the product. Say the equity rule out loud — if a course
requires AI, a free path must exist; premium subscriptions must not buy
grades — it concerns every wallet in the room.
"""
# @guideline: postair-minimal

from custom.prompts import AI_PREFIX, AI_SUFFIX_LANDSCAPE
from custom.refs import citation
from custom.styles import Styles as s
from custom.visuals import hero_image
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    line = s.project.body.bullet + s.center_txt
    accent = s.project.body.bullet + s.project.colors.amber + s.center_txt + s.bold
    cite = s.project.body.caption + s.center_txt


bs = BlockStyles

# ── Le fait : les outils soutenus par l'UL (guidelines, section 3, p.5) ─────
_SUPPORTED = ("Copilot + UL account = THE supported choice · your data stays "
              "in UL's M365")
_UNIGPT = "UniGPT (internal, secure) · staff first"
_OUTSIDE = "outside → paid with your data · personal / sensitive = NEVER"
_EQUITY = [
    "course REQUIRES AI → a free path must exist",
    "conscientious objection → CAR committee",
]
_CITEKEYS = ["i2tl2026-guidelines"]
#: Jamais projeté, gardé pour la vérifiabilité (entrée « big » de l'ancien
#: facts.json) : « The tools UL gives you ».

_BUBBLE_PROMPT = (
    AI_PREFIX
    + "A large transparent paper bubble dome sheltering a small papercut "
      "campus with a glowing warm amber paper orb inside it, cosy and safe. "
      "Outside the bubble, an open paper sky with scattered clouds and small "
      "paper documents flying away in the wind toward the horizon."
    + AI_SUFFIX_LANDSCAPE
)


def build(lang: str = "en", **_):
    st_marker("UL tools")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "The tools ", (s.project.titles.keyword, "UL gives you"),
                         tag=t.div, toc_lvl="+1", label="UL tools")
            with g.cell():
                st_info_tooltip(
                    title="Supported tools (guidelines, section 3, p.5)",
                    entries=[
                        ("Microsoft Copilot (UL account)", _SUPPORTED),
                        ("UniGPT", _UNIGPT),
                        ("Public tools", _OUTSIDE),
                        *[("Equity", e) for e in _EQUITY],
                    ],
                )
        st_space("v", s.project.spacing.title_gap)
        hero_image(
            "guide_bubble", _BUBBLE_PROMPT, "images/guide_bubble_fallback.svg",
            alt_ready=("Papercut protected bubble sheltering a small campus and an "
                       "amber orb, open windy sky with flying documents outside"),
            alt_fallback=("Papercut bubble protecting a campus, documents flying away "
                          "outside"),
            width="58%",
        )
        st_space("v", "1.5vh")
        st_write(bs.accent, "Copilot with your UL account — the supported choice",
                 tag=t.div)
        st_write(bs.line, "inside the bubble your data stays UL's · outside, it is "
                          "the product ", citation(*_CITEKEYS), tag=t.div)
