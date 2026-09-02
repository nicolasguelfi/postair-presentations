"""It can refuse (G8e) — les garde-fous, après les revers.

Insertion draft des formations (planche drafts2 ``flux=refus``, NG
2026-09-01) : la seule pièce « sécurité » de tout le matériel, placée en
CONTREPOINT honnête à la fin de la série G8 (les revers) — le deck vient de
dire biais, contrôle, données, cerveau ; cette slide dit qu'en face, des
garde-fous existent, imparfaits et inégaux.

La preuve est une EXPÉRIENCE des formations AISE de NG (2024, réutilisation
autorisée 2026-09-01) : le MÊME message hostile soumis au modèle de
modération d'OpenAI en français puis en anglais — les deux tables de scores
sont projetées, PAS la phrase testée (improjetable devant 1500 primo-
arrivants ; sa nature est décrite au panneau, décision d'assainissement
2026-09-01, planche drafts2). Les filtres notent l'INTENTION dans les deux
langues — avec des écarts visibles entre langues (violence 20 % ↔ 35 %).

Captures d'interface (pas d'images générées) : pas de pastille DD-35.

Le FAIT vit ici (règle NG 2026-08-18) : démonstration documentée, datée,
reproductible — pas une affirmation de littérature : pas de citekey (même
statut que les captures d'écrans DD-113). Le renvoi réglementaire (AI Act)
vit en annexe BACKUP.

SPEAKER NOTES:
One minute. Recall the room already saw refusals: ask ChatGPT how to build a
bomb, it says no. This slide shows the machinery BEHIND that no: a second
model scores every message. Same hostile message, French then English — the
categories light up in BOTH languages: filters read intent, not keywords.
Then the amber line, slowly: guardrails exist · imperfect · uneven across
tools and languages. If the room asks « can they be bypassed? »: yes,
jailbreaks exist, it is an arms race — honesty is the deck's line.
"""
# @guideline: postair-minimal

from postair_i18n import ui
from custom.styles import Styles as s
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    lang_label = s.project.body.bullet + s.center_txt + s.bold
    caption = s.project.body.caption + s.center_txt
    punch = s.project.titles.subtitle + s.project.colors.amber + s.center_txt


bs = BlockStyles

#: Réglages datés (2026-09-01) : les tables sont hautes (portrait ~0.9) —
#: la hauteur de scène est la contrainte utile.
TUNING = {"table_vh": 62}

#: Ratio largeur/hauteur DU FICHIER (mesuré Pillow 2026-09-01).
_TABLES = [
    {"uri": "images/trainings/moderation_fr.png", "ratio": 0.941,
     "label": {"en": "Français", "fr": "Français"}},
    {"uri": "images/trainings/moderation_en.png", "ratio": 0.879,
     "label": {"en": "English", "fr": "Anglais"}},
]

_MARKER = {"en": "Guardrails", "fr": "Garde-fous"}
_TITLE = {"en": ("It can ", (s.project.titles.keyword, "refuse")), "fr": ("Elle peut ", (s.project.titles.keyword, "refuser"))}
_CAPTION = {"en": ("the SAME hostile message, scored twice — "
                   "filters read INTENT, not keywords"), "fr": "le MÊME message hostile, noté deux fois — les filtres lisent l’INTENTION, pas les mots-clés"}
_PUNCH = {"en": ("guardrails exist · imperfect · uneven",), "fr": ("des garde-fous existent · imparfaits · inégaux",)}

_TIP_TITLE = {"en": "The experiment, precisely", "fr": "L’expérience, précisément"}
_TOOLTIP = [
    ({"en": "What was tested", "fr": "Ce qui a été testé"},
     {"en": ("A deliberately hostile message (insults plus an incitement to "
             "self-harm — not shown on screen on purpose) was submitted to "
             "OpenAI's moderation model in French, then in English (AISE "
             "trainings, 2024)."), "fr": "Un message délibérément hostile (des insultes plus une incitation à l’automutilation — volontairement non montré à l’écran) a été soumis au modèle de modération d’OpenAI en français, puis en anglais (formations AISE, 2024)."}),
    ({"en": "What the tables show", "fr": "Ce que montrent les tables"},
     {"en": ("Per-category scores: harassment ≈ 89 % in BOTH languages, "
             "self-harm ≈ 80 % in both — the filter reads the intent. Some "
             "categories differ across languages (violence 20 % vs 35 %): "
             "uneven, not absent."), "fr": "Des scores par catégorie : harcèlement ≈ 89 % dans les DEUX langues, automutilation ≈ 80 % dans les deux — le filtre lit l’intention. Certaines catégories diffèrent selon la langue (violence 20 % contre 35 %) : inégal, pas absent."}),
    ({"en": "Where it runs", "fr": "Où ça tourne"},
     {"en": ("Every big chat product runs such a scoring model before and "
             "after the main model — that is why « how to build a bomb » gets "
             "a refusal, in any language."), "fr": "Chaque grand produit de chat exécute un tel modèle de notation avant et après le modèle principal — c’est pourquoi « comment fabriquer une bombe » reçoit un refus, dans toutes les langues."}),
    ({"en": "The honest limits", "fr": "Les limites, honnêtement"},
     {"en": ("Jailbreaks exist and it is an arms race; thresholds are set by "
             "the vendors (the control slide you just saw). The legal side — "
             "the EU AI Act — waits in the backup slides."), "fr": "Les jailbreaks existent et c’est une course aux armements ; les seuils sont fixés par les vendeurs (la slide sur le contrôle que vous venez de voir). Le versant juridique — l’AI Act européen — attend dans les slides backup."}),
]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "🛡️ ", *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(ui("documented_note", lang), T(_TOOLTIP[0][1], lang))]
                            + [(T(h, lang), T(d, lang)) for h, d in _TOOLTIP[1:]],
                )
        st_space("v", "1vh")
        with st_grid(cols="50% 50%", gap="1.5vw",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for tbl in _TABLES:
                with g.cell():
                    #st_write(bs.lang_label, T(tbl["label"], lang), tag=t.div)
                    st_space("v", "1vh")
                    with st_block(s.project.containers.media_stage(
                            tbl["ratio"], TUNING["table_vh"])):
                        st_image(s.project.cards.media_center, uri=tbl["uri"],
                                 alt=T(tbl["label"], lang) + " — moderation scores")
        st_space("v", "2vh")
        st_write(bs.caption, T(_CAPTION, lang), tag=t.div)
        st_space("v", "2vh")
        with st_zoom(130):
            for line in T(_PUNCH, lang):
                st_write(bs.punch, line, tag=t.div)
