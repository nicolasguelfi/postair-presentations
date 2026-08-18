"""Closing — the loop of the day (C1).

One dominant papercut image (the morning's campus, matured: the amber sun
higher and brighter) and the four steps of the day in a card row — posture,
understanding, practice, rules.

Le FAIT vit ici (règle NG 2026-08-18) : les quatre étapes du jour et le choix
des citekeys s'éditent dans ce bloc. La phrase bibliographique reste dérivée
de ``references.bib`` par ``citation()`` — clé inconnue = erreur bruyante.

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
    {"icon": "🎡", "label": "Your posture",
     "session": "the morning: nine axes, your radar, the debates"},
    {"icon": "🤖", "label": "Understanding",
     "session": "GenAI: what it is, what it gets wrong"},
    {"icon": "⚡", "label": "Practice",
     "session": "Mistral: build your own study agent"},
    {"icon": "📋", "label": "The rules",
     "session": "these guidelines: use it well, openly"},
]
_CITEKEYS = ["guelfi-postair"]
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


def build():
    st_marker("The loop")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "You now have ", (s.project.titles.keyword, "all four"),
                         tag=t.div, toc_lvl="1", label="The loop")
            with g.cell():
                st_info_tooltip(
                    title="The day, in one sentence each",
                    entries=[(f"{st_['icon']} {st_['label']}", st_["session"])
                             for st_ in _STEPS]
                            + [("The four documents", "All online, linked from the hub "
                                "on the next slide — they stay available after today.")],
                )
        st_space("v", s.project.spacing.title_gap)
        # Gabarit par défaut (NG 2026-08-13) : le campus carré à gauche, les
        # quatre acquis EMPILÉS à droite — la 2e rangée était coupée au pli.
        with hero_split(s, image=lambda: hero_image(
                "guide_loop", _LOOP_PROMPT, "images/guide_loop_fallback.svg",
                alt_ready=("Papercut campus at midday under a radiant amber sun, "
                           "silhouettes walking out carrying lanterns"),
                alt_fallback=("Papercut campus under a high amber sun, silhouettes "
                              "leaving with lanterns"),
                variant="sq")):
            for step in _STEPS:
                with st_block(s.project.cards.blue):
                    st_write(bs.label, step["icon"], "  ", step["label"],
                             tag=t.div)
            st_space("v", "0.5vh")
            st_write(bs.big, "You have everything to start well ",
                     citation(*_CITEKEYS), tag=t.div)
