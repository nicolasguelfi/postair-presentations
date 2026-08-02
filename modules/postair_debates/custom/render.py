"""The seven sub-slides of one axis, rendered from the manifest.

Every axis block is the same code with a different axis id: three sub-slides
for the accelerating pole, three for the decelerating one, then the two face to
face. Writing it once means a change of gabarit reaches all nine axes at the
same instant, and that no axis can quietly drift from the others.

Navigation follows the speaker, not the templates: a visible marker per pole
and one for the face-off — three stops in the marker list — while every
sub-slide still breaks so PageDown advances one screen at a time.
"""

from __future__ import annotations

from postair_pack.components.argument_card import argument_card
from postair_pack.components.figure_card import figure_card
from postair_pack.components.pole_faceoff import pole_faceoff
from postair_pack.components.pole_identity import pole_identity
from shared_widgets import st_info_tooltip
from streamtex import (
    SlideBreakConfig,
    SlideBreakMode,
    st_block,
    st_grid,
    st_marker,
    st_slide_break,
    st_space,
    st_write,
)
from streamtex.enums import Tags as t

from custom.content import axis_poles, text, warnings_for
from custom.pole import faceoff_sides, mascots
from custom.styles import DS
from custom.styles import Styles as s


class RenderStyles:
    title = s.project.titles.slide_title + s.center_txt
    subtitle = s.project.titles.subtitle + s.center_txt
    banner = s.project.body.body + s.center_txt


rs = RenderStyles

#: What each pole does to the diffusion of the technology. Neutral wording:
#: neither side of an axis is the good one, and the badge must not suggest it.
_EFFECT = {"accelerator": "accelerates adoption",
           "decelerator": "slows adoption down"}


def _header(title_parts, tooltip_title, entries, label=None, toc_lvl="+1") -> None:
    with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
        with g.cell():
            st_write(rs.title, *title_parts, tag=t.div, toc_lvl=toc_lvl, label=label)
        with g.cell():
            st_info_tooltip(title=tooltip_title, entries=entries)


def _identity(pole: dict, lang: str | None) -> None:
    pole_name = text(pole["pole"], lang)
    entries = [("What this pole claims",
                f"{pole_name} — the posture that {_EFFECT[pole['effect']]} on the "
                f"{text(pole['axis_name'], lang)} axis. It is a legitimate position, held and "
                f"argued by people whose names are in the history of technology.")]
    for st_item in pole["statements"]:
        guidance = st_item.get("guidance") or {}
        parts = [text(guidance.get("clarification"), lang),
                 text(guidance.get("anchor_low"), lang),
                 text(guidance.get("anchor_high"), lang)]
        for example in (guidance.get("examples") or [])[:1]:
            parts.append(text(example, lang))
        entries.append((text(st_item["text"], lang), " ".join(p for p in parts if p)))
    both = mascots(pole)
    entries.append(("Mascots",
                    " · ".join(f"{m['mascot']}: {m.get('description') or m['label']}"
                               for m in both)))
    _header([pole_name], f"{text(pole['axis_name'], lang)} — {pole_name}", entries,
            label=pole_name, toc_lvl="1")
    st_write(rs.subtitle,
             f"{text(pole['axis_name'], lang)} · {_EFFECT[pole['effect']]}", tag=t.div)
    st_space("v", "1.5vh")
    pole_identity(both, [text(x["text"], lang) for x in pole["statements"]], DS)


