"""Optimism ⇄ Pessimism — the two poles, their figures, their arguments.

Seven sub-slides rendered by ``custom.render.axis_slides``: for each pole its
identity and three survey statements, the three historical figures who held
it, and three sourced contemporary arguments; then the two poles face to face.
Nothing on these slides is written here — everything comes from the frozen
manifest.

SPEAKER NOTES:
The axis where the room performs rather than answers: optimism sounds
young and pessimism sounds serious. Push past the posturing by asking for
a concrete expectation with a date attached — what will be true in five
years? Both benches usually discover their disagreement is about speed,
not direction, and that is a better debate than the one they started.
"""
# @guideline: postair-minimal

from custom.render import axis_slides


def build(lang: str = "en", **_):
    axis_slides("optimism")
