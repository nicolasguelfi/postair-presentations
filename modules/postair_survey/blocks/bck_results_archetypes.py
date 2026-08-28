"""The six archetypes — names read from the shared studio manifest.

The names come from ``_SHARED/mascots/i18n.json``, the same file the survey
application reads, so a rename propagates to the deck without an edit here.
That file carries names only: the published archetype descriptions live in
the study, and this slide does not paraphrase them. What it does explain —
because the room misunderstands it every time — is the mechanism: an
archetype is the NEAREST reference point in nine dimensions, not a box you
have been sorted into.

SPEAKER NOTES:
Four minutes. The room is about to be told which archetype it resembles, and
half of them will hear "you have been put in a category". Kill that first:
these are six reference points in a nine-dimensional space, and the app shows
you the closest one — with a distance. Two people with the same archetype can
be quite different, and someone can sit almost exactly between two. Then say
the fun part: the same engine scores the great figures, so in a minute you
will find out which one of them you argue like.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from postair_data import archetypes
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

_CARDS = [s.project.cards.amber, s.project.cards.blue, s.project.cards.teal,
          s.project.cards.blue, s.project.cards.coral, s.project.cards.teal]


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    name = s.project.body.name_double
    lead = s.project.body.bullet + s.center_txt


bs = BlockStyles

#: Les six noms viennent du manifeste du studio (``archetypes()``) — hors feuille.
_MARKER = {"en": "The six archetypes"}
_TITLE = {"en": ("Six ", (s.project.titles.keyword, "reference archetypes"),
                 " — not six boxes")}
_LEAD = {"en": ("The app shows the ", (s.project.titles.keyword, "nearest"),
                " one + your distance to it")}
_TIP_TITLE = {"en": "What an archetype is, and is not"}
_TIP = [
    ({"en": "A reference point"},
     {"en": ("Each archetype is one position in the nine-"
             "dimensional posture space. The application shows you the NEAREST one, "
             "together with the distance to it — it does not sort you into it.")}),
    ({"en": "Distance matters"},
     {"en": ("A small distance means the archetype describes you "
             "well; a large one means you sit between several, which is common and "
             "perfectly normal.")}),
    ({"en": "Not a personality test"},
     {"en": ("The instrument measures positions on nine "
             "tensions about technology. It says nothing about who you are, and it "
             "predicts nothing about what you will do.")}),
    ({"en": "Same engine for the figures"},
     {"en": ("The historical figures of the study are "
             "scored by exactly this mechanism, which is why the results page can put "
             "the room next to one of them.")}),
    ({"en": "Names"},
     {"en": ("Read from the shared studio manifest, the same source the "
             "survey application uses — the names on this slide and in the app can "
             "never drift apart.")}),
]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(T(h, lang), T(d, lang)) for h, d in _TIP],
                )
        st_space("v", s.project.spacing.title_gap)
        st_write(bs.lead, *TF(_LEAD, lang), tag=t.div)
        # Un franc espace avant les six noms (NG 2026-08-03) : ils sont le sujet
        # de la slide, et une grille collée à sa phrase d'introduction se lit
        # comme une légende.
        st_space("v", "6vh")
        # ONE flat grid — six named cards, wrapping on a narrow window.
        with st_grid(cols=s.project.grids.balanced(len(_CARDS)), gap="1.2vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for (_key, name), card in zip(archetypes(), _CARDS):
                with g.cell(), st_block(card):
                    st_write(bs.name, name, tag=t.div)
