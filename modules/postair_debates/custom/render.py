"""The sub-slides of one axis, rendered from the manifest, in debate order.

Every axis block is the same code with a different axis id. Since NG's
2026-08-31 decision the rhythm follows the DEBATE, not the material: the two
pole identities first (the questions, recalled), then the debate stage — the
room speaks BEFORE seeing the material — and only then the content, pole by
pole (waves, figures, contemporary arguments). Writing it once means a change
of gabarit reaches all nine axes at the same instant, and that no axis can
quietly drift from the others.

Navigation follows the speaker, not the templates: a visible marker per pole
and one for the debate stage — three stops in the marker list — while every
sub-slide still breaks so PageDown advances one screen at a time.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from postair_chain import chain
from postair_data import mascot
from postair_i18n import ui
from postair_lang import T, TF, with_lang
from shared_widgets import st_info_tooltip, st_poster_video

from streamtex import (
    SlideBreakConfig,
    SlideBreakMode,
    Style,
    page_url,
    st_block,
    st_grid,
    st_html,
    st_image,
    st_marker,
    st_slide_break,
    st_space,
    st_zoom,
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
    # Badge de nature des cartes d'argument (NG 2026-08-30) : la taille du
    # sous-titre réduite de 20 % (mêmes jetons d'échelle que le DS — 5vw→4vw,
    # ×1,5→×1,2), en teal gras. Réglage NG du 2026-08-30 soir.
    nature_badge = (s.project.titles.subtitle + s.project.titles.keyword
                    + Style("font-size: min(4vw, calc(var(--stx-scale-12, 32pt) * 1.2));",
                            "pa_nature_badge_80"))
    # Le nom (attribution) calé à GAUCHE (NG 2026-08-30) — le jeton du DS est
    # centré ; on ne change que l'alignement, la taille reste celle du DS.
    person = s.project.body.pole_label + Style("text-align: left;", "pa_arg_person_left")
    # La scène du débat (NG 2026-08-31) : sous-titre AU CORPS DU TITRE mais
    # en teal — la consigne de prise de parole, lisible pendant le débat.
    stage_subtitle = (s.project.titles.slide_title + s.center_txt
                      + s.project.colors.keyword)
    stage_pole = (s.project.body.pole_label
                  + Style("font-size: min(5.2vw, calc(var(--stx-scale-12, 32pt) * 1.3));",
                          "pa_stage_pole_130"))
    stage_synth = s.project.body.bullet + s.center_txt
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

#: Le chrome du gabarit d'axe — les feuilles partagées par les sous-slides
#: d'ici (règle R-i18n : module-local, pas dans le lexique partagé). Les
#: gabarits ``.format(...)`` les valeurs du gel (nom de pôle, d'axe, de
#: figure) — jamais un f-string projeté. Ce qui se répète entre modules
#: (« Mascots », « Reference ») vient de ``postair_i18n.ui``.
#: Le badge de nature des cartes d'argument (i18n 2026-08-30) — résolu ici,
#: passé au composant du pack par ``nature=`` ; l'EN reprend ``NATURES``.
_NATURES = {
    "policy": {"en": "public policy", "fr": "politique publique"},
    "case": {"en": "concrete case", "fr": "cas concret"},
    "quote": {"en": "public statement", "fr": "déclaration publique"},
    "historical": {"en": "historical precedent", "fr": "précédent historique"},
    "tradition": {"en": "established practice", "fr": "pratique établie"},
}

_UI = {
    # What each pole does to the diffusion of the technology. Neutral wording:
    # neither side of an axis is the good one, and the badge must not suggest it.
    "effect": {"accelerator": {"en": "accelerates adoption", "fr": "accélère l'adoption"},
               "decelerator": {"en": "slows adoption down", "fr": "freine l'adoption"}},
    # _identity
    "claims": {"en": "What this pole claims", "fr": "Ce qu'affirme ce pôle"},
    "claims_text": {"en": ("{pole} — the posture that {effect} on the {axis} axis. It is a "
                           "legitimate position, held and argued by people whose names are "
                           "in the history of technology."), "fr": "{pole} — la posture qui {effect} sur l'axe {axis}. C'est une position légitime, tenue et défendue par des gens dont le nom est dans l'histoire des techniques."},
    "axis_pole": {"en": "{axis} — {pole}", "fr": "{axis} — {pole}"},
    "axis_effect": {"en": "{axis} · {effect}", "fr": "{axis} · {effect}"},
    # _pole_banner
    "no_champion": {"en": ("No figure in this study champions this pole. These are the three "
                           "closest to it — the strongest voices this corpus has to offer on "
                           "this side, and that absence is itself worth debating."), "fr": "Aucune figure de cette étude ne défend ce pôle. Voici les trois qui s'en approchent le plus — les voix les plus fortes du corpus de ce côté. Et cette absence, en soi, mérite débat."},
    # _why_here
    "agrees": {"en": "agrees", "fr": "est d'accord"},
    "disagrees": {"en": "disagrees", "fr": "n'est pas d'accord"},
    "no_answer": {"en": "did not answer", "fr": "n'a pas répondu"},
    "stance_line": {"en": "“{statement}” — {name} {stance}", "fr": "« {statement} » — {name} {stance}"},
    "stance_score": {"en": " ({response}/5)", "fr": " ({response}/5)"},
    "points_toward": {"en": ", which points to {pole}.", "fr": ", ce qui pointe vers {pole}."},
    "points_away": {"en": (", which points AWAY from {pole} — the figure is here on its "
                           "overall score for the axis, not on this statement."), "fr": ", ce qui pointe À L'OPPOSÉ de {pole} — la figure est ici pour son score global sur l'axe, pas pour cet énoncé."},
    "evidence": {"en": "Evidence: {anchor}.", "fr": "Preuve : {anchor}."},
    "transposed": {"en": "Transposed to AI: {transposition}.", "fr": "Transposé à l'IA : {transposition}."},
    "confidence": {"en": "Confidence of the inference: {confidence}.", "fr": "Confiance dans l'inférence : {confidence}."},
    "why_pole": {"en": "Why this pole — {item}", "fr": "Pourquoi ce pôle — {item}"},
    # _figure
    "who": {"en": "Who — and why {name}", "fr": "Qui — et pourquoi {name}"},
    "epoch": {"en": "In the society of their time", "fr": "Dans la société de son temps"},
    "name_dates": {"en": "{name} ({dates})", "fr": "{name} ({dates})"},
    "figure_meta": {"en": "{origin} · {wave} · score {score} on this axis.", "fr": "{origin} · {wave} · score {score} sur cet axe."},
    "video": {"en": "Video", "fr": "Vidéo"},
    "video_player": {"en": ("The portrait IS the player: press play and the video runs in "
                            "its frame — full screen and back, without leaving the deck. "), "fr": "Le portrait EST le lecteur : lancez la lecture et la vidéo tourne dans son cadre — plein écran et retour, sans quitter le deck. "},
    "video_talk": {"en": ("It is an AI-generated talking portrait — synthetic face and "
                          "voice, built from documented sources. "), "fr": "C'est un portrait parlant généré par IA — visage et voix synthétiques, construits à partir de sources documentées. "},
    "video_live": {"en": ("A living person is never made to speak by generative AI: "
                          "the author presents the figure on camera. "), "fr": "Jamais l'IA générative ne fait parler une personne vivante : l'auteur présente la figure face caméra. "},
    "video_rules": {"en": "The provenance rules are on the Provenance slide, at the start.", "fr": "Les règles de provenance sont sur la slide Provenance, au début."},
    "reference_text": {"en": ("The quotation is verbatim and verified; its citation code "
                              "opens the full reference on hover, and the References page "
                              "lists them all."), "fr": "La citation est verbatim et vérifiée ; son code de citation ouvre la référence complète au survol, et la page Références les liste toutes."},
    "full_reference": {"en": "Full reference", "fr": "Référence complète"},
    "before_us": {"en": "Before us — ", "fr": "Avant nous — "},
    "figure_pole": {"en": "{name} — {pole}", "fr": "{name} — {pole}"},
    "figure_stance": {"en": "{axis} · {pole} · {effect}", "fr": "{axis} · {pole} · {effect}"},
    "quote": {"en": "“{quote}”", "fr": "« {quote} »"},
    # _arguments
    "symmetry": {"en": "Symmetry", "fr": "Symétrie"},
    "symmetry_text": {"en": ("The opposite pole has its own three arguments, of the same "
                             "three natures. Never open this slide without the other one — "
                             "the room must hear both best cases."), "fr": "Le pôle opposé a ses trois propres arguments, des trois mêmes natures. N'ouvrez jamais cette slide sans l'autre — la salle doit entendre les deux meilleurs plaidoyers."},
    "paraphrase": {"en": "Paraphrase or verbatim", "fr": "Paraphrase ou verbatim"},
    "paraphrase_text": {"en": ("A card carrying a quotation gives it verbatim; the others are "
                               "documented paraphrases of a sourced position."), "fr": "Une carte qui porte une citation la donne verbatim ; les autres sont des paraphrases documentées d'une position sourcée."},
    "today_title": {"en": ("And today for ", (s.project.titles.keyword, "AI"), "? — "), "fr": ("Et aujourd'hui pour l'", (s.project.titles.keyword, "IA"), " ? — ")},
    "today_tip": {"en": "Contemporary arguments for {pole}", "fr": "Arguments contemporains pour {pole}"},
    # _debate_stage (NG 2026-08-31) — la scène du débat, une par axe.
    "stage_title": {"en": "{axis} — {a} / {d}", "fr": "{axis} — {a} / {d}"},
    "stage_title_short": {"en": "{a} / {d}", "fr": "{a} / {d}"},
    "stage_subtitle": {"en": "hands on — mic — tell us", "fr": "à vous — micro — dites-nous"},
    "stage_tip_title": {"en": "Running the debate of this axis", "fr": "Mener le débat de cet axe"},
    "stage_floor": ({"en": "Taking the floor", "fr": "Prendre la parole"},
                    {"en": ("Raise your hand; take the microphone; say why you favour "
                            "the pole on screen — one argument, thirty seconds."), "fr": "Levez la main ; prenez le micro ; dites pourquoi vous défendez le pôle à l'écran — un argument, trente secondes."}),
    "stage_synthesis": ({"en": "The two sentences", "fr": "Les deux phrases"},
                        {"en": ("Each side shows the pole's synthetic statement — the one "
                                "sentence of the quick poll. The material of the axis "
                                "(waves, figures, arguments) comes AFTER the debate."), "fr": "Chaque côté montre l'énoncé synthétique du pôle — la phrase du sondage rapide. Le matériau de l'axe (vagues, figures, arguments) vient APRÈS le débat."}),
    "stage_both": ({"en": "Both sides, always", "fr": "Les deux camps, toujours"},
                   {"en": ("Give the floor alternately — the room must hear the two best "
                           "cases, not the one the speaker prefers."), "fr": "Donnez la parole en alternance — la salle doit entendre les deux meilleurs plaidoyers, pas celui que l'orateur préfère."}),
    # _faceoff
    "where_room": {"en": "Where is this room?", "fr": "Où se situe cette salle ?"},
    "where_room_text": {"en": ("The live distribution is in the survey application, on the "
                               "results page of the day. It cannot be drawn here: it changes "
                               "while you speak."), "fr": "La distribution en direct est dans l'application du sondage, sur la page des résultats du jour. Impossible de la dessiner ici : elle bouge pendant que vous parlez."},
    "reading": {"en": "Reading a distribution", "fr": "Lire une distribution"},
    "reading_text": {"en": ("Averages hide diversity. An axis at fifty can be a room of "
                            "moderates or two opposed halves — look at the shape, not the "
                            "number."), "fr": "Les moyennes cachent la diversité. Un axe à cinquante peut être une salle de modérés ou deux moitiés opposées — regardez la forme, pas le chiffre."},
    "codes": {"en": "Posture codes", "fr": "Codes de posture"},
    "codes_text": {"en": ("Directional: clearly on one pole. Ambivalent: agrees with BOTH "
                          "poles, which is not indecision but a held tension. Balanced: "
                          "deliberately in between. Detached: the question does not mobilise."), "fr": "Tranchée : nettement sur un pôle. Ambivalente : adhère aux DEUX pôles, ce qui n'est pas de l'indécision mais une tension assumée. Équilibrée : délibérément entre les deux. Détachée : la question ne mobilise pas."},
    "three_moves": {"en": "Three moves", "fr": "Trois temps"},
    "three_moves_text": {"en": ("Show of hands — who is on which side. Then one argument from "
                                "each bench. Then what the measurement actually says."), "fr": "À main levée — qui est de quel côté. Puis un argument de chaque banc. Puis ce que la mesure dit vraiment."},
    "faceoff_label": {"en": "{left} ⇄ {right}", "fr": "{left} ⇄ {right}"},
    "protocol": {"en": "show of hands → one argument each bench → the measurement", "fr": "à main levée → un argument par banc → la mesure"},
}


def _effect(pole: dict, lang: str | None) -> str:
    return T(_UI["effect"][pole["effect"]], lang)


def _header(title_parts, tooltip_title, entries, label=None, toc_lvl="+1") -> None:
    with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
        with g.cell():
            st_write(rs.title, *title_parts, tag=t.div, toc_lvl=toc_lvl, label=label)
        with g.cell():
            st_info_tooltip(title=tooltip_title, entries=entries)


@lru_cache(maxsize=64)
def _mascot_ratio(uri: str) -> float:
    """Largeur/hauteur du FICHIER de la mascotte (R4d : une propriété du
    média). Lu une fois par Pillow sur la copie matérialisée ; repli neutre
    (carré) si l'image ou Pillow manquent — jamais d'erreur en séance."""
    try:
        from PIL import Image
        with Image.open(Path(__file__).parent.parent / "static" / "media" / uri) as im:
            return im.width / im.height
    except Exception:
        return 1.0


def _identity(pole: dict, lang: str | None) -> None:
    pole_name = text(pole["pole"], lang)
    axis_name = text(pole["axis_name"], lang)
    entries = [(T(_UI["claims"], lang),
                T(_UI["claims_text"], lang).format(
                    pole=pole_name, effect=_effect(pole, lang), axis=axis_name))]
    for st_item in pole["statements"]:
        guidance = st_item.get("guidance") or {}
        parts = [text(guidance.get("clarification"), lang),
                 text(guidance.get("anchor_low"), lang),
                 text(guidance.get("anchor_high"), lang)]
        for example in (guidance.get("examples") or [])[:1]:
            parts.append(text(example, lang))
        entries.append((text(st_item["text"], lang), " ".join(p for p in parts if p)))
    both = mascots(pole)
    entries.append((ui("mascots", lang),
                    " · ".join(f"{m['mascot']}: {m.get('description') or m['label']}"
                               for m in both)))
    _header([pole_name], T(_UI["axis_pole"], lang).format(axis=axis_name, pole=pole_name),
            entries, label=pole_name, toc_lvl="1")
    st_write(rs.subtitle,
             T(_UI["axis_effect"], lang).format(axis=axis_name, effect=_effect(pole, lang)),
             tag=t.div)
    st_space("v", s.project.spacing.title_gap)
    # +20 % demandés (NG 2026-08-30), tempérés au rendu : à zoom fixe, la
    # troisième carte passait sous le pli sur les pôles aux énoncés longs.
    # Le zoom suit le nombre de LIGNES estimé du texte RENDU (la langue
    # courante — les longueurs EN et FR diffèrent) : ~34 caractères par ligne
    # dans la colonne à ce corps ; ≤ 6 lignes → 116, ≤ 8 → 106, au-delà → 98
    # (mesuré à 1920×1080 sur Contrôle, Transhumanisme, Confiance).
    # Mascottes : largeur +20 % (13vw→15.6vw), et la borne de hauteur suit le
    # RATIO du fichier (R4d) : min(15.6vw, 27vh × ratio) — une mascotte
    # portrait (Serro : 0,51) obtient une largeur plus étroite pour la même
    # hauteur, au lieu de pousser la colonne sous le pli (vu sur Contrôle).
    statements = [text(x["text"], lang) for x in pole["statements"]]
    lines = sum(-(-len(x) // 34) for x in statements)
    widths = [f"min(15.6vw, {27 * _mascot_ratio(m['image']):.1f}vh)" for m in both]
    pole_identity(both, statements, DS, mascot_width=widths,
                  statement_zoom=116 if lines <= 6 else (106 if lines <= 8 else 98))


# ── La slide « vagues » d'un pôle (NG 2026-08-30) ────────────────────────────
#: Provenance des cartes-titres copiées du deck des vagues (drapeau DD-35).
_WAVES_IMAGES = Path(__file__).parent.parent / "static" / "data" / "waves-images.json"
#: Rapport largeur/hauteur des cartes-titres (série 16:9 du deck des vagues) —
#: une propriété du média, pas un choix de mise en page (R4d).
_WAVE_CARD_RATIO = 16 / 9
#: Hauteur maximale d'une carte, en vh : ce qui reste sous le titre pour
#: l'image ET sa ligne de légende. Le levier de taille de cette slide.
_WAVE_STAGE_VH = 62
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
    jour (env local > collection.toml). URL de BASE : chaque carte y ajoute
    ``?marker=<id de vague>`` par ``page_url`` (streamtex ≥ 0.7.27, #42) et
    ouvre le deck DIRECTEMENT sur la vague — app et export HTML, dans la
    langue courante (``?lang=`` conservé)."""
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
    st_space("v", "3vh")
    url = _waves_deck_url(lang)
    # ONE flat grid — one cell per wave, on a single line. La carte prend 100 %
    # de sa cellule (NG 2026-08-30) : la largeur suit le NOMBRE de cartes et la
    # fenêtre — deux cartes ≈ la moitié chacune, une seule ≈ toute la largeur,
    # mobile = une colonne pleine largeur — et `media_stage` (R4d) borne chaque
    # cellule par la hauteur disponible, jamais un `vw` écrit en dur.
    with st_grid(cols=s.project.grids.balanced(len(waves)), gap="1vw",
                 cell_styles=s.project.containers.grid_cell_centered) as g:
        for w in waves:
            with g.cell(), st_block(s.project.containers.media_stage(_WAVE_CARD_RATIO,
                                                                     _WAVE_STAGE_VH)):
                # La clé du marqueur côté waves est l'id de la vague (stable,
                # indépendant du libellé traduit) : le lien marche en EN et FR.
                _wave_card(w, lang, page_url(url, marker=w["id"]), width="100%")
                strength = T(_WAVES_UI["strength"].get(w.get("strength"), {"en": "", "fr": ""}), lang)
                # Une seule ligne de légende, trois couleurs sémantiques du DS
                # (NG 2026-08-30) : la révolution en texte, la période en bleu
                # (cadrage), la solidité en teal (keyword) — jamais d'ambre ici,
                # l'accent focal unique de la slide reste au titre (R5).
                parts = [text(w["name"], lang)]
                if text(w["period"], lang):
                    parts += [" · ", (s.project.colors.primary, text(w["period"], lang))]
                if strength:
                    parts += [" · ", (s.project.colors.keyword, strength)]
                with st_zoom(180):
                    st_write(rs.wave_name, *parts, tag=t.div)


