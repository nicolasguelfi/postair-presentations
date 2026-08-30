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
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.hero_split import hero_split

_STEPS = [
    ({"en": "Read the room first"}, {"en": "results page → divisive axes"}),
    ({"en": "Two or three axes"}, {"en": "never all nine · never in order"}),
    ({"en": "Both poles, always"}, {"en": "symmetrical corpus → play BOTH poles"}),
]

# ── Le texte projeté (règle R-i18n) ──────────────────────────────────────────
_MARKER = {"en": "A bank"}
_TITLE = {"en": ("A ", (s.project.titles.keyword, "bank"), ", not a talk")}
_LEAD = {"en": ("Open only the axes where ", (s.project.titles.keyword, "this room"),
                " disagrees")}
_TIP_TITLE = {"en": "Using the debates bank"}
_TIP_CONTENT = ({"en": "What is in it"},
                {"en": ("{poles} poles — the two sides of each of the nine axes. Each pole "
                        "has its identity and three survey statements, three historical "
                        "figures with a sourced quotation and a presentation video, and "
                        "three contemporary arguments of three different natures.")})
_TIP_CHOOSE = ({"en": "How to choose"},
               {"en": ("The results page of the day ranks the statements by disagreement. "
                       "Open the axes where this room splits — they are never the same two "
                       "rooms running.")})
_TIP_SYMMETRY = ({"en": "Symmetry is the rule"},
                 {"en": ("Every pole has a facing pole with equally sourced material. "
                         "Opening one without the other turns a debate into a lecture with "
                         "a slide deck.")})
_TIP_PROVENANCE = ({"en": "Provenance"},
                   {"en": ("The figures' postures are reconstructed from primary sources and "
                           "commit their author, not the figures. For living people, the "
                           "video presents them — this corpus never makes a living person "
                           "speak through generative AI.")})
_TIP_DECK = ({"en": "Provenance of the deck"},
             {"en": ("Instrument v{instrument} · debate material v{debate} · content "
                     "regenerated from the study, never typed into a slide.")})

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
    st_marker(T(_MARKER, lang))
    meta = manifest().get("metadata", {})
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[
                        (T(_TIP_CONTENT[0], lang),
                         T(_TIP_CONTENT[1], lang).format(poles=len(poles()))),
                        (T(_TIP_CHOOSE[0], lang), T(_TIP_CHOOSE[1], lang)),
                        (T(_TIP_SYMMETRY[0], lang), T(_TIP_SYMMETRY[1], lang)),
                        (T(_TIP_PROVENANCE[0], lang), T(_TIP_PROVENANCE[1], lang)),
                        (T(_TIP_DECK[0], lang),
                         T(_TIP_DECK[1], lang).format(
                             instrument=meta.get("instrument_version", "?"),
                             debate=meta.get("debate_version", "?"))),
                    ],
                )
        st_space("v", s.project.spacing.title_gap)
        st_write(bs.lead, *TF(_LEAD, lang), tag=t.div)
        st_space("v", "2vh")
        # Gabarit par défaut (NG 2026-08-13) : la roue des axes à gauche —
        # l'écran n'est plus vide à moitié — et les trois règles empilées.
        with hero_split(s, image=lambda: st_image(
                s.project.cards.media_center, width="min(38vw, 60vh)", uri=_RADAR,
                alt="The nine-axes wheel, each axis ending in a question mark")):
            for step, detail in _STEPS:
                with st_block(s.project.cards.blue):
                    st_write(bs.step, T(step, lang), tag=t.div)
                    st_write(bs.detail, T(detail, lang), tag=t.div)
