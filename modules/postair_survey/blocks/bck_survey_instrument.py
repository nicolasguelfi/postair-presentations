"""The POSTAIR instrument — l'idée, en une slide (NG 2026-08-20).

Trois questions par posture, dix-huit postures définies : c'est TOUT ce que la
slide dit, avec deux exemples qui montrent la mécanique — les deux pôles d'un
même axe, chacun avec une question qui lui ressemble. La salle comprend en une
lecture pourquoi le questionnaire fait 54 énoncés, et pourquoi aucune posture
n'est un verdict.

Reprend le rôle pédagogique de l'ancienne slide « How to answer » (supprimée
le 2026-08-20) : son tooltip « The instrument » vit désormais ici ; les trois
propriétés cruciales (no right answer / for yourself / no opinion) vivent sur
la slide de l'écran « a statement » (``bck_screens_statement``).

SPEAKER NOTES:
One minute. Say the arithmetic once — eighteen postures, three questions
each — then read the two examples aloud: one welcoming, one resisting, both
legitimate. That symmetry is the whole spirit of the instrument.
"""
# @guideline: postair-minimal

from custom.refs import citation
from custom.styles import Styles as s
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    # Ambre : LE point focal de la slide (même rôle que la valeur des slides
    # « Already here »), posé APRÈS bullet_giant pour surcharger sa couleur.
    lead = s.project.body.bullet_giant + s.center_txt + s.project.colors.amber
    posture = s.project.body.name_double
    question = s.project.body.bullet + s.center_txt + s.italic
    grounding = s.project.body.caption + s.center_txt


bs = BlockStyles

#: L'idée, en une phrase.
_LEAD = "3 questions for each of the \n2 poles of the 9 axes"

#: Deux exemples = les deux pôles d'un même axe (openness), un par carte :
#: la carte bleue accueille, la corail résiste — aucun des deux n'a tort.
_EXAMPLES = [
    (s.project.cards.blue, "Openness",
     "Do you welcome the AI technology in your life?"),
    (s.project.cards.coral, "Resistance",
     "Do you prefer to live without AI as much as possible?"),
]


def build():
    st_marker("The instrument")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                with st_zoom(130):
                    st_write(bs.title, "The ", (s.project.titles.keyword, "POSTAIR"),
                            " instrument", tag=t.div, toc_lvl="+1",
                            label="The instrument")
            with g.cell():
                st_info_tooltip(
                    title="The instrument",
                    entries=[
                        ("54 statements", "Three per posture, two postures per axis, "
                         "nine axes. Half of each axis is phrased toward one pole and "
                         "half toward the other."),
                        ("Why six levels, no middle", "A gentle forced choice: the middle "
                         "of a scale attracts non-answers. If you truly have no opinion, "
                         "use the dedicated 'no opinion' button — it is excluded from "
                         "your scores."),
                        ("Reversed statements", "Half the statements of each axis are "
                         "phrased toward one pole, half toward the other — a standard "
                         "control against automatic agreement. Read each one for itself."),
                        ("Help per question", "Every statement in the app has a help "
                         "button: clarification, anchors and two concrete examples."),
                        ("Duration", "Measured median: 20-40 minutes. You can pause and "
                         "resume on your device."),
                    ],
                )
        st_space("v", "2vh")
        with st_zoom(110):
            st_write(bs.lead, _LEAD, tag=t.div)
        st_space("v", "4vh")
        with st_grid(cols=s.project.grids.balanced(2, min_px=420), gap="2vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_stretch) as g:
            for card, posture, question in _EXAMPLES:
                with g.cell(), st_block(card):
                    with st_zoom(130):
                        st_write(bs.posture, posture, tag=t.div)
                        st_space("v", "1.5vh")
                        st_write(bs.question, "“", question, "”", tag=t.div)
        st_space("v", "2vh")
        # Le code de citation dans le texte VISIBLE : l'instrument dérive d'un
        # article publié — même ancrage que la slide de la roue.
        st_write(bs.grounding, "model: ",
                 citation("guelfi-postair", inline=True), tag=t.div)
