#!/usr/bin/env python3
"""Lanceur local des documents POSTAIR — sur le modèle de run-manuals.py
(streamtex-docs).

Lance en local le jeu de documents choisi, chacun sur son port, et ouvre le
navigateur. Chaque instance lancée reçoit les variables STX_URL_* des AUTRES
modules du jeu (lues par bck_home ET par postair_chain) : le hub local navigue
vers les decks locaux, et le bouton « module suivant » de fin de deck chaîne
en local aussi — l'environnement décide, jamais un geste (décision NG
2026-08-19). Les modules absents du jeu gardent leur URL de production, repli
naturel du collection.toml.

Avec ``--html``, le lanceur reproduit en local le mode « dual » du conteneur :
il génère l'export statique de chaque deck (``stx export html``, le geste de
l'entrypoint) APRÈS le lancement des apps, le sert sur le port 8510, et pose
``STX_EXPORT_URL_<KEY>`` — le lien « static HTML version: local » de la
chaîne devient vrai. Sans ``--html``, ce lien retombe silencieusement sur
l'app (Streamlit sert tout chemin inconnu). L'export est un INSTANTANÉ du
lancement : les éditions à chaud n'y apparaissent pas.

Usage :
    uv run python run-postair.py                     # tout (collection comprise)
    uv run python run-postair.py opening genai      # un sous-ensemble
    uv run python run-postair.py --html …           # + exports statiques servis (8510)
    uv run python run-postair.py --list             # noms et ports
    uv run python run-postair.py --kill             # arrêter les documents (par port)
    uv run python run-postair.py --fresh …          # purge caches puis relance
    uv run python run-postair.py --ports-offset 100 # ports décalés (vérifications)
    uv run python run-postair.py --no-browser …     # sans ouvrir le navigateur

Ports 8510-8516 (distincts de run-manuals, 8501-8507 : les deux jeux peuvent
tourner ensemble) ; 8510 = le serveur des exports statiques. Logs sous le
dossier temporaire système.
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
#: Plage de ports 8511-8516 : les quatre decks historiques gardent leur port
#: (des marque-pages et des sessions d'opérateur les connaissent) ; survey,
#: arrivé après (ss12), prend le port suivant de la plage, pas sa place
#: dans l'agenda.
MODULES = {
    "collection": {"path": "modules/postair_collection", "port": 8511},
    "opening": {"path": "modules/postair_opening", "port": 8512},
    "survey": {"path": "modules/postair_survey", "port": 8516},
    "debates": {"path": "modules/postair_debates", "port": 8513},
    "genai": {"path": "modules/postair_genai", "port": 8514},
    "guidelines": {"path": "modules/postair_guidelines", "port": 8515},
    "handsup": {"path": "modules/postair_handsup", "port": 8517},
}

LOG_DIR = Path(tempfile.gettempdir()) / "postair-presentations"

#: Le serveur des exports statiques (``--html``) — un port, tous les modules,
#: même arborescence que ``/app/static-html`` du conteneur.
HTML_PORT = 8510
HTML_DIR = LOG_DIR / "static-html"


def _html_url(name: str) -> str:
    """L'URL de l'export statique local d'un module (convention entrypoint)."""
    base = Path(MODULES[name]["path"]).name          # postair_<key>
    return f"http://localhost:{HTML_PORT}/{base}/{base}.html"


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


def launch(name: str, selected: list[str], html: bool = False) -> subprocess.Popen | None:
    info = MODULES[name]
    port = info["port"]
    log_file = LOG_DIR / f"{name}.log"
    print(f"Lancement {name} (http://localhost:{port})…")
    free_port(port)

    env = os.environ.copy()
    # Chaque instance connaît les URLs LOCALES des autres modules du jeu :
    # les cartes du hub (bck_home) et le bouton « module suivant » de fin de
    # deck (postair_chain) chaînent en local. Modules absents = URL de
    # production, repli naturel du collection.toml. Avec --html, les exports
    # statiques locaux s'annoncent aussi (lien « local » de la chaîne).
    for other in selected:
        if other != name and other != "collection":
            env[f"STX_URL_{other.upper()}"] = f"http://localhost:{MODULES[other]['port']}"
            if html:
                env[f"STX_EXPORT_URL_{other.upper()}"] = _html_url(other)

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


def fresh(selected: list[str]) -> None:
    """Repartir d'un état propre AVANT relance — répond à « est-ce que je
    regarde la bonne version ? » (NG 2026-08-13).

    Purge ce que le poste peut purger : processus, bytecode, et le cache de
    pages streamtex (`.stx_cache` — son hash ne voit ni ``postair_pack``, ni
    ``shared-blocks``, ni ``custom/visuals.py`` : TOC/marqueurs/recherche
    peuvent survivre à une modification de ces couches). Deux caches restent
    HORS de portée d'un script et sont rappelés à l'écran ; le cache des
    médias (``static/media/``) est un cache VOULU (contenu-adressé) et ne se
    vide que sur décision explicite — jamais ici.
    """
    kill_all()
    removed = 0
    roots = [SCRIPT_DIR / MODULES[n]["path"] for n in selected]
    roots += [SCRIPT_DIR / "postair_pack", SCRIPT_DIR / "modules" / "shared-blocks"]
    for root in roots:
        for cache in list(root.rglob("__pycache__")) + list(root.glob(".stx_cache")):
            for f in sorted(cache.rglob("*"), reverse=True):
                f.unlink(missing_ok=True) if f.is_file() else f.rmdir()
            cache.rmdir()
            removed += 1
    print(f"Caches purgés : {removed} dossier(s) (__pycache__, .stx_cache).")
    print("Restent à VOTRE main, dans le navigateur :")
    print("  - recharger l'onglet (F5) — l'éditeur garde ses réglages en session ;")
    print("  - rechargement forcé (Cmd+Shift+R) — le navigateur cache les médias.")
    print("Le cache des médias (static/media/) est contenu-adressé, donc voulu ;")
    print("pour le refaire : vider le dossier puis relancer sync_media.py.")


