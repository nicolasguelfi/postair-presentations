"""Réserve SV2 — créer TON agent : qui le permet, à quel niveau d'abonnement.

La première carte détaillée derrière la synthèse « Services » : la création
d'un agent personnalisé (GPT, Gem, agent Vibe, Project, agent Copilot, bot
Poe) lue par la grille Gratuit · Étudiant · Payant. Matrice générique
``st_feature_matrix`` (postair_matrix) : symboles en cellules, détail au
survol, ⓘ par ligne. Les données vivent dans ``facts.json`` (section
``services.create``, vérifiée le 2026-09-03) — corriger une offre = éditer la
donnée, jamais ce bloc.

SPEAKER NOTES:
Only on a question. The reading: Gemini is the free door for creating; on
ChatGPT you USE for free and CREATE with a paid plan (verified on a real
Plus account); Vibe agents are Pro (5.99 for students); Claude gives 5 free
Projects; Copilot needs the school account. HuggingChat's Assistants died in
the 2025 relaunch — proof this market moves, hence the volatility banner.
"""
# @guideline: postair-minimal

from custom.facts import section
from custom.styles import Styles as s
from postair_lang import T, TF
from postair_matrix import st_feature_matrix
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    caption = s.project.body.caption + s.center_txt
    volatile = s.project.body.caption + s.project.colors.coral + s.center_txt + s.bold


bs = BlockStyles

_MARKER = {"en": "bk · Create", "fr": "bk · Créer"}
#: Titre court (porte projection 2026-09-03 : « — who allows it » repliait le
#: titre sur trois lignes et poussait la légende au pli — les colonnes de la
#: matrice disent déjà qui le permet).
_TITLE = {"en": ("Create ", (s.project.titles.keyword, "YOUR agent")), "fr": ("Créer ", (s.project.titles.keyword, "TON agent"))}
_COLS = [
    ({"en": "Free", "fr": "Gratuit"}, None),
    ({"en": "Student", "fr": "Étudiant"}, {"en": "a dedicated student offer, and what it opens", "fr": "une offre étudiante dédiée, et ce qu'elle ouvre"}),
    ({"en": "Paid", "fr": "Payant"}, None),
]
_SUB = {"en": "HIGHLY VOLATILE — RECHECK!", "fr": "HAUTEMENT VOLATILE — REVÉRIFIEZ !"}

_TIP_TITLE = {"en": "Reading this map", "fr": "Lire cette carte"}
_TOOLTIP = [
    ({"en": "GPTs, precisely", "fr": "Les GPTs, précisément"},
     {"en": ("Everyone can USE existing GPTs, free plan included; CREATING "
             "them requires a paid plan — verified on a real Plus account "
             "(2026-09-03). Details per plan live in services-sources.md."), "fr": "Tout le monde peut UTILISER les GPTs existants, gratuit compris ; les CRÉER demande un plan payant — vérifié sur un vrai compte Plus (2026-09-03). Le détail par plan vit dans services-sources.md."}),
    ({"en": "A vanished product", "fr": "Un produit disparu"},
     {"en": ("HuggingChat « Assistants » no longer exist: the platform closed "
             "mid-2025 and relaunched as Omni without them. This market "
             "moves — hence the date on every map."), "fr": "Les « Assistants » HuggingChat n'existent plus : la plateforme a fermé mi-2025 et relancé en Omni sans eux. Ce marché bouge — d'où la date sur chaque carte."}),
    ({"en": "Also out there", "fr": "Aussi sur le marché"},
     {"en": ("Perplexity (answer engine, no agent builder in this sense) and "
             "Meta AI (no custom agents for students) are covered on the "
             "voice map instead."), "fr": "Perplexity (moteur de réponse, pas de builder d'agent en ce sens) et Meta AI (pas d'agents personnalisés pour étudiants) sont couverts sur la carte voix."}),
]

# ── La main de l'artiste ────────────────────────────────────────────────────
TUNING = {
    "matrix_zoom": 105,
    "logo_vh": 8,
    # tune1 (NG 2026-09-03) — head_zoom: en-têtes (global, % ; par colonne
    # via un dict {"head", "hover", "zoom"} dans _COLS) ; col_widths:
    # largeurs CSS des colonnes de features (None = égales) ; legend_zoom:
    # la légende, découplée du zoom de la matrice.
    "head_zoom": 100,
    "col_widths": None,
    "legend_zoom": 100,
}


def _rows():
    return [{"name": p["name"], "icon": p.get("icon", ""),
             "icon_ratio": p.get("ratio", 1.0), "hover": p.get("hover"),
             "url": p.get("url", ""), "icon_vh": p.get("icon_vh"),
             "cells": [(c["sym"], c.get("hover")) for c in p["cells"]],
             "details": [(h, b) for h, b in p["details"]]}
            for p in section("services")["create"]
            if p.get("shown", True)]  # poe1 m1 : masquage par la donnée


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with st_zoom(110), g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(T(h, lang), T(d, lang)) for h, d in _TOOLTIP],
                )
        with st_zoom(250):
            st_write(bs.volatile, T(_SUB, lang), tag=t.div)
        st_space("v", "2.5vh")
        st_feature_matrix(s, _COLS, _rows(), lang,
                          zoom=TUNING["matrix_zoom"], logo_vh=TUNING["logo_vh"],
                          head_zoom=TUNING["head_zoom"],
                          col_widths=TUNING["col_widths"],
                          legend_zoom=TUNING["legend_zoom"])
