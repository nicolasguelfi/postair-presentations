"""Démo B — L'agent au travail (M6, 3' en direct) — les trois prompts.

Les trois interactions jouées en direct, projetées en cartes pendant la
manipulation. Le plan B (captures des 3 interactions réussies) se produit
PENDANT LA RÉPÉTITION dans Le Chat sur le cours-exemple. Les prompts de
découverte des formations (v0.2 ``promptsdecouverte``) et la respiration
image (v0.2 ``imagegen``, OPTIONNELLE — les 20' priment) vivent dans
l'infobulle : ils se rejouent à la répétition, jamais improvisés en séance.

Le FAIT vit ici (règle NG 2026-08-18) : les trois prompts s'éditent dans ce
bloc. Aucune affirmation sourcée sur cette slide.

SPEAKER NOTES:
Three minutes, three prompts, in order: quiz me · explain as if I missed the
class · revision plan for the exam. Read each answer's SECTION CITATION out
loud — that is the method working. If time is comfortably ahead, the optional
breather: generate « Place d'Armes, Luxembourg City » in Le Chat — the
environment is not just text. If not, skip it without a word.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    live = s.project.titles.subtitle + s.project.colors.amber + s.center_txt + s.bold
    prompt = s.project.body.bullet + s.center_txt + s.bold
    line = s.project.body.caption + s.center_txt


bs = BlockStyles

_MARKER = {"en": "Demo: use", "fr": "Démo : utiliser"}
_TITLE = {"en": ("Live: the agent ", (s.project.titles.keyword, "at work")), "fr": ("En direct : l’agent ", (s.project.titles.keyword, "au travail"))}
_LIVE = {"en": "▶ LIVE — Le Chat", "fr": "▶ EN DIRECT — Le Chat"}

#: Les trois prompts exacts — la carte porte le prompt, la ligne dit pourquoi
#: il marche (tâche précise · contexte fourni · format demandé).
_PROMPTS = [
    {"prompt": {"en": "« Quiz me »", "fr": "« Fais-moi un quiz »"},
     "line": {"en": "precise task · your notes as context", "fr": "tâche précise · vos notes en contexte"}},
    {"prompt": {"en": "« Explain X as if I missed the class »", "fr": "« Explique-moi X comme si j’avais raté le cours »"},
     "line": {"en": "level asked · format asked", "fr": "niveau demandé · format demandé"}},
    {"prompt": {"en": "« Build my revision plan for the exam »", "fr": "« Fais-moi un plan de révision pour l’examen »"},
     "line": {"en": "goal given · the agent knows the syllabus", "fr": "objectif donné · l’agent connaît le programme"}},
]

_TIP_TITLE = {"en": "The prompts, precisely", "fr": "Les prompts, précisément"}
_TOOLTIP = [
    ({"en": "Why these three work", "fr": "Pourquoi ces trois-là marchent"},
     {"en": ("Each one names a precise task, leans on the provided context "
             "(YOUR course) and asks for a format. Vague prompt, vague "
             "answer — the method slide's techniques are exactly what makes "
             "these sharp."), "fr": "Chacun nomme une tâche précise, s’appuie sur le contexte fourni (VOTRE cours) et demande un format. Prompt vague, réponse vague — les techniques de la slide méthode sont exactement ce qui les rend tranchants."}),
    ({"en": "Useful variants", "fr": "Variantes utiles"},
     {"en": ("« Make flashcards from chapter 3 » · « Write a mock exam, then "
             "grade my answers » · « Play the examiner and push back on my "
             "answers »."), "fr": "« Fais des cartes mémoire du chapitre 3 » · « Rédige un examen blanc, puis corrige mes réponses » · « Joue l’examinateur et conteste mes réponses »."}),
    ({"en": "Two discovery prompts (from the AISE trainings)", "fr": "Deux prompts de découverte (des formations AISE)"},
     {"en": ("« What should one know about Luxembourg? » — the local anchor; "
             "then the pair « define intelligence » / « define intelligence "
             "in ONE sentence » — the effect of a constraint, shown in ten "
             "seconds. Replayed in Le Chat at rehearsal on the example "
             "course; the training screenshots are from another tool and are "
             "NOT reused."), "fr": "« Que faut-il savoir sur le Luxembourg ? » — l’ancrage local ; puis la paire « définis l’intelligence » / « définis l’intelligence en UNE phrase » — l’effet d’une contrainte, montré en dix secondes. Rejoués dans Le Chat à la répétition sur le cours-exemple ; les captures des formations viennent d’un autre outil et ne sont PAS réutilisées."}),
    ({"en": "Optional breather", "fr": "Respiration optionnelle"},
     {"en": ("If time allows: generate an image in Le Chat — « Place "
             "d'Armes, Luxembourg City ». The environment is not only text. "
             "Reserved for a comfortable lead; the twenty minutes come "
             "first."), "fr": "Si le temps le permet : générer une image dans Le Chat — « Place d’Armes, Luxembourg City ». L’environnement n’est pas que du texte. Réservé à une avance confortable ; les vingt minutes priment."}),
]

# ── La main de l'artiste ────────────────────────────────────────────────────
TUNING = {
    "card_zoom": 140,
}


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with st_zoom(150), g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(T(h, lang), T(d, lang)) for h, d in _TOOLTIP],
                )
        st_space("v", "1vh")
        with st_zoom(120):
            st_write(bs.live, T(_LIVE, lang), tag=t.div)
        st_space("v", "3vh")
        # Une carte par prompt, empilées : chaque prompt se lit en entier, de
        # loin — trois colonnes couperaient les phrases.
        for item in _PROMPTS:
            with st_block(s.project.cards.blue):
                with st_zoom(TUNING["card_zoom"]):
                    st_write(bs.prompt, T(item["prompt"], lang), tag=t.div)
                    st_space("v", "0.4vh")
                    st_write(bs.line, T(item["line"], lang), tag=t.div)
            st_space("v", "1.5vh")
