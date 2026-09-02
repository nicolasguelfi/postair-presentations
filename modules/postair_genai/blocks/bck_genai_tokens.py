"""It reads in tokens (G4c) — la phrase de Predict, découpée en jetons.

Insertion draft des formations (planche drafts2 ``flux=tokens``, NG
2026-09-01) : la promotion en slide éclair du tooltip « Tokens » de G4 — la
MÊME phrase que Predict (« Luxembourg is a ____ »), colorisée fragment par
fragment, « Luxembourg » coupé en deux pour montrer les sous-mots. Trente
secondes de parole, juste avant le film qui anime la mécanique complète.

Pure composition Style (décision stxonly=p1) : les couleurs des jetons sont
les JETONS de la palette — aucun st_html, aucun média.

Le FAIT vit ici (règle NG 2026-08-18) : le découpage illustratif (les
tokenizers réels coupent « Luxembourg » en 2–3 morceaux, le découpage exact
varie par modèle — dit dans le panneau), l'équivalence ~4 caractères / ~¾ de
mot par token. Aucune affirmation sourcée.

SPEAKER NOTES:
Thirty seconds, not more. Point at the split inside « Luxembourg »: the
machine never sees words or letters — fragments, each one a NUMBER. Then the
two equivalences, and PageDown into the film while saying « here is the whole
machinery, animated ».
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    sentence = s.project.titles.slide_title + s.center_txt
    caption = s.project.body.bullet + s.center_txt
    punch = s.project.titles.subtitle + s.project.colors.amber + s.center_txt


bs = BlockStyles

#: Réglages datés (2026-09-01) : la phrase-jetons est l'unique scène.
TUNING = {"sentence_zoom": 170, "drop_vh": 24}

# ── La phrase de Predict, en jetons — chaque fragment porte SA couleur ──────
#: Les styles de fragment viennent du design system (une seule vérité des
#: couleurs) : primaire, teal, ambre en alternance — la coupure DANS
#: « Luxembourg » est le message.
_SENTENCE = {"en": (
    (s.project.colors.primary, "Luxem"),
    (s.project.colors.keyword, "bourg"),
    (s.project.colors.amber, " is"),
    (s.project.colors.primary, " a"),
    (s.project.colors.muted, " ____"),
), "fr": (
    (s.project.colors.primary, "Luxem"),
    (s.project.colors.keyword, "bourg"),
    (s.project.colors.amber, " est"),
    (s.project.colors.primary, " un"),
    (s.project.colors.muted, " ____"),
)}
_MARKER = {"en": "Tokens", "fr": "Jetons"}
_TITLE = {"en": ("It reads in ", (s.project.titles.keyword, "tokens")), "fr": ("Elle lit en ", (s.project.titles.keyword, "jetons"))}
_CAPTION = {"en": "never letters · never words · fragments, each one a NUMBER", "fr": "jamais des lettres · jamais des mots · des fragments, chacun un NOMBRE"}
_PUNCH = {"en": ("1 token ≈ 4 characters ≈ ¾ of a word",), "fr": ("1 jeton ≈ 4 caractères ≈ ¾ de mot",)}

_TIP_TITLE = {"en": "Tokens, precisely", "fr": "Les jetons, précisément"}
_TOOLTIP = [
    ({"en": "The split", "fr": "Le découpage"},
     {"en": ("Real tokenizers cut « Luxembourg » into 2–3 pieces; the exact "
             "split varies per model — the one projected is illustrative."), "fr": "Les vrais tokenizers coupent « Luxembourg » en 2–3 morceaux ; le découpage exact varie selon le modèle — celui projeté est illustratif."}),
    ({"en": "Why fragments", "fr": "Pourquoi des fragments"},
     {"en": ("A fixed vocabulary of ~100 000 fragments covers every language "
             "and any new word — even « Schwëtzebuerg » gets pieces."), "fr": "Un vocabulaire fixe d’environ 100 000 fragments couvre toutes les langues et n’importe quel mot nouveau — même « Schwëtzebuerg » reçoit ses morceaux."}),
    ({"en": "Numbers, not text", "fr": "Des nombres, pas du texte"},
     {"en": ("Each fragment has an index in the vocabulary; the model computes "
             "on those numbers. All of G4's probabilities are per-token."), "fr": "Chaque fragment a un index dans le vocabulaire ; le modèle calcule sur ces nombres. Toutes les probabilités de G4 sont par jeton."}),
    ({"en": "Why you should care", "fr": "Pourquoi ça vous concerne"},
     {"en": ("Pricing, context limits (« 128k tokens »), and some silly "
             "mistakes (counting letters in a word) all come from tokens."), "fr": "La tarification, les limites de contexte (« 128k tokens ») et certaines erreurs bêtes (compter les lettres d’un mot) viennent toutes des jetons."}),
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
        # La phrase seule en scène, au centre de la fenêtre (règle amphi).
        st_space("v", f"{TUNING['drop_vh']}vh")
        with st_zoom(TUNING["sentence_zoom"]):
            st_write(bs.sentence, "« ", *TF(_SENTENCE, lang), " »", tag=t.div)
        st_space("v", "6vh")
        st_write(bs.caption, T(_CAPTION, lang), tag=t.div)
        st_space("v", "4vh")
        with st_zoom(130):
            for line in T(_PUNCH, lang):
                st_write(bs.punch, line, tag=t.div)
