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


def build():
    waves_grid_slide("From writing to the press",
                     ("From writing to the ", "press", ""), first=1, last=4)
