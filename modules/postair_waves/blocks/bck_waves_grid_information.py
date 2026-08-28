"""Waves gallery — the computer, synthetic chemistry, genetic engineering, the Web (illustrated table of contents, 2×2).

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

_MARKER = {"en": "From the computer to the Web", "fr": "De l'ordinateur au Web"}
_TITLE = {"en": ("From the computer to the ", (s.project.titles.keyword, "Web")), "fr": ("De l'ordinateur au ", (s.project.titles.keyword, "Web"))}


def build(lang: str = "en", **_):
    waves_grid_slide(_MARKER, _TITLE, first=13, last=16, lang=lang)
