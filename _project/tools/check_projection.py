"""Porte de projection — le rendu des slides aux résolutions de référence.

Décision NG (planche ecran2 + retouches, 2026-09-02) : les tailles se jugent
aux DEUX références de ``postair_display`` — le projecteur (1920×1080) et le
portable de l'orateur (1728×1117) — et la porte est **incrémentale** : elle
ne mesure que les slides des BLOCS modifiés depuis sa dernière application
(manifest d'empreintes ``_project/projection/state.json``, QCM NG
2026-09-02). Elle ne tourne JAMAIS dans ``check_all`` : sur demande, et
obligatoirement avant un push (le push déploie — PLAYBOOK).

Granularités (remarque NG 2026-09-02 : un bloc contient PLUSIEURS slides via
les ``st_slide_break``) :

- le CHANGEMENT se détecte par fichier de bloc (empreinte du ``bck_*.py``) ;
  une dépendance partagée modifiée (shared-blocks, postair_pack, custom/,
  book.py, static/data) invalide le module ENTIER — sinon la porte mentirait ;
- la MESURE se fait par ARRÊT CLAVIER : chaque intervalle entre deux
  marqueurs consécutifs (marqueurs cachés compris) est attribué au bloc du
  dernier marqueur NOMMÉ qui le précède, et un bloc modifié fait re-mesurer
  TOUS ses intervalles.

Verdicts par intervalle (correctif NG 2026-09-03, deux biais tombés le même
jour) : la mesure se fait PANNEAU LATÉRAL FERMÉ (la sidebar de l'export
mangeait ~280 px de largeur et faisait replier le texte) et porte sur le
DERNIER PIXEL PEINT de l'intervalle — texte, média, boîte à fond/bordure —
jamais sur l'écart marqueur→marqueur (qui contient le blanc de fin de slide
et les coupures FULL) : dernier pixel peint ≤ hauteur de fenêtre × tolérance
(défaut 1.03) ; défilement horizontal de page = échec global. Chaque intervalle mesuré est CAPTURÉ en
PNG sous ``_project/projection/<module>/<WxH>/`` pour la relecture d'œil.
La page References est ignorée (liste longue par nature), l'annexe backup
est mesurée comme le reste (elle se projette en séance).

Usage :
    uv run python _project/tools/check_projection.py                 # tous modules, incrémental
    uv run python _project/tools/check_projection.py postair_genai   # un module
    uv run python _project/tools/check_projection.py --all           # ignorer le manifest
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_STATE = _REPO / "_project" / "projection" / "state.json"
_SHOTS = _REPO / "_project" / "projection"

_MODULES = ["postair_opening", "postair_survey", "postair_debates",
            "postair_genai", "postair_mistral", "postair_guidelines",
            "postair_handsup", "postair_waves"]

#: Les références de calibrage — la vérité vit dans postair_display ; copiées
#: ici en repli si l'import échoue hors venv.
_DEFAULT_RESOLUTIONS = [(1920, 1080), (1728, 1117)]

#: Marqueurs ignorés par le verdict de hauteur (listes longues par nature).
_IGNORED_SLUGS = {"references"}

_GREEN, _RED, _YELLOW, _OFF = "\033[32m", "\033[31m", "\033[33m", "\033[0m"


# ── Empreintes ──────────────────────────────────────────────────────────────

def _hash_paths(paths: list[Path]) -> str:
    h = hashlib.sha256()
    for p in sorted(paths):
        h.update(str(p.relative_to(_REPO)).encode())
        try:
            h.update(p.read_bytes())
        except OSError:
            h.update(b"<absent>")
    return h.hexdigest()[:16]


def _shared_hash(module: str) -> str:
    """L'empreinte des dépendances qui invalident le module ENTIER."""
    paths: list[Path] = []
    for root in [_REPO / "modules" / "shared-blocks",
                 _REPO / "postair_pack" / "postair_pack",
                 _REPO / "modules" / module / "custom"]:
        paths += [p for p in root.rglob("*.py") if "__pycache__" not in p.parts]
    paths.append(_REPO / "modules" / module / "book.py")
    data = _REPO / "modules" / module / "static" / "data"
    if data.exists():
        paths += sorted(data.glob("*.json")) + sorted(data.glob("*.bib"))
    return _hash_paths(paths)


