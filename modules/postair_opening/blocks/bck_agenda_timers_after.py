"""APPENDIX · Chronos après-pause — bloc mince, LA CONFIG VIT ICI.

La mécanique et les feuilles vivent dans ``custom/agenda_timers.py``
(data-driven depuis ``postair_event.AGENDA``, mode chaîne, ▶ ⏸ ↺ par carte).
Les RÉGLAGES, eux, vivent dans CE bloc (chparam2, amendement o1 NG
2026-09-03) : DEFAULTS = le schéma sûr ; LOCAL = ta main (pris au PROCHAIN
RERUN — les bck_* se rechargent à chaud, sans tuer les processus) ; l'étage
JSON optionnel ``timers-part2.json`` (static/data/, absent = silence) se relit à
chaque affichage — l'édition de répétition/séance.

SPEAKER NOTES:
Presenter tool — jump here from the sidebar, click ▶ Start. See
custom/agenda_timers.py for the full notes.
"""
# @guideline: postair-minimal

from custom.agenda_timers import build_timer_slide
from postair_tuning import st_tuning

#: Le SCHÉMA et les valeurs sûres de CETTE slide (clés et types attendus).
DEFAULTS = {
    "grid": None,            # None = grille compacte ; (rows, cols) sinon
    "rack_vh": 62,           # place verticale totale, % de fenêtre
    "scale": 1.0,            # zoom fin du contenu des cellules
    "alarm": "bell",         # bell · beep · chime · gong · "off"
    "alarm_volume": 0.6,     # [0, 1] perceptif
    "alarm_duration": None,  # secondes ]0, 60] — None = un motif
}

#: La main de NG — surcharges de CETTE slide (éditables à chaud, rerun).
LOCAL = {}


def build(lang: str = "en", **_):
    build_timer_slide(2, lang,
                      tuning=st_tuning(DEFAULTS, local=LOCAL,
                                       json_path="data/timers-part2.json"))
