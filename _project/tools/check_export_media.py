"""La porte média des exports — présence des fichiers ET marque DD-35.

Deux contrôles, sur l'export HTML statique de chaque module (l'équivalent
aval du gate e2e ``ai-mark.spec.ts`` du dépôt sumvadis) :

1. **Présence** — chaque ``src`` relatif de l'export pointe un fichier
   réellement exporté. C'est le contrôle qui avait trouvé, le 2026-08-03,
   trois slides affichant une image manquante ; il était resté manuel.
2. **Marque DD-35** — tout média affiché porte la pastille « ✦ AI », SAUF
   s'il figure sur la liste blanche calculée depuis les données. La porte est
   FERMÉE par défaut : l'absence de marque se mérite, elle ne se présume pas.

La liste blanche n'est jamais tenue à la main :

- les SVG versionnés (repli dessiné, radars, pictos) ;
- les QR codes et captures d'écran d'application (``images/qr/``, tout
  fichier ``*screenshot*``) ;
- les médias de figures dont le manifeste gelé dit ``portrait_ai: false``
  (personnes vivantes photographiées — le hub décide, jamais ici).

L'export renomme les assets par préfixe de leur SHA-256 : l'association
export → source se fait par empreinte, pas par nom.

Usage::

    uv run python _project/tools/check_export_media.py             # les 6 modules
    uv run python _project/tools/check_export_media.py postair_genai

Ne modifie rien ; code de sortie 1 à la première violation.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path

_REPO = Path(__file__).parent.parent.parent
# postair_waves ajouté le 2026-09-01 (planche baseline, NG) : le deck le plus
# riche en images (68 dans l'export) manquait à la liste depuis sa création —
# la porte ne le contrôlait jamais par défaut.
_MODULES = ["postair_opening", "postair_survey", "postair_debates",
            "postair_genai", "postair_guidelines", "postair_collection",
            "postair_handsup", "postair_waves"]
_CHIP_TEXT = "✦"
_CHIP_CSS_SIGNATURE = "rgba(113, 113, 122, 0.35)"


class _Dom(HTMLParser):
    """Arbre minimal : parents, médias, pastilles."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parents: list[int] = []          # pile d'identifiants de nœuds
        self.node_parent: dict[int, int] = {}
        self.node_style: dict[int, str] = {}
        self.node_tag: dict[int, str] = {}
        self.node_class: dict[int, str] = {}
        self.media: list[tuple[int, str, str]] = []   # (nœud, tag, src)
        self.chips: list[int] = []
        self._next = 0
        self._text_target: int | None = None

    def handle_starttag(self, tag, attrs):
        nid = self._next
        self._next += 1
        a = dict(attrs)
        self.node_parent[nid] = self.parents[-1] if self.parents else -1
        self.node_tag[nid] = tag
        self.node_style[nid] = a.get("style", "")
        self.node_class[nid] = a.get("class", "")
        if tag in ("img", "video", "source", "audio"):
            src = a.get("src") or ""
            if src:
                self.media.append((nid, tag, src))
        if tag not in ("img", "br", "source", "meta", "link", "input", "hr"):
            self.parents.append(nid)
            self._text_target = nid

    def handle_endtag(self, tag):
        if tag not in ("img", "br", "source", "meta", "link", "input", "hr"):
            if self.parents:
                self.parents.pop()
            self._text_target = self.parents[-1] if self.parents else None

    def handle_data(self, data):
        if _CHIP_TEXT in data and self._text_target is not None:
            # Le nœud porteur du texte est la pastille si son style est LE
            # style DD-35 — le glyphe seul ne suffit pas (il peut apparaître
            # dans du texte).
            nid = self._text_target
            if _CHIP_CSS_SIGNATURE in self.node_style.get(nid, ""):
                self.chips.append(nid)

    def ancestors(self, nid: int):
        while nid != -1:
            yield nid
            nid = self.node_parent.get(nid, -1)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _whitelist_hashes(module: str) -> dict[str, str]:
    """empreinte -> raison, pour les médias légitimement SANS marque."""
    root = _REPO / "modules" / module / "static"
    out: dict[str, str] = {}
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(root).as_posix()
        if p.suffix == ".svg":
            out[_sha(p)] = f"svg versionné ({rel})"
        elif "/qr/" in f"/{rel}" :
            out[_sha(p)] = f"QR code ({rel})"
        elif "screenshot" in p.name.lower():
            out[_sha(p)] = f"capture d'application ({rel})"
        elif rel.startswith("media/captures/"):
            # Écrans réels de l'application, matérialisés depuis le catalogue
            # gelé (build_survey_captures.py) — non IA par nature.
            out[_sha(p)] = f"capture d'écran du parcours ({rel})"
    manifest = _REPO / "modules" / module / "static" / "data" / "content.json"
    if manifest.exists():
        data = json.loads(manifest.read_text(encoding="utf-8"))
        for pole in data.get("poles", []):
            for f in pole["figures"]:
                media = f.get("media") or {}
                for role, flag in (("portrait", "portrait_ai"),
                                   ("poster", "video_ai")):
                    local = media.get(role)
                    if local and not media.get(flag, False):
                        file = root / "media" / local
                        if file.exists():
                            out[_sha(file)] = (f"{role} non synthétique "
                                               f"({f['id']}, manifeste hub)")
    return out


