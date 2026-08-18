"""The AI Act — you, concretely (U9b, découpage NG 2026-08-13).

La seconde moitié du découpage AI Act (1 idée = 1 slide) : ce que la loi
demande À L'ÉTUDIANT — les quatre cartes d'articles (numéros exigés par NG)
empilées à droite du visuel, et le punch fournisseur/émotions. La FAQ en
langage non-spécialiste reste au tooltip, identique à la slide précédente.

SPEAKER NOTES:
Two minutes. Walk the four cards top to bottom with their article numbers —
the machine-readable mark is the TOOL's duty, the visible deepfake label and
the never-strip rule are yours. Then the amber punch: build a tool and you
become a provider; emotion inference in education is simply forbidden. The
predictable question (« so EVERY generated image?? ») is answered in the FAQ
tooltip: art. 3(60), resemblance AND false authenticity.
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
    short = s.project.body.bullet + s.center_txt + s.bold
    article = s.project.body.body + s.project.colors.keyword + s.center_txt + s.bold
    punch = s.project.body.body + s.project.colors.amber + s.center_txt + s.bold
    cite = s.project.body.caption + s.center_txt


bs = BlockStyles

_TAGS_PROMPT = (
    AI_PREFIX
    + "A paper desk seen from above: four colourful paper parcels in a neat "
      "column, each parcel carrying a clearly visible little paper tag "
      "attached with paper string; a warm amber paper orb rests beside the "
      "column, a paper stamp and an ink pad nearby."
    + AI_SUFFIX_LANDSCAPE
)


def build():
    st_marker("You, concretely")
    data = section("ai_act")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "The AI Act — ",
                         (s.project.titles.keyword, "you, concretely"),
                         tag=t.div, toc_lvl="+1", label="You, concretely")
            with g.cell():
                st_info_tooltip(
                    title="Plain-language answers, with the article numbers",
                    entries=[(f"❓ {text(f['q'])}", text(f["a"]))
                             for f in data["faq"]]
                            + [(f"{c['icon']} {text(c['short'])} — {text(c['article'])}",
                                text(c["detail"])) for c in data["cards"]]
                            + [("Who enforces, where to complain",
                                text(data["channels"]))],
                )
        st_space("v", s.project.spacing.title_gap)
        with hero_split(s, zoom=88, image=lambda: hero_image(
                "guide_tags", _TAGS_PROMPT, "images/guide_aiact_fallback.svg",
                alt_ready=("Papercut parcels in a column, each with a visible paper "
                           "tag, an amber orb and a stamp beside them"),
                alt_fallback=("Papercut law book with labelled amber orbs around it"),
                variant="sq")):
            for c in data["cards"]:
                with st_block(s.project.cards.blue):
                    st_write(bs.short, c["icon"], " ", text(c["short"]), "  ",
                             (bs.article, text(c["article"])), tag=t.div)
            st_space("v", "0.5vh")
            st_write(bs.punch, text(data["punch"]), " ",
                     citation(*citekeys(data)), tag=t.div)
