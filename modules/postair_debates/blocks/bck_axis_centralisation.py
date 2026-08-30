"""Centralisation ⇄ Decentralisation — the two poles, their figures, their arguments.

Seven sub-slides rendered by ``custom.render.axis_slides``: for each pole its
identity and three survey statements, the three historical figures who held
it, and three sourced contemporary arguments; then the two poles face to face.
Nothing on these slides is written here — everything comes from the frozen
manifest.

SPEAKER NOTES:
The most abstract axis for a first-year room, so ground it immediately in
something they use: whose servers, whose model, whose decision when it is
withdrawn. Centralisation has the better safety argument and the worse
power argument; make the room say both out loud.
"""
# @guideline: postair-minimal

from custom.render import axis_slides


def build(lang: str = "en", **_):
    axis_slides("centralisation", lang=lang)
