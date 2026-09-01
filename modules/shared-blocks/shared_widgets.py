"""Shared widgets for the POSTAIR presentations.

Palette wrappers and the one widget that genuinely needs markup — the tooltip
itself is the native ``st_hover_tooltip`` from streamtex (>= 0.7.8). Blocks
never write markup themselves (design guideline, rule "stx-only"): when a
slide needs behaviour the style system cannot express, it comes from here.
"""

import json

import streamlit as st
from streamtex import st_hover_tooltip, st_html

from postair_pack.design_systems.postair_dark import (
    AMBER,
    CORAL,
    KEYWORD,
    MUTED,
    PRIMARY,
    TEXT,
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


def st_stage_code_input(key: str, placeholder: str = "") -> str:
    """A one-line free-text field the SPEAKER drives (NG 2026-08-21).

    Compagnon du sélecteur : là où ``st_stage_selector`` choisit parmi des
    valeurs déclarées, ce champ accepte une valeur qui n'existe pas encore —
    un code de campagne créé le matin même. Même règle que le sélecteur :
    la clé est passée par l'appelant et doit être STABLE (une clé engendrée
    changerait à chaque rerun et viderait le champ sous la main de l'orateur).
    Le retour est débarrassé de TOUS ses blancs : un code se colle à une URL.
    """
    value = st.text_input(" ", key=key, placeholder=placeholder,
                          label_visibility="collapsed")
    return "".join((value or "").split())


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


def st_countdown(minutes: int, label: str = "Back in", height: int = 340,
                 scale: float = 1.0) -> None:
    """A live break countdown, readable from the back of an amphitheatre.

    ``scale`` is THE size lever (NG 2026-08-30): the widget is an iframe
    (``st_html`` with a height) whose text is sized in ``vw`` of the iframe —
    an enclosing ``st_zoom`` is therefore inert on it (the browser divides the
    iframe's layout width by the zoom, and the ``vw`` sizes cancel it out
    exactly — the R-zoom rule, iframe edition). ``height`` only sizes the
    frame: give it enough room for the scaled digits, nothing more.

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
  <div style="font-size:{3.2 * scale:.2f}vw;color:#7AB8F5;font-weight:700;">{label}</div>
  <div id="stx-countdown"
       style="font-size:{14 * scale:.2f}vw;font-weight:900;letter-spacing:0.04em;line-height:1;
              color:#F39C12;">--:--</div>
  <div id="stx-countdown-at" style="font-size:{2.6 * scale:.2f}vw;color:#95A5A6;"></div>
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


def st_countdown_rack(steps: list[tuple[str, float]], mode: str = "chain",
                      *, start_label: str = "▶ Start", ends_at_label: str = "ends at",
                      height: int = 520, scale: float = 1.0) -> None:
    """Une rangée de comptes à rebours — en chaîne ou en parallèle.

    Décision NG (planche chrono, 2026-09-01 : ``archi=p1 moteur=p1
    commande=p1 habillage=p1``) — la généralisation de ``st_countdown`` :

    - ``steps`` : liste de ``(étiquette, minutes)`` — étiquettes déjà
      RÉSOLUES par le bloc appelant (feuilles ``{en, fr}``, règle R-i18n) ;
      les minutes acceptent les fractions (``0.5`` = 30 s, utile en
      répétition). La liste vit dans le TUNING du bloc appelant, jamais ici.
    - ``mode`` : ``"chain"`` — le clic Start lance le premier, chaque zéro
      lance le suivant ; ``"parallel"`` — le clic lance tout.
    - Le bouton **Start est commun aux deux modes** (leçon inverse du chrono
      de pause : un exercice minuté ne court jamais pendant la consigne) ;
      un **↺ Reset** discret apparaît en coin une fois lancé — le faux
      départ se rattrape devant la salle.
    - UN SEUL fragment ``st_html`` porte toute la rangée : la coordination
      (l'enchaînement, le start commun) vit dans un unique script — deux
      iframes ne se parlent pas. Même statut d'exception que
      ``st_countdown``, au même endroit sanctionné ; identique dans
      l'application et dans l'export HTML statique, zéro rerun.
    - États par carte (le vocabulaire appris à la pause) : à venir = gris
      muted · en cours = ambre · fini = corail en parallèle, ✓ teal en
      chaîne (le suivant a pris l'ambre). Chaque carte affiche son heure de
      fin murale au lancement (en chaîne : heures CUMULÉES — ce que la
      salle consulte vraiment).
    - ``scale`` est LE levier de taille (R-zoom, édition iframe : un
      ``st_zoom`` englobant est inerte — tailles en ``vw`` de l'iframe) ;
      ``height`` ne fait que loger la rangée. Au-delà de ~5 durées, les
      chiffres rapetrissent d'eux-mêmes (largeur partagée) — con documenté
      sur la planche.
    - Aucun son (R7) — la couleur fait l'annonce.
    """
    if mode not in ("chain", "parallel"):
        raise ValueError(f"mode inconnu : {mode!r} — « chain » ou « parallel »")
    if not steps:
        raise ValueError("st_countdown_rack : la liste de durées est vide")
    # Les secondes par étape, gelées côté Python ; le script ne calcule que
    # les instants. Étiquettes échappées par json.dumps (guillemets, accents).
    payload = json.dumps([[label, max(1, round(minutes * 60))]
                          for label, minutes in steps])
    n = len(steps)
    digit_vw = min(9.0, 30.0 / n) * scale
    label_vw = min(2.4, 8.0 / n) * scale
    at_vw = min(1.6, 5.5 / n) * scale
    btn_vw = 2.2 * scale
    html = f"""
<div style="position:relative;display:flex;flex-direction:column;align-items:center;
            justify-content:center;gap:2.5vh;height:100%;
            font-family:'Source Sans Pro',sans-serif;color:{TEXT};">
  <button id="cdr-start" style="font-size:{btn_vw:.2f}vw;font-weight:700;
          color:{AMBER};background:transparent;border:0.18vw solid {AMBER};
          border-radius:0.8vw;padding:0.35em 1.6em;cursor:pointer;">{start_label}</button>
  <button id="cdr-reset" title="reset" style="position:absolute;top:0.8vh;right:0.6vw;
          display:none;font-size:{1.4 * scale:.2f}vw;color:{MUTED};background:transparent;
          border:none;cursor:pointer;">↺</button>
  <div id="cdr-row" style="display:flex;gap:1.2vw;width:96%;justify-content:center;">
  </div>
</div>
<script>
(function () {{
  var STEPS = {payload};
  var MODE = {json.dumps(mode)};
  var row = document.getElementById('cdr-row');
  var startBtn = document.getElementById('cdr-start');
  var resetBtn = document.getElementById('cdr-reset');
  var cards = STEPS.map(function (s, i) {{
    var card = document.createElement('div');
    card.style.cssText = 'flex:1 1 0;min-width:0;text-align:center;padding:2vh 0.5vw;' +
      'background:rgba(122,184,245,0.08);border:0.12vw solid rgba(122,184,245,0.25);' +
      'border-radius:0.9vw;';
    card.innerHTML =
      '<div style="font-size:{label_vw:.2f}vw;font-weight:700;color:{PRIMARY};">' + s[0] + '</div>' +
      '<div class="cdr-digits" style="font-size:{digit_vw:.2f}vw;font-weight:900;' +
      'letter-spacing:0.04em;line-height:1.15;color:{MUTED};"></div>' +
      '<div class="cdr-at" style="font-size:{at_vw:.2f}vw;color:{MUTED};">&nbsp;</div>';
    row.appendChild(card);
    return card;
  }});
  var timer = null, startAt = null, endAt = null;
  function fmt(sec) {{
    var m = Math.floor(sec / 60), s = sec % 60;
    return String(m).padStart(2, '0') + ':' + String(s).padStart(2, '0');
  }}
  function paint() {{
    var now = Date.now();
    var running = startAt !== null;
    STEPS.forEach(function (s, i) {{
      var digits = cards[i].querySelector('.cdr-digits');
      var at = cards[i].querySelector('.cdr-at');
      if (!running) {{
        digits.textContent = fmt(s[1]);
        digits.style.color = '{MUTED}';
        at.innerHTML = '&nbsp;';
        return;
      }}
      var left = Math.max(0, Math.ceil((endAt[i] - now) / 1000));
      if (now < startAt[i]) {{           // à venir (chaîne)
        digits.textContent = fmt(s[1]);
        digits.style.color = '{MUTED}';
      }} else if (now < endAt[i]) {{     // en cours
        digits.textContent = fmt(left);
        digits.style.color = '{AMBER}';
      }} else if (MODE === 'chain') {{   // fini, la chaîne a avancé
        digits.textContent = '✓ 00:00';
        digits.style.color = '{KEYWORD}';
      }} else {{                          // fini, parallèle : le corail de la pause
        digits.textContent = '00:00';
        digits.style.color = '{CORAL}';
      }}
    }});
  }}
  function start() {{
    var t0 = Date.now();
    startAt = []; endAt = [];
    var cursor = t0;
    STEPS.forEach(function (s) {{
      var from = (MODE === 'chain') ? cursor : t0;
      startAt.push(from);
      endAt.push(from + s[1] * 1000);
      cursor = from + s[1] * 1000;
    }});
    STEPS.forEach(function (s, i) {{
      var back = new Date(endAt[i]);
      cards[i].querySelector('.cdr-at').textContent = '{ends_at_label} ' +
        String(back.getHours()).padStart(2, '0') + ':' +
        String(back.getMinutes()).padStart(2, '0');
    }});
    startBtn.style.display = 'none';
    resetBtn.style.display = 'block';
    timer = setInterval(paint, 250);
    paint();
  }}
  function reset() {{
    if (timer) clearInterval(timer);
    timer = null; startAt = null; endAt = null;
    startBtn.style.display = 'block';
    resetBtn.style.display = 'none';
    paint();
  }}
  startBtn.addEventListener('click', start);
  resetBtn.addEventListener('click', reset);
  paint();
}})();
</script>
"""
    st_html(html, height=height)


def st_poster_video(video_url: str, poster_uri: str, *, alt: str = "",
                    width: str = "min(38vw, 66vh)", ai_marked: bool = False,
                    ai_label: str = "AI") -> None:
    """Un portrait qui DEVIENT la vidéo, dans le même cadre (NG 2026-08-24).

    Le portrait n'est pas remplacé par un lecteur noir : il est le ``poster``
    du lecteur. Un clic sur ▶ joue la vidéo À LA PLACE de la photo, le bouton
    plein écran natif fonctionne, et en sortir ramène la lecture dans le
    cadre — c'est le comportement natif de ``<video controls>``, aucun état,
    aucun rerun, aucun onglet (l'ancien ``link=`` ouvrait un onglet et faisait
    quitter le deck en pleine séance).

    ``preload="none"`` est le cœur du contrat de STREAMING : rien n'est
    téléchargé tant que l'orateur ne joue pas. Le CDN répond
    ``accept-ranges: bytes``, donc le navigateur ne tire que les octets qu'il
    lit — la version HD (~12 Mo) se projette sans être embarquée dans
    l'image, et une figure qu'on n'ouvre pas ne coûte rien.

    ``poster_uri`` est le chemin SERVI du portrait (déjà matérialisé dans
    l'image : aucun appel réseau pour la photo, seule la vidéo est distante).

    La pastille DD-35 est rendue ici, en HAUT à droite : le bord bas
    appartient aux contrôles natifs du lecteur. 44 des 54 vidéos sont des
    portraits parlants synthétiques — la marque n'est pas optionnelle.
    """
    chip = (
        f'<span style="position:absolute; top:0.6em; right:0.6em; z-index:10; '
        f'pointer-events:none; background:rgba(113,113,122,0.35); color:#FFF; '
        f'border-radius:999px; padding:0.1em 0.7em; font-weight:700; '
        f'text-transform:uppercase; letter-spacing:0.08em; '
        f'font-size:clamp(11px,1.05vw,22px); line-height:1.7;">'
        f'&#10022; {ai_label}</span>'
    ) if ai_marked else ""
    st_html(
        f'<div style="position:relative; width:{width}; margin:0 auto;">'
        f'<video controls preload="none" playsinline poster="{poster_uri}" '
        f'style="width:100%; height:auto; display:block; border-radius:12px;" '
        f'aria-label="{alt}">'
        f'<source src="{video_url}" type="video/mp4">'
        f'</video>{chip}</div>'
    )
