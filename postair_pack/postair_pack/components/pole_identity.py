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

from streamtex import st_block, st_grid, st_image, st_space, st_write, st_zoom
from streamtex.enums import Tags as t

from postair_pack.components.ai_mark import dd35_overlay

__component_meta__ = {
    "name": "pole_identity",
    "kind": "composition",
    "since": "0.2.0",
}


def pole_identity(mascots, statements, design_system,
                  mascot_width="min(13vw, 24vh)",
                  statement_zoom: int = 100) -> None:
    """Render the identity body of one pole.

    Parameters
    ----------
    mascots: the pole's mascots, one per family, each a dict with ``mascot``,
        ``image`` and ``label`` — bestiary first, object second.
    statements: the three survey statements, already resolved to strings.
    design_system: a POSTAIR-protocol design system.
    mascot_width: CSS width of each mascot — one string for all, or a list
        with one width per mascot (R4d: a portrait file needs a narrower
        width for the same height budget, width = height_vh × file ratio).
    statement_zoom: ``st_zoom`` factor of the statements column (100 =
        neutral) — the per-deck size lever, set by the caller (hero_split
        contract: tuned per slide, never a central config).
    """
    ds = design_system
    with st_grid(cols="34% 66%", gap="2vw",
                 cell_styles=ds.containers.grid_cell_centered) as g:
        with g.cell():
            widths = (mascot_width if isinstance(mascot_width, (list, tuple))
                      else [mascot_width] * len(mascots))
            for m, width in zip(mascots, widths):
                st_image(ds.cards.media_center, width=width, uri=m["image"],
                         alt=f"{m['mascot']} — mascot of the {m['label']} posture",
                    overlay=dd35_overlay())
                st_write(ds.body.mascot_name, m["mascot"], tag=t.div)
        with g.cell():
            with st_zoom(statement_zoom):
                for statement in statements:
                    with st_block(ds.cards.blue):
                        st_write(ds.body.bullet, statement, tag=t.div)
                    st_space("v", "1vh")
