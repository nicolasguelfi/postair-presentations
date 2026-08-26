"""Waves grid — from writing to the steam engine (the first six).

SPEAKER NOTES:
One breath per wave, never all six: point at the number, say the period, name
one figure. The full lines — substitution terms included — live in the
tooltip if someone asks.
"""
# @guideline: postair-minimal

from custom.render import waves_grid_slide


def build():
    waves_grid_slide("From writing to steam",
                     ("From writing to ", "steam", ""), first=1, last=6)
