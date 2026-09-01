"""BACKUP · RAG — pourquoi ça hallucine moins avec des sources.

Annexe backup (planche drafts2 ``backtech=rag``, NG 2026-09-01) : LA réponse
à la question qui suit G7 (« comment on corrige les hallucinations ? »),
jamais présentée, ouverte à la demande. Le même schéma resservira derrière
M7 côté session Mistral (drafts3 ``methode=ragm7``) — une seule vérité de
composition, deux consommateurs.

Pure composition Style (stxonly=p1) : trois cartes, zéro média.

SPEAKER NOTES:
Only if asked. One sentence per card, left to right: give the model YOUR
documents; it searches them BEFORE answering; it answers FROM what it found,
sources shown. Then the honest limit: if the search misses, it still
hallucinates — RAG shrinks the problem, it does not delete it. Tease the
Mistral session: you will build exactly this, live.
"""
# @guideline: postair-minimal

from custom.refs import citation
from custom.styles import Styles as s
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    icon = s.project.titles.subtitle + s.center_txt
    label = s.project.body.bullet + s.center_txt + s.bold
    line = s.project.body.caption + s.center_txt
    punch = s.project.titles.subtitle + s.project.colors.amber + s.center_txt
    cite = s.project.body.caption + s.center_txt


bs = BlockStyles

_MARKER = {"en": "RAG"}
_TITLE = {"en": ("Hallucinations: ", (s.project.titles.keyword, "the remedy"))}
_CITEKEYS = ["lewis2020-rag"]

_STEPS = [
    {"icon": "📁", "label": {"en": "YOUR documents"},
     "line": {"en": "course notes · manuals · the truth you trust"}},
    {"icon": "🔎", "label": {"en": "Search FIRST"},
     "line": {"en": "the question retrieves the relevant passages"}},
    {"icon": "✍️", "label": {"en": "Answer FROM them"},
     "line": {"en": "grounded text · sources you can check"}},
]

_PUNCH = {"en": ("fewer inventions — never zero",
                 "the Mistral session builds one, live")}

_TIP_TITLE = {"en": "RAG, precisely"}
_TOOLTIP = [
    ({"en": "The name"},
     {"en": ("Retrieval-Augmented Generation: retrieve first, generate from "
             "what was retrieved — named in 2020, everywhere today.")}),
    ({"en": "Why it works"},
     {"en": ("G7's fabrications happen when the model completes from its "
             "training average. Anchoring the answer in retrieved passages "
             "replaces « plausible » with « found ».")}),
    ({"en": "The honest limit"},
     {"en": ("If retrieval misses the right passage, the model still invents. "
             "RAG shrinks the problem and makes it CHECKABLE (the sources are "
             "shown) — it does not delete it.")}),
    ({"en": "Where you meet it"},
     {"en": ("Chat tools with « attach a file », enterprise assistants, and "
             "the course agent of the Mistral session — its « no sources » "
             "failure is exactly this slide inverted.")}),
]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(T(h, lang), T(d, lang)) for h, d in _TOOLTIP],
                )
        st_space("v", s.project.spacing.title_gap)
        with st_grid(cols=s.project.grids.balanced(len(_STEPS)), gap="1.2vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for step in _STEPS:
                with g.cell(), st_block(s.project.cards.blue):
                    with st_zoom(150):
                        st_write(bs.icon, step["icon"], tag=t.div)
                    st_space("v", "2vh")
                    with st_zoom(120):
                        st_write(bs.label, T(step["label"], lang), tag=t.div)
                        st_space("v", "1vh")
                        st_write(bs.line, T(step["line"], lang), tag=t.div)
        st_space("v", "4vh")
        with st_zoom(130):
            for line in T(_PUNCH, lang):
                st_write(bs.punch, line, tag=t.div)
            st_write(bs.cite, citation(*_CITEKEYS), tag=t.div)
