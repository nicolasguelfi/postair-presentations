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
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.hero_split import hero_split


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    item = s.project.body.bullet + s.center_txt


bs = BlockStyles

_MARKER = {"en": "Your tutor"}
_TITLE = {"en": ("A ", (s.project.titles.keyword, "tireless tutor"), ", 24/7")}
_TIP_TITLE = {"en": "Recommended uses"}
_TIP_GUIDE = ({"en": "What the guidelines recommend"},
              {"en": ("Clarification, training material, study plans, "
                      "brainstorming — the UL guidelines session details every "
                      "recommended use.")})
_TIP_FOUR = {"en": "The four uses on screen"}

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
    {"en": "Concepts endlessly explained"},
    {"en": "Quizzes + flashcards\nfrom YOUR notes"},
    {"en": "Outlines & first drafts\n→ the thinking stays yours"},
    {"en": "A tireless language partner"},
]

#: Une couleur de palette par usage (demande NG 2026-09-02) — les quatre
#: accents du DS dans l'ordre : bleu électrique, teal, ambre, corail.
_DO_COLOURS = [s.project.colors.primary, s.project.colors.keyword,
               s.project.colors.amber, s.project.colors.coral]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with st_zoom(150),g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[
                        (T(_TIP_GUIDE[0], lang), T(_TIP_GUIDE[1], lang)),
                        (T(_TIP_FOUR, lang),
                         " · ".join(T(d, lang) for d in _DO)),
                    ],
                )
        st_space("v", "3vh")
        with hero_split(s, ratio=37, image=lambda: staged_hero_image(
                "genai_desk", _DESK_PROMPT, "images/genai_desk_fallback.svg",
                alt_ready=("Papercut student desk with open notebook, book stack, "
                           "and an amber orb lighting the page while the student "
                           "writes"),
                alt_fallback=("Papercut desk, silhouette writing, amber orb hovering "
                              "over the notebook"),
                variant="sq")):
            for item, colour in zip(_DO, _DO_COLOURS):
                with st_zoom(150):
                    # Une écriture PAR ligne : ``st_write`` n'interprète pas
                    # le ``\n`` (piège documenté au PLAYBOOK) — les puces
                    # multilignes obtiennent ainsi leur vraie coupure.
                    first, *rest = T(item, lang).split("\n")
                    st_write(bs.item + colour, "▸ ", first, tag=t.div)
                    for line in rest:
                        st_write(bs.item + colour, line, tag=t.div)
                    st_space("v", "1vh")
