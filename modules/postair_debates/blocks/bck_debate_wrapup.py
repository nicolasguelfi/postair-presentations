"""Closing the debate — thank you, every view was heard, all of them live in society.

Rewritten on NG's request (2026-08-30): the slide that ends the bank is now a
NEUTRAL close — no claim, no count on screen. Three short points: thanks for
taking part, every point of view was heard, and all of these postures exist
side by side in society. The corpus (how many figures, how many arguments,
where it all comes from) left the screen and lives in the tooltip, for the
speaker and for whoever is challenged on provenance. The counts still come
from the manifest, so the tooltip cannot overstate the corpus.

The next slide (« No consensus — and that is normal ») says what to take
away; this one only closes the act. Its marker is « Thank you » so the two
no longer share a label in the navigation.

SPEAKER NOTES:
One minute, whichever axes you opened. Thank the room first — every hand
raised, every microphone taken, in a hall this size, is a small act of
courage. Then the point: every view heard this morning is held by someone
in this society, and this room is a fair sample of it. No verdict, no
winner. Then turn the page for the take-aways.
"""
# @guideline: postair-minimal

from custom.content import manifest, poles
from custom.styles import Styles as s
from postair_data import mascot
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.ai_mark import dd35_overlay


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    point = s.project.body.bullet + s.center_txt + s.bold
    detail = s.project.body.caption + s.center_txt
    mascot_name = s.project.body.mascot_name


bs = BlockStyles

# ── Le texte projeté (règle R-i18n) ──────────────────────────────────────────
_MARKER = {"en": "Thank you", "fr": "Merci"}
_TITLE = {"en": ("Thank you for ", (s.project.titles.keyword, "arguing")), "fr": ("Merci d'avoir ", (s.project.titles.keyword, "débattu"))}
_LABEL = {"en": "Thank you", "fr": "Merci"}
#: Trois points courts (≤ 8 mots, un keyword) — un point, une mascotte, une
#: carte bleue. Les mascottes sont nommées, jamais des fichiers (NG 2026-08-30) :
#: Pathos, la pieuvre aux ventouses en cœur, pour le merci ; Voxo, la
#: modératrice « qui capte toutes les voix », pour l'écoute ; Sardo, le banc
#: qui nage « en égaux, sans chef », pour la société.
_POINTS = [
    ("Pathos",
     {"en": ("Thank you for ", (s.project.titles.keyword, "taking part")), "fr": ("Merci d'avoir ", (s.project.titles.keyword, "participé"))},
     {"en": "every hand raised, every microphone taken", "fr": "chaque main levée, chaque micro pris"}),
    ("Voxo",
     {"en": ("Every point of view was ", (s.project.titles.keyword, "heard")), "fr": ("Chaque point de vue a été ", (s.project.titles.keyword, "entendu"))},
     {"en": "for and against, on each pole", "fr": "pour et contre, sur chaque pôle"}),
    ("Sardo",
     {"en": ("All of them live in ", (s.project.titles.keyword, "society")), "fr": ("Tous existent dans la ", (s.project.titles.keyword, "société"))},
     {"en": "side by side — this room is a fair sample", "fr": "côte à côte — cette salle en est un échantillon"}),
]
_TIP_TITLE = {"en": "Where this material comes from", "fr": "D'où vient ce matériau"}
_TIP_CORPUS = {"en": "The corpus", "fr": "Le corpus"}
_TIP_CORPUS_TEXT = {"en": ("{postures} postures, {figures} figures of the study drawn from "
                           "seventeen technological waves — printing, steam, electricity, the "
                           "atom, the network — and {arguments} sourced contemporary arguments. "
                           "{reused} figures defend two different poles, which is exactly as "
                           "inconsistent as real people are."), "fr": "{postures} postures, {figures} figures de l'étude issues de dix-sept vagues technologiques — l'imprimerie, la vapeur, l'électricité, l'atome, le réseau — et {arguments} arguments contemporains sourcés. {reused} figures défendent deux pôles différents, exactement aussi inconséquentes que les vraies personnes."}
_TIP_QUOTES = ({"en": "The quotations", "fr": "Les citations"},
               {"en": ("Verbatim and verified against primary sources. Where a reference is "
                       "still being established, the card says so."), "fr": "Verbatim et vérifiées sur les sources primaires. Quand une référence est encore en cours d'établissement, la carte le dit."})
_TIP_ARGS = ({"en": "The arguments", "fr": "Les arguments"},
             {"en": ("Drawn from the debate material of the study, of three natures — a "
                     "public policy, a concrete case, a public statement — so no pole is "
                     "defended from a single angle."), "fr": "Tirés du matériau de débat de l'étude, de trois natures — une politique publique, un cas concret, une parole publique — pour qu'aucun pôle ne soit défendu sous un seul angle."})
_TIP_TYPED = ({"en": "Nothing typed here", "fr": "Rien n'est écrit ici"},
              {"en": ("Every name, quotation, reference and argument on these slides is "
                      "regenerated from the study. A correction upstream reaches the deck by "
                      "rebuilding it, never by editing a slide."), "fr": "Chaque nom, citation, référence et argument de ces slides est régénéré depuis l'étude. Une correction en amont arrive au deck par régénération, jamais en éditant une slide."})


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    data = manifest()
    corpus = T(_TIP_CORPUS_TEXT, lang).format(
        postures=len(poles()), figures=data.get("figures_used", 0),
        arguments=sum(len(p["arguments"]) for p in poles()),
        reused=data.get("figures_reused", 0))
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="1", label=T(_LABEL, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[
                        (T(_TIP_CORPUS, lang), corpus),
                        (T(_TIP_QUOTES[0], lang), T(_TIP_QUOTES[1], lang)),
                        (T(_TIP_ARGS[0], lang), T(_TIP_ARGS[1], lang)),
                        (T(_TIP_TYPED[0], lang), T(_TIP_TYPED[1], lang)),
                    ],
                )
        st_space("v", "1vh")
        # ONE flat grid — per cell, the mascot above its card (never a second
        # grid for the mascot row), stretched to the remaining height.
        with st_grid(cols=s.project.grids.balanced(len(_POINTS)), gap="1.5vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for name, point, detail in _POINTS:
                m = mascot(name)
                with g.cell():
                    st_image(s.project.cards.media_center, width="min(14vw, 30vh)",
                             uri=m["image"],
                             alt=f"{m['name']}, mascot of the {m['pole'] or 'moderator'} posture",
                             overlay=dd35_overlay())
                    st_write(bs.mascot_name, m["name"], tag=t.div)
                    with st_block(s.project.cards.blue):
                        with st_zoom(130):
                            st_write(bs.point, *TF(point, lang), tag=t.div)
                            st_write(bs.detail, T(detail, lang), tag=t.div)
