"""Waves gallery — electricity, motor and aviation, mass media, the atom (illustrated table of contents, 2×2).

Each cell is the wave's OBJECT card as a clickable button (native paginated
navigation): one click opens the wave's first slide. Ligne NG ``design``
(2026-08-26).

SPEAKER NOTES:
Point, don't enumerate: « each image is a door — we will open two or three ».
The full lines live in the tooltip.
"""
# @guideline: postair-minimal

from custom.render import waves_grid_slide


def build(lang: str = "en", **_):
    waves_grid_slide("From the dynamo to the atom",
                     ("From the dynamo to the ", "atom", ""), first=9, last=12)
