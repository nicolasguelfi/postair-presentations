"""The operator's screens — la régie en trois pages (20, 21, 22), UNE scène.

Ex-première slide de bck_screens_admin (découpage « un écran = un bloc »,
NG 2026-08-23 — les 7 vues du diaporama /present vivent désormais dans
bck_screen_diapo_*). Cette slide reste UNE scène composée :
les trois pages de régie côte à côte, avec leurs géométries réelles — la
console quasi-portrait, la vue salle paysage, et /present en LONG RUBAN
(1976×9482) montré tel quel, en pellicule : illisible par construction,
c'est le diaporama qui suit qui le découpe en vues lisibles. La séparer
n'aurait pas de sens (le ruban seul ne dit rien).

SPEAKER NOTES:
Thirty seconds: who holds the operator key, where the pause button lives.
First reflex on any incident: PAUSE the campaign from the console, then
diagnose — resuming is instant.
"""
# @guideline: postair-minimal

from custom.captures import capture
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

#: Trois pages, trois géométries réelles — largeurs bornées par la hauteur
#: commune (~44vh).
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
                         "next slides walk through."),
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
