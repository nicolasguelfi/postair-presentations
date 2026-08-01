# postair_opening — Design guideline

Héritée de FC-260507 (R1-R13) et adaptée au duo « canvas navy + mascottes Pixar ».
À respecter dans chaque block ; annoter `# @guideline: postair-minimal`.

- **R0 Maximiser l'espace (règle amphi, NG 2026-07-29)** : un slide ne doit JAMAIS être vide à 80 % — les images et les polices prennent tout l'espace disponible ; les participants sont loin de l'écran (amphi 500-1500 places). Vidéo/projection = pleine largeur (`page_fill_full`).
- **R1 Canvas** : navy `#1A1A2E`, 16:9, `page_fill_top|center|full` (88vh), marges minimales, `page_width=100`.
- **R2 Typo** : échelle indexée uniquement (`var(--stx-scale-K)`) via le DS ; **base document 30pt** (ScaleConfig) ⇒ bullet ≈60pt, titre ≈80pt, hero ≈120pt. Jamais de `pt` littéral dans un block. Tailles identiques pour les éléments de même rôle (ex. les deux pôles d'un axe).
- **R3 Texte** : max 8 mots par puce (idéal 4-7), max 5 puces ; **exactement un keyword teal par puce** (`s.project.titles.keyword` en tuple).
- **R4 Tooltip** : `st_info_tooltip` (wrapper palette) immédiatement après le titre, cellule 8 % d'une grille `92% 8%` ; **cadre = 2/3 de la fenêtre (66vw × 66vh), police base 4.5vw** (constantes du DS) ; contenu complet sans limite — chaque slide est autosuffisante en lecture.
- **R4b Grilles** : compositions PLATES — une seule grille par slide, jamais de grilles responsives imbriquées ; les compositions répétées (tableaux d'axes, cartes) vivent dans des composants du pack (`postair_pack.components.*`).
- **R5 Couleurs** : sémantique stable — bleu=cadrage, teal=keyword, **ambre=UN accent focal par slide**, corail=humain/débat. Jamais d'ambre en fond.
- **R6 Mascottes** : WebP détourés (`_SHARED/mascots/web/`), jamais les `.png` du cast (JPEG sans transparence) ; une mascotte = une posture, nom affiché en caption.
- **R7 Vidéos** : lancement par geste opérateur (autoplay+son bloqué par navigateur) ; `st_space("v","30vh")` après un sous-slide vidéo.
- **R8 Images IA** : **style PAPERCUT** (décision NG 2026-07-29, planche stylepostair s4) — collage papier découpé, couleurs vives et joyeuses, silhouettes de dos, IA = soleil/orbe ambre papier. Prompts = `AI_PREFIX + scène + AI_SUFFIX_*` (custom/prompts.py) ; `alt=` descriptif ; nom managé `<cat>_<subject>` ; **affichage 70 % par défaut** (`display_zoom: 70` dans la métadonnée). Architecture UL = photo Belval en base img2img (jamais publiée).
- **R8b Mascottes** : taille de référence −20 % (axis_stack `min(12.8vw, 20.8vh)`, Medio `min(16vw, 33.6vh)`).
- **R9 Multi-slides** : `st_slide_break(marker_label=…)` après fermeture du `st_block`.
- **R10 Nommage — AUCUN numéro dans le code** (durci NG 2026-08-01) : `bck_<categorie>_<topic>.py`, et la règle vaut aussi pour les **docstrings**, les **commentaires** et surtout les **libellés de marqueurs** (vus par l'orateur dans la navigation) et les références à ces règles-ci (citer le nom, pas le `RNN`). Motif : en phase d'analyse et de conception la numérotation change des dizaines de fois — la maintenir dans le code est intenable et devient faux au premier remaniement, alors qu'un nom de contenu reste vrai. L'ordre de lecture vit dans la liste passée à `st_book`. La correspondance plan ↔ blocs vit dans **une seule table**, dans `_project/plans/plan-<module>.md`.
- **R11 stx-only** : jamais de HTML/CSS brut dans un block (composition de `Style` ; `st_html` réservé aux widgets partagés).
- **R12 Speaker notes** : discours complet dans le docstring du block.
- **R13 Data-driven** : tout contenu issu du questionnaire/cast passe par `postair_data` (pas de copier-coller de labels).
- **R14 Annotations de type dans un block** : `from streamtex import *` **masque le builtin `list`** (le module `streamtex/list.py`, celui de `st_list`). Une annotation `-> list[dict]` lève alors `TypeError: 'module' object is not subscriptable` **à l'import**, donc avant toute exécution. Tout block qui annote avec un générique doit ouvrir par `from __future__ import annotations`, qui laisse les annotations non évaluées. Constaté en production le 2026-08-01.