def _block_files(module: str) -> dict[str, Path]:
    blocks = _REPO / "modules" / module / "blocks"
    return {p.stem: p for p in sorted(blocks.glob("bck_*.py"))}


def _marker_slug(text: str) -> str:
    """Le slug qu'emploie l'id ``stx-marker-<slug>-<n>`` (espaces → tirets)."""
    return re.sub(r"\s+", "-", text.strip().lower())


def _block_marker_slugs(path: Path) -> list[str]:
    """Les slugs de marqueur déclarés par le fichier de bloc (feuilles en)."""
    src = path.read_text(encoding="utf-8")
    return [
        _marker_slug(m)
        for m in re.findall(r'_MARKERS?\s*=\s*[\[{]?\s*\{\s*"en"\s*:\s*"([^"]+)"', src)
    ]


# ── Export + mesure Playwright ──────────────────────────────────────────────

def _export(module: str, out_dir: Path) -> Path:
    env = dict(os.environ, STX_EDITABLE="false", STX_LANG="en")
    r = subprocess.run(["uv", "run", "stx", "export", "html",
                        f"modules/{module}", "-o", str(out_dir),
                        "--asset-mode", "external"],
                       cwd=_REPO, capture_output=True, text=True, env=env)
    if r.returncode != 0:
        raise RuntimeError(f"{module}: export en échec — {r.stderr.strip()[-300:]}")
    htmls = list(out_dir.rglob("*.html"))
    if not htmls:
        raise RuntimeError(f"{module}: aucun HTML exporté")
    return htmls[0]


