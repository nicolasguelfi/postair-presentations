#!/usr/bin/env python3
"""Lanceur local des documents POSTAIR — sur le modèle de run-manuals.py
(streamtex-docs).

Lance en local le jeu de documents choisi, chacun sur son port, et ouvre le
navigateur. Quand la collection fait partie du jeu, ses cartes pointent vers
les instances LOCALES (variables STX_URL_* lues par bck_home) — le hub local
navigue donc vers les decks locaux, pas vers la production.

Usage :
    uv run python run-postair.py                     # tout (collection comprise)
    uv run python run-postair.py opening genai      # un sous-ensemble
    uv run python run-postair.py --list             # noms et ports
    uv run python run-postair.py --kill             # arrêter tous les streamlit
    uv run python run-postair.py --no-browser …     # sans ouvrir le navigateur

Ports 8511-8515 (distincts de run-manuals, 8501-8507 : les deux jeux peuvent
tourner ensemble). Logs sous le dossier temporaire système.
"""

from __future__ import annotations

import argparse
import os
import signal
import subprocess
import sys
import tempfile
import time
import webbrowser
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

#: Ordre d'affichage = ordre de l'agenda du jour, collection en tête.
MODULES = {
    "collection": {"path": "modules/postair_collection", "port": 8511},
    "opening": {"path": "modules/postair_opening", "port": 8512},
    "debates": {"path": "modules/postair_debates", "port": 8513},
    "genai": {"path": "modules/postair_genai", "port": 8514},
    "guidelines": {"path": "modules/postair_guidelines", "port": 8515},
}

LOG_DIR = Path(tempfile.gettempdir()) / "postair-presentations"


def check_module(name: str) -> None:
    path = SCRIPT_DIR / MODULES[name]["path"]
    if not (path / "book.py").is_file():
        sys.exit(f"book.py introuvable pour {name} : {path}")


def free_port(port: int) -> None:
    """Libère le port (macOS/Linux : lsof ; Windows : netstat)."""
    if sys.platform == "win32":
        try:
            out = subprocess.run(["netstat", "-ano", "-p", "TCP"],
                                 capture_output=True, text=True, timeout=5).stdout
            for line in out.splitlines():
                if f":{port}" in line and "LISTENING" in line:
                    pid = line.strip().split()[-1]
                    if pid.isdigit():
                        subprocess.run(["taskkill", "/F", "/PID", pid],
                                       capture_output=True, timeout=5)
        except Exception:
            pass
        return
    try:
        pids = subprocess.run(["lsof", "-ti", f":{port}", "-sTCP:LISTEN"],
                              capture_output=True, text=True, timeout=5).stdout.split()
        if pids:
            print(f"   port {port} occupé (PID {' '.join(pids)}) — arrêt…")
            for pid in pids:
                try:
                    os.kill(int(pid), signal.SIGTERM)
                except (ProcessLookupError, ValueError):
                    pass
            time.sleep(2)
    except FileNotFoundError:
        pass


def launch(name: str, selected: list[str]) -> subprocess.Popen | None:
    info = MODULES[name]
    port = info["port"]
    log_file = LOG_DIR / f"{name}.log"
    print(f"Lancement {name} (http://localhost:{port})…")
    free_port(port)

    env = os.environ.copy()
    if name == "collection":
        # Les cartes du hub local pointent vers les instances locales du jeu
        # lancé ; les modules absents gardent leur URL de production (repli
        # naturel du collection.toml).
        for other in selected:
            if other != "collection":
                env[f"STX_URL_{other.upper()}"] = f"http://localhost:{MODULES[other]['port']}"

    with open(log_file, "w") as lf:
        proc = subprocess.Popen(
            ["uv", "run", "streamlit", "run",
             str(SCRIPT_DIR / info["path"] / "book.py"),
             "--server.port", str(port),
             "--server.headless", "true",
             "--logger.level=warning"],
            stdout=lf, stderr=subprocess.STDOUT, cwd=str(SCRIPT_DIR), env=env,
            **({} if sys.platform != "win32"
               else {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP}),
        )
    time.sleep(2)
    if proc.poll() is None:
        return proc
    print(f"   ÉCHEC — dernières lignes de {log_file} :")
    try:
        for line in log_file.read_text(encoding="utf-8").splitlines()[-15:]:
            print(f"   {line}")
    except OSError:
        pass
    return None


def kill_all() -> None:
    print("Arrêt de tous les processus streamlit…")
    if sys.platform == "win32":
        subprocess.run(["taskkill", "/F", "/IM", "streamlit.exe"],
                       capture_output=True, timeout=5)
    else:
        subprocess.run(["pkill", "-f", "streamlit run"],
                       capture_output=True, timeout=5)
    # Le SIGTERM met une à deux secondes à aboutir : on VÉRIFIE port par port
    # au lieu d'annoncer un arrêt qu'on n'a pas constaté.
    time.sleep(2)
    for name, info in MODULES.items():
        free_port(info["port"])
    print("Fait.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("modules", nargs="*", metavar="module",
                    help=f"jeu à lancer parmi {', '.join(MODULES)} (défaut : tout)")
    ap.add_argument("--list", action="store_true", help="liste les modules et ports")
    ap.add_argument("--kill", action="store_true", help="arrête tous les streamlit")
    ap.add_argument("--no-browser", action="store_true", help="n'ouvre pas le navigateur")
    args = ap.parse_args()

    if args.list:
        for name, info in MODULES.items():
            print(f"  {name:12s} {info['path']:35s} http://localhost:{info['port']}")
        return
    if args.kill:
        kill_all()
        return

    selected = args.modules or list(MODULES)
    unknown = [m for m in selected if m not in MODULES]
    if unknown:
        sys.exit(f"module(s) inconnu(s) : {', '.join(unknown)} — voir --list")
    for name in selected:
        check_module(name)

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    processes: dict[str, subprocess.Popen] = {}
    for name in selected:
        proc = launch(name, selected)
        if proc:
            processes[name] = proc
    if not processes:
        sys.exit("aucun module lancé")

    print()
    print("===========================================================")
    print("POSTAIR — documents locaux")
    print("===========================================================")
    for name in MODULES:
        if name in processes:
            print(f"  {name:12s} http://localhost:{MODULES[name]['port']}"
                  f"  (PID {processes[name].pid})")
    print()
    print(f"Logs : {LOG_DIR}")
    print("Arrêt : uv run python run-postair.py --kill")
    print("===========================================================")

    if not args.no_browser:
        first = "collection" if "collection" in processes else next(iter(processes))
        webbrowser.open(f"http://localhost:{MODULES[first]['port']}")


if __name__ == "__main__":
    main()
