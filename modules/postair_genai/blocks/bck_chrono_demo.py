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
resets. Real decks call the widget with their own list. Each zero now rings —
bell on the chain, chime/gong across the parallel row, Discuss stays muted.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from postair_lang import T, TF
from postair_tuning import st_tuning
from shared_widgets import st_countdown_rack, st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    mode_line = s.project.body.caption + s.center_txt


bs = BlockStyles

#: La liste de durées de la DÉMO — une DONNÉE du bloc (courte à dessein,
#: sheets + surcharges par pas : héritage · mutisme « off » · gong 6 s plein
#: volume sur Vote). Un deck consommateur portera SA liste dans SON bloc.
_STEPS = [({"en": "Read", "fr": "Lire"}, 1),
          ({"en": "Discuss", "fr": "Discuter"}, 0.5, "off"),
          ({"en": "Vote", "fr": "Voter"}, 1,
           {"alarm": "gong", "volume": 1.0, "duration": 6})]

#: Les RÉGLAGES (chparam2, NG 2026-09-03) : DEFAULTS = le schéma sûr ; LOCAL
#: = la main de NG, pris au prochain rerun (les bck_* se rechargent à
#: chaud) ; étage json optionnel data/chrono-demo.json, relu à chaque
#: affichage. alarm_duration 6 s = retouche NG du jour, conservée. grid : le
#: temps 1 reste compact (3 → 2×2 avec un trou), le temps 2 force (1, 3).
DEFAULTS = {
    "alarm_chain": "bell",
    "alarm_parallel": "chime",
    "alarm_volume": 0.6,   # [0, 1] perceptif
    "alarm_duration": 6,   # secondes ]0, 60] — None = un motif (main NG)
    "grid_parallel": (1, 3),
    "rack_vh": 62,
    "scale": 1.0,
}
LOCAL = {}

_MARKER = {"en": "Chrono (demo)", "fr": "Chrono (démo)"}
_TITLE = {"en": ("Countdown rack — ", (s.project.titles.keyword, "chain")), "fr": ("Comptes à rebours — ", (s.project.titles.keyword, "chaîne"))}
_TITLE_PAR = {"en": ("Countdown rack — ", (s.project.titles.keyword, "parallel")), "fr": ("Comptes à rebours — ", (s.project.titles.keyword, "parallèle"))}
_LINE_CHAIN = {"en": "one card runs at a time · each zero launches the next · ▶ ⏸ ↺ per card", "fr": "une seule carte court à la fois · chaque zéro lance la suivante · ▶ ⏸ ↺ par carte"}
_LINE_PAR = {"en": "independent cards · ▶ Start launches ALL · ▶ ⏸ ↺ per card", "fr": "cartes indépendantes · ▶ Start les lance TOUTES · ▶ ⏸ ↺ par carte"}

