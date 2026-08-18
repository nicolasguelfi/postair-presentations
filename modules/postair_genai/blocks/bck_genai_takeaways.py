"""Takeaways (G12) — four memo cards, and nothing else.

Four numbered cards, big enough to be photographed from the back row. The
resources to go further live in the tooltip; the full bibliography closes the
document one slide later.

Le FAIT vit ici (règle NG 2026-08-18) : les quatre cartes-mémo s'éditent dans
ce bloc. Aucune affirmation sourcée sur cette slide — quand une source
arrive, la phrase bibliographique reste dérivée de ``references.bib`` par
``citation()``/``cite`` — clé inconnue = erreur bruyante.

SPEAKER NOTES:
One minute. Read the four cards, slowly, once. Suggest the room photograph
the slide. Hand over to the Mistral session: « you now know what it is —
next, you build with it ».
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    number = s.project.titles.subtitle + s.project.colors.amber + s.center_txt + s.bold
    short = s.project.body.bullet + s.center_txt + s.bold
    detail = s.project.body.caption + s.center_txt


bs = BlockStyles

# ── Les quatre cartes-mémo — photographiables du dernier rang ───────────────
_TAKEAWAYS = [
    {
        "n": "1",
        "short": "Predicting ≠ knowing",
        "detail": ("A language model produces the plausible next word. "
                   "Fluency is not truth."),
    },
    {
        "n": "2",
        "short": "Verify everything that matters",
        "detail": "names · numbers · references → check at the source",
    },
    {
        "n": "3",
        "short": "A learning tool, not a replacement",
        "detail": "it explains · it never learns IN YOUR PLACE",
    },
    {
        "n": "4",
        "short": "Your posture is yours",
        "detail": "9 axes · no right answer · not choosing = choosing",
    },
]


def build():
    st_marker("Takeaways")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "Four things to ", (s.project.titles.keyword, "take home"),
                         tag=t.div, toc_lvl="+1", label="Takeaways")
            with g.cell():
                st_info_tooltip(
                    title="To go further",
                    entries=[
                        ("At UL", "Computer science and AI courses, the university's "
                         "AI learning resources, and the guidelines session right "
                         "after Mistral."),
                        ("Beyond UL", "Open MOOCs on machine learning fundamentals, "
                         "and accessible reads on how language models work — ask, "
                         "the speaker has favourites."),
                        ("The session's sources", "Every number and claim of this "
                         "session is on the References page at the end of this "
                         "document — hover any citation code to see its source."),
                    ],
                )
        st_space("v", s.project.spacing.title_gap)
        with st_grid(cols=s.project.grids.balanced(len(_TAKEAWAYS)), gap="1.2vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for item in _TAKEAWAYS:
                with g.cell(), st_block(s.project.cards.blue):
                    st_write(bs.number, item["n"], tag=t.div)
                    st_write(bs.short, item["short"], tag=t.div)
                    st_space("v", "0.6vh")
                    st_write(bs.detail, item["detail"], tag=t.div)
