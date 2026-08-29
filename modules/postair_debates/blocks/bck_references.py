"""References — every BibTeX entry the deck's argument cards cite.

Rendered from the FROZEN ``static/data/references.bib`` by the streamtex
bibliography mechanism — the same entries the hover cards show, formatted
once, from one file. The freeze is produced by ``build_debates_content.py``
from the hub's bibliographies: nothing on this slide is typed, here or in
this repository.

Scope: the sources of the contemporary arguments AND of the historical
figures' quotations — since the hub promotion campaign of 2026-08-11, every
displayed quotation cites its bibliography key (``citekeys_confidence:
"cited"``), and ``--work-order`` reports any that would fall back.

Every entry is listed, not only the ones a given session happened to open:
the document is paginated, so the slides the speaker did not reach never ran,
and a "cited only" list would silently shrink to whatever was clicked that
morning.

SPEAKER NOTES:
Do not present this slide. Skip past it unless a contemporary argument is
challenged — then stop on it, find the line, and read the venue and the year
out loud. That is the whole point of having it.
"""
# @guideline: postair-minimal

from custom.refs import all_entries, config
from custom.styles import Styles as s
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    lead = s.project.body.caption + s.center_txt
    entry = s.project.body.caption
    number = s.project.body.caption + s.project.colors.keyword + s.bold


bs = BlockStyles


def build(lang: str = "en", **_):
    st_marker("References")
    # Le registre est rempli ici, pas ailleurs : cette slide est la seule qui
    # ait besoin de TOUTES les entrées, y compris celles des slides que la
    # séance n'a pas atteintes.
    all_entries()
    with st_block(s.project.containers.page_fill_top):
        st_write(bs.title, "Where the arguments ", (s.project.titles.keyword, "come from"),
                 tag=t.div, toc_lvl="1", label="References")
        st_space("v", "1vh")
        st_write(bs.lead, "every quotation and every contemporary argument of the nine axes, "
                          "with its source", tag=t.div)
        st_space("v", "2vh")
        st_bibliography(title="", only_cited=False, format=config().format,
                        entry_style=bs.entry, number_style=bs.number)
