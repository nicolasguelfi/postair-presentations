"""BACKUP · Framing — même question, deux réponses opposées.

Annexe backup (planche drafts2 ``backtech=cadrage``, NG 2026-09-01) :
l'expérience des formations AISE — la MÊME question posée dans les deux
sens, et le modèle plaide chaque fois le sens demandé, avec le même aplomb.
La paire d'origine (le communisme, 2023-24) est conservée telle quelle : un
backup se projette pour des questions d'initiés, et la paire réelle est la
preuve documentée. La session Mistral rejoue la MÊME mécanique sur un sujet
de cours neutre (M9, drafts3 ``demo=cadragem9``).

Pure composition Style : deux cartes, zéro média, zéro capture.

Démonstration documentée, pas d'affirmation de littérature : pas de citekey
(le versant « flatterie » est décrit au panneau sans phrase bibliographique).

SPEAKER NOTES:
Only if asked (« can I trust its opinions? »). Read the two prompts, then
the two summaries: a confident case FOR, a confident case AGAINST — same
model, same day. The lesson in one line: it completes YOUR framing, it does
not weigh the truth. Verify against sources, never against the AI itself.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    prompt = s.project.body.bullet + s.center_txt + s.bold
    answer = s.project.body.caption + s.center_txt
    punch = s.project.titles.subtitle + s.project.colors.amber + s.center_txt


bs = BlockStyles

_MARKER = {"en": "Framing"}
_TITLE = {"en": ("Same question, ", (s.project.titles.keyword, "two answers"))}

_PAIR = [
    {"prompt": {"en": "« Is communism GOOD for humanity? »"},
     "answer": {"en": "a confident, structured case FOR"}},
    {"prompt": {"en": "« Is communism BAD for humanity? »"},
     "answer": {"en": "a confident, structured case AGAINST"}},
]

_PUNCH = {"en": ("it completes YOUR framing — it does not weigh truth",
                 "verify against sources, never against the AI")}

_TIP_TITLE = {"en": "The experiment, precisely"}
_TOOLTIP = [
    ({"en": "What was run"},
     {"en": ("The two prompts, same model, same session (AISE trainings, "
             "2023-24) — each answer argues the direction of the question, "
             "with equal confidence.")}),
    ({"en": "Why"},
     {"en": ("Prediction again: the most probable continuation of « is X "
             "good? » is a case for X. Assistant tuning adds agreeableness — "
             "models tend to follow the user's lead.")}),
    ({"en": "Same family of surprises"},
     {"en": ("Temperature (G4's panel) makes answers differ between runs; "
             "framing makes them differ by QUESTION. Neither is a bug — both "
             "are the mechanism.")}),
    ({"en": "Where it returns"},
     {"en": ("The Mistral session replays this mechanic on a neutral course "
             "topic (error n°3: believing without checking) — same lesson, "
             "student-sized.")}),
]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
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
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for side in _PAIR:
                with g.cell(), st_block(s.project.cards.blue):
                    with st_zoom(125):
                        st_write(bs.prompt, T(side["prompt"], lang), tag=t.div)
                        st_space("v", "3vh")
                        st_write(bs.answer, "→ ", T(side["answer"], lang), tag=t.div)
        st_space("v", "5vh")
        with st_zoom(130):
            for line in T(_PUNCH, lang):
                st_write(bs.punch, line, tag=t.div)
