"""The tools UL gives you (U6).

One dominant papercut image — the protected M365 bubble versus the open
cloud — and the three lines that matter: Copilot with the UL account is the
supported choice, UniGPT is staff-only for now, free public tools pay
themselves with your data. Equity rules in the tooltip. Data-driven from
``custom.facts`` (section ``tools``).

SPEAKER NOTES:
Two minutes. The image carries the model: inside the bubble, your data stays
UL's; outside, it is the product. Say the equity rule out loud — if a course
requires AI, a free path must exist; premium subscriptions must not buy
grades — it concerns every wallet in the room.
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
    line = s.project.body.bullet + s.center_txt
    accent = s.project.body.bullet + s.project.colors.amber + s.center_txt + s.bold
    cite = s.project.body.caption + s.center_txt


bs = BlockStyles

_BUBBLE_PROMPT = (
    AI_PREFIX
    + "A large transparent paper bubble dome sheltering a small papercut "
      "campus with a glowing warm amber paper orb inside it, cosy and safe. "
      "Outside the bubble, an open paper sky with scattered clouds and small "
      "paper documents flying away in the wind toward the horizon."
    + AI_SUFFIX_LANDSCAPE
)


def build():
    st_marker("UL tools")
    data = section("tools")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "The tools ", (s.project.titles.keyword, "UL gives you"),
                         tag=t.div, toc_lvl="+1", label="UL tools")
            with g.cell():
                st_info_tooltip(
                    title="Supported tools (guidelines, section 3, p.5)",
                    entries=[
                        ("Microsoft Copilot (UL account)", text(data["supported"])),
                        ("UniGPT", text(data["unigpt"])),
                        ("Public tools", text(data["outside"])),
                        *[("Equity", text(e)) for e in data["equity"]],
                    ],
                )
        st_space("v", s.project.spacing.title_gap)
        hero_image(
            "guide_bubble", _BUBBLE_PROMPT, "images/guide_bubble_fallback.svg",
            alt_ready=("Papercut protected bubble sheltering a small campus and an "
                       "amber orb, open windy sky with flying documents outside"),
            alt_fallback=("Papercut bubble protecting a campus, documents flying away "
                          "outside"),
            width="58%",
        )
        st_space("v", "1.5vh")
        st_write(bs.accent, "Copilot with your UL account — the supported choice",
                 tag=t.div)
        st_write(bs.line, "inside the bubble your data stays UL's · outside, it is "
                          "the product ", citation(*citekeys(data)), tag=t.div)
