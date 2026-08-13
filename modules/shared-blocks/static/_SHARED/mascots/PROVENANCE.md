# Provenance des médias gelés

Ce dossier est une **copie gelée**. Rien n'y est produit : tout descend d'une source
de vérité, et cette page dit laquelle. Convention DD-27 de l'écosystème : toute copie
inter-dépôt porte sa provenance et son empreinte.

Rafraîchi le **2026-08-02** pour une raison de conformité : les 36 images du gel étaient
servies **sans manifeste C2PA** (la copie datait d'avant le re-signage du 31/07), alors
que ce support est déployé sur le web. L'article 50 du règlement européen s'applique
depuis le 02/08/2026 : une image générée par IA servie publiquement doit porter une
divulgation lisible par machine.

## Les 36 cartes (`web/`)

Source : `mascoties/shared/cartes/web/` — **identiques à l'octet près**, 36/36 signées
C2PA `RIGHT-ON-SKILL`, `digitalSourceType = trainedAlgorithmicMedia`.

## Les clips (`videos/`) — le dossier a disparu (2026-08-14)

Il ne restait qu'un fichier en sursis, `solyo_optimism_en.mp4` (master 1080×1080 de
l'ancien écran d'attente, gardé le temps de juger la rendition CDN en projection).
La décision est tombée autrement : **l'écran d'attente joue désormais le film
`axes-intro`** (« Les 9 axes — la phrase mémo », production du studio, section
`films` de `cartes-design.json`, adresses de VERSION `/v/…` — règle I3),
matérialisé comme tous les clips par `_project/tools/sync_media.py` sous
`<module>/static/media/clips/`. L'arbitrage Solyo est devenu sans objet ; le
master a été purgé, décision NG du 2026-08-14. Le gel ne contient plus que les
trois manifestes.

## Pour rafraîchir

- **Les images** : recopier `mascoties/shared/cartes/web/*.webp` — elles sont déjà signées.
- **Les clips** : copier le master voulu depuis `commercials`, puis signer LA COPIE avec
  `augmented-student/_tools/embed_c2pa.py` (idempotent : re-signer empilerait un second
  manifeste). **Ne jamais signer un master de release.**
