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

## Le second amont — le gel du studio

`modules/shared-blocks/static/_SHARED/mascots/` est une **copie gelée** de
`mascoties/shared/`, faite à la main : c'est le seul tuyau de la chaîne sans outil de
copie. Depuis le 2026-08-02 il n'y reste que **les 3 manifestes et les 4 clips** — les
36 webp sont sortis du dépôt et viennent du CDN (cf. §Les médias). Les clips restent
faute d'entrée au catalogue amont. Contrôle de fidélité :

```bash
uv run python _project/tools/check_shared_freeze.py
```

Il ne copie rien. Il compare les manifestes octet par octet, rapporte l'état de
signature C2PA des deux côtés et signale les clips sans source. **Ne jamais enrichir
un fichier du gel à la main** : ce serait créer une seconde vérité. Une évolution se
demande au studio, puis le gel se refait.

## Les médias — servis, jamais inlinés, jamais dans git

**Aucun média dans git.** Les octets sont matérialisés **au build** par
`_project/tools/sync_media.py` depuis les catalogues amont, sous
`modules/<module>/static/media/`, et servis par le conteneur lui-même : pendant la
séance, aucun appel au CDN.

**Un bloc ne passe jamais un chemin de fichier à `st_image`.** La librairie encode en
base64 tout fichier qu'elle trouve sur le disque — les 54 portraits pèsent 2,7 Ko en URL
contre ~23 Mo inlinés. `configure_image_path("app/static/media")` dans chaque `book.py`
fait sortir les URI en URL relatives, servies par nginx depuis le disque (donc visibles
même en mode static-only).

- **Recharger tout** : vider `modules/<module>/static/media/`, relancer l'outil. Les URL
  sont content-adressées — un fichier présent **est** à jour, sans revalidation.
- **Le catalogue des mascottes est GELÉ** dans `_SHARED/media-catalogue.json` (8 Ko
  d'URL) : le build Coolify tourne en CI, sans accès aux dépôts privés. Ce qui est
  versionné est la *désignation* des médias, jamais les médias. Regel :
  `sync_media.py --freeze` (machine de l'auteur).
- **Les vidéos de figures restent au CDN** : 51 masters de 12 Mo, ouverts deux ou trois
  fois dans la séance ; les embarquer coûterait 612 Mo pour une interaction ponctuelle.
- **Les clips de mascottes, eux, sont embarqués** : les 72 renditions « Postures »
  (36 mascottes × 2 langues) pèsent 24 Mo au total et sont matérialisées depuis le
  catalogue. L'écran d'attente tourne **vingt minutes devant la salle qui se remplit** —
  le pire moment possible pour dépendre du réseau. Le deck nomme une mascotte
  (`postair_data.mascot_clip`), jamais un fichier.
- **Le build n'a plus besoin d'aucun dépôt privé.** Depuis le catalogue v2.2.0
  (2026-08-03), les 2 modérateurs sont publiés au CDN dans une section `crew`, sœur des
  36 `assets`. Le contournement qui les copiait du studio est retiré : `sync_media.py`
  ne lit le studio que pour `--freeze`. Ce que vous validez en local est donc
  byte-identique à ce qui se déploie, sans exception.
- **Un bloc ne code jamais un chemin de média en dur.** Il demande une mascotte par son
  nom (`postair_data.mascot`). Trois slides portaient une URI écrite à la main vers des
  fichiers partis au CDN et affichaient une image manquante — trouvées le 2026-08-03 en
  contrôlant que chaque `src` de l'export pointe un fichier présent. Ce contrôle vaut
  d'être refait après toute campagne média.
- **Exception assumée** : les illustrations produites pour ces présentations restent
  versionnées ici et ne vont jamais au CDN.
- **Une décision en attente** : `_SHARED/mascots/videos/solyo_optimism_en.mp4` (2,9 Mo)
  est le master de l'écran d'attente, en 1080×1080 à 1,9 Mb/s ; la rendition du CDN
  désormais utilisée est en 720×720 à 295 kb/s. Le fichier est conservé le temps que
  l'auteur juge la rendition en projection. Si elle tient, il part ; sinon, la
  demande va à `commercials` — pas de fichier copié à la main en guise de réponse.

## Généré / versionné

- `modules/postair_*/static/data/content.json` est **généré**. Ne pas l'éditer à la main :
  régénérer.
- `_project/tools/` **est versionné** — ces outils sont le tuyau, pas du pilotage.
  Le reste de `_project/` (plans, analyses, revues, prompts) reste local par choix.
