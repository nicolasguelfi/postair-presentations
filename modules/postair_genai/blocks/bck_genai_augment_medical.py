"""The diagnosis — 85 % vs 20 % (G6b, augmentation 1/3).

Première des trois slides « augmentation » (vision NG 2026-08-13) : l'IA
comme outil qui améliore massivement la qualité du résultat, chiffres
vérifiés à la source. Deux nombres géants face à face, l'image papier
découpé au centre, et la ligne de loyauté EN CLAIR sous le chiffre — les
conditions de l'étude font partie du message, pas des notes de bas de page.

SPEAKER NOTES:
Two minutes. Let the two numbers land before speaking. Then read the grey
loyalty line OUT LOUD — hardest published cases, physicians cut off from
internet and colleagues, preprint — the room must hear that you know the
study's limits; that is what makes the number credible. Bridge to next
slide: "so should the doctor just hand over? Watch the twist."
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
    number_ai = s.project.body.name_double + s.project.colors.amber + s.center_txt
    number_h = s.project.body.name_double + s.center_txt
    who = s.project.body.body + s.center_txt
    message = s.project.titles.subtitle + s.center_txt
    loyalty = s.project.body.caption + s.center_txt


bs = BlockStyles

_HERO_PROMPT = (
    AI_PREFIX
    + "A paper doctor as an abstract silhouette seen from behind, stethoscope "
      "shape cut from paper, facing a large glowing warm amber paper orb that "
      "projects light onto a big paper X-ray sheet held between them, the "
      "sheet showing a simple cut-out ribcage of turquoise and coral paper."
    + AI_SUFFIX_LANDSCAPE
)


def build():
    st_marker("Diagnosis")
    fact = next(a for a in section("augment") if a["id"] == "medical")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "The diagnosis: ",
                         (s.project.titles.keyword, "85 % vs 20 %"),
                         tag=t.div, toc_lvl="+1", label="Diagnosis")
            with g.cell():
                st_info_tooltip(title=text(fact["label"]),
                                entries=[("Verified at the source",
                                          text(fact["detail"]))])
        st_space("v", "1vh")
        hero_image(
            "genai_diagnosis", _HERO_PROMPT, "images/genai_diagnosis_fallback.svg",
            alt_ready=("Papercut doctor silhouette from behind, facing an amber orb "
                       "lighting a paper X-ray sheet"),
            alt_fallback=("Papercut doctor silhouette and amber orb studying a paper "
                          "X-ray together"),
            width="50%",
        )
        st_space("v", "1.5vh")
        with st_grid(cols="1fr 1fr", gap="2vw",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell(), st_block(s.project.cards.amber):
                st_write(bs.number_ai, text(fact["ai_value"]), tag=t.div)
                st_write(bs.who, text(fact["ai_label"]), tag=t.div)
            with g.cell(), st_block(s.project.cards.blue):
                st_write(bs.number_h, text(fact["human_value"]), tag=t.div)
                st_write(bs.who, text(fact["human_label"]), tag=t.div)
        st_space("v", "1.5vh")
        st_write(bs.message, text(fact["message"]), " ",
                 citation(*citekeys(fact)), tag=t.div)
        st_space("v", "0.5vh")
        st_write(bs.loyalty, text(fact["loyalty"]), tag=t.div)
