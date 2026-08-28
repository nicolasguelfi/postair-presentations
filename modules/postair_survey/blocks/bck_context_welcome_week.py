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
_MESSAGES = [
    ("🎡", bs.headline, "An entertaining survey to discover your postures facing the AI revolution."),
    ("🔬", bs.message, "Your first participation in an academic research study :) !!"),
    ("🎭", bs.message, "Anonymous and on a voluntary basis."),
    ("🔞", bs.caveat, "If less than 18 years old, participation is not considered for research."),
]


def build(lang: str = "en", **_):
    st_marker("Welcome Week")
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
                    title="This session's frame",
                    entries=[
                        ("A game AND a study", "The survey is designed to be fun to "
                         "answer, and it is also a real academic research instrument: "
                         "the anonymous answers feed the POSTAIR study."),
                        ("Voluntary", "Nobody has to answer. You can stop at any "
                         "time, and an unfinished survey is simply never sent."),
                        ("Anonymous", "Nothing personal is collected; your report is "
                         "computed on YOUR device and only anonymous answers reach "
                         "the averages."),
                        ("Under 18", "You are welcome to play and see your own "
                         "results — your record is simply excluded from the research "
                         "analysis."),
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
                    toc = ({"toc_lvl": "1", "label": "Contexts"}
                           if index == 0 else {})
                    st_write(style, message, tag=t.div, **toc)
