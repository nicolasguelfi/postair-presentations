"""What it can do today (G6) — seven capabilities, agents in amber.

A grid of seven picto cards, one word each; the dated, sourced example behind
every capability lives in the tooltip. « Agents » is the single amber card of
the slide — it is the teaser for the Mistral session. Data-driven from
``custom.facts``.

SPEAKER NOTES:
Three minutes. One capability, one spoken example — the info panel has one per
faculty if the room needs it closer to home. Finish on the amber card and
plant the flag: « an agent is a model that uses tools in a loop to pursue a
goal — in the next session you will build one, live ».
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
    icon = s.project.titles.subtitle + s.center_txt
    label = s.project.body.bullet + s.center_txt + s.bold
    cite = s.project.body.caption + s.center_txt


bs = BlockStyles


def build():
    st_marker("What it can do")
    caps = section("capabilities")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "What it ", (s.project.titles.keyword, "can do"),
                         " today", tag=t.div, toc_lvl="+1", label="What it can do")
            with g.cell():
                st_info_tooltip(
                    title="One dated example each",
                    entries=[(f"{c['icon']} {text(c['label'])}", text(c["example"]))
                             for c in caps]
                            # Un exemple par faculté (plan G6) : chaque tiers
                            # de la salle se reconnaît dans au moins un.
                            + [(text(f["faculty"]), text(f["example"]))
                               for f in section("capability_faculty")],
                )
        st_space("v", "2vh")
        # Sept cartes sur une grille équilibrée ; « agents » est LA carte ambre.
        with st_grid(cols=s.project.grids.balanced(len(caps)), gap="1vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for c in caps:
                with g.cell(), st_block(s.project.cards.amber if c.get("accent")
                                        else s.project.cards.blue):
                    st_write(bs.icon, c["icon"], tag=t.div)
                    st_write(bs.label, text(c["label"]), tag=t.div)
                    keys = citekeys(c)
                    if keys:
                        st_write(bs.cite, citation(*keys), tag=t.div)
