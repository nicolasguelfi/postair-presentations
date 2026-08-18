"""What it gets wrong: hallucinations (G7) — the serious moment of the session.

The dominant visual is a REAL fabricated reference, projected verbatim: the
non-existent case ChatGPT invented and two lawyers filed in a New York federal
court. Nothing invented by us — the invention is the exhibit, its citation
code opens the sanctions order.

Le FAIT vit ici (règle NG 2026-08-18) : la pièce à conviction, les trois
leçons et le choix des citekeys s'éditent dans ce bloc. La phrase
bibliographique reste dérivée de ``references.bib`` par
``citation()``/``cite`` — clé inconnue = erreur bruyante.

SPEAKER NOTES:
Four minutes — slow down, this is the moment the whole deck exists for. Read
the fake citation aloud, let it sound respectable, THEN say it does not exist.
The three lines below are the lesson; the sourced hallucination rates are on
the middle card. Bridge to the guidelines session: high risk = delegating what
you cannot verify.
"""
# @guideline: postair-minimal

from custom.refs import citation
from custom.styles import Styles as s
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    fake = s.project.titles.subtitle + s.center_txt
    verdict = s.project.body.body + s.project.colors.coral + s.center_txt + s.bold
    claim = s.project.body.bullet + s.center_txt + s.bold
    detail = s.project.body.caption + s.center_txt


bs = BlockStyles

# ── La pièce à conviction : la « référence » inventée, citée verbatim ───────
_CASE_QUOTE = ("Varghese v. China Southern Airlines Co., Ltd., 925 F.3d 1339 "
               "(11th Cir. 2019)")
_CASE_VERDICT = ("This case does not exist. ChatGPT invented it — with a full "
                 "docket number, quotes and internal citations — and two "
                 "lawyers filed it in a New York federal court.")
#: La clé ouvre l'ordonnance de sanctions — la seule vraie référence de la
#: carte corail.
_CASE_CITEKEYS = ["mata-avianca-2023"]

# ── Les trois leçons (carte projetée ; détail au survol) ────────────────────
#: Seule la carte du milieu porte une source (l'étude de profilage) ; les
#: deux autres sont des leçons structurelles, sans citekey — liste vide.
_CLAIMS = [
    {
        "short": "It does not « know » — it predicts",
        "detail": ("The model optimises plausibility, not truth. A fluent, "
                   "confident answer is what it is built to produce — even "
                   "when wrong."),
        "citekeys": [],
    },
    {
        "short": "Plausible ≠ true",
        "detail": ("On precise legal questions, large language models "
                   "hallucinated in 69 % to 88 % of cases in a systematic "
                   "profiling study."),
        "citekeys": ["dahl-legal-fictions-2024"],
    },
    {
        "short": "Verification is non-negotiable",
        "detail": ("Anything that matters gets checked at the source. This "
                   "is the bridge to the UL guidelines: high risk = "
                   "delegating what you cannot verify."),
        "citekeys": [],
    },
]


def build():
    st_marker("Hallucinations")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "What it gets wrong: ",
                         (s.project.titles.keyword, "hallucinations"),
                         tag=t.div, toc_lvl="+1", label="Hallucinations")
            with g.cell():
                st_info_tooltip(
                    title="Why this is structural",
                    entries=[(c["short"], c["detail"]) for c in _CLAIMS]
                            + [("The exhibit", _CASE_VERDICT)],
                )
        st_space("v", s.project.spacing.title_gap)
        # La pièce à conviction : une « référence » très convenable — et fausse.
        with st_block(s.project.cards.coral):
            st_write(bs.fake, "« ", _CASE_QUOTE, " »", tag=t.div)
            st_space("v", "1vh")
            st_write(bs.verdict, "This case does not exist. ",
                     citation(*_CASE_CITEKEYS), tag=t.div)
        st_space("v", "2vh")
        with st_grid(cols=s.project.grids.balanced(len(_CLAIMS)), gap="1.2vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for c in _CLAIMS:
                with g.cell(), st_block(s.project.cards.blue):
                    st_write(bs.claim, c["short"], tag=t.div)
                    if c["citekeys"]:
                        st_write(bs.detail, citation(*c["citekeys"]), tag=t.div)
