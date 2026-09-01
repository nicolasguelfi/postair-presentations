"""APPENDIX · Chronos après-pause — les séances d'APRÈS la pause, en chaîne.

Bloc mince (demande NG 2026-09-01) : la mécanique et les feuilles vivent
dans ``custom/agenda_timers.py`` — data-driven depuis
``postair_event.AGENDA``, mode chaîne, boutons ▶ ⏸ ↺ par carte.

SPEAKER NOTES:
Presenter tool — jump here from the sidebar when the second half starts,
click ▶ Start. See custom/agenda_timers.py for the full notes.
"""
# @guideline: postair-minimal

from custom.agenda_timers import build_timer_slide


def build(lang: str = "en", **_):
    build_timer_slide(2, lang)
