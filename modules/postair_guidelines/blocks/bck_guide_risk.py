"""Reflex 3 — the three risk levels (U4). The ONLY tricolour slide.

The dominant visual is a PAPERCUT traffic light — the tricolour lives inside
the illustration, in the day's graphic line (rappel NG 2026-08-11 : la ligne
des visuels est le papier découpé coloré, jamais une ligne navy plate). Below
it, three cards with green / orange / red washes — the deliberate, single
derogation from the postair palette (plan U4, décision de design à confirmer
au prototype) : the traffic-light semantics IS the message, and it appears
exactly once in the whole day. Data-driven from ``custom.facts`` (section
``risk_levels``).

SPEAKER NOTES:
Three minutes — this is the mental model they will reuse weekly. One level at
a time: YOU are the source (green) · you explore and VERIFY (orange) · you
delegate what you cannot verify (red). Connect red to the Mistral session's
demonstrated failures and to G7 of the GenAI session (the fabricated case).
Close on the frame line: levels are vigilance signals, not prohibitions.
"""
# @guideline: postair-minimal

from custom.facts import citekeys, section, text
from custom.prompts import AI_PREFIX, AI_SUFFIX_LANDSCAPE
from custom.refs import citation
from custom.styles import Styles as s
from custom.visuals import hero_image
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t
from streamtex.styles import Style

_TRAFFIC_PROMPT = (
    AI_PREFIX
    + "A tall friendly paper traffic light at the centre, with three big "
      "round paper lights stacked vertically — leaf green on top, warm "
      "orange in the middle, coral red at the bottom — each light a layered "
      "paper disc with a soft glow. Three small abstract paper silhouettes "
      "seen from behind look up at it from a papercut path."
    + AI_SUFFIX_LANDSCAPE
)

#: Dérogation tricolore assumée (une seule slide du jour) : trois lavis aux
#: couleurs sémantiques, calqués sur la géométrie des cartes du DS.
_WASH = {
    "low": Style("background: rgba(127,176,105,0.18); border: 1px solid rgba(127,176,105,0.55); "
                 "border-radius: 12px; padding: 1.2vw; height: 100%;", "guide_risk_low"),
    "medium": Style("background: rgba(243,156,18,0.16); border: 1px solid rgba(243,156,18,0.55); "
                    "border-radius: 12px; padding: 1.2vw; height: 100%;", "guide_risk_medium"),
    "high": Style("background: rgba(231,76,60,0.16); border: 1px solid rgba(231,76,60,0.6); "
                  "border-radius: 12px; padding: 1.2vw; height: 100%;", "guide_risk_high"),
}


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    icon = s.project.titles.subtitle + s.center_txt
    label = s.project.body.pole_label + s.center_txt
    line = s.project.body.bullet + s.center_txt + s.bold
    frame = s.project.titles.subtitle + s.project.colors.amber + s.center_txt
    cite = s.project.body.caption + s.center_txt


bs = BlockStyles


def build():
    st_marker("Three levels")
    data = section("risk_levels")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "Reflex 3 — the ",
                         (s.project.titles.keyword, "three risk levels"),
                         tag=t.div, toc_lvl="+1", label="Three levels")
            with g.cell():
                st_info_tooltip(
                    title="The levels (guidelines, section 4)",
                    entries=[(f"{lv['icon']} {text(lv['label'])} — {text(lv['line'])}",
                              text(lv["detail"])) for lv in data["levels"]]
                            + [("The frame", text(data["frame"])),
                               ("The red case that matters", "« The AI replaces the "
                                "assessed learning objective » is always high risk — "
                                "that is the one to remember.")],
                )
        st_space("v", "1vh")
        hero_image(
            "guide_traffic", _TRAFFIC_PROMPT, "images/guide_traffic_fallback.svg",
            alt_ready=("Papercut traffic light with three big lights — green, orange, "
                       "red — three paper silhouettes looking up at it"),
            alt_fallback=("Papercut traffic light with green, orange and red lights"),
            width="44%",
        )
        st_space("v", "1.5vh")
        with st_grid(cols=s.project.grids.balanced(len(data["levels"])), gap="1.2vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for lv in data["levels"]:
                with g.cell(), st_block(_WASH[lv["id"]]):
                    st_write(bs.icon, lv["icon"], " ", (bs.label, text(lv["label"])),
                             tag=t.div)
                    st_write(bs.line, text(lv["line"]), tag=t.div)
        st_space("v", "1.5vh")
        st_write(bs.frame, text(data["frame"]), " ", citation(*citekeys(data)), tag=t.div)
