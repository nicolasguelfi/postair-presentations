# `.venv` — pourquoi c'est un lien symbolique, et comment ça marche

> Aide-mémoire du mécanisme décidé le 2026-08-03 (le détail historique et les
> mesures vivent dans `MACHINE.md`). Rien à faire au quotidien : ce fichier
> explique, il ne prescrit qu'un geste **une fois par machine neuve**.

## Le problème

Ce dépôt vit **dans un dossier Dropbox**, partagé entre plusieurs machines.
Un environnement Python réel n'y a pas sa place :

- il pèse ~400 Mo et Dropbox le synchroniserait intégralement ;
- il épingle un interpréteur par **chemin absolu** et des binaires compilés
  pour une architecture — construit sur un poste, il casse sur l'autre ;
- pendant une synchronisation, un processus peut lire un fichier **périmé**
  (vécu : un `book.py` fantôme exécuté cinq minutes après sa réécriture).

## Le mécanisme

`.venv` n'est **pas un dossier** : c'est un **lien symbolique** vers un
dossier local à chaque machine, HORS de Dropbox :

```
.venv -> /Users/<vous>/.venvs/sumvadis-streamtex
```

- **Le lien** (quelques octets) vit dans le dépôt : il est synchronisé par
  Dropbox et versionné par git — identique sur toutes les machines.
- **L'environnement** (les ~400 Mo) vit à la cible du lien, chez chaque
  poste. Deux machines n'écrivent jamais dans le même dossier.
- **Aucune variable d'environnement, aucune configuration shell.**
  (`UV_PROJECT_ENVIRONMENT` a été écarté : global à la machine, il
  détournerait TOUS les projets uv vers le même dossier — vérifié uv 0.9.8,
  pas de clé par projet.)

### Ce que `uv` fait du lien (vérifié uv 0.9.8)

| Situation | Comportement |
|---|---|
| `uv sync` | installe **dans la cible** du lien, et **conserve** le lien |
| `uv run …`, `stx run`, `stx export` | empruntent le lien sans rien savoir |
| cible absente (machine neuve) | **échec bruyant** (`failed to create directory .venv: File exists`) — uv ne reconstruit JAMAIS en douce dans Dropbox |

L'échec bruyant est une **protection voulue** : ne pas le « réparer » par un
script qui recréerait la cible en silence.

## Machine neuve : le seul geste (une fois)

Le lien est déjà là (arrivé par Dropbox). Il reste à créer sa cible :

```bash
mkdir -p ~/.venvs/sumvadis-streamtex
cd "<ce dépôt>" && uv sync
```

⚠ Le lien code le nom d'utilisateur (`/Users/nicolas.guelfi/…`). Sur une
machine dont le compte porte un autre nom, créez la cible **au chemin que le
lien attend** (ou faites de ce chemin un lien local vers votre vrai dossier).

## Détail git

- `.gitignore` contient `.venv` **sans barre finale** : avec `/`, la règle ne
  viserait que les vrais dossiers et laisserait passer un `.venv` réel créé
  par accident sur un poste mal amorcé.
- Le lien lui-même n'est **pas versionné** : c'est **la synchronisation**
  (Dropbox) qui le porte d'une machine à l'autre. Si un projet doit aussi
  voyager par git nu (clone hors Dropbox), un `git add -f .venv` versionne le
  lien en plus — facultatif, hors du standard de ce dépôt.

## L'outil

`_project/tools/venv_standard.py` vérifie et pose le standard dans
n'importe quel projet :

```bash
uv run python _project/tools/venv_standard.py [chemin]            # analyse (ne touche à rien)
uv run python _project/tools/venv_standard.py [chemin] --dry      # simule la pose, action par action
uv run python _project/tools/venv_standard.py [chemin] --install  # pose le standard (un .venv réel est ÉCARTÉ, jamais supprimé)
```

---

## Annexe — reproduire le mécanisme dans un NOUVEAU projet Python

Les commandes complètes, dans l'ordre, pour un projet uv `<projet>` vivant
dans Dropbox (ou tout dossier synchronisé) :

```bash
# 0. Se placer dans le projet
cd "<chemin du projet>"

# 1. Si un .venv RÉEL existe déjà : vérifier ce que c'est, puis le retirer
ls -la .venv            # un dossier ? un lien ? — regarder AVANT de supprimer
rm -rf .venv            # seulement si c'est un vrai dossier à remplacer

# 2. Créer la cible HORS du dossier synchronisé (une par machine)
mkdir -p ~/.venvs/<projet>

# 3. Créer le lien symbolique DANS le projet (chemin absolu de la cible)
ln -s ~/.venvs/<projet> .venv

# 4. git : ignorer .venv (sans barre finale — couvre lien ET dossier).
#    Le lien voyagera par la synchronisation ; le versionner en plus est
#    FACULTATIF (utile seulement si le projet voyage aussi par git nu) :
printf '%s\n' '.venv' >> .gitignore
git add .gitignore
# git add -f .venv        # ← facultatif (hors standard)

# 5. Construire l'environnement dans la cible, à travers le lien
uv sync

# 6. Vérifier : le lien tient, l'environnement est dehors
ls -la .venv                            # → .venv -> ~/.venvs/<projet>
uv run python -c "import sys; print(sys.prefix)"   # → /Users/<vous>/.venvs/<projet>

# 7. Committer
git commit -m "environnement : .venv devient un lien vers ~/.venvs/<projet> (hors Dropbox)"
```

Sur **chaque autre machine** du projet, ensuite (le lien arrive par
Dropbox/git) :

```bash
mkdir -p ~/.venvs/<projet>
cd "<chemin du projet>" && uv sync
```
