"""What it gets wrong — your data is the raw material (G8c). Série « the other side ».

Composition de série (ex-gabarit ``limit_slide``, NG 2026-08-11) : UNE image
papier découpé dominante à gauche (``hero_split``), UN message en gros, UNE
ligne punch. Les 4 blocs ``bck_genai_limit_*`` partagent cette composition :
toute évolution s'y réplique à la main.

Le FAIT vit ici (règle NG 2026-08-18) : label, message, punch et detail
s'éditent dans ce bloc. Slide sans citation — deux règles pratiques, pas une
mesure publiée.

SPEAKER NOTES:
One minute. The image says it: your conversations flow into the funnel. Two
practical rules, spoken plainly — read what you accept, and keep personal and
sensitive data out of free tools. Bridge to the UL-supported tools in the
guidelines session.
"""
# @guideline: postair-minimal

from shared_widgets import st_info_tooltip
from streamtex import st_block, st_grid, st_marker, st_space, st_write
from streamtex.enums import Tags as t

from custom.prompts import AI_PREFIX, AI_SUFFIX_LANDSCAPE
from custom.styles import Styles as s
from custom.visuals import hero_image
from postair_pack.components.hero_split import hero_split


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    message = s.project.titles.subtitle + s.center_txt
    punch = s.project.body.body + s.project.colors.amber + s.center_txt + s.bold


bs = BlockStyles

# ── Le revers ───────────────────────────────────────────────────────────────
_MARKER = "Your data"
_ICON = "🔐"
_LABEL = "Your data is the raw material"
_MESSAGE = "« Free » = paid with your conversations"
_PUNCH = "Read what you sign · personal / sensitive = OUT"
_DETAIL = ("Free tools pay themselves with your conversations. Read what you "
           "accept — and keep personal and sensitive data out.")

# ── L'image papercut ────────────────────────────────────────────────────────
_IMAGE = "genai_data"
_FALLBACK = "images/genai_data_fallback.svg"
_ALT = ("Papercut river of speech bubbles pouring into a funnel feeding an "
        "amber orb, one silhouette watching")
_SCENE = ("A river of colourful paper speech bubbles flowing across the "
          "frame and pouring into a large paper funnel that feeds a glowing "
          "warm amber paper orb; one abstract paper silhouette seen from "
          "behind watches its own speech bubble float away.")


def build(lang: str = "en", **_):
    st_marker(_MARKER)
    prompt = AI_PREFIX + _SCENE + AI_SUFFIX_LANDSCAPE
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, _ICON, " ",
                         (s.project.titles.keyword, _LABEL),
                         tag=t.div, toc_lvl="+1", label=_LABEL)
            with g.cell():
                st_info_tooltip(title=_LABEL,
                                entries=[("Documented, not speculative",
                                          _DETAIL)])
        st_space("v", s.project.spacing.title_gap)
        # Gabarit par défaut (NG 2026-08-13) : image carrée à gauche ~50 %,
        # message + punch empilés à droite — plus rien sous le pli.
        with hero_split(s, image=lambda: hero_image(
                _IMAGE, prompt, _FALLBACK, alt_ready=_ALT, alt_fallback=_ALT,
                variant="sq")):
            st_write(bs.message, _MESSAGE, tag=t.div)
            st_space("v", "1vh")
            st_write(bs.punch, _PUNCH, tag=t.div)
