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
TUNING = {"table_vh": 52}

#: Ratio largeur/hauteur DU FICHIER (mesuré Pillow 2026-09-01).
_TABLES = [
    {"uri": "images/trainings/moderation_fr.png", "ratio": 0.941,
     "label": {"en": "Français"}},
    {"uri": "images/trainings/moderation_en.png", "ratio": 0.879,
     "label": {"en": "English"}},
]

_MARKER = {"en": "Guardrails"}
_TITLE = {"en": ("It can ", (s.project.titles.keyword, "refuse"))}
_CAPTION = {"en": ("the SAME hostile message, scored twice — "
                   "filters read INTENT, not keywords")}
_PUNCH = {"en": ("guardrails exist · imperfect · uneven",)}

_TIP_TITLE = {"en": "The experiment, precisely"}
_TOOLTIP = [
    ({"en": "What was tested"},
     {"en": ("A deliberately hostile message (insults plus an incitement to "
             "self-harm — not shown on screen on purpose) was submitted to "
             "OpenAI's moderation model in French, then in English (AISE "
             "trainings, 2024).")}),
    ({"en": "What the tables show"},
     {"en": ("Per-category scores: harassment ≈ 89 % in BOTH languages, "
             "self-harm ≈ 80 % in both — the filter reads the intent. Some "
             "categories differ across languages (violence 20 % vs 35 %): "
             "uneven, not absent.")}),
    ({"en": "Where it runs"},
     {"en": ("Every big chat product runs such a scoring model before and "
             "after the main model — that is why « how to build a bomb » gets "
             "a refusal, in any language.")}),
    ({"en": "The honest limits"},
     {"en": ("Jailbreaks exist and it is an arms race; thresholds are set by "
             "the vendors (the control slide you just saw). The legal side — "
             "the EU AI Act — waits in the backup slides.")}),
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
        st_space("v", s.project.spacing.title_gap)
        with st_grid(cols="50% 50%", gap="1.5vw",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for tbl in _TABLES:
                with g.cell():
                    st_write(bs.lang_label, T(tbl["label"], lang), tag=t.div)
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
