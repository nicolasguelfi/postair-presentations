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

import json
from pathlib import Path

from postair_chain import chain
from postair_lang import T, with_lang
from shared_widgets import st_info_tooltip, st_poster_video
from streamtex import (
    SlideBreakConfig,
    SlideBreakMode,
    st_block,
    st_grid,
    st_html,
    st_image,
    st_marker,
    st_slide_break,
    st_space,
    st_write,
)
from streamtex.enums import Tags as t

from custom.content import axis_poles, text, warnings_for
from custom.pole import faceoff_sides, mascots
from custom.refs import citation_or
from custom.styles import DS
from custom.styles import Styles as s
from postair_pack.components.ai_mark import DD35_CSS, dd35_overlay
from postair_pack.components.argument_card import argument_card
from postair_pack.components.hero_split import hero_split
from postair_pack.components.pole_faceoff import pole_faceoff
from postair_pack.components.pole_identity import pole_identity


class RenderStyles:
    title = s.project.titles.slide_title + s.center_txt
    subtitle = s.project.titles.subtitle + s.center_txt
    wave_name = s.project.body.pole_label_compact + s.center_txt
    wave_period = s.project.body.caption + s.center_txt
    banner = s.project.body.body + s.center_txt
    # La slide une-figure (NG 2026-08-13) : nom en très grand, méta et
    # référence discrètes, verbatim en corps de lecture.
    figure_name = s.project.body.name_double + s.center_txt
    figure_meta = s.project.body.mascot_name + s.center_txt
    figure_stance = s.project.body.body + s.project.colors.keyword + s.center_txt
    quote = s.project.body.bullet + s.center_txt
    figure_ref = s.project.body.caption + s.center_txt


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
    st_space("v", s.project.spacing.title_gap)
    pole_identity(both, [text(x["text"], lang) for x in pole["statements"]], DS)


# ── La slide « vagues » d'un pôle (NG 2026-08-30) ────────────────────────────
#: Provenance des cartes-titres copiées du deck des vagues (drapeau DD-35).
_WAVES_IMAGES = Path(__file__).parent.parent / "static" / "data" / "waves-images.json"
_WAVES_UI = {
    "title_before": {"en": "When society chose ", "fr": "Quand la société a choisi "},
    "tip_title": {"en": "The waves that illustrate ", "fr": "Les vagues qui illustrent "},
    "how": ({"en": "How a wave is chosen", "fr": "Comment une vague est retenue"},
            {"en": ("A wave illustrates a pole when the collective behaviour that dominated "
                    "the society of the time — institutions, market, opinion, mass practice, "
                    "not only the elites' discourse — committed unanimously and durably in the "
                    "direction of that pole. Rank 1 is the best example; the strength of the "
                    "match is stated. Click a card to open the wave in the waves deck."),
             "fr": "Une vague illustre un pôle quand le comportement collectif dominant de la société de l'époque — institutions, marché, opinion, pratiques de masse, pas seulement le discours des élites — s'est engagé unanimement et durablement dans le sens de ce pôle. Le rang 1 est le meilleur exemple ; la solidité du rapprochement est dite. Cliquer une carte ouvre la vague dans le deck des vagues."}),
    "strength": {"strong": {"en": "strong match", "fr": "rapprochement fort"},
                 "medium": {"en": "moderate match", "fr": "rapprochement moyen"},
                 "weak": {"en": "weak match — best approximation", "fr": "rapprochement faible — meilleure approximation"}},
    "open": {"en": "click to open the wave", "fr": "cliquer pour ouvrir la vague"},
}


def _wave_image_ai(order: int) -> bool:
    """Le drapeau DD-35 de la carte-titre — bruyant si la provenance manque."""
    key = f"v{order:02d}-objet"
    entry = json.loads(_WAVES_IMAGES.read_text(encoding="utf-8"))["images"].get(key)
    if entry is None:
        raise KeyError(f"carte-titre {key!r} absente de waves-images.json (debates) — "
                       f"une image sans provenance ne se projette pas.")
    return bool(entry.get("ai", True))


def _waves_deck_url(lang: str) -> str:
    """Le deck des vagues, dans la langue projetée — résolu comme la chaîne du
    jour (env local > collection.toml). Ouvre le deck en PREMIÈRE page :
    streamtex 0.7.26 n'adresse pas une page par l'URL (évolution demandée à la
    librairie : streamtex #42, 2026-08-30) ; le jour où elle existe, le
    paramètre ``?marker=<vague>`` s'ajoute ici."""
    for m in chain():
        if m["key"] == "waves":
            return with_lang(m["url"], lang)
    raise LookupError("collection.toml ne déclare pas le module `waves`")


