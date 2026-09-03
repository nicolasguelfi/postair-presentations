"""Closing — and now? (C2).

The QR to the hub of the day's presentations, giant, with the four « what
stays with you » lines. URLs and contacts in the tooltip.

Le FAIT vit ici (règle NG 2026-08-18) : les quatre lignes, l'URL du hub et
les contacts s'éditent dans ce bloc. La phrase bibliographique reste dérivée
de ``references.bib`` par ``citation()``/``cite`` — clé inconnue = erreur
bruyante (cette slide ne cite aucune source).

Conversion R-i18n (2026-09-03) : tout texte projeté est une feuille
``{"en", "fr"}`` résolue par ``T()``/``TF()`` de ``postair_lang`` ; l'URL du
hub reste une donnée verbatim.

SPEAKER NOTES:
Two minutes. Leave the QR on screen long enough for the slow phones. Say the
one that matters most: your survey result stays at /r/<your code>, anonymous,
yours — and postures move, retake it at the end of the year.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    item = s.project.body.bullet + s.center_txt
    url = s.project.titles.subtitle + s.project.colors.keyword + s.center_txt + s.bold


bs = BlockStyles

# ── Le fait : ce qui reste après la séance ──────────────────────────────────
_ITEMS = [
    {"en": "Your result: /r/<code> · anonymous · yours",
     "fr": "Votre résultat : /r/<code> · anonyme · à vous"},
    {"en": "4 decks online · one hub",
     "fr": "4 documents en ligne · un seul hub"},
    {"en": "Mistral walkthrough → rebuild at home",
     "fr": "Pas-à-pas Mistral → à refaire chez vous"},
    {"en": "Retake the survey at year end → postures MOVE",
     "fr": "Refaites l’enquête en fin d’année → les postures BOUGENT"},
]
_HUB_URL = "postair-collection.streamtex.org"  # i18n: verbatim
_CONTACTS = {"en": "Guidelines: I2TL@uni.lu · the speakers stay around during the break",
             "fr": "Lignes directrices : I2TL@uni.lu · les orateurs restent là pendant la pause"}

_MARKER = {"en": "And now?", "fr": "Et maintenant ?"}
_TITLE = {"en": ("And ", (s.project.titles.keyword, "now"), "?"),
          "fr": ("Et ", (s.project.titles.keyword, "maintenant"), " ?")}
_TIP_TITLE = {"en": "Everything that stays online", "fr": "Tout ce qui reste en ligne"}
#: Les adresses citées dans les entrées (hub, /r/<code>) sont verbatim.
_TIP_HUB = ({"en": "The hub", "fr": "Le hub"},
            {"en": ("postair-collection.streamtex.org — the four decks "
                    "of the day, one card each."),
             "fr": ("postair-collection.streamtex.org — les quatre documents "
                    "de la journée, une carte chacun.")})
_TIP_RESULT = ({"en": "Your result", "fr": "Votre résultat"},
               {"en": ("app.sumvadis.ai/r/<your code> — anonymous, "
                       "computed on your device, kept for you."),
                "fr": ("app.sumvadis.ai/r/<votre code> — anonyme, "
                       "calculé sur votre appareil, conservé pour vous.")})
_TIP_CONTACTS_HEAD = {"en": "Contacts", "fr": "Contacts"}
#: Jamais projeté, gardé pour la vérifiabilité (entrée « big » de l'ancien
#: facts.json) : « And now? ».


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[
                        (T(_TIP_HUB[0], lang), T(_TIP_HUB[1], lang)),
                        (T(_TIP_RESULT[0], lang), T(_TIP_RESULT[1], lang)),
                        (T(_TIP_CONTACTS_HEAD, lang), T(_CONTACTS, lang)),
                    ],
                )
        st_space("v", s.project.spacing.title_gap)
        # breakpoint : sous 520 px, le QR passe au-dessus de la liste.
        with st_grid(cols="55% 45%", breakpoint="520px",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                # QR versionné (static/images/qr/), généré vers le hub collection.
                st_image(s.project.cards.media_center, width="18vw",
                         uri="images/qr/qr_hub_collection.png",
                         alt="QR code to postair-collection.streamtex.org, the hub of "
                             "the day's presentations")
                st_write(bs.url, _HUB_URL, tag=t.div)
            with g.cell():
                for item in _ITEMS:
                    st_write(bs.item, "▸ ", T(item, lang), tag=t.div)
                    st_space("v", "1vh")
