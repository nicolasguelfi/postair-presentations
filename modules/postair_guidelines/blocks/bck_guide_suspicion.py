"""If misuse is suspected (U7).

One dominant papercut image (the balanced scale of justice — balanced, unlike
the bias slide of the GenAI session) and three cards: standard procedure,
detection is not proof (sourced, citation codes visible), your process
protects you. Data-driven from ``custom.facts`` (section ``suspicion``).

SPEAKER NOTES:
One minute, reassuring: the procedure is the standard one, solid evidence is
required, and a « detector » alone is never enough — the sources behind that
sentence are one hover away. The practical takeaway is the third card: keep
your drafts and prompts, showing your process is your best defence.
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

from postair_pack.components.hero_split import hero_split


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    icon = s.project.titles.subtitle + s.center_txt
    short = s.project.body.caption + s.center_txt + s.bold
    line = s.project.body.bullet + s.project.colors.amber + s.center_txt + s.bold
    cite = s.project.body.caption + s.center_txt


bs = BlockStyles

_BALANCE_PROMPT = (
    AI_PREFIX
    + "A perfectly balanced paper scale of justice standing on a small paper "
      "pedestal, both pans level, in front of a calm luminous paper sky; a "
      "small warm amber paper orb rests gently in one pan, a stack of small "
      "paper documents of equal weight in the other."
    + AI_SUFFIX_LANDSCAPE
)


def build():
    st_marker("If suspected")
    data = section("suspicion")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "If misuse is ", (s.project.titles.keyword, "suspected"),
                         tag=t.div, toc_lvl="+1", label="If suspected")
            with g.cell():
                st_info_tooltip(
                    title="The procedure (guidelines, section 4)",
                    entries=[(f"{c['icon']} {text(c['short'])}", text(c["detail"]))
                             for c in data["cards"]],
                )
        st_space("v", s.project.spacing.title_gap)
        # Gabarit par défaut (NG 2026-08-13) : balance carrée à gauche, les
        # quatre garanties EMPILÉES à droite (le pavé d'une seule ligne se
        # lisait comme un paragraphe).
        with hero_split(s, image=lambda: hero_image(
                "guide_balance", _BALANCE_PROMPT,
                "images/guide_balance_fallback.svg",
                alt_ready=("Papercut balanced scale of justice, an amber orb in one "
                           "pan and documents in the other, calm sky"),
                alt_fallback=("Papercut balanced scale of justice"),
                variant="sq")):
            for part in text(data["line"]).split(" · "):
                st_write(bs.line, "▸ ", part, tag=t.div)
            st_space("v", "0.5vh")
            st_write(bs.cite, citation(*citekeys(data)), tag=t.div)
