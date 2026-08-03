# Une machine, un environnement — à faire UNE fois par poste

Ce dépôt vit **dans un dossier Dropbox**. Un environnement Python n'y a pas sa
place : il n'est pas portable, et deux postes se battraient pour les mêmes
fichiers.

## Le problème, mesuré

`.venv/` pesait **426 Mo** et était synchronisé (attribut `com.dropbox.attrs`
présent, aucune exclusion — `.gitignore` n'y peut rien, git et Dropbox ne se
parlent pas). Il épingle un interpréteur par **chemin absolu** :

```
home = /Users/<vous>/.local/share/uv/python/cpython-3.13.7-macos-aarch64-none/bin
```

Binaires compilés pour une architecture, chemins absolus, lien vers un
interpréteur installé ailleurs : ça marche sur le poste qui l'a construit et
casse sur l'autre. Et pendant une synchronisation, un processus peut lire un
fichier périmé — c'est ce qui a fait exécuter un `book.py` fantôme le
2026-08-03, cinq minutes après sa réécriture.

## La solution : `.venv` est un lien

```
.venv -> /Users/nicolas.guelfi/.venvs/sumvadis-streamtex
```

Le lien est dans le dépôt (quelques octets, identique sur toutes les machines) ;
les 400 Mo vivent chez chaque poste. **Aucune variable d'environnement**, rien
de global, rien à configurer dans le shell.

Pourquoi pas `UV_PROJECT_ENVIRONMENT` : il n'existe qu'en **variable
d'environnement**, jamais en clé de configuration par projet — vérifié sur
uv 0.9.8, `project-environment` n'est pas dans la liste des clés acceptées de
`uv.toml` ni de `[tool.uv]`. Exporté dans `~/.zshrc`, il s'appliquerait donc à
**tous** vos projets uv, qui pointeraient tous le même dossier.

### Ce que uv fait du lien (vérifié le 2026-08-03, uv 0.9.8)

| situation | comportement |
|---|---|
| `uv sync` | installe **dans la cible**, et **conserve le lien** |
| `uv run`, `stx run`, `stx export` | empruntent le lien sans rien savoir |
| cible absente (machine neuve) | **échoue bruyamment** : `failed to create directory .venv: File exists` |

Ce dernier point est le plus important : uv ne reconstruit **jamais** en douce
un environnement dans le dossier synchronisé. Il s'arrête et le dit.

## Sur une machine neuve

Le lien arrive **par Dropbox** — quelques octets, il est là avant vous. Il
reste donc à créer sa cible :

```bash
mkdir -p ~/.venvs/sumvadis-streamtex
cd <ce dépôt> && uv sync
```

C'est tout.

**Le lien n'est PAS versionné**, et ne doit pas l'être : il porte un chemin
absolu vers un dossier personnel, qui n'a rien à faire dans git. Dropbox le
distribue déjà entre les postes ; git n'a pas à s'en mêler. `.gitignore` le
couvre — sans barre finale, sinon le motif ne viserait que les vrais dossiers
et le lien serait proposé au commit.

Sur un clone git **hors Dropbox**, il n'y a donc pas de lien : soit on le
recrée (`ln -s ~/.venvs/<projet> .venv`), soit on laisse uv créer un vrai
`.venv` — hors du dossier synchronisé, il ne gêne personne.

⚠ Le chemin absolu suppose le même nom de compte sur tous les postes. Si un
jour ce n'est plus le cas, uv le dira avec l'erreur ci-dessus : refaire le
lien avec le bon chemin.

## Les autres dossiers propres à la machine

`__pycache__/`, `.stx_cache/`, `modules/*/static/media/` sont eux aussi
propres au poste et se reconstruisent. S'ils encombrent la synchronisation :

```bash
xattr -w com.dropbox.ignored 1 <dossier>
```

C'est le mécanisme officiel d'exclusion de Dropbox — le dossier reste sur le
disque, il n'est plus synchronisé.

## Le déploiement n'est pas concerné

Le `Dockerfile` fait son `uv sync` dans `/app`, hors de tout dossier
synchronisé, et rien dans le dépôt n'écrit `.venv` en dur (vérifié). La
production ignore tout de ce qui précède.
