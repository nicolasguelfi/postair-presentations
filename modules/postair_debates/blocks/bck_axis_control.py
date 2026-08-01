"""Freedom ⇄ Control — the two poles, their figures, their arguments.

Seven sub-slides rendered by ``custom.render.axis_slides``: for each pole its
identity and three survey statements, the three historical figures who held
it, and three sourced contemporary arguments; then the two poles face to face.
Nothing on these slides is written here — everything comes from the frozen
manifest.

SPEAKER NOTES:
Note the display order: here the accelerating pole is Freedom, on the left
of the instrument. The debate slides into 'rules versus no rules' unless
you anchor it — ask who writes the rules, who enforces them, and what
happens to the people the rules did not anticipate.
"""
# @guideline: postair-minimal

from custom.render import axis_slides


def build():
    axis_slides("control")
