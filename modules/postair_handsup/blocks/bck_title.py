"""Titre du deck de secours — le sondage à main levée.

Ce deck existe pour UN scénario : le système sumvadis tombe en séance, et le
sondage se fait quand même — axe par axe, à main levée, sur les mêmes énoncés
(gelés depuis le questionnaire du hub, jamais recopiés à la main).

La slide porte les trois choix d'avant-séance de l'orateur :

- l'illustration PAPERCUT (IA, éditable, repli SVG versionné — une slide qui
  attend une image affiche un trou, jamais) ;
- le SÉLECTEUR DE LANGUE (clé stable ``handsup_lang``) : posé ici une fois,
  relu par chaque page d'axe — en pagination, seule la page courante
  s'exécute, l'état de session est ce qui traverse ;
- l'ancrage biblio de l'instrument, code visible, carte au survol.

SPEAKER NOTES:
Set the language BEFORE facing the room, then never touch it again. One
sentence to open: "the tool is down, the survey is not — we vote by hand,
axis by axis." Then arrow right.
"""
# @guideline: postair-minimal

import streamlit as st
from custom.instrument import LANG_KEY, LANGS, version
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


def build():
    st_marker("Title")
    with st_block(s.project.containers.page_fill_top):
        with st_zoom(140):
            st_write(bs.title, "The survey, ",
                     (s.project.titles.keyword, "by show of hands"),
                     tag=t.div, toc_lvl="1", label="By show of hands")
        st_space("v", "1vh")
        st_write(bs.subtitle,
                 "same nine axes, same statements — your hand is the slider",
                 tag=t.div)
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
        # Le sélecteur écrit directement dans la session — clé STABLE : une
        # clé engendrée se réinitialiserait à chaque rerun sous la main de
        # l'orateur (piège connu, PLAYBOOK §7).
        _left, mid, _right = st.columns([2, 1, 2])
        with mid:
            st.radio("Language", [code for code, _name in LANGS],
                     format_func=dict(LANGS).__getitem__,
                     horizontal=True, key=LANG_KEY,
                     label_visibility="collapsed")
        st_space("v", "1vh")
        st_write(bs.grounding, f"instrument v{version()} — ",
                 citation("guelfi-postair", inline=True), tag=t.div)
