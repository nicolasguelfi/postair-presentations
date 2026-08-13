"""Actor, not spectator (G11) — the loop back to the morning.

One dominant image — a silhouette facing the amber horizon — and three
mascots walking with it: curiosity, optimism, prudence. One line, three
verbs. Data-driven from ``custom.facts``; the mascots are asked by NAME
(``postair_data.mascot``), never by file.

SPEAKER NOTES:
One minute, almost no words. The morning asked « what is your posture? » ;
this slide answers « whatever it is, it is a compass, not a cage ». Say the
three verbs — stay informed, test things, keep doubting — and let the image
do the rest.
"""
# @guideline: postair-minimal

from custom.facts import citekeys, section, text
from custom.prompts import AI_PREFIX, AI_SUFFIX_LANDSCAPE
from custom.refs import citation
from custom.styles import Styles as s
from custom.visuals import hero_image
from postair_data import mascot
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.ai_mark import dd35_overlay


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    verbs = s.project.titles.subtitle + s.project.colors.amber + s.center_txt
    mascot_name = s.project.body.mascot_name + s.center_txt


bs = BlockStyles

_HORIZON_PROMPT = (
    AI_PREFIX
    + "A lone abstract paper silhouette seen from behind, walking toward a "
      "huge warm amber paper sun low on the horizon of a rolling papercut "
      "landscape, long soft shadows, a wide navy paper sky above."
    + AI_SUFFIX_LANDSCAPE
)


def build():
    st_marker("Actor")
    data = section("actor")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, (s.project.titles.keyword, "Actor"), ", not spectator",
                         tag=t.div, toc_lvl="+1", label="Actor")
            with g.cell():
                st_info_tooltip(
                    title="Your posture is your compass",
                    entries=[
                        ("The nine axes", "Trust, optimism, rationality — speed, "
                         "openness, control — centralisation, altruism, "
                         "transhumanism. Your radar from this morning."),
                        ("Not frozen", "A posture is a position, not an identity: it "
                         "moves when the evidence moves. Retake the survey in a year."),
                        ("Three companions", text(data["mascot_why"])),
                    ],
                )
        st_space("v", "1vh")
        hero_image(
            "genai_horizon", _HORIZON_PROMPT, "images/genai_horizon_fallback.svg",
            alt_ready=("Papercut silhouette from behind walking toward a large amber "
                       "sun on the horizon, navy sky"),
            alt_fallback=("Silhouette from behind facing an amber sun on the horizon, "
                          "three small companions beside it"),
            width="62%",
        )
        st_space("v", "1vh")
        st_write(bs.verbs,
                 " · ".join(text(v) for v in data["verbs"]), "   ",
                 citation(*citekeys(data)), tag=t.div)
        st_space("v", "1.5vh")
        # Les trois compagnons — demandés par leur NOM au cast gelé.
        names = data["mascots"]
        with st_grid(cols=s.project.grids.balanced(len(names)), gap="1vw",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for name in names:
                m = mascot(name)
                with g.cell():
                    st_image(s.project.cards.media_center, width="7vw",
                             uri=m["image"], alt=f"Mascot {m['name']}",
                             overlay=dd35_overlay())
                    st_write(bs.mascot_name, m["name"], tag=t.div)
