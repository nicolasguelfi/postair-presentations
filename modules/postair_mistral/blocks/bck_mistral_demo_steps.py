"""The demo, step by step — les captures de la démo B, une par sous-slide.

Demande NG (2026-09-07, J-1) : juste après « l'agent au travail », le
parcours de la démo en captures d'écran, à faire AVANCER À LA MAIN — flèche
droite, PageDown ou télécommande. Chaque capture est un ARRÊT de navigation
(``st_slide_break(marker_hidden=True)``, le pattern de Prédire dans genai) :
une seule entrée « Demo: steps » dans la barre latérale, autant d'arrêts
clavier que d'images, retour arrière par flèche gauche. Aucun JavaScript :
même comportement dans l'app et dans l'export statique.

Les images vivent dans ``static/images/slideshows/demo-use/<lang>/`` — UN
DOSSIER PAR LANGUE, choisi par ``build(lang)`` : ``?lang=fr`` projette la
série française (8 captures, 2026-09-07 17:23-17:43), ``en`` la série
anglaise (9 captures, 17:53-18:03). Les deux séries ne sont PAS des
traductions l'une de l'autre : l'orateur raconte celle de sa langue. Déposer
un fichier suffit (ordre = ordre des noms, ``MISTRAL-<LANG>-NN.webp``) ; les
sources PNG pleine taille restent dans ``sumvadis-central/data/images/
screenshots/MISTRAL/``, hors git, passées par ``optimize_images.py``. Un
dossier de langue absent = erreur bruyante, jamais un trou.

Les mêmes dossiers nourrissent les deux diaporamas automatiques de l'annexe
backup (``bck_mistral_bk_demo_loop_fr`` / ``_en``).

Le FAIT vit ici : le titre, le compteur et le panneau s'éditent dans ce bloc.
Aucune affirmation sourcée.

SPEAKER NOTES:
Use these only if the live demo is not possible, or right after it to
replay the path calmly: welcome screen, the agent, its sources, a prompt,
the answer with its section citation. One arrow press per step, narrate each
screen in one sentence. The captures show the speaker's own account — say
it once and move on.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from postair_lang import T, TF
from postair_slideshow import slideshow_images
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    counter = s.project.body.caption + s.center_txt


bs = BlockStyles

#: Le tiroir des captures — un sous-dossier par langue.
_FOLDER = "images/slideshows/demo-use"

#: Réglages datés (2026-09-07) : la capture est l'unique scène.
TUNING = {
    "stage_vh": 85,      # hauteur de la capture (vh) — LE levier de taille (R4d)
    "title_zoom": 60,
}

_MARKER = {"en": "Demo: steps", "fr": "Démo : étapes"}
_TITLE = {"en": ("The demo, ", (s.project.titles.keyword, "step by step")),
          "fr": ("La démo, ", (s.project.titles.keyword, "pas à pas"))}
_TIP_TITLE = {"en": "Reading these screens", "fr": "Lire ces écrans"}
_TOOLTIP = [
    ({"en": "What you see", "fr": "Ce que vous voyez"},
     {"en": ("The exact path of the live demo, captured beforehand: the "
             "welcome screen, the course agent, its sources, a prompt, the "
             "answer with its section citation."),
      "fr": "Le parcours exact de la démo en direct, capturé à l’avance : l’écran d’accueil, l’agent du cours, ses sources, un prompt, la réponse avec sa citation de section."}),
    ({"en": "One language, one series", "fr": "Une langue, une série"},
     {"en": ("The French and English series were captured separately; they "
             "follow the same path but are not screen-for-screen translations."),
      "fr": "Les séries française et anglaise ont été capturées séparément ; même parcours, mais pas une traduction écran par écran."}),
    ({"en": "Moving on", "fr": "Avancer"},
     {"en": "Right arrow or PageDown: next screen. Left arrow: back.",
      "fr": "Flèche droite ou PageDown : écran suivant. Flèche gauche : retour."}),
]


def _ratio(path) -> float:
    """Largeur/hauteur du fichier — la forme de la scène (R4d)."""
    from PIL import Image
    with Image.open(path) as im:
        w, h = im.size
    return (w / h) if h else 16 / 9


def build(lang: str = "en", **_):
    folder = f"{_FOLDER}/{lang}"
    files = slideshow_images(folder)
    n = len(files)
    for i, f in enumerate(files):
        if i:
            # Arrêt clavier SANS entrée de barre latérale (pattern Prédire).
            st_slide_break(marker_hidden=True)
        else:
            st_marker(T(_MARKER, lang))
        # Chaque sous-slide est AUTOSUFFISANTE : titre, panneau, compteur.
        with st_block(s.project.containers.page_fill_top):
            with st_grid(cols="92% 8%",
                         cell_styles=s.project.containers.grid_cell_centered) as g:
                with g.cell():
                    with st_zoom(TUNING["title_zoom"]):
                        if i == 0:
                            st_write(bs.title, *TF(_TITLE, lang), tag=t.div,
                                     toc_lvl="+1", label=T(_MARKER, lang))
                        else:
                            st_write(bs.title, *TF(_TITLE, lang), tag=t.div)
                with g.cell():
                    st_info_tooltip(
                        title=T(_TIP_TITLE, lang),
                        entries=[(T(h, lang), T(d, lang)) for h, d in _TOOLTIP],
                    )
            #st_write(bs.counter, f"{i + 1} / {n}", tag=t.div)
            st_space("v", "1vh")
            with st_block(s.project.containers.media_stage(_ratio(f), TUNING["stage_vh"])):
                st_image(s.project.cards.media_center, width="100%",
                         uri=f"{folder}/{f.name}",
                         alt=f"Demo screenshot {i + 1} of {n} ({lang})")
