"""Waves gallery — the seventeenth wave, alone and large.

Amendement NG (ligne ``design``, 2026-08-26) : the last gallery slide gives
the AI wave the whole screen — the same clickable object card, at slide
scale, eight figures listed below.

SPEAKER NOTES:
Land here and slow down: « this one is ours ». One click opens it.
"""
# @guideline: postair-minimal

from custom.render import wave_hero_grid_slide
from custom.styles import Styles as s

_MARKER = {"en": "The seventeenth wave"}
_TITLE = {"en": ("The seventeenth ", (s.project.titles.keyword, "wave"))}


def build(lang: str = "en", **_):
    wave_hero_grid_slide(_MARKER, _TITLE, "ai", lang=lang)
