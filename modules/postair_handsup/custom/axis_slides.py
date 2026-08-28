"""Les trois gabarits d'axe du deck à main levée (plan-postair_handsup v2).

Un axe = trois pages, dans l'ordre du book : les 3 énoncés de chaque pôle,
la synthèse de chaque pôle, puis la slide de vote (l'échelle). Les blocs
d'axe sont MINCES : ils nomment un code d'instrument et un gabarit — un même
bloc listé neuf fois casserait marqueurs et TOC, d'où neuf blocs par gabarit.

Conventions reprises des decks existants :

- pôle ACCÉLÉRATEUR à gauche en carte bleue, décélérateur à droite en corail
  (convention d'affichage sumvadis, cf. ``postair_data`` et la slide
  « The instrument » de survey) ;
- les marqueurs et libellés TOC suivent la langue REÇUE par ``build(lang)``
  (règle R-i18n, 2026-08-28) : l'export FR les traduit ; l'app orateur
  garde ceux de la langue de démarrage, le cache de pagination les fige ;
- tous les textes viennent du gel (``custom.instrument``), rien à la main.
"""

from __future__ import annotations

from streamtex import *
from streamtex.enums import Tags as t

from custom.instrument import axis, scale, synthesis
from postair_lang import current_lang
from custom.styles import Styles as s


class _S:
    title = s.project.titles.slide_title + s.center_txt
    pole = s.project.body.name_double + s.center_txt
    statement = s.project.body.bullet + s.center_txt + s.italic
    level = s.project.body.bullet + s.center_txt
    no_opinion = s.project.body.bullet + s.center_txt + s.project.colors.amber


#: LE calibrage du deck, en un seul endroit (NG 2026-08-24) — neuf axes qui
#: doivent rester homogènes se règlent ici, pas dans neuf blocs. Chaque
#: gabarit expose ces mêmes clés en paramètres nommés (mêmes noms camelCase
#: que ``screen_slide`` de survey) : un bloc ne porte QUE ce qu'il surcharge.
_ZOOMS = {
    "questions":    {"zoomTitle": 130, "zoomPole": 100, "zoomCell": 70},
    "pole":         {"zoomTitle": 115, "zoomPole": 120, "zoomCell": 170},
    "vote":         {"zoomTitle": 130, "zoomImage": 100, "zoomText": 180},
    "vote_abstain": {"zoomTitle": 130, "zoomImage": 100, "zoomText": 300},
}


def _z(profile: str, **overrides) -> dict:
    """Le calibrage d'un gabarit : la table, surchargée par l'appel.

    ``None`` veut dire « je ne surcharge pas » — un bloc mince ne cite que
    les clés qu'il règle. Une clé inconnue est une erreur BRUYANTE : une
    faute de frappe silencieuse laisserait la slide au défaut sans un mot,
    et l'orateur ne le verrait qu'en projection.
    """
    zooms = dict(_ZOOMS[profile])
    for key, value in overrides.items():
        if key not in zooms:
            raise KeyError(f"zoom inconnu {key!r} pour {profile!r} — "
                           f"clés valides : {sorted(zooms)}")
        if value is not None:
            zooms[key] = value
    return zooms


def _title(ax: dict, zoom: int, lang: str) -> None:
    with st_zoom(zoom):
        st_write(_S.title, (s.project.titles.keyword, ax["name"][lang]),
                 tag=t.div)


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


def _pole_columns(ax: dict, cells, *, zoomPole: int, zoomCell: int,
                  lang: str) -> None:
    """Deux colonnes : en-tête de pôle (bleu/corail), puis les cellules.

    ``cells(pole, kind)`` rend la liste ``[(carte, énoncé), …]`` — le gabarit
    ne décide pas du contenu, seulement de l'empilement et des zooms.
    """
    columns = [(s.project.cards.blue, "accel"), (s.project.cards.coral, "decel")]
    with st_grid(cols=s.project.grids.balanced(2, min_px=420), gap="2vw",
                 grid_style=s.project.grids.stretch,
                 cell_styles=s.project.containers.grid_cell_stretch) as g:
        for header, kind in columns:
            pole = ax[kind]
            with g.cell():
                with st_block(header), st_zoom(zoomPole):
                    st_write(_S.pole, pole["label"][lang], tag=t.div)
                for card, text in cells(pole, kind):
                    st_space("v", "1.2vh")
                    with st_block(card), st_zoom(zoomCell):
                        st_write(_S.statement, "“", text, "”", tag=t.div)


def questions_slide(code: str, *, lang: str | None = None,
                    zoomTitle: int | None = None,
                    zoomPole: int | None = None,
                    zoomCell: int | None = None) -> None:
    """Page 1 de l'axe : les 3 énoncés de chaque pôle, une cellule chacun.

    Les trois zooms se surchargent depuis le bloc ; sans surcharge, la table
    ``_ZOOMS`` fait foi. ``zoomCell`` est le réglage sensible : à 70 les six
    cellules tiennent dans l'écran, au-delà les dernières passent sous le pli
    (les colonnes sont en %, leur boîte ne grandit pas — règle R-zoom).
    """
    z = _z("questions", zoomTitle=zoomTitle, zoomPole=zoomPole, zoomCell=zoomCell)
    lang = lang or current_lang()
    ax = axis(code)
    st_marker(ax["name"][lang])
    with st_block(s.project.containers.page_fill_top):
        # Pas d'ancre TOC ici : depuis l'exclusion des slides d'énoncés
        # (NG 2026-08-24), l'ancre de l'axe vit sur la slide du pôle
        # accélérateur — la tête de groupe STABLE, que ce bloc soit
        # réactivé ou non (règle des ancres, PLAYBOOK §3).
        _title(ax, z["zoomTitle"], lang)
        st_space("v", "2vh")
        _pole_columns(ax, lambda pole, _kind: [
            (_CELL_CARDS[i], stmt["text"][lang])
            for i, stmt in enumerate(pole["statements"])],
            zoomPole=z["zoomPole"], zoomCell=z["zoomCell"], lang=lang)