_TIP_TITLE = {"en": "The widget, precisely", "fr": "Le widget, précisément"}
_TOOLTIP = [
    ({"en": "Generic", "fr": "Générique"},
     {"en": ("st_countdown_rack(s, steps, mode, key=…, grid=(rows, cols)) in "
             "shared_widgets — steps is a list of (label, minutes), fractions "
             "allowed (0.5 = 30 s). grid fixes the N×P geometry (cards fill "
             "left-to-right, top-to-bottom, holes allowed); omitted = the "
             "smallest compact grid with the biggest cells. Everything "
             "resizes to the cell."), "fr": "st_countdown_rack(s, steps, mode, key=…, grid=(rows, cols)) dans shared_widgets — steps est une liste de (libellé, minutes), fractions permises (0,5 = 30 s). grid fixe la géométrie N×P (les cartes se placent de gauche à droite, de haut en bas, trous permis) ; omis = la plus petite grille compacte avec les plus grandes cellules. Tout se redimensionne à la cellule."}),
    ({"en": "Per-card buttons", "fr": "Boutons par carte"},
     {"en": ("▶ starts or resumes · ⏸ pauses · ↺ resets that counter to its "
             "full duration. In chain mode only ONE card runs at a time (▶ "
             "pauses the others) and a zero starts the next unfinished card; "
             "in parallel mode cards are independent."), "fr": "▶ démarre ou reprend · ⏸ met en pause · ↺ ramène ce compteur à sa durée pleine. En mode chaîne, UNE seule carte court à la fois (▶ met les autres en pause) et un zéro démarre la carte suivante non finie ; en mode parallèle, les cartes sont indépendantes."}),
    ({"en": "Global buttons", "fr": "Boutons globaux"},
     {"en": ("▶ Start launches the first unfinished card (chain) or all of "
             "them (parallel); ↺ Reset restores the whole row. Nothing runs "
             "before a click — the clock never counts during instructions."), "fr": "▶ Start lance la première carte non finie (chaîne) ou toutes (parallèle) ; ↺ Reset restaure la rangée entière. Rien ne court avant un clic — l’horloge ne compte jamais pendant les consignes."}),
    ({"en": "At zero", "fr": "À zéro"},
     {"en": ("The INITIAL duration in translucent red — same width as every "
             "other state, colour alone says « done », in both modes."), "fr": "La durée INITIALE en rouge translucide — même largeur que tous les autres états, la couleur seule dit « fini », dans les deux modes."}),
    #: Réinsérée le 2026-09-02 (planche auditj6, alarmlbl=p1 : libellé EN
    #: validé par NG) — elle était parquée hors du texte projeté en
    #: attendant cette validation, la baseline se regèle avec le lot.
    ({"en": "Alarm", "fr": "Alarme"},
     {"en": ("Optional sound at zero — silent by default. alarm= picks a "
             "WebAudio-synthesised timbre (bell, beep, chime, gong — no audio "
             "file, the room is offline), alarm_volume= sets the intensity "
             "(0–1, perceptual); a third element in a step overrides both for "
             "that card (« off » mutes it). Browsers unlock audio on a click "
             "only — any button of the rack arms it. Here: bell on the chain, "
             "chime on the parallel row, Discuss muted, Vote a full-volume "
             "gong, ringing for 6 seconds (alarm_duration= repeats the timbre's motif "
             "until the requested length — None plays it once). An alarmed rack "
             "starts MUTED: the 🔔 on each card arms IT, the global 🔔 arms them "
             "all (remembered, with a sound preview)."), "fr": "Son optionnel au zéro — silence par défaut. alarm= choisit un timbre synthétisé en WebAudio (cloche, bip, carillon, gong — aucun fichier audio, la salle est hors réseau), alarm_volume= règle l’intensité (0–1, perceptive) ; un troisième élément d’un pas surcharge les deux pour cette carte (« off » la rend muette). Le navigateur ne débloque le son qu’au clic — n’importe quel bouton du rack l’arme. Ici : cloche sur la chaîne, carillon sur la rangée parallèle, Discuter muette, Voter en gong plein volume pendant 6 secondes (alarm_duration= répète le motif du timbre jusqu'à la durée demandée — None le joue une fois). Un rack alarmé démarre EN SOURDINE : la cloche 🔔 de chaque carte l'arme, la globale les arme toutes (mémorisé, avec un aperçu sonore)."}),
    ({"en": "To relocate", "fr": "À déménager"},
     {"en": ("This demo lives in the genai backup annex only while the "
             "consumer deck is unnamed — moving it is one thin block in that "
             "deck plus one book line."), "fr": "Cette démo ne vit dans l’annexe backup de genai que tant que le deck consommateur n’est pas nommé — la déplacer, c’est un bloc mince dans ce deck plus une ligne de book."}),
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
    # La résolution i18n ne touche que l'étiquette : le 3e élément éventuel
    # d'un pas est de la CONFIG d'alarme, pas du texte projeté — il traverse.
    TUNING = st_tuning(DEFAULTS, local=LOCAL, json_path="data/chrono-demo.json")
    steps = [(T(step[0], lang), *step[1:]) for step in _STEPS]
    # ── Temps 1 : le mode chaîne ────────────────────────────────────────────
    # `key` unique par rangée — l'export inline les deux temps dans le même
    # document, deux rangées sans clé partageraient leur bus.
    with st_block(s.project.containers.page_fill_top):
        _header(_TITLE, _LINE_CHAIN, lang)
        # Grille compacte par défaut : 3 compteurs → 2×2 avec un trou.
        st_countdown_rack(s, steps, mode="chain", key="genai-demo-chain",
                          rack_vh=TUNING["rack_vh"], scale=TUNING["scale"],
                          alarm=TUNING["alarm_chain"],
                          alarm_volume=TUNING["alarm_volume"],
                          alarm_duration=TUNING["alarm_duration"])
    st_slide_break(marker_hidden=True)
    # ── Temps 2 : le mode parallèle, en rangée forcée (1, 3) ────────────────
    with st_block(s.project.containers.page_fill_top):
        _header(_TITLE_PAR, _LINE_PAR, lang)
        st_countdown_rack(s, steps, mode="parallel", key="genai-demo-parallel",
                          grid=TUNING["grid_parallel"],
                          rack_vh=TUNING["rack_vh"], scale=TUNING["scale"],
                          alarm=TUNING["alarm_parallel"],
                          alarm_volume=TUNING["alarm_volume"],
                          alarm_duration=TUNING["alarm_duration"])
