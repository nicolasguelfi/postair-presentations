"""Waiting screen while the audience settles in.

Data-driven from ``postair_data.film_clip``: the block names a WORK and a
language, never a file. The bytes are materialised from the CDN catalogue by
``_project/tools/sync_media.py`` — nothing here is versioned.

Since 2026-08-14 (NG) the screen plays « Les 9 axes — la phrase mémo » (68 s,
Medio narration, the nine mascots) — the axes-intro production of the studio,
declared in the catalogue's ``films`` section. It replaced the square Solyo
posture clip, whose kept-on-parole master was purged the same day.

The 16:9 clip still meets the layout problem of this slide.
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

Video: the axes-intro film. If the screen ever needs a different work, name
it below — anything the catalogue's ``films`` section declares is already
materialised in the container, in all its languages.
"""
# @guideline: postair-minimal

from pathlib import Path

from custom.styles import Styles as s
from postair_data import film_clip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.ai_mark import ai_marked

#: Le film est en 16:9 (rendition 1280×720 du master 4K).
_CLIP_RATIO = 16 / 9

#: Blocks live in ``<module>/blocks/``; the media root is a sibling of that
#: directory. Resolved from the file rather than the working directory, so the
#: slide renders the same under Streamlit, under a test harness and at export.
_MEDIA = Path(__file__).parent.parent / "static" / "media"


class BlockStyles:
    hint = s.project.body.caption + s.center_txt


bs = BlockStyles


def build(lang: str = "en", **_):
    st_marker("Waiting screen")
    with st_block(s.project.containers.media_fullscreen):
        # The stage is bounded by the FULL window height; the video fills it.
        with st_block(s.project.containers.media_stage(_CLIP_RATIO, 100)):
            # st.video needs a real file path: the media folder is deliberately
            # NOT a static source, so it cannot be resolved through them.
            with ai_marked(fit=False, top=True):
                st_video(str(_MEDIA / film_clip("axes-intro", "en")), loop=True, autoplay=True)
        with st_block(s.project.containers.media_hint_overlay):
            st_write(bs.hint, "▶ play · loop · sound on", tag=t.div)
