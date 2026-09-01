"""The trick: predict the next word (G4) — THE pedagogical slide of the session.

Deux temps, un seul marqueur (revue genaipat 2026-09-01, pattern debates) :
d'abord la phrase à trou SEULE — la salle devine avant de voir quoi que ce
soit — puis, derrière un ``st_slide_break(marker_hidden=True)``, la
révélation : la même phrase, les trois candidats probabilisés, le punch.
PageDown s'arrête entre les deux ; la barre latérale ne liste qu'une slide.
Avant ce découpage la réponse était projetée avant la question — les notes
d'orateur décrivaient une révélation que la construction interdisait. Tokens,
temperature et le débat prédire-vs-comprendre vivent dans le tooltip.

Le FAIT vit ici (règle NG 2026-08-18) : la phrase à trou, les trois candidats
et le glossaire du panneau s'éditent dans ce bloc. Aucune affirmation sourcée
sur cette slide — quand une source arrive, la phrase bibliographique reste
dérivée de ``references.bib`` par ``citation()``/``cite`` — clé inconnue =
erreur bruyante.

SPEAKER NOTES:
Four minutes — take them. FIRST SCREEN: read the sentence aloud, stop at the
blank, let the room shout the word — the invitation is the whole point of
this screen, wait for the answers. THEN PageDown: the room just DID what a
language model does, and the 78 % bar says it better than any definition.
Then the honest turn: predicting well at this scale starts to look like
understanding, and whether it IS understanding is an open scientific debate —
say that the debate exists, it buys credibility for the whole deck.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.design_systems.postair_dark import AMBER, KEYWORD, PRIMARY


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    sentence = s.project.titles.slide_title + s.center_txt
    punch = s.project.titles.subtitle + s.project.colors.amber + s.center_txt
    word = s.project.body.bullet + s.bold
    prob = s.project.body.bullet


bs = BlockStyles

#: Barres de probabilité : la première est ambre (la réponse du modèle), les
#: suivantes bleu et teal — trois JETONS de la palette, jamais plus (R11,
#: revue genaipat 2026-09-01 : l'ancien st_html portait les hex en dur).
_BAR_COLOURS = [AMBER, PRIMARY, KEYWORD]

def _bar_html(share: float, idx: int) -> str:
    """La barre proportionnelle — ``st_html`` assumé (correctif 2026-09-01,
    capture NG : un ``st_block`` vide n'émet RIEN dans l'application) ;
    les couleurs restent les jetons de la palette."""
    width = max(share * 100, 1.5)          # la barre 0,1 % reste visible
    return (f'<div style="width:100%;background:rgba(255,255,255,0.06);'
            f'border-radius:0.6vh;">'
            f'<div style="width:{width}%;background:{_BAR_COLOURS[idx]};'
            f'height:3.2vh;border-radius:0.6vh;"></div></div>')

# ── La phrase à trou et ses candidats (probabilités illustratives) ──────────
#: La MÊME feuille sert les deux temps — la phrase répétée au temps 2 est
#: identique par construction.
_SENTENCE = {"en": ("« Luxembourg is a ",
                    (s.project.titles.keyword, "____"), " »")}
#: ``share`` pilote la largeur de barre, ``prob`` est l'étiquette projetée.
_CANDIDATES = [
    {"word": {"en": "country"}, "prob": "78 %", "share": 0.78},
    {"word": {"en": "grand duchy"}, "prob": "12 %", "share": 0.12},
    {"word": {"en": "cheese"}, "prob": "0.1 %", "share": 0.001},
]
#: Trois LIGNES, jamais un ``\n`` : ``st_write`` ne l'interprète pas (piège
#: documenté au PLAYBOOK) — la feuille porte un tuple, une écriture par ligne.
_PUNCH = {"en": ("Predict the next word", "= the WHOLE goal",
                 "at scale: enormous")}

# ── Les feuilles {en} du bloc (structure i18n, lot C genaipat 2026-09-01) ────
_MARKER = {"en": "Predict"}
_TITLE = {"en": ("The trick: ", (s.project.titles.keyword, "predict the next word"))}

# ── Le glossaire du panneau « What is really happening » ────────────────────
_TIP_TITLE = {"en": "What is really happening"}
_TOOLTIP = [
    ({"en": "Tokens"},
     {"en": ("The model reads and writes in fragments of words (tokens), a few "
             "characters each. « Luxembourg » is 2–3 tokens.")}),
    ({"en": "Probabilities"},
     {"en": ("For every next token the model scores its whole vocabulary and samples "
             "among the most probable — learned from billions of pages of text.")}),
    ({"en": "Temperature"},
     {"en": ("A dial on the sampling: low = always the safest word, high = more "
             "surprising choices. Same question, different answers — by design, not "
             "by bug.")}),
    ({"en": "Predicting vs understanding"},
     {"en": ("To predict well at this scale, models build internal representations "
             "of grammar, facts and reasoning patterns. Whether that deserves the "
             "word « understanding » is an open scientific debate — honest people "
             "disagree.")}),
]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    # ── Temps 1 : la phrase à trou SEULE — la salle devine d'abord ──────────
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                with st_zoom(120):
                    st_write(bs.title, *TF(_TITLE, lang),
                            tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(T(h, lang), T(d, lang)) for h, d in _TOOLTIP],
                )
        # La phrase descend vers le centre de l'écran : elle est seule en
        # scène sur ce premier temps, elle occupe la fenêtre (règle amphi).
        st_space("v", "30vh")
        with st_zoom(200):
            st_write(bs.sentence, *TF(_SENTENCE, lang), tag=t.div)
    # Arrêt clavier SANS entrée de barre latérale (pattern debates) : la
    # config globale du book (FULL, 30vh) s'applique.
    st_slide_break(marker_hidden=True)
    # ── Temps 2 : la révélation — la phrase, les candidats, le punch ────────
    with st_block(s.project.containers.page_fill_top):
        # Chaque sous-slide est AUTOSUFFISANTE (pattern debates) : le panneau
        # d'info vit aussi sur ce temps — l'en-tête du temps 1 est hors écran
        # après le PageDown, son ℹ️ avec lui (constat NG 2026-09-01).
        with st_grid(cols="92% 8%",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.sentence, *TF(_SENTENCE, lang), tag=t.div)
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(T(h, lang), T(d, lang)) for h, d in _TOOLTIP],
                )
        st_space("v", "10vh")
        # Les trois candidats : mot, barre proportionnelle, probabilité.
        for i, cand in enumerate(_CANDIDATES):
            with st_zoom(150):
                with st_grid(cols="30% 52% 18%",
                            cell_styles=s.project.containers.grid_cell_centered) as g:
                    with g.cell():
                        st_write(bs.word, T(cand["word"], lang), tag=t.div)
                    with g.cell():
                        st_html(_bar_html(cand["share"], i))
                    with g.cell():
                        st_write(bs.prob, cand["prob"], tag=t.div)
            st_space("v", "1vh")
        st_space("v", "2vh")
        with st_zoom(150):
            for line in T(_PUNCH, lang):
                st_write(bs.punch, line, tag=t.div)
