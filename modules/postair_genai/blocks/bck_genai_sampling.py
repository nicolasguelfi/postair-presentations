"""Turn the dials — four generations of « Luxembourg is a ____ », temperature × top-k.

Insertion NG (2026-09-07, J-1) : juste après le film, la preuve par
l'expérience — la MÊME phrase à trou que Predict, soumise quatre fois au
modèle avec des réglages de tirage différents (température, top-k), et
quatre phrases qui n'ont rien à voir. Le tooltip « Temperature » de Predict,
promu en slide : « même question, réponses différentes — par conception, pas
par bug ».

Composition (proposition NG) : une grille 2 × 2, une carte par génération ;
dans chaque carte, la ligne des deux réglages (deux pastilles colorées :
température en bleu, top-k en teal — la MÊME couleur pour le même réglage
sur les quatre cartes, c'est ce qui rend la comparaison lisible), puis la
phrase générée. L'ambre reste l'unique accent focal : le punch sous la
grille. Grille plate (R4b) : les pastilles sont des fragments stylés d'une
seule ligne ``st_write``, jamais une grille imbriquée.

Le FAIT vit ici (règle NG 2026-08-18) : les quatre phrases sont les SORTIES
BRUTES de l'expérience de l'orateur (capture NG du 2026-09-07), reproduites
telles quelles en anglais dans les DEUX langues (donnée citée verbatim, jamais
traduite — traduire une génération serait la falsifier) ; les trois phrases
que la capture coupe portent une ellipse muette. Aucune affirmation sourcée
sur cette slide.

SPEAKER NOTES:
One minute. Same blank as before, four runs. Read the two dials once, out
loud: temperature = how bold the draw, top-k = how many candidates stay in
the hat. Then let the room read the four sentences — laugh at the 3 billion
people, note that not even the cautious one is right (Luxembourg has some
680 000 inhabitants, not 1.5 million). The point is the punch: the machine
does not « know » the answer, it draws a plausible next word, and the dials
decide how plausible. Bridge: « now imagine that draw made at the scale of
the whole web — next slide ».
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.design_systems.postair_dark import KEYWORD, PRIMARY

#: Les deux pastilles de réglage : bleu = température, teal = top-k. Une
#: couleur par RÉGLAGE, jamais par carte — la légende est la couleur.
_CHIP = (
    "display: inline-block; padding: 0.3vh 1.1vw; border-radius: 999px; "
    "border: 0.3vh solid {c}; background-color: rgba({rgb}, 0.14); "
    "color: {c}; font-weight: 700; white-space: nowrap; line-height: 1.6;"
)
_CHIP_TEMPERATURE = Style(_CHIP.format(c=PRIMARY, rgb="122, 184, 245"),
                          "genai_chip_temperature")
_CHIP_TOPK = Style(_CHIP.format(c=KEYWORD, rgb="46, 196, 182"),
                   "genai_chip_topk")
#: La carte : la surface neutre du DS, centrée verticalement et étirée sur
#: toute sa cellule — les quatre cartes ont la même hauteur (règle d'amphi).
_CARD = s.project.cards.pole_cell + Style(
    "justify-content: center; width: 100%; height: 100%; box-sizing: border-box; "
    "padding: 2vh 1.5vw; gap: 0;",
    "genai_sampling_card",
)


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    dials = s.project.body.bullet + s.center_txt
    sentence = s.project.body.body + s.center_txt
    ellipsis = s.project.colors.muted
    punch = s.project.titles.subtitle + s.project.colors.amber + s.center_txt


bs = BlockStyles

#: Réglages datés (2026-09-07) : la grille est l'unique scène.
TUNING = {"dials_zoom": 80, "sentence_zoom": 130, "punch_zoom": 130}

# ── Les quatre générations — sorties brutes de l'expérience de l'orateur ────
#: ``temperature`` et ``top_k`` sont les étiquettes projetées ; ``text`` est
#: la sortie du modèle, verbatim, en anglais dans les deux langues ;
#: ``cut`` = la capture coupe la phrase (ellipse muette à l'écran).
_RUNS = [
    {"temperature": "0.5", "top_k": "5", "cut": True,
     "text": "Luxembourg is a small country, and is home to a small number of"},  # i18n: verbatim
    {"temperature": "10", "top_k": "10", "cut": False,
     "text": "Luxembourg is a city of more 3 billion people"},  # i18n: verbatim
    {"temperature": "0.2", "top_k": "1", "cut": True,
     "text": "Luxembourg is a country of about 1.5 million people,"},  # i18n: verbatim
    {"temperature": "10", "top_k": "50", "cut": True,
     "text": "Luxembourg is a tiny area from western Spain and parts in the southeastern"},  # i18n: verbatim
]

# ── Les feuilles {en, fr} du bloc ───────────────────────────────────────────
_MARKER = {"en": "Dials", "fr": "Réglages"}
_TITLE = {"en": ("The AI ", (s.project.titles.keyword, "flexibility")),
          "fr": ("La ", (s.project.titles.keyword, "flexibilité"), " de l'IA")}
_LABEL_TEMPERATURE = {"en": "temperature", "fr": "température"}
_LABEL_TOPK = {"en": "top-k", "fr": "top-k"}
_PUNCH = {"en": "Same prompt, four valid answers",
          "fr": "Même prompt, quatre réponses valides"}


_TIP_TITLE = {"en": "The two dials", "fr": "Les deux réglages"}
_TOOLTIP = [
    ({"en": "Temperature", "fr": "La température"},
     {"en": ("How bold the draw is. Low (0.2) = almost always the most probable "
             "word, the same answer every time; high (10) = the improbable words "
             "get their chance, and the sentence drifts."),
      "fr": "L’audace du tirage. Basse (0,2) = presque toujours le mot le plus probable, la même réponse à chaque fois ; haute (10) = les mots improbables ont leur chance, et la phrase dérive."}),
    ({"en": "Top-k", "fr": "Le top-k"},
     {"en": ("How many candidates stay in the hat. k = 1 : only the winner, no "
             "draw at all ; k = 50 : fifty words compete for every position."),
      "fr": "Combien de candidats restent dans le chapeau. k = 1 : seul le gagnant, aucun tirage ; k = 50 : cinquante mots en lice à chaque position."}),
    ({"en": "Reading the four", "fr": "Lire les quatre"},
     {"en": ("Cautious dials give a plausible, bland sentence ; wild dials give "
             "3 billion people or a piece of Spain. Not one of the four is right — "
             "Luxembourg has some 680 000 inhabitants."),
      "fr": "Des réglages prudents donnent une phrase plausible et fade ; des réglages débridés donnent 3 milliards d’habitants ou un bout d’Espagne. Aucune des quatre n’est juste — le Luxembourg compte quelque 680 000 habitants."}),
    ({"en": "Where they come from", "fr": "D’où elles viennent"},
     {"en": ("The speaker’s own runs, the same blank as the Predict slide. The "
             "sentences are reproduced unedited, in English in both languages ; "
             "an ellipsis marks where the capture stops."),
      "fr": "Les essais de l’orateur lui-même, le même trou que la slide Prédire. Les phrases sont reproduites telles quelles, en anglais dans les deux langues ; une ellipse marque où la capture s’arrête."}),
]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(T(h, lang), T(d, lang)) for h, d in _TOOLTIP],
                )
        st_space("v", "1vh")
        # Une carte par génération : la ligne des deux réglages, puis la
        # phrase. Grille équilibrée (2 × 2 pour quatre), étirée sur la hauteur.
        with st_grid(cols=s.project.grids.balanced(len(_RUNS)), gap="1.2vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_stretch) as g:
            for run in _RUNS:
                with g.cell(), st_block(_CARD):
                    with st_zoom(TUNING["dials_zoom"]):
                        # Un fragment = UN style (jamais de tuple imbriqué :
                        # st_write l'ignore en silence — constaté 2026-09-07).
                        st_write(
                            bs.dials,
                            (_CHIP_TEMPERATURE,
                             f"{T(_LABEL_TEMPERATURE, lang)} {run['temperature']}"),
                            "  ",
                            (_CHIP_TOPK, f"{T(_LABEL_TOPK, lang)} {run['top_k']}"),
                            tag=t.div,
                        )
                    st_space("v", "1.2vh")
                    with st_zoom(TUNING["sentence_zoom"]):
                        st_write(bs.sentence, "« ", run["text"],
                                 (bs.ellipsis, " …" if run["cut"] else ""), " »",
                                 tag=t.div)
        st_space("v", "1vh")
        with st_zoom(TUNING["punch_zoom"]):
            st_write(bs.punch, T(_PUNCH, lang), tag=t.div)
