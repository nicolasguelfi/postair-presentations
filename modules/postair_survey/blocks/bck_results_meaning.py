"""What the results say about us — two opposite mascots, one flat grid.

The point of the slide is that a cohort is not a bloc: both poles of every
axis are held by real people in this room, and that is precisely what makes
the next twenty minutes worth having. The two mascots are read from the cast
by name, so the slide stays true if the cast is reordered.

SPEAKER NOTES:
Two minutes, and they matter. The room has just seen its averages; the risk
is that everyone concludes "so we all think the same". Say the opposite: an
average is a summary, not a portrait. On every axis, this room holds both
poles — some of you are Rapo, some are Lento, and neither is the correct
answer. That disagreement is not a problem to be fixed before the group work
starts: it is the reason the group work will be any good. Then hand over to
the debate.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from postair_data import mascot
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.ai_mark import dd35_overlay

# One axis, its two poles: the clearest possible illustration that both sides
# live in the same room. Read by name — never by position in the cast.
_FACE_OFF = ("Rapo", "Lento")


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    pole = s.project.body.pole_label
    mascot_name = s.project.body.mascot_name
    lead = s.project.body.bullet + s.center_txt
    versus = s.project.titles.register_title + s.center_txt


bs = BlockStyles

#: Noms et pôles des deux mascottes viennent du cast — hors feuille.
_MARKER = {"en": "What it says about us", "fr": "Ce que cela dit de nous"}
_TITLE = {"en": ("A cohort is ", (s.project.titles.keyword, "not a bloc")), "fr": ("Une cohorte, ", (s.project.titles.keyword, "pas un bloc"))}
_LEAD = {"en": ("both poles · every axis · ", (s.project.titles.keyword, "in this room")), "fr": ("les deux pôles · chaque axe · ", (s.project.titles.keyword, "dans cette salle"))}
_VS = {"en": "vs", "fr": "vs"}
_TIP_TITLE = {"en": "Reading a room, not a person", "fr": "Lire une salle, pas une personne"}
_TIP = [
    ({"en": "Averages hide diversity", "fr": "Les moyennes cachent la diversité"},
     {"en": ("A cohort at fifty on an axis can be made of "
             "people all sitting at fifty — or of two halves at zero and a hundred. "
             "The distribution, not the average, is the interesting object."), "fr": "Une cohorte à cinquante sur un axe peut être faite de gens tous à cinquante — ou de deux moitiés, à zéro et à cent. L'objet intéressant, c'est la distribution, pas la moyenne."}),
    ({"en": "Both poles are here", "fr": "Les deux pôles sont ici"},
     {"en": ("On every one of the nine axes, this room holds "
             "both sides. That is the normal state of any large group, and it is "
             "what the next twenty minutes are for."), "fr": "Sur chacun des neuf axes, cette salle abrite les deux camps. C'est l'état normal de tout grand groupe, et c'est à cela que servent les vingt prochaines minutes."}),
    ({"en": "Why it is useful", "fr": "À quoi cela sert"},
     {"en": ("Your degree programmes put you in teams. A team "
             "where everyone shares one posture is fast and blind; a team that holds "
             "several is slower and much harder to fool."), "fr": "Vos cursus vous mettent en équipe. Une équipe où tout le monde partage une seule posture est rapide et aveugle ; une équipe qui en porte plusieurs est plus lente et bien plus difficile à tromper."}),
    ({"en": "Not a judgement", "fr": "Pas un jugement"},
     {"en": ("No pole is the right answer. The instrument measures "
             "positions, it does not grade them."), "fr": "Aucun pôle n'est la bonne réponse. L'instrument mesure des positions, il ne les note pas."}),
]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    left, right = (mascot(n) for n in _FACE_OFF)
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(T(h, lang), T(d, lang)) for h, d in _TIP],
                )
        st_space("v", s.project.spacing.title_gap)
        st_write(bs.lead, *TF(_LEAD, lang), tag=t.div)
        st_space("v", "2vh")
        # ONE flat grid: mascot · versus · mascot.
        with st_grid(cols="1fr 0.5fr 1fr", gap="1vw",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for side in (left, None, right):
                with g.cell():
                    if side is None:
                        st_write(bs.versus, T(_VS, lang), tag=t.div)
                        continue
                    with st_block(s.project.cards.pole_cell):
                        st_write(bs.pole, side["pole"], tag=t.div)
                        st_image(s.project.cards.media_center, width="min(16vw, 34vh)",
                                 uri=side["image"],
                                 alt=f"{side['name']}, mascot of the {side['pole']} posture",
                                 overlay=dd35_overlay())
                        st_write(bs.mascot_name, side["name"], tag=t.div)
