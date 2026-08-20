"""The first screens — enter the code (01) and the campaign welcome (02).

Héritée de l'ancien bloc « How to answer » (supprimé le 2026-08-20) : sa
sous-slide « The first screens · 1-2 » survit ici telle quelle — les écrans
du consentement (03) et de l'énoncé (04) ont désormais chacun leur slide Q14
(``bck_screens_consent``, ``bck_screens_statement``). Deux captures portrait
par slide (NG 2026-08-15) : chaque écran en grand, lisible du fond.

SPEAKER NOTES:
Thirty seconds. Walk the two screens once, left to right — the room will meet
them again on their own phones minutes later. The code of the day comes two
slides further; nothing to type yet.
"""
# @guideline: postair-minimal

from custom.captures import capture
from custom.styles import Styles as s
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    caption = s.project.body.caption + s.center_txt


bs = BlockStyles

#: Les deux premiers écrans du parcours, dans l'ordre où la salle les
#: rencontrera — captures RÉELLES (facette mobile, Q14), demandées par slug.
_SCREENS = [
    ("01-saisie-code", "1 · enter the code of the day"),
    ("02-accueil-campagne", "2 · the campaign welcomes you"),
]

#: Deux captures portrait côte à côte : la largeur suit la fenêtre, la
#: hauteur borne le portrait.
_WIDTH = "min(24vw, 42vh)"


def build():
    st_marker("The first screens")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "The ", (s.project.titles.keyword, "first screens"),
                         tag=t.div, toc_lvl="+1", label="The first screens")
            with g.cell():
                st_space("h", "0.5vw")
        st_space("v", "1vh")
        with st_grid(cols=s.project.grids.balanced(2, min_px=320), gap="2vw",
                     cell_styles=s.project.containers.grid_cell_top) as g:
            for slug, legend in _SCREENS:
                with g.cell():
                    st_image(s.project.cards.media_center, width=_WIDTH,
                             uri=capture(slug),
                             alt=f"Mobile screen of the survey journey: {legend}")
                    st_write(bs.caption, legend, tag=t.div)
