"""Les trois portes — ouvrir SES agents, quel que soit l'outil (après M6).

La slide-lanceur de l'opérateur : trois boutons qui ouvrent, chacun dans un
nouvel onglet, la galerie d'agents des trois environnements (Le Chat, ChatGPT,
Gemini). Elle prolonge le message de M2 (« whatever YOUR tool ») en acte :
même méthode, trois portes. Grille 3 colonnes × 2 lignes — les logos
officiels en haut, les boutons « Open » en bas, couleur alignée sur le logo.

Les logos officiels sont des ACTIFS DE MARQUE versionnés sous
``static/images/brands/`` (SVG Wikimedia Commons, usage nominatif dans une
présentation pédagogique) — même tiroir que les captures ``trainings/`` :
des fichiers servis, jamais inlinés, jamais au CDN.

Le FAIT vit ici (règle NG 2026-08-18) : les URLs des galeries et le compte à
utiliser par environnement s'éditent dans ce bloc. Le compte apparaît au
survol du bouton (attribut ``title`` natif — d'où le ``st_html`` assumé :
``st_write(link=)`` ne porte pas d'infobulle) et dans l'infobulle coin.

SPEAKER NOTES:
Operator slide — you are the one clicking. Each button opens a NEW tab on the
agent gallery of that environment; hover shows which account to use (Le Chat
and Gemini: bics.lu · ChatGPT: uni.lu). Say one sentence to the room: the
method you just saw is not Mistral's — every environment has the same door.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    line = s.project.body.caption + s.center_txt


bs = BlockStyles

_MARKER = {"en": "Three+ doors", "fr": "Trois+ portes"}
_TITLE = {"en": ("One method · ", (s.project.titles.keyword, "three+ doors")), "fr": ("Une méthode · ", (s.project.titles.keyword, "trois+ portes"))}
_LINE = {"en": "Learn the tools and adapt your agent to your environment.", "fr": "Apprenez les outils et adaptez votre agent à votre environnement."}
_OPEN = {"en": "Open", "fr": "Ouvrir"}

#: Le socle commun des boutons — même gabarit que ``buttons.action_big`` du
#: design system ; seule la couleur vient de la MARQUE (donnée du bloc),
#: jamais de la palette : c'est le sujet de la slide.
_BTN_BASE = (
    "display:inline-block;color:#1A1A2E;font-weight:800;"
    "font-size:calc(var(--stx-scale-12, 32pt) * 1.1);line-height:1.2;"
    "text-align:center;text-decoration:none;padding:1.8vh 3.5vw;"
    "border-radius:18px;"
)

#: Les trois portes — URL de la galerie d'agents, logo officiel (ratio du
#: fichier → hauteur commune), couleur de bouton alignée sur le logo, compte
#: opérateur montré au survol. Ce sont des DONNÉES (adresses et comptes,
#: identiques dans toutes les langues).
_DOORS = [
    {
        "name": "Mistral Le Chat",
        "url": "https://chat.mistral.ai/agents?tab=mine",
        "logo": "images/brands/mistral.svg",
        "ratio": 129 / 91,
        "css": "background:#FF8205;box-shadow:0 6px 24px rgba(255,130,5,0.35);",
        "tip": {"en": "Use the nicolas.guelfi@bics.lu account", "fr": "Utiliser le compte nicolas.guelfi@bics.lu"},
        "alt": "Mistral AI official logo — the pixel M, yellow to red",
    },
    {
        "name": "ChatGPT",
        "url": "https://chatgpt.com/gpts",
        "logo": "images/brands/chatgpt.svg",
        "ratio": 1.0,
        "css": "background:#74AA9C;box-shadow:0 6px 24px rgba(116,170,156,0.35);",
        "tip": {"en": "Use the nicolas.guelfi@uni.lu account", "fr": "Utiliser le compte nicolas.guelfi@uni.lu"},
        "alt": "ChatGPT official logo — white knot on a teal tile",
    },
    {
        "name": "Google Gemini",
        "url": "https://gemini.google.com/gems/view",
        "logo": "images/brands/gemini.svg",
        "ratio": 344 / 127,
        "css": ("background:linear-gradient(90deg,#439DDF,#9476C5,#D6645D);"
                "box-shadow:0 6px 24px rgba(148,118,197,0.35);"),
        "tip": {"en": "Use the nicolas.guelfi@bics.lu account", "fr": "Utiliser le compte nicolas.guelfi@bics.lu"},
        "alt": "Google Gemini official wordmark — blue to red gradient",
    },
]

_TIP_TITLE = {"en": "Operator: the accounts", "fr": "Opérateur : les comptes"}
_TIP_NOTE = ({"en": "The buttons", "fr": "Les boutons"},
             {"en": ("Each button opens the agent gallery of its environment "
                     "in a NEW tab — the deck stays open behind. The account "
                     "to use is also on the button, at hover."), "fr": "Chaque bouton ouvre la galerie d’agents de son environnement dans un NOUVEL onglet — le deck reste ouvert derrière. Le compte à utiliser est aussi sur le bouton, au survol."})

# ── La main de l'artiste ────────────────────────────────────────────────────
TUNING = {
    "logo_vh": 22,       # hauteur commune des logos (largeur = ratio × vh)
    "logo_cap_vw": 28,   # borne largeur d'un logo — le wordmark Gemini est large
    "btn_zoom": 130,     # les boutons « Open » — l'action se lit du fond
}


def _button_html(door: dict, lang: str) -> str:
    """Le bouton « Open » d'une porte — ancre nouvel onglet, compte au survol."""
    return (
        f'<div style="text-align:center;">'
        f'<a href="{door["url"]}" target="_blank" rel="noopener" '
        f'title="{T(door["tip"], lang)}" '
        f'style="{_BTN_BASE}{door["css"]}">{T(_OPEN, lang)}</a></div>'
    )


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
                    entries=[(door["name"], T(door["tip"], lang))
                             for door in _DOORS] + [
                        (T(_TIP_NOTE[0], lang), T(_TIP_NOTE[1], lang))],
                )
        st_space("v", "3vh")
        with st_zoom(140):
            st_write(bs.line, T(_LINE, lang), tag=t.div)
        st_space("v", "8vh")
        # 2 lignes × 3 colonnes FIXES (repeat(3, 1fr), pas d'auto-fit) : un
        # auto-fit qui replie casserait l'alignement logo ↔ bouton entre les
        # deux lignes ; les colonnes en ``fr`` rétrécissent, elles.
        with st_grid(cols="repeat(3, 1fr)", gap="6vh 2vw",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for door in _DOORS:  # ligne du haut : les logos officiels
                with g.cell():
                    st_image(
                        s.project.cards.media_center,
                        width=(f'min({door["ratio"] * TUNING["logo_vh"]:.0f}vh, '
                               f'{TUNING["logo_cap_vw"]}vw)'),
                        uri=door["logo"], alt=door["alt"])
            for door in _DOORS:  # ligne du bas : les boutons « Open »
                with st_zoom(TUNING["btn_zoom"]), g.cell():
                    st_html(_button_html(door, lang))