def _pole_banner(pole: dict, lang: str | None) -> None:
    """L'avertissement « aucune figure ne défend ce pôle », s'il existe."""
    for warning in warnings_for(pole["axis"]):
        if pole["pole"].get("abbr", {}).get("en", "") in warning:
            st_space("v", "1vh")
            with st_block(s.project.cards.amber):
                st_write(rs.banner, T(_UI["no_champion"], lang), tag=t.div)


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
        stance = T(_UI[("agrees" if isinstance(response, int) and response >= 3
                        else "disagrees") if response is not None else "no_answer"], lang)
        parts = [T(_UI["stance_line"], lang).format(statement=statement, name=f["name"],
                                                    stance=stance)]
        if isinstance(response, int):
            parts[0] += T(_UI["stance_score"], lang).format(response=response)
        parts[0] += T(_UI["points_toward" if r.get("direction") == "toward"
                          else "points_away"], lang).format(pole=pole_name)
        if r.get("anchor"):
            parts.append(T(_UI["evidence"], lang).format(anchor=r["anchor"]))
        if r.get("transposition"):
            parts.append(T(_UI["transposed"], lang).format(transposition=r["transposition"]))
        if r.get("confidence"):
            parts.append(T(_UI["confidence"], lang).format(confidence=r["confidence"]))
        out.append((T(_UI["why_pole"], lang).format(item=r["item"]), " ".join(parts)))
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
    who = ([(T(_UI["who"], lang).format(name=f["name"]), f["presentation"])]
           if f.get("presentation") else [])
    if f.get("epoch"):
        who.append((T(_UI["epoch"], lang), f["epoch"]))
    entries = who + _why_here(f, pole_name, lang) + [
               (T(_UI["name_dates"], lang).format(name=f["name"], dates=f.get("dates", "")),
                T(_UI["figure_meta"], lang).format(origin=f.get("origin", ""),
                                                   wave=f.get("wave", ""), score=f["score"])),
               (T(_UI["video"], lang),
                T(_UI["video_player"], lang)
                + T(_UI["video_talk" if (f.get("media") or {}).get("video_kind") == "talk"
                        else "video_live"], lang)
                + T(_UI["video_rules"], lang)),
               (ui("reference", lang), T(_UI["reference_text"], lang))]
    full = f["quote"].get("reference_full")
    if full and full != f["quote"].get("reference"):
        entries.append((T(_UI["full_reference"], lang), full))
    _header([T(_UI["before_us"], lang), (s.project.titles.keyword, pole_name)],
            T(_UI["figure_pole"], lang).format(name=f["name"], pole=pole_name), entries)
    if index == 0:
        _pole_banner(pole, lang)
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
                 T(_UI["figure_stance"], lang).format(
                     axis=text(pole["axis_name"], lang), pole=pole_name,
                     effect=_effect(pole, lang)), tag=t.div)
        st_space("v", "1vh")
        st_write(rs.quote, T(_UI["quote"], lang).format(quote=quote), tag=t.div)
        st_space("v", "0.6vh")
        st_write(rs.figure_ref,
                 citation_or(f["quote"].get("reference"),
                             *(f["quote"].get("citekeys") or [])), tag=t.div)


