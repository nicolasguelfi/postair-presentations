"""S1 — Join the survey: one sub-slide per conference day (QR + giant code).

Data-driven from custom/event.py (three daily sumvadis campaigns). The
presenter navigates to the sub-slide of the current day.

SPEAKER NOTES:
The critical moment — keep the slide up until the counter stabilises.
Scan the QR or type the short URL, then the 6-digit code of the day.
Anonymous, 15-20 minutes, phone OR laptop. No device? Pair up. If the
venue wifi struggles, switch to 4G.
"""
# @guideline: postair-minimal

from custom.event import DAYS, join_url
from custom.styles import Styles as s
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    day = s.project.titles.subtitle + s.center_txt
    url = s.project.ds.stage.url_big
    code = s.project.ds.stage.code_giant
    hint = s.project.body.body + s.center_txt


bs = BlockStyles


def _day_slide(label: str, code: str) -> None:
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, "Your turn — ", (s.project.titles.keyword, "join the survey"),
                         tag=t.div, toc_lvl="+1", label=f"Join — {label.split()[0]}")
                st_write(bs.day, label, tag=t.div)
            with g.cell():
                st_info_tooltip(
                    title="Anonymous by design",
                    entries=[
                        ("Your result is yours", "Your personal radar is computed ON your "
                         "device; the server only receives one anonymous record."),
                        ("GDPR", "No account, no email, no tracking; data stays in the EU. "
                         "Only room-level averages are ever projected (minimum 5 answers)."),
                        ("No device?", "Pair up with a neighbour — one answer per person "
                         "though: your posture, not a committee's."),
                        ("Network", "If the venue wifi is slow, switch your phone to 4G."),
                        ("Keep your code", "At the end the app gives you a personal code to "
                         "retrieve your result later at app.sumvadis.ai/r."),
                    ],
                )
        st_space("v", "1vh")
        with st_grid(cols="45% 55%", gap="1vw",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_image(s.project.cards.media_center, width="min(30vw, 52vh)",
                         uri=f"images/qr/qr_join_{code}.png",
                         alt=f"QR code opening the survey at app.sumvadis.ai/s/{code}")
            with g.cell():
                st_write(bs.url, "app.sumvadis.ai/s", tag=t.div, link=join_url(code),
                         no_link_decor=True)
                st_write(bs.code, code, tag=t.div)
                st_write(bs.hint, (s.project.titles.keyword, "anonymous"),
                         "  ·  15-20 min  ·  phone or laptop", tag=t.div)


def build():
    first = True
    for label, code in DAYS:
        if not first:
            st_slide_break(marker_label=f"S1 — Join ({code})",
                           config=SlideBreakConfig(mode=SlideBreakMode.MARKER_ONLY))
        else:
            st_marker(f"S1 — Join ({code})")
        _day_slide(label, code)
        first = False
