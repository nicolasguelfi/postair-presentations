"""Title — The UL AI Guidelines (U1).

One dominant papercut image (the official document, sealed, under the amber
orb), the exact title, the version line. The full identity card of the
document — issuer, structure, nature, where to download — lives in the
tooltip. Data-driven from ``custom.facts`` (section ``identity``).

SPEAKER NOTES:
One minute, positive tone: « these rules exist so that you CAN use AI, well ».
Say the three facts that matter: official document, for students AND teachers,
version 1.0 of February 2026. Fifteen minutes for the essential — the full
text is nineteen pages and its identity card is in the info panel.
"""
# @guideline: postair-minimal

from custom.facts import citekeys, section, text
from custom.prompts import AI_PREFIX, AI_SUFFIX_LANDSCAPE
from custom.refs import citation
from custom.styles import Styles as s
from custom.visuals import hero_image
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    subtitle = s.project.titles.subtitle + s.project.colors.amber + s.center_txt
    version = s.project.body.caption + s.center_txt


bs = BlockStyles

_COVER_PROMPT = (
    AI_PREFIX
    + "A large paper document standing upright like a monument, made of "
      "cream cardstock with layered paper pages, closed by a bright coral "
      "paper ribbon and a round paper wax seal, on a small paper pedestal. "
      "A warm glowing amber paper orb floats above it like a sun. Small "
      "abstract paper silhouettes seen from behind look up at the document."
    + AI_SUFFIX_LANDSCAPE
)


def build():
    st_marker("Guidelines")
    identity = section("identity")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "The UL ", (s.project.titles.keyword, "AI Guidelines"),
                         tag=t.div, toc_lvl="1", label="Guidelines")
            with g.cell():
                st_info_tooltip(
                    title="The document",
                    entries=[
                        ("Exact title", text(identity["title_exact"])),
                        ("Issuer", text(identity["issuer"])),
                        ("Nature", text(identity["nature"])),
                        ("Structure", text(identity["structure"])),
                    ],
                )
        st_space("v", s.project.spacing.title_gap)
        hero_image(
            "guide_cover", _COVER_PROMPT, "images/guide_cover_fallback.svg",
            alt_ready=("Papercut official document with coral ribbon and seal on a "
                       "pedestal, amber orb above, silhouettes watching"),
            alt_fallback=("Papercut sealed document under an amber orb"),
            width="60%",
        )
        st_space("v", "1vh")
        st_write(bs.subtitle, "15 minutes for the essential", tag=t.div)
        st_write(bs.version, text(identity["version_line"]), " ",
                 citation(*citekeys(identity)), tag=t.div)