#: PLAFOND de zoom des cartes d'argument (NG 2026-08-30, porté à 250) — la
#: taille effective est min(plafond, palier mesuré) : les paliers viennent de
#: la GÉOMÉTRIE (badge triplé + grille 2+1 sous le pli à 1920×1080, mesuré au
#: rendu) et des longueurs réelles des titres du corpus (max FR par trio :
#: 94 à 133 caractères). Monter le plafond au-delà du palier ne change rien ;
#: pour gagner encore, il faut raccourcir les titres (hub) ou changer la
#: composition, pas le zoom.
_ARG_ZOOM_START = 240


def _fit_zoom(longest: int, steps: tuple[int, int], start: int = _ARG_ZOOM_START,
              drop: int = 35) -> int:
    """Le zoom qui tient : ``start`` jusqu'au premier seuil de longueur,
    puis deux crans de ``drop`` en dessous — un titre plus long prend plus
    de lignes, et les DEUX rangées doivent rester au-dessus du pli (mesuré
    au rendu 1920×1080, 2026-08-30 : une demi-largeur porte ~22 caractères
    par ligne à 200, ~30 à 160)."""
    if longest <= steps[0]:
        return start
    return start - drop if longest <= steps[1] else start - 2 * drop


def _arguments(pole: dict, lang: str | None) -> None:
    pole_name = text(pole["pole"], lang)
    # Attribution COURTE à l'écran (« Andrew Ng ») — la titulature complète
    # (« co-founder of Google Brain, professor at Stanford ») vit au tooltip.
    entries = [(text(a["title"], lang),
                " — ".join(x for x in (a.get("person"),
                                       text(a.get("text"), lang) or "") if x))
               for a in pole["arguments"]]
    entries.append((T(_UI["symmetry"], lang), T(_UI["symmetry_text"], lang)))
    entries.append((T(_UI["paraphrase"], lang), T(_UI["paraphrase_text"], lang)))
    _header([*TF(_UI["today_title"], lang), pole_name],
            T(_UI["today_tip"], lang).format(pole=pole_name), entries)
    st_space("v", "1vh")
    # Grille 2+1 (NG 2026-08-30) : rangée 1 = public policy | public statement,
    # rangée 2 = concrete case pleine largeur — trois colonnes faisaient trois
    # cartes étroites et la moitié de l'écran vide ; une longue ligne par
    # argument se lisait mal. L'ordre par NATURE est déterministe : le gel
    # choisit toujours trois natures différentes.
    order = {"policy": 0, "quote": 1, "case": 2, "historical": 2, "tradition": 2}
    args = sorted(pole["arguments"], key=lambda a: order.get(a["category"], 3))
    top, bottom = args[:2], args[2:]

    def _card(a: dict) -> None:
        # La ligne de source est le code de citation natif — carte complète
        # au survol — avec repli sur la chaîne du manifeste si la clé n'était
        # pas gelée.
        person_short = (a.get("person") or "").split(",")[0].strip() or None
        argument_card(a, DS, text(a["title"], lang), person=person_short,
                      badge_style=rs.nature_badge, person_style=rs.person,
                      nature=T(_NATURES.get(a["category"], {"en": a["category"] or ""}), lang),
                      source_html=citation_or(
                          a.get("reference") or a.get("citekey") or "",
                          *([a["citekey"]] if a.get("citekey") else [])))

    # Le zoom part de `_ARG_ZOOM_START` (200, NG) et redescend AUTOMATIQUEMENT
    # avec le titre le plus long de la rangée, pour que les DEUX rangées
    # tiennent au-dessus du pli (même mécanisme que la citation de `_figure`).
    # Le zoom s'applique DANS la cellule, jamais autour de la grille : les
    # planchers en px d'une grille suivent le zoom (R-zoom) et, doublés,
    # feraient retomber deux colonnes en une.
    # UN SEUL zoom pour les deux rangées (NG 2026-08-30 : même taille de
    # texte partout) — calé sur le titre le plus long des trois cartes ; le
    # badge triplé prend sa part du budget de hauteur (paliers resserrés).
    # Paliers calés sur le corpus (le plus long titre FR d'un trio va de 94 à
    # 133 caractères, mesuré au rendu 1920×1080) : ≤ 100 → 130, ≤ 115 → 120,
    # au-delà → 110 — puis le plafond `_ARG_ZOOM_START` s'applique.
    longest = max((len(text(a["title"], lang)) for a in args), default=0)
    zoom = min(_ARG_ZOOM_START, _fit_zoom(longest, (100, 115), start=130, drop=10))
    zoom_top = zoom
    with st_grid(cols=s.project.grids.balanced(len(top), min_px=340), gap="1.2vw",
                 grid_style=s.project.grids.stretch,
                 cell_styles=s.project.containers.grid_cell_top) as g:
        for a in top:
            with g.cell(), st_zoom(zoom_top):
                _card(a)
    if bottom:
        st_space("v", "1vh")
        zoom_bottom = zoom
        with st_grid(cols="1fr", grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_top) as g:
            for a in bottom:
                with g.cell(), st_zoom(zoom_bottom):
                    _card(a)


