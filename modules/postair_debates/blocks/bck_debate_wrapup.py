"""Closing the debate — the corpus behind what the room just argued about.

Ends the bank on the only claim the whole document is really making: every one
of these postures has been held, argued and written down by someone whose name
is in the history of technology. The counts come from the manifest, so the
slide cannot overstate the corpus.

SPEAKER NOTES:
Two minutes, whichever axes you opened. Say the number out loud — this many
figures, this many centuries — and then the point of it: not one of these
positions is a mistake, and not one of them was invented this morning. The
room has just argued its way into a conversation that is older than every
technology it knows. Then hand back to the opening deck for the wrap-up.
"""
# @guideline: postair-minimal

from custom.content import manifest, poles
from custom.styles import Styles as s
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    figure = s.project.titles.register_title + s.center_txt
    label = s.project.body.body + s.center_txt
    lead = s.project.body.bullet + s.center_txt


bs = BlockStyles


def build():
    st_marker("No consensus")
    data = manifest()
    counts = [
        (str(len(poles())), "postures"),
        (str(data.get("figures_used", 0)), "figures who held one"),
        (str(sum(len(p["arguments"]) for p in poles())), "arguments made today"),
    ]
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "Not one of these positions is ",
                         (s.project.titles.keyword, "new"),
                         tag=t.div, toc_lvl="1", label="No consensus")
            with g.cell():
                st_info_tooltip(
                    title="Where this material comes from",
                    entries=[
                        ("The corpus", f"{data.get('figures_used', 0)} figures of the study "
                         f"appear in this bank, drawn from seventeen technological waves — "
                         f"printing, steam, electricity, the atom, the network. "
                         f"{data.get('figures_reused', 0)} of them defend two different poles, "
                         f"which is exactly as inconsistent as real people are."),
                        ("The quotations", "Verbatim and verified against primary sources. "
                         "Where a reference is still being established, the card says so."),
                        ("The arguments", "Drawn from the debate material of the study, of three "
                         "natures — a public policy, a concrete case, a public statement — so no "
                         "pole is defended from a single angle."),
                        ("Nothing typed here", "Every name, quotation, reference and argument on "
                         "these slides is regenerated from the study. A correction upstream "
                         "reaches the deck by rebuilding it, never by editing a slide."),
                        ("Your posture", "It is a snapshot, and it moves. The survey can be "
                         "retaken with the same code at the end of the year."),
                    ],
                )
        st_space("v", "1vh")
        st_write(bs.lead, "Every one of them was ",
                 (s.project.titles.keyword, "argued before you were born"), tag=t.div)
        st_space("v", "3vh")
        with st_grid(cols=s.project.grids.balanced(len(counts)), gap="1.5vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for value, label in counts:
                with g.cell(), st_block(s.project.cards.teal):
                    st_write(bs.figure, value, tag=t.div)
                    st_write(bs.label, label, tag=t.div)
