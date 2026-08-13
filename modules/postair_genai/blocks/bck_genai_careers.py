"""And for your future jobs? (G10) — transformation, not disappearance.

Three faculty cards (the visual loop with the morning's whole-university
slide), one frame line sourced with its visible citation code, and the rising
skill in amber. Data-driven from ``custom.facts``.

SPEAKER NOTES:
Three minutes, one card per third of the room, like the morning. The framing
number is behind the code — 39 % of core skills change by 2030 — say it with
its uncertainty: employer expectations, not destiny. Land on the amber line:
the skill that rises fastest is JUDGING what the AI produced, and judging
requires knowing the domain. That is why they are here for years, not weeks.
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
    faculty = s.project.body.pole_label + s.center_txt
    pair = s.project.titles.subtitle + s.project.colors.keyword + s.center_txt
    frame = s.project.body.body + s.center_txt
    rising = s.project.titles.subtitle + s.project.colors.amber + s.center_txt


bs = BlockStyles


def build():
    st_marker("Your jobs")
    careers = section("careers")
    frame = section("careers_frame")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "And for your ", (s.project.titles.keyword, "future jobs"),
                         "?", tag=t.div, toc_lvl="+1", label="Your jobs")
            with g.cell():
                st_info_tooltip(
                    title="What the evidence says",
                    entries=[(text(c["faculty"]), text(c["detail"])) for c in careers]
                            + [(text(frame["claim"]), text(frame["detail"])),
                               ("The durable skills", "Critical thinking, domain "
                                "expertise, ethics: piloting an AI requires knowing "
                                "the field better than it does.")],
                )
        st_space("v", "2vh")
        with st_grid(cols=s.project.grids.balanced(len(careers)), gap="1.2vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for c in careers:
                with g.cell(), st_block(s.project.cards.blue):
                    st_write(bs.faculty, text(c["faculty"]), tag=t.div)
                    st_space("v", "0.6vh")
                    # Silhouette humaine + orbe côte à côte (plan G10) : le
                    # duo est le visuel de la carte, pas une décoration.
                    st_html('<div style="text-align:center;padding:0.6vh 0;">'
                            '<span style="font-size:3.2vw;">👤</span>'
                            '<span style="font-size:2vw;color:#F2EEE6;"> + </span>'
                            '<span style="display:inline-block;width:2.6vw;height:2.6vw;'
                            'border-radius:50%;background:#F39C12;vertical-align:middle;">'
                            '</span></div>')
                    st_write(bs.pair, text(c["pair"]), tag=t.div)
        st_space("v", "2vh")
        # Télégraphique (NG 2026-08-13) : la phrase-cadre complète vit dans
        # l'infobulle ; l'écran porte la forme courte.
        st_write(bs.frame, text(frame["claim"]), " · ", text(frame["short"]), " ",
                 citation(*citekeys(frame)), tag=t.div)
        st_space("v", "1vh")
        st_write(bs.rising, text(frame["rising_skill"]), tag=t.div)
