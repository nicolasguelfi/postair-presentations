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

from custom.refs import all_entries, config
from custom.styles import Styles as s
from postair_lang import T, TF
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    lead = s.project.body.caption + s.center_txt
    entry = s.project.body.caption
    number = s.project.body.caption + s.project.colors.keyword + s.bold


bs = BlockStyles

_MARKER = {"en": "References", "fr": "Références"}
_TITLE = {"en": ("Where the frame ", (s.project.titles.keyword, "comes from")), "fr": ("Le cadre et ", (s.project.titles.keyword, "ses sources"))}
_LEAD = {"en": "the theoretical frame of the deck — frozen from the "
               "hub's bibliography", "fr": "le cadre théorique du deck — gelé à partir de la bibliographie du hub"}


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    all_entries()
    with st_block(s.project.containers.page_fill_top):
        st_write(bs.title, *TF(_TITLE, lang),
                 tag=t.div, toc_lvl="1", label=T(_MARKER, lang))
        st_space("v", "1vh")
        st_write(bs.lead, T(_LEAD, lang), tag=t.div)
        st_space("v", "2vh")
        st_bibliography(title="", only_cited=False, format=config().format,
                        entry_style=bs.entry, number_style=bs.number)
