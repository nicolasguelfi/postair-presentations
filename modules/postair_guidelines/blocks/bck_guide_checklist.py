"""The final test — the checklist (U8).

Five checkbox lines, then THE closing sentence of the whole session, giant
and amber, verbatim from Appendix 2: « I can explain and defend the work in
my own words, including in an oral follow-up. »

Le FAIT vit ici (règle NG 2026-08-18) : les cinq cases, la phrase finale
verbatim et le choix des citekeys s'éditent dans ce bloc. La phrase
bibliographique reste dérivée de ``references.bib`` par ``citation()`` — clé
inconnue = erreur bruyante.

Conversion R-i18n (2026-09-03) : les textes projetés sont des feuilles
{"en", "fr"} résolues par ``T()``/``TF()`` ; la phrase finale de l'Annexe 2
reste citée verbatim (EN dans les deux langues) ; SPEAKER NOTES restent EN.

SPEAKER NOTES:
One minute. Read the five boxes fast, then STOP, and read the amber sentence
slowly, once. « If you retain one sentence today, it is this one. » Suggest
the room photograph the slide — the tooltip says it too.
"""
# @guideline: postair-minimal

from custom.refs import citation
from custom.styles import Styles as s
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    item = s.project.body.bullet
    final = s.project.titles.subtitle + s.project.colors.amber + s.bold
    cite = s.project.body.caption + s.center_txt


bs = BlockStyles

# ── Le fait : la checklist de l'Appendix 2 (p.19) ───────────────────────────
_ITEMS = [
    {"en": "Course rules checked (allowed · restricted · forbidden — ask if unclear)",
     "fr": "Règles du cours vérifiées (permis · restreint · interdit — demandez si flou)"},
    {"en": "Only permitted uses", "fr": "Uniquement des usages permis"},
    {"en": "Everything that matters verified (facts, citations)",
     "fr": "Tout ce qui compte vérifié (faits, citations)"},
    {"en": "Data and copyright protected", "fr": "Données et droits d'auteur protégés"},
    {"en": "Disclosure ready (+ prompt log if required)",
     "fr": "Déclaration prête (+ journal de prompts si exigé)"},
]
#: La dernière case du document, copiée verbatim — LA phrase de clôture,
#: citée à l'identique dans les deux langues. i18n: verbatim
_FINAL = ("« I can explain and defend the work in my own words, including in "
          "an oral follow-up. »")
_TIP_HEAD = {"en": "Advice", "fr": "Conseil"}
_TIP = {"en": "Appendix 2 = this slide → photograph it",
        "fr": "Annexe 2 = cette slide → photographiez-la"}
_FINAL_HEAD = {"en": "The final box, verbatim", "fr": "La dernière case, verbatim"}
_CITEKEYS = ["i2tl2026-guidelines"]
#: Jamais projeté, gardé pour la vérifiabilité (entrée « big » de l'ancien
#: facts.json) : « Before you submit — the final test ».

_MARKER = {"en": "The final test", "fr": "Le test final"}
_TITLE = {"en": ("Before you submit — ",
                 (s.project.titles.keyword, "the final test")),
          "fr": ("Avant de rendre — ",
                 (s.project.titles.keyword, "le test final"))}
_TIP_TITLE = {"en": "Appendix 2 — the student checklist (p.19)",
              "fr": "Annexe 2 — la checklist étudiante (p.19)"}
_CITE_LINE = {"en": "Appendix 2, verbatim ", "fr": "Annexe 2, verbatim "}


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with st_zoom(130), g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(f"☐ {i+1}", T(item, lang))
                             for i, item in enumerate(_ITEMS)]
                            + [(T(_FINAL_HEAD, lang), _FINAL),
                               (T(_TIP_HEAD, lang), T(_TIP, lang))],
                )
        st_space("v", s.project.spacing.title_gap)
        for item in _ITEMS:
            with st_zoom(120):
                st_write(bs.item, "☐  ", T(item, lang), tag=t.div)
            st_space("v", "0.6vh")
        st_space("v", "2vh")
        st_write(bs.final, "☑  ", _FINAL, tag=t.div)
        # inline : « Appendix 2, verbatim » et le code forment UNE mention
        # d'attribution — coupée en deux lignes, l'étiquette resterait seule.
        st_write(bs.cite, T(_CITE_LINE, lang),
                 citation(*_CITEKEYS, inline=True), tag=t.div)
