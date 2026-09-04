"""The AI Act — you, concretely (U9b, découpage NG 2026-08-13).

La seconde moitié du découpage AI Act (1 idée = 1 slide) : ce que la loi
demande À L'ÉTUDIANT — les quatre cartes d'articles (numéros exigés par NG)
empilées à droite du visuel, et le punch fournisseur/émotions. La FAQ en
langage non-spécialiste reste au tooltip, identique à la slide précédente.

Data-driven from ``custom.facts`` (section ``ai_act``) — exception à la règle
NG 2026-08-18 (« le fait vit dans son bloc ») : la section est PARTAGÉE par
les 2 slides AI Act (U9 et U9b) et reste servie par ``facts.json`` — ce qui
sert plusieurs slides vit dans ``custom/``.

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
from postair_lang import T, TF
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

#: « AI Act » reste « AI Act » en français : nom propre du règlement.
_MARKER = {"en": "You, concretely", "fr": "Vous, concrètement"}
_TITLE = {"en": ("The AI Act — ", (s.project.titles.keyword, "you, concretely")), "fr": ("L’AI Act — ", (s.project.titles.keyword, "vous, concrètement"))}
_CHANNELS_HEAD = {"en": "Who enforces, where to complain", "fr": "Qui contrôle, où se plaindre"}
_TIP_TITLE = {"en": "Plain-language answers, with the article numbers", "fr": "Des réponses en langage courant, avec les numéros d’article"}

_TAGS_PROMPT = (
    AI_PREFIX
    + "A paper desk seen from above: four colourful paper parcels in a neat "
      "column, each parcel carrying a clearly visible little paper tag "
      "attached with paper string; a warm amber paper orb rests beside the "
      "column, a paper stamp and an ink pad nearby."
    + AI_SUFFIX_LANDSCAPE
)


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    data = section("ai_act")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(f"❓ {text(f['q'], lang)}", text(f["a"], lang))
                             for f in data["faq"]]
                            + [(f"{c['icon']} {text(c['short'], lang)} — {text(c['article'], lang)}",
                                text(c["detail"], lang)) for c in data["cards"]]
                            + [(T(_CHANNELS_HEAD, lang),
                                text(data["channels"], lang))],
                )
        st_space("v", s.project.spacing.title_gap)
        with hero_split(s, ratio=30, image=lambda: hero_image(
                "guide_tags", _TAGS_PROMPT, "images/guide_aiact_fallback.svg",
                alt_ready=("Papercut parcels in a column, each with a visible paper "
                           "tag, an amber orb and a stamp beside them"),
                alt_fallback=("Papercut law book with labelled amber orbs around it"),
                variant="sq")):
            for c in data["cards"]:
                with st_block(s.project.cards.blue):
                    st_write(bs.short, c["icon"], " ", text(c["short"], lang), "  ",
                             (bs.article, text(c["article"], lang)), tag=t.div)
            st_space("v", "0.5vh")
            st_write(bs.punch, text(data["punch"], lang), " ",
                     citation(*citekeys(data)), tag=t.div)
