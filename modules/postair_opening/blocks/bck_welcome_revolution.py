"""A revolution already here — four measured figures, each with what contradicts it.

Data-driven from ``custom.facts``: the block renders, it does not know a single
number. Every figure was verified at its own source and carries its date, its
population, its printable reference and its counterpoint; a correction is made
in ``static/data/facts.json`` and arrives here by reload.

The counterpoint sits on the card, next to the figure, not in the tooltip. A
figure projected alone reads as a verdict, and the point of this slide is not to
settle anything — it is to open the tension that makes the survey worth
answering ten minutes later. The amber line that closes the slide is the single
focal accent: none of this started in 2022.

SPEAKER NOTES:
Four minutes, quick rhythm, one figure at a time — do not read the cards, the
room reads faster than you speak. Say the number, then say the coral line, and
move on. The whole slide is built so that every claim you make out loud has its
objection visible on screen: nobody in this room can accuse us of selling them a
future.

Land on the amber line and slow down there. The research field is older than
most of the people in front of you — what changed in 2022 was not the idea, it
was that it arrived in everyone's pocket at once. That sentence is the bridge to
the afternoon session on generative AI.

If someone challenges a figure, the tooltip has the sample and the
methodological caveat, including the vendors' rebuttal on the detector figure —
and each card carries its citation code: hovering it opens the full reference
with a link to the source. Open those rather than improvising: everything on
this slide is defensible, and none of it is ours to soften.
"""
# @guideline: postair-minimal

from __future__ import annotations

from custom.facts import citekeys, figures, framing, text
from custom.refs import citation
from custom.styles import DS
from custom.styles import Styles as s
from postair_pack.components.fact_card import fact_card
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    closing = s.project.titles.subtitle + s.project.colors.amber + s.center_txt


bs = BlockStyles


def _tooltip_entries():
    """One entry per figure, then the long view — everything, in the data's order.

    Each entry carries what the card cannot hold: who was actually measured, why
    a figure of that age is still on screen, and the methodological reservation.
    The references are NOT here: they live behind the citation code on each
    card — a cite() inside a hover panel would be a hover-within-a-hover.
    """
    entries = []
    for figure in figures():
        term = f"{text(figure['value'])} — {text(figure['source'].get('attribution'))}"
        parts = [text(figure["claim"]) + ".",
                 text(figure["population"]) + "."]
        for key in ("trend", "freshness", "counterpoint", "caveat"):
            if figure.get(key):
                parts.append(text(figure[key]))
        entries.append((term, " ".join(parts)))

    long_view = framing("long-wave")
    entries.append((
        text(long_view["headline"]),
        " ".join([text(long_view["statement"]),
                  text(long_view["counterpoint"]),
                  text(long_view["note"])]),
    ))
    return entries


def build():
    st_marker("Already here")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "A revolution ", (s.project.titles.keyword, "already here"),
                         tag=t.div, toc_lvl="+1", label="Already here")
            with g.cell():
                st_info_tooltip(title="Where these figures come from",
                                entries=_tooltip_entries())
        st_space("v", "2vh")
        # ONE flat grid, laid out as a block rather than a strip: the design
        # system picks the most balanced arrangement for the number of figures
        # and stretches the rows to fill the screen. All cards share a single
        # style — they hold the same role, and a colour per figure would
        # suggest a ranking the evidence does not support.
        shown = figures()
        with st_grid(cols=s.project.grids.balanced(len(shown)), gap="1.2vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_top) as g:
            for figure in shown:
                with g.cell():
                    # Le code de citation vit dans le texte VISIBLE de la carte,
                    # à côté de l'attribution ; la référence complète est dans
                    # la carte au survol et sur la page References.
                    fact_card(DS,
                              value=text(figure["value"]),
                              claim=text(figure["claim"]),
                              counterpoint=text(figure["counterpoint"]["short"]),
                              attribution=(text(figure["source"].get("attribution"))
                                           + " " + citation(*citekeys(figure))))
        st_space("v", "2vh")
        long_view = framing("long-wave")
        st_write(bs.closing, text(long_view["headline"]), " ",
                 citation(*citekeys(long_view)), tag=t.div)
