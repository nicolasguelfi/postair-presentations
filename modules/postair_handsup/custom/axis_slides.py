"""Les trois gabarits d'axe du deck à main levée (plan-postair_handsup v2).

Un axe = trois pages, dans l'ordre du book : les 3 énoncés de chaque pôle,
la synthèse de chaque pôle, puis la slide de vote (l'échelle). Les blocs
d'axe sont MINCES : ils nomment un code d'instrument et un gabarit — un même
bloc listé neuf fois casserait marqueurs et TOC, d'où neuf blocs par gabarit.

Conventions reprises des decks existants :

- pôle ACCÉLÉRATEUR à gauche en carte bleue, décélérateur à droite en corail
  (convention d'affichage sumvadis, cf. ``postair_data`` et la slide
  « The instrument » de survey) ;
- les marqueurs restent en ANGLAIS quelle que soit la langue projetée : ce
  sont des ancres de navigation, pas du contenu — un marqueur qui change
  avec le sélecteur perdrait la TOC en pleine séance ;
- tous les textes viennent du gel (``custom.instrument``), rien à la main.
"""

from __future__ import annotations

from streamtex import *
from streamtex.enums import Tags as t

from custom.instrument import axis, lang, scale, synthesis
from custom.styles import Styles as s


class _S:
    title = s.project.titles.slide_title + s.center_txt
    pole = s.project.body.name_double + s.center_txt
    statement = s.project.body.bullet + s.center_txt + s.italic
    level = s.project.body.bullet + s.center_txt
    no_opinion = s.project.body.bullet + s.center_txt + s.project.colors.amber


def _title(ax: dict, *, toc_lvl: str | None = None, label: str | None = None) -> None:
    kwargs = {"toc_lvl": toc_lvl, "label": label} if toc_lvl else {}
    with st_zoom(130):
        st_write(_S.title, (s.project.titles.keyword, ax["name"][lang()]),
                 tag=t.div, **kwargs)


def _pole_cards(ax: dict, body) -> None:
    """Deux cartes pôles — ``body(pole)`` remplit l'intérieur sous le nom."""
    cards = [(s.project.cards.blue, ax["accel"]), (s.project.cards.coral, ax["decel"])]
    with st_grid(cols=s.project.grids.balanced(2, min_px=420), gap="2vw",
                 grid_style=s.project.grids.stretch,
                 cell_styles=s.project.containers.grid_cell_stretch) as g:
        for card, pole in cards:
            with g.cell(), st_block(card):
                with st_zoom(115):
                    st_write(_S.pole, pole["label"][lang()], tag=t.div)
                st_space("v", "1.5vh")
                body(pole)


def questions_slide(code: str) -> None:
    """Page 1 de l'axe : les 3 énoncés de chaque pôle. Porte l'ancre TOC."""
    ax = axis(code)
    st_marker(ax["name"]["en"])
    with st_block(s.project.containers.page_fill_top):
        _title(ax, toc_lvl="1", label=ax["name"]["en"])
        st_space("v", "2vh")

        def body(pole: dict) -> None:
            # 3 énoncés par carte : au corps « bullet » plein ils débordent
            # sous le pli (constaté à la 1re capture) — 70 % les fait tenir
            # tout en restant lisibles du fond de l'amphi.
            with st_zoom(70):
                for i, stmt in enumerate(pole["statements"]):
                    if i:
                        st_space("v", "1.5vh")
                    st_write(_S.statement, "“", stmt["text"][lang()], "”", tag=t.div)

        _pole_cards(ax, body)


def synthetic_slide(code: str) -> None:
    """Page 2 : UNE synthèse par pôle (champ amont v1.10.0 — bruyant avant)."""
    ax = axis(code)
    st_marker(f"{ax['name']['en']} — synthesis")
    with st_block(s.project.containers.page_fill_top):
        _title(ax)
        st_space("v", "3vh")

        def body(pole: dict) -> None:
            with st_zoom(125):
                st_write(_S.statement, "“", synthesis(pole)[lang()], "”", tag=t.div)

        _pole_cards(ax, body)


def scale_slide(code: str) -> None:
    """Page 3 : la slide de vote — même contenu pour les 9 axes, seul le
    titre (et le marqueur) porte l'axe.

    Gauche : pour, en intensité décroissante ; droite : contre, en intensité
    croissante ; dessous, la ligne « No opinion » — le découpage vient
    pré-fait du gel (``scale()``), le gabarit ne réordonne rien.
    """
    ax = axis(code)
    sc = scale()
    st_marker(f"{ax['name']['en']} — vote")
    with st_block(s.project.containers.page_fill_top):
        _title(ax)
        st_space("v", "3vh")
        with st_grid(cols=s.project.grids.balanced(2, min_px=420), gap="2vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_stretch) as g:
            for card, levels in [(s.project.cards.blue, sc["agree"]),
                                 (s.project.cards.coral, sc["disagree"])]:
                with g.cell(), st_block(card):
                    for i, level in enumerate(levels):
                        if i:
                            st_space("v", "1.5vh")
                        with st_zoom(120):
                            st_write(_S.level, level[lang()], tag=t.div)
        st_space("v", "3vh")
        with st_zoom(120):
            st_write(_S.no_opinion, sc["no_opinion"][lang()], tag=t.div)
