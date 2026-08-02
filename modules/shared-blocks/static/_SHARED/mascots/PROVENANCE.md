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

## Les 4 clips (`videos/`)

Source : le dépôt **`sumvadis-commercials`**, série « Postures », release `v02`. C'est un
dépôt DIFFÉRENT du studio — d'où le verdict « orphelin » de `check_shared_freeze.py`, qui
ne cherche que dans `mascoties`. Ils ne le sont plus : voici l'origine exacte.

Chaque fichier est la copie du master de release (1080x1080), **signée sur la copie** — le
master versionné n'est jamais modifié. Le nom du gel est conservé, le support y fait
référence.

| fichier gelé | master de release (`productions/02-serie-postures/releases/v02/`) | sha256 du fichier gelé |
|---|---|---|
| `kuri_openness_en.mp4` | `ep11_kuri_en_1x1_v2.mp4` | `59cde4d37001cad29821ee4b7a70fd59...` |
| `rapo_speed_en.mp4` | `ep09_rapo_en_1x1_v2.mp4` | `008e19b94cdf7bc3b4c599f14e53146c...` |
| `rapo_speed_fr.mp4` | `ep09_rapo_fr_1x1_v2.mp4` | `a65f1368f3d6053f5a2eb773c9e0e3ee...` |
| `solyo_optimism_en.mp4` | `ep01_solyo_en_1x1_v2.mp4` | `15142a897064c80458dd39adf961e771...` |

Clearance vérifiée avant copie pour les quatre : `channel = public-ok`, `ai_label` posé.

## Pour rafraîchir

- **Les images** : recopier `mascoties/shared/cartes/web/*.webp` — elles sont déjà signées.
- **Les clips** : copier le master voulu depuis `commercials`, puis signer LA COPIE avec
  `augmented-student/_tools/embed_c2pa.py` (idempotent : re-signer empilerait un second
  manifeste). **Ne jamais signer un master de release.**
