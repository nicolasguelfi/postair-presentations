"""Waiting screen while the audience settles in.

Data-driven from ``postair_data.mascot_clip``: the block names a mascot and a
language, never a file. The bytes are materialised from the CDN catalogue by
``_project/tools/sync_media.py`` — nothing here is versioned.

The clip is square, and that is the whole layout problem of this slide.
``st.video`` sizes itself on the WIDTH of its container and lets the height
follow the aspect ratio, without ever consulting the window: served full width
on a projector, a square clip is nearly two thousand pixels tall, overflows the
screen, and resizing the window never puts it right. The stage container bounds
the width by the available HEIGHT instead, so the video follows both dimensions
of the window and stays whole.

The stage takes the WHOLE window (NG 2026-08-03): no title, no margin, nothing
else on screen. ``media_stage(ratio, 100)`` lets the clip grow until it touches
one edge of the window — the top and bottom on a wide screen, the two sides on
a narrow one — and it stays proportional at every width in between, because
both bounds are expressed in viewport units rather than in pixels. The play
hint is laid OVER the video rather than under it, so it costs no height at all.

SPEAKER NOTES:
Nothing to say — this screen runs on its own while the 1500 students enter
the auditorium. One looping video, sound ON, no text, no information that
would reveal what comes next. The operator clicks play once when projection
starts (browsers block autoplay with sound).

Video: Solyo, the optimism mascot of the animal family, in the Postures series
published by the commercials repository. If it ever needs to be another
mascot, change the name below — every mascot of the cast has a clip in both
languages, and they are all already in the container.
"""
# @guideline: postair-minimal

from pathlib import Path

from custom.styles import Styles as s
from postair_data import mascot_clip
from streamtex import *
from streamtex.enums import Tags as t

#: The clip is 1080×1080 — a square. Width divided by height, so: one.
_CLIP_RATIO = 1.0

#: Blocks live in ``<module>/blocks/``; the media root is a sibling of that
#: directory. Resolved from the file rather than the working directory, so the
#: slide renders the same under Streamlit, under a test harness and at export.
_MEDIA = Path(__file__).parent.parent / "static" / "media"


class BlockStyles:
    hint = s.project.body.caption + s.center_txt


bs = BlockStyles


def build():
    st_marker("Waiting screen")
    with st_block(s.project.containers.media_fullscreen):
        # The stage is bounded by the FULL window height; the video fills it.
        with st_block(s.project.containers.media_stage(_CLIP_RATIO, 100)):
            # st.video needs a real file path: the media folder is deliberately
            # NOT a static source, so it cannot be resolved through them.
            st_video(str(_MEDIA / mascot_clip("Solyo", "en")), loop=True)
        with st_block(s.project.containers.media_hint_overlay):
            st_write(bs.hint, "▶ play · loop · sound on", tag=t.div)
