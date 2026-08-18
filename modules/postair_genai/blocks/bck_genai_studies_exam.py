"""And for your studies — the exam stays human (G9b).

Le versant exigeant du découpage : l'orbe attend derrière la porte de la
salle d'examen, et le paradoxe ferme la slide en ambre. Le chiffre HEPI porte
son code de citation visible.

SPEAKER NOTES:
Ninety seconds, slower than the previous slide. Read the amber paradox line
once, let it sit. The 94 % is not an accusation — it says the question is HOW,
not whether. Bridge: Mistral shows the how, the guidelines give the rules.
"""
# @guideline: postair-minimal

from custom.facts import section, text
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
    item = s.project.body.bullet + s.center_txt
    paradox = s.project.titles.subtitle + s.project.colors.amber + s.center_txt


bs = BlockStyles

_EXAM_PROMPT = (
    AI_PREFIX
    + "An exam room made of paper: one abstract paper silhouette seen from "
      "behind, writing alone at a small paper desk, a paper wall clock above "
      "— and outside the closed paper door, waiting patiently in the "
      "corridor, a warm amber paper orb."
    + AI_SUFFIX_LANDSCAPE
)


def build():
    st_marker("The exam")
    data = section("studies")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "The exam stays ", (s.project.titles.keyword, "human"),
                         tag=t.div, toc_lvl="+1", label="The exam")
            with g.cell():
                st_info_tooltip(
                    title="Tutor, not ghostwriter",
                    entries=[
                        ("Process originality", "What is graded is YOUR process: "
                         "drafts, choices, verification. Keeping your prompts and "
                         "versions is how you show it."),
                        ("The paradox", text(data["paradox"])),
                    ],
                )
        st_space("v", s.project.spacing.title_gap)
        with hero_split(s, zoom=92, image=lambda: hero_image(
                "genai_exam", _EXAM_PROMPT, "images/genai_exam_fallback.svg",
                alt_ready=("Papercut exam room: a silhouette writing alone at a "
                           "desk, an amber orb waiting outside the closed door"),
                alt_fallback=("Papercut exam room, silhouette writing, amber orb "
                              "waiting behind the closed door"),
                variant="pt")):
            for i, item in enumerate(data["dont"]):
                if i == len(data["dont"]) - 1:
                    st_write(bs.item, "▸ ", text(item), " ",
                             citation(*data["dont_source"]["citekeys"]), tag=t.div)
                else:
                    st_write(bs.item, "▸ ", text(item), tag=t.div)
            st_space("v", "1vh")
            # Le paradoxe — LE message de la slide — en carte ambre, VISIBLE :
            # il vivait sous le pli dans l'ancienne pile verticale.
            with st_block(s.project.cards.amber):
                st_write(bs.paradox, text(data["paradox"]), tag=t.div)
