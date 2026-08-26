"""Waves grid — from the railway to the atom (the middle six).

SPEAKER NOTES:
Same gesture as the previous grid: number, period, one figure per wave.
"""
# @guideline: postair-minimal

from custom.render import waves_grid_slide


def build():
    waves_grid_slide("From rail to the atom",
                     ("From rail to the ", "atom", ""), first=7, last=12)
