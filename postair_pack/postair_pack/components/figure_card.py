"""figure_card — one historical figure of a pole: portrait, quotation, reference.

Layout: a vertical stack inside one grid cell — portrait, caption, quotation,
reference. The caller places three of them side by side in ONE flat grid.

The provenance rules (reconstructed postures commit their author; a living
person is never made to speak by generative AI) are NOT repeated on the card:
since 2026-08-11 they are stated once, on the deck's standalone provenance
slide — fifty-four repetitions turned an honesty clause into wallpaper.

A quotation whose reference is still unresolved upstream renders with a visible
reserve rather than silently looking sourced.
"""

from streamtex import st_block, st_image, st_space, st_write
from streamtex.enums import Tags as t

__component_meta__ = {
    "name": "figure_card",
    "kind": "composition",
    "since": "0.2.0",
}

#: Shown in place of a reference that upstream has not resolved yet.
UNRESOLVED_REFERENCE = "reference being established"


def figure_card(figure: dict, design_system, quote_text: str,
                reference: str | None = None, portrait_width: str = "min(11vw, 22vh)") -> None:
    """Render one figure column.

    Parameters
    ----------
    figure: one entry of ``poles[].figures`` in the debate manifest — ``name``,
        ``dates``, ``origin``, ``wave``, ``score``, ``media``.
    design_system: a POSTAIR-protocol design system.
    quote_text: the quotation, already resolved to the display language.
    reference: its reference, or None when upstream has not resolved one.
    portrait_width: CSS width of the portrait, bounded by viewport height so
        three cards plus their quotations always fit one slide.
    """
    ds = design_system
    media = figure.get("media") or {}
    with st_block(ds.cards.axis_frame):
        st_image(ds.cards.media_center, width=portrait_width,
                 uri=media.get("portrait"), link=media.get("video"),
                 alt=f"Portrait of {figure['name']} — click to play the presentation video")
        st_write(ds.body.pole_label, figure["name"], tag=t.div)
        st_write(ds.body.mascot_name,
                 " · ".join(x for x in (figure.get("dates"), figure.get("origin"),
                                        figure.get("wave")) if x),
                 tag=t.div)
        st_space("v", "1vh")
        st_write(ds.body.body, f"“{quote_text}”", tag=t.div)
        st_space("v", "0.6vh")
        st_write(ds.body.caption, reference or UNRESOLVED_REFERENCE, tag=t.div)
