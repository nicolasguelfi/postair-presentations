"""The question of the day: what is YOUR posture facing AI?

The pivot of the morning, and the slide where the survey stops being a form and
becomes a game. The image is a fairground wheel (NG 2026-08-03): three spokes
carry the name of an axis, the others a question mark, and the students in front
of the stall are about to find out which postures they win. The wheel says what
the empty radar could not — that nobody knows the answer yet, including us, and
that finding out is the point.

Produite en img2img sur le portrait de l'auteur, retenue à la troisième version
(NG 2026-08-03). Deux écarts à l'intention de départ ont été acceptés en
connaissance de cause, et il faut les connaître avant de vouloir « améliorer »
cette image :

- **le mot SURPRISE n'y est pas.** Le prompt le demande, le modèle l'écarte.
  Plus la consigne d'orthographe est stricte, plus il **supprime** le mot long
  au lieu de l'écrire — une version antérieure l'avait rendu « SURPRIST ». Les
  points d'interrogation portent la même idée sans risquer une faute projetée
  devant quinze cents personnes ;
- **le personnage est illustré, pas photographique.** Les versions qui gardaient
  le visage reconnaissable étaient celles qui se trompaient sur les mots.

Les versions écartées restent dans l'historique managé (``axes_wheel_v1``,
``axes_wheel_v2``) : on peut y revenir sans rien régénérer.

Tant que ``axes_wheel`` n'existe pas — sur un poste où l'historique managé
n'aurait pas été récupéré, par exemple — la slide montre le **radar vide**.
Ce n'est pas une précaution de principe : une slide qui attend une image
affiche un trou, et ``st_image`` préfère de lui-même la version managée dès
qu'elle est là.

SPEAKER NOTES:
This is the pivot: we stop talking about "AI in general" and start talking about
YOU. Play the fairground line — in a few minutes you spin the wheel and find out
which postures you carry. Announce the three registers (Knowing, Acting,
Becoming) that the next three slides unfold. Mention that the survey is
anonymous and grounded in a published scientific model.
"""
# @guideline: postair-minimal

from pathlib import Path

from custom.config import IS_EDITABLE
from custom.prompts import AI_PREFIX, AI_SUFFIX_LANDSCAPE_WITH_TEXT
from custom.refs import citation
from custom.styles import Styles as s
from custom.visuals import is_synthetic
from postair_i18n import ui
from postair_lang import T, TF, st_stage_lang_selector
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.ai_mark import dd35_overlay

#: Le nom managé de la roue, et l'endroit où l'éditeur l'enregistre.
_WHEEL = "axes_wheel"
_MANAGED = Path(__file__).parent.parent / "static" / "images" / "managed"

#: Ce que la slide montre tant que la roue n'existe pas : le radar vide, qui
#: pose la même question autrement. Une slide sans image n'est pas une étape
#: intermédiaire acceptable — c'est un trou devant l'amphithéâtre.
_FALLBACK = "images/postair_radar_question.svg"


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    grounding = s.project.body.caption + s.center_txt


bs = BlockStyles

#: The three axes named on the wheel. Chosen to be understood without a glossary
#: by a first-year student: they are everyday words before they are axes. The
#: other segments stay mute — that silence is the subject of the image.
WHEEL_AXES = ("TRUST", "SPEED", "OPTIMISM")

WHEEL_PROMPT = (
    AI_PREFIX
    + "A big fairground prize wheel made of layered cut paper, seen head on and "
      "caught mid-spin with a soft motion blur at its rim, standing on a festive "
      "paper fairground stall under bunting. The wheel is divided into eight "
      "bright segments, alternating between a word and a question mark as you go "
      "round. Going clockwise from the top, the eight segments read: "
    + ", then a large question mark, then ".join(WHEEL_AXES + ("SURPRISE",))
    + ", then a large question mark. Those four words are the only words in the "
      "whole image; spell each one exactly as written here, letter for letter, in "
      "clean bold capitals, large enough to be read across a lecture hall. A warm "
      "amber paper orb glows above the stall like a "
      "small sun. Three young students stand in front of the stall, seen from "
      "beside the wheel with one hand on its rim is the man from the reference "
      "photograph — same face, same glasses, same bald head and short beard — "
      "shown at full length in three-quarter view, rendered as a photographic "
      "cut-out pasted flat into the collage with visible torn paper edges and a "
      "soft drop shadow, in the manner of a photomontage. He is the only "
      "photographic element; everything else is cut paper."
    + AI_SUFFIX_LANDSCAPE_WITH_TEXT
)

#: La roue se fabrique en **img2img**, sur le portrait de l'auteur. Ce fichier
#: n'entre PAS dans le dépôt : il ne sert qu'au moment de la génération, sur la
#: machine de l'auteur, et seule l'image produite est versionnée. Un portrait
#: d'une personne réelle n'a rien à faire dans une image Docker publiée.
PORTRAIT = ("«git»/GENAI/ai4video-projects/augmented-student/assets/images/"
            "NG/_identity/portraits/ng__portrait__studio__v1.png")

# ── Le texte projeté (règle R-i18n) ──────────────────────────────────────────
_MARKER = {"en": "Your posture?", "fr": "Votre posture ?"}
_TITLE = {"en": ("What is ", (s.project.titles.keyword, "your posture"), " facing AI?"), "fr": ("Quelle est ", (s.project.titles.keyword, "votre posture"), " face à l'IA ?")}
_LABEL = {"en": "Getting started", "fr": "Pour commencer"}
_TIP_TITLE = {"en": "The POSTAIR model", "fr": "Le modèle POSTAIR"}
_TIP_POSTURE = ({"en": "A posture", "fr": "Une posture"},
                {"en": ("Your personal position facing the AI revolution — not "
                        "'for or against', but where you stand on nine fundamental "
                        "tensions. There is no right answer."), "fr": "Votre position personnelle face à la révolution de l'IA — pas « pour ou contre », mais là où vous vous situez sur neuf tensions fondamentales. Il n'y a pas de bonne réponse."})
