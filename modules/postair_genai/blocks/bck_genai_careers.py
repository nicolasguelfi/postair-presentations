"""And for your future jobs? (G10) — transformation, not disappearance.

Three faculty cards (the visual loop with the morning's whole-university
slide), one frame line sourced with its visible citation code, and the rising
skill in amber.

Le FAIT vit ici (règle NG 2026-08-18) : cartes par faculté, ligne-cadre et
choix des citekeys s'éditent dans ce bloc. La phrase bibliographique reste
dérivée de ``references.bib`` par ``citation()``/``cite`` — clé inconnue =
erreur bruyante.

SPEAKER NOTES:
Three minutes, one card per third of the room, like the morning. The framing
number is behind the code — 39 % of core skills change by 2030 — say it with
its uncertainty: employer expectations, not destiny. Land on the amber line:
the skill that rises fastest is JUDGING what the AI produced, and judging
requires knowing the domain. That is why they are here for years, not weeks.
"""
# @guideline: postair-minimal

from custom.refs import citation
from custom.styles import Styles as s
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    faculty = s.project.body.pole_label + s.center_txt
    pair = s.project.titles.subtitle + s.project.colors.keyword + s.center_txt
    frame = s.project.body.body + s.center_txt
    rising = s.project.titles.subtitle + s.project.colors.amber + s.center_txt


bs = BlockStyles

# ── Les trois duos par faculté (carte projetée ; détail au survol) ──────────
#: Jamais projeté, gardé pour la vérifiabilité — les identifiants d'origine
#: des cartes : health, law, science.
_CAREERS = [
    {
        "faculty": "Medicine & health",
        "pair": "the clinician + AI",
        "detail": ("Imaging triage, protein structures, paperwork — and a "
                   "human who decides, explains and carries responsibility."),
    },
    {
        "faculty": "Law, economics, finance",
        "pair": "the jurist + AI",
        "detail": ("Research and drafting accelerate; judgement, strategy "
                   "and accountability do not delegate."),
    },
    {
        "faculty": "Science & engineering",
        "pair": "the researcher + AI",
        "detail": ("Hypothesis search, code, literature triage — and the "
                   "experiment, the proof and the doubt stay yours."),
    },
]

# ── La ligne-cadre (forme courte projetée ; phrase complète au survol) ──────
_FRAME_CLAIM = "Transformation, not disappearance"
_FRAME_DETAIL = ("Employers surveyed across 55 economies expect 39 % of core "
                 "skills to change by 2030; analytical thinking and AI "
                 "literacy top the rising list.")
_FRAME_SHORT = "55 economies · 39 % of core skills change → 2030"
_FRAME_RISING = "fastest-rising skill: JUDGING what the AI produced"
_FRAME_CITEKEYS = ["wef2025-jobs"]


def build(lang: str = "en", **_):
    st_marker("Your jobs")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "And for your ", (s.project.titles.keyword, "future jobs"),
                         "?", tag=t.div, toc_lvl="+1", label="Your jobs")
            with g.cell():
                st_info_tooltip(
                    title="What the evidence says",
                    entries=[(c["faculty"], c["detail"]) for c in _CAREERS]
                            + [(_FRAME_CLAIM, _FRAME_DETAIL),
                               ("The durable skills", "Critical thinking, domain "
                                "expertise, ethics: piloting an AI requires knowing "
                                "the field better than it does.")],
                )
        st_space("v", s.project.spacing.title_gap)
        with st_grid(cols=s.project.grids.balanced(len(_CAREERS)), gap="1.2vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for c in _CAREERS:
                with g.cell(), st_block(s.project.cards.blue):
                    st_write(bs.faculty, c["faculty"], tag=t.div)
                    st_space("v", "0.6vh")
                    # Silhouette humaine + orbe côte à côte (plan G10) : le
                    # duo est le visuel de la carte, pas une décoration.
                    st_html('<div style="text-align:center;padding:0.6vh 0;">'
                            '<span style="font-size:3.2vw;">👤</span>'
                            '<span style="font-size:2vw;color:#F2EEE6;"> + </span>'
                            '<span style="display:inline-block;width:2.6vw;height:2.6vw;'
                            'border-radius:50%;background:#F39C12;vertical-align:middle;">'
                            '</span></div>')
                    st_write(bs.pair, c["pair"], tag=t.div)
        st_space("v", "2vh")
        # Télégraphique (NG 2026-08-13) : la phrase-cadre complète vit dans
        # l'infobulle ; l'écran porte la forme courte.
        st_write(bs.frame, _FRAME_CLAIM, " · ", _FRAME_SHORT, " ",
                 citation(*_FRAME_CITEKEYS), tag=t.div)
        st_space("v", "1vh")
        st_write(bs.rising, _FRAME_RISING, tag=t.div)
