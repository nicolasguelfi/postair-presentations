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

import streamlit as st

from custom.styles import Styles as s
from postair_pack.components.ai_mark import DD35_CSS, dd35_overlay
from postair_pack.components.hero_split import hero_split
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex import SlideBreakConfig, SlideBreakMode
from streamtex.enums import Tags as t

from custom import content

#: Page du PREMIER bloc de vague dans la liste de ``book.py`` (0-based) —
#: MIROIR de l'ordre du book (titre, 2 intros, 5 grilles → la vague d'ordre k
#: vit page ``_WAVE_PAGE_FIRST + k - 1``). Les boutons des grilles naviguent
#: par le mécanisme NATIF du runtime paginé (``href="#stx-goto-<page>"``,
#: classe ``stx-page-link`` — celui du TOC). Changer l'ordre du book = mettre
#: cette constante à jour, comme ``FIGURE_VIDEO_MODULES`` dans sync_media.
_WAVE_PAGE_FIRST = 8

#: Page de la PREMIÈRE planche-galerie (« From writing to the press ») —
#: même miroir de l'ordre du book : titre (0), 2 intros (1-2), galerie (3).
#: Cible du retour : clic sur une image du quadriptyque, bouton de la leçon
#: (retour NG 2026-08-27).
_GALLERY_PAGE_FIRST = 3


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


def _wave_button(w: dict, lang: str, width: str = "min(76%, 57vh)") -> None:
    """Le bouton-image d'une vague : la vignette de son OBJET, cliquable.

    Le clic saute à la carte-titre de la vague par le mécanisme natif du
    runtime paginé (``#stx-goto-<page>`` / ``stx-page-link`` — celui du TOC).
    L'image est GÉNÉRÉE PAR IA : la pastille DD-35 (CSS de ``ai_mark``,
    superposition, jamais incrustée) reste sur chaque vignette. Markup ici et
    pas dans un bloc (esprit R11 : le HTML vit dans le composant partagé).
    """
    page = _WAVE_PAGE_FIRST + w["order"] - 1
    img = f"app/static/images/waves/v{w['order']:02d}-objet.webp"
    name = content.text(w["name"], lang)
    chip = ('<span style="' + DD35_CSS + ' position:absolute; right:0.6em; '
            'top:0.6em; pointer-events:none;">✦ AI</span>'
            if content.image_ai(w["id"], "objet") else "")
    st_html(
        f'<a href="#stx-goto-{page}" class="stx-page-link" '
        f'style="display:block; position:relative; width:{width}; '
        f'margin:0 auto; border-radius:12px; overflow:hidden; '
        f'cursor:pointer;">'
        f'<img src="{img}" alt="{name} ({w["period"]}) — AI-generated title '
        f'card, click to open the wave" '
        f'style="width:100%; height:auto; display:block;"/>'
        f'{chip}'
        f'</a>')


