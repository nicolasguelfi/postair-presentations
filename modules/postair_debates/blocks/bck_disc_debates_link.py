"""Now, let's argue — the pivot into the first axis.

Moved here from the opening deck (NG 2026-08-14, ss12-restructure) — the same
movement as bck_disc_wrapup (NG 2026-08-03). In opening this slide was a door
to another document, mascot left and one big button right; now that it LIVES
in the debates deck there is no tab to switch to and no button to press: Voxo
opens the debate, and the next page IS the first axis. What survives is the
promise — two or three axes, the ones where this room splits — now carried
by the tooltip and by these notes, and the two tooltip entries the earlier
intro slides do not already carry.

The right column is the floor-taking procedure for a participant (NG
2026-08-30): three bullets — raise your hand, take the microphone, say why
you favour the pole on screen — each under eight words with one keyword
(R3), rendered with the library's own ``st_list`` — never stacked writes
pretending to be a list. The promise left the screen: the room does not
need it, the speaker does.

SPEAKER NOTES:
Ten seconds — this slide is a hinge, not a stop. The results page told you
where the room splits; name the two or three axes you will open, out loud,
so the room knows the plan. Then turn the page: the first axis begins. Do
not read the bank in order — two axes done properly beat five rushed.
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
    bullet = s.project.body.bullet
    mascot_name = s.project.body.mascot_name


bs = BlockStyles

# ── Le texte projeté (règle R-i18n) — la procédure de prise de parole.
_STEPS = [
    {"en": ("Raise your ", (s.project.titles.keyword, "hand")), "fr": ("Levez la ", (s.project.titles.keyword, "main"))},
    {"en": ("Take the ", (s.project.titles.keyword, "microphone")), "fr": ("Prenez le ", (s.project.titles.keyword, "micro"))},
    {"en": ("Say ", (s.project.titles.keyword, "why"), " you favour the pole"), "fr": ("Dites ", (s.project.titles.keyword, "pourquoi"), " vous défendez le pôle")},
]
_TIP_PLAN = ({"en": "The plan", "fr": "Le plan"},
             {"en": ("Two or three axes — the ones where this room splits, read on the "
                     "results page. Name them out loud before opening the first; two axes "
                     "done properly beat five rushed."), "fr": "Deux ou trois axes — ceux sur lesquels cette salle se divise, lus sur la page des résultats. Nommez-les à voix haute avant d'ouvrir le premier ; deux axes bien menés valent mieux que cinq bâclés."})


def build(lang: str = "en", **_):
    st_marker("The debates")
    voxo = mascot("Voxo")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "Now ... ", (s.project.titles.keyword, "HANDS ON"),
                         tag=t.div, toc_lvl="+1", label="The debates")
            with g.cell():
                st_info_tooltip(
                    title="Navigating the debates bank",
                    entries=[
                        (T(_TIP_PLAN[0], lang), T(_TIP_PLAN[1], lang)),
                        ("What each pole offers", "What the pole claims and its three survey "
                         "statements; three historical figures who defended it, with a portrait, "
                         "a sourced quotation and a presentation video; three sourced "
                         "contemporary arguments; then the two poles face to face."),
                        ("Both sides, always", "The material is symmetrical. Never open one pole "
                         "without its opposite — the room must hear the two best cases, not the "
                         "one the speaker prefers."),
                    ],
                )
        # Un franc espace sous le titre (NG 2026-08-03) : la slide ne porte
        # qu'une promesse, et une promesse collée à son titre se lit comme une
        # note de bas de page.
        st_space("v", s.project.spacing.title_gap)
        with st_grid(cols="45% 55%", gap="1.5vw",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_image(s.project.cards.media_center, width="min(22vw, 46vh)",
                         uri=voxo["image"],
                         alt=f"{voxo['name']}, the moderator mascot, opening the floor to debate",
                         overlay=dd35_overlay())
                st_write(bs.mascot_name, voxo["name"], tag=t.div)
            with g.cell(), st_block(s.project.containers.column_stack):
                # La liste native de streamtex (`st_list`), pas des écrits
                # empilés (NG 2026-08-30) — les puces sont celles de la
                # librairie, le style de l'item est celui du DS.
                with st_zoom(150), st_list(list_type="ul", li_style=bs.bullet) as l:
                    for step in _STEPS:
                        with l.item():
                            st_write(bs.bullet, *TF(step, lang))
