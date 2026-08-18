"""The final test — the checklist (U8).

Five checkbox lines, then THE closing sentence of the whole session, giant
and amber, verbatim from Appendix 2: « I can explain and defend the work in
my own words, including in an oral follow-up. »

Le FAIT vit ici (règle NG 2026-08-18) : les cinq cases, la phrase finale
verbatim et le choix des citekeys s'éditent dans ce bloc. La phrase
bibliographique reste dérivée de ``references.bib`` par ``citation()`` — clé
inconnue = erreur bruyante.

SPEAKER NOTES:
One minute. Read the five boxes fast, then STOP, and read the amber sentence
slowly, once. « If you retain one sentence today, it is this one. » Suggest
the room photograph the slide — the tooltip says it too.
"""
# @guideline: postair-minimal

from custom.refs import citation
from custom.styles import Styles as s
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    item = s.project.body.bullet + s.center_txt
    final = s.project.titles.subtitle + s.project.colors.amber + s.center_txt + s.bold
    cite = s.project.body.caption + s.center_txt


bs = BlockStyles

# ── Le fait : la checklist de l'Appendix 2 (p.19) ───────────────────────────
_ITEMS = [
    "Course rules checked (allowed · restricted · forbidden — ask if unclear)",
    "Only permitted uses",
    "Everything that matters verified (facts, citations)",
    "Data and copyright protected",
    "Disclosure ready (+ prompt log if required)",
]
#: La dernière case du document, copiée verbatim — LA phrase de clôture.
_FINAL = ("« I can explain and defend the work in my own words, including in "
          "an oral follow-up. »")
_TIP = "Appendix 2 = this slide → photograph it"
_CITEKEYS = ["i2tl2026-guidelines"]
#: Jamais projeté, gardé pour la vérifiabilité (entrée « big » de l'ancien
#: facts.json) : « Before you submit — the final test ».


def build():
    st_marker("The final test")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "Before you submit — ",
                         (s.project.titles.keyword, "the final test"),
                         tag=t.div, toc_lvl="+1", label="The final test")
            with g.cell():
                st_info_tooltip(
                    title="Appendix 2 — the student checklist (p.19)",
                    entries=[(f"☐ {i+1}", item)
                             for i, item in enumerate(_ITEMS)]
                            + [("The final box, verbatim", _FINAL),
                               ("Advice", _TIP)],
                )
        st_space("v", s.project.spacing.title_gap)
        for item in _ITEMS:
            st_write(bs.item, "☐  ", item, tag=t.div)
            st_space("v", "0.6vh")
        st_space("v", "2vh")
        st_write(bs.final, "☑  ", _FINAL, tag=t.div)
        # inline : « Appendix 2, verbatim » et le code forment UNE mention
        # d'attribution — coupée en deux lignes, l'étiquette resterait seule.
        st_write(bs.cite, "Appendix 2, verbatim ",
                 citation(*_CITEKEYS, inline=True), tag=t.div)
