"""Une slide « duo vidéo » — deux vidéos carrées côte à côte, UNE seule se lance.

But (NG 2026-08-22) : montrer que l'application permet de consulter les
mascottes et les grandes figures, vidéos comprises. Deux duos : les deux
mascottes les plus fun (une par famille — animaux à gauche, objets à droite)
et deux figures célèbres (un homme, une femme).

Le geste « flèche droite = la vidéo de droite se lance avec le son » repose
sur la PAGINATION : chaque duo occupe DEUX pages jumelles — même scène, seule
la vidéo `active` change. En mode paginé, seule la page courante s'exécute :
arriver sur la page relance son ``st_video(autoplay=True)``. Le son suit la
règle de projection des vidéos du deck d'ouverture (bck_wait_loop) : Chrome
lancé avec ``--autoplay-policy=no-user-gesture-required`` ; sans le flag, la
surimpression « ▶ sound on » rappelle le clic de secours.

TOUT est embarqué (NG 2026-08-22, « tout doit marcher tout de suite ») :
les clips mascottes (static/media/clips, 720×720) comme les vidéos des DEUX
figures projetées (static/media/figure-videos/, matérialisées par
sync_media.py — exception assumée à la règle « vidéos de figures au CDN »,
qui reste vraie pour les 49 autres). Une vidéo distante non chargée
s'affichait en bandeau écrasé : en local, les métadonnées sont immédiates,
la case est juste dès le premier affichage, sans geste préalable.
Les figures viennent du gel debates (content.json, GÉNÉRÉ — lecture seule) ;
changer le casting = changer figure_duo() ICI et FIGURE_VIDEO_MODULES dans
sync_media.py, puis relancer l'outil. Fichier absent = échec bruyant.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from postair_data import axes, mascot_clip
from postair_i18n import term
from postair_lang import T
from postair_pack.components.ai_mark import ai_marked
from shared_widgets import st_info_tooltip
from streamtex import st_block, st_grid, st_marker, st_space, st_video, st_write
from streamtex.enums import Tags as t

from custom.styles import Styles as s

#: Les octets des clips mascottes matérialisés (st.video veut un chemin réel).
_MEDIA = Path(__file__).parent.parent / "static" / "media"

#: Le gel debates — la seule source des figures (généré, jamais édité ici).
_DEBATES_CONTENT = (Path(__file__).parent.parent.parent / "postair_debates"
                    / "static" / "data" / "content.json")

#: La rendition projetée — MIROIR de FIGURE_VIDEO_ROLE dans sync_media.py.
_ROLE = "video"


class _Styles:
    title = s.project.titles.slide_title + s.center_txt
    name = s.project.body.mascot_name + s.center_txt
    tagline = s.project.body.caption + s.center_txt
    hint = s.project.body.caption + s.center_txt


# ── Les feuilles du gabarit (règle R-i18n) ───────────────────────────────────
#: Le titre des DEUX pages jumelles d'un duo — projeté par deux blocs, donc ici.
FIGURES_TITLE = {"en": ("Every figure has its ", (s.project.titles.keyword, "own video")), "fr": ("Chaque figure a sa ", (s.project.titles.keyword, "propre vidéo"))}
MASCOTS_TITLE = {"en": ("Every mascot has its ", (s.project.titles.keyword, "own video")), "fr": ("Chaque mascotte a sa ", (s.project.titles.keyword, "propre vidéo"))}
#: La ligne sous une mascotte : son pôle (donnée du cast, hors feuille) et
#: sa famille.
_MASCOT_TAGLINE = {"en": "{label} — the {family} family", "fr": "{label} — la famille des {family}"}
_FAMILY = {"animals": {"en": "animal", "fr": "animaux"}, "objects": {"en": "object", "fr": "objets"}}
_FIGURE_TAGLINE = {"en": "great figure — presentation video", "fr": "grande figure — vidéo de présentation"}
#: L'indice de projection, sous les deux vidéos.
_SOUND_ON = {"en": "▶ sound on — ", "fr": "▶ son activé — "}
_NEXT_RIGHT = {"en": "next plays the right-hand video", "fr": "suivant lance la vidéo de droite"}
_BACK_LEFT = {"en": "back replays the left-hand video", "fr": "retour relance la vidéo de gauche"}


def _pole_label(pole: dict, lang: str) -> str:
    """Le libellé de pôle dans la langue projetée.

    L'anglais reste celui du cast, byte-identique. Les autres langues viennent
    du glossaire du hub gelé, cherchées PAR CLÉ (``pole.<CODE>.name``) grâce
    au ``pole_code`` que le cast porte depuis le contrat v2.3.0 (studio
    MC-260829-001) — jamais par égalité de libellés entre deux sources. Un
    code absent est une erreur bruyante au build, jamais un trou.
    """
    if lang == "en":
        return pole["label"]
    code = pole.get("code")
    if not code:
        raise KeyError(f"mascotte sans pole_code dans le cast gelé : {pole['mascot']!r} "
                       f"— regel du studio (contrat cartes ≥ 2.3.0)")
    return term(f"pole.{code}.name", lang)


@lru_cache(maxsize=8)
def _mascot_pole(name: str) -> dict:
    """Le pôle (label, famille) d'une mascotte, cherché dans les deux familles."""
    for family in ("animals", "objects"):
        for ax in axes(family).values():
            for side in ("accel", "decel"):
                if ax[side]["mascot"] == name:
                    return {"label": ax[side]["label"], "code": ax[side]["code"],
                            "mascot": name, "family": family}
    raise KeyError(f"mascotte inconnue du cast : {name!r}")


