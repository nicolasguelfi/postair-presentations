"""Waves gallery — the seventeenth wave, alone and large.

Amendement NG (ligne ``design``, 2026-08-26) : the last gallery slide gives
the AI wave the whole screen — the same clickable object card, at slide
scale, eight figures listed below.

SPEAKER NOTES:
Land here and slow down: « this one is ours ». One click opens it.
"""
# @guideline: postair-minimal

from custom.render import wave_hero_grid_slide


def build(lang: str = "en", **_):
    wave_hero_grid_slide("The seventeenth wave", "ai")
