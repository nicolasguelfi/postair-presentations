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
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    sentence = s.project.titles.slide_title + s.center_txt
    punch = s.project.titles.subtitle + s.project.colors.amber + s.center_txt
    word = s.project.body.bullet + s.bold
    prob = s.project.body.bullet


bs = BlockStyles

#: Barres de probabilité : la première est ambre (la réponse du modèle), les
#: suivantes bleu et teal — trois couleurs de la ligne, jamais plus.
_BAR_COLOURS = ["#F39C12", "#7AB8F5", "#2EC4B6"]

# ── La phrase à trou et ses candidats (probabilités illustratives) ──────────
_SENTENCE_HEAD = "Luxembourg is a"
_BLANK = "____"
#: ``share`` pilote la largeur de barre, ``prob`` est l'étiquette projetée.
_CANDIDATES = [
    {"word": "country", "prob": "78 %", "share": 0.78},
    {"word": "grand duchy", "prob": "12 %", "share": 0.12},
    {"word": "cheese", "prob": "0.1 %", "share": 0.001},
]
_PUNCH = "Predict the next word = the WHOLE mechanism · at scale: enormous"

# ── Le glossaire du panneau « What is really happening » ────────────────────
_TOOLTIP = [
    ("Tokens",
     "The model reads and writes in fragments of words (tokens), a few "
     "characters each. « Luxembourg » is 2–3 tokens."),
    ("Probabilities",
     "For every next token the model scores its whole vocabulary and samples "
     "among the most probable — learned from billions of pages of text."),
    ("Temperature",
     "A dial on the sampling: low = always the safest word, high = more "
     "surprising choices. Same question, different answers — by design, not "
     "by bug."),
    ("Predicting vs understanding",
     "To predict well at this scale, models build internal representations "
     "of grammar, facts and reasoning patterns. Whether that deserves the "
     "word « understanding » is an open scientific debate — honest people "
     "disagree."),
]


def build(lang: str = "en", **_):
    st_marker("Predict")
    # ── Temps 1 : la phrase à trou SEULE — la salle devine d'abord ──────────
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "The trick: ",
                         (s.project.titles.keyword, "predict the next word"),
                         tag=t.div, toc_lvl="+1", label="Predict")
            with g.cell():
                st_info_tooltip(
                    title="What is really happening",
                    # [*…], pas list(…) : l'import * de streamtex masque le
                    # builtin list (règle R14 d'opening).
                    entries=[*_TOOLTIP],
                )
        # La phrase descend vers le centre de l'écran : elle est seule en
        # scène sur ce premier temps, elle occupe la fenêtre (règle amphi).
        st_space("v", "18vh")
        st_write(bs.sentence, "« ", _SENTENCE_HEAD, " ",
                 (s.project.titles.keyword, _BLANK), " »", tag=t.div)
    # Arrêt clavier SANS entrée de barre latérale (pattern debates) : la
    # config globale du book (FULL, 30vh) s'applique.
    st_slide_break(marker_hidden=True)
    # ── Temps 2 : la révélation — la phrase, les candidats, le punch ────────
    with st_block(s.project.containers.page_fill_top):
        st_write(bs.sentence, "« ", _SENTENCE_HEAD, " ",
                 (s.project.titles.keyword, _BLANK), " »", tag=t.div)
        st_space("v", "3vh")
        # Les trois candidats : mot, barre proportionnelle, probabilité.
        for i, cand in enumerate(_CANDIDATES):
            width = max(cand["share"] * 100, 1.5)          # la barre 0,1 % reste visible
            with st_grid(cols="18% 64% 18%",
                         cell_styles=s.project.containers.grid_cell_centered) as g:
                with g.cell():
                    st_write(bs.word, cand["word"], tag=t.div)
                with g.cell():
                    st_html(f'<div style="width:100%;background:rgba(255,255,255,0.06);'
                            f'border-radius:0.6vh;">'
                            f'<div style="width:{width}%;background:{_BAR_COLOURS[i]};'
                            f'height:3.2vh;border-radius:0.6vh;"></div></div>')
                with g.cell():
                    st_write(bs.prob, cand["prob"], tag=t.div)
            st_space("v", "1vh")
        st_space("v", "2vh")
        st_write(bs.punch, _PUNCH, tag=t.div)
