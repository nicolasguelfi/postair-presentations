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
from postair_i18n import ui
from postair_lang import T
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.axis_stack import axis_stack


class BlockStyles:
    register = s.project.titles.register_title + s.center_txt
    subtitle = s.project.titles.subtitle + s.center_txt


bs = BlockStyles

#: Le nom et le sous-titre d'un registre viennent de ``postair_data``
#: (REGISTERS) — hors feuille. Les têtes « Mascots » viennent du lexique.
_MARKER = {"en": "Axes — {name}"}
_TIP_TITLE = {"en": "Register: {name}"}
_TOOLTIPS = {
    "Knowing": [
        ({"en": "Trust vs Self-reliance"},
         {"en": ("Do I rely on institutions, experts and tools — or only on "
                 "my own verified judgement?")}),
        ({"en": "Optimism vs Pessimism"},
         {"en": "Do I expect AI to improve our lives — or to degrade them?"}),
        ({"en": "Rationality vs Emotion"},
         {"en": ("Do I want decisions about AI grounded in measures and "
                 "proofs — or do feelings and intuitions count as much?")}),
        ("mascots",
         {"en": ("Fido & Solo · Solyo & Nimbo · Logos & Pathos — each mascot carries one "
                 "posture, so opinions are depersonalised: a figure holds a posture, "
                 "not a person.")}),
    ],
    "Acting": [
        ({"en": "Speed vs Prudence"},
         {"en": ("Deploy AI as fast as possible — or step by step, only after "
                 "each risk is understood?")}),
        ({"en": "Openness vs Resistance"},
         {"en": "Welcome AI into my practices — or protect them from it?"}),
        ({"en": "Freedom vs Control"},
         {"en": ("Let everyone use AI as they see fit — or regulate its uses "
                 "strictly?")}),
        ("mascots", {"en": "Rapo & Lento · Kuri & Piko · Libero & Guardo."}),
    ],
    "Becoming": [
        ({"en": "Centralisation vs Decentralisation"},
         {"en": ("Should AI power be concentrated in a few large "
                 "actors — or distributed among many small ones?")}),
        ({"en": "Individualism vs Altruism"},
         {"en": ("Is AI first a personal advantage — or a common good to "
                 "share?")}),
        ({"en": "Transhumanism vs Humanism"},
         {"en": ("Should AI augment and transform the human condition — or "
                 "preserve it?")}),
        ({"en": "Note"},
         {"en": ("'Accelerator' never means 'good' — the poles are neutral descriptions of "
                 "postures. Mascots: Balo & Sardo · Ego & Unio · Ultra & Vita.")}),
    ],
}


def _entries(name: str, lang: str):
    """Les entrées ``(tête, détail)`` du tooltip d'un registre : une tête
    écrite ``"mascots"`` est une clé du lexique, les autres sont des feuilles.
    (Pas d'annotation générique : règle R14, ``list`` est masqué ici.)"""
    return [(ui(head, lang) if isinstance(head, str) else T(head, lang),
             T(detail, lang)) for head, detail in _TOOLTIPS[name]]


def _register_slide(name: str, subtitle: str, lang: str) -> None:
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.register, name, tag=t.div, toc_lvl="+1",
                         label=T(_MARKER, lang).format(name=name))
                st_write(bs.subtitle, subtitle, tag=t.div)
            with g.cell():
                st_info_tooltip(title=T(_TIP_TITLE, lang).format(name=name),
                                entries=_entries(name, lang))
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
            st_slide_break(marker_label=T(_MARKER, lang).format(name=name),
                           config=SlideBreakConfig(mode=SlideBreakMode.MARKER_ONLY))
        else:
            st_marker(T(_MARKER, lang).format(name=name))
        _register_slide(name, subtitle, lang)
        first = False
