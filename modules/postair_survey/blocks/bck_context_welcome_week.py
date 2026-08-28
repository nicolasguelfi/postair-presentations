"""Contexte 1/2 — la Welcome Week de l'Université du Luxembourg.

L'outil SUMVADIS sera présenté dans des contextes différents (NG 2026-08-20) :
une slide de contexte par cadre d'usage, en tête de deck. Celle-ci est le cadre
ACADÉMIQUE — le logo de l'université en haut, puis les messages qui posent le
contrat avec la salle : un jeu, mais aussi une vraie étude de recherche, avec
ses règles (anonymat, volontariat, mineurs hors analyse).

Le logo est la variante BLANCHE (fond transparent) du dépôt sumvadis
(``apps/web/public/sponsors/ul-logo-dark-512.png``), copiée sous
``static/images/logos/`` — un logo n'est pas un média de campagne : il est
versionné ici, comme les illustrations du deck, jamais tiré du CDN.

SPEAKER NOTES:
One minute. This is the contract slide: say the four lines out loud, slowly.
The room must hear « anonymous », « voluntary » and the under-18 rule once,
from the stage, before anyone opens the survey. Then the fun can start.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from postair_i18n import ui
from postair_lang import T
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    icon = s.center_txt + s.text_6xl
    headline = s.project.body.bullet_giant
    message = s.project.body.bullet
    caveat = s.project.body.bullet + s.project.colors.coral


bs = BlockStyles

#: Le logo — variante blanche pour le thème sombre, sous static/images/
#: (sondé par les sources statiques : inliné, ~18 Ko, assumé).
_LOGO = "images/logos/ul-logo-white.png"
_LOGO_WIDTH = "min(22vw, 30vh)"

#: Une rangée = une icône + un message. Le style dit la hiérarchie : la
#: promesse en géant, le contrat en corps courant, la règle des mineurs en
#: corail (la seule ligne juridique de la slide).
#: La promesse est commune aux deux slides de contexte : lexique
#: (``entertaining_survey``) ; les trois autres lignes sont propres à celle-ci.
_MESSAGES = [
    ("🎡", bs.headline, "entertaining_survey"),
    ("🔬", bs.message, {"en": "Your first participation in an academic research study :) !!"}),
    ("🎭", bs.message, {"en": "Anonymous and on a voluntary basis."}),
    ("🔞", bs.caveat, {"en": "If less than 18 years old, participation is not considered for research."}),
]
_MARKER = {"en": "Welcome Week"}
_LABEL = {"en": "Contexts"}
_TIP_TITLE = {"en": "This session's frame"}
_TIP_GAME = ({"en": "A game AND a study"},
             {"en": ("The survey is designed to be fun to "
                     "answer, and it is also a real academic research instrument: "
                     "the anonymous answers feed the POSTAIR study.")})
#: Têtes « Voluntary », « Anonymous », « Under 18 » : lexique (partagées).
_TIP_VOLUNTARY = {"en": ("Nobody has to answer. You can stop at any "
                         "time, and an unfinished survey is simply never sent.")}
_TIP_ANON = {"en": ("Nothing personal is collected; your report is "
                    "computed on YOUR device and only anonymous answers reach "
                    "the averages.")}
_TIP_UNDER_18 = {"en": ("You are welcome to play and see your own "
                        "results — your record is simply excluded from the research "
                        "analysis.")}


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        # Le gabarit maison 92/8 : le logo tient lieu de titre, le tooltip
        # garde sa cellule habituelle en haut à droite.
        with st_grid(cols="92% 8%",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_image(s.project.cards.media_center, width=_LOGO_WIDTH,
                         uri=_LOGO,
                         alt="Logo of the University of Luxembourg — uni.lu")
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[
                        (T(_TIP_GAME[0], lang), T(_TIP_GAME[1], lang)),
                        (ui("voluntary", lang), T(_TIP_VOLUNTARY, lang)),
                        (ui("anonymous", lang), T(_TIP_ANON, lang)),
                        (ui("under_18", lang), T(_TIP_UNDER_18, lang)),
                    ],
                )
        st_space("v", "2vh")
        with st_grid(cols="10% 90%", gap="1vw",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for index, (icon, style, message) in enumerate(_MESSAGES):
                with g.cell():
                    with st_zoom(130):
                        st_write(bs.icon, icon, tag=t.div)
                with g.cell():
                    # L'ancre TOC de la partie « Contexts » vit sur la première
                    # ligne : la slide n'a pas de titre, le logo EST l'en-tête.
                    toc = ({"toc_lvl": "1", "label": T(_LABEL, lang)}
                           if index == 0 else {})
                    text = (ui(message, lang) if isinstance(message, str)
                            else T(message, lang))
                    st_write(style, text, tag=t.div, **toc)
