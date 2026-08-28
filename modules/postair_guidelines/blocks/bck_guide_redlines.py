"""Reflex 4 — the red lines (U5).

Five sober picto cards — the five families that cover the guidelines' ten
non-permitted practices — with Guardo, the control mascot, as a benevolent
guardian beside the title row. The complete list of the ten practices, in
student words with the WHY of each, lives in the tooltip.

Le FAIT vit ici (règle NG 2026-08-18) : les cinq familles, la règle du doute
et le choix des citekeys s'éditent dans ce bloc. La phrase bibliographique
reste dérivée de ``references.bib`` par ``citation()`` — clé inconnue =
erreur bruyante.

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
    {"icon": "🎭", "short": "Passing AI off as you",
     "detail": ("Submitting AI output as entirely your own without "
                "disclosure; letting AI be the central intellectual "
                "contribution when the assessment targets YOUR reasoning; "
                "impersonation.")},
    {"icon": "🧪", "short": "Fabricating",
     "detail": ("Generating or altering data, results, citations or "
                "evidence; citing unverified or non-existent sources.")},
    {"icon": "🕳️", "short": "Concealing",
     "detail": ("Chaining tools to hide AI involvement or to circumvent "
                "integrity safeguards.")},
    {"icon": "🔐", "short": "Sensitive data & protected material",
     "detail": ("Personal or sensitive data into AI tools; other people's "
                "data or protected course material into external tools; "
                "uploading protected teaching material without "
                "authorisation.")},
    {"icon": "📝", "short": "AI in exams",
     "detail": ("Using AI against the course rules — in exams and controlled "
                "assessments above all.")},
]
_FOOTER = ("10 practices = potential misconduct (§4 p.8) · unless the course "
           "explicitly allows · in doubt → BEFORE")
_CITEKEYS = ["i2tl2026-guidelines"]
#: Jamais projeté, gardé pour la vérifiabilité (entrée « big » de l'ancien
#: facts.json) : « The red lines ».


def build(lang: str = "en", **_):
    st_marker("Red lines")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="80% 12% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "Reflex 4 — the ", (s.project.titles.keyword, "red lines"),
                         tag=t.div, toc_lvl="+1", label="Red lines")
            with g.cell():
                guardo = mascot("Guardo")
                st_image(s.project.cards.media_center, width="5.5vw",
                         uri=guardo["image"], alt="Guardo, the control mascot, benevolent guardian",
                         overlay=dd35_overlay())
                st_write(bs.mascot_name, guardo["name"], tag=t.div)
            with g.cell():
                st_info_tooltip(
                    title="The ten non-permitted practices (section 4, p.8)",
                    entries=[(f"{c['icon']} {c['short']}", c["detail"])
                             for c in _CARDS]
                            + [("The rule of doubt", _FOOTER)],
                )
        st_space("v", s.project.spacing.title_gap)
        with st_grid(cols=s.project.grids.balanced(len(_CARDS)), gap="1vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for c in _CARDS:
                with g.cell(), st_block(s.project.cards.coral):
                    st_write(bs.icon, c["icon"], tag=t.div)
                    st_write(bs.short, c["short"], tag=t.div)
        st_space("v", "2.5vh")
        st_write(bs.footer, "In doubt — ask BEFORE. ", citation(*_CITEKEYS), tag=t.div)
