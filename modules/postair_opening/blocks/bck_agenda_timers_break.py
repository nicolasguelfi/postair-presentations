"""APPENDIX · Chronos pause — la pause (Break 15' puis Re-welcome 5'), en chaîne.

Bloc mince (demande NG 2026-09-01) : la mécanique et les feuilles vivent
dans ``custom/agenda_timers.py`` — l'entrée « 15'+5' » de l'agenda devient
deux compteurs nommés (règle de ``bck_break_countdown`` : jamais les
chiffres collés).

SPEAKER NOTES:
Presenter tool — the projected break screen stays bck_break_countdown in the
debates deck; this one is the control-screen version with pause and reset.
"""
# @guideline: postair-minimal

from custom.agenda_timers import build_timer_slide


def build(lang: str = "en", **_):
    build_timer_slide(1, lang)