def _wave_card(w: dict, lang: str, url: str, width: str) -> None:
    """La carte-titre d'une vague, cliquable (nouvel onglet). Markup ici, pas
    dans un bloc (esprit R11) ; pastille DD-35 en superposition, jamais
    incrustée — même geste que ``_wave_button`` du deck des vagues."""
    img = f"app/static/images/waves/v{w['order']:02d}-objet.webp"
    name = text(w["name"], lang)
    chip = ('<span style="' + DD35_CSS + ' position:absolute; right:0.6em; top:0.6em; '
            'pointer-events:none;">✦ AI</span>') if _wave_image_ai(w["order"]) else ""
    st_html(
        f'<a href="{url}" target="_blank" rel="noopener" '
        f'style="display:block; position:relative; width:{width}; margin:0 auto; '
        f'border-radius:12px; overflow:hidden; cursor:pointer;">'
        f'<img src="{img}" alt="{name} ({text(w["period"], lang)}) — AI-generated title card, '
        f'{T(_WAVES_UI["open"], lang)}" style="width:100%; height:auto; display:block;"/>'
        f'{chip}</a>')


def _waves(pole: dict, lang: str | None) -> None:
    """Les révolutions où une société majoritaire a tenu ce pôle — une ligne
    de cartes-titres cliquables vers le deck des vagues. Tout vient du gel
    (``pole["waves"]``, joint depuis l'artefact du hub) : rien n'est nommé ici."""
    lang = lang or "en"
    pole_name = text(pole["pole"], lang)
    waves = pole["waves"]
    entries = [(T(_WAVES_UI["how"][0], lang), T(_WAVES_UI["how"][1], lang))]
    for w in waves:
        just = w.get("justification") or {}
        strength = T(_WAVES_UI["strength"].get(w.get("strength"), {"en": "", "fr": ""}), lang)
        entries.append((f"{w['order']} · {text(w['name'], lang)} ({text(w['period'], lang)})"
                        + (f" — {strength}" if strength else ""),
                        just.get(lang) or just.get("fr") or just.get("en") or ""))
    _header([T(_WAVES_UI["title_before"], lang), (s.project.titles.keyword, pole_name)],
            T(_WAVES_UI["tip_title"], lang) + pole_name, entries)
    st_space("v", s.project.spacing.title_gap)
    url = _waves_deck_url(lang)
    # ONE flat grid — one cell per wave, on a single line (never more than a few).
    with st_grid(cols=s.project.grids.balanced(len(waves)), gap="1.5vw",
                 cell_styles=s.project.containers.grid_cell_centered) as g:
        for w in waves:
            with g.cell():
                _wave_card(w, lang, url, width="min(38vw, 56vh)")
                st_write(rs.wave_name, text(w["name"], lang), tag=t.div)
                strength = T(_WAVES_UI["strength"].get(w.get("strength"), {"en": "", "fr": ""}), lang)
                st_write(rs.wave_period,
                         " · ".join(x for x in (text(w["period"], lang), strength) if x),
                         tag=t.div)


def _pole_banner(pole: dict) -> None:
    """L'avertissement « aucune figure ne défend ce pôle », s'il existe."""
    for warning in warnings_for(pole["axis"]):
        if pole["pole"].get("abbr", {}).get("en", "") in warning:
            st_space("v", "1vh")
            with st_block(s.project.cards.amber):
                st_write(rs.banner,
                         "No figure in this study champions this pole. These are the three "
                         "closest to it — the strongest voices this corpus has to offer on "
                         "this side, and that absence is itself worth debating.", tag=t.div)