def _measure(html: Path, width: int, height: int, wanted_slugs: set[str] | None,
             shots_dir: Path, tolerance: float) -> list[str]:
    """Mesure les intervalles marqueur→marqueur ; rend la liste des problèmes.

    ``wanted_slugs=None`` = tout mesurer. Un intervalle appartient au dernier
    marqueur NOMMÉ (id ≠ ``stx-marker-marker-N-M``) qui le précède.
    """
    from playwright.sync_api import sync_playwright

    problems: list[str] = []
    shots_dir.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height})
        # Panneau latéral FERMÉ (correctif NG 2026-09-03) : la sidebar de
        # l'export (~280 px) mangeait la largeur et faisait replier le texte —
        # tout se mesurait plus haut qu'en projection réelle (constat NG,
        # DevTools 1920×1080 : slide « 94 » verte panneau fermé, rouge à la
        # porte). On pose la préférence AVANT le chargement : le runtime de
        # l'export la lit et masque la sidebar, exactement comme un opérateur
        # qui l'a refermée. Les books, eux, démarrent ``collapsed`` (même
        # décision, même jour).
        page.add_init_script(
            "try { localStorage.setItem('stx-sidebar', 'hidden'); } catch (e) {}")
        page.goto(html.as_uri(), wait_until="load")
        page.wait_for_timeout(600)   # polices + runtimes d'export
        # Toutes les images DOIVENT être peintes avant la mesure : une image
        # pas encore chargée rend un « dernier pixel peint » trop court et un
        # verdict FAUX VERT (constaté sur error-delegating, 2026-09-03).
        try:
            page.wait_for_function(
                "Array.from(document.images).every(i => i.complete)",
                timeout=10_000)
        except Exception:
            pass  # au pire on mesure l'état courant — jamais bloquer la porte
        info = page.evaluate("""() => {
            const ms = [...document.querySelectorAll('[id^="stx-marker-"]')]
              .map(e => ({id: e.id,
                          top: e.getBoundingClientRect().top + window.scrollY}))
              .sort((a, b) => a.top - b.top);
            // Le verdict porte sur le DERNIER PIXEL PEINT de l'intervalle,
            // pas sur l'écart marqueur→marqueur (correctif NG 2026-09-03) :
            // l'ancienne soustraction des seules coupures laissait dans la
            // mesure le blanc de fin de slide (conteneurs pleine hauteur,
            // marges) — la slide « 94 » d'opening sortait ×1.21 alors qu'elle
            // TIENT à l'écran. Est « peint » : une feuille avec du texte, un
            // média, ou une boîte avec fond/bordure visibles ; les éléments
            // fixed/sticky (pagination) et la chrome de coupure sont exclus.
            const tops = ms.map(m => m.top);
            const best = new Array(Math.max(tops.length, 1)).fill(0);
            const isBreak = e => e.closest(
                '.stx-slide-break-rule, .stx-slide-break-spacer,' +
                ' .stx-slide-break-spacer-before');
            for (const e of document.body.querySelectorAll('*')) {
              const cs = getComputedStyle(e);
              if (cs.position === 'fixed' || cs.position === 'sticky') continue;
              if (cs.visibility === 'hidden' || cs.display === 'none') continue;
              if (isBreak(e)) continue;
              const r = e.getBoundingClientRect();
              if (r.height === 0 || r.width === 0) continue;
              const media = /^(IMG|VIDEO|CANVAS|SVG|IFRAME)$/.test(e.tagName);
              const text = e.childElementCount === 0
                           && e.textContent.trim().length > 0;
              const boxed = (cs.backgroundColor !== 'rgba(0, 0, 0, 0)'
                             && parseFloat(cs.opacity) > 0)
                            || parseFloat(cs.borderTopWidth) > 0
                            || parseFloat(cs.borderLeftWidth) > 0;
              if (!media && !text && !boxed) continue;
              // Un élément rogné par un ancêtre (overflow hidden/clip/auto —
              // les chiffres des racks de chronos dépassent DANS leur carte)
              // ne peint que jusqu'au bord de cet ancêtre : on clippe.
              let clip = r.bottom;
              for (let a = e.parentElement; a && a !== document.body;
                   a = a.parentElement) {
                const ov = getComputedStyle(a).overflowY;
                if (ov === 'hidden' || ov === 'clip' || ov === 'auto'
                    || ov === 'scroll') {
                  clip = Math.min(clip, a.getBoundingClientRect().bottom);
                }
              }
              const bottom = clip + window.scrollY;
              // L'intervalle du haut de l'élément décide de l'attribution —
              // un conteneur qui traverse une coupure est ignoré (son fond
              // s'étendrait sur la slide suivante et fausserait tout).
              const top = r.top + window.scrollY;
              let idx = -1;
              for (let k = 0; k < tops.length; k++) {
                if (tops[k] <= top + 1) idx = k; else break;
              }
              if (idx < 0) continue;
              const ceiling = idx + 1 < tops.length ? tops[idx + 1] : Infinity;
              if (bottom > ceiling + 1) continue;  // traverse l'intervalle
              if (bottom - tops[idx] > best[idx]) best[idx] = bottom - tops[idx];
            }
            return {markers: ms, painted: best,
                    docH: document.documentElement.scrollHeight,
                    docW: document.documentElement.scrollWidth};
        }""")
        if info["docW"] > width + 2:
            problems.append(
                f"défilement HORIZONTAL de page : {info['docW']}px > {width}px")
        markers = info["markers"]
        hidden = re.compile(r"^stx-marker-marker-\d+-\d+$")
        owner = None          # slug du dernier marqueur nommé
        owner_seq = 0         # rang de l'intervalle dans son bloc
        for i, m in enumerate(markers):
            mid = m["id"]
            if not hidden.match(mid):
                owner = re.sub(r"^stx-marker-(.*)-\d+$", r"\1", mid)
                owner_seq = 0
            owner_seq += 1
            if owner is None or owner in _IGNORED_SLUGS:
                continue
            if wanted_slugs is not None and owner not in wanted_slugs:
                continue
            top = m["top"]
            h = info["painted"][i]
            page.evaluate(f"window.scrollTo(0, {int(top)})")
            page.wait_for_timeout(120)
            shot = shots_dir / f"{i:02d}-{owner[:40]}-t{owner_seq}.png"
            page.screenshot(path=str(shot))
            if h > height * tolerance:
                problems.append(
                    f"[{owner} · temps {owner_seq}] {h:.0f}px de contenu pour "
                    f"{height}px de fenêtre (×{h / height:.2f}) — {shot.name}")
        browser.close()
    return problems


# ── Orchestration ───────────────────────────────────────────────────────────

