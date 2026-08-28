"""Contexte 2/2 — tous les autres cadres, hors académique.

L'outil SUMVADIS sera présenté dans des contextes différents (NG 2026-08-20) :
une slide de contexte par cadre d'usage, en tête de deck. Celle-ci est le
cadre GÉNÉRIQUE — entreprise, salon, atelier, soirée : le wordmark sumvadis en
haut, et seulement les deux messages qui valent partout (le jeu, le
volontariat). Pas de ligne « recherche » : hors cadre académique, les réponses
ne nourrissent pas l'étude.

Le wordmark est la variante BLANCHE (fond transparent) du dépôt sumvadis
(``apps/events/brand/wordmark_sumvadis_white_2000.png``), copiée sous
``static/images/logos/`` — versionnée ici comme les illustrations du deck,
jamais tirée du CDN.

SPEAKER NOTES:
Thirty seconds. One promise (a fun way to discover your own postures), one
rule (nobody has to play). Skip this slide entirely when presenting at the
university — the Welcome Week slide before it carries the academic frame.
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


bs = BlockStyles

#: Le wordmark — variante blanche pour le thème sombre, sous static/images/
#: (sondé par les sources statiques : inliné, ~75 Ko, assumé).
_LOGO = "images/logos/sumvadis-wordmark-white.png"
#: Très allongé (2000×352, ratio ≈ 5,7) : la LARGEUR mène, le vh ne borne
#: qu'une fenêtre basse.
_LOGO_WIDTH = "min(34vw, 90vh)"

#: Une rangée = une icône + un message (même grammaire que la slide
#: Welcome Week — les deux slides de contexte se répondent).
_MESSAGES = [
    ("🎡", bs.headline, "An entertaining survey to discover your postures "
                        "facing the AI revolution."),
    ("🙋", bs.message, "On a voluntary basis."),
]


def build(lang: str = "en", **_):
    st_marker("Any other context")
    with st_block(s.project.containers.page_fill_top):
        # Le gabarit maison 92/8 : le wordmark tient lieu de titre, le tooltip
        # garde sa cellule habituelle en haut à droite.
        with st_grid(cols="92% 8%",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_image(s.project.cards.media_center, width=_LOGO_WIDTH,
                         uri=_LOGO, alt="sumvadis wordmark")
            with g.cell():
                st_info_tooltip(
                    title="Beyond the university",
                    entries=[
                        ("One tool, many rooms", "The same survey runs at a "
                         "company workshop, a fair booth or an evening event — "
                         "only the frame changes, never the instrument."),
                        ("Voluntary", "Nobody has to answer. You can stop at "
                         "any time, and an unfinished survey is simply never "
                         "sent."),
                        ("Anonymous by design", "Nothing personal is collected; "
                         "your report is computed on YOUR device."),
                    ],
                )
        st_space("v", "6vh")
        with st_grid(cols="10% 90%", gap="1vw",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for index, (icon, style, message) in enumerate(_MESSAGES):
                with g.cell():
                    st_write(bs.icon, icon, tag=t.div)
                with g.cell():
                    toc = ({"toc_lvl": "+1", "label": "Beyond the university"}
                           if index == 0 else {})
                    st_write(style, message, tag=t.div, **toc)
