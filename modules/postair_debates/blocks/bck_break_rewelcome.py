"""Re-welcome — what the second half holds, in three cards.

Reads the post-break sessions from the agenda rather than restating them, so
the slide cannot drift from the programme. Medio comes back on stage: the
moderator opened the morning, the moderator restarts it.

SPEAKER NOTES:
One minute, energy up. People come back scattered and half of them are still
in the corridor — do not start the content here. Name the three sessions, say
that the first one answers the question everybody actually has ("how does
this thing work?"), and hand over.
"""
# @guideline: postair-minimal

# ``from streamtex import *`` shadows the builtin ``list`` with the st_list
# module: annotations must stay unevaluated.
from __future__ import annotations

from custom.styles import Styles as s
from postair_data import mascot
from postair_event import AGENDA
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.ai_mark import dd35_overlay

#: La promesse est la TÊTE de la carte (rendue au-dessus du titre de session) :
#: capitale initiale, règle R-case (NG 2026-08-30). Les titres de session, eux,
#: viennent de l'agenda et ne sont jamais recasés.
_PROMISE = {
    "Introduction to AI & Generative AI": {"en": "Understand", "fr": "Comprendre"},
    "Using models & agents to study": {"en": "See it in practice", "fr": "Voir en pratique"},
    "The UL AI guidelines": {"en": "The rules of the game", "fr": "Les règles du jeu"},
}

# ── Le texte projeté (règle R-i18n) ──────────────────────────────────────────
_MARKER = {"en": "Part two", "fr": "Deuxième partie"}
_TITLE = {"en": ("Part two — ", (s.project.titles.keyword, "the agenda")), "fr": ("Deuxième partie — ", (s.project.titles.keyword, "le programme"))}
_TIP_TITLE = {"en": "The second half", "fr": "La deuxième partie"}
_TIP = [
    ({"en": "Understand", "fr": "Comprendre"},
     {"en": ("What a large language model is doing when it answers: prediction, not "
             "knowledge — and why that explains both the usefulness and the confident "
             "mistakes."), "fr": "Ce que fait un grand modèle de langage quand il répond : de la prédiction, pas du savoir — et pourquoi cela explique à la fois l'utilité et les erreurs affirmées avec aplomb."}),
    ({"en": "Practice", "fr": "En pratique"},
     {"en": ("A revision agent built live with Mistral, including the anti-patterns: the "
             "agent that flatters, the one that invents sources, the one that does the work "
             "you needed to do yourself."), "fr": "Un agent pour réviser vos cours, construit en direct avec Mistral, avec les pièges à éviter : l'agent qui flatte, celui qui invente des sources, celui qui fait le travail que vous deviez faire vous-même."}),
    ({"en": "The rules", "fr": "Les règles"},
     {"en": ("The university's AI charter: permitted by default, the syllabus prevails, "
             "disclose your use, three risk levels, ten red lines — and the test that "
             "decides the rest: can you defend it out loud?"), "fr": "La charte IA de l'université : autorisé par défaut, le syllabus prime, déclarez votre usage, trois niveaux de risque, dix lignes rouges — et le test qui tranche le reste : pouvez-vous le défendre à voix haute ?"}),
    ({"en": "Same posture, new light", "fr": "Même posture, nouvel éclairage"},
     {"en": ("Everything in the second half connects back to the nine axes you answered "
             "on this morning."), "fr": "Tout, dans la deuxième partie, renvoie aux neuf axes sur lesquels vous avez répondu ce matin."}),
]


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    session = s.project.body.body + s.center_txt + s.bold
    promise = s.project.titles.subtitle + s.center_txt
    duration = s.project.body.caption + s.center_txt
    mascot_name = s.project.body.mascot_name


bs = BlockStyles


def _second_half() -> list[tuple[str, str]]:
    """Sessions after the break, in agenda order — closing excluded."""
    seen_break = False
    out = []
    for session, duration, kind in AGENDA:
        if kind == "break":
            seen_break = True
            continue
        if seen_break and session in _PROMISE:
            out.append((session, duration))
    return out


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    medio = mascot("Medio")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(T(h, lang), T(d, lang)) for h, d in _TIP],
                )
        st_space("v", s.project.spacing.title_gap)
        # ONE flat grid — the moderator is a cell like the others, never a
        # column holding a second responsive grid.
        second = _second_half()
        with st_grid(cols=s.project.grids.balanced(1 + len(second)), gap="1.2vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_image(s.project.cards.media_center, width="min(16vw, 34vh)",
                         uri=medio["image"],
                         alt=f"{medio['name']}, the moderator mascot, restarting the session",
                         overlay=dd35_overlay())
                st_write(bs.mascot_name, medio["name"], tag=t.div)
            for session, duration in second:
                with g.cell(), st_block(s.project.cards.blue):
                    st_write(bs.promise, T(_PROMISE[session], lang), tag=t.div)
                    st_write(bs.session, session, tag=t.div)
                    st_write(bs.duration, duration, tag=t.div)
