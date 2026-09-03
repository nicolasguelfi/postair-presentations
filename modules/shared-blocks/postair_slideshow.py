"""Le diaporama d'images — captures qui défilent en boucle, sans JavaScript.

Décision NG (planche anim1, 2026-09-03) :

- ``compo=p1`` — **fondu enchaîné CSS pur** : les images sont empilées en
  absolu dans une scène et une animation ``@keyframes`` générée fait défiler
  les opacités (boucle infinie). Zéro JavaScript : le même rendu dans l'app,
  l'export HTML hors-ligne de la salle, et rien qui puisse « s'endormir » en
  séance. Limite assumée : l'export PDF ne montre que la première image.
- ``tuyau=p1`` — les images vivent dans un dossier DU MODULE
  (``static/images/slideshows/<nom>/``, versionné — exception assumée du
  dépôt) et le composant **globbe au chargement** : déposer un fichier
  (Dropbox le synchronise) suffit pour le voir au prochain affichage local ;
  la production suit au commit, comme tout média versionné. Les fichiers
  lourds se passent à la moulinette ``_project/tools/optimize_images.py``.
- ``api=a2`` (amendée NG) — durée PAR IMAGE via un sidecar OPTIONNEL
  ``durations.json`` dans le dossier (``{"DLH-01.webp": 8}``, en secondes) ;
  toute image absente du sidecar — ou tout dossier sans sidecar — prend la
  durée par défaut ``dwell_s``, réglable par le module appelant (TUNING).

R4d : la scène est bornée par la hauteur (``stage_vh``) ET par sa cellule —
largeur = ``min(100 %, stage_vh × ratio de la première image)`` ; les images
s'affichent en ``object-fit: contain`` (une capture ne se rogne pas).

Les images passent par ``st_image`` (jamais un chemin en dur dans du HTML) :
URL servies, matérialisation d'export et porte DD-35 restent natives.

⚠ Module PARTAGÉ (shared-blocks) : une édition ici exige un redémarrage du
serveur Streamlit (hors du rechargement à chaud des blocs).
"""

from __future__ import annotations

import json
from pathlib import Path

from streamtex import Style, st_block, st_html, st_image

#: Les extensions acceptées dans un dossier de diaporama.
_EXTS = {".png", ".jpg", ".jpeg", ".webp"}

#: Durée du fondu entre deux images, en secondes.
_FADE_S = 0.8


def _folder_path(folder: str) -> Path:
    """Le dossier sur disque, via le registre ``set_static_sources`` du book.

    ⚠ Jamais ``Path.cwd()`` seul : ``run-postair`` lance depuis la RACINE du
    dépôt quand le conteneur fait ``cd`` dans le module (constaté par NG au
    premier lancement, 2026-09-03) — seules les sources statiques déclarées
    par le book disent où vit ``static/``.
    """
    from streamtex import get_static_sources
    candidates = [Path(src) / folder for src in get_static_sources()]
    for c in candidates:
        if c.is_dir():
            return c
    # Repli (harnais de test sans book) : le répertoire courant.
    return candidates[0] if candidates else Path.cwd() / "static" / folder


def slideshow_images(folder: str) -> list[Path]:
    """Les images du dossier, dans l'ordre des noms (ton nommage 01, 02…)."""
    root = _folder_path(folder)
    if not root.is_dir():
        raise FileNotFoundError(
            f"Diaporama : dossier {root} introuvable — une slide sans images "
            f"est un trou devant l'amphithéâtre, rien n'est affiché en repli.")
    files = sorted(p for p in root.iterdir()
                   if p.suffix.lower() in _EXTS and not p.name.startswith("."))
    if not files:
        raise FileNotFoundError(
            f"Diaporama : {root} ne contient aucune image ({'/'.join(sorted(e.strip('.') for e in _EXTS))}).")
    return files