def _load_state() -> dict:
    try:
        return json.loads(_STATE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def run(modules: list[str], force_all: bool, tolerance: float,
        resolutions: list[tuple[int, int]]) -> int:
    state = _load_state()
    res_key = ",".join(f"{w}x{h}" for w, h in resolutions)
    failures = 0
    for module in modules:
        mstate = state.get(module, {})
        blocks = _block_files(module)
        shared = _shared_hash(module)
        stale_shared = (mstate.get("_shared") != shared
                        or mstate.get("_resolutions") != res_key)
        hashes = {name: _hash_paths([p]) for name, p in blocks.items()}
        if force_all or stale_shared:
            changed = set(blocks)
        else:
            changed = {n for n, h in hashes.items()
                       if mstate.get("blocks", {}).get(n) != h}
        if not changed:
            print(f"  {_GREEN}✓{_OFF} {module}: à jour (aucun bloc modifié "
                  f"depuis la dernière application)")
            continue
        # blocs changés → leurs slugs de marqueur ; bloc sans slug extrait
        # (marqueur rendu par du code partagé) → prudence : tout mesurer.
        wanted: set[str] | None = set()
        for name in changed:
            slugs = _block_marker_slugs(blocks[name])
            if not slugs:
                wanted = None
                break
            wanted.update(slugs)
        scope = ("module ENTIER" if wanted is None or force_all or stale_shared
                 else f"{len(changed)} bloc(s), {len(wanted)} marqueur(s)")
        if force_all or stale_shared:
            wanted = None
        print(f"  … {module}: {scope}")
        with tempfile.TemporaryDirectory(prefix=f"stx-proj-{module}-") as tmp:
            html = _export(module, Path(tmp))
            problems: list[str] = []
            for w, h in resolutions:
                shots = _SHOTS / module / f"{w}x{h}"
                problems += [f"({w}×{h}) {p}" for p in _measure(
                    html, w, h, wanted, shots, tolerance)]
        if problems:
            failures += 1
            print(f"  {_RED}!{_OFF} {module}: {len(problems)} débordement(s)")
            for p in problems:
                print(f"      {p}")
            # Les blocs en échec restent « à revoir » : leurs empreintes ne
            # sont PAS enregistrées — la porte les reprendra au prochain run.
            ok_blocks = {n: h for n, h in hashes.items() if n not in changed}
            mstate_blocks = dict(mstate.get("blocks", {}), **ok_blocks)
        else:
            print(f"  {_GREEN}✓{_OFF} {module}: toutes les slides mesurées "
                  f"tiennent aux deux références — captures sous "
                  f"_project/projection/{module}/")
            mstate_blocks = hashes
        state[module] = {"_shared": shared, "_resolutions": res_key,
                         "blocks": mstate_blocks}
    _STATE.parent.mkdir(parents=True, exist_ok=True)
    _STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False),
                      encoding="utf-8")
    return failures


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("modules", nargs="*", default=None)
    ap.add_argument("--all", action="store_true",
                    help="ignorer le manifest et tout mesurer")
    ap.add_argument("--tolerance", type=float, default=1.03)
    ap.add_argument("--resolutions", default=None,
                    help="ex. 1920x1080,1728x1117 (défaut : postair_display)")
    args = ap.parse_args()
    if args.resolutions:
        resolutions = [tuple(int(v) for v in r.split("x"))
                       for r in args.resolutions.split(",")]
    else:
        try:
            sys.path.insert(0, str(_REPO / "modules" / "shared-blocks"))
            from postair_display import LAPTOP_REF, PROJECTION_REF
            resolutions = [PROJECTION_REF, LAPTOP_REF]
        except Exception:
            resolutions = _DEFAULT_RESOLUTIONS
    modules = args.modules or _MODULES
    bad = [m for m in modules if m not in _MODULES]
    if bad:
        print(f"module(s) inconnu(s) : {bad} — choix : {_MODULES}")
        return 2
    n = run(modules, args.all, args.tolerance, resolutions)
    if n:
        print(f"{_RED}ÉCHEC{_OFF} — {n} module(s) avec débordement(s)")
        return 1
    print(f"{_GREEN}OK{_OFF} — porte de projection passée")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
