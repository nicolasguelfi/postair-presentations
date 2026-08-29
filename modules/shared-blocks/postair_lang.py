"""La langue projetée — UNE source pour tous les decks POSTAIR (plan-i18n, NG 2026-08-28).

Trois décisions vivent ici :

- **D2 — d'où vient la langue : de l'ADRESSE (NG 2026-08-29).**
  ``current_lang()`` lit, dans l'ordre : l'environnement ``STX_LANG`` (l'export
  statique, un passage par langue), le paramètre d'URL ``?lang=fr`` (posé par
  les deux boutons de chaque carte du hub et propagé par le bouton « Next
  deck »), puis le défaut ``"en"``. Aucun widget, aucun état de session : ce
  qu'on a ouvert est ce qu'on projette, et l'adresse le dit. Changer de
  langue en cours de deck = éditer l'adresse et recharger. Le ``book.py`` de
  chaque module la passe à tous les blocs : ``st_book(..., block_kwargs=
  {"lang": current_lang()})`` — un bloc reçoit ``build(lang)``.
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

Le sélecteur de séance du 28 août (radio + patron à deux clés) est retiré le
29 août : R-live retrouve son unique widget, le sélecteur de jour de survey.
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

ENV_KEY = "STX_LANG"
#: Le paramètre d'adresse : ``…/?lang=fr``.
QUERY_KEY = "lang"


def _query_lang() -> str | None:
    """Le ``?lang=`` de l'adresse — absent hors d'une vraie session Streamlit
    (export headless, contrôle des blocs), et ignoré s'il n'est pas une langue
    connue : un suffixe fautif ne doit jamais casser une projection."""
    try:
        value = st.query_params.get(QUERY_KEY)
    except Exception:  # noqa: BLE001 — pas de contexte de script
        return None
    return value if value in LANGS else None


def current_lang() -> str:
    """La langue à projeter maintenant : export > adresse > défaut."""
    lang = os.environ.get(ENV_KEY) or _query_lang() or DEFAULT
    if lang not in LANGS:
        raise ValueError(f"langue {lang!r} hors de LANGS={LANGS} — STX_LANG incohérent")
    return lang


def with_lang(url: str, lang: str) -> str:
    """Un lien vers un module, dans *lang* : la langue voyage dans l'adresse."""
    sep = "&" if "?" in url else "?"
    return f"{url}{sep}{QUERY_KEY}={lang}"


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
    if value is None:
        value = node[DEFAULT]
    # Une chaîne VIDE est une valeur voulue (un suffixe de gabarit que le
    # français n'a pas), jamais une absence : elle ne retombe pas sur l'EN.
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
