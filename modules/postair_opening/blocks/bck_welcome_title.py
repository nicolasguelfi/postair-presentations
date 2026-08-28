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
from postair_lang import T
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

_MARKER = {"en": "Title — AI Day"}
_OVER = {"en": "University of Luxembourg · Welcome Week"}
_TITLE = {"en": "THE AUGMENTED STUDENT"}
_LABEL = {"en": "Welcome"}
_SUB = {"en": "Facing the AI Revolution"}
_TIP_TITLE = {"en": "About this day"}
_TIP = [
    ({"en": "Who"},
     {"en": ("Organised for all new students of the three faculties — FSTM "
             "(Science, Technology and Medicine), FDEF (Law, Economics and "
             "Finance), FHSE (Humanities, Education and Social Sciences).")}),
    ({"en": "Why"},
     {"en": ("AI will be part of every study path. Today is about understanding "
             "it, locating yourself in front of it, and learning the "
             "University's rules of the game.")}),
    ({"en": "Three promises"},
     {"en": ("1. Understand what generative AI really is. 2. Discover YOUR "
             "posture facing AI — measured live. 3. Leave with the UL guidelines "
             "and a concrete method to study with AI.")}),
    ({"en": "Participation"},
     {"en": ("Keep your phone or laptop at hand — the whole room takes part in a "
             "live, anonymous survey.")}),
]
_COHOST = {"en": "{name} — your co-host today"}


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    medio = mascot("Medio")
    # page_fill_full: no side padding, so the 5/55/35/5 grid below is
    # computed against the real window width (NG 2026-07-30).
    with st_block(s.project.containers.page_fill_full):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.over, T(_OVER, lang), tag=t.div)
                with st_zoom(60) :
                    st_write(bs.title, T(_TITLE, lang), tag=t.div, toc_lvl="1",
                             label=T(_LABEL, lang))
                st_write(bs.sub, T(_SUB, lang), tag=t.div)
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(T(h, lang), T(d, lang)) for h, d in _TIP],
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
                st_write(bs.mascot_caption,
                         T(_COHOST, lang).format(name=medio["name"]), tag=t.div)
            with g.cell():
                st_space("h", "1px")
