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
from postair_i18n import ui
from postair_lang import T
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
_MARKER = {"en": "FSTM", "fr": "FSTM"}
_FACULTY = {"en": "Science, Technology and Medicine", "fr": "Sciences, Technologies et Médecine"}
_SCENE = ("A papercut science and technology scene: a large paper laptop "
          "showing cut-out code blocks, a paper flask and a small paper gear "
          "beside it, a glowing warm amber paper orb hovering over the desk; "
          "one abstract paper silhouette seen from behind.")

# ── Les constats (headline projetée ; detail + caveat dans le tooltip) ──────
_EXAMPLES = [
    {
        "headline": {"en": "Codex > median CS1 student", "fr": "Codex > étudiant médian en CS1"},
        "detail": {"en": ("Introductory programming stopped being a filter. In 2022 "
                   "OpenAI Codex already scored above the median student on a "
                   "CS1 final exam; a year later it still beat median "
                   "students on second-year data-structure exercises, though "
                   "the margin narrowed on problems requiring novel design."), "fr": "L'initiation à la programmation n'est plus un filtre. En 2022, OpenAI Codex dépassait déjà l'étudiant médian à un examen final de CS1 ; un an plus tard, il battait encore les étudiants médians sur des exercices de structures de données de deuxième année, avec une marge plus étroite sur les problèmes qui demandaient une conception nouvelle."},
        "caveat": {"en": ("Measured on exams as they were written at the time. The "
                   "result is as much about assessment design as about the "
                   "model."), "fr": "Mesuré sur les examens tels qu'ils étaient rédigés à l'époque. Le résultat en dit autant sur la conception des évaluations que sur le modèle."},
        "citekeys": ["finnie-ansley2022", "finnie-ansley2023"],
        "reported": False,
    },
    # Rééquilibrage NG 2026-08-19 : un bénéfice net entre la capacité et le
    # risque — l'essai randomisé JAMA sur le raisonnement diagnostique.
    {
        "headline": {"en": "GPT-4 out-diagnosed the unaided physicians", "fr": "GPT-4 diagnostique mieux que les médecins seuls"},
        "detail": {"en": ("In a randomized clinical trial on six complex diagnostic "
                   "vignettes, GPT-4 alone reached a median reasoning score "
                   "of 92 % against 74 % for 50 physicians using their usual "
                   "tools — and 76 % when the physicians were given GPT-4: "
                   "the tool alone is not enough, collaborating with it is "
                   "learned."), "fr": "Dans un essai clinique randomisé sur six vignettes diagnostiques complexes, GPT-4 seul a atteint un score médian de raisonnement de 92 % contre 74 % pour 50 médecins avec leurs outils habituels — et 76 % quand les médecins disposaient de GPT-4 : l'outil seul ne suffit pas, collaborer avec lui s'apprend."},
        "caveat": {"en": ("Fifty physicians, six vignettes — a controlled reasoning "
                   "benchmark, not patient outcomes."), "fr": "Cinquante médecins, six vignettes — un test de raisonnement contrôlé, pas des résultats cliniques."},
        "citekeys": ["goh2024llm"],
        "reported": False,
    },
    {
        "headline": {"en": "The least accurate student but the most confident", "fr": "L’étudiant le moins exact mais le plus sûr de lui"},
        "detail": {"en": ("In medicine the danger is confidence, not error. Medical "
                   "students working virtual patient cases with AI support "
                   "and no human feedback produced the least accurate "
                   "diagnoses of the whole cohort — and were the most "
                   "confident of any group."), "fr": "En médecine, le danger, c'est l'excès de confiance, pas l'erreur. Des étudiants en médecine travaillant des cas de patients virtuels avec une aide IA et sans retour humain ont produit les diagnostics les moins exacts de toute la cohorte — et étaient les plus sûrs d'eux de tous les groupes."},
        "caveat": {"en": ("Reported inside the HEPI survey; the underlying study was "
                   "not opened. Cite the primary paper before using this in "
                   "any policy setting."), "fr": "Rapporté dans l'enquête HEPI ; l'étude sous-jacente n'a pas été consultée. Citez l'article original avant de l'utiliser dans tout cadre décisionnel."},
        "citekeys": ["isabel-virtual-patients", "hepi-survey-2026"],
        "reported": True,   # kind = reported-in : la note s'ajoute au tooltip
    },
]

def build(lang: str = "en", **_):
    marker = T(_MARKER, lang)
    st_marker(marker)
    prompt = AI_PREFIX + _SCENE + AI_SUFFIX_LANDSCAPE
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                # Le sigle en titre (une ligne) — le nom complet de la
                # faculté vit dans le titre du tooltip.
                with st_zoom(_TITLE_ZOOM):
                    st_write(bs.title, ui("ai_in", lang),
                             (s.project.titles.keyword, marker),
                             tag=t.div, toc_lvl="+1", label=marker)
            with g.cell():
                entries = [(T(ex["headline"], lang),
                            " ".join([T(ex["detail"], lang), T(ex["caveat"], lang)]
                                     + ([ui("reported_note", lang)]
                                        if ex["reported"] else [])))
                           for ex in _EXAMPLES]
                entries.append((ui("no_figures_university", lang),
                                text(no_faculty_data(), lang)))
                st_info_tooltip(
                    title=ui("faculty_evidence", lang).format(
                        faculty=T(_FACULTY, lang)),
                    entries=entries)
        st_space("v", s.project.spacing.title_gap)
        with hero_split(s, ratio=_RATIO, zoom=_ZOOM,
                        image=lambda: hero_image(
                            "faculty_fstm", prompt,
                            "images/postair_radar_question.svg",
                            alt_ready=f"Papercut scene for {marker}",
                            alt_fallback=f"Papercut scene for {marker}",
                            variant="sq", width="100%")):
            for ex in _EXAMPLES:
                st_write(bs.headline, "▸ ",
                         T(ex["headline"], lang) + " " + citation(*ex["citekeys"]),
                         tag=t.div)
            st_space("v", "0.5vh")
            st_write(bs.reserve, text(no_faculty_data()["headline"], lang), tag=t.div)
