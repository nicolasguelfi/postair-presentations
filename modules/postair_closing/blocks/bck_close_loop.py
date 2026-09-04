"""Closing — the loop of the day (C1).

One dominant papercut image (the morning's campus, matured: the amber sun
higher and brighter) and the four steps of the day in a card row — posture,
understanding, practice, rules.

Le FAIT vit ici (règle NG 2026-08-18) : les quatre étapes du jour et le choix
des citekeys s'éditent dans ce bloc. La phrase bibliographique reste dérivée
de ``references.bib`` par ``citation()`` — clé inconnue = erreur bruyante.

Conversion R-i18n (2026-09-03) : tout texte projeté est une feuille
``{"en", "fr"}`` résolue par ``T()``/``TF()`` de ``postair_lang``.

SPEAKER NOTES:
Two minutes, warm. Walk the four cards in the day's order and land the
sentence: « you now have all four — your posture, the understanding, the
practice, and the rules. You have everything to start well. » The four decks
stay online; the next slide says where.
"""
# @guideline: postair-minimal

from custom.prompts import AI_PREFIX, AI_SUFFIX_LANDSCAPE
from custom.refs import citation
from custom.styles import Styles as s
from custom.visuals import hero_image
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.hero_split import hero_split


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    icon = s.project.titles.subtitle + s.center_txt
    label = s.project.body.bullet + s.center_txt + s.bold
    big = s.project.titles.subtitle + s.project.colors.amber + s.center_txt
    cite = s.project.body.caption + s.center_txt


bs = BlockStyles

# ── Le fait : les quatre acquis du jour ─────────────────────────────────────
#: « label » est projeté sur la carte ; « session » vit dans le tooltip.
_STEPS = [
    {"icon": "🎡",
     "label": {"en": "Your posture", "fr": "Votre posture"},
     "session": {"en": "The morning: nine axes, your radar, the debates",
                 "fr": "Le matin : neuf axes, votre radar, les débats"}},
    {"icon": "🤖",
     "label": {"en": "Understanding", "fr": "La compréhension"},
     "session": {"en": "GenAI: what it is, what it gets wrong",
                 "fr": "GenAI : ce qu’elle est, où elle se trompe"}},
    {"icon": "⚡",
     "label": {"en": "Practice", "fr": "La pratique"},
     "session": {"en": "Mistral: build your own study agent",
                 "fr": "Mistral : construire votre propre agent d’étude"}},
    {"icon": "📋",
     "label": {"en": "The rules", "fr": "Les règles"},
     "session": {"en": "These guidelines: use it well, openly",
                 "fr": "Ces lignes directrices : bien l’utiliser, ouvertement"}},
]
_CITEKEYS = ["guelfi-postair"]

_MARKER = {"en": "The loop", "fr": "La boucle"}
_TITLE = {"en": ("You now have ", (s.project.titles.keyword, "all four")),
          "fr": ("Vous avez désormais ", (s.project.titles.keyword, "les quatre"))}
_BIG = {"en": "You have everything to start well ",
        "fr": "Vous avez tout pour bien commencer "}
_TIP_TITLE = {"en": "The day, in one sentence each",
              "fr": "La journée, une phrase par séance"}
_TIP_DOCS = ({"en": "The four documents", "fr": "Les quatre documents"},
             {"en": ("All online, linked from the hub "
                     "on the next slide — they stay available after today."),
              "fr": ("Tous en ligne, reliés depuis le hub de la slide "
                     "suivante — ils restent disponibles après aujourd’hui.")})
#: Jamais projeté, gardé pour la vérifiabilité (entrée « big » de l'ancien
#: facts.json) : « You now have all four ».

_LOOP_PROMPT = (
    AI_PREFIX
    + "A stylised papercut university campus at midday, the warm amber paper "
      "sun now high and radiant above its towers, the whole scene brighter "
      "and warmer than dawn; a diverse crowd of small abstract paper "
      "silhouettes seen from behind walks OUT of the campus entrance toward "
      "the viewer, carrying small glowing paper lanterns."
    + AI_SUFFIX_LANDSCAPE
)


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(f"{st_['icon']} {T(st_['label'], lang)}",
                              T(st_["session"], lang))
                             for st_ in _STEPS]
                            + [(T(_TIP_DOCS[0], lang), T(_TIP_DOCS[1], lang))],
                )
        st_space("v", s.project.spacing.title_gap)
        # Gabarit par défaut (NG 2026-08-13) : le campus carré à gauche, les
        # quatre acquis EMPILÉS à droite — la 2e rangée était coupée au pli.
        with hero_split(s, ratio=40, image=lambda: hero_image(
                "guide_loop", _LOOP_PROMPT, "images/guide_loop_fallback.svg",
                alt_ready=("Papercut campus at midday under a radiant amber sun, "
                           "silhouettes walking out carrying lanterns"),
                alt_fallback=("Papercut campus under a high amber sun, silhouettes "
                              "leaving with lanterns"),
                variant="sq")):
            for step in _STEPS:
                with st_block(s.project.cards.blue):
                    with st_zoom(150):
                        st_write(bs.label, step["icon"], "  ", T(step["label"], lang),
                             tag=t.div)
            st_space("v", "0.5vh")
            st_write(bs.big, T(_BIG, lang),
                     citation(*_CITEKEYS,inline=True), tag=t.div)
