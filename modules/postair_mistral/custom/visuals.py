"""Le visuel dominant d'une slide — image IA managée, avec repli SVG versionné.

Règle NG (2026-08-11) : dans un amphithéâtre, une image bien conçue vaut mille
mots — chaque slide se construit autour d'un visuel dominant, le texte porte le
minimum. Pattern repris de la roue de ``postair_survey/bck_axes_radar`` :

- ``uri`` est le REPLI, pas la source : dès qu'une version managée de l'image
  existe (générée par l'auteur via l'éditeur, versionnée sous
  ``static/images/managed/``), ``st_image`` la préfère et le SVG n'est plus lu ;
- une slide sans image n'est pas une étape intermédiaire acceptable — c'est un
  trou devant l'amphithéâtre : chaque visuel a donc son repli SVG, versionné
  (exception assumée du dépôt : les illustrations de ces présentations restent
  en git et ne vont jamais au CDN).

Divergence locale assumée (revue genaipat 2026-09-01) : ce fichier ajoute
``image_ratio`` et ``staged_hero_image`` (règle R4d, leçon debates 56fdcc1 —
le média se borne par SA CELLULE et par la hauteur, largeur =
``min(100 % de la cellule, stage_vh × ratio du fichier)``, débordement
impossible par construction). La copie partagée entre modules redeviendra une
seule vérité au geste de capitalisation post-AI Day (plan-capitalisation P5).
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from streamtex import st_block, st_image

from custom.config import IS_EDITABLE
from custom.prompts import AI_SUFFIX_LANDSCAPE, AI_SUFFIX_PORTRAIT, AI_SUFFIX_SQUARE
from custom.styles import Styles as s
from postair_pack.components.ai_mark import dd35_overlay

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
    # (dessiné, versionné) ne l'est pas. Le slot natif (0.7.23) la rend DANS
    # la boîte de l'image — zoom d'éditeur suivi, barre « Edit Image » exclue.
    st_image(
        s.project.cards.media_center, width=width,
        uri="" if ready else fallback,
        alt=alt_ready if ready else alt_fallback,
        editable=IS_EDITABLE, name=full_name,
        prompt=prompt, provider="openai", ai_size=ai_size,
        overlay=dd35_overlay(ready and is_synthetic(full_name)),
    )


@lru_cache(maxsize=32)
def image_ratio(full_name: str, default: float = 1.0) -> float:
    """Largeur / hauteur du FICHIER managé — une propriété du média (R4d).

    Repris de ``postair_debates/custom/render.py::_mascot_ratio`` (copie
    locale, promotion pack post-AI Day) : Pillow lit l'image matérialisée,
    le résultat est mémoïsé, et tout échec (Pillow absent, image pas encore
    générée — le repli SVG est carré d'intention) retombe sur ``default``
    sans jamais lever en séance.
    """
    path = _MANAGED / f"{full_name}.webp"
    try:
        from PIL import Image
        with Image.open(path) as im:
            width, height = im.size
        return (width / height) if height else default
    except Exception:
        return default


def staged_hero_image(name: str, prompt: str, fallback: str, alt_ready: str,
                      alt_fallback: str, width: str = "100%",
                      variant: str | None = None, stage_vh: int = 70) -> None:
    """``hero_image`` bornée par sa cellule ET par la hauteur (règle R4d).

    Leçon debates 56fdcc1 (mesurée au DOM) : une image servie à 100 % de sa
    cellule n'est bornée que par la LARGEUR — un fichier carré passe sous le
    contenu voisin. Ici largeur = ``min(stage_vh × ratio du fichier,
    100 % de la cellule)`` : le débordement vertical est impossible par
    construction. ``stage_vh`` est LE levier de taille d'un média (R-zoom :
    un ``st_zoom`` englobant est inerte sur les largeurs en %) — il se règle
    par slide, via le ``TUNING`` du bloc quand il quitte le défaut.
    """
    full_name = f"{name}_{variant}" if variant else name
    with st_block(s.project.containers.media_stage(image_ratio(full_name), stage_vh)):
        hero_image(name, prompt, fallback, alt_ready, alt_fallback,
                   width=width, variant=variant)


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
