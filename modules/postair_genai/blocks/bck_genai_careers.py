"""And for your future jobs? (G10) — transformation, not disappearance.

Three faculty cards (the visual loop with the morning's whole-university
slide), one frame line sourced with its visible citation code, and the rising
skill in amber.

Le FAIT vit ici (règle NG 2026-08-18) : les cartes par faculté s'éditent dans
ce bloc. EXCEPTION (revue genaipat 2026-09-01) : le fait WEF (55 économies ·
39 % · 2030, clé wef2025-jobs) est PARTAGÉ avec ``bck_genai_future_pm`` — il
vit dans ``facts.json`` (section ``jobs``), chaque slide garde sa formulation
autour de lui. La phrase bibliographique reste dérivée de ``references.bib``
par ``citation()``/``cite`` — clé inconnue = erreur bruyante.

SPEAKER NOTES:
Three minutes, one card per third of the room, like the morning. The framing
number is behind the code — 39 % of core skills change by 2030 — say it with
its uncertainty: employer expectations, not destiny. Land on the amber line:
the skill that rises fastest is JUDGING what the AI produced, and judging
requires knowing the domain. That is why they are here for years, not weeks.
"""
# @guideline: postair-minimal

from custom.facts import citekeys, section, text
from custom.refs import citation
from custom.styles import Styles as s
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.design_systems.postair_dark import AMBER, TEXT


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    faculty = s.project.body.pole_label + s.center_txt
    pair = s.project.titles.subtitle + s.project.colors.keyword + s.center_txt
    frame = s.project.body.body + s.center_txt
    rising = s.project.titles.subtitle + s.project.colors.amber + s.center_txt


bs = BlockStyles

#: Le duo « humain + IA » de chaque carte — compositions de ``Style`` (R11,
#: revue genaipat 2026-09-01 : l'ancien st_html portait texte et ambre en
#: dur). L'IA est l'étincelle ✦ en ambre (choix NG 2026-09-02 : le code
#: graphique universel de l'IA, préféré à l'orbe interne du deck) — même
#: geste, zéro HTML. Sans pastille ni fond : aucune confusion possible avec
#: la marque de divulgation DD-35 « ✦ AI ».
_DUO_LINE = Style("text-align: center; padding: 0.6vh 0;", "genai_duo_line")
_DUO_HUMAN = Style("font-size: 3.2vw;", "genai_duo_human")
_DUO_PLUS = Style(f"font-size: 2vw; color: {TEXT};", "genai_duo_plus")
#: ✦ doublé (2.6 → 5.2vw, demande NG 2026-09-02) — la taille d'un fragment
#: se règle par SON style, jamais par un st_zoom englobant (qui zoomerait le
#: bloc entier sur sa propre ligne).
_DUO_ORB = Style(f"font-size: 5.2vw; color: {AMBER}; vertical-align: middle;",
                 "genai_duo_orb")

# ── Les trois duos par faculté (carte projetée ; détail au survol) ──────────
#: Jamais projeté, gardé pour la vérifiabilité — les identifiants d'origine
#: des cartes : health, law, science.
_CAREERS = [
    {
        "faculty": {"en": "Medicine & health", "fr": "Médecine & santé"},
        "pair": {"en": "the clinician + AI", "fr": "le clinicien + IA"},
        "detail": {"en": ("Imaging triage, protein structures, paperwork — and a "
                          "human who decides, explains and carries responsibility."), "fr": "Tri d’imagerie, structures de protéines, paperasse — et un humain qui décide, explique et porte la responsabilité."},
    },
    {
        "faculty": {"en": "Law, economics, finance", "fr": "Droit, économie, finance"},
        "pair": {"en": "the jurist + AI", "fr": "le juriste + IA"},
        "detail": {"en": ("Research and drafting accelerate; judgement, strategy "
                          "and accountability do not delegate."), "fr": "La recherche et la rédaction s’accélèrent ; le jugement, la stratégie et la responsabilité ne se délèguent pas."},
    },
    {
        "faculty": {"en": "Science & engineering", "fr": "Sciences & ingénierie"},
        "pair": {"en": "the scientist + AI", "fr": "le scientifique + IA"},
        "detail": {"en": ("Hypothesis search, code, literature triage — and the "
                          "experiment, the proof and the doubt stay yours."), "fr": "Recherche d’hypothèses, code, tri de la littérature — et l’expérience, la preuve et le doute restent à vous."},
    },
]

# ── La ligne-cadre (forme courte projetée ; phrase complète au survol) ──────
#: Le chiffre et sa phrase viennent du fait partagé ``jobs``/``wef-outlook``
#: de facts.json — une seule vérité pour les deux slides qui le projettent.
_FRAME_CLAIM = {"en": "Transformation, not disappearance", "fr": "Transformation, pas disparition"}
_FRAME_RISING = {"en": "Fastest-rising skill: JUDGING what the AI produced", "fr": "La compétence qui monte le plus vite : JUGER ce que l’IA a produit"}

_MARKER = {"en": "Your jobs", "fr": "Vos métiers"}
_TITLE = {"en": ("And for your ", (s.project.titles.keyword, "future jobs"), "?"), "fr": ("Et pour vos ", (s.project.titles.keyword, "futurs métiers"), " ?")}
_TIP_TITLE = {"en": "What the evidence says", "fr": "Ce que disent les preuves"}
_TIP_DURABLE = ({"en": "The durable skills", "fr": "Les compétences durables"},
                {"en": ("Critical thinking, domain expertise, ethics: piloting "
                        "an AI requires knowing the field better than it does."), "fr": "Esprit critique, expertise du domaine, éthique : piloter une IA exige de connaître le champ mieux qu’elle."})


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    wef = next(f for f in section("jobs") if f["id"] == "wef-outlook")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with st_zoom(150), g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(T(c["faculty"], lang), T(c["detail"], lang))
                             for c in _CAREERS]
                            + [(T(_FRAME_CLAIM, lang), text(wef["claim"], lang)),
                               (T(_TIP_DURABLE[0], lang), T(_TIP_DURABLE[1], lang))],
                )
        st_space("v", s.project.spacing.title_gap)
        with st_grid(cols=s.project.grids.balanced(len(_CAREERS)), gap="1.2vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for c in _CAREERS:
                with g.cell(), st_block(s.project.cards.blue):
                    with st_zoom(120):
                        st_write(bs.faculty, T(c["faculty"], lang), tag=t.div)
                    st_space("v", "0.6vh")
                    # Silhouette humaine + orbe côte à côte (plan G10) : le
                    # duo est le visuel de la carte, pas une décoration.
                    st_write(_DUO_LINE,
                             (_DUO_HUMAN, "👤"), (_DUO_PLUS, " + "),
                             (_DUO_ORB, "✦"), tag=t.div)
                    st_write(bs.pair, T(c["pair"], lang), tag=t.div)
        st_space("v", "1vh")
        # Télégraphique (NG 2026-08-13) : la phrase-cadre complète vit dans
        # l'infobulle ; l'écran porte la forme courte. Pied à zoom 90 (porte
        # projection 2026-09-02 : la ligne ambre repliée en deux débordait
        # de ×1.08 à 1920×1080).
        with st_zoom(130):
            st_write(bs.frame, T(_FRAME_CLAIM, lang), " · ", text(wef["short"], lang), " ",
                     citation(*citekeys(wef)), tag=t.div)
            st_space("v", "1vh")
            st_write(bs.rising, T(_FRAME_RISING, lang), tag=t.div)
