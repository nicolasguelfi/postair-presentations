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


#: Les timbres d'alarme du rack — SYNTHÉTISÉS en WebAudio (oscillateurs +
#: enveloppes), jamais des fichiers : aucun média dans git, et l'amphi est
#: hors réseau — un son qui dépend d'un octet distant est un son muet.
#: Liste blanche : elle borne ce qui descend dans le JS (garde d'injection).
_ALARM_SOUNDS = ("bell", "beep", "chime", "gong")


def st_countdown_rack(s, steps: list[tuple], mode: str = "chain",
                      *, key: str, grid: tuple[int, int] | None = None,
                      rack_vh: float = 62,
                      ends_at_label: str = "ends at",
                      start_all_label: str = "▶ Start", reset_all_label: str = "↺ Reset",
                      height: int | None = None, scale: float = 1.0,
                      alarm: str | None = None, alarm_volume: float = 0.6,
                      alarm_muted: bool = True,
                      alarm_duration: float | None = None) -> None:
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
    - **Zéro** : la durée INITIALE en rouge translucide, même nombre de
      caractères que les autres états — identique dans les deux modes, la
      couleur seule porte l'accompli (ligne NG ``chronocheck zero=p1``,
      2026-09-02 : la coche verte essayée débordait la ligne maximisée).
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
      cherche donc ses éléments SOUS sa racine ``cdr-<key>-…``. **Silence
      par défaut, alarme opt-in** (NG 2026-09-02) — la couleur porte
      l'accompli, ``alarm=`` y ajoute un timbre.
    - **Alarme (NG 2026-09-02)** : opt-in, silence par défaut ; timbres
      SYNTHÉTISÉS en WebAudio (``bell``/``beep``/``chime``/``gong`` — aucun
      média dans git, l'amphi est hors réseau) ; ``alarm_volume`` 0–1
      perceptif ; 3ᵉ élément optionnel d'un pas = surcharge par carte
      (timbre, ``"off"``, ou ``{"alarm": …, "volume": …}``) ; le navigateur
      ne débloque l'audio qu'après un geste — chaque clic sur le rack arme
      le contexte (unique, sur le document parent), le relais de chaîne
      hérite du déblocage. Sans alarme, la sortie HTML est BYTE-IDENTIQUE à
      l'existant (contrat baseline i18n).
    - **Sourdine + 🔔 (NG 2026-09-03, QCM puis précision)** : un rack ALARMÉ
      démarre EN SOURDINE (``alarm_muted=True`` par défaut) et CHAQUE carte
      alarmée porte sa cloche 🔔/🔕 à côté de ses boutons ▶ ⏸ ↺ — clic =
      armer/couper CETTE carte, choix MÉMORISÉ par carte (localStorage du
      parent, clé ``cdr-alarm-muted-<key>-<i>``, survit aux reruns et au
      rechargement). La cloche GLOBALE à côté de ▶ Start / ↺ Reset suit la
      même logique que ces boutons : elle agit sur TOUTES les cartes alarmées
      (armer s'il en reste une en sourdine, sinon tout couper) ; son glyphe
      dit « tout armé » 🔔 / « pas tout » 🔕. Armer (local ou global) joue un
      APERÇU bref du timbre : le geste confirme le son ET débloque l'autoplay.
    - **Durée d'alarme (NG 2026-09-03)** : ``alarm_duration`` (secondes,
      ]0, 60], ``None`` = un seul motif — le défaut) fait RÉPÉTER le motif du
      timbre jusqu'à couvrir la durée puis coupe proprement ; surcharge par
      pas via ``{"alarm": …, "volume": …, "duration": …}``. Les aperçus
      d'armement restent courts (un motif).
    - **Valeur ÉDITABLE (NG 2026-09-03)** : double-clic sur les chiffres —
      « 40 » = 40 min, « 40:30 » = 40 min 30 s ; Entrée (ou clic ailleurs)
      applique, Échap annule ; un chrono en course repart de la nouvelle
      valeur, un chrono fini REVIT ; ``TOTAL`` ne change pas — ↺ revient
      toujours à la durée d'origine du pas.
    """
    if mode not in ("chain", "parallel"):
        raise ValueError(f"mode inconnu : {mode!r} — « chain » ou « parallel »")
    if not steps:
        raise ValueError("st_countdown_rack : la liste de durées est vide")
    if not key or not key.strip():
        raise ValueError("st_countdown_rack : `key` est obligatoire et unique "
                         "par rangée (l'export inline toutes les slides dans "
                         "un seul document)")
    # ── Alarme (NG 2026-09-02) : tout se valide ICI, AVANT toute
    # interpolation — liste blanche + bornes numériques, puis json.dumps :
    # rien de textuel libre ne descend jamais dans le JS des fragments.
    if alarm is not None and alarm != "off" and alarm not in _ALARM_SOUNDS:
        raise ValueError(
            f"st_countdown_rack : timbre inconnu {alarm!r} — "
            f"{', '.join(_ALARM_SOUNDS)}, « off » ou None")
    if not isinstance(alarm_volume, (int, float)) or not 0.0 <= alarm_volume <= 1.0:
        raise ValueError(
            f"st_countdown_rack : alarm_volume {alarm_volume!r} hors [0, 1]")
    if alarm_duration is not None and (
            not isinstance(alarm_duration, (int, float))
            or not 0 < alarm_duration <= 60):
        raise ValueError(
            f"st_countdown_rack : alarm_duration {alarm_duration!r} hors "
            f"]0, 60] secondes (None = un seul motif du timbre)")
    global_sound = None if alarm in (None, "off") else alarm

    def _resolve_alarm(spec, i):
        """Le réglage RÉSOLU d'une carte : {"sound", "vol"[, "dur"]} ou None.

        Le 3ᵉ élément d'un pas surcharge le global — la config vit à CÔTÉ de
        la durée dans le TUNING de l'appelant et survit aux réordonnancements
        (retenu contre un dict indexé, désynchronisable). Erreur BRUYANTE sur
        toute forme inattendue : un réglage silencieusement ignoré sonnerait
        (ou se tairait) en séance, le pire moment pour le découvrir.
        """
        sound, vol = global_sound, float(alarm_volume)
        dur = float(alarm_duration) if alarm_duration is not None else None
        if spec is None:
            pass
        elif isinstance(spec, str):
            if spec != "off" and spec not in _ALARM_SOUNDS:
                raise ValueError(
                    f"st_countdown_rack : pas #{i}, timbre inconnu {spec!r} — "
                    f"{', '.join(_ALARM_SOUNDS)} ou « off »")
            sound = None if spec == "off" else spec
        elif isinstance(spec, dict):
            unknown = set(spec) - {"alarm", "volume", "duration"}
            if unknown:
                raise ValueError(
                    f"st_countdown_rack : pas #{i}, clé(s) d'alarme "
                    f"inconnue(s) {sorted(unknown)!r} — « alarm », « volume » "
                    f"et/ou « duration »")
            if "alarm" in spec:
                cand = spec["alarm"]
                if cand in (None, "off"):
                    sound = None
                elif cand in _ALARM_SOUNDS:
                    sound = cand
                else:
                    raise ValueError(
                        f"st_countdown_rack : pas #{i}, timbre inconnu "
                        f"{cand!r} — {', '.join(_ALARM_SOUNDS)}, « off » ou "
                        f"None")
            if "volume" in spec:
                cand = spec["volume"]
                if not isinstance(cand, (int, float)) or not 0.0 <= cand <= 1.0:
                    raise ValueError(
                        f"st_countdown_rack : pas #{i}, volume {cand!r} "
                        f"hors [0, 1]")
                vol = float(cand)
            if "duration" in spec:
                cand = spec["duration"]
                if cand is not None and (
                        not isinstance(cand, (int, float))
                        or not 0 < cand <= 60):
                    raise ValueError(
                        f"st_countdown_rack : pas #{i}, duration {cand!r} "
                        f"hors ]0, 60] secondes (None = un seul motif)")
                dur = float(cand) if cand is not None else None
        else:
            raise ValueError(
                f"st_countdown_rack : pas #{i}, 3ᵉ élément de type "
                f"{type(spec).__name__} — attendu un timbre (str), « off » "
                f"ou un dict {{'alarm': …, 'volume': …}}")
        # Volume nul = mutisme : le JS ne reçoit alors AUCUN spec.
        if sound is None or vol <= 0:
            return None
        out = {"sound": sound, "vol": vol}
        if dur is not None:
            out["dur"] = dur
        return out

    norm = []  # triplets (étiquette, minutes, spec) — spec = dict ou None
    for i, step in enumerate(steps):
        if len(step) == 2:
            label, minutes = step
            spec = None
        elif len(step) == 3:
            label, minutes, spec = step
        else:
            raise ValueError(
                f"st_countdown_rack : pas #{i} de longueur {len(step)} — "
                f"attendu (étiquette, minutes) ou (étiquette, minutes, "
                f"alarme)")
        norm.append((label, minutes, _resolve_alarm(spec, i)))
    #: Le contrat cardinal : rack muet ⇒ TOUS les fragments d'alarme valent
    #: "" et le HTML émis est BYTE-IDENTIQUE à l'existant — c'est ce qui
    #: protège les baselines i18n des decks qui n'opinent pas (opening).
    rack_alarmed = any(sp for _l, _m, sp in norm)
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
    secs = [max(1, round(minutes * 60)) for _label, minutes, _sp in norm]
    # Racine DOM unique par rangée : l'export inline tout dans UN document.
    dom = "cdr-" + re.sub(r"[^a-zA-Z0-9_-]", "-", key)

    #: Le prélude commun de chaque script : le bus sur le document parent —
    #: en app, le parent des iframes srcdoc ; en export, window lui-même.
    bus_js = f"""
  var P; try {{ P = window.parent || window; }} catch (e) {{ P = window; }}
  var bus = P.__cdrBus = P.__cdrBus || {{}};
  var rack = bus[{rack_id}] = bus[{rack_id}] || {{cards: {{}}, mode: {json.dumps(mode)}, n: {n}}};
