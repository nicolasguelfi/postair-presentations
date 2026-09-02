"""BACKUP · D'autres outils, même méthode — le podcast NotebookLM (v0.2).

Annexe backup derrière le récap (plan M11, ``podcast``) : le cas NotebookLM
des formations — un podcast de 9 minutes généré depuis des notes de cours.
Assume le message M2 recadré : un outil Google dans une session Mistral & co.,
disclaimer d'usage. Démo audio JAMAIS en direct (son de salle) : la capture du
lecteur seulement (``multimodal_podcast.png``, copyright NG, copie versionnée
de l'illustration du deck genai — exception assumée du dépôt, les
illustrations de ces présentations restent en git).

SPEAKER NOTES:
Only if someone asks « does this work outside Mistral? ». Point at the
screen: course notes went in, a nine-minute two-voice podcast came out —
NotebookLM, a Google tool. Same four steps: frame, sources, test,
iterate. The method is the transferable part; the tool is a detail. Never
play the audio — auditorium sound is not worth the gamble.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    line = s.project.body.bullet + s.center_txt
    caption = s.project.body.caption + s.center_txt
    punch = s.project.titles.subtitle + s.project.colors.amber + s.center_txt


bs = BlockStyles

_MARKER = {"en": "Other tools", "fr": "D’autres outils"}
_TITLE = {"en": ("Other tools, ", (s.project.titles.keyword, "same method")), "fr": ("D’autres outils, ", (s.project.titles.keyword, "même méthode"))}
_LINE = {"en": "course notes in → a 9-minute podcast out (NotebookLM)", "fr": "des notes de cours en entrée → un podcast de 9 minutes en sortie (NotebookLM)"}
_CAPTION = {"en": "generated from the speaker's own notes · audio never played live", "fr": "généré depuis les notes de l’orateur · audio jamais joué en direct"}
_PUNCH = {"en": "frame · sources · test · iterate — whatever the tool", "fr": "cadre · sources · teste · itère — quel que soit l’outil"}

_TIP_TITLE = {"en": "The case, precisely", "fr": "Le cas, précisément"}
_TOOLTIP = [
    ({"en": "What happened", "fr": "Ce qui s’est passé"},
     {"en": ("NotebookLM (Google) received the speaker's own course notes "
             "and generated a nine-minute two-voice podcast discussing them "
             "— the same « give it YOUR sources » step as the course agent, "
             "in another environment."), "fr": "NotebookLM (Google) a reçu les propres notes de cours de l’orateur et a généré un podcast de neuf minutes à deux voix qui en discute — la même étape « donne-lui TES sources » que l’agent de cours, dans un autre environnement."}),
    ({"en": "The disclaimer", "fr": "Le disclaimer"},
     {"en": ("A Google tool shown in a « Mistral & co. » session — on "
             "purpose: the method is the star, the tool is a choice (see the "
             "« your tool, your choice » slide, including where your data "
             "lives)."), "fr": "Un outil Google montré dans une séance « Mistral & co. » — à dessein : la méthode est la vedette, l’outil est un choix (voir la slide « votre outil, votre choix », y compris où vivent vos données)."}),
    ({"en": "Why no live audio", "fr": "Pourquoi pas d’audio en direct"},
     {"en": ("Auditorium sound systems fail in creative ways. The screenshot "
             "carries the point; the podcast itself is a rehearsal artefact."), "fr": "La sonorisation d’un amphi tombe en panne de façons créatives. La capture porte le propos ; le podcast lui-même est un artefact de répétition."}),
]

# ── La main de l'artiste ────────────────────────────────────────────────────
TUNING = {
    #: Ratio mesuré du fichier (1582×628) ; budget hauteur de la capture.
    #: 40 → 36 (porte projection 2026-09-02 : ×1.06 à 1728).
    "ratio": 1582 / 628,
    "stage_vh": 36,
}


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(T(h, lang), T(d, lang)) for h, d in _TOOLTIP],
                )
        st_space("v", s.project.spacing.title_gap)
        with st_zoom(110):
            st_write(bs.line, T(_LINE, lang), tag=t.div)
        st_space("v", "2vh")
        # La capture du lecteur, bornée par SA forme (R4d) — une capture
        # d'écran n'est pas une image générée : pas de pastille DD-35.
        with st_block(s.project.containers.media_stage(TUNING["ratio"], TUNING["stage_vh"])):
            st_image(s.project.cards.media_center, width="100%",
                     uri="images/trainings/multimodal_podcast.png",
                     alt="NotebookLM player: a nine-minute podcast generated from course notes")
        st_space("v", "1vh")
        st_write(bs.caption, T(_CAPTION, lang), tag=t.div)
        st_space("v", "2vh")
        with st_zoom(110):
            st_write(bs.punch, T(_PUNCH, lang), tag=t.div)
