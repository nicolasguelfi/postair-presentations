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

_MARKER = {"en": "Skills 2030", "fr": "Compétences 2030"}
_TITLE = {"en": ("Learn ", (s.project.titles.keyword, "what"), ", then?"), "fr": ("Apprendre ", (s.project.titles.keyword, "quoi"), ", alors ?")}
_CITEKEYS = ["dondi2021-skills"]

_FAMILIES = [
    {"icon": "🧠", "label": {"en": "Cognitive", "fr": "Cognitives"},
     "line": {"en": "critical thinking · structured problems · storytelling", "fr": "esprit critique · problèmes structurés · narration"}},
    {"icon": "💻", "label": {"en": "Digital", "fr": "Numériques"},
     "line": {"en": "literacy · data · cybersecurity reflexes", "fr": "littératie numérique · données · réflexes de cybersécurité"}},
    {"icon": "🤝", "label": {"en": "Interpersonal", "fr": "Interpersonnelles"},
     "line": {"en": "teamwork · empathy · mobilising people", "fr": "travail d’équipe · empathie · mobiliser les autres"}},
    {"icon": "🚀", "label": {"en": "Self-leadership", "fr": "Leadership personnel"},
     "line": {"en": "learning to learn · grit · coping with uncertainty", "fr": "apprendre à apprendre · ténacité · vivre avec l’incertitude"}},
]

_PUNCH = {"en": ("the durable core: what the machine does NOT do",), "fr": ("le noyau durable : ce que la machine ne fait PAS",)}

_TIP_TITLE = {"en": "The study, precisely", "fr": "L’étude, précisément"}
_TOOLTIP = [
    ({"en": "The source", "fr": "La source"},
     {"en": ("McKinsey 2021: 18 000 respondents, 15 countries, 56 elementary "
             "skills (« DELTAs ») grouped in these four families — a "
             "consultancy survey, not peer-reviewed, dated on stage."), "fr": "McKinsey 2021 : 18 000 répondants, 15 pays, 56 compétences élémentaires (« DELTAs ») regroupées en ces quatre familles — une enquête de cabinet, non revue par les pairs, datée sur scène."}),
    ({"en": "How it links to G10", "fr": "Le lien avec G10"},
     {"en": ("The careers slide says HOW MUCH changes (WEF: 39 % of core "
             "skills by 2030); this one says TOWARD WHAT. One number there, "
             "four directions here."), "fr": "La slide carrières dit COMBIEN ça change (WEF : 39 % des compétences clés d’ici 2030) ; celle-ci dit VERS QUOI. Un chiffre là-bas, quatre directions ici."}),
    ({"en": "The AI twist", "fr": "La leçon IA"},
     {"en": ("Written before ChatGPT, the study aged tellingly: the four "
             "families held, the software lists did not — bet on the "
             "families, rent the tools."), "fr": "Écrite avant ChatGPT, l’étude a vieilli de façon parlante : les quatre familles ont tenu, les listes de logiciels non — misez sur les familles, louez les outils."}),
]


# ── La main de l'artiste ────────────────────────────────────────────────────
#: ``cols`` : les 4 familles sur UNE rangée (mesuré porte projection
#: 2026-09-02 : le 2×2 de ``balanced(4)`` débordait de ×1.23 à 1920×1080) —
#: plancher 21 % = 4 colonnes max, plancher 260px = repli responsive en
#: fenêtre étroite, même mécanique que ``balanced``.
TUNING = {
    "cols": "repeat(auto-fit, minmax(max(260px, 21%), 1fr))",
}


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
        with st_grid(cols=TUNING["cols"], gap="1.2vw",
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
