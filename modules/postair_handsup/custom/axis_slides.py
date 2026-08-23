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


#: Variante module-locale, même facture que les lavis du design system :
#: le lilas de la ligne PAPERCUT — troisième couleur de cellule, distincte
#: des deux couleurs d'identité de pôle (bleu accel / corail decel).
_LILAC_CELL = Style(
    "background-color: rgba(179, 157, 219, 0.10); border-left: 4px solid #B39DDB; "
    "border-radius: 12px; padding: 2vh 1.5vw;",
    "handsup_card_lilac",
)

#: UNE cellule par question (NG 2026-08-23) : couleurs par POSITION,
#: identiques sur les deux colonnes et sur les neuf axes — la salle peut
#: dire « la jaune ». Les en-têtes de pôle gardent bleu/corail.
_CELL_CARDS = [s.project.cards.teal, _LILAC_CELL, s.project.cards.amber]

#: Slides de synthèse : une cellule par pôle, deux couleurs fixes (les mêmes
#: sur les neuf axes), prises dans la même palette de cellules.
_SYNTH_CARDS = {"accel": s.project.cards.teal, "decel": s.project.cards.amber}


def _pole_columns(ax: dict, cells) -> None:
    """Deux colonnes : en-tête de pôle (bleu/corail), puis les cellules.

    ``cells(pole, kind)`` rend la liste ``[(carte, énoncé), …]`` — le gabarit
    ne décide pas du contenu, seulement de l'empilement.
    """
    columns = [(s.project.cards.blue, "accel"), (s.project.cards.coral, "decel")]
    with st_grid(cols=s.project.grids.balanced(2, min_px=420), gap="2vw",
                 grid_style=s.project.grids.stretch,
                 cell_styles=s.project.containers.grid_cell_stretch) as g:
        for header, kind in columns:
            pole = ax[kind]
            with g.cell():
                with st_block(header), st_zoom(100):
                    st_write(_S.pole, pole["label"][lang()], tag=t.div)
                for card, text, zoom in cells(pole, kind):
                    st_space("v", "1.2vh")
                    with st_block(card), st_zoom(zoom):
                        st_write(_S.statement, "“", text, "”", tag=t.div)


def questions_slide(code: str) -> None:
    """Page 1 de l'axe : les 3 énoncés de chaque pôle, une cellule chacun.

    Zoom 70 : au corps « bullet » plein les trois cellules débordent sous le
    pli (constaté à la 1re capture de la version en carte unique).
    """
    ax = axis(code)
    st_marker(ax["name"]["en"])
    with st_block(s.project.containers.page_fill_top):
        _title(ax, toc_lvl="1", label=ax["name"]["en"])
        st_space("v", "2vh")
        _pole_columns(ax, lambda pole, _kind: [
            (_CELL_CARDS[i], stmt["text"][lang()], 70)
            for i, stmt in enumerate(pole["statements"])])


#: La colonne d'un pôle seule au centre de la slide : pleine largeur elle
#: étirerait les lignes au-delà du confort de lecture d'amphi.
_POLE_COLUMN = Style(
    "max-width: 62vw; margin-left: auto; margin-right: auto;",
    "handsup_pole_column",
)


def _axis_pair_title(ax: dict) -> None:
    """Le titre au format NG 2026-08-23 : Axis "Trust / Self-reliance"."""
    pair = f"{ax['accel']['label'][lang()]} / {ax['decel']['label'][lang()]}"
    with st_zoom(115):
        st_write(_S.title, "Axis “", (s.project.titles.keyword, pair), "”",
                 tag=t.div)


def pole_synthesis_slide(code: str, kind: str) -> None:
    """La slide d'UN pôle (décision NG 2026-08-23 : vote PAR PÔLE).

    Remplace la synthèse à deux colonnes dans le book : chaque pôle ouvre sa
    propre séquence de vote. Titre = la paire de pôles de l'axe ; dessous, la
    colonne actuelle de CE pôle, seule et en grand — mêmes couleurs (en-tête
    bleu/corail, cellule teal/ambre).
    """
    ax = axis(code)
    pole = ax[kind]
    st_marker(f"{pole['label']['en']} — synthesis")
    with st_block(s.project.containers.page_fill_top):
        _axis_pair_title(ax)
        st_space("v", "4vh")
        header = s.project.cards.blue if kind == "accel" else s.project.cards.coral
        with st_block(_POLE_COLUMN):
            with st_block(header), st_zoom(120):
                st_write(_S.pole, pole["label"][lang()], tag=t.div)
            st_space("v", "1.5vh")
            with st_block(_SYNTH_CARDS[kind]), st_zoom(135):
                st_write(_S.statement, "“", synthesis(pole)[lang()], "”",
                         tag=t.div)