def kill_all() -> None:
    """Arrête les documents POSTAIR — et RIEN d'autre.

    Ciblé par PORT, jamais par nom de processus : un ``pkill streamlit`` global
    tuait aussi run-manuals (8501-8507) et les documents d'un AUTRE opérateur
    sur la même machine — c'est arrivé le 2026-08-13, popup « Connection
    error » sur tous les onglets de l'auteur pendant une session de
    vérification parallèle.
    """
    ports = sorted([info["port"] for info in MODULES.values()] + [HTML_PORT])
    print(f"Arrêt des documents POSTAIR (ports {ports[0]}-{ports[-1]})…")
    for port in ports:
        free_port(port)
    print("Fait.")


def serve_html() -> subprocess.Popen | None:
    """Le serveur des exports statiques — un ``http.server``, dossier partagé."""
    free_port(HTML_PORT)
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / "html-server.log"
    with open(log_file, "w") as lf:
        proc = subprocess.Popen(
            [sys.executable, "-m", "http.server", str(HTML_PORT),
             "-d", str(HTML_DIR)],
            stdout=lf, stderr=subprocess.STDOUT,
        )
    time.sleep(1)
    if proc.poll() is None:
        print(f"Serveur des exports statiques : http://localhost:{HTML_PORT} "
              f"(PID {proc.pid})")
        return proc
    print(f"   ÉCHEC du serveur statique — voir {log_file}")
    return None


def export_html(selected: list[str]) -> None:
    """Génère les exports statiques des decks du jeu — le geste de l'entrypoint.

    Nettoie d'abord le dossier (un export périmé qui resterait servi serait
    pire qu'un export absent), puis exporte module par module, en séquence —
    chaque export rend le deck entier, comptez plusieurs secondes par module.
    """
    for stale in sorted(HTML_DIR.rglob("*"), reverse=True):
        stale.unlink(missing_ok=True) if stale.is_file() else stale.rmdir()
    for name in selected:
        if name == "collection":
            continue  # le hub se consulte en app ; son export n'a pas d'usage
        module_dir = SCRIPT_DIR / MODULES[name]["path"]
        log_file = LOG_DIR / f"export-{name}.log"
        print(f"Export statique {name}…", end=" ", flush=True)
        t0 = time.time()
        with open(log_file, "w") as lf:
            result = subprocess.run(
                ["uv", "run", "stx", "export", "html",
                 "--output", str(HTML_DIR), "."],
                cwd=str(module_dir), stdout=lf, stderr=subprocess.STDOUT,
            )
        if result.returncode == 0:
            print(f"OK ({time.time() - t0:.0f}s) → {_html_url(name)}")
        else:
            print(f"ÉCHEC — voir {log_file}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("modules", nargs="*", metavar="module",
                    help=f"jeu à lancer parmi {', '.join(MODULES)} (défaut : tout)")
    ap.add_argument("--list", action="store_true", help="liste les modules et ports")
    ap.add_argument("--kill", action="store_true",
                    help="arrête les documents POSTAIR (ciblé par port — ne touche "
                         "ni run-manuals ni les autres opérateurs)")
    ap.add_argument("--no-browser", action="store_true", help="n'ouvre pas le navigateur")
    ap.add_argument("--html", action="store_true",
                    help="génère et sert les exports statiques (port 8510) — le lien "
                         "« static HTML version: local » de la chaîne devient vrai ; "
                         "compte plusieurs secondes d'export par module au lancement")
    ap.add_argument("--fresh", action="store_true",
                    help="arrête tout, purge __pycache__ et .stx_cache, puis relance "
                         "(les caches du NAVIGATEUR restent à rafraîchir : F5 / Cmd+Shift+R)")
    ap.add_argument("--ports-offset", type=int, default=0, metavar="N",
                    help="décale tous les ports de N (ex. 100 → 8611-8615) — pour "
                         "qu'une session de VÉRIFICATION tourne à côté des documents "
                         "de l'auteur sans jamais les toucher (--kill compris)")
    args = ap.parse_args()

    if args.ports_offset:
        global HTML_PORT
        HTML_PORT += args.ports_offset
        for info in MODULES.values():
            info["port"] += args.ports_offset

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
    if args.fresh:
        fresh(selected)
    for name in selected:
        check_module(name)

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    processes: dict[str, subprocess.Popen] = {}
    for name in selected:
        proc = launch(name, selected, html=args.html)
        if proc:
            processes[name] = proc
    if not processes:
        sys.exit("aucun module lancé")

    # Les apps d'abord (rapides, utilisables tout de suite), les exports
    # ensuite : le serveur démarre à vide, les liens « local » se remplissent
    # au fil des exports.
    if args.html:
        serve_html()
        export_html(selected)

    print()
    print("===========================================================")
    print("POSTAIR — documents locaux")
    print("===========================================================")
    for name in MODULES:
        if name in processes:
            print(f"  {name:12s} http://localhost:{MODULES[name]['port']}"
                  f"  (PID {processes[name].pid})")
    if args.html:
        print(f"  {'html':12s} http://localhost:{HTML_PORT}  (exports statiques)")
    print()
    print(f"Logs : {LOG_DIR}")
    print("Arrêt : uv run python run-postair.py --kill")
    print("===========================================================")

    if not args.no_browser:
        first = "collection" if "collection" in processes else next(iter(processes))
        webbrowser.open(f"http://localhost:{MODULES[first]['port']}")


if __name__ == "__main__":
    main()
