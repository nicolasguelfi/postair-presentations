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



# ── Réglages visuels de CET axe (NG 2026-08-31) — la main de l'artiste.
# {"<sous-slide>": {"<paramètre>": valeur}} — clés : identity_a/b, stage,
# waves_a/b, figure_a1..a3/b1..b3, arguments_a/b ; paramètres en ABSOLU
# (statement_zoom=120) ou en FACTEUR sur le calcul auto
# (statement_zoom_scale=1.15). Vide = calcul auto partout. La liste
# complète des paramètres est dans la docstring d'axis_slides.
TUNING: dict = {}


def build(lang: str = "en", **_):
    axis_slides("altruism", lang=lang, tuning=TUNING)
