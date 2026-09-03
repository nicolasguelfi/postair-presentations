"""Reflex 4 — the red lines (U5).

Five sober picto cards — the five families that cover the guidelines' ten
non-permitted practices — with Guardo, the control mascot, as a benevolent
guardian beside the title row. The complete list of the ten practices, in
student words with the WHY of each, lives in the tooltip.

Le FAIT vit ici (règle NG 2026-08-18) : les cinq familles, la règle du doute
et le choix des citekeys s'éditent dans ce bloc. La phrase bibliographique
reste dérivée de ``references.bib`` par ``citation()`` — clé inconnue =
erreur bruyante.

Conversion R-i18n (2026-09-03) : les textes projetés sont des feuilles
{"en", "fr"} résolues par ``T()``/``TF()`` ; SPEAKER NOTES et ``alt=``
restent EN.

SPEAKER NOTES:
Three minutes, calm voice — informative, not menacing: these are the lines
NOBODY crosses, and each protects something the room cares about (their name,
the truth, their data, the fairness of exams). Close on the footer line: in
doubt, ask BEFORE using it.
"""
# @guideline: postair-minimal

from custom.refs import citation
from custom.styles import Styles as s
from postair_data import mascot
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.ai_mark import dd35_overlay


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    icon = s.project.titles.subtitle + s.center_txt
    short = s.project.body.caption + s.center_txt + s.bold
    footer = s.project.body.body + s.project.colors.amber + s.center_txt + s.bold
    cite = s.project.body.caption + s.center_txt
    mascot_name = s.project.body.mascot_name + s.center_txt


bs = BlockStyles

# ── Le fait : les cinq familles des dix pratiques non permises (§4 p.8) ─────
#: « short » est projeté sur la carte ; « detail » vit dans le tooltip.
_CARDS = [
    {"icon": "🎭",
     "short": {"en": "Passing AI off as you",
               "fr": "Faire passer l'IA pour vous"},
     "detail": {"en": ("Submitting AI output as entirely your own without "
                       "disclosure; letting AI be the central intellectual "
                       "contribution when the assessment targets YOUR reasoning; "
                       "impersonation."),
                "fr": ("Rendre une sortie d'IA comme entièrement vôtre sans "
                       "déclaration ; laisser l'IA porter la contribution "
                       "intellectuelle centrale quand l'évaluation vise VOTRE "
                       "raisonnement ; usurpation d'identité.")}},
    {"icon": "🧪",
     "short": {"en": "Fabricating", "fr": "Fabriquer"},
     "detail": {"en": ("Generating or altering data, results, citations or "
                       "evidence; citing unverified or non-existent sources."),
                "fr": ("Générer ou altérer des données, résultats, citations ou "
                       "preuves ; citer des sources non vérifiées ou "
                       "inexistantes.")}},
    {"icon": "🕳️",
     "short": {"en": "Concealing", "fr": "Dissimuler"},
     "detail": {"en": ("Chaining tools to hide AI involvement or to circumvent "
                       "integrity safeguards."),
                "fr": ("Enchaîner des outils pour cacher l'implication de l'IA ou "
                       "contourner les garde-fous d'intégrité.")}},
    {"icon": "🔐",
     "short": {"en": "Sensitive data & protected material",
               "fr": "Données sensibles & matériel protégé"},
     "detail": {"en": ("Personal or sensitive data into AI tools; other people's "
                       "data or protected course material into external tools; "
                       "uploading protected teaching material without "
                       "authorisation."),
                "fr": ("Des données personnelles ou sensibles dans des outils "
                       "d'IA ; les données d'autrui ou du matériel de cours "
                       "protégé dans des outils externes ; téléverser du matériel "
                       "d'enseignement protégé sans autorisation.")}},
    {"icon": "📝",
     "short": {"en": "AI in exams", "fr": "L'IA aux examens"},
     "detail": {"en": ("Using AI against the course rules — in exams and controlled "
                       "assessments above all."),
                "fr": ("Utiliser l'IA contre les règles du cours — aux examens et "
                       "évaluations contrôlées avant tout.")}},
]
_FOOTER_HEAD = {"en": "The rule of doubt", "fr": "La règle du doute"}
_FOOTER = {"en": ("10 practices = potential misconduct (§4 p.8) · unless the course "
                  "explicitly allows · in doubt → BEFORE"),
           "fr": ("10 pratiques = manquement potentiel (§4 p.8) · sauf permission "
                  "explicite du cours · dans le doute → AVANT")}
_CITEKEYS = ["i2tl2026-guidelines"]
#: Jamais projeté, gardé pour la vérifiabilité (entrée « big » de l'ancien
#: facts.json) : « The red lines ».

_MARKER = {"en": "Red lines", "fr": "Lignes rouges"}
_TITLE = {"en": ("Reflex 4 — the ", (s.project.titles.keyword, "red lines")),
          "fr": ("Réflexe 4 — les ",
                 (s.project.titles.keyword, "lignes rouges"))}
_TIP_TITLE = {"en": "The ten non-permitted practices (section 4, p.8)",
              "fr": "Les dix pratiques non permises (section 4, p.8)"}
_CLOSE = {"en": "In doubt — ask BEFORE. ",
          "fr": "Dans le doute — demandez AVANT. "}


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="80% 12% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
            with g.cell():
                guardo = mascot("Guardo")
                st_image(s.project.cards.media_center, width="5.5vw",
                         uri=guardo["image"], alt="Guardo, the control mascot, benevolent guardian",
                         overlay=dd35_overlay())
                st_write(bs.mascot_name, guardo["name"], tag=t.div)
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(f"{c['icon']} {T(c['short'], lang)}",
                              T(c["detail"], lang)) for c in _CARDS]
                            + [(T(_FOOTER_HEAD, lang), T(_FOOTER, lang))],
                )
        st_space("v", s.project.spacing.title_gap)
        with st_grid(cols=s.project.grids.balanced(len(_CARDS)), gap="1vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for c in _CARDS:
                with g.cell(), st_block(s.project.cards.coral):
                    st_write(bs.icon, c["icon"], tag=t.div)
                    st_write(bs.short, T(c["short"], lang), tag=t.div)
        st_space("v", "2.5vh")
        st_write(bs.footer, T(_CLOSE, lang), citation(*_CITEKEYS), tag=t.div)
