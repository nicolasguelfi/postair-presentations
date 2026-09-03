"""Réserve SV5 — les offres étudiantes : l'éligibilité LUXEMBOURG d'abord.

Quatrième carte détaillée — celle qui manque partout ailleurs : les offres
étudiantes du marché, jugées par la seule question qui compte pour cette
salle : « et avec mon adresse @uni.lu ? ». Décision NG (QCM 2026-09-03) : la
ligne uni.lu est FACTUELLE et vérifiée sur les pages publiques — et comme le
site est derrière un mur anti-bot, elle porte ❓ là où le texte exact n'a pas
pu être relu (politique « ? »). Données ``facts.json`` (``services.students``).

SPEAKER NOTES:
Only on a question — but this is the map students photograph. Two real deals
for Luxembourg: Google (a free year of AI Plus — school email + SheerID,
before Dec 31) and Mistral (Vibe Pro at 5.99). OpenAI's offers are US-only —
say it before someone wastes an evening. The uni.lu line: Copilot is the
University-supported chatbot; the ❓ means « re-read the exact wording on
uni.lu yourself » — it is YOUR university's page, not mine.
"""
# @guideline: postair-minimal

from custom.facts import section
from custom.refs import citation
from custom.styles import Styles as s
from postair_lang import T, TF
from postair_matrix import st_feature_matrix
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    caption = s.project.body.caption + s.center_txt
    punch = s.project.titles.subtitle + s.project.colors.amber + s.center_txt + s.bold


bs = BlockStyles

_MARKER = {"en": "bk · Student deals", "fr": "bk · Offres étudiantes"}
_TITLE = {"en": ("The ", (s.project.titles.keyword, "student deals")), "fr": ("Les ", (s.project.titles.keyword, "offres étudiantes"))}
_COLS = [
    ({"en": "Offer", "fr": "Offre"}, None),
    ({"en": "Price / duration", "fr": "Prix / durée"}, None),
    ({"en": "Luxembourg", "fr": "Luxembourg"}, {"en": "eligibility with a @uni.lu / @student.uni.lu address", "fr": "éligibilité avec une adresse @uni.lu / @student.uni.lu"}),
]
_PUNCH = {"en": "your @uni.lu address is worth money — use it", "fr": "votre adresse @uni.lu vaut de l'argent — servez-vous-en"}
_SOURCES = {"en": "official pages · verified 2026-09-03 ", "fr": "pages officielles · vérifié le 2026-09-03 "}
_CITEKEYS = ["google-student-2026", "mistral-pricing-2026", "openai-students-2026",
             "perplexity-students-2026", "claude-projects-2026", "unilu-copilot-2025"]

_TIP_TITLE = {"en": "Reading this map", "fr": "Lire cette carte"}
_TOOLTIP = [
    ({"en": "The two real deals", "fr": "Les deux vraies offres"},
     {"en": ("Google: one free year of AI Plus, Luxembourg in the supported "
             "countries — SheerID + school email, claim before 2026-12-31, "
             "auto-converts to ~8 €/month unless cancelled. Mistral: Vibe Pro "
             "5.99 €/month for verified students (12 months, new accounts)."), "fr": "Google : un an d'AI Plus offert, Luxembourg dans les pays supportés — SheerID + email d'école, avant le 31-12-2026, bascule à ~8 €/mois sauf annulation. Mistral : Vibe Pro 5,99 €/mois pour étudiants vérifiés (12 mois, nouveaux comptes)."}),
    ({"en": "The trap", "fr": "Le piège"},
     {"en": ("OpenAI's student offers (Back to School, historic discount) are "
             "US or US/Canada only — the official article titles say so. A "
             "Luxembourg student cannot claim them."), "fr": "Les offres étudiantes OpenAI (Back to School, réduction historique) sont USA ou USA/Canada uniquement — les titres mêmes des articles officiels le disent. Un étudiant luxembourgeois ne peut pas les réclamer."}),
    ({"en": "The uni.lu line", "fr": "La ligne uni.lu"},
     {"en": ("Indexed uni.lu pages (news + the Sept. 2025 GenAI guidelines "
             "PDF) present Copilot as the officially supported chatbot, for "
             "data-privacy reasons. The site blocks robots, so the exact "
             "wording could not be re-read — that is the ❓: check the page "
             "with your own browser."), "fr": "Les pages uni.lu indexées (news + le PDF des lignes directrices IA de sept. 2025) présentent Copilot comme le chatbot officiellement soutenu, pour des raisons de confidentialité des données. Le site bloque les robots, le texte exact n'a pas pu être relu — c'est le ❓ : vérifiez la page avec votre propre navigateur."}),
]

# ── La main de l'artiste ────────────────────────────────────────────────────
TUNING = {
    "matrix_zoom": 92,   # porte projection 2026-09-03 : ×1.04/×1.10 à 100
    "logo_vh": 5,
    "punch_zoom": 100,
}


def _rows():
    return [{"name": p["name"], "icon": p.get("icon", ""),
             "icon_ratio": p.get("ratio", 1.0), "hover": p.get("hover"),
             "cells": [(c["sym"], c.get("hover")) for c in p["cells"]],
             "details": [(h, b) for h, b in p["details"]]}
            for p in section("services")["students"]]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with st_zoom(140), g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(T(h, lang), T(d, lang)) for h, d in _TOOLTIP],
                )
        st_space("v", s.project.spacing.title_gap)
        st_feature_matrix(s, _COLS, _rows(), lang,
                          zoom=TUNING["matrix_zoom"], logo_vh=TUNING["logo_vh"])
        st_space("v", "2vh")
        with st_zoom(TUNING["punch_zoom"]):
            st_write(bs.punch, T(_PUNCH, lang), tag=t.div)
        st_space("v", "1vh")
        st_write(bs.caption, T(_SOURCES, lang), citation(*_CITEKEYS), tag=t.div)
