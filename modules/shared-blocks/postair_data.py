"""POSTAIR mascot / axis data access.

Single source of truth: ``static/_SHARED/mascots/cast_final.json`` (frozen
manifest of the mascoties studio). This module exposes the 9 axes grouped by
register, with the accelerator pole FIRST (left column) — the sumvadis
display convention requested for the register slides (W05b-d).

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
    ("Becoming", "which social order / which human condition results", [7, 8, 9]),
]


@lru_cache(maxsize=1)
def _cast_items() -> list[dict]:
    data = json.loads((_MASCOTS_DIR / "cast_final.json").read_text(encoding="utf-8"))
    items = data["items"]
    return list(items.values()) if isinstance(items, dict) else items


def _webp_uri(item: dict) -> str:
    return "_SHARED/mascots/web/" + item["files"]["rgb"].replace(".png", ".webp")


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


def register_axes(register_name: str, family_en: str = "animals") -> list[dict]:
    """Axes of one register (by EN name), in pedagogical order."""
    nums = next(nums for name, _sub, nums in REGISTERS if name == register_name)
    data = axes(family_en)
    return [data[n] for n in nums]
