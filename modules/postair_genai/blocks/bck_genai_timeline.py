"""Seventy years in one frieze (G3) — seven milestones, amber rising rightward.

Data-driven from ``custom.facts``: milestones, wording and citation keys live
in ``facts.json``. The frieze is drawn in HTML — crisp at any projection size,
and the amber warms up milestone by milestone toward today: the point of the
slide IS that gradient (nothing magical, a long history and a recent tipping
point).

Each milestone card carries its citation code in the visible text — full
reference on hover, canonical bib rule.

SPEAKER NOTES:
Three minutes, half a minute per milestone, walking left to right. Insist on
the two winters — promises outran results twice, and the room should hear
that this can happen again. Land on 2022: what changed is not the idea, it is
that it arrived in everyone's pocket at once.
"""
# @guideline: postair-minimal

from custom.facts import citekeys, section, text
from custom.refs import citation
from custom.styles import Styles as s
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    year = s.project.titles.subtitle + s.center_txt + s.bold
    label = s.project.body.caption + s.center_txt + s.bold
    cite = s.project.body.caption + s.center_txt


bs = BlockStyles

#: L'ambre monte vers la droite : interpolation bleu → ambre par jalon.
#: C'est le message visuel de la slide — la chaleur récente d'une longue
#: histoire — donc il vit ici, pas dans un style partagé.
_DOT_COLOURS = ["#7AB8F5", "#8FB0E0", "#A8A8C8", "#C4A06E", "#D9973F",
                "#F39C12", "#F39C12"]


def build():
    st_marker("70 years")
    milestones = section("timeline")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, (s.project.titles.keyword, "Seventy years"),
                         " in one line", tag=t.div, toc_lvl="+1", label="70 years")
            with g.cell():
                st_info_tooltip(
                    title="The milestones, one sentence each",
                    entries=[(f"{m['year']} — {text(m['label'])}", text(m["detail"]))
                             for m in milestones],
                )
        st_space("v", s.project.spacing.title_gap)
        # La frise : une carte par jalon, point coloré + année + étiquette +
        # code de citation. La ligne est portée par la rangée de points.
        with st_grid(cols=s.project.grids.balanced(len(milestones)), gap="0.8vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for i, m in enumerate(milestones):
                with g.cell(), st_block(s.project.cards.blue):
                    st_html(f'<div style="text-align:center;padding-top:0.5vh;">'
                            f'<span style="display:inline-block;width:1.6vw;height:1.6vw;'
                            f'border-radius:50%;background:{_DOT_COLOURS[i]};"></span></div>')
                    st_write(bs.year, m["year"], tag=t.div)
                    st_write(bs.label, text(m["label"]), tag=t.div)
                    keys = citekeys(m)
                    if keys:
                        st_write(bs.cite, citation(*keys), tag=t.div)
