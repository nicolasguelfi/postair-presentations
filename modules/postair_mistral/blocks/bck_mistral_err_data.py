"""Erreur n°4 — Données perso & matériel protégé (M10) — Serro veille.

Trois règles en cartes, la mascotte gardienne **Serro** en clin d'œil (plan
M10 : bouclier/porte cadenassée — la mascotte du cast gelé remplit ce rôle
sans image générée). Le fait charte est PARTAGÉ (``charter``/``data`` de
facts.json — la même vérité que le rappel de la démo A).

Le deck nomme une mascotte (``postair_data.mascot``), jamais un fichier —
règle médias du dépôt ; la pastille DD-35 vient de ``dd35_overlay``.

SPEAKER NOTES:
One minute, three rules, no drama: never other people's personal data (your
group mates' names in a transcript count); never course recordings without
consent; your own drafts — think before uploading, a free account may train
on them, the settings panel has the opt-out. Serro guards the door: one
image, three rules, done.
"""
# @guideline: postair-minimal

from custom.facts import citekeys, fact, text
from custom.refs import citation
from custom.styles import Styles as s
from postair_data import mascot
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.ai_mark import dd35_overlay


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    icon = s.project.titles.subtitle + s.center_txt
    rule = s.project.body.bullet + s.center_txt + s.bold
    line = s.project.body.caption + s.center_txt
    mascot_name = s.project.body.caption + s.center_txt
    punch = s.project.titles.subtitle + s.project.colors.amber + s.center_txt


bs = BlockStyles

_MARKER = {"en": "Error: your data", "fr": "Erreur : vos données"}
#: Titre RACCOURCI (porte projection 2026-09-02 : l'ancien « personal data &
#: protected material » passait sur 3 lignes à zoom 150 — un titre trop long
#: se raccourcit dans les données, règle du DS) ; le matériel protégé reste
#: dit par les cartes et l'infobulle.
_TITLE = {"en": ("Error 4 — ", (s.project.titles.keyword, "whose data?")), "fr": ("Erreur 4 — ", (s.project.titles.keyword, "les données de qui ?"))}

_RULES = [
    {"icon": "🚫", "rule": {"en": "NEVER others' personal data", "fr": "JAMAIS les données des autres"},
     "line": {"en": "names · emails · group work transcripts", "fr": "noms · e-mails · travaux de groupe"}},
    {"icon": "🎙️", "rule": {"en": "NEVER course recordings without consent", "fr": "JAMAIS d’enregistrement de cours sans accord"},
     "line": {"en": "the professor's voice is personal data", "fr": "la voix du professeur est une donnée personnelle"}},
    {"icon": "🤔", "rule": {"en": "your OWN drafts: think first", "fr": "vos PROPRES brouillons : réfléchissez d’abord"},
     "line": {"en": "free accounts may train on them → opt out", "fr": "les comptes gratuits peuvent s’en servir pour l’entraînement → opt-out"}},
]

_TIP_TITLE = {"en": "The rules, precisely", "fr": "Les règles, précisément"}
_TIP_CHARTER_HEAD = {"en": "What the UL guidelines say", "fr": "Ce que disent les lignes directrices UL"}
_TIP_ACCOUNTS = ({"en": "Personal vs institutional account", "fr": "Compte perso vs compte institutionnel"},
                 {"en": ("An institutional tool (Copilot at UL) comes with a "
                         "data agreement; your personal free account does "
                         "not. Same prompt, different legal ground — that is "
                         "why the guidelines treat external tools with "
                         "caution."), "fr": "Un outil institutionnel (Copilot à l’UL) s’accompagne d’un accord sur les données ; votre compte gratuit personnel non. Même prompt, terrain juridique différent — c’est pourquoi les lignes directrices traitent les outils externes avec prudence."})
_TIP_SETTINGS = ({"en": "Mistral privacy settings", "fr": "Réglages de confidentialité Mistral"},
                 {"en": ("Le Chat's settings include an opt-out from using "
                         "your conversations for training. Check it once at "
                         "sign-up — and re-check after big product updates, "
                         "defaults move."), "fr": "Les réglages du Chat comprennent un opt-out de l’usage de vos conversations pour l’entraînement. Vérifiez-le une fois à l’inscription — et revérifiez après les grosses mises à jour produit, les défauts bougent."})


# ── La main de l'artiste ────────────────────────────────────────────────────
#: Resserrée (porte projection 2026-09-02 : ×1.34/×1.52 aux deux références —
#: la pire slide du module) : mascotte réduite, cartes à 90, icônes à 110.
TUNING = {
    "card_zoom": 130,
    "mascot_width": "min(9vw, 16vh)",
}


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    charter = fact("charter", "data")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with st_zoom(150), g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(T(_TIP_CHARTER_HEAD, lang), text(charter["claim"], lang)),
                             (T(_TIP_ACCOUNTS[0], lang), T(_TIP_ACCOUNTS[1], lang)),
                             (T(_TIP_SETTINGS[0], lang), T(_TIP_SETTINGS[1], lang))],
                )
        st_space("v", "1.5vh")
        # Serro EN COLONNE à gauche des règles (porte projection 2026-09-02 :
        # le rang mascotte au-dessus des cartes portait la slide à ×1.21 à
        # 1728 — la gardienne garde son clin d'œil, sans coûter un étage).
        with st_grid(cols="33% 33% 33%", gap="1vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for rule in _RULES:
                with g.cell(), st_block(s.project.cards.coral):
                    with st_zoom(110):
                        st_write(bs.icon, rule["icon"], tag=t.div)
                    st_space("v", "1vh")
                    with st_zoom(TUNING["card_zoom"]):
                        st_write(bs.rule, T(rule["rule"], lang), tag=t.div)
                        st_space("v", "0.8vh")
                        st_write(bs.line, T(rule["line"], lang), tag=t.div)
        st_space("v", "1.5vh")
        with st_zoom(120):
            st_write(bs.punch, text(charter["short"], lang), " ",
                     citation(*citekeys(charter)), tag=t.div)
