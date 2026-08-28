"""How this bank is used — the opening slide of the debates deck.

Deliberately the only slide of the document that is about the document. It
exists because the deck is a bank, not a talk: whoever opens it, months from
now, must understand in twenty seconds that they are not meant to go through
it from the first slide to the last.

SPEAKER NOTES:
Do not project this one to the room — it is for you, and for whoever presents
this after you. Open the results page first, note the two or three axes where
the room actually splits, and go straight to those. Fifteen minutes buys two
axes done properly. Going in order, from the first, is the one failure mode
this document has.
"""
# @guideline: postair-minimal

from custom.content import manifest, poles
from custom.styles import Styles as s
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.hero_split import hero_split

_STEPS = [
    ("Read the room first", "results page → divisive axes"),
    ("Two or three axes", "never all nine · never in order"),
    ("Both poles, always", "symmetrical corpus → play BOTH poles"),
]

#: La roue des neuf axes — le visuel que la salle a déjà vu dans l'ouverture ;
#: copie versionnée du SVG d'opening (illustration, exception assumée).
_RADAR = "images/postair_radar_question.svg"


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    step = s.project.body.bullet + s.center_txt + s.bold
    detail = s.project.body.caption + s.center_txt
    lead = s.project.titles.subtitle + s.center_txt


bs = BlockStyles


def build(lang: str = "en", **_):
    st_marker("A bank")
    meta = manifest().get("metadata", {})
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "A ", (s.project.titles.keyword, "bank"), ", not a talk",
                         tag=t.div, toc_lvl="+1", label="A bank")
            with g.cell():
                st_info_tooltip(
                    title="Using the debates bank",
                    entries=[
                        ("What is in it", f"{len(poles())} poles — the two sides of each of the "
                         f"nine axes. Each pole has its identity and three survey statements, "
                         f"three historical figures with a sourced quotation and a presentation "
                         f"video, and three contemporary arguments of three different natures."),
                        ("How to choose", "The results page of the day ranks the statements by "
                         "disagreement. Open the axes where this room splits — they are never "
                         "the same two rooms running."),
                        ("Symmetry is the rule", "Every pole has a facing pole with equally "
                         "sourced material. Opening one without the other turns a debate into "
                         "a lecture with a slide deck."),
                        ("Provenance", "The figures' postures are reconstructed from primary "
                         "sources and commit their author, not the figures. For living people, "
                         "the video presents them — this corpus never makes a living person "
                         "speak through generative AI."),
                        ("Provenance of the deck", f"Instrument v{meta.get('instrument_version', '?')} · "
                         f"debate material v{meta.get('debate_version', '?')} · content "
                         f"regenerated from the study, never typed into a slide."),
                    ],
                )
        st_space("v", s.project.spacing.title_gap)
        st_write(bs.lead, "Open only the axes where ",
                 (s.project.titles.keyword, "this room"), " disagrees", tag=t.div)
        st_space("v", "2vh")
        # Gabarit par défaut (NG 2026-08-13) : la roue des axes à gauche —
        # l'écran n'est plus vide à moitié — et les trois règles empilées.
        with hero_split(s, image=lambda: st_image(
                s.project.cards.media_center, width="min(38vw, 60vh)", uri=_RADAR,
                alt="The nine-axes wheel, each axis ending in a question mark")):
            for step, detail in _STEPS:
                with st_block(s.project.cards.blue):
                    st_write(bs.step, step, tag=t.div)
                    st_write(bs.detail, detail, tag=t.div)
