"""Joining a manifest pole to the mascot cast, and to the survey application.

The debate manifest and the mascot cast are produced by two different studios
and share no identifier — except the instrument's axis code, which the cast
carries as ``axis_code`` and every statement id carries as its prefix
(``TRU-04`` → ``TRU``). That code is the join, and reading it from the data
means no table of axis names has to be maintained here in any language.
"""

from __future__ import annotations

from postair_data import axis_by_code

from custom.content import text

#: The survey application shows the room's live distribution per axis.
PRESENT_BASE = "https://app.sumvadis.ai/present"


def axis_code(pole: dict) -> str:
    """The instrument code of a pole, read from its own statements."""
    return pole["statements"][0]["id"].split("-")[0]


def mascots(pole: dict) -> list[dict]:
    """The pole's two mascots — bestiary first, then object."""
    side = "accel" if pole["effect"] == "accelerator" else "decel"
    return [axis_by_code(axis_code(pole), family)[side]
            for family in ("animals", "objects")]


def faceoff_sides(both: list[dict], lang: str | None = None) -> list[dict]:
    """The two poles of an axis as the faceoff component expects them."""
    return [{"label": text(p["pole"], lang),
             "effect": p["effect"],
             **{k: v for k, v in mascots(p)[0].items() if k in ("mascot", "image")}}
            for p in both]


def present_url(code: str) -> str:
    return f"{PRESENT_BASE}/{code}"
