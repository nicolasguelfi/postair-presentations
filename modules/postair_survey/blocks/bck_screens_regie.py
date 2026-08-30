"""The operator's screens — la régie en trois pages (20, 21, 22), UNE scène.

Ex-première slide de bck_screens_admin (découpage « un écran = un bloc »,
NG 2026-08-23 — les 7 vues du diaporama /present vivent désormais dans
bck_screens_diapo_*). Cette slide reste UNE scène composée :
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
from postair_lang import T, TF
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
     {"en": "The console — operator key · FR/EN", "fr": "La console — clé opérateur · FR/EN"},
     ({"en": "Pause first, diagnose after", "fr": "Pause d'abord, diagnostic ensuite"},
      {"en": ("The console steers the campaigns — pause, resume, close, reopen per "
              "day. Any incident: pause, then think."), "fr": "La console pilote les campagnes — pause, reprise, clôture, réouverture par jour. Au moindre incident : pause, puis réflexion."})),
    ("21-admin-salle", "min(26vw, 55vh)",
     "Desktop screen of the /live room view: real-time answer counter, "
     "dark theme",
     {"en": "/live — the room counter, no key", "fr": "/live — compteur de la salle, sans clé"},
     ({"en": "Read-only, safe to open anywhere", "fr": "Lecture seule, sans risque, partout"},
      {"en": ("The live counter refreshes every two seconds and needs no key — "
              "project it while the room answers."), "fr": "Le compteur en direct se rafraîchit toutes les deux secondes, sans clé — projetez-le pendant que la salle répond."})),
    ("22-admin-projection", "min(6vw, 9vh)",
     "Full-page capture of the /present aggregates page, one very long "
     "scroll, dark theme",
     {"en": "/present — one long scroll", "fr": "/present — une seule longue page"},
     ({"en": "The key, then the slideshow", "fr": "La clé, puis le diaporama"},
      {"en": ("The aggregates page opens with the operator key. Nobody scrolls this "
              "in front of 1500 people: its full-screen slideshow follows, view by "
              "view."), "fr": "La page des agrégats s'ouvre avec la clé opérateur. On ne fait pas défiler ça devant 1500 personnes : son diaporama plein écran prend le relais, vue par vue."})),
]

_MARKER = {"en": "The operator's screens", "fr": "Les écrans de l'opérateur"}
_TITLE = {"en": ("The ", (s.project.titles.keyword, "operator's"), " screens"), "fr": ("L'", (s.project.titles.keyword, "opérateur"), " et ses écrans")}
_TIP_TITLE = {"en": "The régie, in three pages", "fr": "La régie, en trois pages"}
_TIP = [
    ({"en": "The console", "fr": "La console"},
     {"en": ("Campaign steering — pause / resume / close / "
             "reopen per day. Operator key required; the console exists in "
             "FR and EN only (DD-66)."), "fr": "Le pilotage des campagnes — pause / reprise / clôture / réouverture par jour. Clé opérateur requise ; la console n'existe qu'en FR et EN (DD-66)."}),
    ({"en": "/live", "fr": "/live"},
     {"en": ("The room counter, refreshed every two seconds. "
             "Read-only, no key — the page projected while the room "
             "answers."), "fr": "Le compteur de la salle, rafraîchi toutes les deux secondes. Lecture seule, sans clé — la page projetée pendant que la salle répond."}),
    ({"en": "/present", "fr": "/present"},
     {"en": ("The room's aggregates, operator key required. "
             "One long page — and a full-screen slideshow mode that the "
             "next slides walk through."), "fr": "Les agrégats de la salle, clé opérateur requise. Une longue page — et un mode diaporama plein écran, que les slides suivantes parcourent."}),
    ({"en": "If anything goes wrong", "fr": "En cas d'incident"},
     {"en": ("First reflex: PAUSE the campaign "
             "from the console, then diagnose. Resuming is instant."), "fr": "Premier réflexe : mettre la campagne en PAUSE depuis la console, puis diagnostiquer. La reprise est instantanée."}),
]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, *TF(_TITLE, lang), tag=t.div, toc_lvl="+1",
                         label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(T(h, lang), T(d, lang)) for h, d in _TIP],
                )
        st_space("v", "1vh")
        with st_grid(cols=s.project.grids.balanced(len(_REGIE)), gap="1.5vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_top) as g:
            for slug, width, alt, legend, (head, detail) in _REGIE:
                with g.cell():
                    st_image(s.project.cards.media_center, width=width,
                             uri=capture(slug, device="desktop", lang=lang), alt=alt)
                    st_write(bs.caption, T(legend, lang), tag=t.div)
                    st_space("v", "0.8vh")
                    with st_block(s.project.cards.blue):
                        st_write(bs.head, T(head, lang), tag=t.div)
                        st_write(bs.detail, T(detail, lang), tag=t.div)