def check_module(module: str, keep: Path | None = None) -> list[str]:
    out_dir = keep or Path(tempfile.mkdtemp(prefix=f"stx-gate-{module}-"))
    # Export en mode PROJECTION, quel que soit le .env d'auteur : c'est ce que
    # la salle verra. (En mode éditeur la pastille passe AVANT l'image — barre
    # « Edit Image » oblige — et l'association « pastille → média précédent »
    # ne tiendrait plus. ``config.py`` lit l'environnement avant le .env.)
    env = dict(os.environ, STX_EDITABLE="false")
    r = subprocess.run(["uv", "run", "stx", "export", "html",
                        f"modules/{module}", "-o", str(out_dir),
                        "--asset-mode", "external"],
                       cwd=_REPO, capture_output=True, text=True, env=env)
    if r.returncode != 0:
        return [f"{module}: export en échec — {r.stderr.strip()[-300:]}"]
    html_files = list(out_dir.rglob("*.html"))
    if not html_files:
        return [f"{module}: aucun HTML exporté"]
    whitelist = _whitelist_hashes(module)
    static_root = _REPO / "modules" / module / "static"
    problems: list[str] = []
    for html in html_files:
        dom = _Dom()
        dom.feed(html.read_text(encoding="utf-8"))
        # Depuis streamtex 0.7.23 la pastille des IMAGES est STRUCTURELLE :
        # ``st_image(overlay=…)`` émet ``stx-media-box`` autour de l'img et de
        # la pastille — un ancêtre porteur de cette classe suffit. Le repli par
        # PROXIMITÉ (pastille ``ai_marked`` la plus proche, amont ou aval — les
        # blocs sont aplatis à l'export) ne sert plus qu'aux VIDÉOS, en
        # attendant la phase 2 du slot natif.
        marked_ids: set[int] = set()
        media_sorted = sorted(dom.media, key=lambda m: m[0])
        for nid, _tag, _src in media_sorted:
            if any("stx-media-box" in dom.node_class.get(a, "")
                   for a in dom.ancestors(nid)):
                marked_ids.add(nid)
        for chip in sorted(dom.chips):
            before = [m for m in media_sorted
                      if m[0] < chip and m[0] not in marked_ids]
            after = [m for m in media_sorted
                     if m[0] > chip and m[0] not in marked_ids]
            candidates = ([before[-1]] if before else []) + \
                         ([after[0]] if after else [])
            if candidates:
                closest = min(candidates, key=lambda m: abs(m[0] - chip))
                marked_ids.add(closest[0])
        for nid, tag, src in media_sorted:
            if re.match(r"^(https?:|data:|blob:)", src):
                continue
            # Le chrome de l'export (sidebar, logo StreamTeX) vit sous <nav> —
            # ce n'est pas du contenu de slide.
            if any(dom.node_tag.get(a) == "nav" for a in dom.ancestors(nid)):
                continue
            # Trois espaces de chemins : l'asset exporté (data/…), l'espace
            # servi par le conteneur (app/static/… — l'export ne le copie pas,
            # nginx le sert en production), et un chemin absolu (st.video).
            candidates = [html.parent / src,
                          static_root / src.removeprefix("app/static/"),
                          Path(src)]
            asset = next((c for c in candidates if c.is_file()), None)
            if asset is None:
                problems.append(f"{module}: src absent — {src}")
                continue
            if nid in marked_ids:
                continue
            reason = whitelist.get(_sha(asset))
            if reason is None:
                problems.append(f"{module}: média SANS marque DD-35 ni raison "
                                f"— {src} ({tag})")
    return problems


def main() -> int:
    modules = sys.argv[1:] or _MODULES
    failed = False
    for m in modules:
        problems = check_module(m)
        if problems:
            failed = True
            for p in problems:
                print(f"  ! {p}")
        else:
            print(f"  ✓ {m}: tous les src présents, toute absence de marque justifiée")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
