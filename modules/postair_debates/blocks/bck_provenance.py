"""Provenance — said once, for the whole document, on its own slide.

Until 2026-08-11 every figure card repeated two caption lines: « reconstructed
profile — commits its author, not the figure » and, for living people,
« video: a presentation of this living person, not their own words ». Decision
NG (2026-08-11): the cards stop carrying them — fifty-four repetitions turn an
honesty clause into wallpaper — and the clause is stated ONCE here, early,
where it frames everything that follows.

SPEAKER NOTES:
Project it once, before opening the first axis, and say it in one breath: the
postures are our reconstruction from primary sources — they commit us, never
the figures; and no living person is ever made to speak by generative AI —
their video is somebody presenting them. Then move on. If a card is challenged
later, come back here rather than improvising the answer.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

#: (picto, règle courte, forme télégraphique, phrase complète → tooltip).
_CLAUSES = [
    ("🧭", "Reconstructed postures",
     "primary sources · commits the AUTHOR, never the figure",
     "Each figure's position on an axis is a reconstruction from primary "
     "sources — it commits its author, never the figure."),
    ("🎙️", "Living people",
     "zero AI voice · video by the author, in his own name",
     "No living person is made to speak by generative AI. Their video is a "
     "presentation of them, by the author, in the author's own name."),
    ("❝", "Quotations",
     "VERBATIM, verified · code → full reference → References page",
     "Every quotation is verbatim and verified; its citation code opens the "
     "full reference, and the References page closes the document."),
]


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    picto = s.project.titles.register_title + s.center_txt
    clause = s.project.body.bullet + s.center_txt + s.bold
    detail = s.project.body.body + s.project.colors.keyword + s.center_txt


bs = BlockStyles


def build():
    st_marker("Provenance")
    with st_block(s.project.containers.page_fill_top):
        # Télégraphique (NG 2026-08-13) : trois cartes picto + mots-clés, les
        # phrases complètes vivent dans l'infobulle — plus aucun paragraphe
        # projeté, et le titre tient sur UNE ligne.
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "Three ", (s.project.titles.keyword, "rules"),
                         tag=t.div, toc_lvl="+1", label="Provenance")
            with g.cell():
                st_info_tooltip(title="Provenance — the full clauses",
                                entries=[(clause, full)
                                         for _, clause, _, full in _CLAUSES])
        st_space("v", "3vh")
        with st_grid(cols=s.project.grids.balanced(len(_CLAUSES)), gap="1.5vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_top) as g:
            for picto, clause, tele, _ in _CLAUSES:
                with g.cell(), st_block(s.project.cards.blue):
                    st_write(bs.picto, picto, tag=t.div)
                    st_write(bs.clause, clause, tag=t.div)
                    st_write(bs.detail, tele, tag=t.div)
