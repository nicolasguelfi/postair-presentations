"""BACKUP · Chrono — la DÉMO du widget ``st_countdown_rack`` (à déplacer).

Slide de démonstration (planche chrono, NG 2026-09-01 : ``archi=p1
moteur=p1 commande=p1 habillage=p1``) — placée dans l'annexe BACKUP de genai
UNIQUEMENT parce que c'est le deck en cours d'itération (rechargeable à
chaud) et que l'annexe n'est jamais présentée : le deck consommateur réel
n'est pas encore nommé. Quand il le sera, ce bloc déménage (un bloc mince
par deck, la liste des durées dans son TUNING) et cette démo disparaît d'ici.

Deux temps cachés (pattern debates), un par mode. Retouches NG 2026-09-01 :
chaque carte porte SES boutons ▶ ⏸ ↺ (chain : une seule carte court, le zéro
lance la suivante non finie ; parallel : cartes indépendantes), les cartes
sont de VRAIS ``st_block(cards.blue)`` sur ``st_grid``, et le zéro s'affiche
en durée initiale rouge translucide (sans coche — ``chronocheck zero=p1``,
2026-09-02 : la couleur seule porte l'accompli). Les boutons
globaux (▶ Start / ↺ Reset) restent au-dessus de la grille. Durées COURTES à
dessein (1' / 0,5' / 1') : la démo se joue en une minute.

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
    # Le temps 1 laisse la grille COMPACTE par défaut (3 → 2×2 avec un trou,
    # spécification NG 2026-09-02 : remplissage gauche→droite, haut→bas) ;
    # le temps 2 force la rangée (1, 3) — la démo montre les deux régimes.
    # Trio de leviers (chronoh leviers=p1) : grid · rack_vh (place verticale
    # totale, % de fenêtre) · scale (zoom fin du contenu).
    "grid_parallel": (1, 3),
    "rack_vh": 62,
    "scale": 1.0,
}

_MARKER = {"en": "Chrono (demo)"}
_TITLE = {"en": ("Countdown rack — ", (s.project.titles.keyword, "chain"))}
_TITLE_PAR = {"en": ("Countdown rack — ", (s.project.titles.keyword, "parallel"))}
_LINE_CHAIN = {"en": "one card runs at a time · each zero launches the next · ▶ ⏸ ↺ per card"}
_LINE_PAR = {"en": "independent cards · ▶ Start launches ALL · ▶ ⏸ ↺ per card"}

_TIP_TITLE = {"en": "The widget, precisely"}
_TOOLTIP = [
    ({"en": "Generic"},
     {"en": ("st_countdown_rack(s, steps, mode, key=…, grid=(rows, cols)) in "
             "shared_widgets — steps is a list of (label, minutes), fractions "
             "allowed (0.5 = 30 s). grid fixes the N×P geometry (cards fill "
             "left-to-right, top-to-bottom, holes allowed); omitted = the "
             "smallest compact grid with the biggest cells. Everything "
             "resizes to the cell.")}),
    ({"en": "Per-card buttons"},
     {"en": ("▶ starts or resumes · ⏸ pauses · ↺ resets that counter to its "
             "full duration. In chain mode only ONE card runs at a time (▶ "
             "pauses the others) and a zero starts the next unfinished card; "
             "in parallel mode cards are independent.")}),
    ({"en": "Global buttons"},
     {"en": ("▶ Start launches the first unfinished card (chain) or all of "
             "them (parallel); ↺ Reset restores the whole row. Nothing runs "
             "before a click — the clock never counts during instructions.")}),
    ({"en": "At zero"},
     {"en": ("The INITIAL duration in translucent red — same width as every "
             "other state, colour alone says « done », in both modes.")}),
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
    # `key` unique par rangée — l'export inline les deux temps dans le même
    # document, deux rangées sans clé partageraient leur bus.
    with st_block(s.project.containers.page_fill_top):
        _header(_TITLE, _LINE_CHAIN, lang)
        # Grille compacte par défaut : 3 compteurs → 2×2 avec un trou.
        st_countdown_rack(s, steps, mode="chain", key="genai-demo-chain",
                          rack_vh=TUNING["rack_vh"], scale=TUNING["scale"])
    st_slide_break(marker_hidden=True)
    # ── Temps 2 : le mode parallèle, en rangée forcée (1, 3) ────────────────
    with st_block(s.project.containers.page_fill_top):
        _header(_TITLE_PAR, _LINE_PAR, lang)
        st_countdown_rack(s, steps, mode="parallel", key="genai-demo-parallel",
                          grid=TUNING["grid_parallel"],
                          rack_vh=TUNING["rack_vh"], scale=TUNING["scale"])
