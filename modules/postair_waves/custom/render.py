"""Le moteur de rendu du deck des vagues — les compositions partagées.

Deux familles, sur le patron de ``debates/custom/render.py`` :

- ``waves_grid_slide`` — la planche de six vagues (R4c : ``grids.balanced`` +
  ``stretch``, jamais un nombre de colonnes en dur), appelée trois fois par
  des blocs de trois lignes ;
- ``wave_slides`` — les slides d'UNE vague : le quadriptyque validé (objet →
  avant → crise → recomposé, chaque image plein cadre avec sa phrase en
  bandeau et sa pastille DD-35), puis une sous-slide par figure (portrait =
  lecteur vidéo CDN, ``st_poster_video``), puis la leçon. Un seul arrêt
  visible par vague ; le reste en marqueurs cachés (régime debates,
  ``scroll_offset=0``).
"""

from __future__ import annotations

from custom.styles import Styles as s
from postair_pack.components.ai_mark import dd35_overlay
from postair_pack.components.hero_split import hero_split
from shared_widgets import st_info_tooltip, st_poster_video
from streamtex import *
from streamtex import SlideBreakConfig, SlideBreakMode
from streamtex.enums import Tags as t

from custom import content


class GridStyles:
    title = s.project.titles.slide_title + s.center_txt
    order = s.project.titles.register_title + s.project.colors.keyword + s.center_txt
    period = s.project.body.caption + s.center_txt
    name = s.project.body.pole_label_compact
    figures = s.project.body.mascot_name


gs = GridStyles


def _tooltip_entries(span: list[dict], lang: str) -> list[tuple[str, str]]:
    """Une entrée par vague : la ligne complète, substitution comprise (R4 —
    chaque slide autosuffisante, sans dépendre d'une autre)."""
    entries = []
    for w in span:
        name = content.text(w["name"], lang)
        subst = content.text(w.get("substitution"), lang)
        figures = ", ".join(f["name"] for f in w["figures"])
        detail = f"{w['period']} — figures: {figures}."
        if subst:
            detail += f" Substitution term: “{subst}”."
        else:
            detail += " The questionnaire applies verbatim (this is the studied wave)."
        entries.append((f"{w['order']} · {name}", detail))
    return entries