def _why_here(f: dict, pole_name: str, lang: str | None) -> list[tuple[str, str]]:
    """Pourquoi CETTE figure est sur CE pôle — dans les mots du hub.

    Le registre des citations dit de quel énoncé une citation *parle*, jamais
    si la figure l'approuve ; c'est le profil qui le dit, par sa réponse
    validée et son ``anchor`` sourcé. Les deux voyagent maintenant dans le gel
    (règle P1, 2026-08-13) : la slide affirmait une position sans jamais la
    justifier, et personne dans la salle ne pouvait relier le verbatim au pôle.

    Rien n'est rédigé ici. Une reformulation locale de ce raisonnement serait
    une seconde vérité — la règle du tuyau amont l'interdit.
    """
    out = []
    for r in (f["quote"].get("reasoning") or []):
        statement = text(r.get("statement"), lang) or ""
        response = r.get("response")
        stance = ("agrees" if isinstance(response, int) and response >= 3
                  else "disagrees") if response is not None else "did not answer"
        parts = [f"“{statement}” — {f['name']} {stance}"]
        if isinstance(response, int):
            parts[0] += f" ({response}/5)"
        parts[0] += (f", which points to {pole_name}." if r.get("direction") == "toward"
                     else f", which points AWAY from {pole_name} — the figure is here on "
                          f"its overall score for the axis, not on this statement.")
        if r.get("anchor"):
            parts.append(f"Evidence: {r['anchor']}.")
        if r.get("transposition"):
            parts.append(f"Transposed to AI: {r['transposition']}.")
        if r.get("confidence"):
            parts.append(f"Confidence of the inference: {r['confidence']}.")
        out.append((f"Why this pole — {r['item']}", " ".join(parts)))
    return out


def _figure(pole: dict, f: dict, index: int, lang: str | None) -> None:
    """UNE figure par slide (NG 2026-08-13, 1 idée = 1 slide).

    Le portrait — enfin grand — à gauche sur ~la moitié de la largeur, et à
    droite : nom, méta télégraphique, le VERBATIM (intouchable), le code de
    citation. L'ancienne grille de trois cartes coupait les citations au pli
    sur les dix-huit exemplaires du gabarit.
    """
    pole_name = text(pole["pole"], lang)
    # En tête du tooltip : QUI est cette figure (demande NG 2026-08-14 —
    # pourquoi elle, sa révolution, son rôle dans la société de l'époque).
    # Les deux textes sont la ``presentation`` et la ``biography.place``
    # éditoriales du hub, gelées telles quelles — jamais rédigés ici.
    who = [(f"Who — and why {f['name']}", f["presentation"])] if f.get("presentation") else []
    if f.get("epoch"):
        who.append(("In the society of their time", f["epoch"]))
    entries = who + _why_here(f, pole_name, lang) + [
               (f"{f['name']} ({f.get('dates', '')})",
                f"{f.get('origin', '')} · {f.get('wave', '')} · score {f['score']} on "
                f"this axis."),
               ("Video", "The portrait IS the player: press play and the video runs in "
                         "its frame — full screen and back, without leaving the deck. "
                         + ("It is an AI-generated talking portrait — synthetic face and "
                            "voice, built from documented sources. "
                            if (f.get("media") or {}).get("video_kind") == "talk" else
                            "A living person is never made to speak by generative AI: "
                            "the author presents the figure on camera. ")
                         + "The provenance rules are on the Provenance slide, at the start."),
               ("Reference", "The quotation is verbatim and verified; its citation code "
                             "opens the full reference on hover, and the References page "
                             "lists them all.")]
    full = f["quote"].get("reference_full")
    if full and full != f["quote"].get("reference"):
        entries.append(("Full reference", full))
    _header(["Before us — ", (s.project.titles.keyword, pole_name)],
            f"{f['name']} — {pole_name}", entries)
    if index == 0:
        _pole_banner(pole)
    st_space("v", s.project.spacing.title_gap)
    media = f.get("media") or {}
    quote = text(f["quote"], lang) or f["quote"].get("en") or ""
    # Le corpus autorise 300 caractères (borne de la salle) mais la colonne
    # n'en affiche ~180 qu'à taille pleine : au-delà, la ligne de référence
    # passait sous le pli (constaté sur Marinetti et Arendt, 2026-08-13). Le
    # zoom suit la longueur pour que TOUT reste au-dessus du pli.
    zoom = 100 if len(quote) <= 180 else (90 if len(quote) <= 240 else 80)
    def _portrait() -> None:
        # Le portrait EST le poster du lecteur (NG 2026-08-24) : la vidéo se
        # joue dans le cadre de la photo, plein écran natif compris, au lieu
        # d'ouvrir un onglet — quitter le deck en séance était le vrai risque.
        # Streaming pur : `preload="none"` + Range du CDN, rien n'est
        # embarqué dans l'image (les 54 masters pèsent 612 Mo).
        video = media.get("video")
        if video:
            st_poster_video(
                video, f"app/static/media/{media.get('portrait')}",
                alt=f"Presentation video of {f['name']}",
                width="min(38vw, 66vh)",
                ai_marked=bool(media.get("video_ai")
                               or media.get("video_kind") == "talk"))
            return
        st_image(DS.cards.media_center, width="min(38vw, 66vh)",
                 uri=media.get("portrait"),
                 alt=f"Portrait of {f['name']}",
            overlay=dd35_overlay(media.get("portrait_ai", False)))

    with hero_split(s, zoom=zoom, image=_portrait):
        st_write(rs.figure_name, f["name"], tag=t.div)
        st_write(rs.figure_meta,
                 " · ".join(x for x in (f.get("dates"), f.get("origin"),
                                        f.get("wave")) if x), tag=t.div)
        st_write(rs.figure_stance,
                 f"{text(pole['axis_name'], lang)} · {pole_name} · "
                 f"{_EFFECT[pole['effect']]}", tag=t.div)
        st_space("v", "1vh")
        st_write(rs.quote, f"“{quote}”", tag=t.div)
        st_space("v", "0.6vh")
        st_write(rs.figure_ref,
                 citation_or(f["quote"].get("reference"),
                             *(f["quote"].get("citekeys") or [])), tag=t.div)


