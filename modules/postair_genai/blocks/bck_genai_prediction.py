"""The trick: predict the next word (G4) — THE pedagogical slide of the session.

One giant cloze sentence, three candidate words with probability bars. The
visual IS the explanation: an auditorium reads the 78 % bar before the speaker
finishes the sentence. Data-driven from ``custom.facts``; tokens, temperature
and the predicting-vs-understanding debate live in the tooltip.

SPEAKER NOTES:
Four minutes — take them. Optional mini-demo: read the sentence aloud, stop at
the blank, let the room shout the word: the room just DID what a language
model does. Then the honest turn: predicting well at this scale starts to look
like understanding, and whether it IS understanding is an open scientific
debate — say that the debate exists, it buys credibility for the whole deck.
"""
# @guideline: postair-minimal

from custom.facts import section, text
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


def build():
    st_marker("Predict")
    data = section("prediction")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "The trick: ",
                         (s.project.titles.keyword, "predict the next word"),
                         tag=t.div, toc_lvl="+1", label="Predict")
            with g.cell():
                st_info_tooltip(
                    title="What is really happening",
                    entries=[(text(e["term"]), text(e["def"]))
                             for e in data["tooltip"]],
                )
        st_space("v", s.project.spacing.title_gap)
        st_write(bs.sentence, "« ", text(data["sentence_head"]), " ",
                 (s.project.titles.keyword, text(data["blank"])), " »", tag=t.div)
        st_space("v", "3vh")
        # Les trois candidats : mot, barre proportionnelle, probabilité.
        for i, cand in enumerate(data["candidates"]):
            width = max(cand["share"] * 100, 1.5)          # la barre 0,1 % reste visible
            with st_grid(cols="18% 64% 18%",
                         cell_styles=s.project.containers.grid_cell_centered) as g:
                with g.cell():
                    st_write(bs.word, text(cand["word"]), tag=t.div)
                with g.cell():
                    st_html(f'<div style="width:100%;background:rgba(255,255,255,0.06);'
                            f'border-radius:0.6vh;">'
                            f'<div style="width:{width}%;background:{_BAR_COLOURS[i]};'
                            f'height:3.2vh;border-radius:0.6vh;"></div></div>')
                with g.cell():
                    st_write(bs.prob, cand["prob"], tag=t.div)
            st_space("v", "1vh")
        st_space("v", "2vh")
        st_write(bs.punch, text(data["punch"]), tag=t.div)
