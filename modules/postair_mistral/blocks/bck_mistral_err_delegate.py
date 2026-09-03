"""Erreur n°2 — Tout déléguer : tu n'apprends rien (M8).

Les deux chemins en image (raccourci brillant → mur de l'examen ; chemin
d'effort → sommet), le constat en trois lignes à droite. L'ancrage charte
(pratique non permise : la contribution intellectuelle centrale évaluée) est
le fait PARTAGÉ ``charter``/``delegation`` de facts.json.

Le FAIT vit ici (règle NG 2026-08-18) pour les lignes projetées ; l'étude sur
l'illusion de maîtrise porte sa clé (kosmyna2025-cognitive-debt), phrase
bibliographique dérivée de ``references.bib`` — clé inconnue = erreur
bruyante.

SPEAKER NOTES:
Two minutes. The honest sentence first: « do my homework » WORKS — the agent
produces something correct-looking in seconds. Then the two walls: you learn
nothing (the EEG study is in the panel), and it is not permitted when the
work is assessed. End on the reversal: paste YOUR draft and ask the agent to
attack it — same tool, opposite outcome.
"""
# @guideline: postair-minimal

from custom.facts import citekeys, fact, text
from custom.prompts import AI_PREFIX, AI_SUFFIX_LANDSCAPE
from custom.refs import citation
from custom.styles import Styles as s
from custom.visuals import staged_hero_image
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.hero_split import hero_split


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    item = s.project.body.bullet + s.center_txt
    punch = s.project.titles.subtitle + s.project.colors.amber + s.center_txt


bs = BlockStyles

_PATHS_PROMPT = (
    AI_PREFIX
    + "Two paper paths diverging from one abstract paper silhouette seen "
      "from behind: a flat shiny golden shortcut ending against a tall coral "
      "paper wall, and a staircase of teal paper steps climbing to a summit "
      "with a small paper flag under a warm amber paper sun."
    + AI_SUFFIX_LANDSCAPE
)

_MARKER = {"en": "Error: delegating", "fr": "Erreur : déléguer"}
_TITLE = {"en": ("Error 2 — delegate everything: ", (s.project.titles.keyword, "you learn nothing")), "fr": ("Erreur 2 — tout déléguer : ", (s.project.titles.keyword, "vous n’apprenez rien"))}

_ITEMS = [
    {"en": "« do my homework » = it works…", "fr": "« fais mon devoir » = ça marche…"},
    {"en": "…and you fail the exam", "fr": "…et vous échouez à l’examen"},
    {"en": "assessed work → not permitted", "fr": "travail évalué → non permis"},
]

_TIP_TITLE = {"en": "The evidence, and the reversal", "fr": "Les preuves, et le retournement"}
_TIP_CHARTER_HEAD = {"en": "What the UL guidelines say", "fr": "Ce que disent les lignes directrices UL"}
_TIP_MASTERY = ({"en": "The illusion of mastery", "fr": "L’illusion de maîtrise"},
                {"en": ("Reading a fluent AI answer FEELS like understanding. "
                        "An EEG study at MIT measured lower brain "
                        "connectivity and worse recall of one's own text when "
                        "essays were written with an LLM — the fluency is the "
                        "assistant's, not yours."), "fr": "Lire une réponse d’IA fluide DONNE L’IMPRESSION de comprendre. Une étude EEG du MIT a mesuré une connectivité cérébrale plus faible et une moins bonne mémorisation de son propre texte quand l’essai est écrit avec un LLM — la fluidité est celle de l’assistant, pas la vôtre."})
_TIP_REVERSAL = ({"en": "Turn the temptation into a use", "fr": "Retourner la tentation en usage"},
                 {"en": ("Instead of asking for the solution, paste YOURS and "
                         "ask the agent to attack it: find my errors, ask me "
                         "the questions an examiner would. Same tool, "
                         "opposite outcome — the thinking stays yours."), "fr": "Au lieu de demander la solution, collez la VÔTRE et demandez à l’agent de l’attaquer : trouve mes erreurs, pose-moi les questions qu’un examinateur poserait. Même outil, résultat inverse — la pensée reste la vôtre."})

# ── La main de l'artiste ────────────────────────────────────────────────────
#: Resserrée (porte projection 2026-09-02 : ×1.09/×1.22) — budget image et
#: zoom de colonne d'un cran.
TUNING = {
    "ratio": 44,
    "hero_vh": 60,
    "column_zoom": 120,
}

_MASTERY_CITEKEYS = ["kosmyna2025-cognitive-debt"]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    charter = fact("charter", "delegation")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with st_zoom(150), g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(T(_TIP_CHARTER_HEAD, lang), text(charter["claim"], lang)),
                             (T(_TIP_MASTERY[0], lang), T(_TIP_MASTERY[1], lang)),
                             (T(_TIP_REVERSAL[0], lang), T(_TIP_REVERSAL[1], lang))],
                )
        st_space("v", s.project.spacing.title_gap)
        with hero_split(s, ratio=TUNING["ratio"], zoom=TUNING["column_zoom"],
                        image=lambda: staged_hero_image(
                            "mistral_paths", _PATHS_PROMPT,
                            "images/mistral_paths_fallback.svg",
                            alt_ready=("Papercut fork: a shiny flat shortcut into a coral "
                                       "wall, teal steps climbing to a summit flag"),
                            alt_fallback=("Papercut silhouette before two paths — golden "
                                          "shortcut to a wall, teal stairs to a summit"),
                            variant="sq", stage_vh=TUNING["hero_vh"])):
            for item in _ITEMS:
                st_write(bs.item, "▸ ", T(item, lang), tag=t.div)
            st_space("v", "2vh")
            st_write(bs.punch, text(charter["short"], lang), " ",
                     citation(*citekeys(charter), *_MASTERY_CITEKEYS), tag=t.div)
