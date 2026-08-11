"""fact_card — one sourced figure and, on the same card, what contradicts it.

A vertical stack inside one grid cell: the value large enough for the back
rows, the claim it supports, the counterpoint in coral, and the attribution.
The caller places four of them in ONE flat grid.

The counterpoint is part of the card, not of the tooltip, and that is the whole
point of the pattern: a figure projected alone reads as a verdict, and this deck
does not project verdicts. If a figure has no counterpoint worth showing, it
does not belong on the slide.

Population and methodological caveat stay in the slide tooltip — an auditorium
reads a number and a line, it does not read a sample description. The reference
travels as a citation code inside ``attribution`` (full reference on hover):
the caller appends it, this component just renders the string it is given.
"""

from streamtex import st_block, st_space, st_write
from streamtex.enums import Tags as t
from streamtex.styles import StxStyles

__component_meta__ = {
    "name": "fact_card",
    "kind": "composition",
    "since": "0.3.0",
}


def fact_card(design_system, value: str, claim: str, counterpoint: str,
              attribution: str, card_style=None) -> None:
    """Render one figure column.

    Parameters
    ----------
    design_system: a POSTAIR-protocol design system.
    value: the figure itself, already resolved to the display language.
    claim: the one-line statement the value supports.
    counterpoint: the short form of what pulls against it — never empty.
    attribution: source and date, in a few words.
    card_style: wash of the card; defaults to the framing blue. All four cards
        of a slide share one style: they hold the same role, and a different
        colour per figure would suggest a ranking that the evidence does not
        support.
    """
    ds = design_system
    # Tout est centré dans la cellule (NG 2026-08-03) : le chiffre l'était déjà
    # de fait, et une phrase courte alignée à gauche sous un grand nombre centré
    # donnait une carte de travers.
    centered = StxStyles.center_txt
    with st_block(card_style or ds.cards.blue):
        st_write(ds.titles.slide_title + centered, value, tag=t.div)
        st_write(ds.body.body + centered, claim, tag=t.div)
        st_space("v", "1vh")
        st_write(ds.body.body + ds.colors.coral + centered, counterpoint, tag=t.div)
        st_space("v", "0.6vh")
        st_write(ds.body.caption + centered, attribution, tag=t.div)
