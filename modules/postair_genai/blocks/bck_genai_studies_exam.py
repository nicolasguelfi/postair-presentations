"""And for your studies — the exam stays human (G9b).

Le versant exigeant du découpage : l'orbe attend derrière la porte de la
salle d'examen, et le paradoxe ferme la slide en ambre. Le chiffre HEPI porte
son code de citation visible.

Le FAIT vit ici (règle NG 2026-08-18) : les trois mises en garde, le paradoxe
et le choix des citekeys s'éditent dans ce bloc (le versant positif vit dans
``bck_genai_studies_tutor`` — entrées disjointes de l'ancienne section
« studies »). La phrase bibliographique reste dérivée de ``references.bib``
par ``citation()``/``cite`` — clé inconnue = erreur bruyante.

SPEAKER NOTES:
Ninety seconds, slower than the previous slide. Read the amber paradox line
once, let it sit. The 94 % is not an accusation — it says the question is HOW,
not whether. Bridge: Mistral shows the how, the guidelines give the rules.
"""
# @guideline: postair-minimal

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
    item = s.project.body.bullet + s.center_txt
    paradox = s.project.titles.subtitle + s.project.colors.amber + s.center_txt


bs = BlockStyles

_EXAM_PROMPT = (
    AI_PREFIX
    + "An exam room made of paper: one abstract paper silhouette seen from "
      "behind, writing alone at a small paper desk, a paper wall clock above "
      "— and outside the closed paper door, waiting patiently in the "
      "corridor, a warm amber paper orb."
    + AI_SUFFIX_LANDSCAPE
)

# ── Les trois mises en garde — la dernière porte le chiffre HEPI sourcé ─────
_DONT = [
    "human exam = human learning",
    "shortcut = the skill-building effort, replaced",
    "94 % UK already use it → the question is HOW",
]
_DONT_CITEKEYS = ["hepi-survey-2026"]

# ── Le paradoxe — LE message de la slide ────────────────────────────────────
_PARADOX = "well used → learning ↑ · INSTEAD of learning → cancelled"


def build(lang: str = "en", **_):
    st_marker("The exam")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "The exam stays ", (s.project.titles.keyword, "human"),
                         tag=t.div, toc_lvl="+1", label="The exam")
            with g.cell():
                st_info_tooltip(
                    title="Tutor, not ghostwriter",
                    entries=[
                        ("Process originality", "What is graded is YOUR process: "
                         "drafts, choices, verification. Keeping your prompts and "
                         "versions is how you show it."),
                        ("The paradox", _PARADOX),
                    ],
                )
        st_space("v", s.project.spacing.title_gap)
        with hero_split(s, zoom=92, image=lambda: hero_image(
                "genai_exam", _EXAM_PROMPT, "images/genai_exam_fallback.svg",
                alt_ready=("Papercut exam room: a silhouette writing alone at a "
                           "desk, an amber orb waiting outside the closed door"),
                alt_fallback=("Papercut exam room, silhouette writing, amber orb "
                              "waiting behind the closed door"),
                variant="pt")):
            for item in _DONT[:-1]:
                st_write(bs.item, "▸ ", item, tag=t.div)
            st_write(bs.item, "▸ ", _DONT[-1], " ",
                     citation(*_DONT_CITEKEYS), tag=t.div)
            st_space("v", "1vh")
            # Le paradoxe — LE message de la slide — en carte ambre, VISIBLE :
            # il vivait sous le pli dans l'ancienne pile verticale.
            with st_block(s.project.cards.amber):
                st_write(bs.paradox, _PARADOX, tag=t.div)
