"""Titre du deck de secours — le sondage à main levée.

Ce deck existe pour UN scénario : le système sumvadis tombe en séance, et le
sondage se fait quand même — axe par axe, à main levée, sur les mêmes énoncés
(gelés depuis le questionnaire du hub, jamais recopiés à la main).

La slide porte les trois choix d'avant-séance de l'orateur :

- l'illustration PAPERCUT (IA, éditable, repli SVG versionné — une slide qui
  attend une image affiche un trou, jamais) ;
- le SÉLECTEUR DE LANGUE commun (``postair_lang.st_stage_lang_selector``,
  clé de séance stable ``postair_lang``) : posé ici une fois, la langue
  arrive ensuite à chaque page par ``build(lang)`` ;
- l'ancrage biblio de l'instrument, code visible, carte au survol.

SPEAKER NOTES:
Set the language BEFORE facing the room, then never touch it again. One
sentence to open: "the tool is down, the survey is not — we vote by hand,
axis by axis." Then arrow right.
"""
# @guideline: postair-minimal

from custom.instrument import version
from postair_i18n import ui
from postair_lang import T, TF, st_stage_lang_selector
from custom.prompts import AI_PREFIX, AI_SUFFIX_LANDSCAPE
from custom.refs import citation
from custom.styles import Styles as s
from custom.visuals import hero_image
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    subtitle = s.project.body.bullet + s.center_txt + s.project.colors.amber
    grounding = s.project.body.caption + s.center_txt


bs = BlockStyles

TITLE_PROMPT = (
    AI_PREFIX
    + "A joyful auditorium of abstract paper silhouettes seen from behind, "
      "many arms raised high in a show-of-hands vote, cut-paper hands "
      "catching the light. On the paper stage, a large blank nine-spoke "
      "paper radar chart on an easel. A warm amber paper sun glows above "
      "the audience."
    + AI_SUFFIX_LANDSCAPE
)

# ── Feuilles projetées (règle R-i18n) — l'EN ne bouge pas, le FR se remplit ici.
_TITLE = {"en": ("The survey, ", (s.project.titles.keyword, "by show of hands"))}
_TITLE_LABEL = {"en": "By show of hands"}
_SUBTITLE = {"en": "same nine axes, same statements — your hand is the slider"}
_GROUNDING = {"en": "instrument v{v} — "}


def build(lang: str = "en", **_):
    st_marker(ui("title", lang))
    with st_block(s.project.containers.page_fill_top):
        with st_zoom(140):
            st_write(bs.title, *TF(_TITLE, lang),
                     tag=t.div, toc_lvl="1", label=T(_TITLE_LABEL, lang))
        st_space("v", "1vh")
        st_write(bs.subtitle, T(_SUBTITLE, lang), tag=t.div)
        st_space("v", "2vh")
        hero_image(
            "handsup_title", TITLE_PROMPT,
            fallback="images/postair_radar_question.svg",
            alt_ready=("Papercut auditorium raising hands in a vote, a blank "
                       "nine-spoke radar chart on stage"),
            alt_fallback=("Empty nine-axis POSTAIR radar chart with a large "
                          "question mark in the centre"),
            width="62%",
        )
        st_space("v", "2vh")
        # Le patron à deux clés (bug vécu 2026-08-24) vit désormais dans
        # postair_lang : un seul sélecteur pour tous les decks.
        st_stage_lang_selector()
        st_space("v", "1vh")
        st_write(bs.grounding, T(_GROUNDING, lang).format(v=version()),
                 citation("guelfi-postair", inline=True), tag=t.div)
