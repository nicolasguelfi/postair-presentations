"""Individualism ⇄ Altruism — the two poles, their figures, their arguments.

Seven sub-slides rendered by ``custom.render.axis_slides``: for each pole its
identity and three survey statements, the three historical figures who held
it, and three sourced contemporary arguments; then the two poles face to face.
Nothing on these slides is written here — everything comes from the frozen
manifest.

SPEAKER NOTES:
The asymmetric axis — no figure in this study champions individualism, and
the slide says so. That absence IS the debate: ask why nobody wrote it
down, and whether a position can be widely held and never defended in
public. It is the sharpest question in the whole bank; keep it for a room
that has warmed up.
"""
# @guideline: postair-minimal

from custom.render import axis_slides


def build(lang: str = "en", **_):
    axis_slides("altruism", lang=lang)
