"""Shared widgets for the POSTAIR presentations.

Palette wrappers and the one widget that genuinely needs markup — the tooltip
itself is the native ``st_hover_tooltip`` from streamtex (>= 0.7.8). Blocks
never write markup themselves (design guideline, rule "stx-only"): when a
slide needs behaviour the style system cannot express, it comes from here.
"""

import json
import math
import re

import streamlit as st
from streamtex import st_hover_tooltip, st_html

from postair_pack.design_systems.postair_dark import (
    AMBER,
    CORAL,
    CRITICAL,
    KEYWORD,
    MUTED,
    PRIMARY,
    SUCCESS,
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


def st_countdown_rack(s, steps: list[tuple[str, float]], mode: str = "chain",
                      *, key: str, grid: tuple[int, int] | None = None,
                      rack_vh: float = 62,
                      ends_at_label: str = "ends at",
                      start_all_label: str = "▶ Start", reset_all_label: str = "↺ Reset",
                      height: int | None = None, scale: float = 1.0) -> None:
    """Une rangée de comptes à rebours sur une VRAIE grille streamtex.

    Décisions NG (planche chrono ``archi=p1 moteur=p1 commande=p1
    habillage=p1`` puis retouches du 2026-09-01) :

    - **Grille streamtex** : les cartes sont des ``st_block(cards.blue)``
      dans un ``st_grid`` ; chaque carte contient UN fragment-cadran
      (étiquette, chiffres, heure de fin, boutons). ``s`` est l'objet
      Styles du module appelant (précédent : ``build_next_module_slide``).
      Depuis la maximisation (NG 2026-09-02, deux passes) : l'étiquette vit
      DANS le cadran pour être zoomée comme le reste, et LES CHIFFRES
      priment — budgets verticaux ≈ 100 % du cadran : étiquette 11 vh +
      chiffres 66 vh + un PIED commun (boutons 13 vh, heure de fin en ligne
      à leur droite) ; répartis en ``space-evenly``, centrés dans les deux
      axes, étiquette longue coupée en ellipse plutôt que débordante.
    - **Boutons PAR carte** : ▶ démarre/reprend · ⏸ met en pause · ↺ remet
      la carte à sa durée pleine (à l'arrêt). Comportements par mode :
      *chain* — UNE seule carte court à la fois (▶ sur une carte met l'autre
      en pause) et le zéro d'une carte lance la première carte suivante non
      finie ; *parallel* — les cartes sont indépendantes. Les boutons
      globaux restent : ▶ Start lance la première carte non finie (chain) ou
      toutes (parallel) ; ↺ Reset remet toute la rangée.
    - **Zéro** : UNE ligne — la coche verte puis la durée INITIALE en rouge
      translucide (``✓ 01:00``), identique dans les deux modes (retouche NG
      2026-09-01, remplace le teal/corail de la v1).
    - **Coordination** : chaque cadran est sa propre iframe ``srcdoc``
      (même origine) dans l'application, et du HTML inliné dans l'export —
      dans les deux cas ``window.parent`` est le MÊME document pour toutes
      les cartes d'une page : un petit bus ``__cdrBus`` y vit, indexé par
      ``key`` (OBLIGATOIRE et unique par rangée — l'export met toutes les
      slides dans un seul document, deux rangées sans clé se marcheraient
      dessus).
    - ``steps`` : liste de ``(étiquette RÉSOLUE, minutes)`` — fractions
      permises (``0.5`` = 30 s) ; la liste vit dans le TUNING du bloc
      appelant. Heure de fin murale par carte pendant qu'elle court
      (``now + restant`` — la pause la recalcule à la reprise).
    - **Grille N×P** (spécification NG 2026-09-02, remplace ``balanced``) :
      ``grid=(lignes, colonnes)`` fixe la géométrie ; les cartes remplissent
      de gauche à droite puis de haut en bas, les cases restantes sont des
      trous assumés. ``grid=None`` (défaut) = la grille COMPACTE minimale à
      cellules maximales : ``colonnes = ⌈√k⌉``, ``lignes = ⌈k/colonnes⌉``
      (4 → 2×2, 3 → 2×2 avec un trou, 5 → 2×3). ``lignes×colonnes < k`` =
      erreur bruyante.
    - **Tout se redimensionne** (correctif du débordement constaté sur le
      2×2 d'opening, 2026-09-02) : chaque taille du cadran est un clamp CSS
      ``min(X vw, Y vh)`` de SON iframe — bornée par la largeur de la
      cellule ET par la hauteur du cadre, quelle que soit la géométrie ;
      les boutons sont épinglés en pied de cadran, l'overflow est caché
      (plus d'ascenseur).
    - **Les trois leviers, orthogonaux** (ligne NG ``chronoh vertical=p1
      leviers=p1``, 2026-09-02) : ``grid`` = la géométrie · ``rack_vh`` =
      la place verticale TOTALE de la matrice, en vh de la fenêtre (défaut
      62 — sous le titre et les boutons globaux), partagée entre les
      lignes : chaque cadran se dimensionne LUI-MÊME à l'affichage et au
      redimensionnement (``window.frameElement``, même origine — vérifié
      doc Streamlit ; en export, hauteur vh CSS directe) · ``scale`` = le
      zoom fin du contenu de chaque cellule (R-zoom édition iframe).
      ``height`` (px) est l'override EXPERT : posé, il fige le cadran et
      désactive l'auto-mesure. La largeur découle de P (les colonnes se
      partagent le slide).
    - **Identifiants DOM scopés par rangée et par carte** : l'export inline
      toutes les slides dans UN document — des ids nus (``cdr-digits``)
      accrocheraient tous les scripts à la première carte ; chaque fragment
      cherche donc ses éléments SOUS sa racine ``cdr-<key>-…``. Aucun son
      (R7) — la couleur fait l'annonce.
    """
    if mode not in ("chain", "parallel"):
        raise ValueError(f"mode inconnu : {mode!r} — « chain » ou « parallel »")
    if not steps:
        raise ValueError("st_countdown_rack : la liste de durées est vide")
    if not key or not key.strip():
        raise ValueError("st_countdown_rack : `key` est obligatoire et unique "
                         "par rangée (l'export inline toutes les slides dans "
                         "un seul document)")
    from streamtex import st_block, st_grid

    rack_id = json.dumps(key)
    n = len(steps)
    # La géométrie : explicite, ou compacte minimale à cellules maximales.
    if grid is None:
        cols = math.ceil(math.sqrt(n))
        rows = math.ceil(n / cols)
    else:
        rows, cols = grid
        if rows < 1 or cols < 1 or rows * cols < n:
            raise ValueError(
                f"st_countdown_rack : grille {rows}×{cols} trop petite pour "
                f"{n} compteur(s) — lignes×colonnes doit couvrir la liste")
    # Le budget vertical : ``rack_vh`` (% de fenêtre) partagé entre les
    # lignes, moins les rembourrages de carte (≈ 4 vh par ligne — depuis la
    # maximisation NG 2026-09-02, l'étiquette vit DANS le cadran).
    # ``height`` posé = override expert : cadran figé.
    dial_vh = max(12.0, rack_vh / rows - 4.0)
    fixed_px = height is not None
    if height is None:
        # Première peinture avant l'auto-mesure (référence fenêtre 1080 px) ;
        # le script du cadran se recale aussitôt sur la fenêtre réelle.
        height = int(round(dial_vh * 10.8))
    secs = [max(1, round(minutes * 60)) for _label, minutes in steps]
    # Racine DOM unique par rangée : l'export inline tout dans UN document.
    dom = "cdr-" + re.sub(r"[^a-zA-Z0-9_-]", "-", key)

    #: Le prélude commun de chaque script : le bus sur le document parent —
    #: en app, le parent des iframes srcdoc ; en export, window lui-même.
    bus_js = f"""
  var P; try {{ P = window.parent || window; }} catch (e) {{ P = window; }}
  var bus = P.__cdrBus = P.__cdrBus || {{}};
  var rack = bus[{rack_id}] = bus[{rack_id}] || {{cards: {{}}, mode: {json.dumps(mode)}, n: {n}}};
"""

    # ── Les boutons globaux — un petit fragment au-dessus de la grille ──────
    st_html(f"""
<div id="{dom}-all" style="display:flex;gap:1.2vw;justify-content:center;align-items:center;
            height:100%;font-family:'Source Sans Pro',sans-serif;">
  <button class="cdr-all-start" style="font-size:{2.0 * scale:.2f}vw;font-weight:700;
          color:{AMBER};background:transparent;border:0.16vw solid {AMBER};
          border-radius:0.7vw;padding:0.3em 1.4em;cursor:pointer;">{start_all_label}</button>
  <button class="cdr-all-reset" style="font-size:{1.6 * scale:.2f}vw;font-weight:700;
          color:{MUTED};background:transparent;border:0.12vw solid {MUTED};
          border-radius:0.7vw;padding:0.3em 1.1em;cursor:pointer;">{reset_all_label}</button>
</div>
<script>
(function () {{
{bus_js}
  var root = document.getElementById('{dom}-all');
  if (window.frameElement) {{
    document.documentElement.style.overflow = 'hidden';
    document.body.style.overflow = 'hidden';
  }}
  root.querySelector('.cdr-all-start').addEventListener('click', function () {{
    var ids = Object.keys(rack.cards).sort(function (a, b) {{ return a - b; }});
    if (rack.mode === 'parallel') {{
      ids.forEach(function (i) {{ if (!rack.cards[i].isDone()) rack.cards[i].start(); }});
    }} else {{
      for (var k = 0; k < ids.length; k++) {{
        if (!rack.cards[ids[k]].isDone()) {{ rack.cards[ids[k]].start(); break; }}
      }}
    }}
  }});
  root.querySelector('.cdr-all-reset').addEventListener('click', function () {{
    Object.keys(rack.cards).forEach(function (i) {{ rack.cards[i].reset(); }});
  }});
}})();
</script>
""", height=int(72 * scale))

    # ── La grille streamtex N×P : remplissage gauche→droite, haut→bas ───────
    # ``repeat(cols, minmax(0, 1fr))`` : P colonnes exactes ; le placement
    # automatique de CSS grid remplit dans l'ordre de la liste, les cases
    # restantes restent vides (trous assumés — spécification NG 2026-09-02).
    with st_grid(cols=f"repeat({cols}, minmax(0, 1fr))", gap="1.2vw",
                 grid_style=s.project.grids.stretch,
                 cell_styles=s.project.containers.grid_cell_centered) as g:
        for i, (label, _minutes) in enumerate(steps):
            with g.cell(), st_block(s.project.cards.blue):
                # MAXIMISATION (NG 2026-09-02) : l'étiquette vit DANS le
                # cadran et tout le contenu remplit la cellule — chaque
                # taille est un clamp min(vw, vh) de l'iframe dont les
                # budgets verticaux totalisent ~100 % du cadran (étiquette
                # 13 + chiffres 48 + heure 9 + boutons 15 + air), répartis
                # en space-evenly : plein sur l'axe contraignant, centré
                # dans les deux axes, débordement impossible (overflow
                # caché en ceinture).
                st_html(f"""
<div id="{dom}-c{i}" style="display:flex;flex-direction:column;align-items:center;
            justify-content:space-evenly;height:100%;padding:0.5vh 0;box-sizing:border-box;
            overflow:hidden;font-family:'Source Sans Pro',sans-serif;color:{TEXT};">
  <div class="cdr-label" style="font-size:min({8 * scale:.2f}vw, {10 * scale:.2f}vh);
       font-weight:700;line-height:1.1;color:{TEXT};text-align:center;white-space:nowrap;
       max-width:96%;overflow:hidden;text-overflow:ellipsis;">{label}</div>
  <div class="cdr-digits" style="font-size:min({32 * scale:.2f}vw, {66 * scale:.2f}vh);
       font-weight:900;letter-spacing:0.04em;line-height:1.0;color:{MUTED};
       white-space:nowrap;"></div>
  <div style="display:flex;align-items:center;gap:min(2vw, 4vh);">
    <button class="cdr-go" style="font-size:min({6.5 * scale:.2f}vw, {12 * scale:.2f}vh);
            color:{AMBER};background:transparent;border:min(0.35vw, 0.8vh) solid {AMBER};
            border-radius:1.2vw;padding:0.1em 0.9em;cursor:pointer;">▶</button>
    <button class="cdr-halt" style="font-size:min({6.5 * scale:.2f}vw, {12 * scale:.2f}vh);
            color:{PRIMARY};background:transparent;border:min(0.35vw, 0.8vh) solid {PRIMARY};
            border-radius:1.2vw;padding:0.1em 0.9em;cursor:pointer;">⏸</button>
    <button class="cdr-zero" style="font-size:min({6.5 * scale:.2f}vw, {12 * scale:.2f}vh);
            color:{MUTED};background:transparent;border:min(0.35vw, 0.8vh) solid {MUTED};
            border-radius:1.2vw;padding:0.1em 0.9em;cursor:pointer;">↺</button>
    <span class="cdr-at" style="font-size:min({4.5 * scale:.2f}vw, {8 * scale:.2f}vh);
          color:{MUTED};white-space:nowrap;">&nbsp;</span>
  </div>
</div>
<script>
(function () {{
{bus_js}
  var IDX = {i}, TOTAL = {secs[i]};
  var root = document.getElementById('{dom}-c{i}');
  var digits = root.querySelector('.cdr-digits');
  var at = root.querySelector('.cdr-at');
  var remaining = TOTAL, endAt = null, timer = null;
  // Auto-dimensionnement (rack_vh, ligne NG chronoh vertical=p1) : le cadran
  // pose SA hauteur = DIAL_VH % de la fenêtre parente — iframe même origine
  // en app (window.frameElement), hauteur vh CSS directe en export.
  // En iframe, le document lui-même ne défile JAMAIS (les ascenseurs blancs,
  // capture NG 2026-09-02) — posé en JS pour rester SCOPÉ à l'app : en
  // export inliné, la page garde son défilement.
  if (window.frameElement) {{
    document.documentElement.style.overflow = 'hidden';
    document.body.style.overflow = 'hidden';
  }}
  var FIXED = {1 if fixed_px else 0}, DIAL_VH = {dial_vh:.2f};
  function fit() {{
    try {{
      var fe = window.frameElement;
      if (fe) {{ fe.style.height = Math.round(P.innerHeight * DIAL_VH / 100) + 'px'; }}
      else {{ root.style.height = DIAL_VH + 'vh'; }}
    }} catch (e) {{}}
  }}
  if (!FIXED) {{ fit(); try {{ P.addEventListener('resize', fit); }} catch (e) {{}} }}
  function fmt(sec) {{
    var m = Math.floor(sec / 60), s2 = Math.floor(sec) % 60;
    return String(m).padStart(2, '0') + ':' + String(s2).padStart(2, '0');
  }}
  function isDone() {{ return remaining <= 0; }}
  function paint() {{
    if (isDone()) {{
      // UNE ligne : la coche verte + la durée INITIALE en rouge translucide.
      digits.innerHTML = '<span style="color:{SUCCESS};">✓</span> ' +
        '<span style="color:{CRITICAL};opacity:0.45;">' + fmt(TOTAL) + '</span>';
      at.innerHTML = '&nbsp;';
      return;
    }}
    digits.textContent = fmt(Math.ceil(remaining));
    digits.style.color = (endAt !== null) ? '{AMBER}' : '{MUTED}';
  }}
  function tick() {{
    if (endAt === null) return;
    remaining = (endAt - Date.now()) / 1000;
    if (remaining <= 0) {{
      remaining = 0; endAt = null;
      clearInterval(timer); timer = null;
      paint();
      if (rack.mode === 'chain') {{
        var ids = Object.keys(rack.cards).map(Number).sort(function (a, b) {{ return a - b; }});
        for (var k = 0; k < ids.length; k++) {{
          if (ids[k] > IDX && !rack.cards[ids[k]].isDone()) {{
            rack.cards[ids[k]].start(); break;
          }}
        }}
      }}
      return;
    }}
    paint();
  }}
  function start() {{
    if (isDone() || endAt !== null) return;
    if (rack.mode === 'chain') {{
      // Une seule carte court : ▶ ici met les autres en pause.
      Object.keys(rack.cards).forEach(function (j) {{
        if (Number(j) !== IDX) rack.cards[j].pause();
      }});
    }}
    endAt = Date.now() + remaining * 1000;
    var back = new Date(endAt);
    at.textContent = '{ends_at_label} ' +
      String(back.getHours()).padStart(2, '0') + ':' +
      String(back.getMinutes()).padStart(2, '0');
    timer = setInterval(tick, 250);
    paint();
  }}
  function pause() {{
    if (endAt === null) return;
    remaining = Math.max(0, (endAt - Date.now()) / 1000);
    endAt = null;
    if (timer) {{ clearInterval(timer); timer = null; }}
    at.innerHTML = '&nbsp;';
    paint();
  }}
  function reset() {{
    if (timer) {{ clearInterval(timer); timer = null; }}
    remaining = TOTAL; endAt = null;
    at.innerHTML = '&nbsp;';
    paint();
  }}
  rack.cards[IDX] = {{start: start, pause: pause, reset: reset, isDone: isDone}};
  root.querySelector('.cdr-go').addEventListener('click', start);
  root.querySelector('.cdr-halt').addEventListener('click', pause);
  root.querySelector('.cdr-zero').addEventListener('click', reset);
  paint();
}})();
</script>
""", height=height)

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
