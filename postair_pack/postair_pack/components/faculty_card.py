"""faculty_card — what AI already does to the disciplines of one faculty.

A vertical stack inside one grid cell: the faculty, then two or three headlines,
each the short form of a sourced finding. The caller places one per faculty in
ONE flat grid.

Each headline is a claim about a *discipline*, never about this university: no
survey measures adoption faculty by faculty here, and the slide that uses this
component is required to say so on screen. The component therefore renders no
rate and no proportion — only what has been established elsewhere about the
work these faculties do.

The full sentence and its caveat stay in the slide tooltip. The reference
travels as a citation code inside each headline (full reference on hover):
the caller appends it, this component just renders the strings it is given.
"""

from streamtex import st_block, st_space, st_write
from streamtex.enums import Tags as t

__component_meta__ = {
    "name": "faculty_card",
    "kind": "composition",
    "since": "0.3.0",
}


def faculty_card(design_system, faculty: str, headlines, card_style=None) -> None:
    """Render one faculty column.

    Parameters
    ----------
    design_system: a POSTAIR-protocol design system.
    faculty: the faculty name, already resolved to the display language.
    headlines: the short forms, in manifest order; two or three read well, more
        than three stops being readable from the back of an auditorium.
    card_style: wash of the card; defaults to the framing blue.
    """
    ds = design_system
    with st_block(card_style or ds.cards.blue):
        st_write(ds.titles.subtitle, faculty, tag=t.div)
        st_space("v", "1vh")
        for headline in headlines:
            st_write(ds.body.body, (ds.titles.keyword, "▸ "), headline, tag=t.div)
            st_space("v", "0.8vh")
