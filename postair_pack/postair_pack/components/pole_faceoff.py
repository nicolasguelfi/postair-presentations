"""pole_faceoff — the two poles of an axis facing each other, and the room.

ONE flat grid of three cells: pole, versus, pole. Each side shows its bestiary
mascot under its label, the accelerator in keyword colour and the decelerator
in white — the same two-tone convention the opening deck uses, so a student who
saw the axes in the morning reads this without being told.

The room's own distribution cannot be drawn here: it lives in the survey
application and changes while the session runs. The caller places the operator
button that opens it; the slide stays readable and debatable without it, which
is the point — a network failure must not end the debate.
"""

from streamtex import st_block, st_grid, st_image, st_write
from streamtex.enums import Tags as t

__component_meta__ = {
    "name": "pole_faceoff",
    "kind": "composition",
    "since": "0.2.0",
}


def pole_faceoff(sides, design_system, mascot_width: str = "min(15vw, 30vh)") -> None:
    """Render the two poles of one axis, face to face.

    Parameters
    ----------
    sides: exactly two entries, accelerator first, each a dict with ``label``,
        ``effect``, ``mascot`` and ``image``.
    design_system: a POSTAIR-protocol design system.
    mascot_width: CSS width of each mascot.
    """
    ds = design_system
    with st_grid(cols="1fr 0.4fr 1fr", gap="1vw",
                 cell_styles=ds.containers.grid_cell_centered) as g:
        left, right = sides
        for side in (left, None, right):
            with g.cell():
                if side is None:
                    st_write(ds.titles.register_title, "⇄", tag=t.div)
                    continue
                with st_block(ds.cards.pole_cell):
                    st_write(ds.body.pole_label_accel
                             if side.get("effect") == "accelerator" else ds.body.pole_label,
                             side["label"], tag=t.div)
                    st_image(ds.cards.media_center, width=mascot_width, uri=side["image"],
                             alt=f"{side['mascot']} — mascot of the {side['label']} posture")
                    st_write(ds.body.mascot_name, side["mascot"], tag=t.div)
