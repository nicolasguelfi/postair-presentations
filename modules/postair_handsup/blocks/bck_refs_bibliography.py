"""References — everything this deck asserts, and where it comes from.

Rendered from ``static/data/references.bib`` by the streamtex bibliography
mechanism. Nothing on this slide is typed: it is the same entries the tooltips
show, formatted once, from one file.

It is not part of the talk. It exists so that a claim challenged from the floor
can be answered in five seconds with the paper on screen, and so that anyone who
asks afterwards can be sent to the document rather than to a memory.

Every entry is listed, not only the ones a given session happened to open: the
document is paginated, so the slides the speaker did not reach never ran, and a
"cited only" list would silently shrink to whatever was clicked that morning.

SPEAKER NOTES:
Do not present this slide. Skip past it unless someone asks — then stop on it,
find the line, and read the journal and the year out loud. That is the whole
point of having it.
"""
# @guideline: postair-minimal

from custom.refs import all_entries, config
from custom.styles import Styles as s
from postair_i18n import ui
from postair_lang import T, TF
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    lead = s.project.body.caption + s.center_txt
    entry = s.project.body.caption
    number = s.project.body.caption + s.project.colors.keyword + s.bold


bs = BlockStyles

# ── Feuilles projetées (règle R-i18n) ; « References » vient du lexique partagé.
_TITLE = {"en": ("Where all of this ", (s.project.titles.keyword, "comes from")), "fr": ("D'où tout cela ", (s.project.titles.keyword, "vient"))}
_LEAD = {"en": "the instrument this deck is built on, with its source", "fr": "l'instrument sur lequel repose ce deck, et sa source"}


def build(lang: str = "en", **_):
    st_marker(ui("references", lang))
    # Le registre est rempli ici, pas ailleurs : cette slide est la seule qui
    # ait besoin de TOUTES les entrées, y compris celles des slides que la
    # séance n'a pas atteintes.
    all_entries()
    with st_block(s.project.containers.page_fill_top):
        st_write(bs.title, *TF(_TITLE, lang),
                 tag=t.div, toc_lvl="1", label=ui("references", lang))
        st_space("v", "1vh")
        st_write(bs.lead, T(_LEAD, lang), tag=t.div)
        st_space("v", "2vh")
        st_bibliography(title="", only_cited=False, format=config().format,
                        entry_style=bs.entry, number_style=bs.number)
