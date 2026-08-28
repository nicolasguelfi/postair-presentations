"""AI in the faculty 1/3 — FSTM (série « AI concerns the whole University »).

Composition de série (ex-gabarit ``faculty_slide``, NG 2026-08-13, 1 idée =
1 slide) : l'image papier découpé carrée à gauche (``hero_split``), à droite
les constats télégraphiques avec leurs codes de citation, et la réserve
d'honnêteté EN CLAIR sur chaque slide de la série. Les 3 blocs
``bck_faculty_*`` partagent cette composition : toute évolution s'y réplique
à la main.

Le FAIT vit ici (règle NG 2026-08-18) : constats, caveats et choix des
citekeys s'éditent dans ce bloc. La phrase bibliographique reste dérivée de
``references.bib`` par ``citation()`` — clé inconnue = erreur bruyante.
Exception : la réserve « no faculty data » est PARTAGÉE par les 3 slides et
reste servie par ``facts.json`` — ce qui sert plusieurs slides vit dans
``custom/``.
"""
# @guideline: postair-minimal

from shared_widgets import st_info_tooltip
from streamtex import st_block, st_grid, st_marker, st_space, st_write, st_zoom
from streamtex.enums import Tags as t

from custom.facts import no_faculty_data, text
from custom.prompts import AI_PREFIX, AI_SUFFIX_LANDSCAPE
from custom.refs import citation
from custom.styles import Styles as s
from custom.visuals import hero_image
from postair_pack.components.hero_split import hero_split


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    headline = s.project.body.bullet + s.center_txt
    reserve = s.project.body.caption + s.project.colors.amber + s.center_txt


bs = BlockStyles

# ── Réglages de la slide ────────────────────────────────────────────────────
_TITLE_ZOOM = 115   # le sigle en titre
_RATIO = 35         # part de largeur de la colonne image, en %
_ZOOM = 125         # st_zoom de la colonne des constats

# ── La faculté et sa scène ──────────────────────────────────────────────────
_MARKER = "FSTM"
_FACULTY = "Science, Technology and Medicine"
_SCENE = ("A papercut science and technology scene: a large paper laptop "
          "showing cut-out code blocks, a paper flask and a small paper gear "
          "beside it, a glowing warm amber paper orb hovering over the desk; "
          "one abstract paper silhouette seen from behind.")

# ── Les constats (headline projetée ; detail + caveat dans le tooltip) ──────
_EXAMPLES = [
    {
        "headline": "Codex > median CS1 student",
        "detail": ("Introductory programming stopped being a filter. In 2022 "
                   "OpenAI Codex already scored above the median student on a "
                   "CS1 final exam; a year later it still beat median "
                   "students on second-year data-structure exercises, though "
                   "the margin narrowed on problems requiring novel design."),
        "caveat": ("Measured on exams as they were written at the time. The "
                   "result is as much about assessment design as about the "
                   "model."),
        "citekeys": ["finnie-ansley2022", "finnie-ansley2023"],
        "reported": False,
    },
    # Rééquilibrage NG 2026-08-19 : un bénéfice net entre la capacité et le
    # risque — l'essai randomisé JAMA sur le raisonnement diagnostique.
    {
        "headline": "GPT-4 out-diagnosed the unaided physicians",
        "detail": ("In a randomized clinical trial on six complex diagnostic "
                   "vignettes, GPT-4 alone reached a median reasoning score "
                   "of 92 % against 74 % for 50 physicians using their usual "
                   "tools — and 76 % when the physicians were given GPT-4: "
                   "the tool alone is not enough, collaborating with it is "
                   "learned."),
        "caveat": ("Fifty physicians, six vignettes — a controlled reasoning "
                   "benchmark, not patient outcomes."),
        "citekeys": ["goh2024llm"],
        "reported": False,
    },
    {
        "headline": "the least accurate student but the most confident",
        "detail": ("In medicine the danger is confidence, not error. Medical "
                   "students working virtual patient cases with AI support "
                   "and no human feedback produced the least accurate "
                   "diagnoses of the whole cohort — and were the most "
                   "confident of any group."),
        "caveat": ("Reported inside the HEPI survey; the underlying study was "
                   "not opened. Cite the primary paper before using this in "
                   "any policy setting."),
        "citekeys": ["isabel-virtual-patients", "hepi-survey-2026"],
        "reported": True,   # kind = reported-in : la note s'ajoute au tooltip
    },
]

_REPORTED_NOTE = ("Reported inside the source cited on the card, not read at "
                  "the original.")


def build(lang: str = "en", **_):
    st_marker(_MARKER)
    prompt = AI_PREFIX + _SCENE + AI_SUFFIX_LANDSCAPE
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                # Le sigle en titre (une ligne) — le nom complet de la
                # faculté vit dans le titre du tooltip.
                with st_zoom(_TITLE_ZOOM):
                    st_write(bs.title, "AI in ",
                             (s.project.titles.keyword, _MARKER),
                             tag=t.div, toc_lvl="+1", label=_MARKER)
            with g.cell():
                entries = [(ex["headline"],
                            " ".join([ex["detail"], ex["caveat"]]
                                     + ([_REPORTED_NOTE] if ex["reported"]
                                        else [])))
                           for ex in _EXAMPLES]
                entries.append(("No figures for this university",
                                text(no_faculty_data())))
                st_info_tooltip(title=f"{_FACULTY} — the evidence",
                                entries=entries)
        st_space("v", s.project.spacing.title_gap)
        with hero_split(s, ratio=_RATIO, zoom=_ZOOM,
                        image=lambda: hero_image(
                            "faculty_fstm", prompt,
                            "images/postair_radar_question.svg",
                            alt_ready=f"Papercut scene for {_MARKER}",
                            alt_fallback=f"Papercut scene for {_MARKER}",
                            variant="sq", width="100%")):
            for ex in _EXAMPLES:
                st_write(bs.headline, "▸ ",
                         ex["headline"] + " " + citation(*ex["citekeys"]),
                         tag=t.div)
            st_space("v", "0.5vh")
            st_write(bs.reserve, text(no_faculty_data()["headline"]), tag=t.div)
