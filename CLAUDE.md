# sumvadis-streamtex — les présentations live POSTAIR

Ce dépôt produit les documents projetés de l'**AI Day** de l'Université du Luxembourg
(8, 9 et 10 septembre 2026, trois séances identiques, ~1500 primo-inscrits).

## Carte de l'écosystème POSTAIR / Sumvadis

Ce dépôt est un maillon d'une chaîne de 6 dépôts (fabrique de médias, hub des figures,
studio mascottes, commercials, sumvadis, et ce dépôt). **La carte maintenue — rôles,
chemins absolus, tuyaux, règles transverses — est `ECOSYSTEM.md` à la racine du dépôt
sumvadis** :
`/Volumes/Mac_Data/Win_data/data/backups/Dropbox-nicolas.guelfi@laposte.net/messir Dropbox/Nicolas Guelfi/users/NG/dev-dropbox/dvlpt/eclipse/git/github/sumvadis/ECOSYSTEM.md`
À lire avant toute action qui traverse les frontières de dépôts.

⚠ Ce dépôt vit **hors de la racine `«git»/`** commune aux cinq autres : il est sous
`NG/Projets/AISE/ROS/projects/sumvadis-central/sumvadis-presentations/`.

## Le tuyau amont — sens unique, lecture seule

`postair_debates` est **entièrement data-driven** : aucun nom de figure, aucune
citation, aucune référence n'est écrite à la main. `_project/tools/build_debates_content.py`
joint cinq sources du hub `ai-social-profiles` et gèle le résultat dans
`modules/postair_debates/static/data/content.json`.

- **Le hub est la vérité.** Une correction se fait **là-bas**, jamais ici : elle arrive
  par simple régénération. Rien n'est jamais à écrire dans le hub depuis ce dépôt.
- **Chemins de machine** : `_project/tools/debates-hub.config.local.json` (gitignoré ;
  copier `debates-hub.config.example.json`). Une seule clé est lue, `hub`. Portraits et
  vidéos viennent des renditions publiées dans `great-figures/media-manifest.json`
  (régime CDN DD-28/DEC-035) — jamais du disque de la fabrique.
- L'outil **avertit** quand l'arbre du hub est sale sur `questionnaire/` ou
  `great-figures/` : le gel photographierait un travail en cours. Il n'échoue pas —
  les sessions de campagne régénèrent le registre bien avant de committer.

## Le contrôle aval — obligatoire après toute campagne amont

Le document choisit, parmi les citations éligibles d'une figure, **celle dont la longueur
est la plus proche de 150 caractères**. Ajouter en amont un verbatim plus proche de cette
longueur **déloge silencieusement** la citation projetée (c'est arrivé une fois, sur
Postman). Après toute campagne touchant `evidence/`, `editorial/` ou le registre :

```bash
uv run python _project/tools/build_debates_content.py --work-order
```

Le pied de page doit rester à **0 sans référence imprimable**. Toute autre variation est
à signaler. La commande ne modifie rien : elle lit et écrit sur la sortie standard.

Une figure n'apparaît que si elle porte **un portrait ET une vidéo**, chacun avec
`clearance.channel == "public-ok"` — un portrait seul ne suffit pas.

## Généré / versionné

- `modules/postair_*/static/data/content.json` est **généré**. Ne pas l'éditer à la main :
  régénérer.
- `_project/tools/` **est versionné** — ces outils sont le tuyau, pas du pilotage.
  Le reste de `_project/` (plans, analyses, revues, prompts) reste local par choix.
