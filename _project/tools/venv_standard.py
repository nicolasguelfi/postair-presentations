"""venv_standard — le STANDARD ``.venv`` (lien hors Dropbox) : analyse et pose.

Le standard (``.venv.readme.md`` / ``MACHINE.md``, décision NG 2026-08-03) :
dans un projet Python vivant dans un dossier synchronisé, ``.venv`` est un
LIEN SYMBOLIQUE vers ``~/.venvs/<projet>`` (l'environnement réel, local à
chaque machine, hors synchronisation) et ``.gitignore`` porte ``.venv`` SANS
barre finale. Le lien voyage par la synchronisation ; le versionner en plus
(``git add -f``) est facultatif, hors standard.

Usage — depuis n'importe quel dossier de projet Python (ou avec un chemin) :

    uv run python _project/tools/venv_standard.py [chemin]            # ANALYSE
    uv run python _project/tools/venv_standard.py [chemin] --dry      # SIMULE la pose
    uv run python _project/tools/venv_standard.py [chemin] --install  # POSE le standard

- L'analyse ne touche à rien et sort 0 (conforme) ou 1 (écarts listés).
- ``--dry`` affiche TOUTES les actions que ``--install`` ferait, sans rien
  toucher (aucune écriture, aucune commande lancée).
- ``--install`` applique : un ``.venv`` réel est ÉCARTÉ (déplacé en
  ``~/.venvs/<projet>.remplace-<horodatage>``, jamais supprimé), la cible est
  créée, le lien posé, ``.gitignore`` complété, et ``uv sync`` lancé si
  ``pyproject.toml`` existe et que l'environnement a bougé. Chaque action est
  annoncée avant d'être faite.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

VENVS = Path.home() / ".venvs"

GREEN, RED, YELLOW, OFF = "\033[32m", "\033[31m", "\033[33m", "\033[0m"


def _ok(msg: str) -> None:
    print(f"  {GREEN}✓{OFF} {msg}")


def _ko(msg: str) -> None:
    print(f"  {RED}✗{OFF} {msg}")


def _warn(msg: str) -> None:
    print(f"  {YELLOW}!{OFF} {msg}")


def _du(path: Path) -> str:
    """Taille humaine approchée d'un arbre (pour montrer le poids d'un venv réel)."""
    total = 0
    try:
        for p in path.rglob("*"):
            try:
                if p.is_file() and not p.is_symlink():
                    total += p.stat().st_size
            except OSError:
                pass
    except OSError:
        pass
    for unit in ("o", "Ko", "Mo", "Go"):
        if total < 1024:
            return f"{total:.0f} {unit}"
        total /= 1024
    return f"{total:.0f} To"


def _synced(path: Path) -> bool:
    """Le chemin vit-il dans un dossier synchronisé ? (heuristique par nom)."""
    parts = " ".join(str(path).lower().split(os.sep))
    return any(m in parts for m in ("dropbox", "onedrive", "google drive",
                                    "icloud", "mobile documents", "sync"))


def _is_git(project: Path) -> bool:
    return subprocess.run(["git", "-C", str(project), "rev-parse", "--git-dir"],
                          capture_output=True).returncode == 0


def _git_tracked(project: Path, rel: str) -> bool:
    r = subprocess.run(["git", "-C", str(project), "ls-files", "--error-unmatch", rel],
                       capture_output=True)
    return r.returncode == 0


def _gitignore_state(project: Path) -> str:
    """« sans-barre » (conforme) · « avec-barre » · « absent » · « pas-de-fichier »."""
    gi = project / ".gitignore"
    if not gi.exists():
        return "pas-de-fichier"
    lines = [ln.strip() for ln in gi.read_text(encoding="utf-8",
                                               errors="replace").splitlines()]
    if ".venv" in lines:
        return "sans-barre"
    if ".venv/" in lines or "/.venv/" in lines or "/.venv" in lines:
        return "avec-barre"
    return "absent"


def analyse(project: Path) -> int:
    """L'état du projet face au standard — 0 conforme, 1 sinon. Ne touche à rien."""
    print(f"Projet : {project}")
    print(f"Synchronisé : {'oui' if _synced(project) else 'non détecté'} "
          f"(heuristique par nom de chemin)")
    issues = 0
    venv = project / ".venv"
    target = VENVS / project.name

    if not venv.exists() and not venv.is_symlink():
        _ko(".venv absent — ni lien ni dossier")
        issues += 1
    elif venv.is_symlink():
        dest = Path(os.readlink(venv))
        if not dest.is_absolute():
            dest = (project / dest).resolve()
        if _synced(dest):
            _ko(f".venv est un lien, mais sa cible {dest} est DANS un dossier "
                f"synchronisé — l'environnement doit vivre dehors")
            issues += 1
        elif not dest.exists():
            _warn(f".venv → {dest} : lien conforme mais cible ABSENTE sur cette "
                  f"machine — geste machine neuve : mkdir -p {dest} && uv sync")
            issues += 1
        else:
            _ok(f".venv → {dest} (lien, cible présente hors synchronisation)")
            if dest != target and dest.parent == VENVS:
                _warn(f"cible nommée {dest.name!r} ≠ dossier du projet "
                      f"{project.name!r} — toléré, mais le standard nomme la "
                      f"cible comme le projet")
            cfg = dest / "pyvenv.cfg"
            if cfg.exists():
                home = next((ln.split("=", 1)[1].strip()
                             for ln in cfg.read_text(encoding="utf-8").splitlines()
                             if ln.startswith("home")), None)
                if home and not Path(home).exists():
                    _warn(f"l'interpréteur épinglé ({home}) n'existe pas ici — "
                          f"« uv sync » le reconstruira")
    else:
        _ko(f".venv est un VRAI dossier ({_du(venv)}) — c'est l'anti-pattern : "
            f"poids synchronisé, chemins absolus, lectures périmées")
        issues += 1

    gi = _gitignore_state(project)
    if gi == "sans-barre":
        _ok(".gitignore porte « .venv » sans barre finale")
    elif gi == "avec-barre":
        _ko(".gitignore vise « .venv/ » (dossiers seulement) — la règle doit "
            "être « .venv » sans barre pour couvrir aussi le lien")
        issues += 1
    elif gi == "absent":
        _ko(".gitignore ne mentionne pas .venv")
        issues += 1
    else:
        _warn("pas de .gitignore")
        issues += 1

    if _is_git(project):
        if venv.is_dir() and _git_tracked(project, ".venv"):
            _ko("un .venv RÉEL est versionné — à écarter d'urgence")
            issues += 1
        elif venv.is_symlink():
            tracked = _git_tracked(project, ".venv")
            _ok("lien " + ("versionné (voyage par git ET par la synchronisation)"
                           if tracked else
                           "non versionné — il voyage par la synchronisation "
                           "(« git add -f .venv » possible si le projet doit "
                           "aussi voyager par git nu)"))
    else:
        _warn("pas un dépôt git — la partie git du standard ne s'applique pas")

    if not (project / "pyproject.toml").exists():
        _warn("pas de pyproject.toml — « uv sync » n'aura rien à installer")

    print()
    if issues:
        print(f"{RED}NON CONFORME{OFF} — {issues} écart(s). "
              f"« --dry » montre la pose, « --install » l'applique.")
        return 1
    print(f"{GREEN}CONFORME{OFF} — le standard .venv est respecté.")
    return 0


