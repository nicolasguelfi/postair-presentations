"""AI in the faculty 2/3 — FDEF (série « AI concerns the whole University »).

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
_TITLE_ZOOM = 120   # le sigle en titre
_RATIO = 45         # part de largeur de la colonne image, en %
_ZOOM = 125         # st_zoom de la colonne des constats

# ── La faculté et sa scène ──────────────────────────────────────────────────
_MARKER = "FDEF"
_FACULTY = "Law, Economics and Finance"
_SCENE = ("A papercut law and finance scene: a paper courthouse column, a "
          "paper balance scale, a small stack of paper coins and a paper "
          "contract sheet with abstract cut-out lines, a glowing warm amber "
          "paper orb hovering above; one abstract paper silhouette seen from "
          "behind.")

# ── Les constats (headline projetée ; detail + caveat dans le tooltip) ──────
_EXAMPLES = [
    {
        "headline": "Legal AI tools still invent case law",
        "detail": ("Purpose-built legal research tools — sold to lawyers, "
                   "marketed as hallucination-free — still invent law: on "
                   "more than 200 open-ended legal queries, 17 % of Lexis+ AI "
                   "answers and 33 % of Westlaw AI-Assisted Research answers "
                   "were hallucinated."),
        "caveat": ("Paywalled; figures taken from the authors’ open preprint "
                   "and consistent secondary reporting. The vendors have "
                   "updated their systems since the queries were run."),
        "citekeys": ["magesh-hallucination-free-2025"],
        "reported": True,   # kind = reported-in : la note s'ajoute au tooltip
    },
    {
        "headline": "General models wrong most of the time",
        "detail": ("General-purpose models are far worse, and do not know "
                   "it: asked specific, verifiable questions about randomly "
                   "chosen US federal court cases, they hallucinated between "
                   "58 % of the time (GPT-4) and 88 % (Llama 2), and often "
                   "accepted a false legal premise handed to them in the "
                   "question."),
        "caveat": ("US case law. The failure mode — fluent, confident and "
                   "wrong — transfers to any jurisdiction; the rates do not."),
        "citekeys": ["dahl-legal-fictions-2024"],
        "reported": False,
    },
    {
        "headline": "Better inside the frontier, worse just outside",
        "detail": ("The edge is jagged, not general. Given eighteen "
                   "realistic consulting tasks, 758 consultants using GPT-4 "
                   "produced better and faster work on tasks inside the "
                   "model’s competence — and worse work than the control "
                   "group on tasks just outside it, because plausible wrong "
                   "answers were accepted uncritically."),
        "caveat": ("A working paper, run inside one consulting firm, and "
                   "co-authored with that firm. The concept it introduced — "
                   "the jagged frontier — has outlived the specific numbers."),
        "citekeys": ["dell-acqua-2023"],
        "reported": False,
    },
]

_REPORTED_NOTE = ("Reported inside the source cited on the card, not read at "
                  "the original.")


def build():
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
                            "faculty_fdef", prompt,
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
