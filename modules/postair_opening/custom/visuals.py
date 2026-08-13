"""Le visuel dominant d'une slide — image IA managée, avec repli SVG versionné.

Règle NG (2026-08-11) : dans un amphithéâtre, une image bien conçue vaut mille
mots — chaque slide se construit autour d'un visuel dominant, le texte porte le
minimum. Pattern repris de la roue de ``postair_opening/bck_axes_radar`` :

- ``uri`` est le REPLI, pas la source : dès qu'une version managée de l'image
  existe (générée par l'auteur via l'éditeur, versionnée sous
  ``static/images/managed/``), ``st_image`` la préfère et le SVG n'est plus lu ;
- une slide sans image n'est pas une étape intermédiaire acceptable — c'est un
  trou devant l'amphithéâtre : chaque visuel a donc son repli SVG, versionné
  (exception assumée du dépôt : les illustrations de ces présentations restent
  en git et ne vont jamais au CDN).
"""

from __future__ import annotations

import json
from pathlib import Path

from streamtex import st_image

from custom.config import IS_EDITABLE
from custom.prompts import AI_SUFFIX_LANDSCAPE, AI_SUFFIX_PORTRAIT, AI_SUFFIX_SQUARE
from custom.styles import Styles as s
from postair_pack.components.ai_mark import ai_marked

_MANAGED = Path(__file__).parent.parent / "static" / "images" / "managed"

#: Par orientation : (suffixe de prompt, taille de génération). La médiathèque
#: du 2026-08-13 porte chaque scène en 3 orientations : ``<name>.webp``
#: (paysage), ``<name>_sq.webp`` (carrée — le DÉFAUT du gabarit hero_split),
#: ``<name>_pt.webp`` (portrait, pour les colonnes hautes).
_VARIANTS = {
    None: (AI_SUFFIX_LANDSCAPE, "1536x1024"),
    "sq": (AI_SUFFIX_SQUARE, "1024x1024"),
    "pt": (AI_SUFFIX_PORTRAIT, "1024x1536"),
}


def hero_image(name: str, prompt: str, fallback: str, alt_ready: str,
               alt_fallback: str, width: str = "100%",
               variant: str | None = None) -> None:
    """Le visuel dominant : version managée si elle existe, sinon le SVG.

    ``variant`` choisit l'orientation managée (``"sq"``/``"pt"``/None) ; le
    prompt passé par le bloc est TOUJOURS le paysage — le suffixe est permuté
    ici, pour que l'éditeur régénère dans la bonne orientation sans que les
    blocs portent trois prompts.
    """
    suffix, ai_size = _VARIANTS[variant]
    full_name = f"{name}_{variant}" if variant else name
    if variant and AI_SUFFIX_LANDSCAPE in prompt:
        prompt = prompt.replace(AI_SUFFIX_LANDSCAPE, suffix)
    ready = (_MANAGED / f"{full_name}.webp").exists()
    # La pastille DD-35 découle du sidecar (source_type), jamais d'une liste :
    # une image managée générée par IA est marquée d'office, le repli SVG
    # (dessiné, versionné) ne l'est pas. fit=False : l'image remplit sa cellule.
    # En mode ÉDITEUR, st_image rend l'image PLUS la barre « Edit Image » :
    # la pastille bas-droite tomberait sous l'image, sur la barre. Elle passe
    # en HAUT-droite le temps de l'édition ; la projection fait foi (bas).
    with ai_marked(ready and is_synthetic(full_name), fit=False,
                   media_width=managed_media_width(full_name, width),
                   top=IS_EDITABLE):
        st_image(
            s.project.cards.media_center, width=width,
            uri="" if ready else fallback,
            alt=alt_ready if ready else alt_fallback,
            editable=IS_EDITABLE, name=full_name,
            prompt=prompt, provider="openai", ai_size=ai_size,
        )


def managed_media_width(full_name: str, width: str = "100%") -> str | None:
    """La largeur RÉELLEMENT affichée du média, pour ancrer la pastille.

    ``st_image`` applique le ``display_zoom`` du sidecar par rapport à son
    conteneur (``width = f"{zoom}%"``) : la pastille doit suivre le bord de
    l'image réduite, pas celui du conteneur. À défaut de réglage d'éditeur,
    c'est la largeur passée par le bloc qui fait foi ; ``None`` = le média
    remplit son conteneur, rien à décaler.
    """
    sidecar = _MANAGED / f"{full_name}.json"
    if sidecar.exists():
        try:
            meta = json.loads(sidecar.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            meta = {}
        if meta.get("display_width"):
            return str(meta["display_width"])
        zoom = meta.get("display_zoom")
        if zoom not in (None, 100):
            return f"{zoom}%"
    return None if width == "100%" else width


def is_synthetic(full_name: str) -> bool:
    """Le drapeau du sidecar de l'image managée — la donnée décide."""
    sidecar = _MANAGED / f"{full_name}.json"
    if not sidecar.exists():
        # Image managée sans sidecar : provenance inconnue — marquer est le
        # défaut sûr, l'absence de marque doit se MÉRITER par la donnée.
        return True
    try:
        meta = json.loads(sidecar.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return True
    return meta.get("source_type") == "ai_generated"
