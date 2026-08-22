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

Les clips MASCOTTES sont embarqués (static/media/clips, 720×720) ; les vidéos
de FIGURES restent au CDN (doctrine du dépôt : 51 masters ouverts deux ou
trois fois par séance — ces slides sont précisément ces ouvertures). Les
figures viennent du gel debates (content.json, GÉNÉRÉ — lecture seule,
KeyError bruyant si une figure en sort).

Limite connue (2026-08-22) : la vidéo CDN NON active s'affiche en bandeau
écrasé tant que ses métadonnées ne sont pas chargées (l'élément <video> n'a
pas de hauteur avant). En projection, charger la slide une fois avant la
séance suffit (cache navigateur) ; un aspect-ratio posé par st_block ne
traverse pas jusqu'à l'élément vidéo de Streamlit — piste : évolution
streamtex si le besoin devient réel.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from postair_data import axes, mascot_clip
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


class _Styles:
    title = s.project.titles.slide_title + s.center_txt
    name = s.project.body.mascot_name + s.center_txt
    tagline = s.project.body.caption + s.center_txt
    hint = s.project.body.caption + s.center_txt


@lru_cache(maxsize=8)
def _mascot_pole(name: str) -> dict:
    """Le pôle (label, famille) d'une mascotte, cherché dans les deux familles."""
    for family in ("animals", "objects"):
        for ax in axes(family).values():
            for side in ("accel", "decel"):
                if ax[side]["mascot"] == name:
                    return {"label": ax[side]["label"], "family": family}
    raise KeyError(f"mascotte inconnue du cast : {name!r}")


@lru_cache(maxsize=8)
def _figure_video(name: str) -> str:
    """L'URL CDN de la vidéo de présentation d'une figure du gel debates."""
    data = json.loads(_DEBATES_CONTENT.read_text(encoding="utf-8"))
    for pole in data["poles"]:
        for f in pole.get("figures", []):
            if f["name"] == name:
                return f["media"]["video"]
    raise KeyError(f"figure absente du gel debates : {name!r} — régénérer "
                   f"content.json ou corriger le nom.")


# ── Les deux duos (le choix éditorial vit ICI, une ligne à changer) ──────────

def mascot_duo() -> tuple[dict, dict]:
    """Animaux à gauche, objets à droite — les plus fun de chaque famille."""
    duo = []
    for name in ("Pathos", "Bici"):
        pole = _mascot_pole(name)
        duo.append({
            "name": name,
            "tagline": f"{pole['label']} — the {pole['family'][:-1]} family",
            "src": str(_MEDIA / mascot_clip(name, "en")),
        })
    return tuple(duo)


def figure_duo() -> tuple[dict, dict]:
    """Un homme, une femme — les noms les plus sûrs devant l'assemblée."""
    return tuple(
        {"name": name, "tagline": tagline, "src": _figure_video(name)}
        for name, tagline in (
            ("Platon", "great figure — presentation video"),
            ("Ada Lovelace", "great figure — presentation video"),
        ))


# ── Le gabarit ───────────────────────────────────────────────────────────────

#: Vidéos carrées (mascottes 720², figures 960²) : la HAUTEUR borne. 56vh de
#: côté laisse le titre, les noms et la ligne d'indice à l'écran.
_STAGE_VH = 56


def media_duo_slide(title_parts, duo, active: str, *, marker: str,
                    toc_label: str | None = None,
                    tooltip: tuple[str, list[tuple[str, str]]] | None = None,
                    ) -> None:
    """La scène : deux vidéos côte à côte, celle du côté ``active`` se lance.

    :param duo: ``(gauche, droite)`` — dicts ``name``/``tagline``/``src``.
    :param active: ``"left"`` ou ``"right"`` — le côté dont la vidéo démarre
        (son actif, flag Chrome de projection).
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
        with st_grid(cols="50% 50%", gap="1.5vw",
                     cell_styles=s.project.containers.grid_cell_top) as g:
            for side, item in (("left", duo[0]), ("right", duo[1])):
                with g.cell(), st_block(s.project.containers.column_stack_centered):
                    # Productions IA (clips mascottes, vidéos de figures) :
                    # la marque de transparence DD-35, comme partout au deck.
                    with st_block(s.project.containers.media_stage(1.0, _STAGE_VH)), \
                         ai_marked(fit=False, top=True):
                        st_video(item["src"], autoplay=(active == side))
                    st_write(_Styles.name, item["name"], tag=t.div)
                    st_write(_Styles.tagline, item["tagline"], tag=t.div)
        st_space("v", "1vh")
        st_write(_Styles.hint,
                 "▶ sound on — ",
                 ("next plays the right-hand video"
                  if active == "left" else "back replays the left-hand video"),
                 tag=t.div)
