"""La moulinette d'optimisation des captures — resize + webp, sur demande.

Née avec le diaporama (planche anim1, tuyau=p1, 2026-09-03) : une capture
d'écran Retina pèse 1 à 6 Mo (DLH-03 : 5,7 Mo) — servie telle quelle à la
salle c'est du poids pour rien. La moulinette borne la largeur et convertit
en webp ; elle ne touche JAMAIS les originaux hors du dossier cible.

Usage :
    uv run python _project/tools/optimize_images.py <dossier> [--max-px 1920]
        [--quality 82] [--keep]

- convertit chaque .png/.jpg/.jpeg du dossier en .webp (même nom) ;
- réduit à ``--max-px`` de large si plus grand (jamais agrandi) ;
- supprime l'original converti (``--keep`` pour le garder) ;
- laisse les .webp existants tels quels ;
- imprime avant/après — la moulinette est un geste, pas une porte.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


def optimize(folder: Path, max_px: int, quality: int, keep: bool) -> int:
    if not folder.is_dir():
        raise SystemExit(f"dossier introuvable : {folder}")
    total_before = total_after = count = 0
    for src in sorted(folder.iterdir()):
        if src.suffix.lower() not in {".png", ".jpg", ".jpeg"}:
            continue
        dst = src.with_suffix(".webp")
        before = src.stat().st_size
        with Image.open(src) as im:
            if im.width > max_px:
                im = im.resize((max_px, round(im.height * max_px / im.width)),
                               Image.LANCZOS)
            im.save(dst, "WEBP", quality=quality, method=6)
        after = dst.stat().st_size
        total_before += before
        total_after += after
        count += 1
        if not keep:
            src.unlink()
        print(f"  {src.name}: {before / 1e6:.2f} Mo → {dst.name}: "
              f"{after / 1e6:.2f} Mo")
    if count:
        print(f"{count} image(s) : {total_before / 1e6:.2f} Mo → "
              f"{total_after / 1e6:.2f} Mo")
    else:
        print("rien à convertir (que des .webp ?)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("folder", type=Path)
    ap.add_argument("--max-px", type=int, default=1920)
    ap.add_argument("--quality", type=int, default=82)
    ap.add_argument("--keep", action="store_true",
                    help="garder les originaux convertis")
    a = ap.parse_args()
    return optimize(a.folder, a.max_px, a.quality, a.keep)


if __name__ == "__main__":
    raise SystemExit(main())