def _durations(root: Path, files: list[Path], dwell_s: float) -> list[float]:
    """La durée de chaque image : sidecar ``durations.json`` sinon défaut."""
    sidecar = root / "durations.json"
    table: dict = {}
    if sidecar.exists():
        try:
            table = json.loads(sidecar.read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            raise ValueError(f"Diaporama : {sidecar} illisible — {e}") from e
    return [float(table.get(f.name, dwell_s)) for f in files]


def _ratio(path: Path, default: float = 16 / 9) -> float:
    """Largeur/hauteur de la PREMIÈRE image — la forme de la scène (R4d)."""
    try:
        from PIL import Image
        with Image.open(path) as im:
            w, h = im.size
        return (w / h) if h else default
    except Exception:
        return default


def st_slideshow(folder: str, dwell_s: float = 4.0, stage_vh: int = 66,
                 alt: str = "") -> None:
    """Le diaporama : les images de ``static/<folder>`` en fondu, en boucle.

    :param folder: dossier relatif au ``static/`` du module, p.ex.
        ``"images/slideshows/dlh"`` — les fichiers y sont lus À CHAQUE
        affichage (déposer une image suffit).
    :param dwell_s: durée par défaut d'une image (secondes) — surchargée par
        image via ``durations.json`` (api=a2).
    :param stage_vh: hauteur de la scène en vh — LE levier de taille (R4d).
    :param alt: préfixe du texte alternatif (défaut : le nom du dossier).
    """
    files = slideshow_images(folder)
    dwell = _durations(_folder_path(folder), files, dwell_s)
    ratio = _ratio(files[0])
    uid = abs(hash((folder, len(files)))) % 100_000
    alt = alt or folder.rstrip("/").split("/")[-1]

    stage = Style(
        f"position: relative; height: {stage_vh}vh; "
        f"width: min(100%, {stage_vh * ratio:.1f}vh); overflow: hidden; "
        f"margin-left: auto; margin-right: auto;",
        f"postair_slideshow_stage_{uid}",
    )
    layer_css = ("position: absolute; inset: 0; width: 100%; height: 100%; "
                 "object-fit: contain; margin: 0;")

    if len(files) == 1:
        with st_block(stage):
            st_image(Style(layer_css, f"postair_slideshow_{uid}_0"),
                     uri=f"{folder}/{files[0].name}", alt=f"{alt} — 1/1")
        return

    # ── Les keyframes : chaque image a sa fenêtre d'opacité sur le cycle. ──
    total = sum(dwell)
    pct = lambda t: max(0.0, min(100.0, t / total * 100))  # noqa: E731
    css: list[str] = []
    start = 0.0
    for i, d in enumerate(dwell):
        a, b = pct(start - _FADE_S), pct(start)
        c, e = pct(start + d), pct(start + d + _FADE_S)
        if i == 0:
            # La première image est déjà visible à 0 % et revient par le
            # fondu de fin de cycle — la boucle est sans couture.
            frames = (f"0% {{opacity: 1;}} {c:.3f}% {{opacity: 1;}} "
                      f"{e:.3f}% {{opacity: 0;}} "
                      f"{pct(total - _FADE_S):.3f}% {{opacity: 0;}} "
                      f"100% {{opacity: 1;}}")
        else:
            frames = (f"0% {{opacity: 0;}} {a:.3f}% {{opacity: 0;}} "
                      f"{b:.3f}% {{opacity: 1;}} {c:.3f}% {{opacity: 1;}} "
                      f"{min(e, 100.0):.3f}% {{opacity: 0;}} 100% {{opacity: 0;}}")
        css.append(f"@keyframes postair-ss-{uid}-{i} {{ {frames} }}")
        start += d
    st_html("<style>" + "\n".join(css) + "</style>")

    with st_block(stage):
        for i, f in enumerate(files):
            st_image(
                Style(layer_css +
                      f" animation: postair-ss-{uid}-{i} {total:.2f}s "
                      f"linear infinite;",
                      f"postair_slideshow_{uid}_{i}"),
                uri=f"{folder}/{f.name}",
                alt=f"{alt} — {i + 1}/{len(files)}")
