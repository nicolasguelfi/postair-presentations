"""Closing — and now? (C2).

The QR to the hub of the day's presentations, giant, with the four « what
stays with you » lines. URLs and contacts in the tooltip.

Le FAIT vit ici (règle NG 2026-08-18) : les quatre lignes, l'URL du hub et
les contacts s'éditent dans ce bloc. La phrase bibliographique reste dérivée
de ``references.bib`` par ``citation()``/``cite`` — clé inconnue = erreur
bruyante (cette slide ne cite aucune source).

SPEAKER NOTES:
Two minutes. Leave the QR on screen long enough for the slow phones. Say the
one that matters most: your survey result stays at /r/<your code>, anonymous,
yours — and postures move, retake it at the end of the year.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
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
    "Your result: /r/<code> · anonymous · yours",
    "4 decks online · one hub",
    "Mistral walkthrough → rebuild at home",
    "Retake the survey at year end → postures MOVE",
]
_HUB_URL = "postair-collection.streamtex.org"
_CONTACTS = "Guidelines: I2TL@uni.lu · the speakers stay around during the break"
#: Jamais projeté, gardé pour la vérifiabilité (entrée « big » de l'ancien
#: facts.json) : « And now? ».


def build(lang: str = "en", **_):
    st_marker("And now?")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "And ", (s.project.titles.keyword, "now"), "?",
                         tag=t.div, toc_lvl="+1", label="And now?")
            with g.cell():
                st_info_tooltip(
                    title="Everything that stays online",
                    entries=[
                        ("The hub", "postair-collection.streamtex.org — the four decks "
                         "of the day, one card each."),
                        ("Your result", "app.sumvadis.ai/r/<your code> — anonymous, "
                         "computed on your device, kept for you."),
                        ("Contacts", _CONTACTS),
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
                    st_write(bs.item, "▸ ", item, tag=t.div)
                    st_space("v", "1vh")