@lru_cache(maxsize=8)
def _figure_video(name: str, lang: str = "en") -> str:
    """Le chemin LOCAL de la vidéo de présentation d'une figure, dans la
    langue projetée (``videos[lang]`` du gel, repli sur le master EN).

    L'URL CDN du gel debates désigne ; les octets sont matérialisés par
    ``sync_media.py`` sous ``figure-videos/`` (nom = deux derniers segments
    de l'URL — même règle des deux côtés, aucune autre convention).
    """
    data = json.loads(_DEBATES_CONTENT.read_text(encoding="utf-8"))
    for pole in data["poles"]:
        for f in pole.get("figures", []):
            if f["name"] == name:
                url = (f["media"].get("videos") or {}).get(lang) or f["media"][_ROLE]
                local = _MEDIA / "figure-videos" / "__".join(url.split("/")[-2:])
                if not local.exists():
                    raise FileNotFoundError(
                        f"vidéo de {name} non matérialisée : {local} — lancer "
                        f"uv run python _project/tools/sync_media.py (et vérifier "
                        f"FIGURE_VIDEO_MODULES si le casting a changé)")
                return str(local)
    raise KeyError(f"figure absente du gel debates : {name!r} — régénérer "
                   f"content.json ou corriger le nom.")


# ── Les deux duos (le choix éditorial vit ICI, une ligne à changer) ──────────

def mascot_duo(lang: str = "en") -> tuple[dict, dict]:
    """Animaux à gauche, objets à droite — les plus fun de chaque famille.

    Le clip suit la langue projetée (``build(lang)``, règle R-i18n) : le
    catalogue gelé porte une rendition par langue pour chaque mascotte.
    """
    duo = []
    for name in ("Pathos", "Bici"):
        pole = _mascot_pole(name)
        duo.append({
            "name": name,
            "tagline": T(_MASCOT_TAGLINE, lang).format(
                label=_pole_label(pole, lang),
                family=T(_FAMILY[pole["family"]], lang)),
            "src": str(_MEDIA / mascot_clip(name, lang)),
        })
    return tuple(duo)


def figure_duo(lang: str = "en") -> tuple[dict, dict]:
    """Un homme, une femme — les noms les plus sûrs devant l'assemblée."""
    return tuple(
        {"name": name, "tagline": T(_FIGURE_TAGLINE, lang), "src": _figure_video(name, lang)}
        for name in ("Platon", "Ada Lovelace"))


# ── Le gabarit ───────────────────────────────────────────────────────────────

#: Vidéos carrées (mascottes 720², figures 960²) : la HAUTEUR borne. 56vh de
#: côté laisse le titre, les noms et la ligne d'indice à l'écran — le défaut,
#: surchargeable à l'appel par ``stage_vh=`` (le SEUL levier de taille : une
#: unité vh que tout respecte, là où un st_zoom bute sur la borne 100 %).
_STAGE_VH = 56


def media_duo_slide(title_parts, duo, active: str, *, marker: str,
                    toc_label: str | None = None,
                    tooltip: tuple[str, list[tuple[str, str]]] | None = None,
                    stage_vh: int = _STAGE_VH,
                    lang: str = "en") -> None:
    """La scène : deux vidéos côte à côte, celle du côté ``active`` se lance.

    :param duo: ``(gauche, droite)`` — dicts ``name``/``tagline``/``src``.
    :param active: ``"left"`` ou ``"right"`` — le côté dont la vidéo démarre
        (son actif, flag Chrome de projection).
    :param stage_vh: le CÔTÉ des vidéos carrées, en vh — passer la même
        valeur aux deux pages jumelles d'un duo, sinon la taille saute au
        passage de la flèche. Module custom/ : redémarrage complet pour voir
        une édition d'ICI (les blocs, eux, rechargent à chaud).
    :param lang: la langue projetée — ne sert qu'à l'indice de projection ;
        titre, marqueur et tooltip arrivent déjà résolus par le bloc.
    """
    st_marker(marker)
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                toc = ({"toc_lvl": "+1", "label": toc_label} if toc_label else {})
                st_write(_Styles.title, *title_parts, tag=t.div, **toc)
            with g.cell():
                if tooltip:
                    st_info_tooltip(title=tooltip[0], entries=tooltip[1])
        st_space("v", "1vh")
        with st_grid(cols="50% 50%", gap="1vw",
                     cell_styles=s.project.containers.grid_cell_top) as g:
            for side, item in (("left", duo[0]), ("right", duo[1])):
                with g.cell(), st_block(s.project.containers.column_stack_centered):
                    # Productions IA (clips mascottes, vidéos de figures) :
                    # la marque de transparence DD-35, comme partout au deck.
                    with st_block(s.project.containers.media_stage(1.0, stage_vh)), \
                         ai_marked(fit=False, top=True):
                        st_video(item["src"], autoplay=(active == side))
                    st_write(_Styles.name, item["name"], tag=t.div)
                    st_write(_Styles.tagline, item["tagline"], tag=t.div)
        st_space("v", "1vh")
        st_write(_Styles.hint,
                 T(_SOUND_ON, lang),
                 T(_NEXT_RIGHT if active == "left" else _BACK_LEFT, lang),
                 tag=t.div)
