"""AI concerns the whole University — one card per faculty, and one honest reserve.

Data-driven from ``custom.facts``: the block renders, it does not know a single
discipline. Each headline is the short form of a finding verified at its source;
the full sentence, its reference and its caveat live in the tooltip.

Every claim here is about a *discipline*, never about this university. No survey
measures generative-AI adoption faculty by faculty at the University of
Luxembourg, and inventing one in front of the people who teach in those three
faculties is not an option. The reserve sentence says so in amber, as the single
focal accent of the slide — the honesty is the point, not a footnote.

SPEAKER NOTES:
Four minutes. Address each third of the room by its faculty, in order: this is
the slide where a first-year law student stops thinking the day is for computer
scientists. One card at a time, one headline each — the room reads the rest.

Say the reserve line out loud. Do not let it sit there silently: "we have no
numbers for this university, nobody has measured it, and these examples are what
your field is already living through, not a measurement of this room." Saying it
buys the credibility of everything that follows, including the survey.

The tooltip carries the full sourced sentence and the caveat for each example,
including the two that come reported inside another publication rather than read
at the primary source. If challenged, say which is which — it is written there.
"""
# @guideline: postair-minimal

from __future__ import annotations

from custom.facts import disciplines, no_faculty_data, text
from custom.styles import DS
from custom.styles import Styles as s
from postair_pack.components.faculty_card import faculty_card
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    reserve = s.project.titles.subtitle + s.project.colors.amber + s.center_txt


bs = BlockStyles


def _tooltip_entries():
    """The full sourced sentence behind every headline, faculty by faculty.

    A headline on a card is a claim without its evidence. Here each one gets its
    complete statement, its reservation and its reference — and, where the
    finding was read inside another publication rather than at its own source,
    that is said rather than smoothed over.
    """
    entries = []
    for group in disciplines():
        for example in group["examples"]:
            parts = [text(example)]
            if example.get("caveat"):
                parts.append(text(example["caveat"]))
            source = example.get("source") or {}
            if source.get("kind") == "reported-in":
                parts.append("Reported inside the source below, not read at the original.")
            if source.get("reference"):
                parts.append(source["reference"])
            term = f"{text(group['faculty'])} — {text(example['headline'])}"
            entries.append((term, " ".join(parts)))
    entries.append(("No figures for this university", text(no_faculty_data())))
    return entries


def build():
    st_marker("The whole University")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "AI concerns the ", (s.project.titles.keyword, "whole University"),
                         tag=t.div, toc_lvl="+1", label="The whole University")
            with g.cell():
                st_info_tooltip(title="What AI already does to these disciplines",
                                entries=_tooltip_entries())
        st_space("v", "2vh")
        # ONE flat grid, stretched to fill the screen. One card style for all
        # three — no faculty is more concerned than another, and that is the
        # message.
        groups = disciplines()
        with st_grid(cols=s.project.grids.balanced(len(groups)), gap="1.2vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_top) as g:
            for group in groups:
                with g.cell():
                    faculty_card(DS,
                                 faculty=text(group["faculty"]),
                                 headlines=[text(e["headline"]) for e in group["examples"]])
        st_space("v", "2vh")
        # The reserve, short enough to be read from the back row. Its full
        # wording — which countries, which studies, what they do and do not
        # measure — is the last entry of the tooltip.
        st_write(bs.reserve, text(no_faculty_data()["headline"]), tag=t.div)