"""
    # ── Le cœur audio, appendu au PRÉLUDE quand le rack sonne ───────────────
    # Le prélude est déjà dupliqué dans CHAQUE fragment : y loger l'alarme
    # donne à chaque realm sa propre copie des fonctions (les realms d'iframe
    # meurent au rerun — jamais de fonction partagée via le bus) tout en
    # n'écrivant le code qu'à UN endroit Python. Chaîne ORDINAIRE (pas une
    # f-string) : accolades JS simples, rien n'y est interpolé.
    if rack_alarmed:
        # Sourdine PAR CARTE (NG 2026-09-03, précision : « chaque chronomètre
        # a son alarme ») : une clé localStorage du PARENT par carte — l'état
        # survit aux reruns d'iframes et au rechargement de la page. La cloche
        # GLOBALE agit sur toutes (même logique que ▶ Start / ↺ Reset).
        bus_js += f"""
  var MBASE = 'cdr-alarm-muted-' + {rack_id} + '-';
  var DEFAULT_MUTED = {json.dumps(bool(alarm_muted))};
"""
        bus_js += """\
  function alarmMuted(i) {
    try {
      var v = P.localStorage.getItem(MBASE + i);
      if (v !== null) return v === '1';
    } catch (e) {}
    return DEFAULT_MUTED;
  }
  function setAlarmMuted(i, m) {
    try { P.localStorage.setItem(MBASE + i, m ? '1' : '0'); } catch (e) {}
  }
  // ── Alarme de fin (NG 2026-09-02) ── UN AudioContext par page, créé par
  // le constructeur du PARENT (P.AudioContext) et rangé sur P.__cdrAudio :
  // il survit aux iframes reconstruites au rerun (contrat __cdrBus) et
  // respecte le plafond navigateur (~6 contextes). Politique autoplay :
  // créé/réveillé UNIQUEMENT dans un geste — l'activation d'une iframe
  // srcdoc même origine se propage au parent (spec HTML). Un échec audio ne
  // casse JAMAIS le chrono : tout sous try/catch, silence assumé.
  function armAudio() {
    try {
      var C = P.AudioContext || P.webkitAudioContext;
      if (!C) return;
      var a = P.__cdrAudio = P.__cdrAudio || new C();
      if (a.state === 'suspended') a.resume();
      if (!a.__kicked) {           // ceinture Safari/iOS : un tampon MUET
        var src = a.createBufferSource();          // joué dans le geste vaut
        src.buffer = a.createBuffer(1, 1, 22050);  // autorisation là où
        src.connect(a.destination); src.start(0);  // resume() seul ne suffit
        a.__kicked = true;                         // pas
      }
    } catch (e) {}
  }
  // TRIM égalise la sonie PERÇUE entre timbres (graves ≠ aigus à gain
  // égal) — LE bouton de recalibrage à l'oreille, en un seul endroit.
  var TRIM = {bell: 0.50, beep: 0.35, chime: 0.60, gong: 0.45};
  // Une voix : oscillateur + rampe linéaire d'attaque + extinction
  // EXPONENTIELLE vers 0.0001 — jamais de coupure sèche, pas de claquement
  // dans la sono de l'amphi.
  function vc(a, out, type, freq, t0, atk, peak, decay) {
    var o = a.createOscillator(), g = a.createGain();
    o.type = type; o.frequency.value = freq;
    g.gain.setValueAtTime(0.0001, t0);
    g.gain.linearRampToValueAtTime(peak, t0 + atk);
    g.gain.exponentialRampToValueAtTime(0.0001, t0 + atk + decay);
    o.connect(g); g.connect(out);
    o.start(t0); o.stop(t0 + atk + decay + 0.05);
  }
  function ring(sp, idx, force) {
    if (!sp || sp.vol <= 0) return;
    if (!force && alarmMuted(idx)) return;  // sourdine de LA carte (NG 2026-09-03)
    var a = P.__cdrAudio;
    if (!a) return;
    try {
      if (a.state === 'suspended') a.resume();
      if (a.state !== 'running') return;
      var t0 = a.currentTime + 0.02;
      var master = a.createGain();
      // pow(1.6) : l'oreille est logarithmique, le curseur devient honnête.
      master.gain.value = Math.pow(sp.vol, 1.6) * (TRIM[sp.sound] || 0.5);
      master.connect(a.destination);
      // Durée d'alarme (NG 2026-09-03) : le MOTIF du timbre se RÉPÈTE
      // jusqu'à couvrir sp.dur (étirer une enveloppe sonnerait faux), puis
      // le maître s'éteint proprement à la durée demandée. Sans dur : un
      // seul motif (comportement d'origine).
      var PERIOD = {bell: 1.2, beep: 0.9, chime: 1.8, gong: 3.0};
      var per = PERIOD[sp.sound] || 1.2;
      var reps = sp.dur ? Math.min(60, Math.max(1, Math.ceil(sp.dur / per))) : 1;
      if (sp.dur) {
        master.gain.setValueAtTime(master.gain.value, t0 + sp.dur);
        master.gain.exponentialRampToValueAtTime(0.0001, t0 + sp.dur + 0.2);
      }
      for (var rp = 0; rp < reps; rp++) {
      var tk = t0 + rp * per;
      if (sp.sound === 'beep') {
        // Trois carrés brefs au passe-bas 3 kHz : le carré nu agresse la
        // sono, le filtre garde le mordant sans les harmoniques criardes.
        var lp = a.createBiquadFilter();
        lp.type = 'lowpass'; lp.frequency.value = 3000;
        lp.connect(master);
        for (var b = 0; b < 3; b++) {
          vc(a, lp, 'square', 1046.5, tk + b * 0.22, 0.01, 1.0, 0.12);
        }
      } else if (sp.sound === 'chime') {
        // Carillon : arpège C5–E5–G5 en triangle, doublé d'une octave
        // sinus discrète — le timbre « fin de tour » sans dureté.
        var notes = [523.25, 659.25, 783.99];
        for (var c = 0; c < notes.length; c++) {
          vc(a, master, 'triangle', notes[c], tk + c * 0.18, 0.01, 0.8, 1.2);
          vc(a, master, 'sine', notes[c] * 2, tk + c * 0.18, 0.01, 0.25, 0.9);
        }
      } else if (sp.sound === 'gong') {
        // Gong : six partiels INHARMONIQUES sur 98 Hz derrière un passe-bas
        // qui se referme (1200 → 300 Hz) — le métal s'assombrit en
        // s'éteignant, comme le vrai.
        var lp2 = a.createBiquadFilter();
        lp2.type = 'lowpass';
        lp2.frequency.setValueAtTime(1200, tk);
        lp2.frequency.exponentialRampToValueAtTime(300, tk + 2.5);
        lp2.connect(master);
        var gp = [1.0, 1.52, 2.01, 2.66, 3.22, 4.16];
        for (var p2 = 0; p2 < gp.length; p2++) {
          vc(a, lp2, 'sine', 98 * gp[p2], tk, 0.02, 0.9 / (1 + p2 * 0.4), 2.5);
        }
      } else {
        // Cloche (défaut) : quatre partiels inharmoniques sur 660 Hz,
        // frappe brève — les rapports non entiers font le « métal ».
        var bp = [1.0, 2.0, 2.92, 4.07];
        for (var p3 = 0; p3 < bp.length; p3++) {
          vc(a, master, 'sine', 660 * bp[p3], tk, 0.005, 0.9 / (1 + p3 * 0.6), 0.9);
        }
      }
      }
    } catch (e) {}
  }
