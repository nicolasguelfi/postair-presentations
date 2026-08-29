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
UN export PAR LANGUE sous ``<project_url>/html/<lang>/`` (nginx.conf —
``location = /html/<lang>/`` redirige vers
``/html/<lang>/postair_<key>/postair_<key>.html`` ; plan-i18n D3). La langue
est celle reçue par ``build(lang)`` — et le bouton « Next deck » la PROPAGE
dans l'adresse du module suivant (``?lang=``, ``postair_lang.with_lang``) ; un
``{lang}`` littéral dans ``export_url`` ou ``STX_EXPORT_URL_<KEY>`` est
substitué. La ligne rendue
(NG 2026-08-19, « flexible et tolérant aux fautes ») :
``static HTML version: local / remote`` — DEUX liens :

- ``remote`` : ``export_url`` (toml) sinon convention ``project_url + /html/``
  — l'export déployé, toujours présent ;
- ``local`` : ``STX_EXPORT_URL_<KEY>`` (env) sinon convention
  ``STX_URL_<KEY> + /html/`` quand ``run-postair`` a déclaré une instance
  locale — absent sinon (en production la ligne ne montre que ``remote``).
  ⚠ ``/html/`` local suppose un service statique (le nginx du conteneur en
  prod) : sans lui le lien local répond 404 — toléré par choix, les deux
  liens sont là précisément pour se secourir l'un l'autre.

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

from postair_i18n import ui
from postair_lang import T, with_lang

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


def leaf(value) -> dict:
    """Un texte du toml → feuille ``{"en": …}`` (une chaîne nue = anglais)."""
    return value if isinstance(value, dict) else {"en": str(value)}


def export_url(template: str | None, lang: str) -> str | None:
    """L'URL d'export dans *lang* — substitue le ``{lang}`` du gabarit."""
    return template.replace("{lang}", lang) if template else None


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
            "title": leaf(data.get("title", key)),
            "emoji": data.get("emoji", "📄"),
            "description": leaf(data.get("description", "")),
            "url": os.environ.get(f"STX_URL_{env_suffix}",
                                  data.get("project_url", "#")),
            # Exports HTML (voir docstring) : remote = toml/convention prod ;
            # local = env explicite, sinon convention sur l'instance locale
            # déclarée par run-postair, sinon absent.
            "export_remote": data.get(
                "export_url",
                data.get("project_url", "").rstrip("/") + "/html/{lang}/"
                if data.get("project_url") else None),
            "export_local": os.environ.get(
                f"STX_EXPORT_URL_{env_suffix}",
                os.environ[f"STX_URL_{env_suffix}"].rstrip("/") + "/html/{lang}/"
                if f"STX_URL_{env_suffix}" in os.environ else None),
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


def build_next_module_slide(s, current: str | None = None,
                            lang: str = "en") -> None:
    """La slide de fin de deck : un gros bouton vers le module suivant.

    :param s: la façade ``Styles`` du module appelant (``s`` dans les blocs).
    :param current: clé du module courant ; détectée du répertoire de travail
        si omise.
    :param lang: la langue projetée, reçue par ``build(lang)``.
    """
    nxt = next_module(current or current_key())
    st_marker(ui("next_deck", lang))
    with st_block(s.project.containers.page_fill_center):
        st_write(s.project.titles.subtitle + s.center_txt, ui("next", lang), tag=t.div)
        st_space("v", "4vh")
        st_html(
            f'<div style="text-align:center;">'
            f'<a href="{with_lang(nxt["url"], lang)}" target="_top" style="{_BUTTON_CSS}">'
            f'{nxt["emoji"]}&nbsp; {T(nxt["title"], lang)}</a></div>'
        )
        st_space("v", "4vh")
        st_write(s.project.body.caption + s.center_txt,
                 T(nxt["description"], lang), tag=t.div)
        # L'axe app/HTML (B allégée) : une ligne discrète, un lien par cible
        # disponible — « local » seulement quand une instance locale est
        # déclarée (run-postair), « remote » toujours.
        targets = [(label, url) for label, url in
                   (("local", export_url(nxt["export_local"], lang)),
                    ("remote", export_url(nxt["export_remote"], lang))) if url]
        if targets:
            link_css = ("color:#95A5A6;text-decoration:underline;")
            links = " / ".join(
                f'<a href="{url}" target="_top" style="{link_css}">{label}</a>'
                for label, url in targets)
            st_space("v", "2vh")
            st_html(
                f'<div style="text-align:center;color:#95A5A6;'
                f'font-size:calc(var(--stx-scale-9, 22pt) * 0.9);">'
                f'{ui("static_html", lang)}: {links}</div>'
            )
