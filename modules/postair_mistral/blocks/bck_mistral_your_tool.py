"""Ton outil, ton choix — la démo est sur Mistral (M2, recadré v0.2).

Positionnement v0.2 (commentaire NG drafts3, 2026-09-01) : la salle utilisera
SURTOUT d'autres outils — assumer, et vendre la MÉTHODE, pas la marque. Une
phrase, pas un débat. L'argument souveraineté vit dans l'infobulle, ancré aux
deux textes officiels (RGPD, CLOUD Act).

Le FAIT vit ici (règle NG 2026-08-18) : les lignes projetées s'éditent dans
ce bloc. EXCEPTION : ce que dit la charte UL des outils est le fait PARTAGÉ
``charter``/``tools`` de facts.json (plusieurs infobulles le citent). La
phrase bibliographique reste dérivée de ``references.bib`` par
``citation()``/``cite`` — clé inconnue = erreur bruyante.

SPEAKER NOTES:
Two minutes. One sentence on the choice: the method works with YOUR tool —
Copilot, ChatGPT, Claude, Gemini — we demonstrate on Mistral, the European
choice, free to start. Do not open a sovereignty debate: the argument is in
the info panel if someone asks. Then move on — the method is the star.
"""
# @guideline: postair-minimal

from custom.facts import citekeys, fact, text
from custom.prompts import AI_PREFIX, AI_SUFFIX_LANDSCAPE
from custom.refs import citation
from custom.styles import Styles as s
from custom.visuals import staged_hero_image
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.hero_split import hero_split


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    item = s.project.body.bullet + s.center_txt
    punch = s.project.titles.subtitle + s.project.colors.amber + s.center_txt


bs = BlockStyles

#: Scène durcie (contrôle visuel 2026-09-02) : la 1re génération ajoutait
#: des bustes humains de face — la scène n'a AUCUNE figure humaine.
_TOOLS_PROMPT = (
    AI_PREFIX
    + "A row of five glowing paper orbs in different bright colours resting "
      "on a paper ground, the central warm amber orb larger and slightly "
      "forward, in front of a soft stylised paper map of Europe with small "
      "paper stars around it. NO human figures, only the orbs and the map."
    + AI_SUFFIX_LANDSCAPE
)

_MARKER = {"en": "Your tool", "fr": "Votre outil"}
_TITLE = {"en": ("Your tool, ", (s.project.titles.keyword, "your choice")), "fr": ("Votre outil, ", (s.project.titles.keyword, "votre choix"))}
#: Télégraphique : la méthode d'abord, le choix de démo ensuite, l'argument
#: européen en une ligne — le débat vit dans l'infobulle.
_ITEMS = [
    {"en": "the method works with YOUR tool", "fr": "la méthode marche avec VOTRE outil"},
    {"en": "Copilot · ChatGPT · Claude · Gemini …", "fr": "Copilot · ChatGPT · Claude · Gemini…"},
    {"en": "the demo: Mistral — Le Chat + agents", "fr": "la démo : Mistral — Le Chat + agents"},
    {"en": "European 🇪🇺", "fr": "européen 🇪🇺"},
]

_TIP_TITLE = {"en": "The choice, precisely", "fr": "Le choix, précisément"}
_TIP_CHARTER_HEAD = {"en": "What the UL guidelines say", "fr": "Ce que disent les lignes directrices UL"}
_TIP_SOVEREIGNTY = ({"en": "The sovereignty argument", "fr": "L’argument souveraineté"},
                    {"en": ("Data processed in Europe stays under GDPR rights "
                            "(access, erasure, purpose limitation); a US "
                            "provider can be compelled by the CLOUD Act to "
                            "hand over data WHEREVER it is stored. Not a "
                            "reason to panic — a reason to know where your "
                            "study material lives."), "fr": "Une donnée traitée en Europe reste sous les droits du RGPD (accès, effacement, limitation de finalité) ; un fournisseur américain peut être contraint par le CLOUD Act de remettre des données OÙ qu’elles soient stockées. Pas une raison de paniquer — une raison de savoir où vit votre matériel de révision."})
_TIP_OFFERS = ({"en": "Student offers", "fr": "Offres étudiantes"},
               {"en": ("Le Chat has a free tier, and Mistral has run student "
                       "offers — check the current conditions the week you "
                       "sign up, they move."), "fr": "Le Chat a une offre gratuite, et Mistral a proposé des offres étudiantes — vérifiez les conditions en vigueur la semaine où vous vous inscrivez, elles bougent."})
_TIP_EQUIV = ({"en": "The same thing everywhere", "fr": "La même chose partout"},
              {"en": ("A Mistral « agent » ≈ a custom GPT ≈ a Claude Project "
                      "≈ a Gem: system instructions + your documents + "
                      "tools. The method's four steps transpose as "
                      "they are."), "fr": "Un « agent » Mistral ≈ un GPT personnalisé ≈ un Projet Claude ≈ un Gem : instructions système + vos documents + outils. Les quatre étapes de la méthode se transposent telles quelles."})

_PUNCH = {"en": "Check the students offers", "fr": "Vérifiez les offres étudiantes"}


# ── La main de l'artiste ────────────────────────────────────────────────────
#: Resserrée (porte projection 2026-09-02 : ×1.13/×1.17) — budget image et
#: zoom de colonne d'un cran, le ratio 40 de NG inchangé.
TUNING = {
    "ratio": 40,
    "hero_vh": 50,
    "column_zoom": 90,
}


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    charter = fact("charter", "tools")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with st_zoom(150), g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(T(_TIP_SOVEREIGNTY[0], lang), T(_TIP_SOVEREIGNTY[1], lang)),
                             (T(_TIP_CHARTER_HEAD, lang),
                              text(charter["claim"], lang)),
                             (T(_TIP_OFFERS[0], lang), T(_TIP_OFFERS[1], lang)),
                             (T(_TIP_EQUIV[0], lang), T(_TIP_EQUIV[1], lang))],
                )
        st_space("v", s.project.spacing.title_gap)
        with hero_split(s, ratio=TUNING["ratio"], zoom=TUNING["column_zoom"],
                        image=lambda: staged_hero_image(
                            "mistral_tools", _TOOLS_PROMPT,
                            "images/mistral_tools_fallback.svg",
                            alt_ready=("Papercut row of coloured tool orbs, the amber one "
                                       "forward, in front of a stylised paper Europe"),
                            alt_fallback=("Row of papercut orbs before a paper map of "
                                          "Europe, amber orb in front"),
                            variant="sq", stage_vh=TUNING["hero_vh"])):
            for item in _ITEMS:
                st_space("v", "2vh")
                st_write(bs.item, "▸ ", T(item, lang), tag=t.div)
            st_space("v", "4vh")
            with st_zoom(150):
                st_write(bs.punch, T(_PUNCH, lang), " ", tag=t.div)
