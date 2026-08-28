"""La langue projetée — UNE source pour tous les decks POSTAIR (plan-i18n, NG 2026-08-28).

Trois décisions vivent ici :

- **D2 — d'où vient la langue.** ``current_lang()`` lit, dans l'ordre :
  l'environnement ``STX_LANG`` (l'export statique, un passage par langue),
  la clé de SESSION ``postair_lang`` (posée par le sélecteur de l'orateur sur
  le premier bloc du module), puis le défaut ``"en"``. Le ``book.py`` de
  chaque module la passe à tous les blocs : ``st_book(..., block_kwargs=
  {"lang": current_lang()})`` — un bloc reçoit ``build(lang)``, il ne lit
  jamais l'état de session lui-même.
- **D1 — où vit le texte.** Une feuille traduisible est un dict indexé par
  code de langue, ``{"en": …, "fr": …}``, écrite DANS le bloc (règle R-facts)
  ou dans le lexique partagé ``postair_i18n`` pour ce qui se répète. ``T()``
  la résout ; ``TF()`` résout une SÉQUENCE de fragments ``st_write`` (chaînes
  et tuples ``(style, texte)`` du keyword teal).
- **Repli.** Une traduction absente ne fait JAMAIS un trou projeté : ``T``
  retombe sur l'anglais en séance. La porte ``check_i18n.py`` (``--parity``)
  est ce qui rend l'absence bruyante — avant la répétition, pas devant la
  salle. Une chaîne nue passée à ``T`` est en revanche une erreur immédiate :
  c'est un oubli de migration, pas une traduction manquante.

Patron à deux clés (PLAYBOOK §7, bug vécu 2026-08-24) : le widget du
sélecteur a SA clé (``postair_lang_widget``) et recopie son choix dans
``LANG_KEY`` via ``on_change`` — en pagination, Streamlit purge la clé d'un
widget dès qu'une page s'exécute sans lui.
"""

from __future__ import annotations

import os
from collections.abc import Sequence

import streamlit as st

#: Les langues projetées, dans l'ordre du sélecteur. L'allemand est accepté
#: dans une feuille (structure ouverte, décision NG 2026-08-28) mais n'est ni
#: exposé ni exigé tant qu'il n'est pas ici.
LANGS: tuple[str, ...] = ("en", "fr")
NAMES = {"en": "English", "fr": "Français", "de": "Deutsch"}
DEFAULT = "en"

#: Clé de SESSION (non-widget) — stable, jamais engendrée.
LANG_KEY = "postair_lang"
WIDGET_KEY = "postair_lang_widget"
ENV_KEY = "STX_LANG"


def current_lang() -> str:
    """La langue à projeter maintenant : export > session > défaut."""
    lang = os.environ.get(ENV_KEY) or st.session_state.get(LANG_KEY) or DEFAULT
    if lang not in LANGS:
        raise ValueError(f"langue {lang!r} hors de LANGS={LANGS} — "
                         f"STX_LANG ou sélecteur incohérent")
    return lang


def T(node, lang: str | None = None) -> str:
    """Une feuille ``{"en": …, "fr": …}`` → son texte dans *lang*.

    Repli sur ``DEFAULT`` si la langue manque (jamais de trou projeté) ; une
    chaîne nue lève : c'est une migration inachevée, pas une traduction.
    """
    if isinstance(node, str):
        raise TypeError(f"chaîne nue passée à T() — la mettre en feuille "
                        f"{{'en': …, 'fr': …}} : {node[:60]!r}")
    if not isinstance(node, dict) or "en" not in node:
        raise TypeError(f"feuille invalide (dict avec clé 'en' attendu) : {node!r}")
    lang = lang or current_lang()
    value = node.get(lang)
    if value is None or value == "":
        value = node[DEFAULT]
    return value


def TF(node, lang: str | None = None) -> tuple:
    """Une feuille de FRAGMENTS → le tuple à déplier dans ``st_write``.

    ``{"en": ("Your turn — ", (KW, "join the survey")), "fr": (…)}`` ; une
    feuille dont la valeur est une simple chaîne est acceptée (un fragment).
    """
    value = T(node, lang)
    if isinstance(value, str):
        return (value,)
    if isinstance(value, Sequence):
        return tuple(value)
    raise TypeError(f"fragments invalides : {value!r}")


def st_stage_lang_selector() -> str:
    """Le sélecteur de langue de l'orateur — posé UNE fois par module.

    Exception actée à la règle R-live (NG 2026-08-28) : c'est le second et
    dernier widget des decks, avec le sélecteur de jour. Retourne la langue
    choisie ; sans effet sous ``STX_LANG`` (l'export n'a pas de widget et
    fige la langue de l'environnement).
    """
    if os.environ.get(ENV_KEY):
        return current_lang()
    codes = [*LANGS]

    def _persist() -> None:
        st.session_state[LANG_KEY] = st.session_state[WIDGET_KEY]

    _left, mid, _right = st.columns([2, 1, 2])
    with mid:
        st.radio("Language", codes,
                 index=codes.index(st.session_state.get(LANG_KEY, DEFAULT)),
                 format_func=NAMES.__getitem__, horizontal=True,
                 key=WIDGET_KEY, on_change=_persist,
                 label_visibility="collapsed")
    return current_lang()