"""
    # Les fragments conditionnels — "" quand le rack est muet : c'est LA
    # garantie de sortie byte-identique (contrat baseline i18n ci-dessus).
    # UN listener d'armement sur la racine de CHAQUE fragment (les clics
    # boutons bullent jusqu'à elle) : le cas critique est la chaîne lancée
    # par ▶ Start global — la carte qui sonnera n'a jamais été cliquée,
    # seul le geste sur le fragment global porte alors le déblocage.
    global_arm = ("\n  root.addEventListener('click', armAudio);"
                  if rack_alarmed else "")
    card_arm = global_arm
    # ring() APRÈS paint() et AVANT le relais de chaîne : les DEUX modes
    # passent par cette branche, et un start() du relais qui jetterait
    # n'empêcherait pas la sonnerie.
    ring_tick = "\n      ring(ALARM, IDX);" if rack_alarmed else ""
    # ⏸ dans la fenêtre de 250 ms après expiration : le clamp pose 0 sans
    # passer par tick — le temps EST écoulé, le zéro sonne. Pas de double
    # sonnerie : la branche zéro de tick pose endAt=null avant, donc pause()
    # sort en tête sans repasser ici.
    ring_pause = "if (isDone()) ring(ALARM, IDX);\n    " if rack_alarmed else ""

    # ── Les boutons globaux — un petit fragment au-dessus de la grille ──────
    # La cloche 🔔/🔕 (NG 2026-09-03) : l'interrupteur de sourdine du rack —
    # présent seulement quand le rack est alarmé (contrat byte-identique).
    # Armer joue un APERÇU bref du premier timbre armé : le geste confirme le
    # son ET débloque l'autoplay dans la même intention.
    if rack_alarmed:
        _first = next(sp for _l, _m, sp in norm if sp)
        _preview = {"sound": _first["sound"], "vol": min(_first["vol"], 0.35)}
        #: Les indices des cartes ALARMÉES — la cloche globale n'agit que sur
        #: elles (une carte « off » reste muette, comme son pas le demande).
        _aidx = [i for i, (_l, _m, sp) in enumerate(norm) if sp]
        # Même GABARIT que ▶ Start (remarque NG 2026-09-03 : la cloche a la
        # taille des boutons de sa ligne) — seule la couleur reste discrète.
        alarm_btn = (f'\n  <button class="cdr-alarm-toggle" '
                     f'style="font-size:{2.0 * scale:.2f}vw;font-weight:700;'
                     f'background:transparent;'
                     f'border:0.16vw solid {MUTED};border-radius:0.7vw;'
                     f'padding:0.3em 0.8em;cursor:pointer;line-height:1.25;">🔕</button>')
        alarm_btn_js = f"""
  var bell = root.querySelector('.cdr-alarm-toggle');
  var PREVIEW = {json.dumps(_preview)};
  var AIDX = {json.dumps(_aidx)};
  function allArmed() {{
    for (var k = 0; k < AIDX.length; k++) if (alarmMuted(AIDX[k])) return false;
    return true;
  }}
  function paintBell() {{
    var on = allArmed();
    bell.textContent = on ? '\\uD83D\\uDD14' : '\\uD83D\\uDD15';
    bell.style.opacity = on ? '1' : '0.55';
  }}
  rack.paintGlobalBell = paintBell;
  paintBell();
  // Même logique que ▶ Start / ↺ Reset globaux : la cloche globale agit sur
  // TOUTES les cartes alarmées — armer si au moins une est en sourdine,
  // sinon tout couper (NG 2026-09-03).
  bell.addEventListener('click', function () {{
    var arm = !allArmed();
    AIDX.forEach(function (i) {{
      setAlarmMuted(i, !arm);
      var c = rack.cards[i];
      if (c && c.paintBell) c.paintBell();
    }});
    paintBell();
    if (arm) {{ armAudio(); setTimeout(function () {{ ring(PREVIEW, -1, true); }}, 60); }}
  }});
