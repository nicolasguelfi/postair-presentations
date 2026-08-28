"""The nine axes, three by three (Knowing / Acting / Becoming).

Three sub-slides (one per register), fully data-driven from the frozen
mascot manifest (postair_data → cast_final.json). Each axis is rendered by
the pack component ``axis_stack``: accelerator pole (teal) on top,
decelerator pole below, same font size for both labels, no nested
responsive grids — the register slide is ONE flat 3-column grid.

SPEAKER NOTES:
One register per slide, ~2 minutes each. Present each axis as a legitimate
tension, not a defect: both poles are respectable postures, and each has a
mascot so nobody has to defend an opinion in person — the mascots carry the
postures. On Becoming, insist that 'accelerator' does not mean 'good'.
"""
# @guideline: postair-minimal

from custom.styles import DS
from custom.styles import Styles as s
from postair_data import REGISTERS, register_axes
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.axis_stack import axis_stack


class BlockStyles:
    register = s.project.titles.register_title + s.center_txt
    subtitle = s.project.titles.subtitle + s.center_txt


bs = BlockStyles

_TOOLTIPS = {
    "Knowing": [
        ("Trust vs Self-reliance", "Do I rely on institutions, experts and tools — or only on "
                                   "my own verified judgement?"),
        ("Optimism vs Pessimism", "Do I expect AI to improve our lives — or to degrade them?"),
        ("Rationality vs Emotion", "Do I want decisions about AI grounded in measures and "
                                   "proofs — or do feelings and intuitions count as much?"),
        ("Mascots", "Fido & Solo · Solyo & Nimbo · Logos & Pathos — each mascot carries one "
                    "posture, so opinions are depersonalised: a figure holds a posture, "
                    "not a person."),
    ],
    "Acting": [
        ("Speed vs Prudence", "Deploy AI as fast as possible — or step by step, only after "
                              "each risk is understood?"),
        ("Openness vs Resistance", "Welcome AI into my practices — or protect them from it?"),
        ("Freedom vs Control", "Let everyone use AI as they see fit — or regulate its uses "
                               "strictly?"),
        ("Mascots", "Rapo & Lento · Kuri & Piko · Libero & Guardo."),
    ],
    "Becoming": [
        ("Centralisation vs Decentralisation", "Should AI power be concentrated in a few large "
                                               "actors — or distributed among many small ones?"),
        ("Individualism vs Altruism", "Is AI first a personal advantage — or a common good to "
                                      "share?"),
        ("Transhumanism vs Humanism", "Should AI augment and transform the human condition — or "
                                      "preserve it?"),
        ("Note", "'Accelerator' never means 'good' — the poles are neutral descriptions of "
                 "postures. Mascots: Balo & Sardo · Ego & Unio · Ultra & Vita."),
    ],
}


def _register_slide(name: str, subtitle: str) -> None:
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.register, name, tag=t.div, toc_lvl="+1", label=f"Axes — {name}")
                st_write(bs.subtitle, subtitle, tag=t.div)
            with g.cell():
                st_info_tooltip(title=f"Register: {name}", entries=_TOOLTIPS[name])
        st_space("v", "1.5vh")
        # ONE flat responsive grid — 3 columns on a projector, stacking on
        # narrow windows; each cell is a self-contained axis stack.
        axes_here = register_axes(name)
        # align-start (NG 2026-08-13) : le centrage vertical décalait les
        # colonnes en escalier quand leurs étiquettes n'avaient pas le même
        # nombre de lignes.
        with st_grid(cols=s.project.grids.balanced(len(axes_here)), gap="1.5vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_top) as g:
            for axis in axes_here:
                with g.cell():
                    with st_zoom(115):
                        axis_stack(axis, DS, image_width="min(10vw, 13.5vh)")


def build(lang: str = "en", **_):
    first = True
    for name, subtitle, _nums in REGISTERS:
        if not first:
            st_slide_break(marker_label=f"Axes — {name}",
                           config=SlideBreakConfig(mode=SlideBreakMode.MARKER_ONLY))
        else:
            st_marker(f"Axes — {name}")
        _register_slide(name, subtitle)
        first = False
