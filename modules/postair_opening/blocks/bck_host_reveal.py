"""Curtain-up — the host, revealed by a studio film.

Data-driven from ``postair_data.film_clip``: the block names a WORK and a
language, never a file. The bytes are materialised from the CDN catalogue by
``_project/tools/sync_media.py`` — nothing here is versioned.

The film is the « host reveal » production of the studio, to be declared in
the ``films`` section of ``cartes-design.json`` with VERSION addresses
``/v/…`` (rule I3 — never ``/c/``), then frozen (``sync_media.py --freeze``)
and materialised. Until then ``film_clip`` raises noisily — which is why the
block stays commented out in ``book.py`` until the freeze exists.

Same layout mechanics as ``bck_wait_loop``: ``st.video`` sizes itself on the
WIDTH of its container, so the stage bounds that width by the available
HEIGHT — the 16:9 clip follows both dimensions of the window and stays whole.
The stage takes the WHOLE window: no title, no margin, nothing else on
screen. The play hint is laid OVER the video, so it costs no height at all.

SPEAKER NOTES:
Nothing to say — the film IS the introduction. The operator clicks play once
(browsers block autoplay with sound), the room watches the curtain rise, and
the NEXT slide says who was just revealed. Do not talk over it.
"""
# @guideline: postair-minimal

from pathlib import Path

from custom.styles import Styles as s
from postair_data import film_clip
from postair_lang import T
from streamtex import *
from streamtex import st_video
from streamtex.enums import Tags as t

from postair_pack.components.ai_mark import ai_marked

#: Le film est en 16:9 (même contrat de rendition que « axes-intro »).
_CLIP_RATIO = 16 / 9

#: Blocks live in ``<module>/blocks/``; the media root is a sibling of that
#: directory — resolved from the file, same as in ``bck_wait_loop``.
_MEDIA = Path(__file__).parent.parent / "static" / "media"


class BlockStyles:
    hint = s.project.body.caption + s.center_txt


bs = BlockStyles

_MARKER = {"en": "Host reveal", "fr": "L'hôte révélé"}
_HINT = {"en": "▶ play · sound on", "fr": "▶ lecture · avec son"}


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.media_fullscreen):
        # The stage is bounded by the FULL window height; the video fills it.
        with st_block(s.project.containers.media_stage(_CLIP_RATIO, 100)):
            # st.video needs a real file path: the media folder is deliberately
            # NOT a static source, so it cannot be resolved through them.
            with ai_marked(fit=False, top=True):
                st_video(str(_MEDIA / film_clip("host-reveal", lang)), autoplay=True, )
        with st_block(s.project.containers.media_hint_overlay):
            st_write(bs.hint, T(_HINT, lang), tag=t.div)
