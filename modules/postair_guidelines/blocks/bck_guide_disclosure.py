"""Reflex 2 — say it: the five disclosure elements (U3).

Five big numbered cards — the visual IS the checklist — and the one-line
example disclaimer in amber below. Prompt-history advice and the Appendix 1
ready-made disclaimers live in the tooltip.

Le FAIT vit ici (règle NG 2026-08-18) : les cinq éléments de disclosure,
l'exemple, les conseils du tooltip et le choix des citekeys s'éditent dans ce
bloc. La phrase bibliographique reste dérivée de ``references.bib`` par
``citation()`` — clé inconnue = erreur bruyante.

SPEAKER NOTES:
Two minutes, one card each, fast. Land on the amber example: a disclosure is
ONE honest sentence, not a confession. Then the practical tip from the
tooltip, said out loud: teachers may ask for your prompt history — keep your
conversations. The wink is in the tooltip too: the appendix's own examples
were generated with Copilot, then revised.
"""
# @guideline: postair-minimal

from custom.refs import citation
from custom.styles import Styles as s
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    number = s.project.titles.subtitle + s.project.colors.keyword + s.center_txt + s.bold
    short = s.project.body.bullet + s.center_txt + s.bold
    example = s.project.titles.subtitle + s.project.colors.amber + s.center_txt
    cite = s.project.body.caption + s.center_txt


bs = BlockStyles

# ── Le fait : les cinq éléments à dire (guidelines, section 2) ──────────────
#: « short » est projeté sur la carte ; « detail » vit dans le tooltip.
_ITEMS = [
    {"n": "1", "short": "Which tool",
     "detail": "Name the tool(s) and version you used."},
    {"n": "2", "short": "For what",
     "detail": "The purpose: brainstorm, draft, translate, debug…"},
    {"n": "3", "short": "How much",
     "detail": ("The extent of the use — a paragraph, the structure, the "
                "whole draft.")},
    {"n": "4", "short": "What YOU did with it",
     "detail": ("Edited, corrected, rewrote, integrated — the output is a "
                "material, not a result.")},
    {"n": "5", "short": "How you verified",
     "detail": ("How sources and claims were validated against reliable "
                "references.")},
]
_EXAMPLE = ("« I used Copilot to brainstorm the outline; all arguments and "
            "sources are mine and verified. »")
_PROMPTS_TIP = ("Teachers may require your prompt history, a usage log and "
                "your verification evidence — keep your conversations.")
_ANNEX_NOTE = ("Appendix 1 provides ready-to-use disclaimers per category "
               "(brainstorming, proofreading, translation, code, content "
               "generation) — copy and adapt. Footnote of the appendix: those "
               "examples were themselves generated with Copilot, then "
               "revised.")
_CITEKEYS = ["i2tl2026-guidelines"]
#: Jamais projeté, gardé pour la vérifiabilité (entrée « big » de l'ancien
#: facts.json) : « Say it — five things ».


def build(lang: str = "en", **_):
    st_marker("Say it")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "Reflex 2 — ", (s.project.titles.keyword, "say it"),
                         tag=t.div, toc_lvl="+1", label="Say it")
            with g.cell():
                st_info_tooltip(
                    title="Disclosure (guidelines, section 2)",
                    entries=[(f"{i['n']} · {i['short']}", i["detail"])
                             for i in _ITEMS]
                            + [("Keep your prompts", _PROMPTS_TIP),
                               ("Appendix 1", _ANNEX_NOTE)],
                )
        st_space("v", s.project.spacing.title_gap)
        with st_grid(cols=s.project.grids.balanced(len(_ITEMS)), gap="1vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for item in _ITEMS:
                with g.cell(), st_block(s.project.cards.blue):
                    st_write(bs.number, item["n"], tag=t.div)
                    st_write(bs.short, item["short"], tag=t.div)
        st_space("v", "2.5vh")
        st_write(bs.example, _EXAMPLE, tag=t.div)
        st_write(bs.cite, "One honest sentence is enough ",
                 citation(*_CITEKEYS), tag=t.div)
