"""Réserve SV4 — lui parler : la voix, du full-duplex à la simple dictée.

Troisième carte détaillée : les modes vocaux comparés — temps réel,
interruption naturelle, caméra/écran, et si c'est dans le GRATUIT. Décision NG
(QCM 2026-09-03) : Grok est PROJETÉ avec les autres. Meta AI n'a pas de ligne :
son vocal n'est pas vérifiable pour l'Europe (US d'abord) — politique « ? »,
il vit dans l'infobulle. Données ``facts.json`` (``services.voice``).

SPEAKER NOTES:
Only on a question. The study use-case first: rehearse a talk out loud, drill
a language, get quizzed by voice on the way to campus. Then the map: Gemini
Live gives the most for free (full-duplex + camera + screen); ChatGPT's new
Live mode is full-duplex too; Vibe is the odd one out — dictation only, no
spoken answers. Grok: free, but 13+ with parental consent up to 17.
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

_MARKER = {"en": "bk · Talk", "fr": "bk · Parler"}
_TITLE = {"en": ("Talk ", (s.project.titles.keyword, "to it")), "fr": ("Lui ", (s.project.titles.keyword, "parler"))}
_COLS = [
    ({"en": "Real-time", "fr": "Temps réel"}, {"en": "spoken conversation, speech-to-speech", "fr": "conversation parlée, speech-to-speech"}),
    ({"en": "Interrupt", "fr": "Interruption"}, {"en": "talk while it talks — it stops and listens", "fr": "parler pendant qu'il parle — il s'arrête et écoute"}),
    ({"en": "Camera/screen", "fr": "Caméra/écran"}, None),
    ({"en": "Free", "fr": "Gratuit"}, None),
]
_SUB = {"en": "HIGHLY VOLATILE — RECHECK!", "fr": "HAUTEMENT VOLATILE — REVÉRIFIEZ !"}

_TIP_TITLE = {"en": "Reading this map", "fr": "Lire cette carte"}
_TOOLTIP = [
    ({"en": "Why voice, for studying", "fr": "Pourquoi la voix, pour étudier"},
     {"en": ("Rehearse a presentation out loud, drill a language with a "
             "native-speed partner, get quizzed hands-free. Voice turns dead "
             "time into study time — the method stays the same."), "fr": "Répéter un exposé à voix haute, travailler une langue avec un partenaire au débit natif, se faire interroger mains libres. La voix change les temps morts en temps d'étude — la méthode ne change pas."}),
    ({"en": "Meta AI (no row)", "fr": "Meta AI (pas de ligne)"},
     {"en": ("Meta AI voice launched « in the US, Canada, Australia and New "
             "Zealand to start »; its availability in French/Europe is not "
             "verifiable on official pages — so no row, per the ❓ policy."), "fr": "Le vocal Meta AI a été lancé « aux USA, Canada, Australie et Nouvelle-Zélande d'abord » ; sa disponibilité en français/Europe n'est pas vérifiable sur les pages officielles — donc pas de ligne, politique ❓."}),
    ({"en": "Perplexity (no row)", "fr": "Perplexity (pas de ligne)"},
     {"en": ("Real-time voice exists (built on OpenAI's gpt-realtime) but "
             "full-duplex, camera and free quotas are all unverifiable at the "
             "source — three ❓ in a four-column row says nothing useful."), "fr": "La voix temps réel existe (bâtie sur gpt-realtime d'OpenAI) mais full-duplex, caméra et quotas gratuits sont invérifiables à la source — trois ❓ sur quatre colonnes ne disent rien d'utile."}),
    ({"en": "Grok, for this room", "fr": "Grok, pour cette salle"},
     {"en": ("Free tier with its own limits; 13 years minimum and parental "
             "consent required from 13 to 17 — say it if freshmen ask."), "fr": "Gratuit avec ses limites ; 13 ans minimum et accord parental obligatoire de 13 à 17 ans — à dire si des primo-inscrits demandent."}),
]

# ── La main de l'artiste ────────────────────────────────────────────────────
TUNING = {
    "matrix_zoom": 100,
    "logo_vh": 5,
}


def _rows():
    return [{"name": p["name"], "icon": p.get("icon", ""),
             "icon_ratio": p.get("ratio", 1.0), "hover": p.get("hover"),
             "cells": [(c["sym"], c.get("hover")) for c in p["cells"]],
             "details": [(h, b) for h, b in p["details"]]}
            for p in section("services")["voice"]]


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
        with st_zoom(115):
            st_write(bs.volatile, T(_SUB, lang), tag=t.div)
        st_space("v", "2.5vh")
        st_feature_matrix(s, _COLS, _rows(), lang,
                          zoom=TUNING["matrix_zoom"], logo_vh=TUNING["logo_vh"])
