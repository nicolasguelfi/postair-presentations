"""Who is speaking — the host behind the reveal, in a few facts.

The reveal film introduced a figure; this slide gives it a name. Portrait on
one side, a handful of facts on the other — few enough to be read from the
back of the amphitheatre.

Both visuals are ILLUSTRATIONS produced for these presentations: versioned
in git under ``static/images/host/`` (the repo's assumed exception — they
never go to the CDN, and ``sync_media`` plays no part). The day the studio
publishes the still grid of the nine incarnations (the host wearing each of
the nine postures), drop it as ``host_incarnations.webp`` and the slide
switches to it — the same present-file pattern as the survey deck's
``bck_axes_radar`` (wheel vs empty radar):
never a missing image in front of the amphitheatre.

SPEAKER NOTES:
Thirty seconds, third person then first: « …and that was me ». One sentence
on why YOU host this day, one on the incarnations — you will wear all nine
postures today, which is the whole point: no posture is shameful here, and
the host himself will argue each of them. Then hand over: « here is what we
will do together » (agenda comes after the framing facts).
"""
# @guideline: postair-minimal

from pathlib import Path

from custom.styles import Styles as s
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.ai_mark import dd35_overlay

_STATIC = Path(__file__).parent.parent / "static"

#: Portrait de l'orateur — illustration versionnée, jamais au CDN.
_PORTRAIT = "images/host/host_portrait.webp"
#: La grille des 9 incarnations, quand le studio la publie (repli : portrait).
_INCARNATIONS = "images/host/host_incarnations.webp"

#: L'orateur porte-t-il une image de synthèse ? Production studio = marquée
#: DD-35 d'office ; passer à False UNIQUEMENT si le portrait est une
#: photographie réelle (l'absence de marque doit se mériter par la donnée).
_SYNTHETIC = True

# TODO-NG — chaque fait est à VALIDER avant projection ; rien d'inventé ne
# passe devant 1500 personnes. (fait court, détail lisible du fond.)
_FACTS = [
    ({"en": "Dr. Nicolas Guelfi"}, {"en": "your host for these three hours"}),
    ({"en": "Professor, FSTM"}, {"en": "software engineering & artifical intelligence · University of Luxembourg"}),  # TODO-NG vérifier l'intitulé exact
    ({"en": "POSTAIR"}, {"en": "author of the posture instrument used today ;)"}),    # TODO-NG formulation
]

_MARKER = {"en": "Your host"}
_TITLE = {"en": ("Your ", (s.project.titles.keyword, "host"))}
_TIP_TITLE = {"en": "About the host"}
# TODO-NG — panneau à remplir par l'auteur.
_TIP = [
    ({"en": "Who"}, {"en": "To be provided by the author."}),
    ({"en": "The nine incarnations"},
     {"en": ("The host appears in each of the nine postures of the instrument: "
             "no posture is shameful, and every one of them will be argued for "
             "today.")}),
]
_CAPTION = {"en": "one host · nine postures"}


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    fact = s.project.body.bullet + s.center_txt + s.bold
    detail = s.project.body.caption + s.center_txt
    caption = s.project.body.mascot_name + s.center_txt


bs = BlockStyles


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    incarnations_ready = (_STATIC / _INCARNATIONS).exists()
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
        st_space("v", "2vh")
        if incarnations_ready:
            st_image(s.project.cards.media_center, width="min(70vw, 62vh)",
                     uri=_INCARNATIONS,
                     alt="The host portrayed nine times, once in each of the "
                         "nine postures of the instrument",
                     overlay=dd35_overlay(_SYNTHETIC))
            st_write(bs.caption, T(_CAPTION, lang), tag=t.div)
        else:
            with st_grid(cols="40% 60%", gap="1.5vw",
                         cell_styles=s.project.containers.grid_cell_centered) as g:
                with g.cell():
                    st_image(s.project.cards.media_center, width="min(32vw, 63vh)",
                             uri=_PORTRAIT,
                             alt="Portrait of the host of the AI Day",
                             overlay=dd35_overlay(_SYNTHETIC))
                with g.cell(), st_block(s.project.containers.column_stack):
                    with st_zoom(150):
                        for fact, detail in _FACTS:
                            with st_block(s.project.cards.blue):
                                st_write(bs.fact, T(fact, lang), tag=t.div)
                                st_write(bs.detail, T(detail, lang), tag=t.div)
