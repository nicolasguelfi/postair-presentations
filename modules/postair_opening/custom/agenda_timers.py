"""Agenda timers — la mécanique commune des trois slides de chronos.

Demande NG (2026-09-01, après la planche chrono) : trois slides, une par
colonne de la slide agenda — avant la pause, la pause, après la pause —
chacune portant les compteurs de ses séances via ``st_countdown_rack``
(mode chaîne : les séances s'enchaînent, chaque zéro lance la suivante ;
boutons ▶ ⏸ ↺ par carte, ▶ Start / ↺ Reset globaux).

Convention du dépôt : UN bloc = UN marqueur (un ``st_slide_break`` nu entre
deux slides d'un même bloc crée un marqueur anonyme parasite — constaté à la
porte i18n le 2026-09-01). La mécanique vit donc ICI, et trois blocs minces
(``bck_agenda_timers_part1/_break/_part2``) appellent ``build_timer_slide``.

Data-driven comme la slide agenda : les ensembles se LISENT dans
``postair_event.AGENDA`` (même découpage que ``bck_welcome_agenda._columns``
— la pause est l'entrée de ``kind == "break"``), jamais recopiés à la main.
Déplacer une séance dans ``postair_event.py`` et les trois slides suivent.
L'entrée « 15'+5' » de la pause devient DEUX compteurs (Break 15, Re-welcome
5 — la règle de ``bck_break_countdown`` : jamais les chiffres collés).

Placées en zone APPENDIX (après « Next deck », avant References) : des
outils d'orateur, atteints en deux secondes par la barre latérale, jamais
traversés par le fil répété de la séance. Les remonter dans le fil est une
ligne de book si NG le préfère.

SPEAKER NOTES:
Presenter tools, never part of the rehearsed flow. Jump here from the
sidebar when a half starts, click ▶ Start, and leave the tab visible on the
control screen if you want the running clock — the room screen stays on the
deck. Each card can be paused or reset alone (a session that overruns is a
⏸, not a drama).
"""
# @guideline: postair-minimal

import re

from custom.styles import Styles as s
from postair_event import AGENDA
from postair_lang import T, TF
from shared_widgets import st_countdown_rack, st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt


bs = BlockStyles

#: Réglages datés (2026-09-02, trio chronoh leviers=p1) : ``grid=None`` =
#: grille compacte du widget (4 séances → 2×2, la pause → 1×2) — forcer
#: ``(1, 4)`` pour la rangée linéaire ; ``rack_vh`` = la place verticale
#: TOTALE de la matrice en % de fenêtre (le levier proportionnel) ;
#: ``scale`` = zoom fin du contenu des cellules.
#: alarm/alarm_volume : cloche de fin (QCM NG 2026-09-03) — les racks
#: démarrent EN SOURDINE (défaut du widget), NG arme celui qu'il veut par
#: la cloche 🔔 à côté des boutons globaux (choix mémorisé par rack).
TUNING = {"grid": None, "rack_vh": 62, "scale": 1.0,
          "alarm": "bell", "alarm_volume": 1.0,
          "alarm_duration": 6}  # secondes ]0,60] — None = un motif

# ── Les feuilles {en, fr} du bloc (opening est bilingue) ────────────────────
_MARKERS = [
    {"en": "Timers · part 1", "fr": "Chronos · partie 1"},
    {"en": "Timers · break", "fr": "Chronos · pause"},
    {"en": "Timers · part 2", "fr": "Chronos · partie 2"},
]
_TITLES = [
    {"en": ("Part 1 — ", (s.project.titles.keyword, "before the break")),
     "fr": ("Partie 1 — ", (s.project.titles.keyword, "avant la pause"))},
    {"en": ((s.project.titles.keyword, "The break"),),
     "fr": ((s.project.titles.keyword, "La pause"),)},
    {"en": ("Part 2 — ", (s.project.titles.keyword, "after the break")),
     "fr": ("Partie 2 — ", (s.project.titles.keyword, "après la pause"))},
]
#: Les deux temps de l'entrée « 15'+5' » de l'agenda (bck_break_countdown :
#: quinze minutes de pause, cinq de re-accueil).
_BREAK_LABELS = [{"en": "Break", "fr": "Pause"},
                 {"en": "Re-welcome", "fr": "Re-accueil"}]
#: L'horloge murale en TÊTE de chaque rangée (NG 2026-09-04, chronotypes) :
#: type "clock" sans cible — carte LIBRE, toujours vivante, jamais une porte
#: de la chaîne ; la ville (Luxembourg) s'affiche d'elle-même dans le pied.
_CLOCK_LABEL = {"en": "Now", "fr": "Maintenant"}
_CLOCK_STEP = {"type": "clock", "tz": "Europe/Luxembourg"}

