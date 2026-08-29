# PLAYBOOK — le comment-faire des présentations POSTAIR

Distillé des 120 premiers commits (2026-07-29 → 2026-08-23) et des sessions de
mise au point. **Ici vivent les procédures et les pièges** ; les *règles de
design* vivent dans `design-guideline.md`, la doctrine des tuyaux dans
`CLAUDE.md`, et la vérité des décisions datées reste dans les docstrings et
commits qu'indexe l'annexe. Un état qui change (URLs, versions) n'a pas sa
place ici — une procédure, si.

## 1. Lancer, régler, répéter

```bash
uv run python run-postair.py --kill && uv run python run-postair.py --fresh          # le jeu complet
uv run python run-postair.py --fresh --html                                          # + exports statiques locaux (port 8510)
uv run python run-postair.py --ports-offset 300 --no-browser survey                  # instance isolée (tests, captures)
uv run python _project/tools/check_all.py                                            # LA porte d'avant-répétition
```

- **Rechargement à chaud** : les blocs (`blocks/bck_*.py`) et le `book.py`
  rechargent à la volée. **Tout le reste est en cache serveur** : une édition
  sous `custom/`, `shared-blocks/`, `postair_pack/` ou un changement de version
  de librairie exige `--kill` puis `--fresh`. C'est LE réflexe qui évite de
  conclure « ça ne marche pas » devant du code jamais exécuté.
- Un deck qui **bloque au chargement** (barre figée sur « module N/M ») cache
  presque toujours une exception d'un bloc : `check_all` (ou
  `check_blocks_build.py <module>`) donne le bloc fautif et l'erreur exacte en
  quelques secondes — plus rapide que les logs.
- **Projection** : Chrome dédié lancé avec
  `--autoplay-policy=no-user-gesture-required` (autoplay + son des vidéos) ;
  conception en fenêtre 16:9 (responsive 1920×1080) ; passer une fois sur
  toutes les slides avant la séance (caches, vidéos, QR).
- L'orateur **choisit le jour** dans le sélecteur de la slide de participation
  avant de se tourner vers la salle ; « Custom code… » accepte une campagne
  créée le matin même (QR généré localement).

## 2. Ajouter un module au jeu

1. `modules/postair_<clé>/` : `book.py`, `setup.py`, `blocks/`, `custom/`,
   `static/` — copier le `.streamlit/config.toml` d'opening À L'IDENTIQUE
   (thème sombre + `enableStaticServing` ; trois modules ont tourné blanc-sur-
   blanc en prod faute de ce fichier).
2. Déclarer le module dans `postair_collection/collection.toml` (ordre, titre,
   URL) : le hub **et** la chaîne « Next deck » en dérivent — rien d'autre à
   écrire pour la chaîne, mais ajouter le `blocks/bck_next_module.py` du module
   avec sa clé EXPLICITE (jamais déduite du répertoire courant : le lanceur
   local part de la racine).
3. Créer l'app Coolify (POST `/api/v1/applications/public`, uuids projet/serveur
   dans `.stx-deploy.json`, env `FOLDER` + `STX_SERVE_MODE=dual`, domaine), puis
   reporter l'UUID aux TROIS endroits : `.github/workflows/hetzner-deploy.yml`,
   `.stx-deploy.json`, `DEPLOY.md`. Un placeholder oublié = échec bruyant du
   workflow (voulu).
4. `sync_media.py` : ajouter le module aux listes qui le concernent
   (`MASCOT_MODULES`, `CLIP_MODULES`, `FILM_MODULES`…) — les **films** ne vont
   qu'aux modules qui les projettent (~150 Mo économisés sur survey).

## 3. Blocs et slides — les conventions qui tiennent

- **Un écran/un message = un bloc = une ligne du book** : ordonner, inclure,
  exclure se fait en commentant une ligne. Préfixes triables (`bck_screens_*`,
  `bck_video_*`…), **jamais de numéro dans un nom de fichier** (l'ordre change
  sans cesse ; les `05-progression` visibles dans les blocs sont des *slugs du
  registre*, des identifiants de données).
- **Une slide générique répétée = UN bloc, listé N fois** (NG 2026-08-24,
  vote handsup) : l'ancre d'un marqueur embarque l'index du registre
  (`stx-marker-<slug>-<idx>`), un libellé répété ne collisionne donc JAMAIS —
  ne pas répliquer des fichiers identiques par peur de la collision (erreur
  vécue : 54 blocs pour 3 slides). Marqueur `hidden=True` sur ces blocs :
  les flèches traversent chaque occurrence, la barre latérale ne liste que
  les slides porteuses. Besoin d'ancres nommées par occurrence ? une
  fabrique paramétrable (`st_include` accepte tout objet portant `build()`),
  pas des copies.
