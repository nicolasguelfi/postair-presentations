"""Justice 2/2 — in the lab (G6e, augmentation 4/4).

La seconde moitié du découpage justice (NG 2026-08-13) : le résultat Posner &
Saran (le LLM suit le précédent là où de vrais juges suivaient la sympathie),
le message « humeurs ≠ constance », et le garde-fou Dressel & Farid SUR la
slide — l'honnêteté est la ligne du deck. L'anecdote Unikowsky et la mise en
garde sur le « 79 % » légendaire restent dans l'infobulle de la slide 1/2.

Exception à la règle « le fait vit dans son bloc » (NG 2026-08-18) : l'entrée
``augment``/``justice`` est PARTAGÉE par les 2 slides justice et reste servie
par ``custom.facts`` — ce qui sert plusieurs slides vit dans ``custom/``. La
phrase bibliographique reste dérivée de ``references.bib`` par
``citation()``/``cite`` — clé inconnue = erreur bruyante.

SPEAKER NOTES:
Ninety seconds. The lab result is the one students should remember: the
machine had no mood, no hunger, no sympathy — constancy is the tool's
contribution, not wisdom. Close on the counterpoint: « specialised » is a
marketing word until it is measured — that is why YOU must judge the tool.
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
    second = s.project.body.bullet + s.center_txt
    message = s.project.titles.subtitle + s.project.colors.amber + s.center_txt + s.bold
    counterpoint = s.project.body.caption + s.center_txt


bs = BlockStyles

_HERO_PROMPT = (
    AI_PREFIX
    + "A paper judge's gavel resting on a stack of thick paper law books in "
      "coral and turquoise cardstock; beside the books, a single glowing "
      "warm amber paper orb rests level on the paper table, calm and still; "
      "a luminous paper window behind."
    + AI_SUFFIX_LANDSCAPE
)


def build(lang: str = "en", **_):
    st_marker("In the lab")
    fact = next(a for a in section("augment") if a["id"] == "justice")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "Justice — in the ",
                         (s.project.titles.keyword, "lab"),
                         tag=t.div, toc_lvl="+1", label="In the lab")
            with g.cell():
                st_info_tooltip(title=text(fact["label"]),
                                entries=[("Verified at the source",
                                          text(fact["detail"]))])
        st_space("v", s.project.spacing.title_gap)
        with hero_split(s, image=lambda: hero_image(
                "genai_justice_lab", _HERO_PROMPT,
                "images/genai_justice_fallback.svg",
                alt_ready=("Papercut gavel on law books, a calm amber orb resting "
                           "beside them"),
                alt_fallback=("Papercut balance scale weighing paper case files "
                              "against an amber orb"),
                variant="sq")):
            st_write(bs.second, text(fact["second"]), " ",
                     citation(*fact["second_source"]["citekeys"]), tag=t.div)
            st_space("v", "1vh")
            st_write(bs.message, text(fact["message"]), tag=t.div)
            st_space("v", "1vh")
            st_write(bs.counterpoint, text(fact["counterpoint"]), " ",
                     citation(*fact["counterpoint_source"]["citekeys"]), tag=t.div)
