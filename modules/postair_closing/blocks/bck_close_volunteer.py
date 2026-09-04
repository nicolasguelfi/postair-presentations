"""Closing — call for volunteers (demande NG 2026-09-04).

The giant QR opens a PRE-FILLED email (to · subject · short standard body) —
one tap to send, nothing sent until the person presses Send. The wording
stays deliberately VAGUE (consigne NG) : on parle de « l'outil d'enquête
utilisé aujourd'hui » (sumvadis) et d'activités à venir, sans en dire plus ;
la double affiliation de l'étude (UL + sumvadis) est dite dans le tooltip.

Le FAIT vit ici : les lignes projetées, l'adresse et les textes du mailto
s'éditent dans ce bloc. Les deux QR (un par langue — le corps du mail est
localisé) sont GÉNÉRÉS et versionnés sous ``static/images/qr/`` ; le payload
exact est documenté ci-dessous — toute retouche du texte du mail exige de
REGÉNÉRER les QR (voir le bloc ``_MAILTO`` plus bas), jamais de retoucher
les PNG.

Conversion R-i18n native : tout texte projeté est une feuille ``{"en",
"fr"}`` résolue par ``T()``/``TF()``.

SPEAKER NOTES:
One minute, light tone. The survey you all used this morning is a living
tool — if you want to be part of what comes next, scan: your mail is
already written, just press Send. No commitment, no spam — a declaration.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from postair_data import mascot
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.ai_mark import dd35_overlay


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    item = s.project.body.bullet + s.center_txt
    mail = s.project.titles.subtitle + s.project.colors.keyword + s.center_txt + s.bold
    hint = s.project.body.caption + s.center_txt


bs = BlockStyles

# ── Le fait : l'appel, volontairement flou ──────────────────────────────────
_ITEMS = [
    {"en": "The live survey you used today → a tool that keeps evolving",
     "fr": "L’enquête live d’aujourd’hui → un outil qui continue d’évoluer"},
    {"en": "Volunteers welcome · tests, feedback, ideas, ...",
     "fr": "Volontaires bienvenus · essais, retours, idées, ..."},
    {"en": "Historical figures — verification and enquiries",
     "fr": "Personnages historiques — vérification et enquêtes"},
]
_MAIL_ADDR = "contact@sumvadis.ai"  # i18n: verbatim
#: Une couleur du DS par item (retouche NG 2026-09-04) — le trio de la
#: journée sur fond navy : teal · ambre · corail, dans l'ordre des lignes.
_ITEM_COLORS = [s.project.colors.keyword, s.project.colors.amber,
                s.project.colors.coral]
#: Le payload des QR — DOCUMENTATION du contenu gelé dans les PNG versionnés
#: (qr_volunteer_en.png / qr_volunteer_fr.png). Regénération :
#:   mailto:contact@sumvadis.ai?subject=Volunteer%20Declaration&body=<corps>
#: corps EN : « Hello, / I would like to take part as a volunteer in the
#:   activities related to the sumvadis survey tool. / Best regards, »
#: corps FR : « Bonjour, / Je souhaite participer en tant que volontaire aux
#:   activités liées à l'outil d'enquête sumvadis. / Cordialement, »

_MARKER = {"en": "Volunteers", "fr": "Volontaires"}
_TITLE = {"en": ("Call for ", (s.project.titles.keyword, "volunteers")),
          "fr": ("Appel à ", (s.project.titles.keyword, "volontaires"))}
_TIP_TITLE = {"en": "What this is", "fr": "De quoi il s’agit"}
_TIP_STUDY = ({"en": "The study", "fr": "L’étude"},
              {"en": ("Today's survey belongs to a study with a double "
                      "affiliation — the University of Luxembourg and the "
                      "sumvadis initiative. Volunteering is occasional and "
                      "informal: trying things out, giving feedback."),
               "fr": ("L’enquête d’aujourd’hui relève d’une étude en double "
                      "affiliation — l’Université du Luxembourg et "
                      "l’initiative sumvadis. Le volontariat est ponctuel et "
                      "informel : essayer, donner un avis.")})
_TIP_MAIL = ({"en": "The QR", "fr": "Le QR"},
             {"en": ("It opens a PRE-FILLED email (contact@sumvadis.ai · "
                     "« Volunteer Declaration » · a short standard text). "
                     "Nothing is sent until you press Send."),
              "fr": ("Il ouvre un e-mail PRÉ-REMPLI (contact@sumvadis.ai · "
                     "« Volunteer Declaration » · un court texte standard). "
                     "Rien ne part tant que vous n’appuyez pas sur "
                     "Envoyer.")})
_HINT = {"en": "Scan & Send",
         "fr": "Scannez & Envoyez"}


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        # Rangée de titre à TROIS colonnes (retouche NG 2026-09-04) : la
        # mascotte à gauche rend la slide accueillante — Unio, le pôle
        # altruisme de l'axe 8 : LE geste du volontariat.
        with st_grid(cols="10% 82% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                unio = mascot("Unio")
                with st_zoom(150):
                    st_image(s.project.cards.media_center, width="10vw",
                         uri=unio["image"],
                         alt="Unio, the altruism mascot, welcoming volunteers")
            with g.cell():
                with st_zoom(160):
                    st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[
                        (T(_TIP_STUDY[0], lang), T(_TIP_STUDY[1], lang)),
                        (T(_TIP_MAIL[0], lang), T(_TIP_MAIL[1], lang)),
                    ],
                )
        st_space("v", "1vh")
        # Même gabarit que la slide du hub : le QR géant à gauche, les
        # lignes à droite ; sous 520 px le QR passe au-dessus.
        with st_grid(cols="40% 60%", breakpoint="520px",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                # QR versionné, UN PAR LANGUE (le corps du mail est localisé).
                with st_zoom(100):
                    st_image(s.project.cards.media_center, width="30vw",
                         uri=f"images/qr/qr_volunteer_{lang}.png",
                         alt="QR code opening a pre-filled volunteer email to "
                             "contact@sumvadis.ai (subject: Volunteer Declaration)")
                #st_write(bs.mail, _MAIL_ADDR, tag=t.div)
                with st_zoom(260):
                    st_write(bs.hint, T(_HINT, lang), tag=t.div)
            with g.cell():
                for item, color in zip(_ITEMS, _ITEM_COLORS):
                    with st_zoom(140):
                        st_write(bs.item + color, "▸ ", T(item, lang),
                                 tag=t.div)
                    st_space("v", "1vh")
