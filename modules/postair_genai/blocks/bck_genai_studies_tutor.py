"""And for your studies — the tireless tutor (G9a).

Découpage NG (2026-08-11) : l'ancienne slide « studies » portait deux messages
opposés — scindée en deux. Celle-ci est le versant positif : le bureau
augmenté en image dominante, et ce que l'IA fait POUR l'apprentissage.

Le FAIT vit ici (règle NG 2026-08-18) : les quatre usages recommandés
s'éditent dans ce bloc (le versant exigeant vit dans
``bck_genai_studies_exam`` — entrées disjointes de l'ancienne section
« studies »). Aucune affirmation sourcée sur cette slide — quand une source
arrive, la phrase bibliographique reste dérivée de ``references.bib`` par
``citation()``/``cite`` — clé inconnue = erreur bruyante.

SPEAKER NOTES:
Ninety seconds. This is the good news slide: a tutor that never tires, never
judges, and adapts to your pace — the four lines are the recommended uses,
the guidelines session details them. Do not open the caveat here: the next
slide carries it, and it lands harder when this one was generous.
"""
# @guideline: postair-minimal

from custom.prompts import AI_PREFIX, AI_SUFFIX_LANDSCAPE
from custom.styles import Styles as s
from custom.visuals import staged_hero_image
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.hero_split import hero_split


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    item = s.project.body.bullet + s.center_txt


bs = BlockStyles

_DESK_PROMPT = (
    AI_PREFIX
    + "A student desk seen from the side: an open paper notebook, a small "
      "stack of colourful paper books, a desk lamp — and a warm amber paper "
      "orb hovering just above the notebook, lighting the page. The student, "
      "an abstract paper silhouette seen from behind, writes in the notebook "
      "with a pencil."
    + AI_SUFFIX_LANDSCAPE
)

# ── Les quatre usages recommandés — ce que l'IA fait POUR l'apprentissage ───
_DO = [
    "Concepts explained until they CLICK · 24/7",
    "Quizzes + flashcards from YOUR notes",
    "Outlines & first drafts → the thinking stays yours",
    "A tireless language partner",
]


def build(lang: str = "en", **_):
    st_marker("Your tutor")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "A ", (s.project.titles.keyword, "tireless tutor"),
                         ", 24/7", tag=t.div, toc_lvl="+1", label="Your tutor")
            with g.cell():
                st_info_tooltip(
                    title="Recommended uses",
                    entries=[
                        ("What the guidelines recommend", "Clarification, training "
                         "material, study plans, brainstorming — the UL guidelines "
                         "session details every recommended use."),
                        ("The four uses on screen", " · ".join(_DO)),
                    ],
                )
        st_space("v", s.project.spacing.title_gap)
        with hero_split(s, image=lambda: staged_hero_image(
                "genai_desk", _DESK_PROMPT, "images/genai_desk_fallback.svg",
                alt_ready=("Papercut student desk with open notebook, book stack, "
                           "and an amber orb lighting the page while the student "
                           "writes"),
                alt_fallback=("Papercut desk, silhouette writing, amber orb hovering "
                              "over the notebook"),
                variant="sq")):
            for item in _DO:
                st_write(bs.item, "▸ ", item, tag=t.div)
