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

⚠ Et il vit **dans un dossier Dropbox**. Tout ce qui est propre à une machine reste donc
hors de l'arbre synchronisé : **`.venv` est un lien symbolique** vers
`~/.venvs/sumvadis-streamtex`, et les 400 Mo vivent chez chaque poste. Aucune variable
d'environnement n'est en jeu — `UV_PROJECT_ENVIRONMENT` n'existe qu'en variable globale,
donc il s'appliquerait à *tous* les projets uv de la machine. uv respecte le lien
(`uv sync` installe dans la cible et le conserve) et, si la cible manque, **échoue
bruyamment** au lieu de reconstruire en douce dans Dropbox. Voir `MACHINE.md`.
Un `.venv` réel ici pèse 426 Mo, épingle un interpréteur par chemin absolu, casse sur le
second poste, et fait lire des fichiers périmés pendant les synchronisations — c'est
arrivé le 2026-08-03.

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

Le pied de page doit rester à **0 sans référence imprimable** et à **0 problème(s) de
gel .bib**. Les deux compteurs du milieu (« sans traduction française », « citations
sans clé BibTeX promue ») sont une dette connue qui se résorbe par campagnes hub —
toute autre variation est à signaler. La commande ne modifie rien : elle lit et écrit
sur la sortie standard.

Une figure n'apparaît que si elle porte **un portrait ET une vidéo**, chacun avec
`clearance.channel == "public-ok"` — un portrait seul ne suffit pas.

**RÈGLE I3 (sumvadis design/11, lot L5, 2026-08-03) — un artefact GELÉ ne
porte JAMAIS d'adresse de concept `/c/…`.** Les manifestes de ce dépôt
(`media-catalogue.json`, `content.json`) et l'image Docker vivent sous le
contrat « fichier présent = à jour, jamais revalidé » : une adresse `/c/`
(dernier segment stable, contenu changeant) y servirait du périmé en silence
et créerait des collisions de noms locaux. Dans un gel : uniquement des
adresses contenu-adressées (l'actuel) ou des adresses de VERSION
`/v/…/<horodatage>` — jamais `/c/`.

## Le second amont — le gel du studio

`modules/shared-blocks/static/_SHARED/mascots/` est une **copie gelée** de
`mascoties/shared/`, faite à la main : c'est le seul tuyau de la chaîne sans outil de
copie. Depuis le 2026-08-14 il n'y reste que **les 3 manifestes** — les 36 webp
viennent du CDN, les clips passent par `media-catalogue.json` (sections `crew` et
`films` comprises), et le dernier master en sursis (`solyo_optimism_en.mp4`) a été
purgé quand l'écran d'attente est passé au film `axes-intro` (voir `PROVENANCE.md`).
Contrôle de fidélité :

```bash
uv run python _project/tools/check_shared_freeze.py
```

Il ne copie rien. Il compare les manifestes octet par octet, rapporte l'état de
signature C2PA des deux côtés et signale les clips sans source. **Ne jamais enrichir
un fichier du gel à la main** : ce serait créer une seconde vérité. Une évolution se
demande au studio, puis le gel se refait.

## Le thème — un module = un `.streamlit/config.toml`

Le conteneur fait `cd` dans le module avant de lancer Streamlit : le thème
sombre vient du `config.toml` LOCAL au module, jamais d'un défaut global.
**Tout nouveau module copie celui d'opening à l'identique** (thème +
`enableStaticServing`, qui rend aussi les médias visibles en lancement
local). Constaté le 2026-08-13 : genai, guidelines et collection ont tourné
en thème clair en production — textes blancs sur fond blanc — parce que ce
fichier manquait.

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
- **L'écran d'attente joue le film `axes-intro`** (décision NG 2026-08-14) : une
  *production* du studio (« Les 9 axes — la phrase mémo », 68 s), déclarée dans la
  section `films` de `cartes-design.json` avec des adresses de VERSION `/v/…`
  (règle I3 — jamais `/c/`), gelée au catalogue et matérialisée comme les clips
  sous `static/media/clips/`. Les blocs la nomment par `postair_data.film_clip`.
  L'ancien arbitrage sur le master Solyo est clos : master purgé le même jour.

## Les références bibliographiques — le pattern canonique streamtex, pour TOUS les modules

**Règle (2026-08-11)** : toute référence d'une présentation suit le mécanisme natif de
la librairie, dans sa **forme** comme dans sa **provenance**. Concrètement :

1. **Un `.bib` par module**, chargé une seule fois par
   `st_book(bib_sources=[...], bib_config=BibConfig(...))` — jamais de chargement
   manuel dans un bloc.
2. **Le code de citation dans le texte VISIBLE de la slide**, juste après
   l'affirmation : `cite("clé")` (ou le wrapper bruyant du module). Jamais de phrase
   bibliographique imprimée dans une slide ni dans un panneau tooltip — la phrase
   complète vit dans la carte au survol et sur la page References. Jamais de `cite()`
   *dans* un panneau `st_hover_tooltip` : hover-dans-hover, fragile en projection.
3. **La carte de survol calibrée projection** via l'API `BibConfig` (≥ 0.7.20) :
   `cite_color`, `card_width="780px"`, `card_font_scale=2.0`,
   `card_css="#stx-bib-card{max-height:70vh;overflow-y:auto;}"`. Le défaut (420 px,
   corps ~12 px) est illisible en amphi.
4. **Page References compatible pagination** : en mode paginé, `get_cited_entries()`
   est vide (seule la slide courante s'exécute) — donc tout enregistrer
   (`only_cited=False`) ou nommer les clés explicitement. Jamais `only_cited=True`
   dans un deck paginé.
5. **Clé inconnue = erreur bruyante en amont** (le natif se contente d'un warning et
   affiche `[clé?]` à l'écran — inacceptable découvert en séance).

Limite connue (streamtex 0.7.22, constatée 2026-08-11) : la carte au survol est
injectée par `st_book` (application Streamlit — le mode de projection). L'export HTML
statique enrichit les runtimes marker/TOC mais PAS le scaffold bib : le code s'y
affiche sans carte. Même limite pour le deck DCS. Une évolution se demande à la
librairie (`enrich_export_html`), jamais en contournement local.

Implémentations de référence, à consulter avant tout travail sur les références :
- le deck DCS : `messir Team Folder/users/Nicolas/DCS/260630-DCS-annual-meeting/slides/v01/projects/dcs-annual-meeting-slides` (`book.py`, `custom/deck_config.py`, `custom/appendix_refs.py` pour l'annexe paginée) ;
- le manuel officiel : `github/streamtex-dev/streamtex-docs/manuals/stx_manual_advanced` (chapitre « Bibliography & References », exemples sous `static/examples/bib/`).

Pourquoi cette section existe : les deux modules POSTAIR ont dévié en août 2026
(phrases APA imprimées dans les tooltips d'opening, chaînes gelées sans `.bib` dans
debates) parce qu'aucun pointeur d'ici ne menait aux implémentations de référence.
Pour `postair_debates`, le `.bib` du module est **GELÉ et généré** par
`build_debates_content.py` depuis les `.bib` du hub — même contrat que
`content.json` : ne jamais l'éditer à la main, régénérer.

## Généré / versionné

- `modules/postair_*/static/data/content.json` est **généré**. Ne pas l'éditer à la main :
  régénérer.
- `_project/tools/` **est versionné** — ces outils sont le tuyau, pas du pilotage.
  Le reste de `_project/` (plans, analyses, revues, prompts) reste local par choix.
