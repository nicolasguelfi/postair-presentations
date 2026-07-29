"""Shared widgets for the POSTAIR presentations.

Only palette wrappers live here — the tooltip itself is the native
``st_hover_tooltip`` from streamtex (>= 0.7.8).
"""

from postair_pack.design_systems.postair_dark import (
    TOOLTIP_BG,
    TOOLTIP_DEF_CSS,
    TOOLTIP_MAX_HEIGHT,
    TOOLTIP_SCALE,
    TOOLTIP_TERM_CSS,
    TOOLTIP_TITLE_CSS,
    TOOLTIP_WIDTH,
)
from streamtex import st_hover_tooltip


def st_info_tooltip(title: str, entries: list[tuple[str, str]], **kw):
    """Info tooltip with the POSTAIR palette and auditorium geometry pre-applied.

    Convention (design guideline R4): placed immediately after the slide
    title, in the narrow right-hand cell of a ``92% 8%`` grid; opens
    downward, panel on the left side. Geometry and font unit come from the
    design system (2/3 viewport panel, large base font) — override per call
    only when a slide really needs it.
    """
    kw.setdefault("bg_color", TOOLTIP_BG)
    kw.setdefault("title_style", TOOLTIP_TITLE_CSS)
    kw.setdefault("term_style", TOOLTIP_TERM_CSS)
    kw.setdefault("def_style", TOOLTIP_DEF_CSS)
    kw.setdefault("width", TOOLTIP_WIDTH)
    kw.setdefault("max_height", TOOLTIP_MAX_HEIGHT)
    kw.setdefault("position", "left")
    kw.setdefault("scale", TOOLTIP_SCALE)
    return st_hover_tooltip(icon="ℹ️", title=title, entries=entries, **kw)
