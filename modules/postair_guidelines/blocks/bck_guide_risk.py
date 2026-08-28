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
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t
from streamtex.styles import Style

from postair_pack.components.hero_split import hero_split

# ── Le fait : les trois niveaux de risque (guidelines, section 4) ───────────
#: « label » et « line » sont projetés sur les cartes ; « detail » vit dans
#: le tooltip ; « id » sélectionne le lavis sémantique.
_LEVELS = [
    {"id": "low", "icon": "🟢", "label": "LOW",
     "line": "YOU are the source — the AI polishes",
     "detail": ("You know the answer; the AI works on the surface: "
                "proofreading, form, organising your own ideas.")},
    {"id": "medium", "icon": "🟠", "label": "MODERATE",
     "line": "You explore — and you VERIFY",
     "detail": ("You are learning the topic: summaries and syntheses of "
                "complex material help, but you check omissions, distortions "
                "and inventions against reliable sources.")},
    {"id": "high", "icon": "🔴", "label": "HIGH",
     "line": "You delegate what you cannot verify",
     "detail": ("You depend on the AI for claims you cannot check — or the "
                "AI replaces the assessed learning objective itself. "
                "Hallucinations, fabricated citations, overconfidence.")},
]
_FRAME = "risk level ↑ = verification ↑ · never a ban"
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


def build(lang: str = "en", **_):
    st_marker("Three levels")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "Reflex 3 — the ",
                         (s.project.titles.keyword, "three risk levels"),
                         tag=t.div, toc_lvl="+1", label="Three levels")
            with g.cell():
                st_info_tooltip(
                    title="The levels (guidelines, section 4)",
                    entries=[(f"{lv['icon']} {lv['label']} — {lv['line']}",
                              lv["detail"]) for lv in _LEVELS]
                            + [("The frame", _FRAME),
                               ("The red case that matters", "« The AI replaces the "
                                "assessed learning objective » is always high risk — "
                                "that is the one to remember.")],
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
                    st_write(bs.icon, lv["icon"], " ", (bs.label, lv["label"]),
                             tag=t.div)
                    st_write(bs.line, lv["line"], tag=t.div)
            st_space("v", "0.5vh")
            st_write(bs.frame, _FRAME, " ",
                     citation(*_CITEKEYS), tag=t.div)
