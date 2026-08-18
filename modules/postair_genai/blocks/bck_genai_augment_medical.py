"""The diagnosis — 85 % vs 20 % (G6b, augmentation 1/3).

Première des trois slides « augmentation » (vision NG 2026-08-13) : l'IA
comme outil qui améliore massivement la qualité du résultat, chiffres
vérifiés à la source. Deux nombres géants face à face, l'image papier
découpé au centre, et la ligne de loyauté EN CLAIR sous le chiffre — les
conditions de l'étude font partie du message, pas des notes de bas de page.

Le FAIT vit ici (règle NG 2026-08-18) : chiffres, lignes de loyauté et choix
des citekeys s'éditent dans ce bloc. La phrase bibliographique reste dérivée
de ``references.bib`` par ``citation()``/``cite`` — clé inconnue = erreur
bruyante.

SPEAKER NOTES:
Two minutes. Let the two numbers land before speaking. Then read the grey
loyalty line OUT LOUD — hardest published cases, physicians cut off from
internet and colleagues, preprint — the room must hear that you know the
study's limits; that is what makes the number credible. If challenged on
"puzzles are not consultations", the AMIE line answers: in a randomized
BLINDED study of full diagnostic conversations — skin photos, ECGs and
documents included — the multimodal agent still beat the physicians on 7 of
9 multimodal axes; and its authors still say actors are not patients, and
run a real-hospital study before claiming more. Bridge to next slide: "so
should the doctor just hand over? Watch the twist."
"""
# @guideline: postair-minimal

from custom.prompts import AI_PREFIX, AI_SUFFIX_LANDSCAPE
from custom.refs import citation
from custom.styles import Styles as s
from custom.visuals import hero_image
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.hero_split import hero_split


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    number_ai = s.project.body.name_double + s.project.colors.amber + s.center_txt
    number_h = s.project.body.name_double + s.center_txt
    who = s.project.body.body + s.center_txt
    message = s.project.body.bullet + s.project.colors.primary + s.center_txt
    loyalty = s.project.body.caption + s.center_txt


bs = BlockStyles

_HERO_PROMPT = (
    AI_PREFIX
    + "A paper doctor as an abstract silhouette seen from behind, stethoscope "
      "shape cut from paper, facing a large glowing warm amber paper orb that "
      "projects light onto a big paper X-ray sheet held between them, the "
      "sheet showing a simple cut-out ribcage of turquoise and coral paper."
    + AI_SUFFIX_LANDSCAPE
)

# ── Le fait (ex-entrée « medical » de la section augment) ───────────────────
#: Jamais projeté, gardé pour la vérifiabilité — l'identifiant d'origine de
#: l'entrée : medical ; son pictogramme d'origine : 🩺.
_LABEL = "The diagnosis: 85 % vs 20 %"
_AI_VALUE = "85.5 %"
_AI_LABEL = "specialised AI orchestrator"
_HUMAN_VALUE = "20 %"
_HUMAN_LABEL = "21 experienced physicians"
_MESSAGE = "medicine's hardest cases · specialised AI ≫ unaided doctor"
#: La ligne de loyauté EN CLAIR : les conditions de l'étude font partie du
#: message, pas des notes de bas de page.
_LOYALTY = ("304 NEJM clinical puzzles · physicians without internet or "
            "colleagues · preprint, 2025")
_CONFIRM = ("confirmed in live dialogue: AMIE > GPs · 7/9 multimodal axes · "
            "blinded RCT — actors, not patients")
_CONFIRM_CITEKEYS = ["saab2025-amie"]
_DETAIL = ("Microsoft's MAI-DxO orchestrator solved 304 New England Journal "
           "of Medicine clinicopathological puzzles sequentially — ordering "
           "tests one by one — and reached 80 to 85.5 % correct diagnoses; "
           "21 experienced physicians on the same cases averaged about 20 %. "
           "Honest framing: these are the hardest published cases in "
           "medicine, the physicians were deprived of internet, textbooks "
           "and colleagues, and the study is a 2025 preprint, not yet "
           "peer-reviewed.")
_AMIE_DETAIL = ("AMIE (Google DeepMind, 2025): in a randomized, BLINDED "
                "OSCE-style study, the multimodal agent built on Gemini 2.0 "
                "Flash held full diagnostic conversations over 105 scenarios "
                "— interpreting smartphone skin photos, ECGs and clinical "
                "document PDFs — and was rated by specialists as superior to "
                "primary-care physicians on 7 of 9 multimodal axes and 29 of "
                "32 non-multimodal axes, diagnostic accuracy included. The "
                "authors' own working assumptions: patient ACTORS, not real "
                "patients; text-chat consultations, an unusual medium for "
                "physicians that hides non-verbal cues; a scenario set that "
                "under-represents both the complexity of real multimodal "
                "data and the expertise of clinicians. Their verbatim "
                "conclusion: further research is needed before real-world "
                "translation — a prospective consented study in a real "
                "clinical setting (Beth Israel Deaconess Medical Center) is "
                "underway.")
_CITEKEYS = ["nori2025sequential"]


def build():
    st_marker("Diagnosis")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "The diagnosis: ",
                         (s.project.titles.keyword, "85 % vs 20 %"),
                         tag=t.div, toc_lvl="+1", label="Diagnosis")
            with g.cell():
                st_info_tooltip(title=_LABEL,
                                entries=[("Verified at the source",
                                          _DETAIL),
                                         ("The multimodal check — AMIE",
                                          _AMIE_DETAIL)])
        st_space("v", s.project.spacing.title_gap)
        with hero_split(s, image=lambda: hero_image(
                "genai_diagnosis", _HERO_PROMPT,
                "images/genai_diagnosis_fallback.svg",
                alt_ready=("Papercut doctor silhouette from behind, facing an amber "
                           "orb lighting a paper X-ray sheet"),
                alt_fallback=("Papercut doctor silhouette and amber orb studying a "
                              "paper X-ray together"),
                variant="sq")):
            with st_block(s.project.cards.amber):
                st_write(bs.number_ai, _AI_VALUE, tag=t.div)
                st_write(bs.who, _AI_LABEL, tag=t.div)
            with st_block(s.project.cards.blue):
                st_write(bs.number_h, _HUMAN_VALUE, tag=t.div)
                st_write(bs.who, _HUMAN_LABEL, tag=t.div)
            st_space("v", "0.5vh")
            st_write(bs.message, _MESSAGE, " ",
                     citation(*_CITEKEYS), tag=t.div)
            st_write(bs.loyalty, _LOYALTY, tag=t.div)
            st_write(bs.loyalty, _CONFIRM, " ",
                     citation(*_CONFIRM_CITEKEYS), tag=t.div)
