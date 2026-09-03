"""L'objectif : un agent pour UN cours (M3) — le schéma, pas un chatbot.

Composition ``agentflow`` (v0.2, drafts NG 2026-09-01) : le schéma
[tes supports] + [tes consignes] → agent → [quiz · explications · plan] est
REFAIT aux jetons de la palette (cartes + flèches Style), jamais réutilisé en
capture des formations. Pure composition Style, zéro média.

Le FAIT vit ici (règle NG 2026-08-18) : les cartes du schéma s'éditent dans
ce bloc. Aucune affirmation sourcée sur cette slide.

SPEAKER NOTES:
Two minutes. Left to right, one sentence per box: you give it YOUR course and
YOUR rules; that makes an agent; the agent gives you quizzes, explanations
and a revision plan. Insist on « ONE course »: a generic chatbot knows
everything and your course nothing — the next slide gives the four steps.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    icon = s.project.titles.subtitle + s.center_txt
    label = s.project.body.bullet + s.center_txt + s.bold
    line = s.project.body.caption + s.center_txt
    arrow = s.project.titles.subtitle + s.project.colors.amber + s.center_txt + s.bold
    punch = s.project.titles.subtitle + s.project.colors.amber + s.center_txt


bs = BlockStyles

_MARKER = {"en": "The goal", "fr": "L’objectif"}
_TITLE = {"en": ("An agent for ", (s.project.titles.keyword, "ONE course")), "fr": ("Un agent pour ", (s.project.titles.keyword, "UN cours"))}

#: Le schéma en trois colonnes — entrées → agent → sorties.
_INPUTS = {
    "icon": "📚",
    "label": {"en": "YOUR inputs", "fr": "VOS entrées"},
    "lines": [{"en": "your course material", "fr": "vos supports de cours"},
              {"en": "your instructions", "fr": "vos consignes"}],
}
_AGENT = {
    "icon": "🤖",
    "label": {"en": "the agent", "fr": "l’agent"},
    "lines": [{"en": "knows THIS course", "fr": "connaît CE cours"},
              {"en": "follows YOUR rules", "fr": "suit VOS règles"}],
}
_OUTPUTS = {
    "icon": "🎯",
    "label": {"en": "what you get", "fr": "ce que vous obtenez"},
    "lines": [{"en": "quizzes · flashcards", "fr": "quiz · cartes mémoire"},
              {"en": "explanations · revision plan", "fr": "explications · plan de révision"}],
}

_PUNCH = {"en": "not a generic chatbot — an assistant that knows YOUR course", "fr": "pas un chatbot générique — un assistant qui connaît VOTRE cours"}

_TIP_TITLE = {"en": "An agent, precisely", "fr": "Un agent, précisément"}
_TOOLTIP = [
    ({"en": "The definition", "fr": "La définition"},
     {"en": ("A Mistral agent = system instructions (its role and limits) + "
             "your documents (what it answers from) + tools. You configure "
             "it once, then talk to it like a chat."), "fr": "Un agent Mistral = des instructions système (son rôle et ses limites) + vos documents (ce depuis quoi il répond) + des outils. Vous le configurez une fois, puis vous lui parlez comme à un chat."}),
    ({"en": "Chat vs agent", "fr": "Chat vs agent"},
     {"en": ("A chat starts from zero every conversation. An agent carries "
             "its role, its sources and its limits into EVERY conversation — "
             "that constancy is what makes it a study companion."), "fr": "Un chat repart de zéro à chaque conversation. Un agent emporte son rôle, ses sources et ses limites dans CHAQUE conversation — cette constance en fait un compagnon de révision."}),
    ({"en": "What it does NOT replace", "fr": "Ce qu’il ne remplace PAS"},
     {"en": ("The course, the professor, and your effort. An agent explains "
             "and drills; attending, understanding and learning stay yours — "
             "the fourth error slide shows why that matters."), "fr": "Le cours, le professeur et votre effort. Un agent explique et fait réviser ; assister, comprendre et apprendre restent à vous — la slide de la quatrième erreur montre pourquoi c’est important."}),
]

# ── La main de l'artiste ────────────────────────────────────────────────────
TUNING = {
    #: Colonnes du schéma : carte · flèche · carte · flèche · carte.
    "cols": "30% 5% 30% 5% 30%",
    "card_zoom": 150,
}


def _schema_card(card: dict, style, lang: str) -> None:
    with st_block(style):
        with st_zoom(130):
            st_write(bs.icon, card["icon"], tag=t.div)
        st_space("v", "1vh")
        with st_zoom(TUNING["card_zoom"]):
            st_write(bs.label, T(card["label"], lang), tag=t.div)
            st_space("v", "0.6vh")
            for line in card["lines"]:
                st_write(bs.line, T(line, lang), tag=t.div)


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with st_zoom(150), g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(T(h, lang), T(d, lang)) for h, d in _TOOLTIP],
                )
        st_space("v", s.project.spacing.title_gap)
        # Le schéma : l'agent au centre en AMBRE (le seul accent focal, R5),
        # entrées et sorties en cadrage bleu.
        with st_grid(cols=TUNING["cols"], gap="0",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                _schema_card(_INPUTS, s.project.cards.blue, lang)
            with g.cell():
                st_write(bs.arrow, "→", tag=t.div)
            with g.cell():
                _schema_card(_AGENT, s.project.cards.amber, lang)
            with g.cell():
                st_write(bs.arrow, "→", tag=t.div)
            with g.cell():
                _schema_card(_OUTPUTS, s.project.cards.blue, lang)
        # Punch resserré (porte projection 2026-09-02 : ×1.18 à 1728) — le
        # zoom 150 de NG ramené à 120, l'écart à 2vh.
        st_space("v", "2vh")
        with st_zoom(120):
            st_write(bs.punch, T(_PUNCH, lang), tag=t.div)
