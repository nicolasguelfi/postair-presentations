"""Reflex 3 — the three risk levels (U4). The ONLY tricolour slide.

The dominant visual is a PAPERCUT traffic light — the tricolour lives inside
the illustration, in the day's graphic line (rappel NG 2026-08-11 : la ligne
des visuels est le papier découpé coloré, jamais une ligne navy plate). Below
it, three cards with green / orange / red washes — the deliberate, single
derogation from the postair palette (plan U4, décision de design à confirmer
au prototype) : the traffic-light semantics IS the message, and it appears
exactly once in the whole day.

Le FAIT vit ici (règle NG 2026-08-18) : les trois niveaux, la ligne-cadre et
le choix des citekeys s'éditent dans ce bloc. La phrase bibliographique reste
dérivée de ``references.bib`` par ``citation()`` — clé inconnue = erreur
bruyante.

Conversion R-i18n (2026-09-03) : les textes projetés sont des feuilles
{"en", "fr"} résolues par ``T()``/``TF()`` ; SPEAKER NOTES et ``alt=``
restent EN.

SPEAKER NOTES:
Three minutes — this is the mental model they will reuse weekly. One level at
a time: YOU are the source (green) · you explore and VERIFY (orange) · you
delegate what you cannot verify (red). Connect red to the Mistral session's
demonstrated failures and to G7 of the GenAI session (the fabricated case).
Close on the frame line: levels are vigilance signals, not prohibitions.
"""
# @guideline: postair-minimal

from custom.prompts import AI_PREFIX, AI_SUFFIX_LANDSCAPE
from custom.refs import citation
from custom.styles import Styles as s
from custom.visuals import hero_image
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t
from streamtex.styles import Style

from postair_pack.components.hero_split import hero_split

# ── Le fait : les trois niveaux de risque (guidelines, section 4) ───────────
#: « label » et « line » sont projetés sur les cartes ; « detail » vit dans
#: le tooltip ; « id » sélectionne le lavis sémantique.
_LEVELS = [
    {"id": "low", "icon": "🟢",
     "label": {"en": "LOW", "fr": "FAIBLE"},
     "line": {"en": "YOU are the source — the AI polishes",
              "fr": "VOUS êtes la source — l'IA polit"},
     "detail": {"en": ("You know the answer; the AI works on the surface: "
                       "proofreading, form, organising your own ideas."),
                "fr": ("Vous connaissez la réponse ; l'IA travaille la surface : "
                       "relecture, forme, organisation de vos propres idées.")}},
    {"id": "medium", "icon": "🟠",
     "label": {"en": "MODERATE", "fr": "MODÉRÉ"},
     "line": {"en": "You explore — and you VERIFY",
              "fr": "Vous explorez — et vous VÉRIFIEZ"},
     "detail": {"en": ("You are learning the topic: summaries and syntheses of "
                       "complex material help, but you check omissions, distortions "
                       "and inventions against reliable sources."),
                "fr": ("Vous découvrez le sujet : résumés et synthèses de matière "
                       "complexe aident, mais vous contrôlez omissions, distorsions "
                       "et inventions contre des sources fiables.")}},
    {"id": "high", "icon": "🔴",
     "label": {"en": "HIGH", "fr": "ÉLEVÉ"},
     "line": {"en": "You delegate what you cannot verify",
              "fr": "Vous déléguez ce que vous ne pouvez pas vérifier"},
     "detail": {"en": ("You depend on the AI for claims you cannot check — or the "
                       "AI replaces the assessed learning objective itself. "
                       "Hallucinations, fabricated citations, overconfidence."),
                "fr": ("Vous dépendez de l'IA pour des affirmations que vous ne "
                       "pouvez pas contrôler — ou l'IA remplace l'objectif "
                       "d'apprentissage évalué lui-même. Hallucinations, citations "
                       "fabriquées, excès de confiance.")}},
]
_FRAME = {"en": "Risk level ↑ = verification ↑ · never a ban",
          "fr": "Niveau de risque ↑ = vérification ↑ · jamais une interdiction"}
