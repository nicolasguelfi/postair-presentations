"""Gabarit « une faculté par slide » — la série AI concerns the whole University.

Découpage NG (2026-08-13, 1 idée = 1 slide) : l'ancienne slide posait trois
cartes de phrases, toutes tronquées au pli. Chaque faculté a maintenant SA
slide : l'image papier découpé carrée à gauche, et à droite les constats
télégraphiques avec leurs codes de citation. La réserve d'honnêteté (aucune
mesure par faculté à l'UL) reste EN CLAIR sur chaque slide de la série.

Un gabarit, trois blocs minces — le pattern ``limit_slide`` de postair_genai.
"""

from __future__ import annotations

from shared_widgets import st_info_tooltip
from streamtex import st_block, st_grid, st_marker, st_space, st_write
from streamtex.enums import Tags as t

from custom.facts import disciplines, no_faculty_data, text
from custom.prompts import AI_PREFIX, AI_SUFFIX_LANDSCAPE
from custom.refs import citation
from custom.styles import Styles as s
from custom.visuals import hero_image
from postair_pack.components.hero_split import hero_split


class SlideStyles:
    title = s.project.titles.slide_title + s.center_txt
    headline = s.project.body.bullet + s.center_txt
    reserve = s.project.body.caption + s.project.colors.amber + s.center_txt


ss = SlideStyles

#: Par faculté (ordre des données) : marqueur, image managée, scène papercut.
_VISUALS = [
    ("FSTM", "faculty_fstm",
     "A papercut science and technology scene: a large paper laptop showing "
     "cut-out code blocks, a paper flask and a small paper gear beside it, a "
     "glowing warm amber paper orb hovering over the desk; one abstract paper "
     "silhouette seen from behind."),
    ("FDEF", "faculty_fdef",
     "A papercut law and finance scene: a paper courthouse column, a paper "
     "balance scale, a small stack of paper coins and a paper contract sheet "
     "with abstract cut-out lines, a glowing warm amber paper orb hovering "
     "above; one abstract paper silhouette seen from behind."),
    ("FHSE", "faculty_fhse",
     "A papercut humanities scene: a pile of colourful paper books, a paper "
     "quill, speech bubbles cut from bright cardstock rising like a "
     "conversation, a glowing warm amber paper orb among them; one abstract "
     "paper silhouette seen from behind."),
]


def _headline(example) -> str:
    keys = (example.get("source") or {}).get("citekeys")
    if not keys:
        return text(example["headline"])
    return text(example["headline"]) + " " + citation(*keys)


def build_faculty(index: int) -> None:
    """One faculty, one papercut scene, its findings in keywords."""
    group = disciplines()[index]
    marker, name, scene = _VISUALS[index]
    prompt = AI_PREFIX + scene + AI_SUFFIX_LANDSCAPE
    st_marker(marker)
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                # Le sigle en titre (une ligne) — le nom complet de la
                # faculté vit dans le titre du tooltip.
                st_write(ss.title, "AI in ",
                         (s.project.titles.keyword, marker),
                         tag=t.div, toc_lvl="+1", label=marker)
            with g.cell():
                entries = []
                for example in group["examples"]:
                    parts = [text(example)]
                    if example.get("caveat"):
                        parts.append(text(example["caveat"]))
                    if (example.get("source") or {}).get("kind") == "reported-in":
                        parts.append("Reported inside the source cited on the "
                                     "card, not read at the original.")
                    entries.append((text(example["headline"]), " ".join(parts)))
                entries.append(("No figures for this university",
                                text(no_faculty_data())))
                st_info_tooltip(title=f"{text(group['faculty'])} — the evidence",
                                entries=entries)
        st_space("v", "1vh")
        with hero_split(s, image=lambda: hero_image(
                name, prompt, "images/postair_radar_question.svg",
                alt_ready=f"Papercut scene for {marker}",
                alt_fallback=f"Papercut scene for {marker}",
                variant="sq")):
            for example in group["examples"]:
                st_write(ss.headline, "▸ ", _headline(example), tag=t.div)
            st_space("v", "0.5vh")
            st_write(ss.reserve, text(no_faculty_data()["headline"]), tag=t.div)
