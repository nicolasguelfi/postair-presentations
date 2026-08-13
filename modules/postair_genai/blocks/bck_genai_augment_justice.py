"""The case file, read in full — justice (G6d, augmentation 3/3).

Le deuxième domaine de la vision augmentation (NG 2026-08-13) : sur dossier,
la prédiction de la machine bat celle du juge (Kleinberg, QJE 2018) et, en
laboratoire, le LLM suit le droit là où des juges réels suivent leur
sympathie (Posner & Saran 2026). Le contre-point Dressel & Farid est SUR la
slide, en caption sourcée — pas caché : l'honnêteté est la ligne du deck.
Le « 79 % » légendaire d'Aletras reste au tooltip, avec sa mise en garde.

SPEAKER NOTES:
Two minutes. The headline is a policy simulation, say the word "simulation"
— nobody replaced a judge. The lab result is the interesting one for
students: the machine had no mood, no sympathy, no hunger — constancy is
the tool's contribution. Close on the counterpoint caption: specialised
does not automatically mean better; that is why you must judge the tool.
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
    headline = s.project.body.name_double + s.project.colors.amber + s.center_txt
    sub = s.project.body.body + s.center_txt
    second = s.project.body.bullet + s.center_txt
    message = s.project.titles.subtitle + s.center_txt
    counterpoint = s.project.body.caption + s.center_txt


bs = BlockStyles

_HERO_PROMPT = (
    AI_PREFIX
    + "A large paper balance scale standing level: one pan holds a tall neat "
      "stack of paper case files in coral, turquoise and lilac cardstock, "
      "the other pan holds a single glowing warm amber paper orb; behind the "
      "scale a paper courthouse facade with simple cut-out columns. No human "
      "figures, no other sun or orb — the orb on the pan is the only one."
    + AI_SUFFIX_LANDSCAPE
)


def build():
    st_marker("Justice")
    fact = next(a for a in section("augment") if a["id"] == "justice")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "The case file, read ",
                         (s.project.titles.keyword, "in full"),
                         tag=t.div, toc_lvl="+1", label="Justice")
            with g.cell():
                st_info_tooltip(title=text(fact["label"]),
                                entries=[("Verified at the source",
                                          text(fact["detail"]))])
        st_space("v", "1vh")
        hero_image(
            "genai_justice", _HERO_PROMPT, "images/genai_justice_fallback.svg",
            alt_ready=("Papercut balance scale: a stack of paper case files on one "
                       "pan, a glowing amber orb on the other, courthouse behind"),
            alt_fallback=("Papercut balance scale weighing paper case files against "
                          "an amber orb"),
            width="48%",
        )
        st_space("v", "1.5vh")
        st_write(bs.headline, text(fact["headline"]), tag=t.div)
        st_write(bs.sub, text(fact["headline_sub"]), " ",
                 citation(*citekeys(fact)), tag=t.div)
        st_space("v", "1vh")
        st_write(bs.second, text(fact["second"]), " ",
                 citation(*fact["second_source"]["citekeys"]), tag=t.div)
        st_space("v", "1vh")
        st_write(bs.message, text(fact["message"]), tag=t.div)
        st_space("v", "0.5vh")
        st_write(bs.counterpoint, text(fact["counterpoint"]), " ",
                 citation(*fact["counterpoint_source"]["citekeys"]), tag=t.div)
