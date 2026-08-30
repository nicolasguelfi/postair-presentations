"""Your place: project manager of your assistants (G10bis).

La slide de la vision NG (2026-08-13) : les assistants génératifs avancés
entrent dans la production professionnelle — la place de l'humain remonte
d'un cran (diriger, juger, assumer) et cette place S'APPREND pendant les
études. La maxime est projetée dans les deux langues : la version anglaise
en ambre porte le message, l'originale française reste sous elle — c'est la
formule de l'auteur, elle se lit telle quelle.

Le FAIT vit ici (règle NG 2026-08-18) : message, maxime, réponse et choix des
citekeys s'éditent dans ce bloc. La phrase bibliographique reste dérivée de
``references.bib`` par ``citation()``/``cite`` — clé inconnue = erreur
bruyante.

SPEAKER NOTES:
Two minutes, right after the careers cards — this is their consequence. Ask
the room the amber question and WAIT three full seconds. Then give the only
honest answer: you cannot. You can only direct what you can judge, and
judgement is built by learning the craft — which is why handing your degree
to the assistant would saw off the branch you will stand on. Bridge to the
actor slide: choosing your posture is choosing how you will direct.
"""
# @guideline: postair-minimal

from custom.prompts import AI_PREFIX, AI_SUFFIX_LANDSCAPE
from custom.refs import citation
from custom.styles import Styles as s
from custom.visuals import hero_image
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.hero_split import hero_split


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    message = s.project.body.bullet + s.center_txt
    punch = s.project.titles.subtitle + s.project.colors.amber + s.center_txt + s.bold
    punch_original = s.project.body.caption + s.center_txt
    answer = s.project.body.body + s.project.colors.keyword + s.center_txt


bs = BlockStyles

_HERO_PROMPT = (
    AI_PREFIX
    + "One abstract paper human silhouette seen from behind, standing on a "
      "small paper podium like an orchestra conductor, arms raised, directing "
      "a team of glowing warm amber paper orbs — plain spheres with no "
      "bodies, no limbs and no faces — each orb floating above its own "
      "little paper desk, and from every desk colourful cut-out paper sheets "
      "fly upward into the luminous sky."
    + AI_SUFFIX_LANDSCAPE
)

# ── La place de l'humain (message projeté ; phrase complète au survol) ──────
_LABEL = "You will all be project managers"
_MESSAGE = ("Generative assistants → professional production · your place: "
            "DIRECT · JUDGE · OWN IT")
#: La maxime dans les deux langues — l'anglaise en ambre porte le message,
#: l'originale française de l'auteur se lit telle quelle.
_PUNCH = "How do you have it done, if you do not know how to do it?"
_PUNCH_ORIGINAL = "« Comment faire faire, si nous ne savons pas faire ? »"
_ANSWER = ("You can only direct what you can judge → learn the craft DURING "
           "your studies")
_DETAIL = ("Employers surveyed across 55 economies expect 39 % of core "
           "skills to change by 2030, with AI literacy and analytical "
           "thinking rising fastest. Directing an assistant that produces in "
           "seconds requires exactly what a degree builds: knowing the "
           "domain well enough to specify, to judge the output, and to take "
           "responsibility for it.")
_CITEKEYS = ["wef2025-jobs"]


def build(lang: str = "en", **_):
    st_marker("Your place")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "All ", (s.project.titles.keyword,
                         "project managers"), tag=t.div,
                         toc_lvl="+1", label="Your place")
            with g.cell():
                st_info_tooltip(title=_LABEL,
                                entries=[("Why this is the hard part",
                                          _DETAIL)])
        st_space("v", s.project.spacing.title_gap)
        with hero_split(s, image=lambda: hero_image(
                "genai_conductor", _HERO_PROMPT,
                "images/genai_conductor_fallback.svg",
                alt_ready=("Papercut silhouette on a podium conducting plain amber "
                           "orbs floating above empty paper desks, colourful sheets "
                           "flying upward"),
                alt_fallback=("Papercut conductor silhouette directing amber orbs "
                              "producing paper sheets"),
                variant="sq")):
            st_write(bs.message, _MESSAGE, " ",
                     citation(*_CITEKEYS), tag=t.div)
            st_space("v", "1vh")
            with st_block(s.project.cards.amber):
                st_write(bs.punch, _PUNCH, tag=t.div)
                st_write(bs.punch_original, _PUNCH_ORIGINAL, tag=t.div)
            st_space("v", "1vh")
            st_write(bs.answer, _ANSWER, tag=t.div)