def plan(project: Path) -> list[tuple[str, "callable"]]:
    """Le plan de pose : [(description, action)] — les actions ne sont
    exécutées que par ``--install`` ; ``--dry`` n'affiche que les textes."""
    venv = project / ".venv"
    target = VENVS / project.name
    steps: list[tuple[str, object]] = []

    # ── L'état du lien, en booléens clairs ──────────────────────────────────
    link_ok, dest = False, target
    if venv.is_symlink():
        dest = Path(os.readlink(venv))
        if not dest.is_absolute():
            dest = (project / dest).resolve()
        link_ok = not _synced(dest)
    touched_env = False

    if link_ok:
        target = dest
        if not dest.exists():
            steps.append((f"créer la cible du lien existant : mkdir -p {dest}",
                          lambda d=dest: d.mkdir(parents=True, exist_ok=True)))
            touched_env = True
    else:
        if venv.is_symlink():
            steps.append((f"retirer le lien non conforme .venv → {dest} "
                          f"(cible dans un dossier synchronisé)",
                          lambda v=venv: v.unlink()))
        elif venv.is_dir():
            aside = VENVS / f"{project.name}.remplace-{time.strftime('%Y%m%d-%H%M%S')}"
            steps.append((f"écarter le .venv RÉEL ({_du(venv)}) vers {aside} "
                          f"(déplacé, jamais supprimé — à purger à la main)",
                          lambda v=venv, a=aside: (VENVS.mkdir(exist_ok=True),
                                                   shutil.move(str(v), str(a)))))
        steps.append((f"créer la cible : mkdir -p {target}",
                      lambda t=target: t.mkdir(parents=True, exist_ok=True)))
        steps.append((f"poser le lien : ln -s {target} .venv",
                      lambda v=venv, t=target: v.symlink_to(t)))
        touched_env = True

    # ── .gitignore ──────────────────────────────────────────────────────────
    gi_state = _gitignore_state(project)
    gi = project / ".gitignore"
    if gi_state in ("absent", "pas-de-fichier"):
        steps.append(("ajouter « .venv » (sans barre finale) à .gitignore",
                      lambda g=gi: g.open("a", encoding="utf-8")
                      .write(("" if not g.exists() or
                              g.read_text(encoding="utf-8").endswith("\n")
                              else "\n") + ".venv\n")))
    elif gi_state == "avec-barre":
        steps.append(("remplacer « .venv/ » par « .venv » (sans barre) dans .gitignore",
                      lambda g=gi: g.write_text(
                          g.read_text(encoding="utf-8")
                          .replace("/.venv/", ".venv").replace(".venv/", ".venv"),
                          encoding="utf-8")))

    # ── uv sync : seulement si l'environnement a bougé ou n'existe pas ──────
    if (project / "pyproject.toml").exists() and (
            touched_env or not (target / "pyvenv.cfg").exists()):
        steps.append(("construire l'environnement dans la cible : uv sync",
                      lambda p=project: subprocess.run(
                          ["uv", "sync"], cwd=str(p), check=True)))
    return steps


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("project", nargs="?", default=".",
                    help="dossier du projet (défaut : le dossier courant)")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--dry", action="store_true",
                      help="SIMULER la pose : afficher toutes les actions, ne rien toucher")
    mode.add_argument("--install", action="store_true",
                      help="POSER le standard (chaque action annoncée avant exécution)")
    args = ap.parse_args()

    project = Path(args.project).resolve()
    if not project.is_dir():
        print(f"{RED}✗{OFF} {project} n'est pas un dossier")
        return 2

    code = analyse(project)
    if not (args.dry or args.install):
        return code

    steps = plan(project)
    print()
    if not steps:
        print("Rien à faire — le standard est déjà en place.")
        return 0
    label = "PLAN (simulation, rien n'est touché)" if args.dry else "POSE"
    print(f"{label} — {len(steps)} action(s) :")
    for i, (desc, action) in enumerate(steps, 1):
        print(f"  {i}. {desc}")
        if args.install:
            action()
    if args.install:
        print()
        print("Pose terminée — contrôle final :")
        return analyse(project)
    print()
    print("Simulation seulement — relancer avec --install pour appliquer.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
