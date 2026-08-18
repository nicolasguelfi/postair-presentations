"""Gabarit « un chiffre par slide » — la série A revolution already here.

Découpage NG (2026-08-13, 1 idée = 1 slide) : l'ancienne grille 2×2 coupait
sa rangée basse au pli et projetait huit phrases. Chaque chiffre a maintenant
SA slide : la valeur en très grand (ambre — LE point focal), la lecture
télégraphique, le contrepoint corail (l'honnêteté reste À CÔTÉ du chiffre),
l'attribution + code de citation. Le dernier chiffre porte aussi la ligne
« long-wave » qui fermait l'ancienne slide.

Écrire le gabarit une fois, un bloc mince par chiffre — le pattern
``limit_slide`` de postair_genai.
"""

from __future__ import annotations

from shared_widgets import st_info_tooltip
from streamtex import st_block, st_grid, st_marker, st_space, st_write, st_zoom
from streamtex.enums import Tags as t

from custom.facts import citekeys, figures, framing, text
from custom.refs import citation
from custom.styles import Styles as s


class SlideStyles:
    title = s.project.titles.slide_title + s.center_txt
    value = s.project.titles.register_title + s.center_txt
    claim = s.project.body.bullet_giant + s.center_txt
    counterpoint = s.project.body.bullet + s.project.colors.coral + s.center_txt
    attribution = s.project.body.caption + s.center_txt
    closing = s.project.titles.subtitle + s.project.colors.amber + s.center_txt


ss = SlideStyles

#: Un marqueur court par chiffre, dans l'ordre des données.
_MARKERS = ["94 %", "−40 %", "61 %", "68 %"]


def build_already(index: int , zoom: int = 100) -> None:
    """One measured figure, huge — with its counterpoint beside it."""
    figure = figures()[index]
    st_marker(_MARKERS[index])
    with st_zoom(zoom):
        with st_block(s.project.containers.page_fill_top):
            with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
                with g.cell():
                    st_write(ss.title, "Already here — ",
                            (s.project.titles.keyword,
                            text(figure["source"].get("attribution"))),
                            tag=t.div, toc_lvl="+1", label=_MARKERS[index])
                with g.cell():
                    parts = [text(figure["claim"]) + ".",
                            text(figure["population"]) + "."]
                    for key in ("trend", "freshness", "counterpoint", "caveat"):
                        if figure.get(key):
                            parts.append(text(figure[key]))
                    st_info_tooltip(title="Where this figure comes from",
                                    entries=[(text(figure["value"]), " ".join(parts))])
            st_space("v", s.project.spacing.title_gap)
            st_write(ss.value, text(figure["value"]), tag=t.div)
            st_space("v", "1vh")
            st_write(ss.claim, text(figure["claim"]), tag=t.div)
            st_space("v", "2vh")
            st_write(ss.counterpoint, text(figure["counterpoint"]["short"]), tag=t.div)
            st_space("v", "1vh")
            st_write(ss.attribution, text(figure["source"].get("attribution")), " ",
                    citation(*citekeys(figure)), tag=t.div)
            if index == len(figures()) - 1:
                long_view = framing("long-wave")
                st_space("v", "2vh")
                st_write(ss.closing, text(long_view["headline"]), " ",
                        citation(*citekeys(long_view)), tag=t.div)
