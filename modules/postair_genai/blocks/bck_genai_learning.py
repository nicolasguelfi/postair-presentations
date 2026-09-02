"""How does it learn? (G3b) — le jeu de l'âge et la rétro-propagation.

Insertion draft des formations (planche drafts2 ``flux=intuition``, NG
2026-09-01, matériel back-propagation préféré aux boîtes-cadeaux — message NG
du même jour) : la marche conceptuelle qui manquait entre la frise (G3) et
Predict (G4) — ce que « apprendre » VEUT DIRE, joué avec la salle.

Six temps, UN marqueur (pattern debates, ``st_slide_break(marker_hidden=
True)``) :

1. le jeu — la salle devine l'âge de l'orateur depuis sa photo (elle sait
   faire : elle s'entraîne sur des visages depuis toujours) ;
2. la machine joue au même jeu — la photo devient un nombre, les fils
   portent des molettes (les POIDS) ;
3. premier essai — 245 ans : faux, et de loin ;
4. la correction — CHAQUE molette est poussée dans le sens qui réduit
   l'erreur : c'est la rétro-propagation ;
5. deuxième essai — 35 : plus près, le schéma seul en scène ;
6. la chute (scission NG 2026-09-01) — le raton « Piece of Cake » et le
   punch : répété des millions de fois, ça converge.

Les visuels sont la séquence pédagogique des formations AISE de NG
(``static/images/trainings/``, copyright NG, réutilisation autorisée
2026-09-01) — dessins d'auteur sur fond sombre, AUCUN n'est généré par IA :
pas de pastille DD-35. La photo est celle de l'orateur, de son propre
matériel.

Le FAIT vit ici (règle NG 2026-08-18) : chiffres du réseau-exemple (7, poids,
245/35/60) — illustratifs, cohérents avec les visuels, aucune affirmation
sourcée.

SPEAKER NOTES:
Four minutes, the room plays. FIRST SCREEN: « How old am I? » — wait, let
them shout, take three answers. Point out they never met you: they GUESS from
the picture because they trained on faces their whole life. PageDown — the
machine version: picture becomes numbers, dials on the wires. PageDown — read
the multiplication once, land on 245 vs 60: laugh WITH the machine. PageDown —
the only idea that matters today: every dial nudged in the direction that
reduces the error, that is back-propagation. PageDown — 35, closer. PageDown —
the raccoon closes it: error, correction, repeat, millions of times. Bridge:
« now replace “age” with “the next word” » — and PageDown into Predict.
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
    headline = s.project.titles.subtitle + s.center_txt
    cite = s.project.body.caption + s.center_txt
    verdict = s.project.titles.subtitle + s.project.colors.amber + s.center_txt + s.bold
    punch = s.project.titles.subtitle + s.project.colors.amber + s.center_txt


bs = BlockStyles

#: Réglages datés (pattern TUNING, revue genaipat) : hauteur de scène par
#: visuel — larges bandeaux ~2:1, la hauteur est la contrainte utile (R4d).
TUNING = {
    "stage_vh": 65,       # les 5 grands schémas du réseau (dont le 2e essai)
    "cake_vh": 60,        # la chute humoristique, temps 6 (raton pleine scène)
}

#: Ratio largeur/hauteur DU FICHIER (mesuré Pillow 2026-09-01) — les images
#: sont versionnées et figées, la mesure vit avec le choix du fichier.
_VISUALS = {
    "crowd":    ("images/trainings/learning_crowd.png",    2.042),
    "weights":  ("images/trainings/learning_weights.png",  2.118),
    "forward":  ("images/trainings/learning_forward.png",  1.979),
    "backprop": ("images/trainings/learning_backprop.png", 1.691),
    "retry":    ("images/trainings/learning_retry.png",    1.944),
    "cake":     ("images/trainings/learning_cake.png",     1.347),
}

# ── Les feuilles {en} du bloc ───────────────────────────────────────────────
_MARKER = {"en": "Learning"}
_TITLE = {"en": ("Let's play: ", (s.project.titles.keyword, "how old am I?"))}
_T1_LINE = {"en": "You never met me — yet you CAN guess"}
_T2_HEAD = {"en": ("The machine plays the same game — ",
                   (s.project.titles.keyword, "dials"), " on the wires")}
_T3_HEAD = {"en": ("First try: ", (s.project.titles.keyword, "245 years old"))}
_T3_LINE = {"en": "truth: 60 — wrong, and NOT by a little"}
_T4_HEAD = {"en": ("Every dial, nudged the right way = ",
                   (s.project.titles.keyword, "back-propagation"))}
_T5_HEAD = {"en": ("Second try: ", (s.project.titles.keyword, "35"), " — closer")}
_PUNCH = {"en": ("error → correction → repeat", "millions of examples later: it works")}

_ALT = {
    "crowd": "A photo of the speaker, a small crowd of stick figures, age: ???",
    "weights": "The photo encoded as the number 7, wires with weights toward one output",
    "forward": "The forward pass computed: prediction 245 against the true age 60",
    "backprop": "Each weight crossed out and nudged up or down by the error",
    "retry": "Second forward pass with nudged weights: prediction 35, closer to 60",
    "cake": "A raccoon making two peace signs, captioned Piece of Cake",
}

# ── Le panneau « the idea, precisely » ──────────────────────────────────────
_TIP_TITLE = {"en": "The idea, precisely"}
_TOOLTIP = [
    ({"en": "Encode"},
     {"en": ("A picture (or a text) becomes numbers — here one single number, "
             "7. Real systems use thousands of them per input.")}),
    ({"en": "Weights (the dials)"},
     {"en": ("Every wire carries a number that multiplies what passes through. "
             "The example network has 6 weights; a large language model has "
             "hundreds of BILLIONS.")}),
    ({"en": "Error"},
     {"en": ("Predicted 245, truth 60: the gap is measured, not judged. "
             "The machine never « knows » it is wrong — it computes a distance.")}),
    ({"en": "Back-propagation"},
     {"en": ("The error flows backwards through the network and every weight "
             "is nudged in the direction that reduces it. Rumelhart, Hinton "
             "and Williams made it practical in 1986 — it still trains "
             "every model you use today.")}),
    ({"en": "At scale"},
     {"en": ("Nudge billions of dials on billions of examples: nobody writes "
             "rules, the rules emerge from the corrections. That is machine "
             "« learning » — and the next slide plays it on words.")}),
]


def _stage(key: str, vh: int) -> None:
    """Le visuel borné par sa scène (R4d) : hauteur fixée, largeur = ratio."""
    uri, ratio = _VISUALS[key]
    with st_block(s.project.containers.media_stage(ratio, vh)):
        st_image(s.project.cards.media_center, uri=uri, alt=_ALT[key])


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    # ── Temps 1 : le jeu — la salle devine ──────────────────────────────────
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
        st_space("v", s.project.spacing.title_gap)
        _stage("crowd", TUNING["stage_vh"])
        st_space("v", "2vh")
        st_write(bs.headline, T(_T1_LINE, lang), tag=t.div)
    st_slide_break(marker_hidden=True)
    # ── Temps 2 : la machine — la photo devient un nombre, les molettes ─────
    with st_block(s.project.containers.page_fill_top):
        st_write(bs.headline, *TF(_T2_HEAD, lang), tag=t.div)
        st_space("v", s.project.spacing.title_gap)
        _stage("weights", TUNING["stage_vh"])
    st_slide_break(marker_hidden=True)
    # ── Temps 3 : premier essai — 245, faux et de loin ──────────────────────
    with st_block(s.project.containers.page_fill_top):
        st_write(bs.headline, *TF(_T3_HEAD, lang), tag=t.div)
        st_space("v", s.project.spacing.title_gap)
        _stage("forward", TUNING["stage_vh"])
        st_space("v", "2vh")
        st_write(bs.verdict, T(_T3_LINE, lang), tag=t.div)
    st_slide_break(marker_hidden=True)
    # ── Temps 4 : la rétro-propagation — chaque molette corrigée ────────────
    with st_block(s.project.containers.page_fill_top):
        st_write(bs.headline, *TF(_T4_HEAD, lang), tag=t.div)
        st_space("v", s.project.spacing.title_gap)
        _stage("backprop", TUNING["stage_vh"])
        st_space("v", "1vh")
        # Le fait daté (1986) porte son code de citation VISIBLE (règle bib
        # canonique) — la phrase complète vit dans la carte et References.
        st_write(bs.cite, citation("rumelhart1986-backprop"), tag=t.div)
    st_slide_break(marker_hidden=True)
    # ── Temps 5 : deuxième essai — le schéma seul, pleine scène ─────────────
    # (scission NG 2026-09-01 : le second try et la chute sur DEUX slides.)
    with st_block(s.project.containers.page_fill_top):
        st_write(bs.headline, *TF(_T5_HEAD, lang), tag=t.div)
        st_space("v", s.project.spacing.title_gap)
        _stage("retry", TUNING["stage_vh"])
    st_slide_break(marker_hidden=True)
    # ── Temps 6 : la chute — le raton-laveur et le punch ────────────────────
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_space("v", "1vh")
            with g.cell():
                # Autosuffisance du dernier temps (pattern debates) : l'en-tête
                # du temps 1 et son ℹ️ sont hors écran depuis longtemps.
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(T(h, lang), T(d, lang)) for h, d in _TOOLTIP],
                )
        _stage("cake", TUNING["cake_vh"])
        st_space("v", "3vh")
        with st_zoom(130):
            for line in T(_PUNCH, lang):
                st_write(bs.punch, line, tag=t.div)
