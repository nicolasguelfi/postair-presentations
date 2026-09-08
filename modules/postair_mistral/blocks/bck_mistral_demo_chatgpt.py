"""The same method, in ChatGPT — la démo rejouée dans un autre outil, en vidéo.

Demande NG (2026-09-07, J-1) : juste après la démo pas à pas, une vidéo
montre que la méthode ne dépend pas de Mistral — un tuteur de langue rejoué
dans ChatGPT Voice. Deux enregistrements d'auteur, un par langue, choisis par
``build(lang)`` (pattern videogen) : ``?lang=fr`` joue la piste française
(un francophone demande à « Liliane », tutrice d'anglais, trois expressions
pour la journée d'accueil), ``en`` l'anglaise (un anglophone demande à
« Carl », tuteur de français, trois mots pour la Welcome week). La vidéo prend la scène sous le titre (``media_stage`` au
ratio du fichier, R4d) ; ``autoplay=True, loop=False`` comme le film de
genai — le Chrome de projection lancé par ``run-postair.py`` autorise
l'autoplay sonore.

Les fichiers sont VERSIONNÉS dans ``static/video/`` (exception assumée du
dépôt, comme ``transformers-01.mp4``) et ne portent PAS de pastille DD-35 :
captures d'écran filmées par NG, pas un média généré. Fabrication
(v2 du 2026-09-08, sources ``sumvadis-central/data/videos/Language-tutor/``
— exports ScreenFlow 1920 × 1080 refaits par NG, intouchées) : aucune coupe,
30 → 15 i/s (H.264 CRF 23), son passe-haut 90 Hz + passe-bas 12 kHz +
réduction de souffle ``afftdn`` puis normalisation EBU R128 en deux passes
(−16 LUFS, crête −1,5 dBTP ; les sources crêtaient au-dessus de 0 dBTP, donc
mode dynamique). Durées : EN 1 min 48, FR 2 min 06. La v1 du 2026-09-07
(captures 1920 × 1242, coupées) est remplacée.

SPEAKER NOTES:
About two minutes, sound on. Say one sentence before pressing: « same
method, another tool — and by voice: a tutor for the language you need
tomorrow ». Let it play; point at the correction when the tutor fixes a word
(« ground », not « earth » in FR; the « th » of amphithéâtre in EN). Bridge: « the tool is yours to choose — the method
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
#: Mesuré sur les fichiers (ffprobe) : 1920 × 1080 (v2, 2026-09-08).
_RATIO = 1920 / 1080


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    line = s.project.body.caption + s.center_txt


bs = BlockStyles

#: Réglages datés (2026-09-07 ; ratio 16/9 depuis le 2026-09-08).
TUNING = {"stage_vh": 80, "title_zoom": 60}

_MARKER = {"en": "Demo: ChatGPT", "fr": "Démo : ChatGPT"}
_TITLE = {"en": ("The same method, ", (s.project.titles.keyword, "in ChatGPT")),
          "fr": ("La même méthode, ", (s.project.titles.keyword, "dans ChatGPT"))}
_LINE = {"en": "Charles, the French tutor — real time voice discussion",
         "fr": "Charles, le tuteur de français — discussion en direct à la voix"}
_TIP_TITLE = {"en": "About this video", "fr": "À propos de cette vidéo"}
_TOOLTIP = [
    ({"en": "What you see", "fr": "Ce que vous voyez"},
     {"en": ("A language tutor set up in ChatGPT Voice and put to work: your "
             "situation, a precise request, an answer you can repeat and check."),
      "fr": "Un tuteur de langue installé dans ChatGPT Voice et mis au travail : votre situation, une demande précise, une réponse que vous pouvez répéter et vérifier."}),
    ({"en": "Why another tool", "fr": "Pourquoi un autre outil"},
     {"en": ("The demo runs on Mistral, the method is yours: give the tool "
             "YOUR course, ask precise things, verify. It works the same "
             "elsewhere."),
      "fr": "La démo tourne sur Mistral, la méthode est à vous : donner VOTRE cours à l’outil, demander des choses précises, vérifier. Ça marche pareil ailleurs."}),
    ({"en": "Two recordings", "fr": "Deux enregistrements"},
     {"en": ("Recorded separately by the speaker: in English, Charles teaches "
             "three French words for the Welcome week; in French, Charles teaches "
             "teaches three English expressions for the welcome day. The deck "
             "plays the one of its language."),
      "fr": "Enregistrés séparément par l’orateur : en anglais, Charles enseigne trois mots de français pour la Welcome week ; en français, Charles enseigne trois expressions anglaises pour la journée d’accueil. Le deck joue celui de sa langue."}),
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
