"""Closing — the loop of the day (C1).

One dominant papercut image (the morning's campus, matured: the amber sun
higher and brighter) and the four steps of the day in a card row — posture,
understanding, practice, rules. Data-driven from ``custom.facts`` (section
``loop``).

SPEAKER NOTES:
Two minutes, warm. Walk the four cards in the day's order and land the
sentence: « you now have all four — your posture, the understanding, the
practice, and the rules. You have everything to start well. » The four decks
stay online; the next slide says where.
"""
# @guideline: postair-minimal

from custom.facts import citekeys, section, text
from custom.prompts import AI_PREFIX, AI_SUFFIX_LANDSCAPE
from custom.refs import citation
from custom.styles import Styles as s
from custom.visuals import hero_image
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    icon = s.project.titles.subtitle + s.center_txt
    label = s.project.body.bullet + s.center_txt + s.bold
    big = s.project.titles.subtitle + s.project.colors.amber + s.center_txt
    cite = s.project.body.caption + s.center_txt


bs = BlockStyles

_LOOP_PROMPT = (
    AI_PREFIX
    + "A stylised papercut university campus at midday, the warm amber paper "
      "sun now high and radiant above its towers, the whole scene brighter "
      "and warmer than dawn; a diverse crowd of small abstract paper "
      "silhouettes seen from behind walks OUT of the campus entrance toward "
      "the viewer, carrying small glowing paper lanterns."
    + AI_SUFFIX_LANDSCAPE
)


def build():
    st_marker("The loop")
    data = section("loop")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "You now have ", (s.project.titles.keyword, "all four"),
                         tag=t.div, toc_lvl="1", label="The loop")
            with g.cell():
                st_info_tooltip(
                    title="The day, in one sentence each",
                    entries=[(f"{st_['icon']} {text(st_['label'])}", text(st_["session"]))
                             for st_ in data["steps"]]
                            + [("The four documents", "All online, linked from the hub "
                                "on the next slide — they stay available after today.")],
                )
        st_space("v", "1vh")
        hero_image(
            "guide_loop", _LOOP_PROMPT, "images/guide_loop_fallback.svg",
            alt_ready=("Papercut campus at midday under a radiant amber sun, silhouettes "
                       "walking out carrying lanterns"),
            alt_fallback=("Papercut campus under a high amber sun, silhouettes leaving "
                          "with lanterns"),
            width="58%",
        )
        st_space("v", "1.5vh")
        with st_grid(cols=s.project.grids.balanced(len(data["steps"])), gap="1vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for step in data["steps"]:
                with g.cell(), st_block(s.project.cards.blue):
                    st_write(bs.icon, step["icon"], tag=t.div)
                    st_write(bs.label, text(step["label"]), tag=t.div)
        st_space("v", "1.5vh")
        st_write(bs.big, "You have everything to start well ",
                 citation(*citekeys(data)), tag=t.div)
