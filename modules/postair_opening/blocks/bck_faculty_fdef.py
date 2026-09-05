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
from postair_i18n import ui
from postair_lang import T
from postair_pack.components.hero_split import hero_split


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    headline = s.project.body.bullet + s.center_txt
    reserve = s.project.body.caption + s.project.colors.amber + s.center_txt


bs = BlockStyles

# ── Réglages de la slide ────────────────────────────────────────────────────
_TITLE_ZOOM = 120   # le sigle en titre
_RATIO = 35         # part de largeur de la colonne image, en %
_ZOOM = 115         # st_zoom de la colonne des constats

# ── La faculté et sa scène ──────────────────────────────────────────────────
_MARKER = {"en": "FDEF", "fr": "FDEF"}
_FACULTY = {"en": "Law, Economics and Finance", "fr": "Droit, Économie et Finance"}
_SCENE = ("A papercut law and finance scene: a paper courthouse column, a "
          "paper balance scale, a small stack of paper coins and a paper "
          "contract sheet with abstract cut-out lines, a glowing warm amber "
          "paper orb hovering above; one abstract paper silhouette seen from "
          "behind.")

# ── Les constats (headline projetée ; detail + caveat dans le tooltip) ──────
# Rééquilibrage NG 2026-08-19 : autant de bénéfices que de revers — deux
# résultats positifs solides (Kleinberg, Posner & Saran), un revers documenté
# (Magesh), et la synthèse honnête en clôture (Dell'Acqua). Dahl et al. 2024
# (les modèles généralistes, 58–88 % d'hallucinations) quitte la projection —
# son message est porté par Magesh — mais reste en précision de tooltip.
_EXAMPLES = [
    {
        "headline": {"en": "AI -> −24.7 % crime, same jailing rate", "fr": "IA -> criminalité −24,7 %, prison inchangée"},
        "detail": {"en": ("On New York pre-trial release decisions, following a "
                   "machine-learning risk prediction instead of the judge "
                   "would cut crime by up to 24.7 % at an unchanged jailing "
                   "rate — or cut jailing by 41.9 % at unchanged crime."), "fr": "À New York, sur les libérations avant procès, suivre une prédiction de risque par apprentissage automatique plutôt que le juge ferait baisser la criminalité jusqu'à 24,7 % à incarcération inchangée — ou l'incarcération de 41,9 % à criminalité inchangée."},
        "caveat": {"en": ("A policy simulation on real dossiers, not a deployment. "
                   "And specialised is no automatic guarantee: the commercial "
                   "COMPAS tool predicted recidivism at 65.2 % against "
                   "64.0 % for untrained laypeople (Dressel & Farid, 2018)."), "fr": "Une simulation de politique publique sur des dossiers réels, pas un déploiement. Et un outil spécialisé ne garantit rien d'office : l'outil commercial COMPAS prédisait la récidive à 65,2 % contre 64,0 % pour des profanes sans formation (Dressel & Farid, 2018)."},
        "citekeys": ["kleinberg2018human"],
        "reported": False,
    },
    {
        "headline": {"en": "The model follows precedent — the judges followed sympathy", "fr": "Le modèle suit la jurisprudence — les juges, la sympathie"},
        "detail": {"en": ("A controlled experiment once run on 31 real US federal "
                   "judges was replicated with GPT-4o judging the same full "
                   "case file: the model follows legal precedent and ignores "
                   "the defendant’s sympathy — the exact opposite of the "
                   "human judges in the original experiment."), "fr": "Une expérience contrôlée menée auparavant sur 31 vrais juges fédéraux américains a été répliquée avec GPT-4o jugeant le même dossier complet : le modèle suit la jurisprudence et ignore la sympathie qu’inspire l’accusé — l’exact inverse des juges humains de l’expérience originale."},
        "caveat": {"en": ("A replication case-study on one experimental protocol — "
                   "a laboratory result, not a courtroom record."), "fr": "Une étude de cas répliquant un seul protocole expérimental — un résultat de laboratoire, pas une décision de tribunal."},
        "citekeys": ["posner2026judgeai"],
        "reported": False,
    },
    {
        "headline": {"en": "Legal AI tools still invent case law", "fr": "L’IA juridique invente encore des arrêts"},
        "detail": {"en": ("Purpose-built legal research tools — sold to lawyers, "
                   "marketed as hallucination-free — still invent law: on "
                   "more than 200 open-ended legal queries, 17 % of Lexis+ AI "
                   "answers and 33 % of Westlaw AI-Assisted Research answers "
                   "were hallucinated. General-purpose models do far worse "
                   "still — 58 % to 88 % hallucination rates on verifiable "
                   "case-law questions (Dahl et al., 2024)."), "fr": "Des outils de recherche juridique dédiés — vendus aux avocats, présentés comme sans hallucination — inventent encore du droit : sur plus de 200 questions juridiques ouvertes, 17 % des réponses de Lexis+ AI et 33 % de celles de Westlaw AI-Assisted Research étaient hallucinées. Les modèles généralistes font bien pire encore — 58 % à 88 % d’hallucinations sur des questions de jurisprudence vérifiables (Dahl et al., 2024)."},
        "caveat": {"en": ("Paywalled; figures taken from the authors’ open preprint "
                   "and consistent secondary reporting. The vendors have "
                   "updated their systems since the queries were run."), "fr": "Accès payant ; chiffres tirés de la prépublication ouverte des auteurs et de comptes rendus secondaires concordants. Les éditeurs ont mis à jour leurs systèmes depuis que les requêtes ont été lancées."},
        "citekeys": ["magesh-hallucination-free-2025"],
        "reported": True,   # kind = reported-in : la note s'ajoute au tooltip
    },
    {
        "headline": {"en": "Better inside the frontier, worse outside", "fr": "Meilleur en deçà de la frontière, pire au-delà"},
        "detail": {"en": ("The edge is jagged, not general. Given eighteen "
                   "realistic consulting tasks, 758 consultants using GPT-4 "
                   "produced better and faster work on tasks inside the "
                   "model’s competence — and worse work than the control "
                   "group on tasks just outside it, because plausible wrong "
                   "answers were accepted uncritically."), "fr": "L’avantage est dentelé, pas uniforme. Sur dix-huit tâches de conseil réalistes, 758 consultants utilisant GPT-4 ont produit un travail meilleur et plus rapide sur les tâches que le modèle maîtrise — et moins bon que le groupe témoin sur celles juste au-delà, parce que des réponses fausses mais plausibles étaient acceptées sans esprit critique."},
        "caveat": {"en": ("A working paper, run inside one consulting firm, and "
                   "co-authored with that firm. The concept it introduced — "
                   "the jagged frontier — has outlived the specific numbers."), "fr": "Un document de travail, mené dans un seul cabinet de conseil et cosigné avec ce cabinet. Le concept qu’il a introduit — la frontière dentelée — a survécu aux chiffres précis."},
        "citekeys": ["dell-acqua-2023"],
        "reported": False,
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
                            "faculty_fdef", prompt,
                            "images/postair_radar_question.svg",
                            alt_ready=f"Papercut scene for {marker}",
                            alt_fallback=f"Papercut scene for {marker}",
                            variant="sq", width="100%")):
            for ex in _EXAMPLES:
                st_write(bs.headline, "▸ ",
                         T(ex["headline"], lang) + " " + citation(*ex["citekeys"], inline=True),
                         tag=t.div)
            st_space("v", "0.5vh")
            st_write(bs.reserve, text(no_faculty_data()["headline"], lang), tag=t.div)
