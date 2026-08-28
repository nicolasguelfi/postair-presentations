"""Le lexique du chrome — ce qui se répète d'un bloc ou d'un module à l'autre.

Règle D1 (plan-i18n, NG 2026-08-28) : une chaîne projetée par UNE slide vit
dans son bloc (R-facts) ; une chaîne qui apparaît dans DEUX blocs ou plus vit
ici, une seule fois, dans les deux langues. Les blocs l'obtiennent par
``ui("references", lang)`` ; le vocabulaire POSTAIR (axes, pôles, archétypes,
« posture »…) vient du glossaire du hub gelé par ``build_glossary_content.py``
et se lit par ``term("archetype.promethean", lang)``.

Une clé inconnue lève : comme pour les citations, un libellé plausible
imprimé à la place d'un libellé manquant est le pire des échecs en amphi.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from postair_lang import T

_GLOSSARY = Path(__file__).parent / "static" / "data" / "glossary.json"

#: Le chrome partagé — clé → feuille. Ordre : navigation, tooltips
#: récurrents, boutons, libellés d'opérateur.
UI: dict[str, dict[str, str]] = {
    # navigation / appendice
    "references": {"en": "References", "fr": "Références"},
    "references_sub": {"en": "everything this deck asserts, and where it comes from",
                       "fr": "tout ce que ce deck affirme, et d'où cela vient"},
    "title": {"en": "Title", "fr": "Titre"},
    "next_deck": {"en": "Next deck", "fr": "Deck suivant"},
    "next": {"en": "Next", "fr": "Ensuite"},
    "static_html": {"en": "static HTML version", "fr": "version HTML statique"},
    "open_deck": {"en": "Open the deck", "fr": "Ouvrir le deck"},
    # tooltips récurrents
    "where_figure_from": {"en": "Where this figure comes from",
                          "fr": "D'où vient ce chiffre"},
    "verified_at_source": {"en": "Verified at the source", "fr": "Vérifié à la source"},
    "operator_checklist": {"en": "Operator checklist", "fr": "Liste de l'opérateur"},
    "back_to_gallery": {"en": "Back to the waves gallery",
                        "fr": "Retour à la galerie des vagues"},
    "no_consensus": {"en": "No consensus", "fr": "Pas de consensus"},
    # opérateur / sondage
    "anonymous": {"en": "Anonymous", "fr": "Anonyme"},
    "fallback": {"en": "Fallback", "fr": "Repli"},
    "voluntary": {"en": "Voluntary", "fr": "Volontaire"},
    "what_to_comment": {"en": "What to comment", "fr": "Quoi commenter"},
    "room_radar": {"en": "Room radar", "fr": "Radar de la salle"},
    "per_question_detail": {"en": "Per-question detail", "fr": "Détail par question"},
    "nine_axes": {"en": "Nine axes", "fr": "Neuf axes"},
    "mascots": {"en": "Mascots", "fr": "Mascottes"},
    # chiffres et sources
    "source": {"en": "Source", "fr": "Source"},
    "reference": {"en": "Reference", "fr": "Référence"},
    # opening — séries « Already here » et « AI in the faculty »
    "already_here": {"en": "Already here — ", "fr": "Déjà là — "},
    "ai_in": {"en": "AI in ", "fr": "L'IA à la "},
    "faculty_evidence": {"en": "{faculty} — the evidence",
                         "fr": "{faculty} — les preuves"},
    "no_figures_university": {"en": "No figures for this university",
                              "fr": "Aucun chiffre pour cette université"},
    "reported_note": {"en": "Reported inside the source cited on the card, not read "
                            "at the original.",
                      "fr": "Rapporté dans la source citée sur la carte, non lu à "
                            "l'original."},
    # survey — partagés par deux blocs ou plus du parcours
    "under_18": {"en": "Under 18", "fr": "Moins de 18 ans"},
    "anonymous_by_design": {"en": "Anonymous by design", "fr": "Anonyme par conception"},
    "statement_by_statement": {"en": "Statement by statement", "fr": "Énoncé par énoncé"},
    "same_instrument": {"en": "Same instrument", "fr": "Le même instrument"},
    "in_the_app": {"en": "In the app", "fr": "Dans l'application"},
    "help_per_question": {"en": "Help per question", "fr": "Une aide par question"},
    "first_screens_dash": {"en": "The first screens — ", "fr": "Les premiers écrans — "},
    "entertaining_survey": {"en": "An entertaining survey to discover your postures "
                                  "facing the AI revolution.",
                            "fr": "Un sondage ludique pour découvrir vos postures face "
                                  "à la révolution de l'IA."},
}


def ui(key: str, lang: str | None = None) -> str:
    """Un libellé de chrome dans *lang* — clé inconnue = erreur bruyante."""
    try:
        node = UI[key]
    except KeyError:
        raise KeyError(f"libellé de chrome inconnu : {key!r} — l'ajouter à "
                       f"postair_i18n.UI") from None
    return T(node, lang)


@lru_cache(maxsize=1)
def _glossary() -> dict:
    if not _GLOSSARY.exists():
        raise FileNotFoundError(
            "glossary.json est absent — le gel du glossaire n'a pas été fait : "
            "uv run python _project/tools/build_glossary_content.py")
    return json.loads(_GLOSSARY.read_text(encoding="utf-8"))["terms"]


def term(key: str, lang: str | None = None) -> str:
    """Un terme du glossaire du hub (``pole.TRUS.name``, ``archetype.…``)."""
    try:
        node = _glossary()[key]
    except KeyError:
        raise KeyError(f"terme absent du glossaire gelé : {key!r} — une "
                       f"évolution se demande au hub, puis regel") from None
    return T(node, lang)


def terms(prefix: str) -> dict[str, dict[str, str]]:
    """Toutes les entrées d'un espace de clés (``pole.``, ``archetype.``)."""
    return {k: v for k, v in _glossary().items() if k.startswith(prefix)}
