"""Erreur n°1 — Pas de sources : l'agent invente ton cours (M7).

LE mode de défaillance en contexte pointu — à marteler. Le choix pédagogique
du plan : l'erreur est MONTRÉE, pas énoncée. La capture réelle (même question
posée à l'agent SANS documents → réponse plausible mais fausse par rapport au
cours) se produit PENDANT LA RÉPÉTITION sur le cours-exemple et remplacera la
colonne gauche ; d'ici là la paire de cartes porte le contraste.

Le FAIT vit ici (règle NG 2026-08-18) : les deux cartes s'éditent dans ce
bloc. Le POURQUOI (le RAG) vit dans le backup ``bck_mistral_bk_rag`` — jamais
projeté dans les 20', ouvert si un curieux demande la mécanique.

SPEAKER NOTES:
Two minutes. Hammer it: this is THE failure mode in a specialised context.
Without your documents the model completes with its average of the web — a
definition that is plausible, fluent, and NOT your professor's. Every course
has ITS notations. Show the fix in one line: ask the agent to cite the
section; no citation, no trust. If someone asks WHY it works — the RAG
backup slide is two clicks away.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    head = s.project.body.pole_label + s.center_txt
    line = s.project.body.bullet + s.center_txt
    bad = s.project.body.pole_label + s.project.colors.coral + s.center_txt + s.bold
    good = s.project.body.pole_label + s.project.colors.keyword + s.center_txt + s.bold
    punch = s.project.titles.subtitle + s.project.colors.amber + s.center_txt


bs = BlockStyles

_MARKER = {"en": "Error: no sources", "fr": "Erreur : sans sources"}
_TITLE = {"en": ("Error 1 — no sources: it ", (s.project.titles.keyword, "invents your course")), "fr": ("Erreur 1 — sans sources : il ", (s.project.titles.keyword, "invente votre cours"))}

#: La paire de contraste — remplacée à la répétition par la capture réelle
#: (gauche) et sa correction (droite), produites dans Le Chat.
_WITHOUT = {
    "head": {"en": "WITHOUT your documents", "fr": "SANS vos documents"},
    "lines": [{"en": "plausible · fluent · generic", "fr": "plausible · fluide · générique"},
              {"en": "the web's average definition", "fr": "la définition moyenne du web"},
              {"en": "≠ YOUR professor's notation", "fr": "≠ la notation de VOTRE professeur"}],
    "verdict": {"en": "wrong for YOUR exam", "fr": "faux pour VOTRE examen"},
}
_WITH = {
    "head": {"en": "WITH your documents", "fr": "AVEC vos documents"},
    "lines": [{"en": "grounded in the course", "fr": "ancré dans le cours"},
              {"en": "cites the section", "fr": "cite la section"},
              {"en": "your professor's vocabulary", "fr": "le vocabulaire de votre professeur"}],
    "verdict": {"en": "checkable", "fr": "vérifiable"},
}

_TIP_TITLE = {"en": "Why, and how to check", "fr": "Pourquoi, et comment vérifier"}
_TOOLTIP = [
    ({"en": "Why it invents", "fr": "Pourquoi il invente"},
     {"en": ("A language model completes with the most plausible "
             "continuation from its training data — the average of the web, "
             "not YOUR course. In a specialised context the error is fine: "
             "a definition that differs by one clause, a notation that "
             "differs by one symbol."), "fr": "Un modèle de langue complète avec la suite la plus plausible de ses données d’entraînement — la moyenne du web, pas VOTRE cours. En contexte pointu, l’erreur est fine : une définition qui diffère d’une proposition, une notation qui diffère d’un symbole."}),
    ({"en": "How to check the sources are used", "fr": "Comment vérifier que les sources servent"},
     {"en": ("Ask the agent to cite the section of the course with every "
             "answer (it is among the limits framed in step 1). An answer "
             "without a section is an answer from the average — challenge "
             "it."), "fr": "Demandez à l’agent de citer la section du cours à chaque réponse (c’est une des limites cadrées à l’étape 1). Une réponse sans section est une réponse de la moyenne — contestez-la."}),
    ({"en": "The vocabulary trap", "fr": "Le piège du vocabulaire"},
     {"en": ("Every professor has their OWN notations and definitions. The "
             "generic version can be « right » in general and wrong in your "
             "exam — the exam grades your course, not the web."), "fr": "Chaque professeur a SES notations et SES définitions. La version générique peut être « juste » en général et fausse à votre examen — l’examen note votre cours, pas le web."}),
]

# ── La main de l'artiste ────────────────────────────────────────────────────
#: Resserrée (porte projection 2026-09-02 : ×1.12/×1.15 avec le 130) —
#: cartes à 110, en-têtes/verdicts à 110.
TUNING = {
    "card_zoom": 130,
}


def _contrast_card(card: dict, style, head_style, verdict_style, lang: str) -> None:
    with st_block(style):
        with st_zoom(105):
            st_write(head_style, T(card["head"], lang), tag=t.div)
        st_space("v", "1vh")
        with st_zoom(TUNING["card_zoom"]):
            for line in card["lines"]:
                st_write(bs.line, T(line, lang), tag=t.div)
        st_space("v", "1vh")
        with st_zoom(105):
            st_write(verdict_style, T(card["verdict"], lang), tag=t.div)


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
        with st_grid(cols="50% 50%", gap="1.5vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_stretch) as g:
            with g.cell():
                _contrast_card(_WITHOUT, s.project.cards.coral, bs.bad, bs.bad, lang)
            with g.cell():
                _contrast_card(_WITH, s.project.cards.teal, bs.good, bs.good, lang)