# ── Les trois slides de vote — VRAIMENT génériques (NG 2026-08-24) ──────────
#
# Trois blocs, listés dix-huit fois chacun dans le book : l'ancre d'un
# marqueur embarque l'index du registre (``stx-marker-<slug>-<idx>``), un
# libellé répété ne collisionne donc jamais — la première conception qui
# répliquait 54 blocs par peur de la collision était fausse (NG l'a vue).
# Les marqueurs sont CACHÉS (``hidden=True``) : les flèches traversent
# chaque occurrence, la barre latérale ne liste que les slides porteuses
# (axes et pôles). Même schéma pour les trois : illustration PAPERCUT à
# gauche, valeurs de l'échelle à droite (gel, découpage pré-fait).

from custom.prompts import AI_PREFIX, AI_SUFFIX_LANDSCAPE  # noqa: E402
from custom.visuals import hero_image  # noqa: E402

_VOTE_FALLBACK = "images/postair_radar_question.svg"

#: Par volet : (mot-clé du titre, carte, nom managé, scène PAPERCUT).
_VOTE_PROMPTS = {
    "support": (
        "A cheerful crowd of abstract paper silhouettes seen from behind, "
        "every arm raised high in enthusiastic approval, open cut-paper "
        "hands reaching toward a warm glowing amber paper sun, bright "
        "turquoise and leaf-green cardstock sky."),
    "oppose": (
        "A calm crowd of abstract paper silhouettes seen from behind, arms "
        "crossed or palms raised gently forward in polite refusal, coral "
        "and lilac cardstock sky, a warm amber paper sun low on the "
        "horizon."),
    "abstain": (
        "A relaxed crowd of abstract paper silhouettes seen from behind, "
        "hands in pockets or shrugging softly, standing a step back from "
        "the scene, soft lilac and pale-yellow cardstock, a warm amber "
        "paper sun half hidden behind a paper cloud."),
}


def _vote_prompt(kind: str) -> str:
    return AI_PREFIX + _VOTE_PROMPTS[kind] + AI_SUFFIX_LANDSCAPE


def _vote_slide(*, kind: str, keyword: str, card,
                levels: list[dict], alt_ready: str) -> None:
    """Le schéma commun des trois volets : image à gauche, valeurs à droite."""
    st_marker(f"Vote — {keyword}", hidden=True)
    with st_block(s.project.containers.page_fill_top):
        with st_zoom(130):
            st_write(_S.title, "Vote: ", (s.project.titles.keyword, keyword),
                     tag=t.div)
        st_space("v", "3vh")
        with st_grid(cols="46% 54%", gap="2vw",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                hero_image(f"vote_{kind}", _vote_prompt(kind),
                           fallback=_VOTE_FALLBACK,
                           alt_ready=alt_ready,
                           alt_fallback=("Empty nine-axis POSTAIR radar chart "
                                         "with a question mark in the centre"),
                           width="88%", variant="sq")
            with g.cell(), st_block(card):
                for i, level in enumerate(levels):
                    if i:
                        st_space("v", "2.5vh")
                    with st_zoom(135):
                        st_write(_S.level, level[lang()], tag=t.div)


def vote_support_slide() -> None:
    """Volet 1 : les trois réponses EN FAVEUR, intensité décroissante."""
    _vote_slide(kind="support", keyword="I support",
                card=s.project.cards.blue, levels=scale()["agree"],
                alt_ready=("Papercut crowd with every arm raised high in "
                           "enthusiastic approval under an amber paper sun"))


def vote_oppose_slide() -> None:
    """Volet 2 : les trois réponses EN DÉFAVEUR, intensité croissante."""
    _vote_slide(kind="oppose", keyword="I oppose",
                card=s.project.cards.coral, levels=scale()["disagree"],
                alt_ready=("Papercut crowd with arms crossed or palms raised "
                           "gently forward in polite refusal"))


def vote_abstain_slide() -> None:
    """Volet 3 : la réponse de qui ne souhaite pas se prononcer."""
    _vote_slide(kind="abstain", keyword="no opinion",
                card=s.project.cards.amber, levels=[scale()["no_opinion"]],
                alt_ready=("Papercut crowd standing back with hands in "
                           "pockets, an amber paper sun behind a cloud"))
