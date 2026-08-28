"""The substitution protocol — what makes the 25-century comparison rigorous.

The hub's METHOD (§2): every figure answers the SAME 54-item questionnaire,
with « artificial intelligence » replaced by the disruptive technology of
their own wave — « the printing press », « the railway and the telegraph »,
« the atomic energy and weapons »… The postures become comparable because the
construct stays the same; only the era's term changes. The figures of the AI
wave answer verbatim: it is the studied wave.

SPEAKER NOTES:
This is the legitimacy slide — say it slowly, once: « same questions, the
technology of their time ». If someone challenges a historical posture later,
come back here: the method is the answer, not the anecdote.
"""
# @guideline: postair-minimal

from custom import content
from custom.styles import Styles as s
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    big = s.project.body.bullet_giant + s.center_txt
    line = s.project.body.bullet + s.center_txt
    example = s.project.body.caption + s.center_txt


bs = BlockStyles


def build(lang: str = "en", **_):
    st_marker("The substitution")
    # Trois exemples RÉELS du gel — jamais tapés ici (R13).
    samples = [w for w in content.waves() if w["id"] in
               ("printing-press", "rail-telegraph", "atom")]
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "The ", (s.project.titles.keyword, "substitution"),
                         " protocol", tag=t.div, toc_lvl="1",
                         label="The substitution")
            with g.cell():
                st_info_tooltip(
                    title="The protocol, in full",
                    entries=[
                        ("Same construct", "Every figure answers the same "
                         "54-item questionnaire; only the era's term replaces "
                         "« artificial intelligence » — the hub's METHOD §2."),
                        ("Verbatim for AI", "The figures of the AI wave answer "
                         "with no substitution: it is the studied wave."),
                        ("Per-axis rules", "Trust maps to the epistemic "
                         "authorities of the era, centralisation to its "
                         "governance structures — documented per figure in "
                         "the hub's evidence dossiers."),
                    ])
        st_space("v", s.project.spacing.title_gap)
        st_write(bs.big, "same 54 questions", tag=t.div)
        st_write(bs.line, "« AI » becomes ",
                 (s.project.colors.keyword, "the technology of their time"),
                 tag=t.div)
        st_space("v", "3vh")
        for w in samples:
            st_write(bs.example,
                     f"{content.text(w['name'])} — “{content.text(w['substitution'])}”",
                     tag=t.div)
