"""AI image prompt system — POSTAIR graphic line: PAPERCUT.

Style retained by NG on the 2026-07-29 review board (stylepostair style=s4):
layered paper-cut collage, bright joyful colors, luminous — the flat navy
line is superseded. Every generated image = AI_PREFIX + specific scene +
AI_SUFFIX_<orientation>. The 3D Pixar mascots stay unchanged and pop on
top of the papercut scenes.

Display convention (NG): generated images render at 70% display zoom by
default (managed-image metadata ``display_zoom: 70``).
"""

AI_PREFIX = (
    "Layered paper-cut collage illustration, bright colored cardstock "
    "(yellow, coral, turquoise, lilac, leaf green), visible paper edges and "
    "soft drop shadows, playful handcrafted festive mood, luminous sky. "
    "Human figures as abstract paper silhouettes seen from behind, never "
    "faces. AI is always represented as a glowing warm amber paper sun or "
    "orb, never anthropomorphic. Clean layered composition. "
)

AI_SUFFIX_LANDSCAPE = (
    " Wide 16:9 composition, one off-centre focal point, rising diagonal "
    "energy. NO text, NO logos, NO signage, NO photorealism."
)

AI_SUFFIX_PORTRAIT = (
    " Vertical composition, one off-centre focal point, rising diagonal "
    "energy. NO text, NO logos, NO signage, NO photorealism."
)
