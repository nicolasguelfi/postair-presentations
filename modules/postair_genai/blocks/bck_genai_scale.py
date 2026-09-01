"""Scale changes everything (G5) — data + compute + parameters, and emergence.

Three rising gauges and one emergence line. The sourced orders of magnitude
carry their citation codes in the visible text (full reference on hover); the
controversies live in the tooltip AND on the slide — the counterpoint is
projected, not hidden, house style since the opening deck.

Le FAIT vit ici (règle NG 2026-08-18) : jauges, ligne d'émergence et choix
des citekeys s'éditent dans ce bloc. La phrase bibliographique reste dérivée
de ``references.bib`` par ``citation()``/``cite`` — clé inconnue = erreur
bruyante.

SPEAKER NOTES:
Two minutes. The three gauges are one sentence each; the sentence that matters
is the amber one — capabilities nobody programmed appear with scale — and its
honest counterpoint: part of that abruptness may be an artefact of how we
measure. Both are sourced, hover the codes if challenged.
"""
# @guideline: postair-minimal

from custom.refs import citation
from custom.styles import Styles as s
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.design_systems.postair_dark import AMBER, KEYWORD, PRIMARY


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    gauge_label = s.project.body.bullet + s.center_txt + s.bold
    gauge_value = s.project.titles.subtitle + s.project.colors.keyword + s.center_txt
    cite = s.project.body.caption + s.center_txt
    claim = s.project.titles.subtitle + s.project.colors.amber + s.center_txt
    counter = s.project.body.caption + s.center_txt


bs = BlockStyles

#: Trois jauges qui montent — la hauteur dit « plus », pas une mesure.
_GAUGE_HEIGHTS = ["52%", "72%", "92%"]

#: Le fût et son remplissage teal — compositions de ``Style`` (R11, revue
#: genaipat 2026-09-01 : l'ancien st_html portait le teal en dur).
_GAUGE_TUBE = Style(
    "height: 18vh; width: 3.2vw; margin: 1vh auto; "
    "background: rgba(255,255,255,0.06); border-radius: 1vw; "
    "display: flex; flex-direction: column; justify-content: flex-end;",
    "genai_gauge_tube",
)


def _gauge_fill(height: str, idx: int) -> Style:
    return Style(
        f"height: {height}; background: {KEYWORD}; border-radius: 1vw;",
        f"genai_gauge_fill_{idx}",
    )

# ── Les trois ordres de grandeur (valeur projetée ; détail au survol) ───────
#: La jauge « Data » est un ordre de grandeur de notoriété publique, sans
#: source dédiée — sa liste de citekeys est vide.
_SLIDERS = [
    {
        "label": {"en": "Data"},
        "value": {"en": "≈ the public web"},
        "detail": {"en": ("Training corpora sample most of the accessible public "
                          "web, plus books and code.")},
        "citekeys": [],
    },
    {
        "label": {"en": "Compute"},
        "value": {"en": "×2.4 per year"},
        "detail": {"en": ("The training compute cost of frontier models has grown "
                          "about 2.4× per year since 2016 — the largest runs cost "
                          "tens to hundreds of millions of euros.")},
        "citekeys": ["cottier2024-costs"],
    },
    {
        "label": {"en": "Energy"},
        "value": {"en": "≈ 1.5 % → ×2 by 2030"},
        "detail": {"en": ("Data centres used about 1.5 % of world electricity in "
                          "2024; that could more than double by 2030, with AI as "
                          "the main driver.")},
        "citekeys": ["iea2025-energy"],
    },
]

# ── L'émergence — la revendication ET son contrepoint, tous deux sourcés ────
_EMERGENCE_CLAIM = {"en": "Scale → capabilities NOBODY programmed"}
_EMERGENCE_DETAIL = {"en": ("Abilities like multi-step arithmetic or translation "
                            "appear abruptly past certain scales — « emergent "
                            "abilities ».")}
_EMERGENCE_COUNTERPOINT = {"en": "« mirage » debate open — measurement artefact?"}

# ── Les feuilles {en} du bloc (structure i18n, lot C genaipat 2026-09-01) ────
_MARKER = {"en": "Scale"}
_TITLE = {"en": ((s.project.titles.keyword, "Scale"), " changes everything")}
_TIP_TITLE = {"en": "Orders of magnitude"}
#: La source de la revendication ET celle du contrepoint — l'honnêteté est
#: la ligne du deck.
_EMERGENCE_CITEKEYS = ["wei2022-emergent", "schaeffer2023-mirage"]


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
                    entries=[(T(sl["label"], lang), T(sl["detail"], lang))
                             for sl in _SLIDERS]
                            + [(T(_EMERGENCE_CLAIM, lang),
                                T(_EMERGENCE_DETAIL, lang) + " "
                                + T(_EMERGENCE_COUNTERPOINT, lang))],
                )
        st_space("v", s.project.spacing.title_gap)
        with st_grid(cols=s.project.grids.balanced(len(_SLIDERS)), gap="1.2vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for i, sl in enumerate(_SLIDERS):
                with g.cell(), st_block(s.project.cards.blue):
                    st_write(bs.gauge_label, T(sl["label"], lang), tag=t.div)
                    # La jauge : un fût sombre, un remplissage teal qui monte.
                    with st_block(_GAUGE_TUBE):
                        with st_block(_gauge_fill(_GAUGE_HEIGHTS[i], i)):
                            pass
                    st_write(bs.gauge_value, T(sl["value"], lang), tag=t.div)
                    if sl["citekeys"]:
                        st_write(bs.cite, citation(*sl["citekeys"]), tag=t.div)
        st_space("v", "2.5vh")
        # La courbe d'émergence (plan G5) : plate, puis le saut — en ambre,
        # le seul accent chaud de la slide. EXCEPTION R11 ASSUMÉE (revue
        # genaipat 2026-09-01) : un tracé SVG n'a pas d'équivalent en
        # composition stx — le fragment reste, mais ses couleurs sont les
        # jetons de la palette, plus aucun hex en dur.
        st_html(f'<div style="text-align:center;">'
                f'<svg viewBox="0 0 600 110" style="width:34vw;max-width:60%;">'
                f'<line x1="0" y1="100" x2="600" y2="100" stroke="{PRIMARY}" '
                f'stroke-opacity="0.4" stroke-width="2"/>'
                f'<path d="M0 96 C 240 92, 330 88, 390 78 C 440 68, 470 20, 560 12" '
                f'fill="none" stroke="{AMBER}" stroke-width="6" stroke-linecap="round"/>'
                f'</svg></div>')
        st_write(bs.claim, T(_EMERGENCE_CLAIM, lang), " ",
                 citation(*_EMERGENCE_CITEKEYS), tag=t.div)
        st_write(bs.counter, T(_EMERGENCE_COUNTERPOINT, lang), tag=t.div)
