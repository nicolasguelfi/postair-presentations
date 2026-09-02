"""And for your studies — the exam stays human (G9b).

Le versant exigeant du découpage : l'orbe attend derrière la porte de la
salle d'examen, et le paradoxe ferme la slide en ambre. Le chiffre HEPI porte
son code de citation visible.

Le FAIT vit ici (règle NG 2026-08-18) : les trois mises en garde, le paradoxe
et le choix des citekeys s'éditent dans ce bloc (le versant positif vit dans
``bck_genai_studies_tutor`` — entrées disjointes de l'ancienne section
« studies »). La phrase bibliographique reste dérivée de ``references.bib``
par ``citation()``/``cite`` — clé inconnue = erreur bruyante.

SPEAKER NOTES:
Ninety seconds, slower than the previous slide. Read the amber paradox line
once, let it sit. The 94 % is not an accusation — it says the question is HOW,
not whether. Bridge: Mistral shows the how, the guidelines give the rules.
"""
# @guideline: postair-minimal

from custom.prompts import AI_PREFIX, AI_SUFFIX_LANDSCAPE
from custom.refs import citation
from custom.styles import Styles as s
from custom.visuals import staged_hero_image
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.hero_split import hero_split


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    item = s.project.body.bullet + s.center_txt
    paradox = s.project.titles.subtitle + s.project.colors.amber + s.center_txt


bs = BlockStyles

_EXAM_PROMPT = (
    AI_PREFIX
    + "An exam room made of paper: one abstract paper silhouette seen from "
      "behind, writing alone at a small paper desk, a paper wall clock above "
      "— and outside the closed paper door, waiting patiently in the "
      "corridor, a warm amber paper orb."
    + AI_SUFFIX_LANDSCAPE
)

# ── Les trois mises en garde — réécriture pédagogique (formulations NG,
# planches examped/examped2, 2026-09-02) : chaque ligne a un acteur et une
# conséquence, décodable SEULE. Choix rhétorique ASSUMÉ par NG sur la 3e :
# « for the good » et « +300 % » projetés SANS les chiffres bruts (3→12 %) —
# la précision complète vit au panneau et dans la note .bib (les 94 % sont
# l'usage TOTAL ; +300 % = ×4 ; l'analyse R-facts versée à la planche,
# décision d'auteur par-dessus). Les \n des feuilles = vraies coupures
# (une écriture par ligne, piège st_write du PLAYBOOK).
_DONT = [
    {"en": "The exam tests YOUR skill — Not the AI"},
    {"en": "Skip the effort → the skill never forms"},
    {"en": "94 % UK already use it for the good\nBUT bad usage has\ngrown by 300% since 2024"},
]
_DONT_CITEKEYS = ["hepi-survey-2026"]

#: Une couleur de palette par mise en garde (demande NG 2026-09-02, même
#: geste que les puces du tuteur G9a) : bleu électrique, teal, corail —
#: l'AMBRE reste réservé à la carte du paradoxe qui ferme la slide.
_DONT_COLOURS = [s.project.colors.primary, s.project.colors.keyword,
                 s.project.colors.coral]

# ── Le paradoxe — LE message de la slide (formulation NG, grow/shrink) ──────
_PARADOX = {"en": "Learn WITH it → you grow\nlet it REPLACE you\n→ you shrink"}

_MARKER = {"en": "The exam"}
_TITLE = {"en": ("The exam stays ", (s.project.titles.keyword, "human"))}
_TIP_TITLE = {"en": "Tutor, not ghostwriter"}
_TOOLTIP = [
    ({"en": "How to prove the work is yours"},
     {"en": ("Graders look at your PROCESS: drafts, prompts, versions, "
             "choices. Keep them — they are your signature.")}),
    ({"en": "The paradox, in full"},
     {"en": ("The same tool that multiplies learning when it assists you "
             "cancels it when it replaces you. The exam room is where the "
             "difference shows.")}),
    ({"en": "The numbers, precisely"},
     {"en": ("HEPI 2026 (1054 UK undergraduates): 94 % use generative AI in "
             "some form; directly pasting AI text into GRADED work rose from "
             "3 % (2024) to 8 % (2025) to 12 % (2026) — that is the "
             "« +300 % » on screen, a fourfold rise.")}),
    ({"en": "Why exams stay AI-free"},
     {"en": ("Assessment is being redesigned in three regimes — AI-free, "
             "AI-assisted, AI-integrated. The AI-free room measures what "
             "remains when the tool is gone.")}),
]

# ── La main de l'artiste (pattern TUNING debates, revue genaipat 2026-09-01) ─
#: Les réglages visuels de la slide vivent ICI, nommés et commentés — jamais
#: en littéral anonyme au point d'appel. ``zoom`` = paramètre ``zoom=`` du
#: hero_split (réglage préexistant à la revue, motif non consigné — à
#: confirmer à la repasse visuelle NG).
TUNING = {
    "zoom": 92,
}


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
                    entries=[(T(h, lang), T(d, lang)) for h, d in _TOOLTIP],
                )
        st_space("v", s.project.spacing.title_gap)
        with hero_split(s, zoom=TUNING["zoom"], image=lambda: staged_hero_image(
                "genai_exam", _EXAM_PROMPT, "images/genai_exam_fallback.svg",
                alt_ready=("Papercut exam room: a silhouette writing alone at a "
                           "desk, an amber orb waiting outside the closed door"),
                alt_fallback=("Papercut exam room, silhouette writing, amber orb "
                              "waiting behind the closed door"),
                variant="pt")):
            # Une écriture PAR ligne (st_write ignore le \n) : puces × lignes,
            # UN seul corps (simplification NG 2026-09-02) — le « ▸ » n'orne
            # que la 1re ligne d'une puce, le code HEPI ne s'accroche qu'à la
            # toute dernière ligne de la dernière puce ; le zoom 120 (retouche
            # NG) couvre TOUTES les lignes uniformément.
            with st_zoom(120):
                for i, (item, colour) in enumerate(zip(_DONT, _DONT_COLOURS)):
                    lines = T(item, lang).split("\n")
                    for j, line in enumerate(lines):
                        prefix = ("▸ ",) if j == 0 else ()
                        very_last = (i == len(_DONT) - 1
                                     and j == len(lines) - 1)
                        cite = ((" ", citation(*_DONT_CITEKEYS))
                                if very_last else ())
                        st_write(bs.item + colour, *prefix, line, *cite,
                                 tag=t.div)
            st_space("v", "1vh")
            # Le paradoxe — LE message de la slide — en carte ambre, VISIBLE,
            # sur DEUX lignes (formulation NG grow/shrink).
            with st_block(s.project.cards.amber):
                for line in T(_PARADOX, lang).split("\n"):
                    st_write(bs.paradox, line, tag=t.div)