- Les ancres TOC de groupe vivent sur le bloc de TÊTE du groupe : exclure ce
  bloc = déplacer son `toc_label` sur le survivant.
- Gabarits de mise en page module-locaux : `screen_slide` (Q14 : capture à
  gauche, cartes à droite — `device`/`theme`/`lang`/`crop`/`split`/
  `image_width`/`zoomImage`/`zoomText`), `media_duo` (deux vidéos carrées,
  pages JUMELLES : la page active lance sa vidéo, la flèche droite passe à la
  jumelle — c'est la pagination qui fait l'autoplay séquencé ; taille par
  `stage_vh=`).
- Les faits d'une slide vivent DANS son bloc (règle R-facts) ; les images IA
  suivent la ligne PAPERCUT (`custom/prompts.py`) en mode éditable avec repli
  tant que l'image managée n'existe pas — jamais de trou projeté.

- **Traduire un module (plan-i18n, recette R1→R9)** : `check_i18n.py
  --inventory <module>` donne le work-order ; d'abord la STRUCTURE (chaque
  littéral devient une feuille `{"en": …}`, régression EN nulle, commit),
  puis les lots de ~8 blocs traduits (V1) → rétro-traduits à l'aveugle (V2)
  → trois lentilles (glossaire, faits, amphi/R3) → assemblage, un commit par
  lot ; puis planche EN/FR pour NG. Un module sort de `I18N_PENDING`
  (`check_i18n.py`) au tag `i18n/<module>-done` : sa parité devient ROUGE.
  L'export EN doit rester identique à `_project/i18n/baseline/` à CHAQUE
  commit (`check_i18n.py --regress`) ; refiger la baseline (`--baseline`)
  seulement quand l'anglais évolue de façon voulue.

## 4. Campagnes médias — regel et matérialisation

Chaîne générale : **publier en amont → regeler le catalogue → purger →
matérialiser → contrôler**. Jamais d'URL ni de chemin écrit à la main ; jamais
d'enrichissement d'un gel à la main (seconde vérité).

```bash
# Captures du parcours (après toute campagne sumvadis)
uv run python _project/tools/build_survey_captures.py --work-order   # constat
uv run python _project/tools/build_survey_captures.py                # regel
rm -rf modules/postair_survey/static/media/captures
uv run python _project/tools/sync_media.py

# Mascottes / clips / films (après une évolution du studio)
uv run python _project/tools/sync_media.py --freeze                  # machine de l'auteur
uv run python _project/tools/check_shared_freeze.py

# Débats (après toute campagne hub) — le contrôle AVAL OBLIGATOIRE
uv run python _project/tools/build_debates_content.py --work-order

# Glossaire (après toute campagne de traduction du hub)
uv run python _project/tools/build_glossary_content.py --work-order

# Vocabulaire des écrans (après tout changement d'intitulé dans l'application sumvadis)
uv run python _project/tools/build_screens_vocabulary.py --work-order
```

- **Quatre gels par chemin avant chaque export** : débats, glossaire, captures,
  vocabulaire des écrans — `check_all.py` porte les quatre en `--work-order`.
- **Le vocabulaire des écrans (septième tuyau, DD-113 O2, 2026-08-29)** : ce
  qu'une slide CITE de l'application — le nom d'un bouton, le titre d'une vue
  que le participant verra sur son téléphone — passe par
  `screen("04-question", "action", lang)` (gel `shared-blocks/static/data/screens.json`
  de `sumvadis/packages/core/assets/ecrans/vocabulaire.json`). Ce que le deck
  dit avec ses mots (marqueur, titre, messages) reste une feuille du bloc. Un
  intitulé faux se corrige DANS sumvadis, puis se regèle ici. La lentille de
  `check_i18n --parity --verbose` signale les feuilles qui recopient un intitulé
  à la ponctuation près — avertissement, à trancher au cas par cas.

- Le gel des captures est **matrice complète + opportuniste** : la matrice de
  base (mobile/desktop × sombre/clair × en/fr/de) est exigée, toute facette
  publiée au-delà (ex. `mobile-complet`, la pleine page) est gelée si présente.
  Une facette absente du catalogue = KeyError bruyant dans la slide — le
  remède est TOUJOURS en amont (publier) puis regel, jamais un contournement.
- Les noms locaux portent l'horodatage de version : « fichier présent = à
  jour » par construction ; purger un dossier de médias est toujours sûr.
- Vidéos : les clips mascottes et les films sont embarqués ; les vidéos de
  figures restent au CDN **sauf** celles que le deck projette
  (`FIGURE_VIDEO_MODULES` dans `sync_media.py`, miroir de `figure_duo()`).
  Motif : une vidéo distante non chargée s'affiche en bandeau écrasé — en
  local, la case est juste immédiatement.

## 5. Déployer

