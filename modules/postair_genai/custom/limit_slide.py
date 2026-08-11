"""The four « other side » slides — same code, four concern ids.

Découpage NG (2026-08-11) : une slide dense vaut moins que quatre messages
forts — chaque revers (biais, contrôle, données, dépendance) a SA slide, avec
UNE image papier découpé dominante, UN message en gros, UNE ligne de preuve
sourcée (code de citation visible). Même pattern que les blocs d'axes de
``postair_debates`` : écrire le gabarit une fois, un bloc mince par id — un
changement de gabarit touche les quatre slides au même instant.

Data-driven from ``custom.facts`` (section ``concerns``).
"""

from __future__ import annotations

from shared_widgets import st_info_tooltip
from streamtex import st_block, st_grid, st_marker, st_space, st_write
from streamtex.enums import Tags as t

from custom.facts import citekeys, section, text
from custom.prompts import AI_PREFIX, AI_SUFFIX_LANDSCAPE
from custom.refs import citation
from custom.styles import Styles as s
from custom.visuals import hero_image


class SlideStyles:
    title = s.project.titles.slide_title + s.center_txt
    message = s.project.titles.subtitle + s.center_txt
    punch = s.project.body.body + s.project.colors.amber + s.center_txt + s.bold
    cite = s.project.body.caption + s.center_txt


ss = SlideStyles

#: Par revers : (marker, image managée, prompt papercut, repli SVG, alt).
_VISUALS = {
    "bias": (
        "Bias", "genai_bias",
        AI_PREFIX
        + "A large paper balance scale, clearly tilted: one pan low, loaded "
          "with many warm amber paper spheres, the other pan high with a "
          "single small teal sphere. Behind it, a slightly warped paper "
          "mirror leaning against the luminous sky, reflecting the scene "
          "imperfectly."
        + AI_SUFFIX_LANDSCAPE,
        "images/genai_mirror_fallback.svg",
        "Papercut tilted balance scale, one pan loaded with amber spheres, "
        "a warped paper mirror behind",
    ),
    "control": (
        "Control", "genai_control",
        AI_PREFIX
        + "Three enormous paper hands rising from the bottom of the frame, "
          "each holding a glowing warm amber paper orb high above a small "
          "crowd of tiny abstract paper silhouettes watching from below."
        + AI_SUFFIX_LANDSCAPE,
        "images/genai_control_fallback.svg",
        "Papercut giant hands holding amber orbs above a small crowd of "
        "paper silhouettes",
    ),
    "data": (
        "Your data", "genai_data",
        AI_PREFIX
        + "A river of colourful paper speech bubbles flowing across the "
          "frame and pouring into a large paper funnel that feeds a glowing "
          "warm amber paper orb; one abstract paper silhouette seen from "
          "behind watches its own speech bubble float away."
        + AI_SUFFIX_LANDSCAPE,
        "images/genai_data_fallback.svg",
        "Papercut river of speech bubbles pouring into a funnel feeding an "
        "amber orb, one silhouette watching",
    ),
    "brain": (
        "Your brain", "genai_brain",
        AI_PREFIX
        + "A big cheerful paper brain with two strong paper arms lifting a "
          "barbell overhead, small paper sweat drops flying; a warm amber "
          "paper orb rests on the ground nearby, watching idle."
        + AI_SUFFIX_LANDSCAPE,
        "images/genai_brain_fallback.svg",
        "Papercut brain lifting a barbell with paper arms, an amber orb "
        "resting on the ground beside it",
    ),
}


def build_limit(concern_id: str) -> None:
    """One strong message, one strong papercut image, one sourced line."""
    concern = next(c for c in section("concerns") if c["id"] == concern_id)
    marker, name, prompt, fallback, alt = _VISUALS[concern_id]
    st_marker(marker)
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(ss.title, concern["icon"], " ",
                         (s.project.titles.keyword, text(concern["label"])),
                         tag=t.div, toc_lvl="+1", label=text(concern["label"]))
            with g.cell():
                st_info_tooltip(title=text(concern["label"]),
                                entries=[("Documented, not speculative",
                                          text(concern["detail"]))])
        st_space("v", "1vh")
        hero_image(name, prompt, fallback,
                   alt_ready=alt, alt_fallback=alt, width="56%")
        st_space("v", "1.5vh")
        st_write(ss.message, text(concern["message"]), tag=t.div)
        keys = citekeys(concern)
        st_write(ss.punch, text(concern["punch"]),
                 *((" ", citation(*keys)) if keys else ()), tag=t.div)