_CITEKEYS = ["i2tl2026-guidelines", "parmentier-vicens-2025"]
#: Jamais projeté, gardé pour la vérifiabilité (entrée « big » de l'ancien
#: facts.json) : « Three risk levels ».

_TRAFFIC_PROMPT = (
    AI_PREFIX
    + "A tall friendly paper traffic light at the centre, with three big "
      "round paper lights stacked vertically — leaf green on top, warm "
      "orange in the middle, coral red at the bottom — each light a layered "
      "paper disc with a soft glow. Three small abstract paper silhouettes "
      "seen from behind look up at it from a papercut path."
    + AI_SUFFIX_LANDSCAPE
)

#: Dérogation tricolore assumée (une seule slide du jour) : trois lavis aux
#: couleurs sémantiques, calqués sur la géométrie des cartes du DS.
_WASH = {
    "low": Style("background: rgba(127,176,105,0.18); border: 1px solid rgba(127,176,105,0.55); "
                 "border-radius: 12px; padding: 1.2vw; height: 100%;", "guide_risk_low"),
    "medium": Style("background: rgba(243,156,18,0.16); border: 1px solid rgba(243,156,18,0.55); "
                    "border-radius: 12px; padding: 1.2vw; height: 100%;", "guide_risk_medium"),
    "high": Style("background: rgba(231,76,60,0.16); border: 1px solid rgba(231,76,60,0.6); "
                  "border-radius: 12px; padding: 1.2vw; height: 100%;", "guide_risk_high"),
}


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    icon = s.project.titles.subtitle + s.center_txt
    label = s.project.body.pole_label + s.center_txt
    line = s.project.body.bullet + s.center_txt + s.bold
    frame = s.project.titles.subtitle + s.project.colors.amber + s.center_txt
    cite = s.project.body.caption + s.center_txt


bs = BlockStyles

_MARKER = {"en": "Three levels", "fr": "Trois niveaux"}
_TITLE = {"en": ("Reflex 3 — the ",
                 (s.project.titles.keyword, "three risk levels")),
          "fr": ("Réflexe 3 — les ",
                 (s.project.titles.keyword, "trois niveaux de risque"))}
_TIP_TITLE = {"en": "The levels (guidelines, section 4)",
              "fr": "Les niveaux (lignes directrices, section 4)"}
_FRAME_HEAD = {"en": "The frame", "fr": "Le cadre"}
_RED_HEAD = {"en": "The red case that matters",
             "fr": "Le cas rouge qui compte"}
_RED_CASE = {"en": ("« The AI replaces the assessed learning objective » is "
                    "always high risk — that is the one to remember."),
             "fr": ("« L'IA remplace l'objectif d'apprentissage évalué » est "
                    "toujours un risque élevé — c'est celui à retenir.")}


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
                    entries=[(f"{lv['icon']} {T(lv['label'], lang)} — {T(lv['line'], lang)}",
                              T(lv["detail"], lang)) for lv in _LEVELS]
                            + [(T(_FRAME_HEAD, lang), T(_FRAME, lang)),
                               (T(_RED_HEAD, lang), T(_RED_CASE, lang))],
                )
        st_space("v", s.project.spacing.title_gap)
        # Gabarit par défaut (NG 2026-08-13) : le feu tricolore carré à gauche,
        # les trois niveaux EMPILÉS à droite — ils étaient coupés à 40 % sous
        # le pli, le contenu opérationnel de la slide.
        with hero_split(s, image=lambda: hero_image(
                "guide_traffic", _TRAFFIC_PROMPT, "images/guide_traffic_fallback.svg",
                alt_ready=("Papercut traffic light with three big lights — green, "
                           "orange, red — three paper silhouettes looking up at it"),
                alt_fallback=("Papercut traffic light with green, orange and red "
                              "lights"),
                variant="sq")):
            for lv in _LEVELS:
                with st_block(_WASH[lv["id"]]):
                    st_write(bs.icon, lv["icon"], " ",
                             (bs.label, T(lv["label"], lang)), tag=t.div)
                    st_write(bs.line, T(lv["line"], lang), tag=t.div)
            st_space("v", "0.5vh")
            st_write(bs.frame, T(_FRAME, lang), " ",
                     citation(*_CITEKEYS), tag=t.div)