**Push sur `main` = production** (workflow « Deploy to Hetzner » → Coolify,
les 6 services). Le workflow est **séquentiel pur** : un build à la fois,
attente du statut terminal — le lot de 4 d'origine tuait le serveur de build
depuis que les images embarquent ~600 Mo de médias (exit 255 en plein cache
warmup, deux déploiements de suite).

- Un build qui échoue **laisse l'ancien conteneur en ligne** : le site reste
  sain mais périmé — vérifier le *contenu* servi, pas seulement le code 200
  (chercher un marqueur de la nouvelle version dans l'export `/html/`).
- Relance manuelle d'un service :
  `curl "$COOLIFY_URL/api/v1/deploy?uuid=<uuid>" -H "Authorization: Bearer $TOKEN"`
  (identifiants dans `.stx-deploy.env`, UUIDs dans `DEPLOY.md`).
- Chaque conteneur sert le mode **dual** : l'app Streamlit (orateur) et
  l'export statique sous `/html/` (public). En local, `run-postair.py --html`
  reproduit exactement ce couple.

## 6. Incidents connus du CDN `media.sumvadis.ai` (vécu, août 2026)

| Symptôme | Cause vue | Geste |
|---|---|---|
| HTTP 429 en rafale au build | plusieurs builds parallèles matérialisant les mêmes médias | le retry de `sync_media` (5 essais, backoff, `Retry-After`) absorbe ; le déploiement séquentiel évite |
| Corps d'**1 octet** servis en masse | épisode transitoire du proxy (~2 h), résolu seul | re-vérifier en GET PLEIN (magic bytes + taille plancher) avant de conclure à une perte ; ne jamais juger sur un `content-length` de 206 |
| **206 à un GET sans Range**, octets invalides | objet servi corrompu par le proxy | reproduire avec `curl` + `xxd -l 16`, envoyer l'URL exacte à la session sumvadis ; en attendant, rendition de repli si elle est saine |

Leçon générale : les garde-fous de `sync_media` (magic bytes, taille annoncée,
écriture atomique) déplacent la panne du pire moment (l'amphi) au moins cher
(le build) — les conserver tels quels.

## 7. Pièges de code — la liste qui fait gagner une heure

- **`from streamtex import *` masque le builtin `list`** (règle R14) : `[*x]`
  au lieu de `list(x)`, `from __future__ import annotations` pour les
  annotations génériques. Filet : `check_blocks_build.py`.
- **Zoom CSS inerte sur les `%`** (règle R-zoom) — et `display_zoom` du JSON
  managé qui écrase le `width=` du code.
- **Clé de widget stable** : une clé engendrée se réinitialise à chaque rerun
  sous la main de l'orateur (`_SELECTOR_KEY`…).
- **La langue ne se règle pas par widget** : elle est dans l'adresse (`?lang=`),
  posée par le hub et propagée par la chaîne — un deck ouvert « à la main » est en
  anglais tant qu'on n'ajoute pas le suffixe.
- **Un état de séance lu par PLUSIEURS pages vit dans une clé NON-widget**
  (patron à deux clés — bug vécu 2026-08-24, sélecteur de langue handsup) :
  Streamlit PURGE la clé d'un widget dès qu'un rerun se termine sans le
  widget — or en pagination, le widget ne vit que sur sa page. Le widget a
  sa propre clé et recopie son choix via `on_change` dans la clé de séance ;
  symptôme sans le patron : l'état tient UNE page puis retombe au défaut.
- **En mode paginé, seule la page courante s'exécute** : jamais
  `only_cited=True` pour la bibliographie ; et c'est ce qui permet l'autoplay
  séquencé des pages jumelles.
- **`Path.cwd()` interdit pour se repérer** : ancrer sur `__file__` (le
  lanceur part de la racine, le conteneur fait `cd`) — bug vécu sur la chaîne.
- Le `.bib` se lit par streamtex, pas LaTeX : UTF-8 direct, pas d'accolades de
  casse ; clé inconnue = erreur bruyante voulue.
- Un artefact GELÉ ne porte jamais d'adresse `/c/` (règle I3) — uniquement du
  contenu-adressé ou du `/v/` horodaté.
- **`T("chaîne")` lève** : une chaîne nue passée au résolveur de langue est
  une migration inachevée, pas une traduction manquante ; une feuille sans
  `fr` retombe sur l'anglais en séance et c'est `check_i18n --parity` qui la
  signale avant la répétition (règle R-i18n).

## Annexe — index des décisions datées (pointeurs, jamais de copie)

| Décision | Date | Où vit le texte canonique |
|---|---|---|
| Style PAPERCUT (planche s4) | 2026-07-29 | `custom/prompts.py` (opening) + règle des images IA de la guideline |
| Médias servis, jamais inlinés / gels | 2026-08-01→03 | `CLAUDE.md` + docstring `sync_media.py` |
| Règle I3 (jamais `/c/` dans un gel) | 2026-08-03 | `CLAUDE.md` |
| Pattern bib canonique | 2026-08-03/11 | `CLAUDE.md` + règle R-bib |
| Marque DD-35 sur tout média IA | 2026-08-12 | `postair_pack/components/ai_mark.py` + `check_export_media.py` |
| Q14 — captures mobiles, mise en page capture/cartes | 2026-08-14 | docstring `custom/screen_slide.py` (survey) |
| Q15 — écrans d'opérateur en desktop paysage | 2026-08-14 | docstring `bck_screens_regie.py` |
| Écran d'attente = film `axes-intro` | 2026-08-14 | `CLAUDE.md` + `PROVENANCE.md` |
| R-facts — le fait vit dans son bloc | 2026-08-18 | guideline |
| R-balance — bénéfices/risques un-pour-un | 2026-08-19 | guideline |
| Chaîne du jour « C + B allégée » | 2026-08-19 | docstring `shared-blocks/postair_chain.py` |
| Décision D — gel matrice complète des captures | 2026-08-21 | docstring `build_survey_captures.py` |
| Gel opportuniste des facettes hors matrice | 2026-08-23 | docstring `build_survey_captures.py` |
| Films matérialisés seulement où projetés | 2026-08-23 | docstring `sync_media.py` |
| Exception vidéos de figures embarquées (duos) | 2026-08-23 | `CLAUDE.md` + `sync_media.py` |
| Un écran = un bloc ; préfixe pluriel | 2026-08-23 | docstrings `bck_screens_*` + book |
| i18n D1–D4 (feuilles dans le bloc, `block_kwargs`, double export, porte rouge) | 2026-08-28 | règle R-i18n + docstrings `postair_lang.py`, `check_i18n.py` |
| Lot 1 i18n clos (opening, survey, waves, handsup bilingues) ; lot 2 au tag `en-final/<module>` | 2026-08-29 | `_project/i18n/rapport-lot1.md` (local) + `I18N_PENDING` de `check_i18n.py` |
| La langue vit dans l'adresse (`?lang=`) : deux boutons par carte du hub, pas de sélecteur dans les modules | 2026-08-29 | docstring `postair_lang.py` + règle R-i18n |
| streamtex 0.7.26 lève les trois contournements i18n : `<html lang>` posé par l'export (plus de `sed`), `BibConfig.locale` lu par les formateurs (`refs.config()`), cache paginé par langue (warmup EN puis FR au build) | 2026-08-29 | `entrypoint.sh`, `Dockerfile`, `modules/*/custom/refs.py`, règle R-i18n ; streamtex #37–#41 |
| Gel du studio refait (cast v2.3.0 `pole_code`, profils `{_doc, profiles}`) ; le libellé de pôle traduit se cherche PAR CLÉ, jamais par égalité de libellés | 2026-08-29 | `_SHARED/mascots/PROVENANCE.md`, `media_duo._pole_label`, `postair_data.axes()[…]["code"]` |
| Campagne hub du 2026-08-29 absorbée (figures 0.2.0 : `period` feuille, noms FR sans article ; glossaire 103 : `pole.effect.*` ; contrat éditorial v2.7 : 39 citations promues FR/DE, `debate_choice` {en, fr}) — `quote()` apparie sur toute langue et prend le FR du choix éditorial ; effet de pôle lu au glossaire ; baseline EN des débats refaite (référence imprimable sur 39 citations, 4 originaux FR passés en EN) | 2026-08-29 | `build_debates_content.py`, `waves/custom/render.py`, gels régénérés (hub `8e50c813`) |
| Registres et pôles PAR CLÉ : `REGISTERS` = (code, sous-titre feuille, axes), nom au glossaire (`register_name`), `axes(family, lang)` traduit les libellés de pôle ; vidéos de figures par langue (`videos` du gel débats, `FIGURE_VIDEO_LANGS` de `sync_media`) | 2026-08-29 | `postair_data.py`, `survey/bck_axes_registers.py`, `media_duo.py`, `build_debates_content.py` |
| Septième tuyau sumvadis → présentations : vocabulaire des écrans gelé (`build_screens_vocabulary.py` → `screens.json`), `screen(id, role, lang)` pour ce qu'une slide CITE de l'app ; porte `gate_frozen_vocabularies` (glossaire + écrans) ; lentille de recopie dans `check_i18n --parity` | 2026-08-29 | DD-113 (sumvadis), `ECOSYSTEM.md` v1.8, CLAUDE.md « Le troisième amont » |
| Débat rythmé par ÉTAPES (énoncé · pour · contre · mains), jamais par chronomètre — l'orateur tient les 20' en ouvrant deux axes plutôt que trois | 2026-08-29 | docstring `bck_disc_method.py` (debates) |
