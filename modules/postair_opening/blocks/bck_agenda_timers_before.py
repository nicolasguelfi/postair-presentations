"""APPENDIX · Chronos avant-pause — bloc mince, LA CONFIG VIT ICI.

La mécanique et les feuilles vivent dans ``custom/agenda_timers.py``
(data-driven depuis ``postair_event.AGENDA``, mode chaîne, ▶ ⏸ ↺ par carte).
Les RÉGLAGES, eux, vivent dans CE bloc (chparam2, amendement o1 NG
2026-09-03) : DEFAULTS = le schéma sûr ; LOCAL = ta main (pris au PROCHAIN
RERUN — les bck_* se rechargent à chaud, sans tuer les processus) ; l'étage
JSON optionnel ``timers-part1.json`` (static/data/, absent = silence) se relit à
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
    "grid": (2, 3),          # horloge en tête (NG 2026-09-04) — rangées × colonnes
    "rack_vh": 62,           # place verticale totale, % de fenêtre
    "scale": 1.0,            # zoom fin du contenu des cellules
    "alarm": "bell",         # bell · beep · chime · gong · "off"
    "alarm_volume": 1.,     # [0, 1] perceptif
    "alarm_duration": 6,  # secondes ]0, 60] — None = un motif
    "label_scale": 2.0,      # taille des noms de cartes (retour NG 2026-09-04)
    "ends_scale": 2.0,       # taille de « ends at HH:MM » sous les chiffres
    "digits_width": 80,      # largeur des chiffres, % de la cellule (100 = bord à bord)
    "clock_width": 100,      # idem pour L'HORLOGE seule — l'heure au plus grand
}

#: La main de NG — surcharges de CETTE slide (éditables à chaud, rerun).
LOCAL = {}


def build(lang: str = "en", **_):
    build_timer_slide(0, lang,
                      tuning=st_tuning(DEFAULTS, local=LOCAL,
                                       json_path="data/timers-part1.json"))
