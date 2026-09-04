"""Debate wrap-up — the whole cast, and the permission to change your mind.

The eighteen pole mascots are read from the frozen cast manifest and laid out
in ONE flat responsive grid: the full company on stage at the end of the act.
No plate image is needed — the grid is the plate, and it stays true when the
cast changes.

SPEAKER NOTES:
Two minutes to close. The room has just failed to agree, and some of them
will read that as the session having gone badly. Say the opposite, plainly:
on questions like these, a cohort that agreed would be a cohort that had not
thought. Then give them the two things they can take away — their posture is
a snapshot and it will move, and they can retake the survey later with the
same code to see how far. That lands better than any conclusion.
"""
# @guideline: postair-minimal

# ``from streamtex import *`` shadows the builtin ``list`` with the st_list
# module: annotations must stay unevaluated.
from __future__ import annotations

from custom.styles import Styles as s
from postair_data import REGISTERS, register_axes
from postair_i18n import ui
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.ai_mark import dd35_overlay


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    lead = s.project.body.bullet + s.center_txt
    mascot_name = s.project.body.mascot_name


bs = BlockStyles

# ── Le texte projeté (règle R-i18n) — marqueur et libellé : ui("no_consensus").
_TITLE = {"en": ("No consensus — and that is ", (s.project.titles.keyword, "normal")), "fr": ("Pas de consensus — et c'est ", (s.project.titles.keyword, "normal"))}
_LEAD = {"en": ("posture = ", (s.project.titles.keyword, "snapshot"), " → retake at year end"), "fr": ("posture = ", (s.project.titles.keyword, "instantané"), " → à refaire fin d'année")}
_TIP_TITLE = {"en": "After today", "fr": "Et après ?"}
_TIP = [
    ({"en": "A posture is a snapshot", "fr": "Une posture est un instantané"},
     {"en": ("It is where you stand today, with what you know today. The instrument "
             "measures a position, not a personality — and positions move, especially in "
             "a first year."), "fr": "C'est là où vous en êtes aujourd'hui, avec ce que vous savez aujourd'hui. L'instrument mesure une position, pas une personnalité — et les positions bougent, surtout en première année."}),
    ({"en": "Retake it later", "fr": "Refaites-le plus tard"},
     {"en": ("The same survey can be retaken at the end of the year with the same code. "
             "Comparing the two is the interesting part; most people are surprised by "
             "which axis moved."), "fr": "Le même sondage peut se refaire en fin d'année, avec le même code. L'intéressant, c'est de comparer les deux : la plupart des gens sont surpris par l'axe qui a bougé."}),
    ({"en": "Disagreement is the material", "fr": "Le désaccord est la matière"},
     {"en": ("Every one of these eighteen postures has been held, argued and written down "
             "by someone whose name is in the history of technology. None of them is a "
             "mistake."), "fr": "Chacune de ces dix-huit postures a été tenue, défendue et écrite par quelqu'un dont le nom est dans l'histoire des techniques. Aucune n'est une erreur."}),
    ({"en": "Where to go next", "fr": "Pour aller plus loin"},
     {"en": ("The afternoon sessions take the same questions to practice: how generative "
             "AI actually works, how to use it for study, and what the university's rules "
             "say."), "fr": "Les séances de l'après-midi mettent les mêmes questions à l'épreuve de la pratique : comment marche vraiment l'IA générative, comment étudier avec elle, et ce que disent les règles de l'université."}),
]


def _all_poles() -> list[dict]:
    """The eighteen pole mascots, in register order, accelerator first."""
    return [axis[kind]
            for code, _sub, _n in REGISTERS
            for axis in register_axes(code)
            for kind in ("accel", "decel")]


def build(lang: str = "en", **_):
    st_marker(ui("no_consensus", lang))
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="+1", label=ui("no_consensus", lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(T(h, lang), T(d, lang)) for h, d in _TIP],
                )
        st_space("v", s.project.spacing.title_gap)
        st_write(bs.lead, *TF(_LEAD, lang), tag=t.div)
        st_space("v", "1.5vh")
        # ONE flat grid, the full company: eighteen cells, wrapping naturally.
        company = _all_poles()
        with st_grid(cols=s.project.grids.balanced(len(company)), gap="0.6vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for pole in company:
                with g.cell():
                    st_image(s.project.cards.media_center, width="min(8vw, 15vh)",
                             uri=pole["image"],
                             alt=f"{pole['mascot']}, mascot of the {pole['label']} posture",
                             overlay=dd35_overlay(scale=0.5))
                    st_write(bs.mascot_name, pole["mascot"], tag=t.div)
