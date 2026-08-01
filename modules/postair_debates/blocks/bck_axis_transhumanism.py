"""Transhumanism ⇄ Humanism — the two poles, their figures, their arguments.

Seven sub-slides rendered by ``custom.render.axis_slides``: for each pole its
identity and three survey statements, the three historical figures who held
it, and three sourced contemporary arguments; then the two poles face to face.
Nothing on these slides is written here — everything comes from the frozen
manifest.

SPEAKER NOTES:
The axis that makes a room go quiet, so give it room. Avoid science
fiction: start from what already exists — a prosthesis, a pacemaker, a
model that writes in your voice. The line each student draws, and their
reason for drawing it there, is the whole content of this debate.
"""
# @guideline: postair-minimal

from custom.render import axis_slides


def build():
    axis_slides("transhumanism")
