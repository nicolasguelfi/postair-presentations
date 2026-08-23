"""Accès au gel de l'instrument — la SEULE source des textes du deck.

``static/data/content.json`` est GELÉ et GÉNÉRÉ par
``_project/tools/build_handsup_content.py`` depuis le questionnaire du hub
``ai-social-profiles`` (v1.9.1+) : aucun énoncé, aucune synthèse, aucun
libellé d'échelle n'est écrit à la main dans ce module — une correction se
fait au hub, jamais ici, et arrive par régénération (plan-postair_handsup
v2, NG 2026-08-23).

La langue projetée est un état de séance (sélecteur de la slide de titre,
clé stable ``handsup_lang``) : chaque page la relit — en pagination, seule
la page courante s'exécute, l'état de session est ce qui traverse.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

import streamlit as st

_FREEZE = Path(__file__).parent.parent / "static" / "data" / "content.json"

#: La clé de widget du sélecteur — STABLE (piège connu : une clé engendrée se
#: réinitialise à chaque rerun sous la main de l'orateur).
LANG_KEY = "handsup_lang"

#: Langues du gel, dans l'ordre du sélecteur ; l'anglais est la langue des
#: decks POSTAIR, donc le défaut.
LANGS = [("en", "English"), ("fr", "Français"), ("de", "Deutsch")]


@lru_cache(maxsize=1)
def _content() -> dict:
    if not _FREEZE.exists():
        raise FileNotFoundError(
            "content.json est absent — le gel de l'instrument n'a pas été "
            "fait : uv run python _project/tools/build_handsup_content.py")
    return json.loads(_FREEZE.read_text(encoding="utf-8"))


def lang() -> str:
    """La langue de la séance — posée par le sélecteur du titre, défaut en."""
    return st.session_state.get(LANG_KEY, "en")


def axes() -> list[dict]:
    """Les 9 axes, dans l'ordre HORAIRE du radar (champ ``order`` du gel)."""
    return _content()["axes"]


def axis(code: str) -> dict:
    """Un axe par son code d'instrument (``TRU``, ``OPT``…) — bruyant sinon."""
    for ax in axes():
        if ax["code"] == code:
            return ax
    raise KeyError(f"axe {code!r} absent du gel — régénérer le contenu ?")


def synthesis(pole: dict) -> dict:
    """La synthèse d'un pôle — bruyant tant que l'amont n'a pas livré.

    Le champ est ``null`` dans le gel tant que le questionnaire du hub n'a
    pas sa v1.10.0 (champ ``synthesis`` par pôle) : jamais de texte
    provisoire écrit ici à la place.
    """
    if pole["synthesis"] is None:
        raise KeyError(
            "synthèse absente du gel — le questionnaire du hub n'a pas "
            "encore livré le champ `synthesis` (ticket ai-social-profiles, "
            "v1.10.0) ; regel ensuite : build_handsup_content.py")
    return pole["synthesis"]


def scale() -> dict:
    """L'échelle pré-découpée pour la slide de vote (agree/disagree/no_opinion)."""
    return _content()["scale"]


def version() -> str:
    """La version du questionnaire embarquée dans le gel (pied de titre)."""
    return _content()["questionnaire_version"]