"""
    else:
        alarm_btn = ""
        alarm_btn_js = ""
    st_html(f"""
<div id="{dom}-all" style="display:flex;gap:1.2vw;justify-content:center;align-items:center;
            height:100%;font-family:'Source Sans Pro',sans-serif;">
  <button class="cdr-all-start" style="font-size:{2.0 * scale:.2f}vw;font-weight:700;
          color:{AMBER};background:transparent;border:0.16vw solid {AMBER};
          border-radius:0.7vw;padding:0.3em 1.4em;cursor:pointer;">{start_all_label}</button>
  <button class="cdr-all-reset" style="font-size:{1.6 * scale:.2f}vw;font-weight:700;
          color:{MUTED};background:transparent;border:0.12vw solid {MUTED};
          border-radius:0.7vw;padding:0.3em 1.1em;cursor:pointer;">{reset_all_label}</button>{alarm_btn}
</div>
<script>
(function () {{
{bus_js}
  var root = document.getElementById('{dom}-all');{global_arm}
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
  }});{alarm_btn_js}
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
        for i, (label, _minutes, _sp) in enumerate(norm):
            # Le spec de CETTE carte descend en JSON (garde d'injection) —
            # null pour une carte muette : ring(null) se tait.
            card_alarm_var = (f"\n  var ALARM = {json.dumps(norm[i][2])};"
                              if rack_alarmed else "")
            # La cloche de LA carte (NG 2026-09-03) : seulement quand ce pas
            # est alarmé — un pas « off » n'a rien à armer ; les racks muets
            # restent byte-identiques (fragments vides).
            if rack_alarmed and norm[i][2]:
                # Même GABARIT que ▶ ⏸ ↺ de la ligne (remarque NG 2026-09-03).
                card_bell = (
                    f'\n    <button class="cdr-bell" '
                    f'style="font-size:min({6.5 * scale:.2f}vw, {12 * scale:.2f}vh);'
                    f'background:transparent;border:min(0.35vw, 0.8vh) solid {MUTED};'
                    f'border-radius:1.2vw;padding:0.1em 0.6em;cursor:pointer;'
                    f'line-height:1;">\U0001F515</button>')
                card_bell_js = """
  var bell = root.querySelector('.cdr-bell');
  function paintBell() {
    var m = alarmMuted(IDX);
    bell.textContent = m ? '\\uD83D\\uDD15' : '\\uD83D\\uDD14';
    bell.style.opacity = m ? '0.55' : '1';
  }
  rack.cards[IDX].paintBell = paintBell;
  paintBell();
  bell.addEventListener('click', function () {
    var m = !alarmMuted(IDX);
    setAlarmMuted(IDX, m);
    paintBell();
    if (rack.paintGlobalBell) rack.paintGlobalBell();
    if (!m) { armAudio(); setTimeout(function () {
      // Aperçu COURT : un seul motif, jamais la durée configurée.
      ring({sound: ALARM.sound, vol: Math.min(ALARM.vol, 0.35)}, IDX, true); }, 60); }
  });
"""
            else:
                card_bell = ""
                card_bell_js = ""
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
            border-radius:1.2vw;padding:0.1em 0.9em;cursor:pointer;">↺</button>{card_bell}
    <span class="cdr-at" style="font-size:min({4.5 * scale:.2f}vw, {8 * scale:.2f}vh);
          color:{MUTED};white-space:nowrap;">&nbsp;</span>
  </div>
