"""Les captures d'écran du parcours SUMVADIS — accès par slug, jamais par fichier.

Module-local (un seul consommateur, un seul service redéployé) : le deck
survey est le seul à projeter les écrans de l'application. La désignation vit
dans le catalogue GELÉ ``static/data/captures-catalogue.json``, produit par
``_project/tools/build_survey_captures.py`` depuis le registre des médias du
dépôt sumvadis ; les octets sont matérialisés par ``sync_media.py`` sous
``static/media/captures/`` et servis par le conteneur (voir
``configure_image_path`` dans ``book.py`` — l'URI doit rester introuvable via
les sources statiques pour sortir en URL relative, jamais en base64).

Défaut ``device="mobile"`` (décision Q14, NG 2026-08-14) : les écrans
participants sont projetés tels que la salle les tient en main. Les écrans de
régie (console, /live, /present, diaporama) se demandent explicitement en
``device="desktop"``.

Slug ou facette absents du catalogue = **KeyError bruyant** — le défaut
silencieux serait une image cassée devant l'amphithéâtre.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

_CATALOGUE = Path(__file__).parent.parent / "static" / "data" / "captures-catalogue.json"


@lru_cache(maxsize=1)
def _entries() -> dict[tuple[str, str, str], dict]:
    if not _CATALOGUE.exists():
        raise FileNotFoundError(
            f"{_CATALOGUE.name} est absent — le geler d'abord : "
            f"uv run python _project/tools/build_survey_captures.py")
    data = json.loads(_CATALOGUE.read_text(encoding="utf-8"))
    return {(c["slug"], c["lang"], c["facette"]): c for c in data["captures"]}


def capture(slug: str, device: str = "mobile", theme: str = "sombre",
            lang: str = "en") -> str:
    """L'URI locale de la capture d'un écran du parcours.

    Le bloc nomme un ÉCRAN (slug du registre sumvadis) et une facette, jamais
    un fichier : le nom local porte l'horodatage de version et change à chaque
    regel.
    """
    facette = f"capture-{device}-{theme}"
    entry = _entries().get((slug, lang, facette))
    if entry is None:
        raise KeyError(
            f"capture absente du catalogue gelé : {slug} · {lang} · {facette} — "
            f"publier l'écran dans sumvadis (parcours_publier.py) ou élargir la "
            f"politique de gel (build_survey_captures.py), puis regeler. "
            f"Jamais de chemin de fichier écrit à la main à la place.")
    return f"captures/{entry['file']}"
