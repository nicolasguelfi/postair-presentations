"""La planche EN/FR d'un module — ce que NG relit (recette R8 du plan-i18n).

Exporte le module dans les deux langues, capture chaque page (marqueur) de
l'export FR en 1920×1080 avec le Chromium de playwright (dépendance dev,
poste de l'auteur — jamais le conteneur), et écrit UNE page HTML autonome :
pour chaque marqueur, le texte EN et le texte FR côte à côte, la capture FR
dessous. Sortie : ``_project/i18n/<module>/planche.html`` (+ ``shots/``).

Usage::

    uv run python _project/tools/i18n_planche.py postair_opening
    uv run python _project/tools/i18n_planche.py postair_survey --no-shots   # texte seul, rapide
"""

from __future__ import annotations

import argparse
import html
import json
import sys
import tempfile
from pathlib import Path

_TOOLS = Path(__file__).parent
_REPO = _TOOLS.parent.parent
sys.path.insert(0, str(_TOOLS))
import check_i18n as ci  # noqa: E402


def _shots(module: str, out_dir: Path, markers: list[str]) -> dict[str, str]:
    from playwright.sync_api import sync_playwright
    out_dir.mkdir(parents=True, exist_ok=True)
    shots: dict[str, str] = {}
    with tempfile.TemporaryDirectory(prefix=f"stx-planche-{module}-") as tmp:
        html_path = ci._export(module, "fr", Path(tmp))
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1920, "height": 1080})
            page.goto(html_path.as_uri())
            page.wait_for_timeout(800)
            # Masquer le chrome de l'export (sidebar, barre des marqueurs).
            page.add_style_tag(content="#stx-sidebar,#stx-marker-nav,.stx-sidebar-toggle"
                                       "{display:none!important}.streamtex-page{margin-left:0!important}")
            for i, m in enumerate(markers):
                el = page.locator(f"#{m}")
                if el.count() == 0:
                    continue
                el.scroll_into_view_if_needed()
                page.evaluate(f"document.getElementById('{m}').scrollIntoView({{block:'start'}})")
                page.wait_for_timeout(250)
                file = out_dir / f"{i:03d}.png"
                page.screenshot(path=str(file))
                shots[m] = file.name
            browser.close()
    return shots


def build(module: str, with_shots: bool) -> Path:
    en, fr = ci.snapshot(module, "en"), ci.snapshot(module, "fr")
    out = _REPO / "_project" / "i18n" / module
    out.mkdir(parents=True, exist_ok=True)
    shots = _shots(module, out / "shots", fr["markers"]) if with_shots else {}
    rows = []
    for i, (me, mf) in enumerate(zip(en["markers"], fr["markers"])):
        te, tf = en["text"].get(me, ""), fr["text"].get(mf, "")
        same = " same" if te == tf else ""
        shot = (f'<img src="shots/{shots[mf]}" alt="page {i} FR">'
                if mf in shots else "")
        rows.append(
            f'<section class="page{same}"><h2>{i} · {html.escape(mf)}</h2>'
            f'<div class="cols"><div class="col"><h3>EN</h3><p>{html.escape(te)}</p></div>'
            f'<div class="col"><h3>FR</h3><p>{html.escape(tf)}</p></div></div>{shot}</section>')
    doc = f"""<!doctype html><html lang="fr"><meta charset="utf-8">
<title>Planche EN/FR — {module}</title>
<style>
body{{font-family:-apple-system,system-ui,sans-serif;margin:0;background:#f3f5f8;color:#1a1a2e}}
header{{padding:20px 32px;background:#1a1a2e;color:#fff}}
header small{{opacity:.7}}
section.page{{margin:24px 32px;padding:16px 20px;background:#fff;border:1px solid #cfd4e0}}
section.same h2::after{{content:" — identique EN/FR";color:#c9574b;font-weight:400;font-size:.8em}}
h2{{font-size:15px;margin:0 0 10px;font-family:ui-monospace,monospace}}
.cols{{display:grid;grid-template-columns:1fr 1fr;gap:20px}}
h3{{font-size:12px;letter-spacing:.08em;color:#178f84;margin:0 0 6px}}
p{{font-size:14px;line-height:1.5;margin:0}}
img{{max-width:100%;margin-top:14px;border:1px solid #cfd4e0}}
</style>
<header><h1>Planche EN/FR — {module}</h1><small>{len(rows)} pages · TOC FR : {html.escape(" · ".join(fr["toc"][:12]))}{" …" if len(fr["toc"]) > 12 else ""}</small></header>
{"".join(rows)}
</html>"""
    (out / "planche.html").write_text(doc, encoding="utf-8")
    (out / "snapshots.json").write_text(json.dumps({"en": en, "fr": fr}, ensure_ascii=False, indent=1), encoding="utf-8")
    return out / "planche.html"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("module")
    ap.add_argument("--no-shots", action="store_true")
    args = ap.parse_args()
    path = build(args.module, with_shots=not args.no_shots)
    print(f"planche : {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
