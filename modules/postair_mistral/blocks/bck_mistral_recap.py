"""Récap méthode + bonnes pratiques (M11) — les 5 cartes en rappel.

LES MÊMES quatre étapes que la slide méthode, depuis le MÊME fait partagé
(facts.json section ``method`` — une seule vérité, deux consommateurs), plus
le badge « keep your prompt history ». Le backup NotebookLM (« d'autres
outils, même méthode ») vit derrière, dans l'annexe.

Le FAIT vit ici (règle NG 2026-08-18) pour le badge et les lignes de
l'infobulle ; la raison charte du badge cite sa clé.

SPEAKER NOTES:
One minute. Read the four words once — frame, sources, test,
iterate — then the badge: keep your prompt history, the guidelines can ask
you to show HOW you used AI. Tease the next session: « the official UL
rules, now ». Hand over.
"""
# @guideline: postair-minimal

from custom.facts import citekeys, fact, section, text
from custom.refs import citation
from custom.styles import Styles as s
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    number = s.project.titles.subtitle + s.project.colors.amber + s.center_txt + s.bold
    label = s.project.body.bullet + s.center_txt + s.bold
    badge = s.project.titles.subtitle + s.project.colors.amber + s.center_txt + s.bold
    badge_line = s.project.body.caption + s.center_txt


bs = BlockStyles

_MARKER = {"en": "Recap", "fr": "Récap"}
_TITLE = {"en": ("The method, ", (s.project.titles.keyword, "to take home")), "fr": ("La méthode, ", (s.project.titles.keyword, "à emporter"))}
_BADGE = {"en": "🗂 keep your prompt history", "fr": "🗂 gardez l’historique de vos prompts"}
_BADGE_LINE = {"en": "transparency · disclosure · the guidelines may ask for it", "fr": "transparence · déclaration · les lignes directrices peuvent le demander"}

_TIP_TITLE = {"en": "Good practices, precisely", "fr": "Les bonnes pratiques, précisément"}
_TIP_WHY_HEAD = {"en": "Why keep your prompts (UL guidelines)", "fr": "Pourquoi garder ses prompts (lignes directrices UL)"}
_TIP_WHY_TAIL = {"en": " Declaring AI use is the default; being able to SHOW how you used it — your prompts, your iterations — is what makes the declaration credible if it is ever challenged.", "fr": " Déclarer l’usage de l’IA est le défaut ; pouvoir MONTRER comment vous l’avez utilisée — vos prompts, vos itérations — rend la déclaration crédible si elle est un jour contestée."}
_TIP_STEPBYSTEP = ({"en": "The written step-by-step", "fr": "Le pas-à-pas écrit"},
                   {"en": ("The complete walkthrough of this session — every "
                           "click, the full system prompt, the four errors "
                           "with their fixes — is published online after the "
                           "AI Day."), "fr": "Le pas-à-pas complet de cette séance — chaque clic, le prompt système complet, les quatre erreurs et leurs corrections — est publié en ligne après l’AI Day."})
_TIP_NEXT = ({"en": "Right after this", "fr": "Juste après"},
             {"en": "The official UL rules, now — the guidelines session grades uses by risk and draws the red lines.", "fr": "Les règles officielles de l’UL, maintenant — la session des lignes directrices classe les usages par risque et trace les lignes rouges."})

# ── La main de l'artiste ────────────────────────────────────────────────────
TUNING = {
    #: Le rappel réutilise la rangée unique de la slide méthode, en plus
    #: compact (pas de ligne de détail : les quatre mots seuls).
    "cols": "repeat(auto-fit, minmax(max(260px, 21%), 1fr))",
    "card_zoom": 110,
}


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    steps = section("method")
    charter = fact("charter", "tools")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with st_zoom(150), g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(T(_TIP_WHY_HEAD, lang),
                              text(charter["claim"], lang) + T(_TIP_WHY_TAIL, lang)),
                             (T(_TIP_STEPBYSTEP[0], lang), T(_TIP_STEPBYSTEP[1], lang)),
                             (T(_TIP_NEXT[0], lang), T(_TIP_NEXT[1], lang))],
                )
        st_space("v", s.project.spacing.title_gap)
        with st_grid(cols=TUNING["cols"], gap="1vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for step in steps:
                with g.cell(), st_block(s.project.cards.blue):
                    with st_zoom(120):
                        st_write(bs.number, step["n"], tag=t.div)
                    with st_zoom(TUNING["card_zoom"]):
                        st_write(bs.label, text(step["label"], lang), tag=t.div)
        st_space("v", "4vh")
        with st_zoom(120):
            st_write(bs.badge, T(_BADGE, lang), tag=t.div)
        st_space("v", "1vh")
        st_write(bs.badge_line, T(_BADGE_LINE, lang), " ",
                 citation(*citekeys(charter)), tag=t.div)
