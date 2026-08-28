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
from postair_i18n import ui
from postair_lang import T
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
#: Welcome Week — les deux slides de contexte se répondent). La promesse
#: est commune aux deux slides : elle vient du lexique (``entertaining_survey``).
_MESSAGES = [
    ("🎡", bs.headline, "entertaining_survey"),
    ("🙋", bs.message, {"en": "On a voluntary basis."}),
]
_MARKER = {"en": "Any other context"}
_LABEL = {"en": "Beyond the university"}
_TIP_TITLE = {"en": "Beyond the university"}
_TIP_ROOMS = ({"en": "One tool, many rooms"},
              {"en": ("The same survey runs at a "
                      "company workshop, a fair booth or an evening event — "
                      "only the frame changes, never the instrument.")})
#: Tête « Voluntary » : lexique (partagée avec la slide Welcome Week).
_TIP_VOLUNTARY = {"en": ("Nobody has to answer. You can stop at "
                         "any time, and an unfinished survey is simply never "
                         "sent.")}
#: Tête « Anonymous by design » : lexique.
_TIP_ANON = {"en": ("Nothing personal is collected; "
                    "your report is computed on YOUR device.")}


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
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
                    title=T(_TIP_TITLE, lang),
                    entries=[
                        (T(_TIP_ROOMS[0], lang), T(_TIP_ROOMS[1], lang)),
                        (ui("voluntary", lang), T(_TIP_VOLUNTARY, lang)),
                        (ui("anonymous_by_design", lang), T(_TIP_ANON, lang)),
                    ],
                )
        st_space("v", "6vh")
        with st_grid(cols="10% 90%", gap="1vw",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for index, (icon, style, message) in enumerate(_MESSAGES):
                with g.cell():
                    st_write(bs.icon, icon, tag=t.div)
                with g.cell():
                    toc = ({"toc_lvl": "+1", "label": T(_LABEL, lang)}
                           if index == 0 else {})
                    text = (ui(message, lang) if isinstance(message, str)
                            else T(message, lang))
                    st_write(style, text, tag=t.div, **toc)
