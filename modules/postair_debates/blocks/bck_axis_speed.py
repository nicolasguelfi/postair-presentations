"""Speed ⇄ Prudence — the two poles, their figures, their arguments.

Seven sub-slides rendered by ``custom.render.axis_slides``: for each pole its
identity and three survey statements, the three historical figures who held
it, and three sourced contemporary arguments; then the two poles face to face.
Nothing on these slides is written here — everything comes from the frozen
manifest.

SPEAKER NOTES:
The most familiar axis and the one with the sharpest split in a first-year
room. Keep it concrete: not 'should we go fast' but 'who pays if we are
wrong, and can it be undone'. The prudence bench wins on irreversible
harms, the speed bench wins on the cost of waiting — let both land.
"""
# @guideline: postair-minimal

from custom.render import axis_slides


def build(lang: str = "en", **_):
    axis_slides("speed", lang=lang)
