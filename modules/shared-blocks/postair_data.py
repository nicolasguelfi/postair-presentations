"""POSTAIR mascot / axis data access.

Single source of truth: ``static/_SHARED/mascots/cast_final.json`` (frozen
manifest of the mascoties studio). This module exposes the 9 axes grouped by
register, with the accelerator pole FIRST (left column) — the sumvadis
display convention requested for the register slides.

The accelerator side per axis comes from the ``effect`` field of the POSTAIR
questionnaire (sumvadis ``packages/core/assets/postair/questionnaire.json``):
axes 6 (control) and 8 (altruism) have their accelerator pole on the LEFT
side of the instrument; all other axes have it on the RIGHT.
"""

import json
from functools import lru_cache
from pathlib import Path

_MASCOTS_DIR = Path(__file__).parent / "static" / "_SHARED" / "mascots"

# Instrument side ("left"/"right") of the ACCELERATOR pole, per axis number.
ACCEL_SIDE = {1: "right", 2: "right", 3: "right", 4: "right", 5: "right",
              6: "left", 7: "right", 8: "left", 9: "right"}

# Registers (category_en of cast_final.json) with EN subtitles.
REGISTERS = [
    ("Knowing", "how I judge / whom I trust", [1, 2, 3]),
    ("Acting", "how fast / under which rules I deploy", [4, 5, 6]),
    ("Becoming", "which social order · which human condition", [7, 8, 9]),
]


@lru_cache(maxsize=1)
def _cast_items() -> list[dict]:
    data = json.loads((_MASCOTS_DIR / "cast_final.json").read_text(encoding="utf-8"))
    items = data["items"]
    return list(items.values()) if isinstance(items, dict) else items


def _webp_uri(item: dict) -> str:
    """L'URI d'une mascotte, relative à la base d'images du module.

    Elle DOIT rester introuvable sur le disque via les sources statiques :
    ``st_image`` encode en base64 tout fichier qu'il trouve, et la planche des
    36 mascottes pèserait alors 2,1 Mo de base64 dans la page, renvoyés à chaque
    rerun. Introuvable, l'URI retombe sur ``configure_image_path`` et sort en URL
    relative — quelques dizaines d'octets, servie par le conteneur lui-même.

    Les octets vivent dans ``<module>/static/media/mascots/``, matérialisés
    depuis le catalogue du studio par ``_project/tools/sync_media.py``.

    Une seule règle pour tout le monde depuis le 2026-08-03 : le catalogue publie
    tout en WebP. Les deux modérateurs faisaient exception — ils n'étaient pas au
    CDN et étaient copiés du studio en png — jusqu'à la section ``crew`` du
    catalogue v2.2.0, qui les publie comme les autres, signés C2PA.
    """
    return "mascots/" + item["files"]["rgb"].replace(".png", ".webp")


def mascot_clip(name: str, lang: str = "en") -> str:
    """L'URI du clip « Postures » d'une mascotte, relative au dossier des médias.

    Les 72 clips (36 mascottes × 2 langues) sont publiés par le dépôt
    ``commercials``, déclarés dans le catalogue du studio et matérialisés par
    ``_project/tools/sync_media.py`` sous ``<module>/static/media/clips/``.

    Le nom local est dérivé de la clé d'axe, jamais du nom content-adressé du
    CDN : celui-ci change à chaque republication, et un deck qui le porterait
    en dur deviendrait faux en silence.

    Les deux modérateurs n'ont pas de clip — ils n'ont pas d'axe, et la série
    « Postures » est construite axe par axe.
    """
    for item in _cast_items():
        if item.get("name") != name:
            continue
        if item.get("axis") is None:
            raise KeyError(f"{name} has no axis, and the Postures series has no clip for it")
        return f"clips/{item['files']['rgb'].rsplit('.', 1)[0]}-{lang}.mp4"
    raise KeyError(f"no mascot named {name!r} in the frozen cast manifest")


@lru_cache(maxsize=4)
def axes(family_en: str = "animals") -> dict[int, dict]:
    """Return {axis_num: axis info} for one mascot family.

    Each axis dict: ``axis_code``, ``axis_name``, ``category_en`` and two
    pole dicts ``accel`` / ``decel`` with ``label`` (EN, capitalised),
    ``mascot`` (name), ``image`` (static uri), ``description`` (FR tagline).
    """
    result: dict[int, dict] = {}
    for item in _cast_items():
        if item.get("family_en") != family_en or "axis" not in item:
            continue
        n = item["axis"]
        ax = result.setdefault(n, {
            "axis": n,
            "axis_code": item["axis_code"],
            "axis_name": item["axis_name"],
            "category_en": item.get("category_en", ""),
        })
        pole = {
            "label": item["pole_label_en"].replace("-", " ").capitalize(),
            "mascot": item["name"],
            "image": _webp_uri(item),
            "description": item.get("description", ""),
        }
        ax["accel" if item["side"] == ACCEL_SIDE[n] else "decel"] = pole
    return result


@lru_cache(maxsize=8)
def axis_by_code(code: str, family_en: str = "animals") -> dict:
    """One axis by its instrument code (``TRU``, ``SPE``, ``CEN``…).

    The code is the join key between the questionnaire and the mascot cast:
    a statement id such as ``TRU-04`` carries it, so a consumer holding survey
    data can reach the mascots without knowing an axis number or an axis name
    in any particular language.
    """
    for axis in axes(family_en).values():
        if axis["axis_code"] == code:
            return axis
    raise KeyError(f"no axis with instrument code {code!r} in the frozen cast manifest")


@lru_cache(maxsize=4)
def archetypes(lang: str = "en") -> list[tuple[str, str]]:
    """The six POSTAIR archetypes as ``(key, name)``, in the published order.

    Names come from the shared ``i18n.json`` of the mascot studio — the same
    file the survey application reads, so a rename propagates everywhere at
    once. The file carries names only: the archetype *descriptions* live in
    the study and are deliberately not duplicated here.
    """
    data = json.loads((_MASCOTS_DIR / "i18n.json").read_text(encoding="utf-8"))
    return [(key, names[lang]) for key, names in data["archetypes"].items()]


@lru_cache(maxsize=64)
def mascot(name: str) -> dict:
    """One mascot by its name — including the two moderators, which carry no axis.

    Returns ``name``, ``image`` (static uri), ``description`` (FR tagline),
    ``pole`` (EN pole label, empty for a moderator) and ``axis_name``. Blocks
    that need a single mascot ask for it by name rather than by position, so
    the call stays true when the cast is reordered.
    """
    for item in _cast_items():
        if item.get("name") == name:
            return {
                "name": item["name"],
                "image": _webp_uri(item),
                "description": item.get("description", ""),
                "pole": (item.get("pole_label_en") or "").replace("-", " ").capitalize(),
                "axis_name": item.get("axis_name") or "",
            }
    raise KeyError(f"no mascot named {name!r} in the frozen cast manifest")


def register_axes(register_name: str, family_en: str = "animals") -> list[dict]:
    """Axes of one register (by EN name), in pedagogical order."""
    nums = next(nums for name, _sub, nums in REGISTERS if name == register_name)
    data = axes(family_en)
    return [data[n] for n in nums]
