"""axis_stack — one POSTAIR axis as a vertical column.

Layout (auditorium rule — NG 2026-07-29):
- ACCELERATOR pole on TOP (teal label + mascot), DECELERATOR pole BELOW
  (white label + mascot);
- both labels use the SAME font size (only the color differs);
- a plain vertical stack inside a simple framed block — NO nested
  responsive grids.

The caller places N axis_stack columns side by side in ONE flat grid
(e.g. ``st_grid(cols=3)`` for a register slide).
"""

from streamtex import st_block, st_image, st_write
from streamtex.enums import Tags as t

from postair_pack.components.ai_mark import ai_marked

__component_meta__ = {
    "name": "axis_stack",
    "kind": "composition",
    "since": "0.1.0",
}


def axis_stack(axis: dict, design_system, image_width: str = "min(12.8vw, 20.8vh)",
               compact: bool = False) -> None:
    """Render one axis column.

    Parameters
    ----------
    axis: dict with ``accel`` / ``decel`` pole dicts (``label``, ``mascot``,
        ``image`` static uri) — see modules/shared-blocks/postair_data.py.
    design_system: a POSTAIR-protocol design system (body + cards bundles).
    image_width: CSS width of each mascot image (bounded by viewport height
        so two stacked mascots + labels always fit one slide).
    compact: étiquettes de pôle bornées plus bas (NG 2026-08-13) — pour les
        grilles serrées (neuf cartes) où le plancher 16pt cassait les mots
        en césures sauvages (« Opennes-s », « Rationalit-y »).
    """
    ds = design_system
    label_pair = ((ds.body.pole_label_accel_compact, ds.body.pole_label_compact)
                  if compact else (ds.body.pole_label_accel, ds.body.pole_label))
    with st_block(ds.cards.axis_frame):
        for kind, label_style in (("accel", label_pair[0]),
                                  ("decel", label_pair[1])):
            pole = axis[kind]
            with st_block(ds.cards.pole_cell):
                st_write(label_style, pole["label"], tag=t.div)
                # Mascotte = média synthétique par construction (toute la
                # famille sort du catalogue gelé) : pastille DD-35 d'office.
                with ai_marked():
                    st_image(ds.cards.media_center, width=image_width, uri=pole["image"],
                             alt=f"{pole['mascot']} — mascot of the {pole['label']} posture")
                st_write(ds.body.mascot_name, pole["mascot"], tag=t.div)
