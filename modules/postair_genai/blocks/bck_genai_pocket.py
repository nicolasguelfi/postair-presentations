"""Already in your pocket (G2) — you have been using AI for years.

Recomposition NG (2026-08-13, gabarit par défaut) : l'image CARRÉE à gauche
sur ~50 %, les cinq étiquettes empilées à droite — l'ancienne grille 3+2 sous
l'image coupait sa seconde rangée au pli. La distinction classique/génératif
ferme la colonne en télégraphique ; le détail vit dans l'infobulle.

Le FAIT vit ici (règle NG 2026-08-18) : les cinq étiquettes et la distinction
classique/génératif s'éditent dans ce bloc. Aucune affirmation sourcée sur
cette slide — quand une source arrive, la phrase bibliographique reste
dérivée de ``references.bib`` par ``citation()``/``cite`` — clé inconnue =
erreur bruyante.

SPEAKER NOTES:
Two minutes. Start from lived experience, never from theory: everyone in the
room used at least three of these five today. Land the distinction once —
classic AI picks among existing things, generative AI writes the next thing —
it is the hinge of the whole session.
"""
# @guideline: postair-minimal

from custom.prompts import AI_PREFIX, AI_SUFFIX_LANDSCAPE
from custom.styles import Styles as s
from custom.visuals import hero_image
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.hero_split import hero_split


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    label = s.project.body.bullet + s.center_txt
    distinction = s.project.body.body + s.project.colors.keyword + s.center_txt


bs = BlockStyles

_POCKET_PROMPT = (
    AI_PREFIX
    + "A large paper smartphone standing upright at the centre, its screen a "
      "warm amber paper glow, with five small colourful paper satellites "
      "orbiting around it on visible paper orbit rings: a tiny camera, a "
      "speech bubble, a globe, a film strip and a keyboard, all cut from "
      "bright cardstock."
    + AI_SUFFIX_LANDSCAPE
)

# ── Les cinq IA déjà dans la poche (étiquette projetée ; détail au survol) ──
#: Jamais projeté, gardé pour la vérifiabilité — la phrase d'accroche de
#: l'ancienne section « pocket » de facts.json (entrée ``lead``, jamais
#: consommée par le rendu) : « You have been using AI for years ».
#: Les identifiants d'origine des items : autocomplete, photos, reco,
#: translate, assistants.
_ITEMS = [
    {
        "icon": "⌨️",
        "label": "Autocomplete",
        "detail": ("Your keyboard predicts your next word — a small language "
                   "model, running on your phone."),
    },
    {
        "icon": "📷",
        "label": "Photo filters",
        "detail": ("Portrait mode, night mode, face unlock: neural networks "
                   "process every shot."),
    },
    {
        "icon": "🎬",
        "label": "Recommendations",
        "detail": ("What you watch, hear and scroll next is ranked by "
                   "prediction models trained on billions of choices."),
    },
    {
        "icon": "🌍",
        "label": "Translation",
        "detail": ("Instant translation between ~100 languages runs on the "
                   "same Transformer architecture as chatbots."),
    },
    {
        "icon": "💬",
        "label": "Assistants",
        "detail": ("ChatGPT, Copilot, Le Chat: the newcomers — the first AI "
                   "you TALK to."),
    },
]

# ── La distinction — la charnière de toute la séance ────────────────────────
_CLASSIC = "Classic AI = CHOOSES · feed · faces · spam"
_GENERATIVE = "Generative AI = PRODUCES · text · image · sound · code"


def build():
    st_marker("In your pocket")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "Already in ", (s.project.titles.keyword, "your pocket"),
                         tag=t.div, toc_lvl="+1", label="In your pocket")
            with g.cell():
                st_info_tooltip(
                    title="Two kinds of AI",
                    entries=[
                        ("Classic AI", _CLASSIC),
                        ("Generative AI", _GENERATIVE),
                        *[(f"{item['icon']} {item['label']}", item["detail"])
                          for item in _ITEMS],
                    ],
                )
        st_space("v", s.project.spacing.title_gap)
        with hero_split(s, image=lambda: hero_image(
                "genai_pocket", _POCKET_PROMPT, "images/genai_pocket_fallback.svg",
                alt_ready=("Papercut smartphone with an amber glowing screen, five "
                           "paper satellites orbiting it: camera, speech bubble, "
                           "globe, film strip, keyboard"),
                alt_fallback=("Stylised smartphone with amber orb screen, five "
                              "orbiting icons: keyboard, camera, film, globe, chat"),
                variant="sq")):
            # Cinq étiquettes, un mot chacune — la salle lit l'image, pas un texte.
            for item in _ITEMS:
                with st_block(s.project.cards.blue):
                    st_write(bs.label, item["icon"], "  ",
                             item["label"], tag=t.div)
            st_space("v", "0.5vh")
            st_write(bs.distinction, _CLASSIC, tag=t.div)
            st_write(bs.distinction, _GENERATIVE, tag=t.div)
