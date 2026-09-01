"""BACKUP · AI Act — la pyramide européenne du risque.

Annexe backup (planche drafts2 ``backsoc=aiact``, NG 2026-09-01) : LA
réponse à « c'est régulé ? » — et personne d'autre dans la journée ne la
donne (le deck guidelines couvre la charte de l'université, pas la loi).
Faits rafraîchis à la production (la table du draft datait d'avant
l'adoption) : Règlement (UE) 2024/1689, adopté juin 2024, application
échelonnée 2025-2027 — clé ``eu2024-aiact``, code visible.

Pure composition Style : trois niveaux empilés, zéro média.

SPEAKER NOTES:
Only if asked about regulation. Read the pyramid top-down: banned uses
(social scoring…); high-risk with strict obligations — and EDUCATION is on
that list, with hiring and justice; everything else, minimal. One date:
adopted 2024, applying in stages through 2027. Bridge if useful: what the
UNIVERSITY expects from you is the guidelines deck, later today.
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
    level = s.project.body.bullet + s.center_txt + s.bold
    line = s.project.body.caption + s.center_txt
    punch = s.project.titles.subtitle + s.project.colors.amber + s.center_txt
    cite = s.project.body.caption + s.center_txt


bs = BlockStyles

_MARKER = {"en": "AI Act"}
_TITLE = {"en": ("Regulated? ", (s.project.titles.keyword, "Yes — by risk"))}
_CITEKEYS = ["eu2024-aiact"]

#: La carte ambre porte le niveau qui concerne la salle (éducation).
_LEVELS = [
    {"accent": False, "level": {"en": "🚫 Unacceptable → BANNED"},
     "line": {"en": "social scoring · manipulative systems"}},
    {"accent": True, "level": {"en": "⚠️ High-risk → strict obligations"},
     "line": {"en": "EDUCATION & exams · hiring · justice · critical infrastructure"}},
    {"accent": False, "level": {"en": "✅ Minimal → transparency at most"},
     "line": {"en": "chatbots, filters, games — say it is an AI, and go"}},
]

_PUNCH = {"en": ("education is a HIGH-RISK sector — your university knows",)}

_TIP_TITLE = {"en": "The Act, precisely"}
_TOOLTIP = [
    ({"en": "The text"},
     {"en": ("Regulation (EU) 2024/1689, adopted June 2024 — the first "
             "horizontal AI law in the world; the pyramid comes from its "
             "articles 5-6 and annex III.")}),
    ({"en": "The calendar"},
     {"en": ("Staged application: bans since February 2025, general-purpose "
             "model duties since August 2025, most high-risk obligations "
             "2026-2027.")}),
    ({"en": "Why « education »"},
     {"en": ("Systems that grade you, admit you, or proctor your exams can "
             "change your life — annex III lists them with hiring, credit, "
             "justice and borders.")}),
    ({"en": "And the university?"},
     {"en": ("What UL expects from students is the guidelines deck, later "
             "today — the law binds providers and deployers, the charter "
             "binds YOU.")}),
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
        for lvl in _LEVELS:
            with st_block(s.project.cards.amber if lvl["accent"]
                          else s.project.cards.blue):
                with st_zoom(125):
                    st_write(bs.level, T(lvl["level"], lang), tag=t.div)
                    st_write(bs.line, T(lvl["line"], lang), tag=t.div)
            st_space("v", "1.5vh")
        st_space("v", "2vh")
        with st_zoom(130):
            for line in T(_PUNCH, lang):
                st_write(bs.punch, line, tag=t.div)
            st_write(bs.cite, citation(*_CITEKEYS), tag=t.div)
