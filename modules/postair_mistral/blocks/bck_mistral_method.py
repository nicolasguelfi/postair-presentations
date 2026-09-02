"""La méthode en 4 étapes (M4) — LA slide à photographier.

Quatre cartes numérotées sur UNE rangée (refonte NG 2026-09-02 : l'ancienne
étape « Fixe les limites » est FONDUE dans l'étape 1 — « Quelles limites ? »
fait partie du cadrage du rôle — et l'itération couvre instructions ET
sources). L'infobulle contient TOUT le détail opérationnel : le prompt
système complet de l'agent-exemple, l'essentiel de la taxonomie PE des
formations AISE trié à ~8 techniques (v0.2 ``pem4``), et le processus
Personas absorbé dans l'étape 4 (v0.2 ``personas`` — fusionné, pas
juxtaposé ; vocabulaire « Quasible » neutralisé).

Le FAIT partagé vit dans facts.json (section ``method``) : le récap M11
projette LES MÊMES quatre étapes — une seule vérité, deux consommateurs.
Aucune affirmation sourcée sur cette slide.

SPEAKER NOTES:
Three minutes — the heart of the session. One sentence per card, left to
right, then say it explicitly: « photograph THIS slide, the info panel of the
published version contains the full system prompt ». The four steps are the
transferable part: they work in Copilot, ChatGPT, Claude and Gemini alike.
"""
# @guideline: postair-minimal

from custom.facts import section, text
from custom.styles import Styles as s
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    number = s.project.titles.subtitle + s.project.colors.amber + s.center_txt + s.bold
    label = s.project.body.bullet + s.center_txt + s.bold
    line = s.project.body.caption + s.center_txt
    punch = s.project.titles.subtitle + s.project.colors.amber + s.center_txt


bs = BlockStyles

_MARKER = {"en": "The method", "fr": "La méthode"}
_TITLE = {"en": ("The method in ", (s.project.titles.keyword, "4 steps")), "fr": ("La méthode en ", (s.project.titles.keyword, "4 étapes"))}

_TIP_TITLE = {"en": "The four steps, operationally", "fr": "Les quatre étapes, opérationnellement"}
#: Le prompt système COMPLET de l'agent-exemple — la pièce que la salle vient
#: photographier. Une feuille par langue : l'étudiant colle la version de SA
#: langue (le prompt lui-même est un texte utilisateur, pas une UI).
_TIP_PROMPT = ({"en": "The full system prompt of the demo agent", "fr": "Le prompt système complet de l’agent de démo"},
               {"en": ("« You are a Socratic revision tutor for the course "
                       "[COURSE NAME]. Answer ONLY from the documents "
                       "provided; if the answer is not in them, say 'I don't "
                       "know — not covered in the provided material'. Cite "
                       "the section of the course with every answer. Ask me "
                       "a question before giving a full explanation. Never "
                       "write my assignments; if I paste one, critique my "
                       "draft instead. Keep answers under 200 words unless I "
                       "ask for more. »"), "fr": "« Tu es un tuteur socratique de révision pour le cours [NOM DU COURS]. Réponds UNIQUEMENT depuis les documents fournis ; si la réponse n’y est pas, dis “je ne sais pas — absent du matériel fourni”. Cite la section du cours à chaque réponse. Pose-moi une question avant de donner une explication complète. Ne rédige jamais mes devoirs ; si j’en colle un, critique mon brouillon à la place. Reste sous 200 mots sauf si je demande plus. »"})
#: v0.2 ``pem4`` : la taxonomie PE des formations, triée 30 → 8, une ligne
#: chacune — chaque technique doit SERVIR l'agent de révision.
_TIP_PE = ({"en": "Eight prompting techniques that serve the agent", "fr": "Huit techniques de prompt au service de l’agent"},
           {"en": ("Give examples (few-shot: paste a model Q&A) · think step "
                   "by step (ask for the reasoning before the answer) · "
                   "explicit constraints (length, level, language) · answer "
                   "template (« question, then hint, then solution ») · "
                   "decompose the problem (one chapter at a time) · iterate "
                   "incrementally (refine the last answer, do not restart) · "
                   "role/persona (the tutor role above) · direct questions "
                   "(one thing at a time)."), "fr": "Donner des exemples (few-shot : collez une paire question-réponse modèle) · pas à pas (demander le raisonnement avant la réponse) · contraintes explicites (longueur, niveau, langue) · gabarit de réponse (« question, puis indice, puis solution ») · décomposer le problème (un chapitre à la fois) · itérer par retouches (affiner la dernière réponse, ne pas repartir de zéro) · rôle/persona (le rôle de tuteur ci-dessus) · questions directes (une chose à la fois)."})
#: v0.2 ``personas`` : le processus en 6 étapes des formations, absorbé
#: dans l'étape 4 — spécifier → générer → documenter → tester → écarts → itérer.
_TIP_ITERATE = ({"en": "Step 4, like the professionals", "fr": "L’étape 4, comme les professionnels"},
                {"en": ("Iterating an agent is the same loop professionals "
                        "use to build personas: specify the expertise, have "
                        "the model generate its own role description, "
                        "document it, test it, list the gaps, iterate. Keep "
                        "a file with your instructions and what each change "
                        "fixed."), "fr": "Itérer un agent, c’est la boucle même des professionnels pour construire des personas : spécifier l’expertise, faire générer au modèle sa propre description de rôle, documenter, tester, lister les écarts, itérer. Gardez un fichier avec vos instructions et ce que chaque retouche a corrigé."})

# ── La main de l'artiste ────────────────────────────────────────────────────
TUNING = {
    #: UNE rangée de 4 : plancher 21 % (4 × 21 % + écarts < 100 %) — le même
    #: geste que les 4 familles de compétences de genai (porte projection).
    "cols": "repeat(auto-fit, minmax(max(260px, 21%), 1fr))",
    "card_zoom": 140,
}


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    steps = section("method")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with st_zoom(150), g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(text(step["label"], lang), text(step["detail"], lang))
                             for step in steps]
                            + [(T(_TIP_PROMPT[0], lang), T(_TIP_PROMPT[1], lang)),
                               (T(_TIP_PE[0], lang), T(_TIP_PE[1], lang)),
                               (T(_TIP_ITERATE[0], lang), T(_TIP_ITERATE[1], lang))],
                )
        st_space("v", s.project.spacing.title_gap)
        with st_grid(cols=TUNING["cols"], gap="1vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for step in steps:
                with g.cell(), st_block(s.project.cards.blue):
                    with st_zoom(130):
                        st_write(bs.number, step["n"], tag=t.div)
                    with st_zoom(TUNING["card_zoom"]):
                        st_write(bs.label, text(step["label"], lang), tag=t.div)
                        st_space("v", "0.6vh")
                        st_write(bs.line, text(step["line"], lang), tag=t.div)

