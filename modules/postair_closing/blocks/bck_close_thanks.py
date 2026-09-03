"""Closing — thank you! (C3).

The family photo: the eighteen bestiary mascots of the nine axes plus the two
moderators, in one festive grid under the closing line. High energy, applause
slide — the credits live in the tooltip. Mascots are asked by the frozen cast
manifest (``postair_data``), never by file.

Le FAIT vit ici (règle NG 2026-08-18) : la phrase de clôture et les crédits
s'éditent dans ce bloc. La phrase bibliographique reste dérivée de
``references.bib`` par ``citation()``/``cite`` — clé inconnue = erreur
bruyante (cette slide ne cite aucune source).

Conversion R-i18n (2026-09-03) : tout texte projeté est une feuille
``{"en", "fr"}`` résolue par ``T()``/``TF()`` de ``postair_lang`` ; les noms
de mascottes restent des données du manifeste.

SPEAKER NOTES:
One minute, all energy. Read the line — « Welcome to the University of
Luxembourg — make AI yours » — open your arms, let the room applaud the
mascots. Logistics of what follows (break, rooms) is said here if needed.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from postair_data import axes, mascot
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.ai_mark import dd35_overlay


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    big = s.project.titles.subtitle + s.project.colors.amber + s.center_txt + s.bold
    confetti = s.project.titles.subtitle + s.center_txt
    name = s.project.body.mascot_name + s.center_txt


bs = BlockStyles

# ── Le fait : la phrase de clôture et les crédits ───────────────────────────
_BIG = {"en": "Welcome to the University of Luxembourg — make AI yours.",
        "fr": "Bienvenue à l’Université du Luxembourg — faites de l’IA la vôtre."}
_CREDITS = {"en": ("AI Day team · the POSTAIR study and its 55 figures · sumvadis "
                   "(the live survey) · 38 mascots, 100 % generative AI · built "
                   "with streamtex"),
            "fr": ("L’équipe de l’AI Day · l’étude POSTAIR et ses 55 figures · "
                   "sumvadis (l’enquête live) · 38 mascottes, 100 % IA générative · "
                   "réalisé avec streamtex")}

_MARKER = {"en": "Thank you!", "fr": "Merci !"}
_TITLE = {"en": ((s.project.titles.keyword, "Thank you"), "!"),
          "fr": ((s.project.titles.keyword, "Merci"), " !")}
_TIP_TITLE = {"en": "Credits", "fr": "Crédits"}
_TIP_DAY_HEAD = {"en": "The day", "fr": "La journée"}
_TIP_MASCOTS = ({"en": "The mascots", "fr": "Les mascottes"},
                {"en": ("38 characters, 100 % generative AI, designed "
                        "in the mascoties studio — each carries one pole of one axis."),
                 "fr": ("38 personnages, 100 % IA générative, conçus au studio "
                        "mascoties — chacun porte un pôle d’un axe.")})


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
                        (T(_TIP_DAY_HEAD, lang), T(_CREDITS, lang)),
                        (T(_TIP_MASCOTS[0], lang), T(_TIP_MASCOTS[1], lang)),
                    ],
                )
        st_space("v", s.project.spacing.title_gap)
        st_write(bs.confetti, "🎉 🎊 🎉", tag=t.div)
        st_space("v", "0.5vh")
        # La photo de famille : 9 axes × 2 pôles (bestiaire) + les 2 modérateurs.
        family = axes("animals")
        crew = [family[n][side]for n in sorted(family) for side in ("accel", "decel")]
        crew += [{"mascot": m["name"], "image": m["image"]}
                 for m in (mascot("Medio"), mascot("Voxo"))]
        with st_grid(cols=10, gap="0.5vw",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for member in crew:
                with g.cell():
                    st_image(s.project.cards.media_center, width="6vw",
                             uri=member["image"],
                             alt=f"Mascot {member['mascot']}",
                             overlay=dd35_overlay())
                    st_write(bs.name, member["mascot"], tag=t.div)
        st_space("v", "2vh")
        st_write(bs.big, T(_BIG, lang), tag=t.div)
