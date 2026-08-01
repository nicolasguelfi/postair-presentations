"""argument_card — one contemporary argument supporting a pole.

A vertical stack inside one grid cell: a nature badge, the argument's title,
its spokesperson, and its dated source. The caller places three of them in ONE
flat grid, deliberately of three different natures — a public policy, a
concrete case, a public statement — so a pole is never defended from a single
angle.

The full paragraph belongs in the slide tooltip, not on the card: an
auditorium reads a title and a name, it does not read a paragraph.
"""

from streamtex import st_block, st_space, st_write
from streamtex.enums import Tags as t

__component_meta__ = {
    "name": "argument_card",
    "kind": "composition",
    "since": "0.2.0",
}

#: Badge wording per manifest category — the reader sees a nature, not a key.
NATURES = {
    "policy": "public policy",
    "case": "concrete case",
    "quote": "public statement",
    "historical": "historical precedent",
    "tradition": "established practice",
}


def argument_card(argument: dict, design_system, title: str, badge_style=None) -> None:
    """Render one argument column.

    Parameters
    ----------
    argument: one entry of ``poles[].arguments`` — ``category``, ``person``,
        ``reference``, ``citekey``.
    design_system: a POSTAIR-protocol design system.
    title: the argument's title, already resolved to the display language.
    badge_style: style of the nature badge; defaults to the keyword colour.
    """
    ds = design_system
    with st_block(ds.cards.coral):
        st_write(badge_style or ds.titles.keyword,
                 NATURES.get(argument.get("category"), argument.get("category") or ""),
                 tag=t.div)
        st_space("v", "0.6vh")
        st_write(ds.body.body, title, tag=t.div)
        st_space("v", "0.6vh")
        if argument.get("person"):
            st_write(ds.body.pole_label, argument["person"], tag=t.div)
        st_write(ds.body.caption,
                 argument.get("reference") or argument.get("citekey") or "", tag=t.div)
