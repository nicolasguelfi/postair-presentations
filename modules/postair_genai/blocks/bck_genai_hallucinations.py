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
from postair_lang import T, TF
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

_MARKER = {"en": "'Hallucinations'", "fr": "« Hallucinations »"}
_TITLE = {"en": ("When it goes wrong: ",
                 (s.project.titles.keyword, "'hallucinations'")), "fr": ("Quand ça déraille : les ", (s.project.titles.keyword, "« hallucinations »"))}
_TIP_TITLE = {"en": "Why this is structural", "fr": "Pourquoi c’est structurel"}
_EXHIBIT_HEAD = {"en": "The exhibit", "fr": "La pièce à conviction"}

# ── La pièce à conviction : la « référence » inventée, citée verbatim ───────
#: PAS une feuille : la fausse référence est une DONNÉE, citée telle quelle
#: dans toutes les langues (R-case — les données ne se recasent ni ne se
#: traduisent). i18n: verbatim
_CASE_QUOTE = ("Varghese v. China Southern Airlines Co., Ltd.,\n 925 F.3d 1339 "
               "(11th Cir. 2019)")
_CASE_VERDICT = {"en": ("This case does not exist. ChatGPT invented it — with a full "
                        "docket number, quotes and internal citations — and two "
                        "lawyers filed it in a New York federal court."), "fr": "Cette affaire n’existe pas. ChatGPT l’a inventée — avec un numéro de rôle complet, des citations et des renvois internes — et deux avocats l’ont déposée devant un tribunal fédéral de New York."}
_CASE_VERDICT_SHORT = {"en": "This case does not exist. ", "fr": "Cette affaire n’existe pas. "}
#: La clé ouvre l'ordonnance de sanctions — la seule vraie référence de la
#: carte corail.
_CASE_CITEKEYS = ["mata-avianca-2023"]

# ── Les trois leçons (carte projetée ; détail au survol) ────────────────────
#: Seule la carte du milieu porte une source (l'étude de profilage) ; les
#: deux autres sont des leçons structurelles, sans citekey — liste vide.
_CLAIMS = [
    {
        "short": {"en": "Highly capable and reliable IF …", "fr": "Très capable et fiable SI …"},
        "detail": {"en": ("The model optimises plausibility, not truth. A fluent, "
                          "confident answer is what it is built to produce — even "
                          "when wrong."), "fr": "Le modèle optimise la plausibilité, pas la vérité. Une réponse fluide et assurée est ce qu’il est construit pour produire — même quand elle est fausse."},
        "citekeys": [],
    },
    {
        "short": {"en": "Plausible\n≠ true", "fr": "Plausible\n≠ vrai"},
        "detail": {"en": ("On precise legal questions, large language models "
                          "hallucinated in 69 % to 88 % of cases in a systematic "
                          "profiling study."), "fr": "Sur des questions juridiques précises, les grands modèles de langage ont halluciné dans 69 % à 88 % des cas dans une étude de profilage systématique."},
        "citekeys": ["dahl-legal-fictions-2024"],
    },
    {
        "short": {"en": "Verification is non-negotiable", "fr": "La vérification est non négociable"},
        "detail": {"en": ("Anything that matters gets checked at the source. This "
                          "is the bridge to the UL guidelines: high risk = "
                          "delegating what you cannot verify."), "fr": "Tout ce qui compte se vérifie à la source. C’est le pont vers les lignes directrices de l’UL : risque élevé = déléguer ce que vous ne pouvez pas vérifier."},
        "citekeys": [],
    },
]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                with st_zoom(130):
                    st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(T(c["short"], lang), T(c["detail"], lang))
                             for c in _CLAIMS]
                            + [(T(_EXHIBIT_HEAD, lang), T(_CASE_VERDICT, lang))],
                )
        st_space("v", s.project.spacing.title_gap)
        # La pièce à conviction : une « référence » très convenable — et fausse.
        with st_block(s.project.cards.coral):
            st_write(bs.fake, "« ", _CASE_QUOTE, " »", tag=t.div)
            st_space("v", "1vh")
            with st_zoom(150):
                st_write(bs.verdict, T(_CASE_VERDICT_SHORT, lang),
                     citation(*_CASE_CITEKEYS), tag=t.div)
        st_space("v", "2vh")
        with st_grid(cols=s.project.grids.balanced(len(_CLAIMS)), gap="1.2vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for c in _CLAIMS:
                with st_zoom(140),g.cell(), st_block(s.project.cards.blue):
                    st_write(bs.claim, T(c["short"], lang), tag=t.div)
                    if c["citekeys"]:
                        st_write(bs.detail, citation(*c["citekeys"]), tag=t.div)
