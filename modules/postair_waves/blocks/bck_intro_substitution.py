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
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    big = s.project.body.bullet_giant + s.center_txt
    line = s.project.body.bullet + s.center_txt
    example = s.project.body.caption + s.center_txt


bs = BlockStyles

_MARKER = {"en": "The substitution", "fr": "La substitution"}
_TITLE = {"en": ("The ", (s.project.titles.keyword, "substitution"), " protocol"), "fr": ("La ", (s.project.titles.keyword, "substitution"), " comme protocole")}
_TIP_TITLE = {"en": "The protocol, in full", "fr": "Le protocole, en entier"}
_TIP = [
    ({"en": "Same construct", "fr": "Le même construit"},
     {"en": "Every figure answers the same 54-item questionnaire; only "
            "the era's term replaces « artificial intelligence » — the "
            "hub's METHOD §2.", "fr": "Chaque figure répond au même questionnaire de 54 items ; seul le terme de l'époque remplace « intelligence artificielle » — METHOD § 2 du hub."}),
    ({"en": "Verbatim for AI", "fr": "Verbatim pour l'IA"},
     {"en": "The figures of the AI wave answer with no substitution: it "
            "is the studied wave.", "fr": "Les figures de la vague IA répondent sans substitution : c'est la vague étudiée."}),
    ({"en": "Per-axis rules", "fr": "Règles par axe"},
     {"en": "Trust maps to the epistemic authorities of the era, "
            "centralisation to its governance structures — documented "
            "per figure in the hub's evidence dossiers.", "fr": "La confiance porte sur les autorités épistémiques de l'époque, la centralisation sur ses structures de gouvernance — documenté figure par figure dans les dossiers de preuves du hub."}),
]
_BIG = {"en": "same 54 questions", "fr": "mêmes 54 questions"}
_LINE = {"en": ("« AI » becomes ",
                (s.project.colors.keyword, "the technology of their time")), "fr": ("« IA » devient ", (s.project.colors.keyword, "la technologie de leur temps"))}
#: Un exemple du gel : nom de la vague et terme de substitution (données).
_EXAMPLE = {"en": "{name} — “{substitution}”", "fr": "{name} — « {substitution} »"}


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    # Trois exemples RÉELS du gel — jamais tapés ici (R13).
    samples = [w for w in content.waves() if w["id"] in
               ("printing-press", "rail-telegraph", "atom")]
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(T(head, lang), T(detail, lang))
                             for head, detail in _TIP])
        st_space("v", s.project.spacing.title_gap)
        st_write(bs.big, T(_BIG, lang), tag=t.div)
        st_write(bs.line, *TF(_LINE, lang), tag=t.div)
        st_space("v", "3vh")
        for w in samples:
            st_write(bs.example,
                     T(_EXAMPLE, lang).format(
                         name=content.text(w["name"], lang),
                         substitution=content.text(w["substitution"], lang)),
                     tag=t.div)
