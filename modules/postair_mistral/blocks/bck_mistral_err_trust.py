"""Erreur n°3 — Croire sans vérifier (M9) — le cadrage démontré.

La démonstration de CADRAGE des formations (v0.2 ``cadragem9``), transposée
sur un sujet de cours NEUTRE : « X est-elle la bonne approche ? » vs « X
est-elle la mauvaise approche ? » → deux plaidoyers opposés, même aplomb. La
version « communisme » du draft reste écartée en amphi (elle vit en backup du
deck genai). La paire réelle sur le cours-exemple se prépare EN RÉPÉTITION —
d'ici là les deux cartes portent le motif avec un X générique.

Le FAIT vit ici (règle NG 2026-08-18) : les deux cartes s'éditent dans ce
bloc. Aucune affirmation sourcée sur cette slide.

SPEAKER NOTES:
Two minutes. Read the two framings out loud with the SAME confident voice —
that is the demonstration. The model completes the most probable answer to
YOUR question; it does not weigh the truth. Land the amber line: confidence
is not truth — verify against the course, never against the AI itself. Link
forward: the guidelines session gives the three risk levels.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    ask = s.project.body.pole_label + s.project.colors.primary + s.center_txt + s.bold
    answer = s.project.body.bullet + s.center_txt
    verdict = s.project.body.caption + s.center_txt
    punch = s.project.titles.subtitle + s.project.colors.amber + s.center_txt


bs = BlockStyles

_MARKER = {"en": "Error: trusting", "fr": "Erreur : croire"}
_TITLE = {"en": ("Error 3 — believing ", (s.project.titles.keyword, "without checking")), "fr": ("Erreur 3 — croire ", (s.project.titles.keyword, "sans vérifier"))}

#: La paire de cadrage — X = notion du cours-exemple, fixée à la répétition.
_FRAMINGS = [
    {"ask": {"en": "« Is X the right approach? »", "fr": "« X est-elle la bonne approche ? »"},
     "answer": {"en": "a confident plea FOR", "fr": "un plaidoyer assuré POUR"}},
    {"ask": {"en": "« Is X the wrong approach? »", "fr": "« X est-elle la mauvaise approche ? »"},
     "answer": {"en": "a confident plea AGAINST", "fr": "un plaidoyer assuré CONTRE"}},
]
_VERDICT = {"en": "same model · same aplomb", "fr": "même modèle · même aplomb"}

_PUNCH_LINES = {"en": ("confidence ≠ truth", "verify against the COURSE, not against the AI"), "fr": ("aplomb ≠ vérité", "vérifiez contre le COURS, pas contre l’IA")}

_TIP_TITLE = {"en": "Verifying, precisely", "fr": "Vérifier, précisément"}
_TOOLTIP = [
    ({"en": "Why it follows your framing", "fr": "Pourquoi il suit votre cadrage"},
     {"en": ("The model completes the most PROBABLE answer to the question "
             "as asked — it does not weigh what is true. Frame the question "
             "one way, it argues that way, with the same fluency either "
             "direction."), "fr": "Le modèle complète la réponse la plus PROBABLE à la question telle que posée — il ne pèse pas le vrai. Cadrez la question dans un sens, il plaide dans ce sens, avec la même fluidité dans les deux directions."}),
    ({"en": "Four checks that work for a student", "fr": "Quatre vérifications qui marchent pour un étudiant"},
     {"en": ("Cross-check with the course material · ask for the exact "
             "source and section · ask the question the OTHER way round · "
             "test on a case whose answer you already know."), "fr": "Recouper avec le support du cours · demander la source et la section exactes · poser la question dans l’AUTRE sens · tester sur un cas dont vous connaissez déjà la réponse."}),
    ({"en": "In a specialised context, the error is fine", "fr": "En contexte pointu, l’erreur est fine"},
     {"en": ("Not a wild invention: a subtly wrong clause, a swapped "
             "condition, a dated result — exactly the errors that cost exam "
             "points. The finer the topic, the harder you check."), "fr": "Pas une invention folle : une proposition subtilement fausse, une condition inversée, un résultat daté — exactement les erreurs qui coûtent des points à l’examen. Plus le sujet est fin, plus on vérifie."}),
    ({"en": "The rules that follow", "fr": "Les règles qui suivent"},
     {"en": ("The UL guidelines session right after this one grades AI uses "
             "in three risk levels — verification is what moves a use from "
             "risky to reasonable."), "fr": "La session sur les lignes directrices de l’UL, juste après celle-ci, classe les usages de l’IA en trois niveaux de risque — la vérification est ce qui fait passer un usage de risqué à raisonnable."}),
]

# ── La main de l'artiste ────────────────────────────────────────────────────
TUNING = {
    "card_zoom": 160,
}


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with st_zoom(120), g.cell():
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
            for framing in _FRAMINGS:
                with g.cell(), st_block(s.project.cards.blue):
                    with st_zoom(TUNING["card_zoom"]):
                        st_write(bs.ask, T(framing["ask"], lang), tag=t.div)
                        st_space("v", "1.5vh")
                        st_write(bs.answer, T(framing["answer"], lang), tag=t.div)
                        st_space("v", "1.5vh")
                        st_write(bs.verdict, T(_VERDICT, lang), tag=t.div)
        st_space("v", "3vh")
        with st_zoom(110):
            for line in T(_PUNCH_LINES, lang):
                st_write(bs.punch, line, tag=t.div)
