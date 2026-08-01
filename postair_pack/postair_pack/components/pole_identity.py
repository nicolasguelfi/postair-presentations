"""pole_identity — what a pole claims, and the three statements that measure it.

ONE flat grid, two columns: the pole's two mascots stacked on the left
(bestiary above, object below), its three survey statements on the right.

The design brief described a two-column-by-three-row grid with the left column
merged across the three rows. A merged column facing three rows is, in layout
terms, exactly a two-cell grid whose left cell stacks and whose right cell
stacks — and expressing it that way keeps a single flat grid instead of a
row-span construction that browsers reflow unpredictably at projection widths.
The rendering is identical; the rule on flat grids stays intact.
"""

from streamtex import st_block, st_grid, st_image, st_space, st_write
from streamtex.enums import Tags as t

__component_meta__ = {
    "name": "pole_identity",
    "kind": "composition",
    "since": "0.2.0",
}


def pole_identity(mascots, statements, design_system,
                  mascot_width: str = "min(13vw, 24vh)") -> None:
    """Render the identity body of one pole.

    Parameters
    ----------
    mascots: the pole's mascots, one per family, each a dict with ``mascot``,
        ``image`` and ``label`` — bestiary first, object second.
    statements: the three survey statements, already resolved to strings.
    design_system: a POSTAIR-protocol design system.
    mascot_width: CSS width of each mascot, bounded by viewport height so the
        two stacked portraits and the three statements share one slide.
    """
    ds = design_system
    with st_grid(cols="34% 66%", gap="2vw",
                 cell_styles=ds.containers.grid_cell_centered) as g:
        with g.cell():
            for m in mascots:
                st_image(ds.cards.media_center, width=mascot_width, uri=m["image"],
                         alt=f"{m['mascot']} — mascot of the {m['label']} posture")
                st_write(ds.body.mascot_name, m["mascot"], tag=t.div)
        with g.cell():
            for statement in statements:
                with st_block(ds.cards.blue):
                    st_write(ds.body.bullet, statement, tag=t.div)
                st_space("v", "1vh")
