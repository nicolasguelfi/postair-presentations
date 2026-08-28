"""The room's own results — relay slide to the sumvadis presentation page.

Same operator motif as the live-monitoring and results slides: one big button
per day opens ``/present/<code>`` in a new tab. The deck cannot read the live
distribution itself, so the projection is a deliberate stage gesture.

SPEAKER NOTES:
Ten minutes, the longest single moment of the sequence. Open the page of the
day and comment three things, in this order: the axis where the room is most
marked, the axis where it is most ambivalent, and the dominant archetype.
Then compare the room with a great historical figure — it always gets a
laugh, and it plants the debate that follows. Keep the per-question detail
open at the end: it is where the divisive questions come from.
If the network fails, the rehearsal screenshots are the fallback; announce
them as such rather than pretending they are live.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from postair_data import mascot
from postair_event import DAYS, present_url
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.ai_mark import dd35_overlay


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    button = s.project.ds.buttons.action_amber
    mascot_name = s.project.body.mascot_name
    caption = s.project.body.caption + s.center_txt


bs = BlockStyles


def build(lang: str = "en", **_):
    st_marker("The room's results")
    medio = mascot("Medio")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                # Rétrogradé "+1" (ss12) : la partie 2 est ancrée par
                # bck_results_poster (« The Results »). Les captures de RÉGIE
                # et les 7 vues du diaporama /present (Q15) adossent cette
                # séquence régie + diaporama (bck_screens_regie et bck_screens_diapo_*), juste après.
                st_write(bs.title, "So — who ", (s.project.titles.keyword, "are we"), "?",
                         tag=t.div, toc_lvl="+1", label="The room's results")
            with g.cell():
                st_info_tooltip(
                    title="Driving the projection",
                    entries=[
                        ("Room radar", "The cohort's average profile on the nine axes, with "
                         "optional overlays: nearest archetype, nearest great figure."),
                        ("What to comment", "Three things, in this order: the most marked axis, "
                         "the most ambivalent axis, the dominant archetype. Resist the urge to "
                         "comment all nine — the room stops listening after three."),
                        ("Great figures", "The overlay places the room next to figures scored by "
                         "the same engine. It is a smile, not a verdict — say so."),
                        ("Per-question detail", "Expandable distribution for each statement. "
                         "This is where the debate questions come from: pick the ones where the "
                         "room splits, not the ones where it agrees."),
                        ("Refresh", "The page refreshes every four seconds and can export a room "
                         "report. It requires the operator key — the audience cannot open it."),
                        ("Fallback", "If the network fails, use the rehearsal screenshots and say "
                         "clearly that they are from the rehearsal, not from this room."),
                    ],
                )
        st_space("v", s.project.spacing.title_gap)
        with st_grid(cols="45% 55%", gap="1.5vw",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_image(s.project.cards.media_center, width="min(22vw, 46vh)",
                         uri=medio["image"],
                         alt=f"{medio['name']}, the moderator mascot, presenting the results",
                         overlay=dd35_overlay())
                st_write(bs.mascot_name, medio["name"], tag=t.div)
                st_write(bs.caption, "your answers, live", tag=t.div)
            with g.cell():
                for label, code in DAYS:
                    st_write(bs.button, f"Project the results · {label}",
                             tag=t.div, link=present_url(code), no_link_decor=True)
