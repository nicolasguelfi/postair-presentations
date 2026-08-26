"""References — the theoretical frame the intro cites.

Rendered from the FROZEN ``static/data/references.bib`` (kuhn1962, perez2002 —
copied verbatim from the hub's root bibliography by
``build_waves_content.py``). Nothing on this slide is typed here. Every entry
is listed, not only the cited ones: the document is paginated, so
``get_cited_entries`` would only ever see the current slide.

SPEAKER NOTES:
Never presented — opened only if the frame is challenged.
"""
# @guideline: postair-minimal

from custom.refs import CONFIG, all_entries
from custom.styles import Styles as s
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    lead = s.project.body.caption + s.center_txt
    entry = s.project.body.caption
    number = s.project.body.caption + s.project.colors.keyword + s.bold


bs = BlockStyles


def build():
    st_marker("References")
    all_entries()
    with st_block(s.project.containers.page_fill_top):
        st_write(bs.title, "Where the frame ", (s.project.titles.keyword, "comes from"),
                 tag=t.div, toc_lvl="1", label="References")
        st_space("v", "1vh")
        st_write(bs.lead, "the theoretical frame of the deck — frozen from the "
                          "hub's bibliography", tag=t.div)
        st_space("v", "2vh")
        st_bibliography(title="", only_cited=False, format=CONFIG.format,
                        entry_style=bs.entry, number_style=bs.number)
