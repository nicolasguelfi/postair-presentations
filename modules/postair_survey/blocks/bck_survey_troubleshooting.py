"""Before you start — the six things that go wrong, and what to do about them.

The last slide before the room takes out fifteen hundred phones. Everything on
it was chosen for one reason: it is a problem the speaker would otherwise have
to answer fifteen hundred times, from a stage, over the noise of a full
amphitheatre. Answering it once, on screen, in advance, is the only version
that scales.

Two of them are the ones that actually happen at this scale. Fifteen hundred
devices on one venue access point is a load no campus wifi is dimensioned for,
so the room is told to switch to mobile data BEFORE it becomes a queue at the
front. And people finish at very different speeds — twenty minutes apart from
first to last — so the ones who finish early are given something to read rather
than a neighbour to talk to.

SPEAKER NOTES:
Ninety seconds, brisk, and do not dramatise any of it. Read the first two out
loud — the wifi one and the finished-early one — and let the room read the rest.
Say plainly that nothing here is an emergency: the survey saves as you go, so
the worst case is picking it back up. Then stop talking and go to the join
slide: this room is ready, and the only thing left to do is start.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from postair_i18n import ui
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

#: (situation, ce qu'on fait, carte, accent du titre). Ordonnés par probabilité
#: décroissante : les deux premiers arrivent à coup sûr avec quinze cents
#: personnes dans la salle. Un accent DIFFÉRENT par titre (NG 2026-08-15) :
#: six situations, six couleurs — l'œil retrouve sa carte depuis le fond.
_TIPS = [
    ({"en": "QR won't scan?"}, {"en": "Type the address and the code by hand"},
     s.project.cards.blue, s.project.colors.primary),
    ({"en": "Wifi struggling?"}, {"en": "wifi OFF → mobile data"},
     s.project.cards.amber, s.project.colors.amber),
    ({"en": "Finished early?"}, {"en": "Read the six archetype descriptions"},
     s.project.cards.teal, s.project.colors.keyword),
    ({"en": "Lost the page?"}, {"en": "Reopen it — your answers are saved"},
     s.project.cards.blue, s.project.colors.success),
    ({"en": "Battery low?"}, {"en": "Pair up with a neighbour and share one"},
     s.project.cards.coral, s.project.colors.critical),
    ({"en": "Something else?"}, {"en": "raise a hand → we come to you"},
     s.project.cards.coral, s.project.colors.coral),
]

_MARKER = {"en": "Before you start"}
_TITLE = {"en": ("If something ", (s.project.titles.keyword, "goes wrong"))}
_LEAD = {"en": ("Nothing here is serious — ",
                (s.project.titles.keyword, "your answers are saved as you go"))}
#: Le titre du tooltip (« Operator checklist ») vient du lexique.
_TIP = [
    ({"en": "The wifi will struggle"},
     {"en": ("Fifteen hundred devices on one venue access "
             "point is beyond what campus wifi is dimensioned for. Say it before it "
             "happens, not after: mobile data works, and the survey is a few hundred "
             "kilobytes, not a video.")}),
    ({"en": "Nothing is lost"},
     {"en": ("Answers are stored on the device as they are given. "
             "Closing the page, losing the network or running out of battery costs "
             "the current statement at worst — reopening the same link resumes.")}),
    ({"en": "Nothing to install"},
     {"en": ("It runs in the browser. Anyone being sent to an "
             "app store is on the wrong address.")}),
    ({"en": "The spread is twenty minutes"},
     {"en": ("First and last finisher are far apart. "
             "Give the early ones the archetype descriptions to read — an idle "
             "amphitheatre becomes a loud one within two minutes.")}),
    ({"en": "Sharing a device"},
     {"en": ("One answer per person, in turn. Two people "
             "answering as one produce a profile that describes nobody.")}),
    ({"en": "If it goes badly wrong"},
     {"en": ("Pause the campaign from the admin console "
             "first, diagnose after. Resuming is instant, and a paused campaign "
             "loses nothing.")}),
]


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    lead = s.project.body.bullet + s.center_txt
    case = s.project.body.body + s.center_txt + s.bold
    fix = s.project.body.body + s.center_txt


bs = BlockStyles


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                with st_zoom(130):
                    st_write(bs.title, *TF(_TITLE, lang),
                            tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=ui("operator_checklist", lang),
                    entries=[(T(h, lang), T(d, lang)) for h, d in _TIP],
                )
        st_space("v", "2vh")
        st_write(bs.lead, *TF(_LEAD, lang), tag=t.div)
        st_space("v", "2.5vh")
        # ONE flat grid, laid out as a block rather than a strip.
        with st_grid(cols=s.project.grids.balanced(len(_TIPS)), gap="1.2vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for case, fix, card, accent in _TIPS:
                with g.cell(), st_block(card):
                    with st_zoom(120):
                        st_write(bs.case + accent, T(case, lang), tag=t.div)
                        st_space("v", "0.8vh")
                        st_write(bs.fix, T(fix, lang), tag=t.div)
