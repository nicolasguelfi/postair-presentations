"""Title slide: AI DAY — Facing the AI Revolution.

SPEAKER NOTES:
Warm welcome. Introduce yourself and the team. One sentence on why the
university dedicates three hours of Welcome Week to AI: it will be part of
every study path in every faculty. Announce that the whole room will
participate with their phone OR laptop. Do not reveal the survey mechanics
yet — just promise: by the end of the day you will (1) understand generative
AI, (2) know your own posture facing it, (3) know the UL rules and one
concrete method to study with AI.
"""
# @guideline: postair-minimal

from custom.config import IS_EDITABLE
from custom.prompts import AI_PREFIX, AI_SUFFIX_LANDSCAPE
from custom.styles import Styles as s
from custom.visuals import is_synthetic
from postair_data import mascot
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.ai_mark import dd35_overlay


class BlockStyles:
    over = s.project.titles.subtitle + s.center_txt
    title = s.project.titles.hero + s.center_txt
    sub = s.project.titles.subtitle + s.center_txt
    mascot_caption = s.project.body.mascot_name + s.center_txt


bs = BlockStyles

HERO_PROMPT = (
    AI_PREFIX
    + "A stylised university campus at dawn seen from a distance, a warm glowing "
      "amber orb rising above its towers like a new sun, a diverse crowd of small "
      "abstract silhouettes seen from behind walking together toward the campus "
      "entrance."
    + AI_SUFFIX_LANDSCAPE
)


def build(lang: str = "en", **_):
    st_marker("Title — AI Day")
    medio = mascot("Medio")
    # page_fill_full: no side padding, so the 5/55/35/5 grid below is
    # computed against the real window width (NG 2026-07-30).
    with st_block(s.project.containers.page_fill_full):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.over, "University of Luxembourg · Welcome Week", tag=t.div)
                with st_zoom(60) :
                    st_write(bs.title, "THE AUGMENTED STUDENT", tag=t.div, toc_lvl="1", label="Welcome")
                st_write(bs.sub, "Facing the AI Revolution", tag=t.div)
            with g.cell():
                st_info_tooltip(
                    title="About this day",
                    entries=[
                        ("Who", "Organised for all new students of the three faculties — "
                                "FSTM (Science, Technology and Medicine), FDEF (Law, Economics "
                                "and Finance), FHSE (Humanities, Education and Social Sciences)."),
                        ("Why", "AI will be part of every study path. Today is about "
                                "understanding it, locating yourself in front of it, and "
                                "learning the University's rules of the game."),
                        ("Three promises", "1. Understand what generative AI really is. "
                                           "2. Discover YOUR posture facing AI — measured live. "
                                           "3. Leave with the UL guidelines and a concrete method "
                                           "to study with AI."),
                        ("Participation", "Keep your phone or laptop at hand — the whole room "
                                          "takes part in a live, anonymous survey."),
                    ],
                )
        # st_space("v", s.project.spacing.title_gap)
        # Window-width layout (NG): 5% free · hero 55% · Medio 35% · 5% free.
        with st_grid(cols="5% 55% 35% 5%",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_space("h", "1px")
            with g.cell():
                with st_zoom(50):
                    st_image(
                        s.project.cards.media_center, width="100%",
                        alt="Stylised campus at dawn under a rising amber AI orb, "
                            "crowd of silhouettes walking toward the entrance",
                        editable=IS_EDITABLE, name="welcome_title_hero",
                        prompt=HERO_PROMPT, provider="openai", ai_size="1536x1024",
                        overlay=dd35_overlay(is_synthetic("welcome_title_hero")))
            with g.cell():
                st_image(s.project.cards.media_center, width="100%",
                         uri=medio["image"],
                         alt=f"{medio['name']}, the panda moderator mascot, "
                             "welcoming the audience",
                    overlay=dd35_overlay())
                st_write(bs.mascot_caption, f"{medio['name']} — your co-host today", tag=t.div)
            with g.cell():
                st_space("h", "1px")
