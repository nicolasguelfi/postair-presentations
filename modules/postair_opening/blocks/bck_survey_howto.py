"""How to answer — shown just before the join slide.

Five properties, and nothing else (NG 2026-08-03). The commentary that used to
follow each one is gone: it was there to be read, and nobody reads a second
clause on a slide that is up for ninety seconds. What survives is the property
itself, at the largest size the slide can hold — everything that was explanatory
lives in the tooltip, where a challenged speaker can find it.

The right-hand side shows the six agreement levels as the room will meet them on
their own screen. If a real screenshot of the application is dropped in under
the name below, the slide shows it; otherwise it draws the scale itself, which
projects better than a phone capture and can never fall out of date silently.

SPEAKER NOTES:
Three minutes, calm and clear. 54 statements, six agreement levels, no middle
point — a gentle forced choice; "no opinion" exists and is NOT a middle
answer. Say that last line slowly: it is the one people get wrong, and it is
the one in red. There is no right answer and no image to polish: answer for
yourself, honestly. Some statements feel "reversed" — that's intentional
(acquiescence control), read carefully.
"""
# @guideline: postair-minimal

from pathlib import Path

from custom.styles import DS
from custom.styles import Styles as s
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    bullet = s.project.body.bullet_giant
    alert = s.project.body.bullet_giant + s.project.colors.critical
    level = s.project.body.body + s.center_txt + s.bold
    caption = s.project.body.caption + s.center_txt


bs = BlockStyles

#: Les cinq propriétés, sans commentaire. La dernière est en deux morceaux :
#: ce qui est rouge est ce que la salle comprend de travers une fois sur deux.
_PROPERTIES = [
    ("54 statements", ""),
    ("Six levels", ""),
    ("No right answer", ""),
    ("Answer for YOURSELF", ""),
    ("No opinion is ", "not a middle answer"),
]

#: L'échelle telle que la salle la rencontrera. Dessinée ici faute de capture :
#: le libellé exact vient de l'application, et doit être revu si elle change.
_LEVELS = [
    "Strongly disagree",
    "Disagree",
    "Somewhat disagree",
    "Somewhat agree",
    "Agree",
    "Strongly agree",
]

#: Capture d'écran réelle des six niveaux, si elle est déposée un jour. Absente,
#: la slide dessine l'échelle — jamais d'image manquante devant l'amphithéâtre.
_SCREENSHOT = "images/survey_levels.png"
_STATIC = Path(__file__).parent.parent / "static"


def _scale() -> None:
    """The six levels, drawn — coral at one end, teal at the other, no middle."""
    for index, label in enumerate(_LEVELS):
        with st_block(DS.cards.scale_step(index, len(_LEVELS))):
            st_write(bs.level, label, tag=t.div)
        st_space("v", "0.6vh")
    st_space("v", "0.8vh")
    st_write(bs.caption, "plus a separate “no opinion” button — outside the scale",
             tag=t.div)


def build():
    st_marker("How to answer")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "How to ", (s.project.titles.keyword, "answer"),
                         tag=t.div, toc_lvl="+1", label="How to answer")
            with g.cell():
                st_info_tooltip(
                    title="The instrument",
                    entries=[
                        ("54 statements", "Six per axis, nine axes. Half of each axis is phrased "
                         "toward one pole and half toward the other."),
                        ("Why six levels, no middle", "A gentle forced choice: the middle of a "
                         "scale attracts non-answers. If you truly have no opinion, use the "
                         "dedicated 'no opinion' button — it is excluded from your scores."),
                        ("Why that matters", "A middle answer would be counted as a position "
                         "halfway between the poles. 'No opinion' is counted as nothing at all. "
                         "They are not the same measurement, and confusing them is the one "
                         "mistake that distorts a profile."),
                        ("No right answer", "It is a portrait, not a test. Nothing is scored as "
                         "correct, and nobody sees your individual answers."),
                        ("Answer for yourself", "Not for the image you would like to give. The "
                         "result is only useful if it is yours."),
                        ("Reversed statements", "Half the statements of each axis are phrased "
                         "toward one pole, half toward the other — a standard control against "
                         "automatic agreement. Read each one for itself."),
                        ("Help per question", "Every statement in the app has a help button: "
                         "clarification, anchors and two concrete examples."),
                        ("Duration", "Measured median: 20-40 minutes. You can pause and resume "
                         "on your device."),
                    ],
                )
        st_space("v", "1vh")
        # Two cells — the properties and the scale. The pixel floor is raised
        # well above the default: neither half is worth splitting further, and
        # on a narrow window they stack instead of shrinking.
        with st_grid(cols=s.project.grids.balanced(2, min_px=420), gap="2vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                with st_list(li_style=bs.bullet) as ul:
                    for head, alert in _PROPERTIES:
                        with ul.item():
                            if alert:
                                st_write(bs.bullet, head, (bs.alert, alert))
                            else:
                                st_write(bs.bullet, head)
            with g.cell():
                with st_block(s.project.containers.column_stack_centered):
                    if (_STATIC / _SCREENSHOT).exists():
                        st_image(s.project.cards.media_center, width="100%",
                                 uri=_SCREENSHOT,
                                 alt="Screenshot of the survey: the six agreement levels "
                                     "offered for one statement")
                    else:
                        _scale()
