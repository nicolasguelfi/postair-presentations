"""If misuse is suspected (U7).

One dominant papercut image (the balanced scale of justice — balanced, unlike
the bias slide of the GenAI session) and three cards: standard procedure,
detection is not proof (sourced, citation codes visible), your process
protects you.

Le FAIT vit ici (règle NG 2026-08-18) : la ligne des garanties, les trois
cartes et le choix des citekeys s'éditent dans ce bloc. La phrase
bibliographique reste dérivée de ``references.bib`` par ``citation()`` — clé
inconnue = erreur bruyante.

SPEAKER NOTES:
One minute, reassuring: the procedure is the standard one, solid evidence is
required, and a « detector » alone is never enough — the sources behind that
sentence are one hover away. The practical takeaway is the third card: keep
your drafts and prompts, showing your process is your best defence.
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
    short = s.project.body.caption + s.center_txt + s.bold
    line = s.project.body.bullet + s.project.colors.amber + s.center_txt + s.bold
    cite = s.project.body.caption + s.center_txt


bs = BlockStyles

_MARKER = {"en": "If suspected", "fr": "En cas de soupçon"}
_TITLE = {"en": ("If misuse is ", (s.project.titles.keyword, "suspected")), "fr": ("Si un mésusage est ", (s.project.titles.keyword, "soupçonné"))}
_TIP_TITLE = {"en": "The procedure (guidelines, section 4)", "fr": "La procédure (lignes directrices, section 4)"}

# ── Le fait : la procédure en cas de soupçon (guidelines, section 4) ────────
#: La ligne des garanties, projetée en quatre puces (split sur « · »).
_LINE = {"en": ("Standard procedure · Solid evidence required · A detector alone "
                "≠ proof · Your rights protected"), "fr": ("Procédure standard · Des preuves solides exigées · Un détecteur seul ≠ preuve · Vos droits protégés")}
#: « short » titre l'entrée du tooltip ; « detail » en est le corps.
_CARDS = [
    {"icon": "⚖️", "short": {"en": "Standard procedure", "fr": "Procédure standard"},
     "detail": {"en": ("The existing UL academic-conduct procedure applies — these "
                       "guidelines create no new tribunal."), "fr": "La procédure disciplinaire existante de l'UL s'applique — ces lignes directrices ne créent aucun tribunal nouveau."}},
    {"icon": "🚫", "short": {"en": "Detection is not proof", "fr": "Détecter n'est pas prouver"},
     "detail": {"en": ("A presumed « AI detection » is not a sufficient basis: "
                       "detectors are unreliable and biased against non-native "
                       "writers."), "fr": "Une « détection d'IA » présumée n'est pas une base suffisante : les détecteurs sont peu fiables et biaisés contre les non-natifs."}},
    {"icon": "🛡️", "short": {"en": "Your process protects you", "fr": "Votre processus vous protège"},
     "detail": {"en": ("Drafts, prompts, versions: showing your process is your "
                       "best defence — one more reason to keep them."), "fr": "Brouillons, prompts, versions : montrer votre processus est votre meilleure défense — une raison de plus de les garder."}},
]
_CITEKEYS = ["i2tl2026-guidelines", "liang2023-bias", "giray-detectors-2026"]
#: Jamais projeté, gardé pour la vérifiabilité (entrée « big » de l'ancien
#: facts.json) : « If misuse is suspected ».

_BALANCE_PROMPT = (
    AI_PREFIX
    + "A perfectly balanced paper scale of justice standing on a small paper "
      "pedestal, both pans level, in front of a calm luminous paper sky; a "
      "small warm amber paper orb rests gently in one pan, a stack of small "
      "paper documents of equal weight in the other."
    + AI_SUFFIX_LANDSCAPE
)


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
                    entries=[(f"{c['icon']} {T(c['short'], lang)}", T(c["detail"], lang))
                             for c in _CARDS],
                )
        st_space("v", s.project.spacing.title_gap)
        # Gabarit par défaut (NG 2026-08-13) : balance carrée à gauche, les
        # quatre garanties EMPILÉES à droite (le pavé d'une seule ligne se
        # lisait comme un paragraphe).
        with hero_split(s, image=lambda: hero_image(
                "guide_balance", _BALANCE_PROMPT,
                "images/guide_balance_fallback.svg",
                alt_ready=("Papercut balanced scale of justice, an amber orb in one "
                           "pan and documents in the other, calm sky"),
                alt_fallback=("Papercut balanced scale of justice"),
                variant="sq")):
            for part in T(_LINE, lang).split(" · "):
                st_write(bs.line, "▸ ", part, tag=t.div)
            st_space("v", "0.5vh")
            st_write(bs.cite, citation(*_CITEKEYS), tag=t.div)
