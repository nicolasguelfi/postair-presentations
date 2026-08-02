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

## Les clips (`videos/`) — un seul reste, et il est en sursis

Source : le dépôt **`sumvadis-commercials`**, série « Postures », release `v02`. C'est un
dépôt DIFFÉRENT du studio — d'où le verdict « orphelin » de `check_shared_freeze.py`, qui
ne cherche que dans `mascoties`.

**Ce dossier n'a plus lieu d'être.** Depuis le 2026-08-02, `commercials` publie les
72 renditions « Postures » au CDN et les déclare dans `cartes-design.json` ; le deck les
matérialise par `_project/tools/sync_media.py` sous `<module>/static/media/clips/`. Trois
des quatre copies n'étaient référencées par aucun bloc et ont été retirées.

| fichier gelé | master de release (`productions/02-serie-postures/releases/v02/`) | sha256 du fichier gelé |
|---|---|---|
| `solyo_optimism_en.mp4` | `ep01_solyo_en_1x1_v2.mp4` | `15142a897064c80458dd39adf961e771...` |

Chaque fichier est la copie du master de release (1080x1080), **signée sur la copie** — le
master versionné n'est jamais modifié.

Clearance vérifiée avant copie : `channel = public-ok`, `ai_label` posé.

**Pourquoi celui-ci survit** : c'est l'écran d'attente, projeté plein écran devant la
salle qui se remplit. Le master est en 1080×1080 à 1,9 Mb/s, la rendition du CDN en
720×720 à 295 kb/s. Le bloc utilise désormais la rendition ; ce fichier est conservé le
temps que l'auteur juge le rendu en projection. Décision à prendre, puis ce dossier
disparaît.

## Pour rafraîchir

- **Les images** : recopier `mascoties/shared/cartes/web/*.webp` — elles sont déjà signées.
- **Les clips** : copier le master voulu depuis `commercials`, puis signer LA COPIE avec
  `augmented-student/_tools/embed_c2pa.py` (idempotent : re-signer empilerait un second
  manifeste). **Ne jamais signer un master de release.**
