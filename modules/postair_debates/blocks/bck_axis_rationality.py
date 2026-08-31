"""Rationality ⇄ Emotion — the two poles, their figures, their arguments.

Seven sub-slides rendered by ``custom.render.axis_slides``: for each pole its
identity and three survey statements, the three historical figures who held
it, and three sourced contemporary arguments; then the two poles face to face.
Nothing on these slides is written here — everything comes from the frozen
manifest.

SPEAKER NOTES:
Handle with care: the pole named Emotion is heard as the pole of being
wrong. It is not. It is the position that a technology can be refused for
reasons that no measurement captures — dignity, attachment, the kind of
life one wants. Make someone argue that side properly before the show of
hands, otherwise the vote measures social desirability, not posture.
"""
# @guideline: postair-minimal

from custom.render import axis_slides



# ── Réglages visuels de CET axe (NG 2026-08-31) — la main de l'artiste.
# {"<sous-slide>": {"<paramètre>": valeur}} — clés : identity_a/b, stage,
# waves_a/b, figure_a1..a3/b1..b3, arguments_a/b ; paramètres en ABSOLU
# (statement_zoom=120) ou en FACTEUR sur le calcul auto
# (statement_zoom_scale=1.15). Vide = calcul auto partout. La liste
# complète des paramètres est dans la docstring d'axis_slides.
TUNING: dict = {}


def build(lang: str = "en", **_):
    axis_slides("rationality", lang=lang, tuning=TUNING)
