"""BACKUP · Chrono — la DÉMO du widget ``st_countdown_rack`` (à déplacer).

Slide de démonstration (planche chrono, NG 2026-09-01 : ``archi=p1
moteur=p1 commande=p1 habillage=p1``) — placée dans l'annexe BACKUP de genai
UNIQUEMENT parce que c'est le deck en cours d'itération (rechargeable à
chaud) et que l'annexe n'est jamais présentée : le deck consommateur réel
n'est pas encore nommé. Quand il le sera, ce bloc déménage (un bloc mince
par deck, la liste des durées dans son TUNING) et cette démo disparaît d'ici.

Deux temps cachés (pattern debates), un par mode :

1. **chain** — le clic Start lance « Read » ; chaque zéro lance le suivant
   (Discuss, puis Vote) ; les cartes finies passent au ✓ teal, les heures de
   fin murales sont CUMULÉES ;
2. **parallel** — le même clic lance les trois ensemble ; à zéro, corail
   (le vocabulaire du chrono de pause).

Le ↺ en coin remet la rangée à zéro (faux départ, répétition). Durées
COURTES à dessein (1' / 0,5' / 1') : la démo se joue en une minute.

SPEAKER NOTES:
Never presented — a widget demo. Click Start, watch the chain hand over at
each zero; PageDown, click Start again, watch the three run together. The ↺
resets. Real decks call the widget with their own list.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from postair_lang import T, TF
from shared_widgets import st_countdown_rack, st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    mode_line = s.project.body.caption + s.center_txt


bs = BlockStyles

#: Réglages datés (2026-09-01) : la liste de durées de la DÉMO — courte à
#: dessein. Un deck consommateur portera SA liste dans SON bloc.
TUNING = {
    "steps": [({"en": "Read"}, 1), ({"en": "Discuss"}, 0.5), ({"en": "Vote"}, 1)],
    "height": 460,
    "scale": 1.0,
}

_MARKER = {"en": "Chrono (demo)"}
_TITLE = {"en": ("Countdown rack — ", (s.project.titles.keyword, "chain"))}
_TITLE_PAR = {"en": ("Countdown rack — ", (s.project.titles.keyword, "parallel"))}
_LINE_CHAIN = {"en": "Start launches the first · each zero launches the next"}
_LINE_PAR = {"en": "Start launches ALL · coral at zero"}

_TIP_TITLE = {"en": "The widget, precisely"}
_TOOLTIP = [
    ({"en": "Generic"},
     {"en": ("st_countdown_rack(steps, mode) in shared_widgets — steps is a "
             "list of (label, minutes), fractions allowed (0.5 = 30 s). Any "
             "deck can call it with its own list.")}),
    ({"en": "Two modes"},
     {"en": ("« chain »: each zero starts the next counter; « parallel »: one "
             "click starts them all. Same Start button in both.")}),
    ({"en": "On stage"},
     {"en": ("The clock never runs while you give the instructions — nothing "
             "starts before the click; the ↺ corner button recovers a false "
             "start. Wall-clock end times are shown per counter (cumulative "
             "in chain mode).")}),
    ({"en": "To relocate"},
     {"en": ("This demo lives in the genai backup annex only while the "
             "consumer deck is unnamed — moving it is one thin block in that "
             "deck plus one book line.")}),
]


def _header(title_sheet, line_sheet, lang: str) -> None:
    with st_grid(cols="92% 8%",
                 cell_styles=s.project.containers.grid_cell_centered) as g:
        with g.cell():
            st_write(bs.title, *TF(title_sheet, lang),
                     tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
        with g.cell():
            st_info_tooltip(
                title=T(_TIP_TITLE, lang),
                entries=[(T(h, lang), T(d, lang)) for h, d in _TOOLTIP],
            )
    st_write(bs.mode_line, T(line_sheet, lang), tag=t.div)
    st_space("v", "2vh")


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    steps = [(T(label, lang), minutes) for label, minutes in TUNING["steps"]]
    # ── Temps 1 : le mode chaîne ────────────────────────────────────────────
    with st_block(s.project.containers.page_fill_top):
        _header(_TITLE, _LINE_CHAIN, lang)
        st_countdown_rack(steps, mode="chain",
                          height=TUNING["height"], scale=TUNING["scale"])
    st_slide_break(marker_hidden=True)
    # ── Temps 2 : le mode parallèle ─────────────────────────────────────────
    with st_block(s.project.containers.page_fill_top):
        _header(_TITLE_PAR, _LINE_PAR, lang)
        st_countdown_rack(steps, mode="parallel",
                          height=TUNING["height"], scale=TUNING["scale"])
