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

_MARKER = {"en": "RAG", "fr": "RAG"}
_TITLE = {"en": ("Hallucinations: ", (s.project.titles.keyword, "the remedy")), "fr": ("Hallucinations : ", (s.project.titles.keyword, "le remède"))}
_CITEKEYS = ["lewis2020-rag"]

_STEPS = [
    {"icon": "📁", "label": {"en": "YOUR documents", "fr": "VOS documents"},
     "line": {"en": "course notes · manuals · the truth you trust", "fr": "notes de cours · manuels · la vérité de confiance"}},
    {"icon": "🔎", "label": {"en": "Search FIRST", "fr": "Chercher D’ABORD"},
     "line": {"en": "the question retrieves the relevant passages", "fr": "la question retrouve les passages pertinents"}},
    {"icon": "✍️", "label": {"en": "Answer FROM them", "fr": "Répondre À PARTIR d’eux"},
     "line": {"en": "grounded text · sources you can check", "fr": "texte ancré · sources vérifiables"}},
]

_PUNCH = {"en": ("fewer inventions — never zero",
                 "the Mistral session builds one, live"), "fr": ("moins d’inventions — jamais zéro", "la session Mistral en construit un, en direct")}

_TIP_TITLE = {"en": "RAG, precisely", "fr": "Le RAG, précisément"}
_TOOLTIP = [
    ({"en": "The name", "fr": "Le nom"},
     {"en": ("Retrieval-Augmented Generation: retrieve first, generate from "
             "what was retrieved — named in 2020, everywhere today."), "fr": "Retrieval-Augmented Generation : retrouver d’abord, générer à partir de ce qui a été retrouvé — nommé en 2020, partout aujourd’hui."}),
    ({"en": "Why it works", "fr": "Pourquoi ça marche"},
     {"en": ("G7's fabrications happen when the model completes from its "
             "training average. Anchoring the answer in retrieved passages "
             "replaces « plausible » with « found »."), "fr": "Les fabrications de G7 surviennent quand le modèle complète depuis sa moyenne d’entraînement. Ancrer la réponse dans des passages retrouvés remplace « plausible » par « trouvé »."}),
    ({"en": "The honest limit", "fr": "La limite honnête"},
     {"en": ("If retrieval misses the right passage, the model still invents. "
             "RAG shrinks the problem and makes it CHECKABLE (the sources are "
             "shown) — it does not delete it."), "fr": "Si la recherche manque le bon passage, le modèle invente encore. Le RAG réduit le problème et le rend VÉRIFIABLE (les sources sont affichées) — il ne le supprime pas."}),
    ({"en": "Where you meet it", "fr": "Où vous le croisez"},
     {"en": ("Chat tools with « attach a file », enterprise assistants, and "
             "the course agent of the Mistral session — its « no sources » "
             "failure is exactly this slide inverted."), "fr": "Les outils de chat avec « joindre un fichier », les assistants d’entreprise, et l’agent de cours de la session Mistral — sa panne « sans sources » est exactement cette slide inversée."}),
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
