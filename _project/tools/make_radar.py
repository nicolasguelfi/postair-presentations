"""Generate the two POSTAIR radar SVGs of the opening deck.

Deterministic, stdlib-only. Outputs, in
``modules/postair_opening/static/images/``:

``postair_radar_question.svg``
    Nine named axes, concentric guides, a big '?' in the centre — the slide
    that asks the room where it stands.
``postair_radar_example.svg``
    The same frame carrying an EXAMPLE profile, plus the scale marks (0 at the
    centre, 100 at the rim), for the slide that teaches how to read a radar.

    The profile is illustrative and labelled as such on the slide. It is NOT
    the published 'Sovereign Explorer' archetype: its real coordinates live in
    the sumvadis demo, and drawing invented numbers under a real archetype's
    name would be a fabrication. Replace with the demo profile when exported.
"""

import math
from pathlib import Path

AXES = [
    "Trust", "Optimism", "Rationality",
    "Speed", "Openness", "Freedom / Control",
    "Centralisation", "Altruism", "Transhumanism",
]

W, H = 1600, 1000
CX, CY = W / 2, H / 2
R = 380
NAVY = "#1A1A2E"
BLUE = "#7AB8F5"
TEAL = "#2EC4B6"
AMBER = "#F39C12"
TEXT = "#F2EEE6"


def pt(i: int, r: float) -> tuple[float, float]:
    a = -math.pi / 2 + i * 2 * math.pi / len(AXES)
    return CX + r * math.cos(a), CY + r * math.sin(a)


def ring(r: float, opacity: float) -> str:
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in (pt(i, r) for i in range(len(AXES))))
    return (f'<polygon points="{pts}" fill="none" stroke="{BLUE}" '
            f'stroke-opacity="{opacity}" stroke-width="2"/>')


parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
    f'font-family="Inter, Source Sans Pro, sans-serif">',
    f'<rect width="{W}" height="{H}" fill="{NAVY}"/>',
]

for frac, op in ((0.33, 0.18), (0.66, 0.28), (1.0, 0.55)):
    parts.append(ring(R * frac, op))

for i, label in enumerate(AXES):
    x, y = pt(i, R)
    parts.append(f'<line x1="{CX}" y1="{CY}" x2="{x:.1f}" y2="{y:.1f}" '
                 f'stroke="{BLUE}" stroke-opacity="0.35" stroke-width="2"/>')
    parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="{TEAL}"/>')
    lx, ly = pt(i, R + 55)
    anchor = "middle"
    if lx > CX + 40:
        anchor = "start"
    elif lx < CX - 40:
        anchor = "end"
    parts.append(f'<text x="{lx:.1f}" y="{ly:.1f}" fill="{TEXT}" font-size="40" '
                 f'font-weight="600" text-anchor="{anchor}" dominant-baseline="middle">'
                 f'{label}</text>')

parts.append(f'<circle cx="{CX}" cy="{CY}" r="120" fill="{NAVY}" stroke="{AMBER}" '
             f'stroke-width="4" stroke-opacity="0.9"/>')
parts.append(f'<text x="{CX}" y="{CY + 12}" fill="{AMBER}" font-size="170" font-weight="800" '
             f'text-anchor="middle" dominant-baseline="middle">?</text>')
parts.append("</svg>")

IMAGES = (Path(__file__).parent.parent.parent / "modules" / "postair_opening" /
          "static" / "images")
IMAGES.mkdir(parents=True, exist_ok=True)
out = IMAGES / "postair_radar_question.svg"
out.write_text("\n".join(parts), encoding="utf-8")
print(f"wrote {out}")


# --- the annotated example -------------------------------------------------
# One value per axis, in the order of AXES. Chosen to show every posture the
# slide names: two axes hard against a pole, several mid-range, one dead
# centre. Illustrative — see the module docstring.
EXAMPLE = [88, 62, 50, 74, 91, 33, 20, 55, 47]

ex = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
    f'font-family="Inter, Source Sans Pro, sans-serif">',
    f'<rect width="{W}" height="{H}" fill="{NAVY}"/>',
]
for frac, op in ((0.33, 0.18), (0.66, 0.28), (1.0, 0.55)):
    ex.append(ring(R * frac, op))

for i, label in enumerate(AXES):
    x, y = pt(i, R)
    ex.append(f'<line x1="{CX}" y1="{CY}" x2="{x:.1f}" y2="{y:.1f}" '
              f'stroke="{BLUE}" stroke-opacity="0.35" stroke-width="2"/>')
    lx, ly = pt(i, R + 55)
    anchor = "middle"
    if lx > CX + 40:
        anchor = "start"
    elif lx < CX - 40:
        anchor = "end"
    ex.append(f'<text x="{lx:.1f}" y="{ly:.1f}" fill="{TEXT}" font-size="40" '
              f'font-weight="600" text-anchor="{anchor}" dominant-baseline="middle">'
              f'{label}</text>')

profile = " ".join(f"{x:.1f},{y:.1f}"
                   for x, y in (pt(i, R * v / 100) for i, v in enumerate(EXAMPLE)))
ex.append(f'<polygon points="{profile}" fill="{TEAL}" fill-opacity="0.28" '
          f'stroke="{TEAL}" stroke-width="5"/>')
for i, v in enumerate(EXAMPLE):
    x, y = pt(i, R * v / 100)
    ex.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="10" fill="{TEAL}"/>')

# Scale marks read along the first axis: the centre is one pole, the rim the
# other — the single most misread thing about a posture radar.
ex.append(f'<circle cx="{CX}" cy="{CY}" r="9" fill="{AMBER}"/>')
ex.append(f'<text x="{CX + 24}" y="{CY + 8}" fill="{AMBER}" font-size="38" '
          f'font-weight="700">0 — one pole</text>')
rim_x, rim_y = pt(0, R)
ex.append(f'<text x="{rim_x + 24}" y="{rim_y - 18}" fill="{AMBER}" font-size="38" '
          f'font-weight="700">100 — the other</text>')
ex.append("</svg>")

out = IMAGES / "postair_radar_example.svg"
out.write_text("\n".join(ex), encoding="utf-8")
print(f"wrote {out}")
