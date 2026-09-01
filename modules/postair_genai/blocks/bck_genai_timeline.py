"""Seventy years in one frieze (G3) — seven milestones, amber rising rightward.

The amber warms up milestone by milestone toward today: the point of the
slide IS that gradient (nothing magical, a long history and a recent tipping
point). Les pastilles sont des compositions de ``Style`` (R11, revue genaipat
2026-09-01 — l'ancien ``st_html`` portait ses couleurs en dur) ; les deux
extrémités du lavis sont les jetons de la palette.

Each milestone card carries its citation code in the visible text — full
reference on hover, canonical bib rule.

Le FAIT vit ici (règle NG 2026-08-18) : jalons, formulations et choix des
citekeys s'éditent dans ce bloc. La phrase bibliographique reste dérivée de
``references.bib`` par ``citation()``/``cite`` — clé inconnue = erreur
bruyante.

SPEAKER NOTES:
Three minutes, half a minute per milestone, walking left to right. Insist on
the two winters — promises outran results twice, and the room should hear
that this can happen again. Land on 2022: what changed is not the idea, it is
that it arrived in everyone's pocket at once.
"""
# @guideline: postair-minimal

from custom.refs import citation
from custom.styles import Styles as s
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.design_systems.postair_dark import AMBER, PRIMARY


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    year = s.project.titles.subtitle + s.center_txt + s.bold
    label = s.project.body.caption + s.center_txt + s.bold
    cite = s.project.body.caption + s.center_txt


bs = BlockStyles

#: L'ambre monte vers la droite : interpolation bleu → ambre par jalon.
#: Les EXTRÉMITÉS sont les jetons de la palette (PRIMARY → AMBER) ; les
#: intermédiaires sont un lavis réglé à l'œil pour CETTE frise — c'est le
#: message visuel de la slide, il vit ici, pas dans un style partagé.
_DOT_COLOURS = [PRIMARY, "#8FB0E0", "#A8A8C8", "#C4A06E", "#D9973F",
                AMBER, AMBER]


def _dot(colour: str, idx: int) -> Style:
    """La pastille du jalon — composition de ``Style`` (R11), pas de HTML."""
    return Style(
        f"width: 1.6vw; height: 1.6vw; border-radius: 50%; "
        f"margin: 0.5vh auto 0; background: {colour};",
        f"genai_timeline_dot_{idx}",
    )

# ── Les sept jalons (année + étiquette projetées ; détail au survol) ────────
#: Jamais projeté, gardé pour la vérifiabilité — les identifiants d'origine
#: des jalons : turing, dartmouth, winters, deep, transformers, chatgpt,
#: agents. Le jalon 2026 (agents) n'a pas de source : c'est une annonce de
#: séance, pas une affirmation — sa liste de citekeys est vide.
_MILESTONES = [
    {
        "year": "1950",
        "label": {"en": "The Turing test"},
        "detail": {"en": ("Can a machine hold a conversation indistinguishable from "
                          "a human's? The question that started the field.")},
        "citekeys": ["turing1950-mind"],
    },
    {
        "year": "1956",
        "label": {"en": "The name: « AI »"},
        "detail": {"en": ("A summer workshop at Dartmouth coins the term "
                          "« artificial intelligence » — and predicts fast progress.")},
        "citekeys": ["mccarthy1955-dartmouth"],
    },
    {
        "year": "1974–1993",
        "label": {"en": "Two AI winters"},
        "detail": {"en": ("Twice, promises outran results and funding collapsed. The "
                          "field learned humility the hard way.")},
        "citekeys": ["lighthill1973-survey"],
    },
    {
        "year": "2012",
        "label": {"en": "Deep learning works"},
        "detail": {"en": ("AlexNet crushes the ImageNet vision contest: neural "
                          "networks plus GPUs plus data finally deliver.")},
        "citekeys": ["krizhevsky2012-alexnet"],
    },
    {
        "year": "2017",
        "label": {"en": "Transformers"},
        "detail": {"en": ("« Attention Is All You Need » — the architecture every "
                          "current large language model is built on.")},
        "citekeys": ["vaswani2017-attention"],
    },
    {
        "year": "2022",
        "label": {"en": "ChatGPT"},
        "detail": {"en": ("An estimated 100 million users two months after launch — "
                          "the fastest-adopted consumer application of its time.")},
        "citekeys": ["hu2023-fastest"],
    },
    {
        "year": "2026",
        "label": {"en": "The year of agents"},
        "detail": {"en": ("Models that use tools in a loop to pursue a goal — the "
                          "frontier you will see live in the Mistral session.")},
        "citekeys": [],
    },
]

# ── Les feuilles {en} du bloc (structure i18n, lot C genaipat 2026-09-01) ────
_MARKER = {"en": "70 years"}
_TITLE = {"en": ((s.project.titles.keyword, "Seventy years"), " in one line")}
_TIP_TITLE = {"en": "The milestones, one sentence each"}


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(f"{m['year']} — {T(m['label'], lang)}",
                              T(m["detail"], lang))
                             for m in _MILESTONES],
                )
        st_space("v", s.project.spacing.title_gap)
        # La frise : une carte par jalon, point coloré + année + étiquette +
        # code de citation. La ligne est portée par la rangée de points.
        with st_grid(cols=s.project.grids.balanced(len(_MILESTONES)), gap="0.8vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for i, m in enumerate(_MILESTONES):
                with g.cell(), st_block(s.project.cards.blue):
                    with st_block(_dot(_DOT_COLOURS[i], i)):
                        pass
                    st_write(bs.year, m["year"], tag=t.div)
                    st_write(bs.label, T(m["label"], lang), tag=t.div)
                    if m["citekeys"]:
                        st_write(bs.cite, citation(*m["citekeys"]), tag=t.div)
