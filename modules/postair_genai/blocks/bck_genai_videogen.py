"""Two years of generated video (G5c) — 2023 face au 2025, côte à côte.

Choix de médias NG 2026-09-02 : à gauche, une génération de 2023 issue de
ses formations (le visage cartoon d'un astronaute, une seconde en boucle,
des artefacts — recadrée du cadre crème d'origine, GIF→mp4). À droite, la
présentation vidéo de NG par son DOUBLE IA (asset ``ng__presentation__<lang>``
de la figure ``guelfi``, hub selected-figures, clearance public-ok,
``ai_generated: true``) — une vidéo PAR LANGUE, matérialisée en HD depuis le
CDN (adresses contenu-adressées, règle I3) et versionnée sous
``static/video/videogen-2025-<lang>.mp4`` — exception assumée du dépôt, même
geste que ``transformers-01.mp4``.

Autoplay MUET en boucle (décision NG 2026-09-02, QCM audio) : les clips
tournent dès l'arrivée sur la slide, aucun son, aucun clic — la qualité
visuelle fait la démonstration ; la version parlante existe (105 s EN,
117 s FR). Pastille DD-35 sur les deux (contenus générés par IA).

Le FAIT vit ici (règle NG 2026-08-18) : les années et la nature des deux
clips — dits dans le panneau, jamais projetés en gros. Annonces d'outillage,
pas d'affirmation scientifique : pas de citekey.

SPEAKER NOTES:
One minute, mostly silent — let the loops speak. Point left: 2023, this was
the state of the art, one second of a melting cartoon face. Point right:
2025 — that professor on screen is not filmed, it is generated, my face and
my voice included. Then the amber line, slowly: two years. that's all it
took. If someone asks « so are videos still trustable? »: that is exactly
where the deck goes next (capabilities, then the other side).
"""
# @guideline: postair-minimal

from pathlib import Path

from custom.styles import Styles as s
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.ai_mark import ai_marked

#: Résolus depuis le fichier, jamais du répertoire courant (piège du lanceur).
_VIDEO_DIR = Path(__file__).parent.parent / "static" / "video"

#: Mesuré ffprobe (2026-09-02) : 2023 = 1512×608 (1 s, recadré du cadre
#: crème) ; 2025 = 960×960 (105 s EN, 117 s FR). ``file`` est une chaîne
#: (même fichier dans les deux langues) ou un dict par langue — PAS une
#: feuille i18n : c'est une désignation de média, résolue par ``_clip_file``.
#: ``ratio`` nourrit ``media_stage`` (R4d — chaque clip borne par SA forme).
_CLIPS = [
    {
        "file": "videogen-2023.mp4",
        "ratio": 1512 / 608,
        "year": {"en": "2023", "fr": "2023"},
        "line": {"en": "a cartoon face · one second · artefacts", "fr": "un visage cartoon · une seconde · des artefacts"},
    },
    {
        "file": {"en": "videogen-2025-en.mp4", "fr": "videogen-2025-fr.mp4"},
        "ratio": 1.0,
        "year": {"en": "2025", "fr": "2025"},
        "line": {"en": "your professor — face and voice entirely AI-generated", "fr": "votre professeur — visage et voix entièrement générés par l’IA"},
    },
]


def _clip_file(clip: dict, lang: str) -> str:
    """Le fichier du clip pour ``lang`` — désignation de média, pas feuille."""
    f = clip["file"]
    return f.get(lang, f["en"]) if isinstance(f, dict) else f


_MARKER = {"en": "2023 → 2025", "fr": "2023 → 2025"}
_TITLE = {"en": ("Two years of ", (s.project.titles.keyword, "generated video")), "fr": ("Deux ans de ", (s.project.titles.keyword, "vidéo générée"))}
#: Formulation NG 2026-09-02 (QCM punch : « la version minimale ») — le choc
#: du délai seul, le pont vers la slide Scale reste à l'oral.
_PUNCH = {"en": ("two years. that's all it took",), "fr": ("deux ans. c'est tout ce qu'il a fallu",)}

_TIP_TITLE = {"en": "The two clips, precisely", "fr": "Les deux clips, précisément"}
_TOOLTIP = [
    ({"en": "Left — 2023", "fr": "À gauche — 2023"},
     {"en": ("An early text-to-video generation from the AISE trainings: one "
             "looping second of a morphing cartoon astronaut, visible "
             "artefacts — the honest state of the art of that year."), "fr": "Une génération texte-vers-vidéo précoce des formations AISE : une seconde en boucle d’un astronaute cartoon qui se déforme, des artefacts visibles — l’honnête état de l’art de cette année-là."}),
    ({"en": "Right — 2025", "fr": "À droite — 2025"},
     {"en": ("Nicolas Guelfi's video introduction, entirely AI-generated — "
             "his face and voice, in an English and a French version. Muted "
             "here on purpose: the full version speaks for almost two "
             "minutes."), "fr": "La présentation vidéo de Nicolas Guelfi, entièrement générée par l’IA — son visage et sa voix, en version anglaise et française. Volontairement muette ici : la version complète parle pendant près de deux minutes."}),
    ({"en": "Why it matters here", "fr": "Pourquoi c’est important ici"},
     {"en": ("This is the scale slide made visible: same mechanism, two years "
             "of data + compute — and a reason to trust your EYES a bit less "
             "(the deepfake question comes back in the limits)."), "fr": "C’est la slide de l’échelle rendue visible : même mécanisme, deux ans de données + calcul — et une raison de faire un peu moins confiance à vos YEUX (la question des deepfakes revient dans les limites)."}),
]


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    year = s.project.titles.subtitle + s.project.colors.keyword + s.center_txt + s.bold
    line = s.project.body.caption + s.center_txt
    punch = s.project.titles.subtitle + s.project.colors.amber + s.center_txt


bs = BlockStyles


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
        with st_grid(cols="50% 50%", gap="1.5vw",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for clip in _CLIPS:
                with g.cell():
                    with st_zoom(140):
                        st_write(bs.year, T(clip["year"], lang), tag=t.div)
                    st_space("v", "1vh")
                    # Chaque clip borne par SA forme (2023 large, 2025 carré)
                    # — la scène borne par la hauteur ET la cellule (R4d).
                    # 52 → 42 vh à l'arrivée du clip CARRÉ (porte projection
                    # 2026-09-02 : ×1.09/×1.11 aux deux références).
                    with st_block(s.project.containers.media_stage(clip["ratio"], 42)):
                        with ai_marked(fit=False, top=True):
                            st_video(str(_VIDEO_DIR / _clip_file(clip, lang)),
                                     loop=True, autoplay=True)
                    st_space("v", "1vh")
                    st_write(bs.line, T(clip["line"], lang), tag=t.div)
        st_space("v", "3vh")
        with st_zoom(130):
            for line in T(_PUNCH, lang):
                st_write(bs.punch, line, tag=t.div)
