"""Trust ⇄ Self-reliance — the two poles, their figures, their arguments.

Seven sub-slides rendered by ``custom.render.axis_slides``: for each pole its
identity and three survey statements, the three historical figures who held
it, and three sourced contemporary arguments; then the two poles face to face.
Nothing on these slides is written here — everything comes from the frozen
manifest.

SPEAKER NOTES:
The opening axis, and the easiest to get wrong. Self-reliance is not
ignorance and trust is not naivety — say that before anyone speaks, or the
debate turns into experts against cranks in ninety seconds. The useful
question is not whom you believe but who has the last word when they
disagree. Ask the room for a case where they checked an expert claim
themselves, and for one where they could not.
"""
# @guideline: postair-minimal

from custom.render import axis_slides


def build(lang: str = "en", **_):
    axis_slides("trust", lang=lang)
