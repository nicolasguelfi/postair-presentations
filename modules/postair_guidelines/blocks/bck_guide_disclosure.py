"""Reflex 2 — say it: the five disclosure elements (U3).

Five big numbered cards — the visual IS the checklist — and the one-line
example disclaimer in amber below. Prompt-history advice and the Appendix 1
ready-made disclaimers live in the tooltip. Data-driven from ``custom.facts``
(section ``disclosure``).

SPEAKER NOTES:
Two minutes, one card each, fast. Land on the amber example: a disclosure is
ONE honest sentence, not a confession. Then the practical tip from the
tooltip, said out loud: teachers may ask for your prompt history — keep your
conversations. The wink is in the tooltip too: the appendix's own examples
were generated with Copilot, then revised.
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
    number = s.project.titles.subtitle + s.project.colors.keyword + s.center_txt + s.bold
    short = s.project.body.bullet + s.center_txt + s.bold
    example = s.project.titles.subtitle + s.project.colors.amber + s.center_txt
    cite = s.project.body.caption + s.center_txt


bs = BlockStyles


def build():
    st_marker("Say it")
    data = section("disclosure")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "Reflex 2 — ", (s.project.titles.keyword, "say it"),
                         tag=t.div, toc_lvl="+1", label="Say it")
            with g.cell():
                st_info_tooltip(
                    title="Disclosure (guidelines, section 2)",
                    entries=[(f"{i['n']} · {text(i['short'])}", text(i["detail"]))
                             for i in data["items"]]
                            + [("Keep your prompts", text(data["prompts_tip"])),
                               ("Appendix 1", text(data["annex_note"]))],
                )
        st_space("v", s.project.spacing.title_gap)
        with st_grid(cols=s.project.grids.balanced(len(data["items"])), gap="1vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for item in data["items"]:
                with g.cell(), st_block(s.project.cards.blue):
                    st_write(bs.number, item["n"], tag=t.div)
                    st_write(bs.short, text(item["short"]), tag=t.div)
        st_space("v", "2.5vh")
        st_write(bs.example, text(data["example"]), tag=t.div)
        st_write(bs.cite, "one honest sentence is enough ",
                 citation(*citekeys(data)), tag=t.div)