# ── La scène du débat (NG 2026-08-31) ────────────────────────────────────────
def _debate_stage(both: list[dict], lang: str | None) -> None:
    """Le moment-débat de l'axe, juste après les deux identités : la salle
    s'exprime PENDANT que l'écran rappelle la thématique (NG 2026-08-31).

    Trois colonnes — pôle accélérateur / VOXO / pôle ralentisseur. Chaque
    côté : ses deux mascottes, puis son énoncé SYNTHÉTIQUE en carte (nom du
    pôle en tête — ``pole.synthesis`` du gel, la phrase du sondage rapide).
    Au centre : Voxo, la modératrice au micro (NG 2026-08-31), à 70 % de sa
    taille d'intro dans ``bck_disc_debates_link`` (min(22vw, 46vh) × 0,7).
    Le titre nomme l'axe et les deux pôles ; le sous-titre, au corps du
    titre et en teal, porte la consigne « hands on — mic — tell us »."""
    a, d = (text(p["pole"], lang) for p in both)
    axis_name = text(both[0]["axis_name"], lang)
    label = T(_UI["faceoff_label"], lang).format(left=a, right=d)
    entries = [
        (T(_UI["stage_floor"][0], lang), T(_UI["stage_floor"][1], lang)),
        (T(_UI["stage_synthesis"][0], lang), T(_UI["stage_synthesis"][1], lang)),
        (T(_UI["stage_both"][0], lang), T(_UI["stage_both"][1], lang)),
    ]
    # Forme courte quand l'axe est homonyme d'un pôle (Trust, Centralisation,
    # Transhumanisme…) : « Trust — Trust / … » doublonne et prend deux lignes.
    title_key = "stage_title_short" if axis_name in (a, d) else "stage_title"
    _header([T(_UI[title_key], lang).format(axis=axis_name, a=a, d=d)],
            T(_UI["stage_tip_title"], lang), entries, label=label)
    st_write(rs.stage_subtitle, T(_UI["stage_subtitle"], lang), tag=t.div)
    st_space("v", "1vh")

    def _side(pole: dict) -> None:
        with st_grid(cols="1fr 1fr", gap="0.8vw",
                     cell_styles=s.project.containers.grid_cell_centered) as gg:
            for m in mascots(pole):
                with gg.cell():
                    st_image(s.project.cards.media_center,
                             width=f"min(9vw, {16 * _mascot_ratio(m['image']):.1f}vh)",
                             uri=m["image"],
                             alt=f"{m['mascot']} — mascot of the {m['label']} posture",
                             overlay=dd35_overlay())
                    st_write(s.project.body.mascot_name, m["mascot"], tag=t.div)
        st_space("v", "1vh")
        # L'énoncé synthétique va de 89 à 160 caractères selon le pôle et la
        # langue : le zoom suit la longueur RENDUE pour que la carte reste
        # au-dessus du pli (mesuré à 1920×1080 — même logique que _identity).
        # +20 % demandés (NG 2026-08-31), tempérés sur le palier le plus long :
        # à 130, le nom du pôle +30 % et Voxo pris, les 160 caractères FR de
        # l'Humanisme passaient deux lignes sous le pli.
        synth = text(pole["pole"].get("synthesis"), lang)
        with st_zoom(118 if len(synth) <= 100 else (108 if len(synth) <= 130 else 96)):
            with st_block(DS.cards.blue):
                # Le nom du pôle EN TÊTE DE CARTE (pas au-dessus des
                # mascottes : un stub st_block décalait la première cellule
                # de la grille de ~49 px et désalignait les deux intitulés).
                st_write(rs.stage_pole, text(pole["pole"], lang), tag=t.div)
                st_write(rs.stage_synth, synth, tag=t.div)

    with st_grid(cols="37% 26% 37%", gap="1.2vw",
                 cell_styles=s.project.containers.grid_cell_top) as g:
        with g.cell():
            _side(both[0])
        with g.cell():
            voxo = mascot("Voxo")
            st_image(s.project.cards.media_center, width="min(15.4vw, 32.2vh)",
                     uri=voxo["image"],
                     alt=f"{voxo['name']}, the moderator mascot, opening the floor",
                     overlay=dd35_overlay())
            st_write(s.project.body.mascot_name, voxo["name"], tag=t.div)
        with g.cell():
            _side(both[1])