def waves_grid_slide(marker: str, title_parts: tuple, first: int, last: int,
                     lang: str | None = None) -> None:
    """Une planche de vagues en boutons-image (2×2), sommaire ILLUSTRÉ du deck.

    Ligne NG 2026-08-26 (planche design) : la vignette de l'OBJET est le
    bouton, le titre vit dessous, et le clic NAVIGUE vers la première slide
    de la vague. ``title_parts`` = (avant, mot-clé teal, après) — un accent
    par titre (R3). La ligne complète de chaque vague (substitution comprise)
    reste dans l'infobulle du titre (R4).
    """
    lang = lang or content.default_language()
    span = content.wave_span(first, last)
    st_marker(marker)
    # page_fill_full : pas de marge latérale — les cellules prennent toute la
    # fenêtre pour que la ligne période+figures tienne sur UNE ligne ;
    # interlignes au minimum (retour NG tour 4).
    with st_block(s.project.containers.page_fill_full):
        with st_grid(cols="92% 8%",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                before, keyword, after = title_parts
                st_write(gs.title, before, (s.project.titles.keyword, keyword),
                         after, tag=t.div, toc_lvl="+1", label=marker)
            with g.cell():
                st_info_tooltip(title=f"{marker} — the full lines",
                                entries=_tooltip_entries(span, lang))
        st_space("v", "0.4vh")
        with st_grid(cols=s.project.grids.balanced(len(span), min_px=420),
                     gap="0.4vw", grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_top) as g:
            for w in span:
                with g.cell():
                    _wave_button(w, lang)
                    st_write(gs.name,
                             f"{w['order']} · {content.text(w['name'], lang)}",
                             tag=t.div)
                    st_write(gs.figures,
                             f"{w['period']} — "
                             + " · ".join(f["name"] for f in w["figures"]),
                             tag=t.div)


def wave_hero_grid_slide(marker: str, wave_id: str,
                         lang: str | None = None) -> None:
    """La dernière planche du sommaire : UNE vague, seule et en grand (l'IA).

    Amendement NG (ligne ``design``, 2026-08-26) : « l'IA seule sur la
    dernière, en gros » — le même bouton-image, à l'échelle de la slide.
    """
    lang = lang or content.default_language()
    w = content.wave(wave_id)
    st_marker(marker)
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(gs.title, "The seventeenth ",
                         (s.project.titles.keyword, "wave"),
                         tag=t.div, toc_lvl="+1", label=marker)
            with g.cell():
                st_info_tooltip(title=f"{marker} — the full line",
                                entries=_tooltip_entries([w], lang))
        st_space("v", "2vh")
        _wave_button(w, lang, width="min(72%, 96vh)")
        st_write(gs.name,
                 f"{w['order']} · {content.text(w['name'], lang)} · {w['period']}",
                 tag=t.div)
        st_write(gs.figures, " · ".join(f["name"] for f in w["figures"]),
                 tag=t.div)


def _gallery_back_button() -> None:
    """Le petit bouton DISCRET de retour à la première planche-galerie.

    Même mécanisme natif ``#stx-goto`` que les boutons de galerie — un lien
    pilule sobre, dimensionné caption, qui ne dispute rien au titre.
    """
    st_html(
        f'<a href="#stx-goto-{_GALLERY_PAGE_FIRST}" class="stx-page-link" '
        f'title="Back to the waves gallery" '
        f'style="display:inline-block; padding:0.15em 0.7em; '
        f'border:1px solid rgba(149,165,166,0.45); border-radius:999px; '
        f'color:#95A5A6; text-decoration:none; cursor:pointer; '
        f'font-size:clamp(11px, 1.1vw, 22px); white-space:nowrap;">'
        f'🌊 all waves</a>')


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

#: Bornée pour que image + bandeaux tiennent SANS SCROLL en 1920×1080
#: (retour NG 2026-08-26 : −20 %) : hauteur d'image ≈ 57vh (16:9), unités de
#: fenêtre — jamais de %, le zoom y est inerte (règle R-zoom).
_STAGE_WIDTH = "min(77%, 102vh)"

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
        # Image CLIQUABLE (retour NG 2026-08-27) : un clic renvoie à la
        # première planche-galerie — même mécanisme natif #stx-goto que les
        # boutons de galerie. La pastille DD-35 reste pilotée par le manifeste
        # de provenance (waves-images.json), jamais par le bloc.
        chip = ('<span style="' + DD35_CSS + ' position:absolute; '
                'right:0.6em; top:0.6em; pointer-events:none;">✦ AI</span>'
                if content.image_ai(w["id"], etage) else "")
        st_html(
            f'<a href="#stx-goto-{_GALLERY_PAGE_FIRST}" class="stx-page-link" '
            f'title="Back to the waves gallery" '
            f'style="display:block; position:relative; width:{_STAGE_WIDTH}; '
            f'margin:0 auto; border-radius:12px; overflow:hidden; '
            f'cursor:pointer;">'
            f'<img src="app/static/{content.image_uri(w["id"], etage)}" '
            f'alt="{content.etage_label(etage, "en")} — {name} '
            f'({w["period"]}): AI-generated historical reconstruction" '
            f'style="width:100%; height:auto; display:block;"/>'
            f'{chip}'
            f'</a>')
        st_write(ss.phrase, content.phrase(w["id"], etage, lang), tag=t.div)


#: L'ordre et le libellé des langues du lecteur (retour NG 2026-08-27) —
#: seules les langues réellement gelées s'affichent.
_LANG_FLAGS = {"en": "🇬🇧 EN", "fr": "🇫🇷 FR", "de": "🇩🇪 DE"}

#: Préférence de langue vidéo, PARTAGÉE entre les slides de figures — clé
#: NON-widget (patron à deux clés, PLAYBOOK §7 : chaque figure a son widget
#: `pvl_<id>`, la préférence survit d'une page à l'autre dans cette clé).
_LANG_PREF_KEY = "waves_video_lang"


def _poster_video_langs(fig_id: str, media: dict, name: str,
                        width: str = "min(38vw, 66vh)") -> None:
    """Le portrait-lecteur MULTILINGUE : drapeaux sous la vidéo.

    Bascule par WIDGET Streamlit (rerun) et non par CSS : ``st.html``
    supprime les gestionnaires d'événements, et un ``<video>`` masqué en CSS
    continuait de jouer — deux bandes-son simultanées, constaté par NG le
    2026-08-27. Le rerun DÉTRUIT l'ancien lecteur et en recrée UN SEUL dans
    la langue choisie : une seule piste peut exister. La préférence suit
    l'orateur de figure en figure (clé non-widget partagée). Limite connue :
    l'export statique n'a pas de widgets — il fige la langue préférée par
    défaut (en).
    """
    codes = [c for c in _LANG_FLAGS if c in media["videos"]]
    pref = st.session_state.get(_LANG_PREF_KEY, "en")
    current = pref if pref in codes else codes[0]
    key = f"pvl_{''.join(c for c in fig_id if c.isalnum())}"

    def _sync() -> None:
        st.session_state[_LANG_PREF_KEY] = st.session_state[key]

    chip = (f'<span style="{DD35_CSS} position:absolute; right:0.6em; '
            f'top:0.6em; pointer-events:none;">✦ AI</span>'
            if media.get("video_ai") else "")
    st_html(
        f'<div style="position:relative; width:{width}; margin:0 auto;">'
        f'<video controls preload="none" playsinline '
        f'poster="app/static/media/{media["portrait"]}" '
        f'style="width:100%; height:auto; display:block; border-radius:12px;" '
        f'aria-label="Presentation video of {name} ({current})">'
        f'<source src="{media["videos"][current]}" type="video/mp4">'
        f'</video>{chip}</div>')
    if len(codes) > 1:
        st.radio("video language", codes, index=codes.index(current),
                 key=key, on_change=_sync, horizontal=True,
                 label_visibility="collapsed",
                 format_func=lambda c: _LANG_FLAGS[c])


def _figure(w: dict, f: dict, lang: str,
            zoomImage: int = 100, zoomText: int = 180) -> None:
    """Une figure de la vague — le portrait EST le lecteur (patron debates).

    Les vidéos restent au CDN (``preload="none"`` : rien n'est téléchargé
    tant que l'orateur ne joue pas), en TROIS langues quand le gel les porte
    — les drapeaux sous le lecteur basculent la piste (retour NG 2026-08-27).
    Une figure sans portrait+vidéo ``public-ok`` (gandhi, hawking) est
    présentée en nom seul — jamais de trou projeté. ``zoomImage``/``zoomText``
    (ligne NG ``design``, 2026-08-26) : réglables par vague à l'appel de
    ``wave_slides``.
    """
    media = f.get("media")
    meta = " · ".join(x for x in (f.get("dates"), f.get("origin"),
                                  f.get("stance")) if x)

    def _portrait():
        _poster_video_langs(f["id"], media, f["name"])

    if media:
        with hero_split(s, image=_portrait, ratio=46,
                        zoom=zoomText, image_zoom=zoomImage):
            st_write(ss.name, f["name"], tag=t.div, toc_lvl="+1",
                     label=f["name"])
            st_write(ss.meta, meta, tag=t.div)
            st_write(ss.line, "a witness of ",
                     (s.project.colors.keyword, content.text(w["name"], lang)),
                     tag=t.div)
            # Pas de mention répétée du streaming/du deck Debates : la leçon
            # debates du 2026-08-11 (une clause répétée 54 fois devient du
            # papier peint) ; l'info orateur vit dans les speaker notes.
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


class TwoPlusOneStyles:
    head_top = s.project.body.pole_label
    body_top = s.project.body.bullet + s.center_txt
    head_bottom = s.project.body.pole_label + s.project.colors.amber
    body_bottom = s.project.body.bullet_giant + s.center_txt


tp = TwoPlusOneStyles


def two_plus_one(cells_top: list[tuple], cell_bottom: tuple,
                 zoom_top: int = 100, zoom_bottom: int = 80) -> None:
    """La grille 2+1 (ligne NG ``design``, 2026-08-26) — le gabarit des
    leçons et de « Why look back ».

    Rangée 1 : DEUX cellules colorées (bleu, sarcelle — palette p1) ;
    rangée 2 : UNE cellule pleine largeur, AMBRE, polices un cran au-dessus —
    la plus visible des trois (l'ambre reste l'accent unique de la slide, R5).
    ``zoom_top``/``zoom_bottom`` se règlent PAR SLIDE, à l'appel — le contrat
    ``hero_split``, jamais une configuration centrale.

    :param cells_top: deux tuples ``(titre, *parts)`` — les ``parts`` passent
        tels quels à ``st_write`` (texte, tuples stylés, HTML de citation).
    :param cell_bottom: un tuple ``(titre, *parts)``.
    """
    top_cards = (s.project.cards.blue, s.project.cards.teal)
    with st_zoom(zoom_top):
        with st_grid(cols=s.project.grids.balanced(len(cells_top), min_px=420),
                     gap="1.5vw", grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_top) as g:
            for card, (head, *parts) in zip(top_cards, cells_top):
                with g.cell(), st_block(card):
                    st_write(tp.head_top, head, tag=t.div)
                    st_write(tp.body_top, *parts, tag=t.div)
    st_space("v", "2vh")
    with st_zoom(zoom_bottom):
        with st_grid(cols="1fr", grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_top) as g:
            head, *parts = cell_bottom
            with g.cell(), st_block(s.project.cards.amber):
                st_write(tp.head_bottom, head, tag=t.div)
                st_write(tp.body_bottom, *parts, tag=t.div)


def _lesson(w: dict, lang: str,
            zoom_top: int = 100, zoom_bottom: int = 80) -> None:
    """La leçon de la vague — PLACEHOLDER rubriqué (conception L1 validée).

    Gabarit 2+1 : « craint » / « advenu » en haut, l'ÉCHO IA seul en bas, en
    grand et en ambre — la rangée la plus visible (ligne NG ``design``).
    Phase 2 (campagne hub) : l'objet ``ai_lesson`` trilingue, sourcé, avec le
    miroir de citations hier/aujourd'hui — gelé par l'outil.
    """
    name = content.text(w["name"], lang)
    # L'écho est le point SPÉCIFIQUE de la vague (retour NG 2026-08-26 :
    # la phrase générique de substitution n'apprenait rien) — il vit dans le
    # récit (waves-story.json, champ `echo`), jamais généré ici.
    echo = content.echo(w["id"], lang)
    with st_block(s.project.containers.page_fill_top):
        # Rangée de titre 90/10 (retour NG 2026-08-27) : le petit bouton
        # discret de la 2e cellule renvoie à la première planche-galerie.
        with st_grid(cols="90% 10%",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(ss.title, "What ", (s.project.titles.keyword, name),
                         " teaches us", tag=t.div, toc_lvl="+1",
                         label="The lesson")
            with g.cell():
                _gallery_back_button()
        st_space("v", "3vh")
        two_plus_one(
            [("What was feared", content.phrase(w["id"], "crise", lang)),
             ("What came of it", content.phrase(w["id"], "recompose", lang))],
            ("The echo for AI", echo),
            zoom_top=zoom_top, zoom_bottom=zoom_bottom)


def wave_slides(wave_id: str, lang: str | None = None,
                zoomImage: int = 100, zoomText: int = 180,
                lesson_zoom_top: int = 100,
                lesson_zoom_bottom: int = 80) -> None:
    """Toutes les slides d'une vague — UN arrêt visible, le reste caché.

    Ordre : la carte-titre (l'OBJET de la révolution), puis le récit
    (avant → crise → recomposé), puis les figures au portrait-lecteur,
    puis la leçon. Les flèches traversent tout ; la barre latérale ne
    liste que la vague. Les quatre zooms se règlent PAR VAGUE, dans son
    bloc de trois lignes (contrat ``hero_split``).
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
        _figure(w, f, lang, zoomImage=zoomImage, zoomText=zoomText)
    st_slide_break(**_HIDDEN)
    _lesson(w, lang, zoom_top=lesson_zoom_top, zoom_bottom=lesson_zoom_bottom)
