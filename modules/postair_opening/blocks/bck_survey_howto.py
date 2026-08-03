"""How to answer — shown just before the join slide.

SPEAKER NOTES:
Three minutes, calm and clear. 54 statements, six agreement levels, no middle
point — a gentle forced choice; "no opinion" exists and is NOT a middle
answer. There is no right answer and no image to polish: answer for
yourself, honestly. Some statements feel "reversed" — that's intentional
(acquiescence control), read carefully. Solyo and Nimbo embody the two ends
of the scale.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from postair_data import mascot
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    bullet = s.project.body.bullet
    scale_end = s.project.body.pole_label
    scale_bar = s.project.cards.pole_cell


bs = BlockStyles

_BULLETS = [
    ("54 statements", " — about AI and you"),
    ("Six levels", " — strongly disagree ↔ strongly agree"),
    ("No right answer", " — it's a portrait, not a test"),
    ("Answer for YOURSELF", " — honestly, not for the image"),
    ("“No opinion” exists", " — and it's not a middle answer"),
]


def build():
    st_marker("How to answer")
    nimbo, solyo = mascot("Nimbo"), mascot("Solyo")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "How to ", (s.project.titles.keyword, "answer"),
                         tag=t.div, toc_lvl="+1", label="How to answer")
            with g.cell():
                st_info_tooltip(
                    title="The instrument",
                    entries=[
                        ("Why six levels, no middle", "A gentle forced choice: the middle of a "
                         "scale attracts non-answers. If you truly have no opinion, use the "
                         "dedicated 'no opinion' button — it is excluded from your scores."),
                        ("Reversed statements", "Half the statements of each axis are phrased "
                         "toward one pole, half toward the other — a standard control against "
                         "automatic agreement. Read each one for itself."),
                        ("Help per question", "Every statement in the app has a help button: "
                         "clarification, anchors and two concrete examples."),
                        ("Duration", "Measured median: 15-20 minutes. You can pause and resume "
                         "on your device."),
                    ],
                )
        st_space("v", "1vh")
        # Two cells — the instructions and the scale. The pixel floor is raised
        # well above the default: a bullet list needs room to breathe before it
        # is worth splitting the screen at all.
        with st_grid(cols=s.project.grids.balanced(2, min_px=420), gap="2vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                with st_list(li_style=bs.bullet) as ul:
                    for kw, rest in _BULLETS:
                        with ul.item():
                            st_write(bs.bullet, (s.project.titles.keyword, kw), rest)
            with g.cell():
                with st_block(bs.scale_bar):
                    st_write(bs.scale_end, "Strongly disagree", tag=t.div)
                    # Asked for by name, never by path: these two carried
                    # hand-typed URIs into the frozen folder the 36 mascots left
                    # when they moved to the CDN, and showed missing images.
                    st_image(s.project.cards.media_center, width="min(10vw, 18vh)",
                             uri=nimbo["image"],
                             alt=f"{nimbo['name']}, the pessimist mole mascot, "
                                 "at the disagree end")
                    st_write(s.project.body.mascot_name, "⬍  six levels  ⬍", tag=t.div)
                    st_image(s.project.cards.media_center, width="min(10vw, 18vh)",
                             uri=solyo["image"],
                             alt=f"{solyo['name']}, the optimist squirrel mascot, "
                                 "at the agree end")
                    st_write(bs.scale_end, "Strongly agree", tag=t.div)
