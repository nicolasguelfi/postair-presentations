"""The whole company — both mascot families, eighteen poles, one plate.

Closes the welcome sequence, just before the survey: every posture the room
is about to be asked about, animal and object side by side. The pairing of
the two families is the visual signature this deck shares with the debates
document.

If a film of the nine axes is dropped into the shared video folder under the
name below, the slide plays it instead of the plate — no code change. The
plate is not a placeholder waiting to be replaced: it reads better in a large
room than a video does, and it stays available either way.

SPEAKER NOTES:
Three minutes at most, and mostly silence. Let the room look. Say one thing
before: each of these characters is a possible posture, and none of them is
wrong. Say one thing after: the survey is about to tell you which ones look
like you. If the film is playing, do not talk over it — and check the sound
before the session, not during.
"""
# @guideline: postair-minimal

# ``from streamtex import *`` shadows the builtin ``list`` with the st_list
# module: annotations must stay unevaluated.
from __future__ import annotations

from pathlib import Path

import streamtex as stx
from custom.styles import Styles as s
from postair_data import REGISTERS, axes, register_axes
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex import st_video
from streamtex.enums import Tags as t

# Dropped in by the mascot studio when it exists; absent today.
_FILM = "_SHARED/mascots/videos/axes_intro_en_1080p.mp4"
_SHARED_STATIC = Path(__file__).resolve().parents[3] / "shared-blocks" / "static"


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    lead = s.project.body.bullet + s.center_txt
    pole = s.project.body.pole_label
    mascot_name = s.project.body.mascot_name


bs = BlockStyles


def _poles_by_family() -> list[tuple[dict, dict]]:
    """The eighteen poles, each as its (animal, object) pair."""
    objects = axes("objects")
    pairs = []
    for name, _sub, _n in REGISTERS:
        for axis in register_axes(name):
            for kind in ("accel", "decel"):
                pairs.append((axis[kind], objects[axis["axis"]][kind]))
    return pairs


def build():
    st_marker("The whole company")
    film = _SHARED_STATIC / _FILM
    with st_block(s.project.containers.page_fill_full if film.exists()
                  else s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "Nine axes, eighteen postures — ",
                         (s.project.titles.keyword, "which are yours"), "?",
                         tag=t.div, toc_lvl="+1", label="The whole company")
            with g.cell():
                st_info_tooltip(
                    title="Two families, one cast",
                    entries=[
                        ("Why two families", "Every pole is carried by an animal AND an object. "
                         "Some people recognise themselves in a creature, others in a thing — and "
                         "having two makes it obvious that the character is a position, not a "
                         "portrait of anybody."),
                        ("Eighteen poles", "Nine axes, two poles each. Both poles of an axis are "
                         "legitimate: the cast has no villain."),
                        ("Two moderators", "Medio and Voxo belong to no axis. They open, arbitrate "
                         "and close — the only two characters who do not hold a position."),
                        ("Production", "Made in house, entirely with generative AI, from the "
                         "definitions of the nine axes. The mascots are the study's own "
                         "vocabulary made visible."),
                        ("Next", "The survey asks you six questions per axis. You are about to "
                         "find out which of these characters keeps showing up in your answers."),
                    ],
                )
        if film.exists():
            # st.video needs an absolute path — resolve via static sources.
            st_video(stx.resolve_static(_FILM))
            st_space("v", "30vh")
            return
        st_space("v", "1vh")
        st_write(bs.lead, "Each one is a ", (s.project.titles.keyword, "possible posture"),
                 " — none of them is wrong", tag=t.div)
        st_space("v", "1.5vh")
        # ONE flat grid: eighteen cells, each stacking its two families.
        pairs = _poles_by_family()
        with st_grid(cols=s.project.grids.balanced(len(pairs)), gap="0.6vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_top) as g:
            for animal, obj in pairs:
                with g.cell(), st_block(s.project.cards.pole_cell):
                    st_write(bs.pole, animal["label"], tag=t.div)
                    for m in (animal, obj):
                        st_image(s.project.cards.media_center, width="min(7vw, 13vh)",
                                 uri=m["image"],
                                 alt=f"{m['mascot']}, mascot of the {m['label']} posture")
                    st_write(bs.mascot_name, f"{animal['mascot']} · {obj['mascot']}", tag=t.div)
