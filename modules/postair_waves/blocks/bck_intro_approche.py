"""Why look back — the theoretical frame of the deck, in the 2+1 grid.

Kuhn reads a revolution as paradigm → anomaly → crisis → new paradigm; Perez
shows the great surges repeating their social pattern; and the POSTAIR report
documents that every stance of today's AI debate has an ancestor — the amber
row, the most visible of the slide (ligne NG ``design``, 2026-08-26). The
quadriptych of every wave IS that cycle, made visible.

SPEAKER NOTES:
One sentence per cell: revolutions follow a cycle (Kuhn) ; the cycle repeats
across surges (Perez) ; so — the amber line — the sixteen crossed waves are
DATA about ours. Then the substitution slide explains the rigour.
"""
# @guideline: postair-minimal

from custom.refs import citation
from custom.render import two_plus_one
from custom.styles import Styles as s
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt


bs = BlockStyles

_MARKER = {"en": "Why look back"}
_TITLE = {"en": ("Why look ", (s.project.titles.keyword, "back"))}
_TIP_TITLE = {"en": "The frame, in full sentences"}
_TIP = [
    ({"en": "A cycle"},
     {"en": "Kuhn, The Structure of Scientific Revolutions (1962): "
            "resistances, conversions and generation effects are part of "
            "every paradigm shift."}),
    ({"en": "A repetition"},
     {"en": "Perez, Technological Revolutions and Financial Capital (2002): "
            "each surge brings the same sequence of irruption, frenzy, "
            "crisis and deployment."}),
    ({"en": "An inheritance"},
     {"en": "The POSTAIR report documents it figure by figure: today's "
            "enthusiasts, sceptics and regulators all have documented "
            "ancestors in the sixteen previous waves."}),
]
# Les trois cellules de la grille 2+1 — titre + fragments (la citation
# reste hors feuille : ``citation()`` est un code, pas du texte).
_CYCLE = {"en": "A cycle"}
_CYCLE_TEXT = {"en": "paradigm → anomaly → crisis → new paradigm "}
_REPETITION = {"en": "A repetition"}
_REPETITION_TEXT = {"en": "great surges repeat their social pattern "}
_INHERITANCE = {"en": "An inheritance"}
_INHERITANCE_TEXT = {"en": ("every AI stance has a documented ",
                            (s.project.colors.keyword, "ancestor"))}


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(T(head, lang), T(detail, lang))
                             for head, detail in _TIP])
        st_space("v", "3vh")
        # Zooms réglables PAR SLIDE (contrat hero_split) — neutres ici.
        two_plus_one(
            [(T(_CYCLE, lang),
              T(_CYCLE_TEXT, lang), citation("kuhn1962")),
             (T(_REPETITION, lang),
              T(_REPETITION_TEXT, lang), citation("perez2002"))],
            (T(_INHERITANCE, lang), *TF(_INHERITANCE_TEXT, lang)),
            zoom_top=100, zoom_bottom=80)
