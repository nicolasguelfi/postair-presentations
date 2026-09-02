"""What it gets wrong — the brain is a muscle (G8d). Série « the other side ».

Composition de série (ex-gabarit ``limit_slide``, NG 2026-08-11) : UNE image
papier découpé dominante à gauche (``hero_split``), UN message en gros, UNE
ligne de preuve sourcée (code de citation visible). Les 4 blocs
``bck_genai_limit_*`` partagent cette composition : toute évolution s'y
réplique à la main.

Le FAIT vit ici (règle NG 2026-08-18) : label, message, punch, detail et
choix des citekeys s'éditent dans ce bloc. La phrase bibliographique reste
dérivée de ``references.bib`` par ``citation()`` — clé inconnue = erreur
bruyante.

SPEAKER NOTES:
One minute, and finish the sequence on this one: the EEG study is recent, on
students, doing exactly what this room does every week — weaker connectivity,
weaker memory of your own text. The image carries the answer: the brain that
lifts its own weights keeps its muscle. Perfect hand-over to « your studies ».
"""
# @guideline: postair-minimal

from postair_i18n import ui
from postair_lang import T
from shared_widgets import st_info_tooltip
from streamtex import st_block, st_grid, st_marker, st_space, st_write, st_zoom
from streamtex.enums import Tags as t

from custom.prompts import AI_PREFIX, AI_SUFFIX_LANDSCAPE
from custom.refs import citation
from custom.styles import Styles as s
from custom.visuals import staged_hero_image
from postair_pack.components.hero_split import hero_split


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    message = s.project.titles.subtitle + s.center_txt
    punch = s.project.body.body + s.project.colors.amber + s.center_txt + s.bold


bs = BlockStyles

# ── Le revers ───────────────────────────────────────────────────────────────
_MARKER = {"en": "Your brain"}
_ICON = "🧠"
_LABEL = {"en": "The brain is a muscle"}
_MESSAGE = {"en": "Effort delegated = muscle melted"}
_PUNCH = {"en": "EEG: brain connectivity ↓\nmemory of YOUR OWN text ↓"}
_DETAIL = {"en": ("In an EEG study, students writing essays with an LLM showed "
                  "weaker brain connectivity and remembered their own text less — "
                  "delegation has a cognitive price. Assessment is being redesigned "
                  "around that fact: AI-free, AI-assisted, AI-integrated.")}
_CITEKEYS = ["kosmyna2025-cognitive-debt", "dec2025-assessment"]

# ── L'image papercut ────────────────────────────────────────────────────────
_IMAGE = "genai_brain"
_FALLBACK = "images/genai_brain_fallback.svg"
_ALT = ("Papercut brain lifting a barbell with paper arms, an amber orb "
        "resting on the ground beside it")
_SCENE = ("A big cheerful paper brain with two strong paper arms lifting a "
          "barbell overhead, small paper sweat drops flying; a warm amber "
          "paper orb rests on the ground nearby, watching idle.")


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    prompt = AI_PREFIX + _SCENE + AI_SUFFIX_LANDSCAPE
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with st_zoom(150),g.cell():
                st_write(bs.title, _ICON, " ",
                         (s.project.titles.keyword, T(_LABEL, lang)),
                         tag=t.div, toc_lvl="+1", label=T(_LABEL, lang))
            with g.cell():
                st_info_tooltip(title=T(_LABEL, lang),
                                entries=[(ui("documented_note", lang),
                                          T(_DETAIL, lang))])
        st_space("v", s.project.spacing.title_gap)
        # Gabarit par défaut (NG 2026-08-13) : image carrée à gauche ~50 %,
        # message + punch empilés à droite — plus rien sous le pli.
        with hero_split(s, ratio=40, image=lambda: staged_hero_image(
                _IMAGE, prompt, _FALLBACK, alt_ready=_ALT, alt_fallback=_ALT,
                variant="sq")):
            with st_zoom(150):
                st_write(bs.message, T(_MESSAGE, lang), tag=t.div)
                st_space("v", "1vh")
                st_write(bs.punch, T(_PUNCH, lang), " ", citation(*_CITEKEYS), tag=t.div)
