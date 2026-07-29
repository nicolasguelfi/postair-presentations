"""W00 — Waiting screen while the audience settles in.

SPEAKER NOTES:
Nothing to say — this screen runs on its own while the 1500 students enter
the auditorium. One looping video, sound ON, no text, no information that
would reveal what comes next. The operator clicks play once when projection
starts (browsers block autoplay with sound). Placeholder video: Solyo's
talking portrait (EN) — to be replaced by a dedicated teaser produced with
the mascoties studio.
"""
# @guideline: postair-minimal

import streamtex as stx
from custom.styles import Styles as s
from streamtex import *
from streamtex import st_marker, st_video
from streamtex.enums import Tags as t


class BlockStyles:
    hint = s.project.body.caption + s.center_txt


bs = BlockStyles


def build():
    st_marker("W00 — Waiting screen")
    # Full-window video: no grid, no side margins — the player spans the
    # whole page width and scales automatically with the window.
    with st_block(s.project.containers.page_fill_full):
        # st.video needs an absolute file path — resolve via static sources.
        st_video(stx.resolve_static("_SHARED/mascots/videos/waiting_loop_placeholder_en.mp4"),
                 loop=True)
        st_write(bs.hint, "▶ play · loop · sound on", tag=t.div)