def _figures(pole: dict, lang: str | None) -> None:
    pole_name = text(pole["pole"], lang)
    entries = []
    for f in pole["figures"]:
        entries.append((f"{f['name']} ({f.get('dates', '')})",
                        f"{f.get('origin', '')} · {f.get('wave', '')} · score {f['score']} on "
                        f"this axis. The profile is a reconstruction from primary sources: it "
                        f"commits its author, never the figure."))
    entries.append(("Videos", "Clicking a portrait opens the figure's presentation video. For "
                              "the living people of this study the video presents them — the "
                              "corpus never makes a living person speak through generative AI."))
    entries.append(("References", "Every quotation is verbatim and verified. Where a reference "
                                  "is still being established, the card says so rather than "
                                  "looking sourced. The cards carry the caption form; the "
                                  "complete references follow."))
    # The full reference belongs here, not under the portrait: a dossier's
    # source entry is written to be complete, not to be read from row thirty.
    for f in pole["figures"]:
        full = f["quote"].get("reference_full")
        if full and full != f["quote"].get("reference"):
            entries.append((f"{f['name']} — full reference", full))
    _header(["Who thought this ", (s.project.titles.keyword, "before us"), " — ", pole_name],
            f"The three figures of {pole_name}", entries)
    for warning in warnings_for(pole["axis"]):
        if pole["pole"].get("abbr", {}).get("en", "") in warning:
            st_space("v", "1vh")
            with st_block(s.project.cards.amber):
                st_write(rs.banner,
                         "No figure in this study champions this pole. These are the three "
                         "closest to it — the strongest voices this corpus has to offer on "
                         "this side, and that absence is itself worth debating.", tag=t.div)
    st_space("v", "1.5vh")
    with st_grid(cols=s.project.grids.balanced(len(pole["figures"])), gap="1.2vw",
                 grid_style=s.project.grids.stretch,
                 cell_styles=s.project.containers.grid_cell_top) as g:
        for f in pole["figures"]:
            with g.cell():
                figure_card(f, DS, text(f["quote"], lang) or f["quote"].get("en") or "",
                            f["quote"].get("reference"))


def _arguments(pole: dict, lang: str | None) -> None:
    pole_name = text(pole["pole"], lang)
    entries = [(text(a["title"], lang), text(a.get("text"), lang) or "")
               for a in pole["arguments"]]
    entries.append(("Symmetry", "The opposite pole has its own three arguments, of the same "
                                "three natures. Never open this slide without the other one — "
                                "the room must hear both best cases."))
    entries.append(("Paraphrase or verbatim", "A card carrying a quotation gives it verbatim; "
                                              "the others are documented paraphrases of a "
                                              "sourced position."))
    _header(["And ", (s.project.titles.keyword, "today"), "? — ", pole_name],
            f"Contemporary arguments for {pole_name}", entries)
    st_space("v", "1.5vh")
    with st_grid(cols=s.project.grids.balanced(len(pole["arguments"])), gap="1.2vw",
                 grid_style=s.project.grids.stretch,
                 cell_styles=s.project.containers.grid_cell_top) as g:
        for a in pole["arguments"]:
            with g.cell():
                argument_card(a, DS, text(a["title"], lang))


def _faceoff(both: list[dict], lang: str | None) -> None:
    left, right = (text(p["pole"], lang) for p in both)
    entries = [
        ("Where is this room?", "The live distribution is in the survey application, on the "
                                "results page of the day. It cannot be drawn here: it changes "
                                "while you speak."),
        ("Reading a distribution", "Averages hide diversity. An axis at fifty can be a room of "
                                   "moderates or two opposed halves — look at the shape, not the "
                                   "number."),
        ("Posture codes", "Directional: clearly on one pole. Ambivalent: agrees with BOTH poles, "
                          "which is not indecision but a held tension. Balanced: deliberately in "
                          "between. Detached: the question does not mobilise."),
        ("Three moves", "Show of hands — who is on which side. Then one argument from each "
                        "bench. Then what the measurement actually says."),
    ]
    _header([left, " ⇄ ", right], f"{left} ⇄ {right}", entries, label=f"{left} ⇄ {right}")
    st_space("v", "2vh")
    pole_faceoff(faceoff_sides(both, lang), DS)


def axis_slides(axis: str, lang: str | None = None) -> None:
    """The seven sub-slides of one axis, accelerator pole first."""
    both = axis_poles(axis)
    first = True
    for pole in both:
        pole_name = text(pole["pole"], lang)
        for part in (_identity, _figures, _arguments):
            if first:
                st_marker(pole_name)
                first = False
            elif part is _identity:
                st_slide_break(marker_label=pole_name)
            else:
                st_slide_break(marker_hidden=True,
                               config=SlideBreakConfig(mode=SlideBreakMode.FULL, space="30vh"))
            with st_block(s.project.containers.page_fill_top):
                part(pole, lang)
    st_slide_break(marker_label=" ⇄ ".join(text(p["pole"], lang) for p in both))
    with st_block(s.project.containers.page_fill_top):
        _faceoff(both, lang)
