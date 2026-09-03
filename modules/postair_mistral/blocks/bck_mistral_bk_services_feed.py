"""Réserve SV3 — nourrir l'agent de TON cours : fichiers, volumes, instruction.

Deuxième carte détaillée : ce que chaque plateforme accepte comme base de
connaissance (le cœur de la méthode — étape 2) et la taille de l'instruction
système. Matrice ``st_feature_matrix`` ; données ``facts.json``
(``services.feed``, vérifiées le 2026-09-03). Politique « ? » : une taille
d'instruction non documentée officiellement s'affiche ❓ — la plupart le sont.

SPEAKER NOTES:
Only on a question. The line to say: an agent is only as good as the course
you feed it — this map is step 2 of the method, shop by shop. Poe's 5 GB is
the free-tier giant; Copilot is the only one to DOCUMENT its instruction size
(8,000 characters); most others do not publish theirs — that is what the ❓
means, not a defect of the tool.
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

_MARKER = {"en": "bk · Feed", "fr": "bk · Nourrir"}
_TITLE = {"en": ("Feed it ", (s.project.titles.keyword, "your course")), "fr": ("Le nourrir de ", (s.project.titles.keyword, "ton cours"))}
_COLS = [
    ({"en": "Files / agent", "fr": "Fichiers / agent"}, None),
    ({"en": "Volume", "fr": "Volume"}, {"en": "per-file caps and total knowledge base", "fr": "plafonds par fichier et base totale"}),
    ({"en": "Instruction", "fr": "Instruction"}, {"en": "max size of the system instructions", "fr": "taille max des instructions système"}),
]
_SUB = {"en": "HIGHLY VOLATILE — RECHECK!", "fr": "HAUTEMENT VOLATILE — REVÉRIFIEZ !"}

_TIP_TITLE = {"en": "Reading this map", "fr": "Lire cette carte"}
_TOOLTIP = [
    ({"en": "Why it matters", "fr": "Pourquoi ça compte"},
     {"en": ("This is step 2 of the method (provide the sources): the agent "
             "answers FROM your course only if the platform can hold it. "
             "Sizes decide whether one PDF or the whole semester fits."), "fr": "C'est l'étape 2 de la méthode (fournir les sources) : l'agent répond DEPUIS ton cours seulement si la plateforme peut le porter. Les tailles décident si UN pdf ou tout le semestre rentre."}),
    ({"en": "The ❓ cells", "fr": "Les cellules ❓"},
     {"en": ("A ❓ means « not documented on an official page as of "
             "2026-09-03 » — most editors simply do not publish their "
             "instruction cap. Only Microsoft documents 8,000 characters."), "fr": "Un ❓ signifie « non documenté sur une page officielle au 2026-09-03 » — la plupart des éditeurs ne publient pas leur plafond d'instruction. Seul Microsoft documente 8 000 caractères."}),
    ({"en": "The free-tier giant", "fr": "Le géant du gratuit"},
     {"en": ("Poe: 5 GB or 30 million characters of knowledge on the free "
             "plan — by far the most generous documented base."), "fr": "Poe : 5 Go ou 30 millions de caractères de connaissance en gratuit — de loin la base documentée la plus généreuse."}),
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
            for p in section("services")["feed"]]


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
        with st_zoom(250):
            st_write(bs.volatile, T(_SUB, lang), tag=t.div)
        st_space("v", "2.5vh")
        st_feature_matrix(s, _COLS, _rows(), lang,
                          zoom=TUNING["matrix_zoom"], logo_vh=TUNING["logo_vh"],
                          head_zoom=TUNING["head_zoom"],
                          col_widths=TUNING["col_widths"],
                          legend_zoom=TUNING["legend_zoom"])
