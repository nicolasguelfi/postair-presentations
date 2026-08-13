"""Reflex 1 — by default: PERMITTED (U2).

THE rule the whole room must remember word for word. One dominant papercut
image (the green light), the verbatim boxed rule of the guidelines (p.4), the
two caveats, and Kuri the curiosity mascot beside the message. Data-driven
from ``custom.facts`` (section ``default_rule``).

SPEAKER NOTES:
Two minutes. Read the verbatim rule slowly, once — this is the sentence 1500
people must retain. Then the two caveats, in order: the course rules PRIME,
and in doubt you ask BEFORE. The consultation anecdote (the default became
permissive after community feedback) is in the tooltip if the room doubts the
openness is real.
"""
# @guideline: postair-minimal

from custom.facts import citekeys, section, text
from custom.prompts import AI_PREFIX, AI_SUFFIX_LANDSCAPE
from custom.refs import citation
from custom.styles import Styles as s
from custom.visuals import hero_image
from postair_data import mascot
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.ai_mark import ai_marked
from postair_pack.components.hero_split import hero_split


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    verbatim = s.project.body.bullet + s.center_txt
    caveat = s.project.body.bullet + s.project.colors.amber + s.center_txt + s.bold
    cite = s.project.body.caption + s.center_txt
    mascot_name = s.project.body.mascot_name + s.center_txt


bs = BlockStyles

_GREEN_PROMPT = (
    AI_PREFIX
    + "A tall paper traffic light with a single big round glowing leaf-green "
      "paper light, standing beside a papercut road that curves toward a "
      "bright horizon; a small paper signpost next to it. One abstract paper "
      "silhouette seen from behind walks confidently past the green light."
    + AI_SUFFIX_LANDSCAPE
)


def build():
    st_marker("Permitted")
    rule = section("default_rule")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "Reflex 1 — by default: ",
                         (s.project.titles.keyword, "permitted"),
                         tag=t.div, toc_lvl="+1", label="Permitted")
            with g.cell():
                st_info_tooltip(
                    title="The default rule (guidelines, section 2, p.4)",
                    entries=[
                        ("The boxed rule, verbatim", text(rule["verbatim"])),
                        ("Who can restrict it", "A course can — explicitly, and with a "
                         "pedagogical justification. The syllabus always primes."),
                        ("Why it is permissive", text(rule["anecdote"])),
                    ],
                )
        st_space("v", "1vh")
        # Gabarit par défaut (NG 2026-08-13) : image carrée à gauche, LA règle
        # verbatim boxée à droite — elle était coupée à mi-phrase sous le pli.
        with hero_split(s, zoom=92, image=lambda: hero_image(
                "guide_greenlight", _GREEN_PROMPT,
                "images/guide_greenlight_fallback.svg",
                alt_ready=("Papercut traffic light with one big green light beside "
                           "a road, a silhouette walking past confidently"),
                alt_fallback=("Papercut green light beside a road"),
                variant="sq")):
            with st_block(s.project.cards.blue):
                st_write(bs.verbatim, "« ", text(rule["verbatim"]), " » ",
                         citation(*citekeys(rule)), tag=t.div)
            st_space("v", "0.5vh")
            for caveat in rule["caveats"]:
                st_write(bs.caveat, text(caveat), tag=t.div)
            st_space("v", "0.5vh")
            kuri = mascot("Kuri")
            with ai_marked():
                st_image(s.project.cards.media_center, width="min(7vw, 13vh)",
                         uri=kuri["image"], alt="Kuri, the curiosity mascot")
            st_write(bs.mascot_name, kuri["name"], tag=t.div)
