"""The second family — the nine axes again, in objects.

Closes the welcome sequence, just before the survey. The three register slides
have already walked the room through the nine axes with the animal family, one
register at a time; there is nothing left to teach here. What this slide does is
introduce the OTHER cast (NG 2026-08-03): the same nine tensions, the same
eighteen poles, carried by objects instead of creatures.

Nine cards on two rows, one per axis, each holding its two poles. Not thirty-six
cells: a plate of everything at once was a poster, and a poster is read in
silence for ten seconds and then forgotten. Nine cards can be pointed at.

If a film of the nine axes is dropped into the shared video folder under the
name below, the slide plays it instead of the cards — no code change.

SPEAKER NOTES:
Two minutes, and mostly silence. Say one thing before: you have met these nine
questions already, here is the second cast that carries them — some people
recognise themselves in a creature, others in a thing. Say one thing after: the
survey is about to tell you which ones look like you. If the film is playing, do
not talk over it — and check the sound before the session, not during.
"""
# @guideline: postair-minimal

# ``from streamtex import *`` shadows the builtin ``list`` with the st_list
# module: annotations must stay unevaluated.
from __future__ import annotations

from pathlib import Path

from custom.styles import DS
from custom.styles import Styles as s
from postair_data import REGISTERS, axes, film_clip, register_axes
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex import st_video, st_zoom
from streamtex.enums import Tags as t

from postair_pack.components.ai_mark import ai_marked
from postair_pack.components.axis_stack import axis_stack

#: Le film des axes (« Les 9 axes — la phrase mémo », 68 s) — nommé au
#: catalogue (section `films` du studio, NG 2026-08-14), matérialisé par
#: sync_media sous static/media/clips/. Le chemin mort vers le gel manuel
#: (_SHARED/mascots/videos/) a vécu : ce dossier est vide depuis le 02/08.
_MEDIA = Path(__file__).parent.parent / "static" / "media"

#: Neuf cartes sur DEUX lignes (NG 2026-08-03) : cinq puis quatre. Le plancher
#: en pourcentage plafonne à cinq colonnes — posé entre 100/5 et 100/6, il en
#: laisse tenir cinq et pas une de plus. Le plancher en pixels reprend la main
#: sur une fenêtre étroite et fait retomber la grille à moins de colonnes, donc
#: rien ne déborde quelle que soit la largeur.
_COLS = "repeat(auto-fit, minmax(max(220px, 18%), 1fr))"

#: Deux mascottes empilées dans une carte deux fois moins haute qu'une slide de
#: registre : l'image se borne par la HAUTEUR autant que par la largeur.
_IMAGE_WIDTH = "min(7vw, 9.5vh)"


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    lead = s.project.body.bullet + s.center_txt
    axis_name = s.project.body.mascot_name


bs = BlockStyles


def _axes_in_order() -> list[dict]:
    """The nine axes of the OBJECTS family, in register order.

    Register order rather than axis number: it is the order the room has just
    been walked through, and a cast that reappears in a different order reads as
    a different cast.
    """
    objects = axes("objects")
    return [objects[axis["axis"]]
            for name, _sub, _n in REGISTERS
            for axis in register_axes(name)]


def build():
    st_marker("The whole company")
    film = _MEDIA / film_clip("axes-intro", "en")
    with st_block(s.project.containers.page_fill_full if film.exists()
                  else s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "The same nine axes — ",
                         (s.project.titles.keyword, "the other family"),
                         tag=t.div, toc_lvl="+1", label="The whole company")
            with g.cell():
                st_info_tooltip(
                    title="Two families, one cast",
                    entries=[
                        ("Why two families", "Every pole is carried by an animal AND an object. "
                         "Some people recognise themselves in a creature, others in a thing — and "
                         "having two makes it obvious that the character is a position, not a "
                         "portrait of anybody."),
                        ("Eighteen poles", "Nine axes, two poles each. Both poles of an axis are "
                         "legitimate: the cast has no villain."),
                        ("Top and bottom", "On every card the accelerating pole is on top, by "
                         "convention. 'Accelerator' never means 'better'."),
                        ("Two moderators", "Medio and Voxo belong to no axis. They open, arbitrate "
                         "and close — the only two characters who do not hold a position."),
                        ("Production", "Made in house, entirely with generative AI, from the "
                         "definitions of the nine axes. The mascots are the study's own "
                         "vocabulary made visible."),
                        ("Next", "The survey asks you six questions per axis. You are about to "
                         "find out which of these characters keeps showing up in your answers."),
                    ],
                )
        if film.exists():
            # st.video veut un chemin réel ; le dossier des médias n'est pas
            # une source statique, on passe le chemin absolu matérialisé.
            with ai_marked(fit=False, top=True):
                st_video(str(film))
            st_space("v", "30vh")
            return
        st_space("v", "1vh")
        st_write(bs.lead, "Nine axes, eighteen postures — ",
                 (s.project.titles.keyword, "none of them is wrong"), tag=t.div)
        st_space("v", "1.5vh")
        # ONE flat grid: nine cells, each a self-contained axis card.
        # st_zoom (NG 2026-08-13) : la seule slide du deck à 18 cellules —
        # la réduction proportionnelle locale fait tenir les deux rangées
        # SANS changer le layout ; les étiquettes s'élargissent d'autant
        # (fin du « Transhumani-sm » coupé).
        with st_zoom(60), st_grid(cols=_COLS, gap="0.8vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_top) as g:
            for axis in _axes_in_order():
                # Le nom d'axe du manifeste est français sur un deck anglais et
                # redondant avec les deux pôles affichés (NG 2026-08-13) : les
                # étiquettes de pôles portent la tension à elles seules.
                with g.cell(), st_block(s.project.containers.column_stack_centered):
                    axis_stack(axis, DS, image_width=_IMAGE_WIDTH, compact=True)
