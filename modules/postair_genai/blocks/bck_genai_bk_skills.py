"""BACKUP · Skills 2030 — quelles compétences, après G10b.

Annexe backup (planche drafts2 ``backsoc=skills``, NG 2026-09-01) : LA
question d'étudiant après « project manager of your assistants » — « alors
j'apprends QUOI ? ». Les 56 « DELTAs » de l'enquête McKinsey (18 000
personnes, 15 pays) condensés en quatre familles ; la taxonomie détaillée
des formations AISE vit au panneau. Clé ``dondi2021-skills``, code visible —
étude de cabinet, dite comme telle.

Réconciliation avec G10 (obligation de la planche) : G10 projette le chiffre
WEF (39 % des compétences bougent d'ici 2030) ; ce backup répond « vers
QUOI » — jamais un second chiffre concurrent.

SPEAKER NOTES:
Only if asked « what should I learn? ». Sweep the four families: think
(critical thinking, communication), master the digital (literacy, data,
security), work with humans (teams, empathy), drive yourself (learning to
learn, grit). The punch, slowly: the durable core is what the machine does
NOT do. Date the study if challenged: 2021, pre-ChatGPT — its four families
aged well, its tool list did not.
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

_MARKER = {"en": "Skills 2030"}
_TITLE = {"en": ("Learn ", (s.project.titles.keyword, "what"), ", then?")}
_CITEKEYS = ["dondi2021-skills"]

_FAMILIES = [
    {"icon": "🧠", "label": {"en": "Cognitive"},
     "line": {"en": "critical thinking · structured problems · storytelling"}},
    {"icon": "💻", "label": {"en": "Digital"},
     "line": {"en": "literacy · data · cybersecurity reflexes"}},
    {"icon": "🤝", "label": {"en": "Interpersonal"},
     "line": {"en": "teamwork · empathy · mobilising people"}},
    {"icon": "🚀", "label": {"en": "Self-leadership"},
     "line": {"en": "learning to learn · grit · coping with uncertainty"}},
]

_PUNCH = {"en": ("the durable core: what the machine does NOT do",)}

_TIP_TITLE = {"en": "The study, precisely"}
_TOOLTIP = [
    ({"en": "The source"},
     {"en": ("McKinsey 2021: 18 000 respondents, 15 countries, 56 elementary "
             "skills (« DELTAs ») grouped in these four families — a "
             "consultancy survey, not peer-reviewed, dated on stage.")}),
    ({"en": "How it links to G10"},
     {"en": ("The careers slide says HOW MUCH changes (WEF: 39 % of core "
             "skills by 2030); this one says TOWARD WHAT. One number there, "
             "four directions here.")}),
    ({"en": "The AI twist"},
     {"en": ("Written before ChatGPT, the study aged tellingly: the four "
             "families held, the software lists did not — bet on the "
             "families, rent the tools.")}),
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
        with st_grid(cols=s.project.grids.balanced(len(_FAMILIES)), gap="1.2vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for f in _FAMILIES:
                with g.cell(), st_block(s.project.cards.blue):
                    with st_zoom(150):
                        st_write(bs.icon, f["icon"], tag=t.div)
                    st_space("v", "2vh")
                    with st_zoom(115):
                        st_write(bs.label, T(f["label"], lang), tag=t.div)
                        st_space("v", "1vh")
                        st_write(bs.line, T(f["line"], lang), tag=t.div)
        st_space("v", "5vh")
        with st_zoom(130):
            for line in T(_PUNCH, lang):
                st_write(bs.punch, line, tag=t.div)
            st_write(bs.cite, citation(*_CITEKEYS), tag=t.div)
