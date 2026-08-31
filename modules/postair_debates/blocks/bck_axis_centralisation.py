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



# ── Réglages visuels de CET axe (NG 2026-08-31) — la main de l'artiste.
# {"<sous-slide>": {"<paramètre>": valeur}} — clés : identity_a/b, stage,
# waves_a/b, figure_a1..a3/b1..b3, arguments_a/b ; paramètres en ABSOLU
# (statement_zoom=120) ou en FACTEUR sur le calcul auto
# (statement_zoom_scale=1.15). Vide = calcul auto partout. La liste
# complète des paramètres est dans la docstring d'axis_slides.
TUNING: dict = {}


def build(lang: str = "en", **_):
    axis_slides("centralisation", lang=lang, tuning=TUNING)
