"""What it gets wrong: hallucinations (G7) — the serious moment of the session.

The dominant visual is a REAL fabricated reference, projected verbatim: the
non-existent case ChatGPT invented and two lawyers filed in a New York federal
court. Nothing invented by us — the invention is the exhibit, its citation
code opens the sanctions order. Data-driven from ``custom.facts``.

SPEAKER NOTES:
Four minutes — slow down, this is the moment the whole deck exists for. Read
the fake citation aloud, let it sound respectable, THEN say it does not exist.
The three lines below are the lesson; the sourced hallucination rates are on
the middle card. Bridge to the guidelines session: high risk = delegating what
you cannot verify.
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
    fake = s.project.titles.subtitle + s.center_txt
    verdict = s.project.body.body + s.project.colors.coral + s.center_txt + s.bold
    claim = s.project.body.bullet + s.center_txt + s.bold
    detail = s.project.body.caption + s.center_txt


bs = BlockStyles


def build():
    st_marker("Hallucinations")
    data = section("hallucination")
    case = data["display_case"]
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "What it gets wrong: ",
                         (s.project.titles.keyword, "hallucinations"),
                         tag=t.div, toc_lvl="+1", label="Hallucinations")
            with g.cell():
                st_info_tooltip(
                    title="Why this is structural",
                    entries=[(text(c["short"]), text(c["detail"]))
                             for c in data["claims"]]
                            + [("The exhibit", text(case["verdict"]))],
                )
        st_space("v", "2vh")
        # La pièce à conviction : une « référence » très convenable — et fausse.
        with st_block(s.project.cards.coral):
            st_write(bs.fake, "« ", text(case["quote"]), " »", tag=t.div)
            st_space("v", "1vh")
            st_write(bs.verdict, "This case does not exist. ",
                     citation(*citekeys(case)), tag=t.div)
        st_space("v", "2vh")
        with st_grid(cols=s.project.grids.balanced(len(data["claims"])), gap="1.2vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for c in data["claims"]:
                with g.cell(), st_block(s.project.cards.blue):
                    st_write(bs.claim, text(c["short"]), tag=t.div)
                    keys = citekeys(c)
                    if keys:
                        st_write(bs.detail, citation(*keys), tag=t.div)
