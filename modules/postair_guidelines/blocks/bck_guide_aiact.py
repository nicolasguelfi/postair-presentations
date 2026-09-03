"""The law above the rules — the AI Act (U9, ajout NG 2026-08-12).

Depuis le 2 août 2026, l'AI Office et les autorités nationales font appliquer
l'AI Act, et les règles de transparence (art. 50) sont en vigueur : elles
concernent les productions des étudiants MÊME quand le cours autorise l'IA.
Rigueur académique exigée par NG : chaque notion porte son numéro d'article,
et la définition du deepfake (art. 3(60), verbatim au tooltip) répond à LA
confusion prévisible — non, une image générée n'est pas automatiquement un
deepfake. Fiche : ``_project/analysis/02-ai-act-etudiants.md``.

Data-driven from ``custom.facts`` (section ``ai_act``) — exception à la règle
NG 2026-08-18 (« le fait vit dans son bloc ») : la section est PARTAGÉE par
les 2 slides AI Act (U9 et U9b) et reste servie par ``facts.json`` — ce qui
sert plusieurs slides vit dans ``custom/``.

SPEAKER NOTES:
Three minutes, descriptive register — the law goes the same way as the
guidelines: say what the AI did. Walk the four cards with their article
numbers, then the amber line: build an AI and you become a provider; and
emotion inference in education is simply forbidden. If a hand rises on « so
every generated image must be labelled?? », the answer is card 2: read the
art. 3(60) definition from the tooltip — resemblance to real people/places
AND false appearance of authenticity. The timeline (high-risk in education,
December 2027) is in the tooltip too.
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
    since = s.project.body.caption + s.center_txt
    icon = s.project.titles.subtitle + s.center_txt
    short = s.project.body.caption + s.center_txt + s.bold
    article = s.project.body.caption + s.project.colors.keyword + s.center_txt + s.bold
    big = s.project.body.bullet + s.center_txt + s.bold
    punch = s.project.body.body + s.project.colors.amber + s.center_txt + s.bold
    cite = s.project.body.caption + s.center_txt


bs = BlockStyles

#: « AI Act » reste « AI Act » en français : nom propre du règlement.
_MARKER = {"en": "The AI Act", "fr": "L’AI Act"}
_TITLE = {"en": ("The law above the rules — the ", (s.project.titles.keyword, "AI Act")), "fr": ("La loi au-dessus des règles — l’", (s.project.titles.keyword, "AI Act"))}
_CHANNELS_HEAD = {"en": "Who enforces, where to complain", "fr": "Qui contrôle, où se plaindre"}
_TIP_TITLE = {"en": "Applicable law, with the article numbers", "fr": "La loi applicable, avec les numéros d’article"}

_AIACT_PROMPT = (
    AI_PREFIX
    + "A large open paper book of law on a paper pedestal, its pages cut from "
      "cream cardstock, a paper ribbon bookmark. Around and below it, several "
      "small warm amber paper orbs, each carrying a clearly visible little "
      "paper tag attached with paper string, like labelled parcels. Small "
      "abstract paper silhouettes seen from behind look at the book."
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
                    entries=[(f"{c['icon']} {text(c['short'], lang)} — {text(c['article'], lang)}",
                              text(c["detail"], lang)) for c in data["cards"]]
                            # FAQ en langage non-spécialiste (exigence NG) : qui est
                            # fournisseur/déployeur, que faire si l'outil ne marque
                            # pas, et ce qui vaut pour TOUTE image générée.
                            + [(f"❓ {text(f['q'], lang)}", text(f["a"], lang))
                               for f in data["faq"]]
                            + [(f"📅 {text(tl['when'], lang)}", text(tl["what"], lang))
                               for tl in data["timeline"]]
                            + [(T(_CHANNELS_HEAD, lang), text(data["channels"], lang))],
                )
        st_space("v", "0.5vh")
        st_write(bs.since, text(data["since"], lang), tag=t.div)
        st_space("v", "1vh")
        # Découpage NG (2026-08-13) : cette slide porte LA LOI (le cadre et
        # son calendrier) ; « vous, concrètement » (les 4 cartes d'articles et
        # le punch fournisseur) a SA slide, juste après.
        with hero_split(s, image=lambda: hero_image(
                "guide_aiact", _AIACT_PROMPT, "images/guide_aiact_fallback.svg",
                alt_ready=("Papercut open book of law on a pedestal, small amber "
                           "orbs around it each carrying a visible paper tag, "
                           "silhouettes watching"),
                alt_fallback=("Papercut law book with labelled amber orbs around it"),
                variant="sq")):
            with st_block(s.project.cards.amber):
                st_write(bs.big, text(data["big"], lang), tag=t.div)
            st_space("v", "0.5vh")
            for tl in data["timeline"]:
                st_write(bs.short, text(tl["when"], lang), " · ", text(tl["short"], lang),
                         tag=t.div)
            st_space("v", "0.5vh")
            st_write(bs.cite, citation(*citekeys(data)), tag=t.div)
