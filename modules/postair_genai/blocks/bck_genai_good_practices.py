"""Good Practices for the AI Augmented Student — l'ouverture de section (G8½).

Insertion NG (2026-09-02) : une slide-titre qui ouvre la seconde moitié du
deck — tout ce qui suit (tes données, ton cerveau, les garde-fous, le
tuteur, l'examen, les carrières, le chef de projet de tes assistants, la
posture) n'est plus « ce que la machine rate » mais « comment TOI tu t'en
sers bien ». Une image papier découpé dominante symbolise le titre :
l'étudiant en chemin, l'orbe ambre en compagnon d'épaule, les jalons des
bonnes pratiques au bord du sentier.

L'image suit le circuit managé habituel (``staged_hero_image`` : la version
générée par NG via l'éditeur prendra la place dès qu'elle existera sous
``static/images/managed/genai_practices*.webp``) ; d'ici là le repli SVG
versionné ``genai_practices_fallback.svg`` tient l'écran — une slide sans
image n'est pas une étape acceptable (règle du dépôt).

Le FAIT vit ici (règle NG 2026-08-18) : titre, carte de section du panneau.
Aucune affirmation sourcée.

SPEAKER NOTES:
Fifteen seconds — a breath, not a lecture. Announce the turn: « you now know
what it is and what it gets wrong — the rest of this session is about YOU
using it well ». Then walk the path: data, brain, guardrails, tutor, exam,
careers, your posture. PageDown without lingering.
"""
# @guideline: postair-minimal

from custom.prompts import AI_PREFIX, AI_SUFFIX_LANDSCAPE
from custom.styles import Styles as s
from custom.visuals import staged_hero_image
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt


bs = BlockStyles

_MARKER = {"en": "Good practices", "fr": "Bonnes pratiques"}
#: Le titre sur DEUX lignes (retouche NG 2026-09-02 — son ``\n`` d'intention
#: rendu par deux écritures : ``st_write`` n'interprète pas le ``\n``,
#: piège documenté au PLAYBOOK).
_TITLE_L1 = {"en": "Good practices for the", "fr": "Les bonnes pratiques de"}
_TITLE_L2 = {"en": ((s.project.titles.keyword, "AI-AUGMENTED"), " STUDENT"), "fr": ((s.project.titles.keyword, "l’ÉTUDIANT AUGMENTÉ"), " PAR L’IA")}

_TIP_TITLE = {"en": "This second half", "fr": "Cette seconde moitié"}
_TIP = [
    ({"en": "The turn", "fr": "Le tournant"},
     {"en": ("You now know what generative AI is and what it gets wrong — "
             "everything from here is about USING it well as a student."), "fr": "Vous savez désormais ce qu’est l’IA générative et ce qu’elle rate — tout ce qui suit porte sur la manière de BIEN l’utiliser en tant qu’étudiant."}),
    ({"en": "The path", "fr": "Le chemin"},
     {"en": ("Your data (read what you sign) · your brain (a muscle) · the "
             "guardrails · the tireless tutor · the exam stays human · "
             "careers transform · project manager of your assistants · "
             "your posture."), "fr": "Vos données (lisez ce que vous signez) · votre cerveau (un muscle) · les garde-fous · le tuteur infatigable · l’examen reste humain · les carrières se transforment · chef de projet de vos assistants · votre posture."}),
    ({"en": "Where the rules live", "fr": "Où vivent les règles"},
     {"en": ("The official UL guidelines are the session after Mistral — "
             "this half gives you the reflexes they formalise."), "fr": "Les lignes directrices officielles de l’UL sont la session qui suit Mistral — cette moitié vous donne les réflexes qu’elles formalisent."}),
]

#: La main de l'artiste (pattern TUNING) : budget hauteur de l'image héro.
TUNING = {"hero_vh": 62}

_HERO_PROMPT = (
    AI_PREFIX
    + "A paper student silhouette with a small backpack walking along a "
      "luminous winding paper path toward a bright horizon, a warm amber "
      "paper orb hovering at shoulder height like a companion lighting the "
      "way; along the path, small bright paper milestones: a checklist "
      "card, a compass, a shield with a check mark."
    + AI_SUFFIX_LANDSCAPE
)


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, T(_TITLE_L1, lang),
                         tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
                st_write(bs.title, *TF(_TITLE_L2, lang), tag=t.div)
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(T(h, lang), T(d, lang)) for h, d in _TIP],
                )
        st_space("v", "3vh")
        with st_zoom(110):
            staged_hero_image(
                "genai_practices", _HERO_PROMPT,
                "images/genai_practices_fallback.svg",
                alt_ready=("Papercut student walking a luminous path with an amber "
                        "orb companion, milestones of good practices along the "
                        "way"),
                alt_fallback=("Papercut student on a winding path, amber orb at "
                            "the shoulder, checklist, compass and shield "
                            "milestones"),
                stage_vh=TUNING["hero_vh"],
            )