#: Tête « Nine axes » : lexique (partagée avec la lecture du radar).
_TIP_AXES = {"en": ("Grouped in three registers: KNOWING (how I judge — trust, "
                    "optimism, rationality), ACTING (how I deploy — speed, "
                    "openness, freedom/control), BECOMING (what results — "
                    "centralisation, altruism, transhumanism)."), "fr": "Regroupés en trois registres : CONNAÎTRE (comment je juge — confiance, optimisme, rationalité), AGIR (comment je déploie l'IA — vitesse, ouverture, liberté/contrôle), DEVENIR (ce qui en résulte — centralisation, altruisme, transhumanisme)."}
_TIP_WHEEL = ({"en": "Why a wheel", "fr": "Pourquoi une roue"},
              {"en": ("Because nobody in this room knows their own answer yet. "
                      "You are not being sorted into anything — you are about "
                      "to discover which postures you already carry."), "fr": "Parce que personne dans cette salle ne connaît encore sa propre réponse. On ne vous range dans aucune case — vous allez découvrir quelles postures vous portez déjà."})
# La référence n'est PAS ici : elle vit derrière le code de citation visible
# sous la roue (un cite() dans un panneau de survol serait un hover-dans-hover).
_TIP_BASIS = ({"en": "Scientific basis", "fr": "Base scientifique"},
              {"en": ("The instrument derives from a published research "
                      "article — the citation under the wheel opens it."), "fr": "L'instrument dérive d'un article de recherche publié — la référence sous la roue y donne accès."})
#: Tête « Anonymous » : lexique (partagée avec la slide Welcome Week).
_TIP_ANON = {"en": ("The survey you are about to take is fully anonymous: your "
                    "result is computed on YOUR device; only anonymous averages "
                    "reach the room screen."), "fr": "Le sondage auquel vous allez répondre est entièrement anonyme : votre résultat est calculé sur VOTRE appareil ; seules des moyennes anonymes arrivent sur l'écran de la salle."}
_GROUNDING = {"en": "answers: anonymous · model: ", "fr": "réponses : anonymes · modèle : "}


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                # Ancre TOC de la partie 1 (ss12) : le label dit la PARTIE,
                # le titre visible garde la question qui la lance.
                with st_zoom(130):
                    st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="1", label=T(_LABEL, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[
                        (T(_TIP_POSTURE[0], lang), T(_TIP_POSTURE[1], lang)),
                        (ui("nine_axes", lang), T(_TIP_AXES, lang)),
                        (T(_TIP_WHEEL[0], lang), T(_TIP_WHEEL[1], lang)),
                        (T(_TIP_BASIS[0], lang), T(_TIP_BASIS[1], lang)),
                        (ui("anonymous", lang), T(_TIP_ANON, lang)),
                    ],
                )
        st_space("v", s.project.spacing.title_gap)
        # The wheel as large as the remaining viewport allows.
        with st_grid(cols="1fr 70% 1fr", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_space("h", "0.5vw")
            with g.cell():
                _wheel_image()
            with g.cell():
                st_space("h", "0.5vw")
        st_space("v", "1vh")
        # Le code de citation dans le texte VISIBLE de la slide : la carte au
        # survol porte la référence complète et le lien vers l'article.
        # Deux faits distincts, chacun avec son étiquette — « anonymous » seul
        # collé au code de citation se lisait comme « publication anonyme »
        # (incompris NG, 2026-08-13). La titulature complète du rapport
        # (titre, auteur, statut) vit dans la carte au survol du code.
        st_write(bs.grounding,
                 T(_GROUNDING, lang),
                 # inline : le code EST l'objet de l'étiquette « model: » —
                 # un retour à la ligne les séparerait et referait naître la
                 # lecture « publication anonyme » (incompris NG 2026-08-13).
                 citation("guelfi-postair", inline=True), tag=t.div)
        # Le sélecteur de langue de l'orateur (règle R-i18n, exception R-live) :
        # posé UNE fois, sur le premier bloc du module.
        st_stage_lang_selector()


def _wheel_image():
    """La roue — ou le radar vide tant qu'elle n'existe pas.

    ``uri`` est le REPLI, pas la source : dès qu'une version managée de
    ``axes_wheel`` existe, ``st_image`` la préfère et l'URI n'est plus lue.
    Rien à changer ici le jour de la génération.
    """
    ready = (_MANAGED / f"{_WHEEL}.webp").exists()
    st_image(
        s.project.cards.media_center, width="100%",
        uri="" if ready else _FALLBACK,
        alt=("Papercut fairground prize wheel, three segments naming an axis — "
             "trust, speed, optimism — the others marked with a large question "
             "mark, three students watching from the front and the host of the "
             "stall holding the rim") if ready else
            ("Empty nine-axis POSTAIR radar chart with a large question mark in "
             "the centre — axes: Trust, Optimism, Rationality, Speed, Openness, "
             "Freedom/Control, Centralisation, Altruism, Transhumanism"),
        editable=IS_EDITABLE, name=_WHEEL,
        prompt=WHEEL_PROMPT, provider="openai", ai_size="1536x1024",
        overlay=dd35_overlay(ready and is_synthetic(_WHEEL)))
