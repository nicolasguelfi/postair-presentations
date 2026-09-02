"""What it can do today (G6) — seven capabilities, agents in amber.

A grid of seven picto cards, one word each; the dated, sourced example behind
every capability lives in the tooltip. « Agents » is the single amber card of
the slide — it is the teaser for the Mistral session.

Le FAIT vit ici (règle NG 2026-08-18) : capacités, exemples datés, exemples
par faculté et choix des citekeys s'éditent dans ce bloc. La phrase
bibliographique reste dérivée de ``references.bib`` par
``citation()``/``cite`` — clé inconnue = erreur bruyante.

SPEAKER NOTES:
Three minutes. One capability, one spoken example — the info panel has one per
faculty if the room needs it closer to home. Finish on the amber card and
plant the flag: « an agent is a model that uses tools in a loop to pursue a
goal — in the next session you will build one, live ».
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
    icon = s.project.titles.subtitle + s.center_txt
    label = s.project.body.bullet + s.center_txt + s.bold
    cite = s.project.body.caption + s.center_txt


bs = BlockStyles

# ── Les sept capacités (carte projetée ; exemple daté au survol) ────────────
#: Jamais projeté, gardé pour la vérifiabilité — les identifiants d'origine
#: des capacités : write, translate, code, summarise, create, reason, act.
#: Seule « Write » porte une source (essai contrôlé) ; les autres exemples
#: sont télégraphiques, sans citekey — leur liste est vide.
_CAPABILITIES = [
    {
        "icon": "✍️",
        "label": {"en": "Write"},
        "example": {"en": "Writing: ~40 % faster (controlled trial)"},
        "citekeys": ["noy-zhang-2023"],
    },
    {
        "icon": "🌍",
        "label": {"en": "Translate"},
        "example": {"en": "~100 languages · Lëtzebuergesch: imperfect"},
        "citekeys": [],
    },
    {
        "icon": "💻",
        "label": {"en": "Code"},
        "example": {"en": "Sentence → program · explains others' code"},
        "citekeys": [],
    },
    {
        "icon": "📚",
        "label": {"en": "Summarise"},
        "example": {"en": "60 pages → 1 · risk: THE nuance lost"},
        "citekeys": [],
    },
    {
        "icon": "🎨",
        "label": {"en": "Create media"},
        "example": {"en": "Text → image / music / video · this deck: 100 % generated"},
        "citekeys": [],
    },
    {
        "icon": "🧩",
        "label": {"en": "Reason\n(a bit)"},
        "example": {"en": "Reasoning ↑ fast · unverified: fragile"},
        "citekeys": [],
    },
    {
        "icon": "⚡",
        "label": {"en": "Act — agents"},
        "example": {"en": "Agents = tools in a loop → Mistral session"},
        "citekeys": [],
        "accent": True,   # LA carte ambre — le teaser de la session Mistral.
    },
]

# ── Un exemple par faculté (panneau uniquement, plan G6) ────────────────────
_FACULTY_EXAMPLES = [
    ({"en": "Science & engineering"},
     {"en": ("Code assistants draft, test and explain programs — the FSTM way in: "
             "build with it, then break it to understand it.")}),
    ({"en": "Law, economics, finance"},
     {"en": ("Contract review and case-law search accelerate massively — and G7 "
             "shows why a jurist verifies every citation it returns.")}),
    ({"en": "Humanities, education, social sciences"},
     {"en": ("Transcription, translation and thematic coding of interviews — the "
             "analysis and the interpretation stay the researcher's.")}),
]

# ── Les feuilles {en} du bloc (structure i18n, lot C genaipat 2026-09-01) ────
_MARKER = {"en": "What it can do"}
_TITLE = {"en": ("What it ", (s.project.titles.keyword, "can do"), " today")}
_TIP_TITLE = {"en": "One dated example each"}


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
                    entries=[(f"{c['icon']} {T(c['label'], lang)}",
                              T(c["example"], lang))
                             for c in _CAPABILITIES]
                            # Un exemple par faculté (plan G6) : chaque tiers
                            # de la salle se reconnaît dans au moins un.
                            + [(T(h, lang), T(d, lang))
                               for h, d in _FACULTY_EXAMPLES],
                )
        st_space("v", s.project.spacing.title_gap)
        # Sept cartes sur une grille équilibrée ; « agents » est LA carte ambre.
        with st_grid(cols=s.project.grids.balanced(len(_CAPABILITIES)), gap="1vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for c in _CAPABILITIES:
                with st_zoom(130), g.cell(), st_block(s.project.cards.amber if c.get("accent")
                                        else s.project.cards.blue):
                    st_write(bs.icon, c["icon"], tag=t.div)
                    # Une écriture PAR ligne : ``st_write`` n'interprète pas
                    # le ``\n`` (piège documenté au PLAYBOOK) — la retouche NG
                    # « Reason\n(a bit) » (2026-09-01) obtient ainsi sa vraie
                    # coupure de ligne.
                    for line in T(c["label"], lang).split("\n"):
                        st_write(bs.label, line, tag=t.div)
                    if c["citekeys"]:
                        st_write(bs.cite, citation(*c["citekeys"]), tag=t.div)