# Retirée du rythme d'axe (NG 2026-08-31, décision 3A : l'axe se ferme sur
# les arguments du second pôle, « la mesure » est un geste d'orateur vers
# /present) — conservée pour réversibilité.
def _faceoff(both: list[dict], lang: str | None) -> None:
    left, right = (text(p["pole"], lang) for p in both)
    entries = [
        (T(_UI["where_room"], lang), T(_UI["where_room_text"], lang)),
        (T(_UI["reading"], lang), T(_UI["reading_text"], lang)),
        (T(_UI["codes"], lang), T(_UI["codes_text"], lang)),
        (T(_UI["three_moves"], lang), T(_UI["three_moves_text"], lang)),
    ]
    label = T(_UI["faceoff_label"], lang).format(left=left, right=right)
    _header([left, " ⇄ ", right], label, entries, label=label)
    st_space("v", s.project.spacing.title_gap)
    pole_faceoff(faceoff_sides(both, lang), DS)
    st_space("v", "2vh")
    # Le protocole, VISIBLE (NG 2026-08-13) : la slide-pivot du débat ne
    # doit plus dépendre du tooltip pour être comprise.
    st_write(rs.banner, T(_UI["protocol"], lang), tag=t.div)


def axis_slides(axis: str, lang: str | None = None) -> None:
    """Les sous-slides d'un axe, au rythme du débat (NG 2026-08-31).

    D'abord les deux identités — le rappel des questions de chaque pôle —
    puis la SCÈNE DU DÉBAT (la salle s'exprime avant d'avoir vu le
    matériau), et enfin le contenu, pôle par pôle : vagues (si le gel en
    porte), figures, arguments contemporains. Le face-à-face de fin d'axe
    est retiré (3A). Le deck est paginé et le présentateur n'ouvre que les
    axes clivants : le nombre de pages n'est pas un coût, la lisibilité en
    est un.
    """
    both = axis_poles(axis)
    # 1-2 : l'identité de chaque pôle — accélérateur d'abord.
    for i, pole in enumerate(both):
        pole_name = text(pole["pole"], lang)
        if i == 0:
            st_marker(pole_name)
        else:
            st_slide_break(marker_label=pole_name)
        with st_block(s.project.containers.page_fill_top):
            _identity(pole, lang)
    # 3 : la scène du débat — marqueur visible « A ⇄ B ».
    st_slide_break(marker_label=T(_UI["faceoff_label"], lang).format(
        left=text(both[0]["pole"], lang), right=text(both[1]["pole"], lang)))
    with st_block(s.project.containers.page_fill_top):
        _debate_stage(both, lang)
    # 4+ : le matériau, pôle par pôle, en marqueurs cachés — il se parcourt
    # (ou s'échantillonne) APRÈS le débat.
    for pole in both:
        parts = ([_waves] if pole.get("waves") else []) + \
            [(lambda p, lg, ff=f, i=i: _figure(p, ff, i, lg))
             for i, f in enumerate(pole["figures"])] + [_arguments]
        for part in parts:
            st_slide_break(marker_hidden=True,
                           config=SlideBreakConfig(mode=SlideBreakMode.FULL, space="30vh"))
            with st_block(s.project.containers.page_fill_top):
                part(pole, lang)