def _arguments(pole: dict, lang: str | None) -> None:
    pole_name = text(pole["pole"], lang)
    # Attribution COURTE à l'écran (« Andrew Ng ») — la titulature complète
    # (« co-founder of Google Brain, professor at Stanford ») vit au tooltip.
    entries = [(text(a["title"], lang),
                " — ".join(x for x in (a.get("person"),
                                       text(a.get("text"), lang) or "") if x))
               for a in pole["arguments"]]
    entries.append(("Symmetry", "The opposite pole has its own three arguments, of the same "
                                "three natures. Never open this slide without the other one — "
                                "the room must hear both best cases."))
    entries.append(("Paraphrase or verbatim", "A card carrying a quotation gives it verbatim; "
                                              "the others are documented paraphrases of a "
                                              "sourced position."))
    _header(["And ", (s.project.titles.keyword, "today"), "? — ", pole_name],
            f"Contemporary arguments for {pole_name}", entries)
    st_space("v", s.project.spacing.title_gap)
    with st_grid(cols=s.project.grids.balanced(len(pole["arguments"])), gap="1.2vw",
                 grid_style=s.project.grids.stretch,
                 cell_styles=s.project.containers.grid_cell_centered) as g:
        for a in pole["arguments"]:
            with g.cell():
                # La ligne de source est le code de citation natif — carte
                # complète au survol — avec repli sur la chaîne du manifeste
                # si la clé n'était pas gelée.
                person_short = (a.get("person") or "").split(",")[0].strip() or None
                argument_card(a, DS, text(a["title"], lang),
                              person=person_short,
                              source_html=citation_or(
                                  a.get("reference") or a.get("citekey") or "",
                                  *([a["citekey"]] if a.get("citekey") else [])))


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
    st_space("v", s.project.spacing.title_gap)
    pole_faceoff(faceoff_sides(both, lang), DS)
    st_space("v", "2vh")
    # Le protocole, VISIBLE (NG 2026-08-13) : la slide-pivot du débat ne
    # doit plus dépendre du tooltip pour être comprise.
    st_write(rs.banner, "show of hands → one argument each bench → the measurement",
             tag=t.div)


def axis_slides(axis: str, lang: str | None = None) -> None:
    """Les sous-slides d'un axe, pôle accélérateur d'abord.

    Depuis le 2026-08-13 : identité du pôle, puis UNE slide PAR figure (trois
    par pôle), puis les arguments contemporains — onze slides par axe plus le
    face-à-face. Depuis le 2026-08-30, entre l'identité et les figures : la
    slide des VAGUES qui illustrent le pôle, quand le gel en porte. Le deck est paginé et le présentateur n'ouvre que les axes
    clivants : le nombre de pages n'est pas un coût, la lisibilité en est un.
    """
    both = axis_poles(axis)
    first = True
    for pole in both:
        pole_name = text(pole["pole"], lang)
        # La slide « vagues » suit l'identité (NG 2026-08-30) et ne se rend
        # que si le gel porte des vagues pour ce pôle (artefact du hub).
        parts = [_identity] + ([_waves] if pole.get("waves") else []) + \
            [(lambda p, lg, ff=f, i=i: _figure(p, ff, i, lg))
             for i, f in enumerate(pole["figures"])] + [_arguments]
        for part in parts:
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
