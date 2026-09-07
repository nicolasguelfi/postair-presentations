"""The same method, in ChatGPT — la démo rejouée dans un autre outil, en vidéo.

Demande NG (2026-09-07, J-1) : juste après la démo pas à pas, une vidéo
montre que la méthode ne dépend pas de Mistral — Charles, le tuteur, rejoué
dans ChatGPT. Deux enregistrements d'auteur, un par langue, choisis par
``build(lang)`` (pattern videogen) : ``?lang=fr`` joue la piste française,
``en`` l'anglaise. La vidéo prend la scène sous le titre (``media_stage`` au
ratio du fichier, R4d) ; ``autoplay=True, loop=False`` comme le film de
genai — le Chrome de projection lancé par ``run-postair.py`` autorise
l'autoplay sonore.

Les fichiers sont VERSIONNÉS dans ``static/video/`` (exception assumée du
dépôt, comme ``transformers-01.mp4``) et ne portent PAS de pastille DD-35 :
captures d'écran filmées par NG, pas un média généré. Fabrication
(2026-09-07, sources ``sumvadis-central/data/images/screenshots/ChatGPT/``,
intouchées) : coupe des 7 s (FR) / 4 s (EN) d'ouverture, réduction à 1920 px
(15 i/s conservés, H.264 CRF 23), son passe-haut 90 Hz + passe-bas 12 kHz +
réduction de souffle ``afftdn`` puis normalisation EBU R128 en deux passes
(−16 LUFS, crête −1,5 dBTP) — les sources étaient à −50 / −58 LUFS,
inaudibles en amphi.

SPEAKER NOTES:
One minute and change, sound on. Say one sentence before pressing: « same
course, same three prompts, another tool ». Let it play; point at the cited
section when it appears. Bridge: « the tool is yours to choose — the method
is what you keep ».
"""
# @guideline: postair-minimal

from pathlib import Path

from custom.styles import Styles as s
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

#: Résolu depuis le fichier, jamais du répertoire courant (piège du lanceur).
_VIDEO_DIR = Path(__file__).parent.parent / "static" / "video"
#: Un fichier PAR LANGUE — désignation de média, pas feuille de texte.
_VIDEO = {"en": "charles-chatgpt-en.mp4", "fr": "charles-chatgpt-fr.mp4"}
#: Mesuré sur les fichiers (ffprobe) : 1920 × 1242 après réduction.
_RATIO = 1920 / 1242


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    line = s.project.body.caption + s.center_txt


bs = BlockStyles

#: Réglages datés (2026-09-07).
TUNING = {"stage_vh": 80, "title_zoom": 60}

_MARKER = {"en": "Demo: ChatGPT", "fr": "Démo : ChatGPT"}
_TITLE = {"en": ("The same method, ", (s.project.titles.keyword, "in ChatGPT")),
          "fr": ("La même méthode, ", (s.project.titles.keyword, "dans ChatGPT"))}
_LINE = {"en": "Charles, the tutor — same course, same prompts, another tool · ▶ sound on",
         "fr": "Charles, le tuteur — même cours, mêmes prompts, un autre outil · ▶ son activé"}
_TIP_TITLE = {"en": "About this video", "fr": "À propos de cette vidéo"}
_TOOLTIP = [
    ({"en": "What you see", "fr": "Ce que vous voyez"},
     {"en": ("The course tutor rebuilt in ChatGPT and put to work: the same "
             "sources, the same kind of prompts, an answer you can check."),
      "fr": "Le tuteur du cours reconstruit dans ChatGPT et mis au travail : les mêmes sources, le même genre de prompts, une réponse que vous pouvez vérifier."}),
    ({"en": "Why another tool", "fr": "Pourquoi un autre outil"},
     {"en": ("The demo runs on Mistral, the method is yours: give the tool "
             "YOUR course, ask precise things, verify. It works the same "
             "elsewhere."),
      "fr": "La démo tourne sur Mistral, la méthode est à vous : donner VOTRE cours à l’outil, demander des choses précises, vérifier. Ça marche pareil ailleurs."}),
    ({"en": "Two recordings", "fr": "Deux enregistrements"},
     {"en": ("Recorded separately in French and in English by the speaker; "
             "the deck plays the one of its language."),
      "fr": "Enregistrés séparément en français et en anglais par l’orateur ; le deck joue celui de sa langue."}),
]


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                with st_zoom(TUNING["title_zoom"]):
                    st_write(bs.title, *TF(_TITLE, lang),
                             tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(T(h, lang), T(d, lang)) for h, d in _TOOLTIP],
                )
        st_write(bs.line, T(_LINE, lang), tag=t.div)
        st_space("v", "1vh")
        with st_block(s.project.containers.media_stage(_RATIO, TUNING["stage_vh"])):
            st_video(str(_VIDEO_DIR / _VIDEO.get(lang, _VIDEO["en"])),
                     autoplay=True, loop=False)
