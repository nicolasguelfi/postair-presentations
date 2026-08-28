"""Openness ⇄ Resistance — the two poles, their figures, their arguments.

Seven sub-slides rendered by ``custom.render.axis_slides``: for each pole its
identity and three survey statements, the three historical figures who held
it, and three sourced contemporary arguments; then the two poles face to face.
Nothing on these slides is written here — everything comes from the frozen
manifest.

SPEAKER NOTES:
Resistance is not technophobia; it is protecting a practice that works
from a tool that has not proved itself. Ask for one practice each student
would defend from AI, and one they would hand over tomorrow. The answers
split by discipline, which makes this the best axis to run with a room
holding three faculties.
"""
# @guideline: postair-minimal

from custom.render import axis_slides


def build(lang: str = "en", **_):
    axis_slides("openness")
