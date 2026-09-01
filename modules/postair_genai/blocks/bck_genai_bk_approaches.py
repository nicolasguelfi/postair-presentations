"""BACKUP · 4 approaches — la carte mentale « améliorer un LLM ».

Annexe backup (planche drafts2 ``backtech=approches``, NG 2026-09-01) : le
vocabulaire qu'un étudiant avancé peut lancer en questions — prompt
engineering, RAG, fine-tuning, modèle spécialisé — situé en UNE image, du
geste gratuit au chantier lourd. Les critères de choix vivent au panneau
(la taxonomie des formations AISE, condensée).

Pure composition Style : quatre cartes, zéro média. Vocabulaire, pas
d'affirmation sourcée : pas de citekey.

SPEAKER NOTES:
Only if an insider asks (« couldn't you fine-tune it? »). Sweep left to
right: write better prompts (free, minutes); give it your documents (cheap,
hours); retrain it on your examples (costly, weeks); build a domain model
(heavy, months). Land on the punch: most real needs stop at the first two —
which is exactly what the Mistral session teaches.
"""
# @guideline: postair-minimal

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


bs = BlockStyles

_MARKER = {"en": "4 approaches"}
_TITLE = {"en": ("Four ways to ", (s.project.titles.keyword, "improve a model"))}

_APPROACHES = [
    {"icon": "💬", "label": {"en": "Prompt engineering"},
     "line": {"en": "ask better · free · minutes"}},
    {"icon": "📚", "label": {"en": "RAG"},
     "line": {"en": "add YOUR documents · cheap · hours"}},
    {"icon": "🔧", "label": {"en": "Fine-tuning"},
     "line": {"en": "retrain on your examples · costly · weeks"}},
    {"icon": "🏗️", "label": {"en": "Specialised model"},
     "line": {"en": "build for one domain · heavy · months"}},
]

_PUNCH = {"en": ("most real needs stop at the first two",)}

_TIP_TITLE = {"en": "Choosing, precisely"}
_TOOLTIP = [
    ({"en": "The gradient"},
     {"en": ("Left to right: rising cost, rising specialisation, falling "
             "generality. Start left; move right only when measured quality "
             "says so.")}),
    ({"en": "Choose based on"},
     {"en": ("Result quality needed · domain specificity · dataset quality "
             "and size · resources · development time — the AISE criteria "
             "grid, five questions before any chantier.")}),
    ({"en": "Where the deck stands"},
     {"en": ("The Mistral session lives entirely in the first two columns: "
             "a well-framed prompt plus your course documents — the 80/20 of "
             "this whole map.")}),
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
        with st_grid(cols=s.project.grids.balanced(len(_APPROACHES)), gap="1.2vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for a in _APPROACHES:
                with g.cell(), st_block(s.project.cards.blue):
                    with st_zoom(150):
                        st_write(bs.icon, a["icon"], tag=t.div)
                    st_space("v", "2vh")
                    with st_zoom(115):
                        st_write(bs.label, T(a["label"], lang), tag=t.div)
                        st_space("v", "1vh")
                        st_write(bs.line, T(a["line"], lang), tag=t.div)
        st_space("v", "5vh")
        with st_zoom(130):
            for line in T(_PUNCH, lang):
                st_write(bs.punch, line, tag=t.div)
