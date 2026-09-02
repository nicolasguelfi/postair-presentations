"""Takeaways (G12) — four memo cards, and nothing else.

Four numbered cards, big enough to be photographed from the back row. The
resources to go further live in the tooltip; the full bibliography closes the
document one slide later.

Le FAIT vit ici (règle NG 2026-08-18) : les quatre cartes-mémo s'éditent dans
ce bloc. Aucune affirmation sourcée sur cette slide — quand une source
arrive, la phrase bibliographique reste dérivée de ``references.bib`` par
``citation()``/``cite`` — clé inconnue = erreur bruyante.

SPEAKER NOTES:
One minute. Read the four cards, slowly, once. Suggest the room photograph
the slide. Hand over to the Mistral session: « you now know what it is —
next, you build with it ».
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    number = s.project.titles.subtitle + s.project.colors.amber + s.center_txt + s.bold
    short = s.project.body.bullet + s.center_txt + s.bold
    detail = s.project.body.caption + s.center_txt


bs = BlockStyles

# ── Les quatre cartes-mémo — photographiables du dernier rang ───────────────
_TAKEAWAYS = [
    {
        "n": "1",
        "short": {"en": "Predicting ≠ knowing", "fr": "Prédire ≠ savoir"},
        "detail": {"en": ("A language model produces the plausible next word. "
                          "Fluency is not truth."), "fr": "Un modèle de langue produit le prochain mot plausible. La fluidité n’est pas la vérité."},
    },
    {
        "n": "2",
        "short": {"en": "Verify everything that matters", "fr": "Vérifier tout ce qui compte"},
        "detail": {"en": "Names · numbers · references → check at the source", "fr": "Noms · chiffres · références → vérifier à la source"},
    },
    {
        "n": "3",
        "short": {"en": "A learning tool, not a replacement", "fr": "Un outil pour apprendre, pas un remplaçant"},
        "detail": {"en": "It explains · it never learns IN YOUR PLACE", "fr": "Il explique · il n’apprend jamais À VOTRE PLACE"},
    },
    {
        "n": "4",
        "short": {"en": "Your posture is yours", "fr": "Votre posture vous appartient"},
        "detail": {"en": "9 axes · no right answer · not choosing = choosing", "fr": "9 axes · pas de bonne réponse · ne pas choisir = choisir"},
    },
]

_MARKER = {"en": "Takeaways", "fr": "À retenir"}
_TITLE = {"en": ("Four things to ", (s.project.titles.keyword, "take home")), "fr": ("Quatre choses à ", (s.project.titles.keyword, "emporter"))}
_TIP_TITLE = {"en": "To go further", "fr": "Pour aller plus loin"}
_TIP = [
    ({"en": "At UL", "fr": "À l’UL"},
     {"en": ("Computer science and AI courses, the university's AI learning "
             "resources, and the guidelines session right after Mistral."), "fr": "Les cours d’informatique et d’IA, les ressources d’apprentissage de l’IA de l’université, et la session sur les lignes directrices juste après Mistral."}),
    ({"en": "Beyond UL", "fr": "Au-delà de l’UL"},
     {"en": ("Open MOOCs on machine learning fundamentals, and accessible "
             "reads on how language models work — ask, the speaker has "
             "favourites."), "fr": "Des MOOC ouverts sur les fondements de l’apprentissage automatique, et des lectures accessibles sur le fonctionnement des modèles de langue — demandez, l’orateur a ses favoris."}),
    ({"en": "The session's sources", "fr": "Les sources de la session"},
     {"en": ("Every number and claim of this session is on the References "
             "page at the end of this document — hover any citation code to "
             "see its source."), "fr": "Chaque chiffre et chaque affirmation de cette session figurent sur la page Références à la fin de ce document — survolez un code de citation pour voir sa source."}),
]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(T(h, lang), T(d, lang)) for h, d in _TIP],
                )
        st_space("v", "1vh")
        with st_grid(cols=s.project.grids.balanced(len(_TAKEAWAYS)), gap="1vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for item in _TAKEAWAYS:
                with st_zoom(120),g.cell(), st_block(s.project.cards.blue):
                    st_write(bs.number, item["n"], tag=t.div)
                    with st_zoom(120):
                        st_write(bs.short, T(item["short"], lang), tag=t.div)
                    st_space("v", "0.2vh")
                    st_write(bs.detail, T(item["detail"], lang), tag=t.div)