def waves_grid_slide(marker: str, title_parts: tuple, first: int, last: int,
                     lang: str | None = None) -> None:
    """Une planche de six vagues (numéro / période / nom / figures).

    ``title_parts`` = (avant, mot-clé teal, après) — exactement un accent par
    titre (R3). Les cellules restent télégraphiques : le NUMÉRO porte le seul
    accent teal de la cellule, les figures vivent en légende, et la phrase
    complète (substitution comprise) vit dans l'infobulle du titre.
    """
    lang = lang or content.default_language()
    span = content.wave_span(first, last)
    st_marker(marker)
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                before, keyword, after = title_parts
                st_write(gs.title, before, (s.project.titles.keyword, keyword),
                         after, tag=t.div, toc_lvl="+1", label=marker)
            with g.cell():
                st_info_tooltip(title=f"{marker} — the full lines",
                                entries=_tooltip_entries(span, lang))
        st_space("v", s.project.spacing.title_gap)
        with st_grid(cols=s.project.grids.balanced(len(span)), gap="1.2vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_top) as g:
            for w in span:
                with g.cell(), st_block(s.project.cards.blue):
                    st_write(gs.order, str(w["order"]), tag=t.div)
                    st_write(gs.period, w["period"], tag=t.div)
                    st_write(gs.name, content.text(w["name"], lang), tag=t.div)
                    st_write(gs.figures,
                             " · ".join(f["name"] for f in w["figures"]),
                             tag=t.div)


# ── Le quadriptyque d'une vague ─────────────────────────────────────────────

class StageStyles:
    overline = s.project.body.caption + s.center_txt
    etage = s.project.titles.register_title + s.project.colors.keyword + s.center_txt
    title = s.project.titles.slide_title + s.center_txt
    phrase = s.project.body.bullet + s.center_txt
    name = s.project.body.name_double
    meta = s.project.body.caption + s.center_txt
    line = s.project.body.body + s.center_txt
    card_title = s.project.body.pole_label_accel_compact
    card_text = s.project.body.mascot_name


ss = StageStyles

#: Bornée pour que image + bandeaux tiennent SANS scroll : hauteur d'image
#: ≈ 72vh (16:9), unités de fenêtre — jamais de %, le zoom y est inerte
#: (règle R-zoom).
_STAGE_WIDTH = "min(96%, 128vh)"

_HIDDEN = dict(marker_hidden=True,
               config=SlideBreakConfig(mode=SlideBreakMode.FULL, space="30vh"))


def _stage(w: dict, etage: str, lang: str, first: bool) -> None:
    """Un étage du quadriptyque : l'image validée plein cadre + sa phrase.

    Les 68 images sont GÉNÉRÉES PAR IA (série validée les 25-26/08/2026,
    manifeste ``_project/reviews/260826-serie-complete/``) : la pastille DD-35
    est posée par ``overlay=`` — superposition, jamais incrustée, le drapeau
    de données décide.
    """
    name = content.text(w["name"], lang)
    with st_block(s.project.containers.page_fill_full):
        st_write(ss.overline, f"{w['order']} · {name} · {w['period']}", tag=t.div)
        if first:
            # La carte-titre de la vague : son entrée TOC de niveau 1.
            st_write(ss.etage, content.etage_label(etage, lang), tag=t.div,
                     toc_lvl="1", label=name)
        else:
            st_write(ss.etage, content.etage_label(etage, lang), tag=t.div)
        st_image(s.project.cards.media_center, width=_STAGE_WIDTH,
                 uri=content.image_uri(w["id"], etage),
                 alt=f"{content.etage_label(etage, 'en')} — {name} "
                     f"({w['period']}): AI-generated historical reconstruction",
                 overlay=dd35_overlay(True))
        st_write(ss.phrase, content.phrase(w["id"], etage, lang), tag=t.div)


def _figure(w: dict, f: dict, lang: str) -> None:
    """Une figure de la vague — le portrait EST le lecteur (patron debates).

    La vidéo reste au CDN (``preload="none"`` : rien n'est téléchargé tant que
    l'orateur ne joue pas). Une figure sans portrait+vidéo ``public-ok``
    (gandhi, hawking) est présentée en nom seul — jamais de trou projeté.
    """
    media = f.get("media")
    meta = " · ".join(x for x in (f.get("dates"), f.get("origin"),
                                  f.get("stance")) if x)

    def _portrait():
        st_poster_video(
            media["video"], f"app/static/media/{media['portrait']}",
            alt=f"Presentation video of {f['name']}",
            width="min(38vw, 66vh)",
            ai_marked=bool(media.get("video_ai")))

    if media:
        with hero_split(s, image=_portrait, ratio=46):
            st_write(ss.name, f["name"], tag=t.div, toc_lvl="+1",
                     label=f["name"])
            st_write(ss.meta, meta, tag=t.div)
            st_write(ss.line, "a witness of ",
                     (s.project.colors.keyword, content.text(w["name"], lang)),
                     tag=t.div)
            st_write(ss.meta, "press play — the video streams from the CDN; "
                              "the full debates live in the Debates deck",
                     tag=t.div)
    else:
        with st_block(s.project.containers.page_fill_center):
            st_write(ss.name, f["name"], tag=t.div, toc_lvl="+1",
                     label=f["name"])
            st_write(ss.meta, meta, tag=t.div)
            st_write(ss.line, "a witness of ",
                     (s.project.colors.keyword, content.text(w["name"], lang)),
                     tag=t.div)
            st_write(ss.meta, "portrait and video pending at the hub",
                     tag=t.div)


def _lesson(w: dict, lang: str) -> None:
    """La leçon de la vague — PLACEHOLDER rubriqué (conception L1 validée).

    Phase 1 : trois rubriques dérivées des phrases validées + le pont de
    substitution. Phase 2 (campagne hub) : l'objet ``ai_lesson`` trilingue,
    sourcé, avec le miroir de citations hier/aujourd'hui — gelé par l'outil.
    """
    name = content.text(w["name"], lang)
    subst = content.text(w.get("substitution"), lang)
    if w["id"] == "ai":
        echo = ("The crisis is open and YOUR posture is the data — "
                "the live survey measures it next.")
    else:
        echo = (f"This study asks AI the questions once asked of {subst} — "
                f"same items, same axes, twenty-five centuries apart.")
    cards = [
        ("What was feared", content.phrase(w["id"], "crise", lang)),
        ("What came of it", content.phrase(w["id"], "recompose", lang)),
        ("The echo for AI", echo),
    ]
    with st_block(s.project.containers.page_fill_top):
        st_write(ss.title, "What ", (s.project.titles.keyword, name),
                 " teaches us", tag=t.div, toc_lvl="+1", label="The lesson")
        st_space("v", s.project.spacing.title_gap)
        with st_grid(cols=s.project.grids.balanced(len(cards)), gap="1.5vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_top) as g:
            for title, body in cards:
                with g.cell(), st_block(s.project.cards.blue):
                    st_write(ss.card_title, title, tag=t.div)
                    st_write(ss.card_text, body, tag=t.div)


def wave_slides(wave_id: str, lang: str | None = None) -> None:
    """Toutes les slides d'une vague — UN arrêt visible, le reste caché.

    Ordre : la carte-titre (l'OBJET de la révolution), puis le récit
    (avant → crise → recomposé), puis les figures au portrait-lecteur,
    puis la leçon. Les flèches traversent tout ; la barre latérale ne
    liste que la vague.
    """
    lang = lang or content.default_language()
    w = content.wave(wave_id)
    st_marker(content.text(w["name"], lang))
    _stage(w, "objet", lang, first=True)
    for etage in ("avant", "crise", "recompose"):
        st_slide_break(**_HIDDEN)
        _stage(w, etage, lang, first=False)
    for f in w["figures"]:
        st_slide_break(**_HIDDEN)
        _figure(w, f, lang)
    st_slide_break(**_HIDDEN)
    _lesson(w, lang)
