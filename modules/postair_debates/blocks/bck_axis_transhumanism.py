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



# ── Réglages visuels de CET axe (NG 2026-08-31) — la main de l'artiste.
# {"<sous-slide>": {"<paramètre>": valeur}} — clés : identity_a/b, stage,
# waves_a/b, figure_a1..a3/b1..b3, arguments_a/b ; paramètres en ABSOLU
# (statement_zoom=120) ou en FACTEUR sur le calcul auto
# (statement_zoom_scale=1.15). Vide = calcul auto partout. La liste
# complète des paramètres est dans la docstring d'axis_slides.
TUNING: dict = {}


def build(lang: str = "en", **_):
    axis_slides("transhumanism", lang=lang, tuning=TUNING)
