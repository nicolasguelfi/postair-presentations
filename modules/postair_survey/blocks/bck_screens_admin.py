"""The operator's screens — the régie (20-22) and the /present slideshow (23-29).

Backs the room's-results slides (decision Q15, NG 2026-08-14): when the
speaker opens ``/present`` for real, these captures are what the room is
about to see — and if the network fails, they are the honest fallback
(announced as captures, never passed off as live).

First sub-slide: the three régie pages side by side — admin console
(FR/EN only, DD-66, operator key), ``/live`` (read-only room counter, no
key), ``/present`` (aggregates, operator key) whose full page is one long
scroll. Then SEVEN sub-slides, one per real view of the ``/present``
full-screen slideshow — desktop captures, landscape layout (Q15 adapts the
Q14 mobile layout: capture full-stage on top, messages in a row below).

All captures are the REAL application, frozen from the sumvadis media
registry (``build_survey_captures.py``, facet capture-desktop-sombre, en).

SPEAKER NOTES:
This block is a rehearsal, not a talk: thirty seconds on the régie (who
holds the key, where the pause button lives), then walk the seven views in
order — one sentence each, the room will see them again live minutes later.
On 'what divides the room', slow down: that view is the menu of the
afternoon's debates.
"""
# @guideline: postair-minimal

from custom.captures import capture
from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    head = s.project.body.bullet + s.center_txt + s.bold
    detail = s.project.body.caption + s.center_txt
    caption = s.project.body.mascot_name + s.center_txt


bs = BlockStyles

#: Trois pages, trois géométries réelles : la console est quasi-portrait
#: (1976×2692), la vue salle est paysage (2008×1612) et la page /present est
#: UN LONG RUBAN (1976×9482, ratio 0,21) — montré tel quel, en pellicule :
#: illisible par construction, c'est le diaporama qui suit qui le découpe en
#: vues lisibles. Largeurs bornées par la hauteur commune (~44vh).
_REGIE = [
    ("20-admin-console", "min(18vw, 32vh)",
     "Desktop screen of the sumvadis admin console, dark theme",
     "the console — operator key · FR/EN",
     ("Pause first, diagnose after",
      "The console steers the campaigns — pause, resume, close, reopen per "
      "day. Any incident: pause, then think.")),
    ("21-admin-salle", "min(26vw, 55vh)",
     "Desktop screen of the /live room view: real-time answer counter, "
     "dark theme",
     "/live — the room counter, no key",
     ("Read-only, safe to open anywhere",
      "The live counter refreshes every two seconds and needs no key — "
      "project it while the room answers.")),
    ("22-admin-projection", "min(6vw, 9vh)",
     "Full-page capture of the /present aggregates page, one very long "
     "scroll, dark theme",
     "/present — one long scroll",
     ("The key, then the slideshow",
      "The aggregates page opens with the operator key. Nobody scrolls this "
      "in front of 1500 people: its full-screen slideshow follows, view by "
      "view.")),
]

#: Les sept vues RÉELLES du diaporama plein écran de /present, dans l'ordre
#: du visionneur (slugs 23-29 du registre — Q15). Une vue = une sous-slide.
_SLIDESHOW = [
    ("23-diapo-radar", "The room's radar",
     ["The room's ", (s.project.titles.keyword, "radar")],
     [("The average shape of the room",
       "Every answer in the room, averaged into one nine-axis profile."),
      ("What to comment",
       "The most marked axis, the most ambivalent axis, the dominant "
       "archetype — three things, then stop."),
      ]),
    ("24-diapo-etendue", "The room's spread",
     ["The room's ", (s.project.titles.keyword, "spread")],
     [("Beyond the average",
       "The interquartile band shows where the middle half of the room "
       "actually stands, axis by axis."),
      ("Narrow is agreement, wide is a debate",
       "Dispersion made visible — this view announces where the afternoon "
       "will be lively."),
      ]),
    ("25-diapo-details", "The detail per question",
     ["The ", (s.project.titles.keyword, "detail"), " per question"],
     [("Statement by statement",
       "The answer distribution of each of the 54 statements."),
      ("Where the debate questions come from",
       "Pick the statements where the room splits, not the ones where it "
       "agrees."),
      ]),
    ("26-diapo-gaufre", "The archetype waffle",
     ["The archetype ", (s.project.titles.keyword, "waffle")],
     [("Each dot is one of you",
       "Every anonymous answer takes its place in an archetype — the room, "
       "person by person, name by nobody."),
      ("Six archetypes at a glance",
       "The distribution of the six archetypes across the room, in one "
       "figure."),
      ]),
    ("27-diapo-divisions", "What divides the room",
     ["What ", (s.project.titles.keyword, "divides"), " the room"],
     [("The most divisive statements",
       "Ranked by how strongly the room splits on them."),
      ("The menu of the debates",
       "This view IS the shortlist: the afternoon's arguments start from "
       "these lines."),
      ]),
    ("28-diapo-abstentions", "Where the room abstains",
     ["Where the room ", (s.project.titles.keyword, "abstains")],
     [("The 'no opinion' map",
       "Where the room chose not to answer — counted apart, never as a "
       "middle answer."),
      ("An abstention is information",
       "It names the questions this room does not yet feel equipped to "
       "answer — worth one comment, not a judgement."),
      ]),
    ("29-diapo-groupes", "The group comparison",
     ["The ", (s.project.titles.keyword, "group"), " comparison"],
     [("Groups, side by side",
       "The same aggregates split by group, when the campaign defines "
       "groups."),
      ("Absence is normal here",
       "A room without declared groups shows no comparison — the section "
       "stays away cleanly, it is not a failure."),
      ]),
]


def build():
    st_marker("The operator's screens")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "The ", (s.project.titles.keyword, "operator's"),
                         " screens", tag=t.div, toc_lvl="+1",
                         label="The operator's screens")
            with g.cell():
                st_info_tooltip(
                    title="The régie, in three pages",
                    entries=[
                        ("The console", "Campaign steering — pause / resume / close / "
                         "reopen per day. Operator key required; the console exists in "
                         "FR and EN only (DD-66)."),
                        ("/live", "The room counter, refreshed every two seconds. "
                         "Read-only, no key — the page projected while the room "
                         "answers."),
                        ("/present", "The room's aggregates, operator key required. "
                         "One long page — and a full-screen slideshow mode that the "
                         "next seven sub-slides walk through."),
                        ("If anything goes wrong", "First reflex: PAUSE the campaign "
                         "from the console, then diagnose. Resuming is instant."),
                    ],
                )
        st_space("v", "1vh")
        with st_grid(cols=s.project.grids.balanced(len(_REGIE)), gap="1.5vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_top) as g:
            for slug, width, alt, legend, (head, detail) in _REGIE:
                with g.cell():
                    st_image(s.project.cards.media_center, width=width,
                             uri=capture(slug, device="desktop"), alt=alt)
                    st_write(bs.caption, legend, tag=t.div)
                    st_space("v", "0.8vh")
                    with st_block(s.project.cards.blue):
                        st_write(bs.head, head, tag=t.div)
                        st_write(bs.detail, detail, tag=t.div)
    # ── Les sept vues du diaporama, une par sous-slide (Q15) ─────────
    for slug, marker, title_parts, messages in _SLIDESHOW:
        st_slide_break(marker_label=marker,
                       config=SlideBreakConfig(mode=SlideBreakMode.MARKER_ONLY))
        screen_slide(
            title_parts, slug,
            f"Desktop view of the /present full-screen slideshow: {marker}, "
            f"dark theme",
            messages, device="desktop", landscape=True)