</div>
<script>
(function () {{
{bus_js}
  var IDX = {i}, TOTAL = {secs[i]};{card_alarm_var}
  var root = document.getElementById('{dom}-c{i}');{card_arm}
  var digits = root.querySelector('.cdr-digits');
  var at = root.querySelector('.cdr-at');
  var remaining = TOTAL, endAt = null, timer = null;
  // ── Édition de la valeur (NG 2026-09-03) : DOUBLE-CLIC sur les chiffres —
  // « 40 » = 40 min, « 40:30 » = 40 min 30 s ; Entrée/clic ailleurs applique,
  // Échap annule ; un chrono en course repart de la nouvelle valeur, un
  // chrono FINI revit (le zéro rouge s'édite aussi). TOTAL ne change pas :
  // ↺ Reset revient toujours à la durée d'origine.
  var editing = false;
  function parseTime(v) {{
    var pm = String(v).trim().match(/^(\\d{{1,3}})(?::([0-5]?\\d))?$/);
    if (!pm) return null;
    var ps = parseInt(pm[1], 10) * 60 + (pm[2] ? parseInt(pm[2], 10) : 0);
    return ps > 0 ? ps : null;
  }}
  digits.style.cursor = 'pointer';
  digits.addEventListener('dblclick', function () {{
    if (editing) return;
    var wasRunning = endAt !== null;
    if (wasRunning) pause();
    editing = true;
    var cur = fmt(Math.ceil(remaining > 0 ? remaining : TOTAL));
    // La boîte de saisie DOIT contenir « MM:SS » entier (capture NG
    // 2026-09-03 : 4.6ch + interlettrage hérité rognaient les chiffres) —
    // police réduite, largeur large, interlettrage neutre, boîte bornée.
    digits.innerHTML = '<input class="cdr-edit" value="' + cur + '" ' +
      'style="font-size:0.5em;width:7ch;max-width:96%;box-sizing:border-box;' +
      'text-align:center;background:transparent;color:inherit;border:none;' +
      'border-bottom:0.06em solid currentColor;outline:none;padding:0;' +
      'font-weight:inherit;font-family:inherit;letter-spacing:normal;">';
    var inp = digits.querySelector('.cdr-edit');
    inp.focus(); inp.select();
    function done(apply) {{
      if (!editing) return;
      editing = false;
      var ns = apply ? parseTime(inp.value) : null;
      if (ns !== null) remaining = ns;
      paint();
      if (wasRunning && remaining > 0) start();
    }}
    inp.addEventListener('keydown', function (ev) {{
      if (ev.key === 'Enter') done(true);
      else if (ev.key === 'Escape') done(false);
      ev.stopPropagation();
    }});
    inp.addEventListener('blur', function () {{ done(true); }});
  }});
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
    if (editing) return;   // l'input d'édition ne se fait pas écraser
    if (isDone()) {{
      // État zéro SANS coche (ligne NG chronocheck zero=p1, 2026-09-02) :
      // la durée INITIALE en rouge translucide — même nombre de caractères
      // que les autres états, débordement impossible par construction ;
      // la couleur seule porte l'accompli (l'essai « ✓ » débordait la
      // ligne maximisée des deux côtés, capture NG).
      digits.innerHTML = '<span style="color:{CRITICAL};opacity:0.45;">' +
        fmt(TOTAL) + '</span>';
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
      paint();{ring_tick}
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
    {ring_pause}paint();
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
  root.querySelector('.cdr-zero').addEventListener('click', reset);{card_bell_js}
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
