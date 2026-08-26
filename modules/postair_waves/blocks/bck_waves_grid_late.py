"""Waves grid — from computing to artificial intelligence (the last five).

The seventeenth cell is the studied wave: its questionnaire applies verbatim,
no substitution — the tooltip says so.

SPEAKER NOTES:
Land on the last cell and stay there: « this one is ours ». It is the pivot
toward the chronological walk that follows.
"""
# @guideline: postair-minimal

from custom.render import waves_grid_slide


def build():
    waves_grid_slide("From computing to AI",
                     ("From computing to ", "AI", ""), first=13, last=17)