_TIP_TITLE = {"en": "How these timers work", "fr": "Comment marchent ces chronos"}
_TIP = [
    ({"en": "Chain mode", "fr": "Mode chaîne"},
     {"en": ("▶ Start launches the first session; each zero launches the next. "
             "One card runs at a time."),
      "fr": ("▶ Start lance la première séance ; chaque zéro lance la "
             "suivante. Une seule carte court à la fois.")}),
    ({"en": "Per-card buttons", "fr": "Boutons par carte"},
     {"en": ("▶ starts or resumes · ⏸ pauses (an overrun is a pause, not a "
             "drama) · ↺ resets that card to its full duration."),
      "fr": ("▶ démarre ou reprend · ⏸ met en pause (un dépassement est une "
             "pause, pas un drame) · ↺ remet la carte à sa durée pleine.")}),
    ({"en": "Data-driven", "fr": "Piloté par les données"},
     {"en": ("Sessions and durations come from the agenda "
             "(postair_event.AGENDA) — change the programme there and these "
             "three slides follow."),
      "fr": ("Séances et durées viennent de l'agenda (postair_event.AGENDA) — "
             "changez le programme là-bas et ces trois slides suivent.")}),
    ({"en": "The clock", "fr": "L'horloge"},
     {"en": ("The first card is the wall clock (Europe/Luxembourg) — always "
             "running, never a step of the chain."),
      "fr": ("La première carte est l'horloge murale (Europe/Luxembourg) — "
             "toujours vivante, jamais une étape de la chaîne.")}),
    ({"en": "Local only", "fr": "Local seulement"},
     {"en": ("Everything runs in THIS browser: no server state, no effect on "
             "any other computer showing the deck."),
      "fr": ("Tout tourne dans CE navigateur : aucun état serveur, aucun "
             "effet sur un autre ordinateur affichant le deck.")}),
]


def _sets(lang: str):
    """Les trois ensembles ``[(étiquette, minutes), …]``, lus de l'AGENDA.

    Même découpage que la slide agenda (la pause = ``kind == "break"``) ;
    une séance prend sa PREMIÈRE durée, la pause éclate « 15'+5' » en deux
    compteurs nommés.
    """
    kinds = [kind for _s, _d, kind in AGENDA]
    pause = kinds.index("break")
    before, brk, after = AGENDA[:pause], AGENDA[pause], AGENDA[pause + 1:]

    def first_minutes(duration: str) -> int:
        found = re.search(r"\d+", duration)
        if not found:
            raise ValueError(f"durée illisible dans l'agenda : {duration!r}")
        return int(found.group())

    break_minutes = [int(m) for m in re.findall(r"\d+", brk[1])]
    if len(break_minutes) != len(_BREAK_LABELS):
        raise ValueError(
            f"l'entrée pause {brk[1]!r} porte {len(break_minutes)} durée(s), "
            f"{len(_BREAK_LABELS)} étiquette(s) déclarées — les accorder ici")
    clock = (T(_CLOCK_LABEL, lang), None, dict(_CLOCK_STEP))
    return [
        [clock] + [(session, first_minutes(duration))
                   for session, duration, _k in before],
        [clock] + [(T(label, lang), m)
                   for label, m in zip(_BREAK_LABELS, break_minutes)],
        [clock] + [(session, first_minutes(duration))
                   for session, duration, _k in after],
    ]


_KEYS = ["opening-timers-p1", "opening-timers-break", "opening-timers-p2"]


def build_timer_slide(index: int, lang: str = "en",
                      tuning: dict | None = None) -> None:
    """La slide de chronos ``index`` (0 = avant-pause, 1 = pause, 2 = après).

    ``tuning`` : le dict RÉSOLU par le bloc appelant (``st_tuning`` —
    defaults/local du bloc + json optionnel). ``None`` = filet ``_FALLBACK``.
    """
    TUNING = tuning if tuning is not None else _FALLBACK
    steps = _sets(lang)[index]
    st_marker(T(_MARKERS[index], lang))
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, *TF(_TITLES[index], lang),
                         tag=t.div, toc_lvl="+1", label=T(_MARKERS[index], lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(T(h, lang), T(d, lang)) for h, d in _TIP],
                )
        st_space("v", s.project.spacing.title_gap)
        st_countdown_rack(s, steps, mode="chain", key=_KEYS[index],
                          grid=TUNING["grid"], rack_vh=TUNING["rack_vh"],
                          scale=TUNING["scale"],
                          alarm=TUNING["alarm"],
                          alarm_volume=TUNING["alarm_volume"],
                          alarm_duration=TUNING["alarm_duration"])
