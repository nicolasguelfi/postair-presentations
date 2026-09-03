"""La carte des services (SV1, flux — après « Trois portes »).

La synthèse en séance (décision NG : « synthèse en flux + réserve ») : ce que
le marché offre pour étudier, lu par la SEULE grille qui compte pour la salle —
Gratuit · Étudiant · Payant. Les quatre cartes complètes (créer un agent, le
nourrir, lui parler, les offres étudiantes) vivent en RÉSERVE et se projettent
sur une question.

Les faits du marché vivent dans ``facts.json`` (section ``services``, campagne
de vérification 2026-09-03, sources officielles) — ce bloc ne porte que la
synthèse éditoriale. Politique « ? » (NG) : un fait non vérifiable s'affiche
❓, jamais un ✅ de confiance moyenne.

SPEAKER NOTES:
One minute. The point is the three-tier reading, not the logos: free is
enough to LEARN the method; your school email unlocks real money (Google: a
free year, Luxembourg eligible; Mistral: 5.99 a month); paid buys comfort,
not the method. Say the date out loud — this market moves monthly. The four
detailed maps are in Backup for questions.
"""
# @guideline: postair-minimal

from custom.facts import section
from custom.styles import Styles as s
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    tier = s.project.body.bullet + s.center_txt + s.bold
    line = s.project.body.caption + s.center_txt
    punch = s.project.titles.subtitle + s.project.colors.amber + s.center_txt + s.bold


bs = BlockStyles

_MARKER = {"en": "Services", "fr": "Services"}
_TITLE = {"en": ("Study services — ", (s.project.titles.keyword, "the map")), "fr": ("Les services pour étudier — ", (s.project.titles.keyword, "la carte"))}

#: Les trois niveaux d'accès — LA grille de lecture de toutes les cartes.
_TIERS = [
    {"head": {"en": "✅ Free", "fr": "✅ Gratuit"},
     "line": {"en": "enough to LEARN — quotas & limits", "fr": "assez pour APPRENDRE — quotas et limites"}},
    {"head": {"en": "🎓 Student", "fr": "🎓 Étudiant"},
     "line": {"en": "your school email is worth money", "fr": "votre email d'école vaut de l'argent"}},
    {"head": {"en": "💰 Paid", "fr": "💰 Payant"},
     "line": {"en": "≈ 6-23 €/month — comfort, not the method", "fr": "≈ 6-23 €/mois — le confort, pas la méthode"}},
]

_PUNCH = {"en": "the method is free — the comfort is not", "fr": "la méthode est gratuite — le confort, pas toujours"}
_DATE_LINE = {"en": "snapshot of 2026-09-03 — this market moves monthly: check at the source", "fr": "photo du 2026-09-03 — ce marché bouge chaque mois : vérifiez à la source"}
_BACKUP_HINT = {"en": "the four full maps live in Backup — create · feed · talk · student deals", "fr": "les quatre cartes complètes vivent en réserve — créer · nourrir · parler · offres étudiantes"}

_TIP_TITLE = {"en": "The three tiers, precisely", "fr": "Les trois niveaux, précisément"}
_TOOLTIP = [
    ({"en": "✅ Free", "fr": "✅ Gratuit"},
     {"en": ("Every platform of the day has a working free tier: Gems creation, "
             "Claude Projects (5), Poe bots, ChatGPT usage, Vibe chat. Limits "
             "are quotas and model access, not the method."), "fr": "Chaque plateforme du jour a un gratuit qui marche : création de Gems, Projects Claude (5), bots Poe, usage de ChatGPT, chat Vibe. Les limites sont des quotas et des modèles, pas la méthode."}),
    ({"en": "🎓 Student", "fr": "🎓 Étudiant"},
     {"en": ("The two real deals for THIS room: Google — one free year of AI "
             "Plus, Luxembourg eligible (SheerID + school email, before "
             "2026-12-31); Mistral — Vibe Pro at 5.99 €/month for verified "
             "students. OpenAI's student offers are US-only."), "fr": "Les deux vraies offres pour CETTE salle : Google — un an d'AI Plus offert, Luxembourg éligible (SheerID + email d'école, avant le 31-12-2026) ; Mistral — Vibe Pro à 5,99 €/mois pour étudiants vérifiés. Les offres OpenAI sont USA uniquement."}),
    ({"en": "💰 Paid", "fr": "💰 Payant"},
     {"en": ("Reference prices in Europe: Vibe Pro 14.99 € (student 5.99 €), "
             "Google AI Pro 21.99 €, ChatGPT Plus ≈ 23 € incl. VAT, Claude Pro "
             "17-20 $. Paid buys bigger quotas, contexts and file bases."), "fr": "Prix de référence en Europe : Vibe Pro 14,99 € (étudiant 5,99 €), Google AI Pro 21,99 €, ChatGPT Plus ≈ 23 € TTC, Claude Pro 17-20 $. Le payant achète des quotas, des contextes et des bases de fichiers plus grands."}),
    ({"en": "Why the date matters", "fr": "Pourquoi la date compte"},
     {"en": ("Everything here was verified on official pages on 2026-09-03 — "
             "and can change next month. A ❓ anywhere means: not verifiable "
             "at the source that day. Checking the pricing page yourself IS "
             "part of the method."), "fr": "Tout ici a été vérifié sur les pages officielles le 2026-09-03 — et peut changer le mois prochain. Un ❓ signifie : non vérifiable à la source ce jour-là. Vérifier soi-même la page de prix FAIT PARTIE de la méthode."}),
]

# ── La main de l'artiste ────────────────────────────────────────────────────
TUNING = {
    "logo_vh": 8,        # la rangée de logos — un bandeau, pas un héros
    "card_zoom": 120,
    "punch_zoom": 120,
}

#: La rangée de logos suit les plateformes de la section ``create`` du gel —
#: l'ordre et la liste ne sont écrits qu'une fois (facts.json).
def _logo_row():
    return [(p["icon"], p.get("ratio", 1.0), p["name"])
            for p in section("services")["create"]]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with st_zoom(150), g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(T(h, lang), T(d, lang)) for h, d in _TOOLTIP],
                )
        st_space("v", s.project.spacing.title_gap)
        # La grille de lecture : trois cartes, une par niveau d'accès.
        with st_grid(cols=s.project.grids.balanced(3), gap="1.2vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for tier in _TIERS:
                with st_zoom(TUNING["card_zoom"]), g.cell(), st_block(s.project.cards.blue):
                    st_write(bs.tier, T(tier["head"], lang), tag=t.div)
                    st_space("v", "0.5vh")
                    st_write(bs.line, T(tier["line"], lang), tag=t.div)
        st_space("v", "4vh")
        # Le paysage : les logos des plateformes du jour (données du gel).
        logos = _logo_row()
        with st_grid(cols=f"repeat({len(logos)}, 1fr)", gap="1vw",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for icon, ratio, name in logos:
                with g.cell():
                    if icon:
                        st_image(s.project.cards.media_center,
                                 width=f"min({ratio * TUNING['logo_vh']:.1f}vh, 12vw)",
                                 uri=icon, alt=name)
                    else:
                        st_write(bs.tier, name, tag=t.div)  # i18n: verbatim
        st_space("v", "4vh")
        with st_zoom(TUNING["punch_zoom"]):
            st_write(bs.punch, T(_PUNCH, lang), tag=t.div)
        st_space("v", "2vh")
        st_write(bs.line, T(_DATE_LINE, lang), tag=t.div)
        st_write(bs.line, T(_BACKUP_HINT, lang), tag=t.div)
