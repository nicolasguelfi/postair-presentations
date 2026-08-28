"""Waves gallery — writing, Chinese movable type, urban crafts, the printing press (illustrated table of contents, 2×2).

Each cell is the wave's OBJECT card as a clickable button (native paginated
navigation): one click opens the wave's first slide. Ligne NG ``design``
(2026-08-26).

SPEAKER NOTES:
Point, don't enumerate: « each image is a door — we will open two or three ».
The full lines live in the tooltip.
"""
# @guideline: postair-minimal

from custom.render import waves_grid_slide
from custom.styles import Styles as s

_MARKER = {"en": "From writing to the press"}
_TITLE = {"en": ("From writing to the ", (s.project.titles.keyword, "press"))}


def build(lang: str = "en", **_):
    waves_grid_slide(_MARKER, _TITLE, first=1, last=4, lang=lang)