#: La colonne d'un pôle seule au centre de la slide : pleine largeur elle
#: étirerait les lignes au-delà du confort de lecture d'amphi.
_POLE_COLUMN = Style(
    "max-width: 62vw; margin-left: auto; margin-right: auto;",
    "handsup_pole_column",
)


def _axis_pair_title(ax: dict, zoom: int, lang: str, **toc) -> None:
    """Le titre au format NG 2026-08-23 : Axis "Trust / Self-reliance"."""
    pair = f"{ax['accel']['label'][lang]} / {ax['decel']['label'][lang]}"
    with st_zoom(zoom):
        st_write(_S.title, "Axis “", (s.project.titles.keyword, pair), "”",
                 tag=t.div, **toc)


def pole_synthesis_slide(code: str, kind: str, *, lang: str | None = None,
                         zoomTitle: int | None = None,
                         zoomPole: int | None = None,
                         zoomCell: int | None = None) -> None:
    """La slide d'UN pôle (décision NG 2026-08-23 : vote PAR PÔLE).

    Remplace la synthèse à deux colonnes dans le book : chaque pôle ouvre sa
    propre séquence de vote. Titre = la paire de pôles de l'axe ; dessous, la
    colonne actuelle de CE pôle, seule et en grand — mêmes couleurs (en-tête
    bleu/corail, cellule teal/ambre). Les trois zooms se surchargent depuis
    le bloc ; sans surcharge, la table ``_ZOOMS`` fait foi.
    """
    z = _z("pole", zoomTitle=zoomTitle, zoomPole=zoomPole, zoomCell=zoomCell)
    lang = lang or current_lang()
    ax = axis(code)
    pole = ax[kind]
    st_marker(f"{pole['label'][lang]} — synthesis")
    with st_block(s.project.containers.page_fill_top):
        # L'ancre TOC de l'axe vit ICI, sur le pôle accélérateur — la tête
        # de groupe stable depuis l'exclusion des slides d'énoncés.
        toc = ({"toc_lvl": "1", "label": ax["name"][lang]}
               if kind == "accel" else {})
        _axis_pair_title(ax, z["zoomTitle"], lang, **toc)
        st_space("v", "4vh")
        header = s.project.cards.blue if kind == "accel" else s.project.cards.coral
        with st_block(_POLE_COLUMN):
            with st_block(header), st_zoom(z["zoomPole"]):
                st_write(_S.pole, pole["label"][lang], tag=t.div)
            st_space("v", "1.5vh")
            with st_block(_SYNTH_CARDS[kind]), st_zoom(z["zoomCell"]):
                st_write(_S.statement, "“", synthesis(pole)[lang], "”",
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


def _vote_slide(profile: str, *, kind: str, keyword: str, card,
                levels: list[dict], alt_ready: str, lang: str | None = None,
                zoomTitle: int | None = None, zoomImage: int | None = None,
                zoomText: int | None = None) -> None:
    """Le schéma commun des trois volets : image à gauche, valeurs à droite."""
    z = _z(profile, zoomTitle=zoomTitle, zoomImage=zoomImage, zoomText=zoomText)
    lang = lang or current_lang()
    st_marker(f"Vote — {keyword}", hidden=True)
    with st_block(s.project.containers.page_fill_top):
        with st_zoom(z["zoomTitle"]):
            st_write(_S.title, "Vote: ", (s.project.titles.keyword, keyword),
                     tag=t.div)
        st_space("v", "3vh")
        with st_grid(cols="46% 54%", gap="2vw",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                with st_zoom(z["zoomImage"]):
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
                    with st_zoom(z["zoomText"]):
                        st_write(_S.level, level[lang], tag=t.div)


def vote_support_slide(**zooms) -> None:
    """Volet 1 : les trois réponses EN FAVEUR, intensité décroissante."""
    _vote_slide("vote", kind="support", keyword="I support",
                card=s.project.cards.blue, levels=scale()["agree"],
                alt_ready=("Papercut crowd with every arm raised high in "
                           "enthusiastic approval under an amber paper sun"),
                **zooms)


def vote_oppose_slide(**zooms) -> None:
    """Volet 2 : les trois réponses EN DÉFAVEUR, intensité croissante."""
    _vote_slide("vote", kind="oppose", keyword="I oppose",
                card=s.project.cards.coral, levels=scale()["disagree"],
                alt_ready=("Papercut crowd with arms crossed or palms raised "
                           "gently forward in polite refusal"),
                **zooms)


def vote_abstain_slide(**zooms) -> None:
    """Volet 3 : la réponse de qui ne souhaite pas se prononcer.

    Profil de zoom PROPRE (``vote_abstain``) : une seule valeur à afficher,
    donc un corps beaucoup plus grand que les volets à trois niveaux.
    """
    _vote_slide("vote_abstain", kind="abstain", keyword="no opinion",
                card=s.project.cards.amber, levels=[scale()["no_opinion"]],
                alt_ready=("Papercut crowd standing back with hands in "
                           "pockets, an amber paper sun behind a cloud"),
                **zooms)
