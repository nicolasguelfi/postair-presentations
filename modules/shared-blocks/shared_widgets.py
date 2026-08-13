"""Shared widgets for the POSTAIR presentations.

Palette wrappers and the one widget that genuinely needs markup — the tooltip
itself is the native ``st_hover_tooltip`` from streamtex (>= 0.7.8). Blocks
never write markup themselves (design guideline, rule "stx-only"): when a
slide needs behaviour the style system cannot express, it comes from here.
"""

import streamlit as st
from streamtex import st_hover_tooltip, st_html

from postair_pack.design_systems.postair_dark import (
    TOOLTIP_BG,
    TOOLTIP_DEF_CSS,
    TOOLTIP_MAX_HEIGHT,
    TOOLTIP_SCALE,
    TOOLTIP_TERM_CSS,
    TOOLTIP_TITLE_CSS,
    TOOLTIP_WIDTH,
)


def st_stage_selector(options: list[str], key: str, label: str = "") -> str:
    """A one-line chooser the SPEAKER drives, on a slide the room reads.

    The only interactive control of these decks. It exists for one reason: a
    slide that must show something different depending on the day, without the
    other days being visible or reachable — three sub-slides put the three
    codes one arrow-key apart, and a room that sees a code it should not use is
    a room that can pollute another day's campaign.

    Blocks never touch Streamlit directly (design guideline, rule "stx-only"):
    when a slide needs behaviour the style system cannot express, it comes from
    here. The key is passed in and must be a STABLE string — a generated one
    would change at every rerun and reset the choice under the speaker's hand.
    """
    return st.selectbox(label or " ", options, index=0, key=key,
                        label_visibility="collapsed")


def st_info_tooltip(title: str, entries: list[tuple[str, str]], **kw):
    """Info tooltip with the POSTAIR palette and auditorium geometry pre-applied.

    Convention (design guideline, rule "Tooltip"): placed after the slide
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


def st_countdown(minutes: int, label: str = "Back in", height: int = 340) -> None:
    """A live break countdown, readable from the back of an amphitheatre.

    The clock starts when the slide is displayed, not when the deck is built:
    the presenter reaches the break when they reach it, and a break screen
    that already expired would be worse than none. It also prints the wall
    time the room is expected back, because that is what people actually act
    on once they are in the corridor.

    Rendered through ``st_html`` — the single markup bridge — with an explicit
    height, since a script needs the iframe to run. Sizes are in ``vw`` of the
    iframe, so the digits follow the projection width.
    """
    html = f"""
<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
            height:100%;font-family:'Source Sans Pro',sans-serif;color:#F2EEE6;">
  <div style="font-size:3.2vw;color:#7AB8F5;font-weight:700;">{label}</div>
  <div id="stx-countdown"
       style="font-size:14vw;font-weight:900;letter-spacing:0.04em;line-height:1;
              color:#F39C12;">--:--</div>
  <div id="stx-countdown-at" style="font-size:2.6vw;color:#95A5A6;"></div>
</div>
<script>
(function () {{
  var end = Date.now() + {minutes} * 60 * 1000;
  var out = document.getElementById('stx-countdown');
  var at = document.getElementById('stx-countdown-at');
  var back = new Date(end);
  at.textContent = 'we resume at ' +
    String(back.getHours()).padStart(2, '0') + ':' +
    String(back.getMinutes()).padStart(2, '0');
  function tick() {{
    var left = Math.max(0, end - Date.now());
    var m = Math.floor(left / 60000), s = Math.floor(left / 1000) % 60;
    out.textContent = String(m).padStart(2, '0') + ':' + String(s).padStart(2, '0');
    if (left === 0) {{ out.style.color = '#E07A6E'; clearInterval(timer); }}
  }}
  var timer = setInterval(tick, 1000);
  tick();
}})();
</script>
"""
    st_html(html, height=height)
