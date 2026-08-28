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
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


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

# ── Les trois ordres de grandeur (valeur projetée ; détail au survol) ───────
#: La jauge « Data » est un ordre de grandeur de notoriété publique, sans
#: source dédiée — sa liste de citekeys est vide.
_SLIDERS = [
    {
        "label": "Data",
        "value": "≈ the public web",
        "detail": ("Training corpora sample most of the accessible public "
                   "web, plus books and code."),
        "citekeys": [],
    },
    {
        "label": "Compute",
        "value": "×2.4 per year",
        "detail": ("The training compute cost of frontier models has grown "
                   "about 2.4× per year since 2016 — the largest runs cost "
                   "tens to hundreds of millions of euros."),
        "citekeys": ["cottier2024-costs"],
    },
    {
        "label": "Energy",
        "value": "≈ 1.5 % → ×2 by 2030",
        "detail": ("Data centres used about 1.5 % of world electricity in "
                   "2024; that could more than double by 2030, with AI as "
                   "the main driver."),
        "citekeys": ["iea2025-energy"],
    },
]

# ── L'émergence — la revendication ET son contrepoint, tous deux sourcés ────
_EMERGENCE_CLAIM = "Scale → capabilities NOBODY programmed"
_EMERGENCE_DETAIL = ("Abilities like multi-step arithmetic or translation "
                     "appear abruptly past certain scales — « emergent "
                     "abilities ».")
_EMERGENCE_COUNTERPOINT = "« mirage » debate open — measurement artefact?"
#: La source de la revendication ET celle du contrepoint — l'honnêteté est
#: la ligne du deck.
_EMERGENCE_CITEKEYS = ["wei2022-emergent", "schaeffer2023-mirage"]


def build(lang: str = "en", **_):
    st_marker("Scale")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, (s.project.titles.keyword, "Scale"),
                         " changes everything", tag=t.div, toc_lvl="+1", label="Scale")
            with g.cell():
                st_info_tooltip(
                    title="Orders of magnitude",
                    entries=[(sl["label"], sl["detail"]) for sl in _SLIDERS]
                            + [(_EMERGENCE_CLAIM,
                                _EMERGENCE_DETAIL + " "
                                + _EMERGENCE_COUNTERPOINT)],
                )
        st_space("v", s.project.spacing.title_gap)
        with st_grid(cols=s.project.grids.balanced(len(_SLIDERS)), gap="1.2vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for i, sl in enumerate(_SLIDERS):
                with g.cell(), st_block(s.project.cards.blue):
                    st_write(bs.gauge_label, sl["label"], tag=t.div)
                    # La jauge : un fût sombre, un remplissage teal qui monte.
                    st_html(f'<div style="height:18vh;width:3.2vw;margin:1vh auto;'
                            f'background:rgba(255,255,255,0.06);border-radius:1vw;'
                            f'display:flex;flex-direction:column;justify-content:flex-end;">'
                            f'<div style="height:{_GAUGE_HEIGHTS[i]};background:#2EC4B6;'
                            f'border-radius:1vw;"></div></div>')
                    st_write(bs.gauge_value, sl["value"], tag=t.div)
                    if sl["citekeys"]:
                        st_write(bs.cite, citation(*sl["citekeys"]), tag=t.div)
        st_space("v", "2.5vh")
        # La courbe d'émergence (plan G5) : plate, puis le saut — en ambre,
        # le seul accent chaud de la slide. Inline : trois traits suffisent.
        st_html('<div style="text-align:center;">'
                '<svg viewBox="0 0 600 110" style="width:34vw;max-width:60%;">'
                '<line x1="0" y1="100" x2="600" y2="100" stroke="#7AB8F5" '
                'stroke-opacity="0.4" stroke-width="2"/>'
                '<path d="M0 96 C 240 92, 330 88, 390 78 C 440 68, 470 20, 560 12" '
                'fill="none" stroke="#F39C12" stroke-width="6" stroke-linecap="round"/>'
                '</svg></div>')
        st_write(bs.claim, _EMERGENCE_CLAIM, " ",
                 citation(*_EMERGENCE_CITEKEYS), tag=t.div)
        st_write(bs.counter, _EMERGENCE_COUNTERPOINT, tag=t.div)
