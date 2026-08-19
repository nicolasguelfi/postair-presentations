"""La chaîne des decks — la slide « module suivant », en boucle.

Source de vérité : ``postair_collection/collection.toml`` — l'ordre officiel
du jour (``order``) et l'URL de chaque module (``project_url``), surchargée en
déploiement par ``STX_URL_<KEY>`` : exactement la résolution de ``bck_home``.
Rien n'est écrit ici : ajouter un module au toml suffit, la chaîne suit — le
hub et les boutons de fin de deck ne peuvent pas diverger.

``build_next_module_slide(s)`` rend la dernière slide présentée d'un deck :
UN gros bouton (ambre — l'accent focal de la slide) qui ouvre le module
suivant dans le MÊME onglet (``target="_top"`` : l'opérateur enchaîne, il ne
collectionne pas les onglets). Le module courant est détecté par le répertoire
de travail — le conteneur comme le lancement local font ``cd`` dans le module.
Après le dernier module de l'ordre, la boucle revient au premier.

Décision NG 2026-08-19 (« C + B allégée ») : la cible locale ou déployée
n'est JAMAIS un geste de clic — c'est l'ENVIRONNEMENT qui décide, via les
``STX_URL_<KEY>`` que ``run-postair.py`` pose sur chaque instance locale (une
instance locale chaîne en local, la déployée en déployé). L'axe app/HTML est
un petit lien discret sous le bouton.

L'URL de l'export HTML se DÉRIVE de l'infrastructure : chaque conteneur sert
son export sous ``<project_url>/html/`` (nginx.conf — ``location = /html/``
redirige vers ``/html/postair_<key>/postair_<key>.html``). Précédence :
``STX_EXPORT_URL_<KEY>`` (env) > ``export_url`` (toml) > convention
``project_url + /html/``. La convention s'appuie sur l'URL de PRODUCTION du
toml, jamais sur l'URL résolue : en local, aucun nginx ne sert ``/html/`` —
le lien pointe donc vers l'export déployé, qui existe toujours (et sert de
secours si l'app locale déraille). Un export local servi se déclare par
``STX_EXPORT_URL_<KEY>``.

⚠ Module PARTAGÉ (shared-blocks) : comme ``postair_event``, une édition ici
exige un redémarrage du serveur Streamlit — hors du périmètre du rechargement
à chaud des blocs.
"""

from __future__ import annotations

import os
import tomllib
from functools import lru_cache
from pathlib import Path

from streamtex import st_block, st_html, st_marker, st_space, st_write
from streamtex.enums import Tags as t

#: Le toml du hub — la seule déclaration de l'ordre et des URLs.
_TOML = Path(__file__).parent.parent / "postair_collection" / "collection.toml"

#: Le bouton : style maison de ``bck_home``, à l'échelle amphi. Taille en
#: unités de fenêtre + variable d'échelle — suit le projecteur et ``SCALE``.
_BUTTON_CSS = (
    "display:inline-block;max-width:80vw;padding:4vh 5vw;"
    "background:#F39C12;color:#1A1A2E;text-align:center;border-radius:2vh;"
    "text-decoration:none;font-weight:800;line-height:1.25;"
    "font-size:min(5vw, calc(var(--stx-scale-15, 48pt) * 1.1));"
)


@lru_cache(maxsize=1)
def chain() -> tuple[dict, ...]:
    """Les modules du jour, dans l'ordre du toml, URL résolue (env > toml)."""
    with open(_TOML, "rb") as f:
        config = tomllib.load(f)
    entries = []
    for key, data in sorted(config.get("projects", {}).items(),
                            key=lambda item: item[1].get("order", 0)):
        env_suffix = key.upper().replace("-", "_")
        entries.append({
            "key": key,
            "title": data.get("title", key),
            "emoji": data.get("emoji", "📄"),
            "description": data.get("description", ""),
            "url": os.environ.get(f"STX_URL_{env_suffix}",
                                  data.get("project_url", "#")),
            # Export HTML : env > toml > convention /html/ du nginx conteneur
            # — dérivée de l'URL de PRODUCTION (voir docstring du module).
            "export_url": os.environ.get(
                f"STX_EXPORT_URL_{env_suffix}",
                data.get("export_url",
                         data.get("project_url", "").rstrip("/") + "/html/"
                         if data.get("project_url") else None)),
        })
    if not entries:
        raise ValueError(f"{_TOML} ne déclare aucun module — la chaîne est vide.")
    return tuple(entries)


def current_key() -> str:
    """Le module courant, déduit du répertoire de travail (``postair_<key>``)."""
    name = Path.cwd().name
    key = name.removeprefix("postair_")
    if not any(m["key"] == key for m in chain()):
        known = ", ".join(m["key"] for m in chain())
        raise ValueError(
            f"Répertoire courant {name!r} : module {key!r} inconnu de "
            f"collection.toml ({known}). Passer ``current=`` explicitement.")
    return key


def next_module(current: str) -> dict:
    """Le module qui suit *current* dans l'ordre du jour — boucle à la fin."""
    keys = [m["key"] for m in chain()]
    if current not in keys:
        raise ValueError(f"module {current!r} inconnu de collection.toml "
                         f"({', '.join(keys)})")
    return chain()[(keys.index(current) + 1) % len(chain())]


def build_next_module_slide(s, current: str | None = None) -> None:
    """La slide de fin de deck : un gros bouton vers le module suivant.

    :param s: la façade ``Styles`` du module appelant (``s`` dans les blocs).
    :param current: clé du module courant ; détectée du répertoire de travail
        si omise.
    """
    nxt = next_module(current or current_key())
    st_marker("Next deck")
    with st_block(s.project.containers.page_fill_center):
        st_write(s.project.titles.subtitle + s.center_txt, "Next", tag=t.div)
        st_space("v", "4vh")
        st_html(
            f'<div style="text-align:center;">'
            f'<a href="{nxt["url"]}" target="_top" style="{_BUTTON_CSS}">'
            f'{nxt["emoji"]}&nbsp; {nxt["title"]}</a></div>'
        )
        st_space("v", "4vh")
        st_write(s.project.body.caption + s.center_txt,
                 nxt["description"], tag=t.div)
        # L'axe app/HTML (B allégée) : un lien discret, seulement si déclaré.
        if nxt["export_url"]:
            st_space("v", "2vh")
            st_html(
                f'<div style="text-align:center;">'
                f'<a href="{nxt["export_url"]}" target="_top" '
                f'style="color:#95A5A6;font-size:calc(var(--stx-scale-9, 22pt)'
                f' * 0.9);text-decoration:underline;">static HTML version</a>'
                f'</div>'
            )
