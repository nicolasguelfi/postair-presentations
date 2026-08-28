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


def build(lang: str = "en", **_):
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
        # PATRON À DEUX CLÉS (bug vécu 2026-08-24) : Streamlit PURGE la clé
        # d'un widget dès qu'un rerun se termine sans que le widget ait été
        # instancié — or en pagination, ce sélecteur ne vit que sur cette
        # page. La langue lue par toutes les pages vit donc dans LANG_KEY,
        # une clé NON-widget que la purge ne touche jamais ; le widget a sa
        # propre clé et y recopie son choix via on_change. Constaté sans le
        # patron : français en page 2, retombée en anglais dès la page 3.
        _codes = [code for code, _name in LANGS]

        def _persist_lang() -> None:
            st.session_state[LANG_KEY] = st.session_state["handsup_lang_widget"]

        _left, mid, _right = st.columns([2, 1, 2])
        with mid:
            st.radio("Language", _codes,
                     index=_codes.index(st.session_state.get(LANG_KEY, "en")),
                     format_func=dict(LANGS).__getitem__,
                     horizontal=True, key="handsup_lang_widget",
                     on_change=_persist_lang,
                     label_visibility="collapsed")
        st_space("v", "1vh")
        st_write(bs.grounding, f"instrument v{version()} — ",
                 citation("guelfi-postair", inline=True), tag=t.div)
