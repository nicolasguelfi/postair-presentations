"""Reflex 2 — say it: the five disclosure elements (U3).

Five big numbered cards — the visual IS the checklist — and the one-line
example disclaimer in amber below. Prompt-history advice and the Appendix 1
ready-made disclaimers live in the tooltip.

Le FAIT vit ici (règle NG 2026-08-18) : les cinq éléments de disclosure,
l'exemple, les conseils du tooltip et le choix des citekeys s'éditent dans ce
bloc. La phrase bibliographique reste dérivée de ``references.bib`` par
``citation()`` — clé inconnue = erreur bruyante.

Conversion R-i18n (2026-09-03) : les textes projetés sont des feuilles
{"en", "fr"} résolues par ``T()``/``TF()`` ; SPEAKER NOTES et ``alt=``
restent EN.

SPEAKER NOTES:
Two minutes, one card each, fast. Land on the amber example: a disclosure is
ONE honest sentence, not a confession. Then the practical tip from the
tooltip, said out loud: teachers may ask for your prompt history — keep your
conversations. The wink is in the tooltip too: the appendix's own examples
were generated with Copilot, then revised.
"""
# @guideline: postair-minimal

from custom.refs import citation
from custom.styles import Styles as s
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    number = s.project.titles.subtitle + s.project.colors.keyword + s.center_txt + s.bold
    short = s.project.body.bullet + s.center_txt + s.bold
    example = s.project.titles.subtitle + s.project.colors.amber + s.center_txt
    cite = s.project.body.caption + s.center_txt


bs = BlockStyles

# ── Le fait : les cinq éléments à dire (guidelines, section 2) ──────────────
#: « short » est projeté sur la carte ; « detail » vit dans le tooltip.
_ITEMS = [
    {"n": "1", "short": {"en": "Which tool", "fr": "Quel outil"},
     "detail": {"en": "Name the tool(s) and version you used.", "fr": "Nommez le ou les outils et la version utilisés."}},
    {"n": "2", "short": {"en": "For what", "fr": "Pour quoi"},
     "detail": {"en": "The purpose: brainstorm, draft, translate, debug…", "fr": "Le but : idées, brouillon, traduction, débogage…"}},
    {"n": "3", "short": {"en": "How much", "fr": "Dans quelle mesure"},
     "detail": {"en": ("The extent of the use — a paragraph, the structure, the "
                       "whole draft."), "fr": "L'étendue de l'usage — un paragraphe, la structure, tout le brouillon."}},
    {"n": "4", "short": {"en": "What YOU did with it", "fr": "Ce que VOUS en avez fait"},
     "detail": {"en": ("Edited, corrected, rewrote, integrated — the output is a "
                       "material, not a result."), "fr": "Édité, corrigé, réécrit, intégré — la sortie est un matériau, pas un résultat."}},
    {"n": "5", "short": {"en": "How you verified", "fr": "Comment vous avez vérifié"},
     "detail": {"en": ("How sources and claims were validated against reliable "
                       "references."), "fr": "Comment sources et affirmations ont été validées contre des références fiables."}},
]
_EXAMPLE = {"en": ("« I used Copilot to brainstorm the outline; all arguments "
                   "and sources are mine and verified. »"),
            "fr": ("« J’ai utilisé Copilot pour ébaucher le plan ; tous les "
                   "arguments et toutes les sources sont de moi et "
                   "vérifiés. »")}
_PROMPTS_HEAD = {"en": "Keep your prompts", "fr": "Gardez vos prompts"}
_PROMPTS_TIP = {"en": ("Teachers may require your prompt history, a usage log and "
                       "your verification evidence — keep your conversations."), "fr": "Les enseignants peuvent exiger votre historique de prompts, un journal d'usage et vos preuves de vérification — gardez vos conversations."}
_ANNEX_HEAD = {"en": "Appendix 1", "fr": "Annexe 1"}
_ANNEX_NOTE = {"en": ("Appendix 1 provides ready-to-use disclaimers per category "
                      "(brainstorming, proofreading, translation, code, content "
                      "generation) — copy and adapt. Footnote of the appendix: those "
                      "examples were themselves generated with Copilot, then "
                      "revised."), "fr": "L'annexe 1 fournit des mentions prêtes à l'emploi par catégorie (idées, relecture, traduction, code, génération de contenu) — copiez et adaptez. Note de bas de page de l'annexe : ces exemples ont eux-mêmes été générés avec Copilot, puis révisés."}
_CITEKEYS = ["i2tl2026-guidelines"]
#: Jamais projeté, gardé pour la vérifiabilité (entrée « big » de l'ancien
#: facts.json) : « Say it — five things ».

_MARKER = {"en": "Say it", "fr": "Le dire"}
_TITLE = {"en": ("Reflex 2 — ", (s.project.titles.keyword, "say it")),
          "fr": ("Réflexe 2 — ", (s.project.titles.keyword, "le dire"))}
_TIP_TITLE = {"en": "Disclosure (guidelines, section 2)",
              "fr": "Déclaration (lignes directrices, section 2)"}
_CITE_LINE = {"en": "One honest sentence is enough ",
              "fr": "Une phrase honnête suffit "}


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
                    entries=[(f"{i['n']} · {T(i['short'], lang)}", T(i["detail"], lang))
                             for i in _ITEMS]
                            + [(T(_PROMPTS_HEAD, lang), T(_PROMPTS_TIP, lang)),
                               (T(_ANNEX_HEAD, lang), T(_ANNEX_NOTE, lang))],
                )
        #st_space("v", "2vh")
        with st_grid(cols=s.project.grids.balanced(len(_ITEMS)), gap="0vh 1vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for item in _ITEMS:
                with g.cell(), st_block(s.project.cards.blue):
                    with st_zoom(110):
                        st_write(bs.number, item["n"], tag=t.div)
                    with st_zoom(140):
                        st_write(bs.short, T(item["short"], lang), tag=t.div)
        st_space("v", "1.5vh")
        st_write(bs.example, T(_EXAMPLE, lang), tag=t.div)
        st_write(bs.cite, T(_CITE_LINE, lang),
                 citation(*_CITEKEYS, inline=True), tag=t.div)
