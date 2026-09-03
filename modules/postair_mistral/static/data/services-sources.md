# services-sources.md — le registre de maintenance des tables « services »

> Demande NG (2026-09-03) : « un fichier MD avec le plan et les sources pour
> récupérer ces données — nous allons faire de la maintenance fréquente. »
> Ce fichier est LA carte de re-vérification : chaque valeur projetée des
> slides SV1…SV5 (deck mistral) pointe sa source et sa méthode. La donnée
> projetée vit dans `facts.json` (section `services`) — CE fichier dit d'où
> elle vient et comment la revérifier ; les deux se mettent à jour ENSEMBLE.

## La procédure de maintenance (à chaque re-vérification)

1. **Parcourir les sources ci-dessous** (¼ h au navigateur — plusieurs pages
   bloquent les robots : le navigateur humain est l'outil de référence ; en
   agent, la Wayback Machine datée est le meilleur substitut).
2. **Éditer `facts.json`** section `services` : cellules (`sym` — feuille
   `{en, fr}` si des unités/mots diffèrent), hovers, détails ⓘ, `url` (logo
   cliquable). Symboles : ✅ inclus · 💰 payant · 🎓 étudiant · ⚠️ limité ·
   ❌ absent · ❓ non vérifié à la source.
3. **Mettre à jour ce fichier** : date, verdicts changés.
4. **Portes** : `check_blocks_build`, `check_i18n --baseline postair_mistral`
   puis `--regress`, `check_projection postair_mistral --all`, commit.

## Leçons de méthode (payées)

- **2026-09-03 · l'extrait indexé ment** : la passe 1 a donné « confiance
  haute » à des extraits indexés de pages bloquées. Règle : un ✅/❌ exige une
  page lue EN DIRECT, 2+ sources directes concordantes, une archive Wayback
  DATÉE, ou une vérité terrain ; sinon ⚠️/❓.
- **2026-09-03 · les pages officielles se contredisent** : « 10 fichiers par
  GPT » (File Uploads FAQ) vs « 20 fichiers » (Creating GPTs) — quand deux
  pages officielles divergent, la cellule montre l'intervalle + ❓.
- **2026-09-03 · la doc et le produit divergent pendant un rollout** : l'article
  OpenAI (version datée ~16-08) ferme la création de GPTs aux comptes perso,
  le compte Plus de NG crée encore le 03-09 — les DEUX se disent, avec dates.
- **2026-09-03 · la Wayback datée bat l'extrait indexé** : deux versions du
  même article (11-08 vs 25-08) ont daté la bascule OpenAI au ~16-08.
- Pages qui BLOQUENT les robots (navigateur humain requis) : help.openai.com,
  openai.com, chatgpt.com, x.ai, grok.com, perplexity.ai, pages HTML uni.lu
  (le PDF des guidelines, lui, se télécharge).

## Le registre — passe 2 adversariale du 2026-09-03

Méthodes : **[D]** page officielle lue en direct · **[P]** page officielle
rendue au NAVIGATEUR Playwright (passe certains murs anti-bot — le Help
Center Perplexity, pas ses autres pages) · **[W]** archive Wayback DATÉE
d'une page officielle (se tire par curl quand le fetch est bloqué) · **[S]**
sources secondaires récentes CONCORDANTES (2+) — admises par NG (poe1,
2026-09-03) quand [D]/[P]/[W] échouent · **[I]** extraits indexés seulement ·
**[T]** vérité terrain (compte réel) · **[?]** invérifiable ce jour.

### SV2 — Créer un agent (`services.create`)

| Ligne | Valeur projetée | Méthode | Source |
|---|---|---|---|
| ChatGPT / GPTs | gratuit ⚠️ (utiliser oui) ; payant **⚠️ ❓ EN BASCULE** : doc du ~16-08 « New GPT creation… not available on personal accounts, including Free, Go, Plus, and Pro » (édition des existants maintenue) MAIS le compte Plus de NG crée encore au 03-09 (rollout progressif probable — re-tester avant séance) | [W] 25-08 + [W] 11-08 + **[T]** | web.archive.org/web/20260825223743/https://help.openai.com/en/articles/8554397 · …20260811121615/…/8554407 |
| Gemini / Gems | création gratuite ✅ (« at no cost », web app, 13+) | [D] | blog.google/products/gemini/new-gemini-app-features-march-2025/ · support.google.com/gemini/answer/15235603 · /13278668 |
| Mistral Vibe / agents | gratuit ❌ ; **Pro ET Team ✅** (« available on Le Chat Pro and Team plans », « Custom subagents ») ; Enterprise : custom agents | [D] | mistral.ai/news/mistral-vibe-2-0/ · /news/vibe-remote-agents-mistral-medium-3-5/ · /pricing |
| Claude / Projects | gratuit ✅ 5 max ; payant ✅ illimité + RAG ×10 | [D] | support.claude.com/en/articles/9517075 · /11473015 |
| Copilot / agents | école ⚠️ : Agent Builder sans licence = instructions + web public, **fichiers embarqués ❌** (facturation/licence) | [D] | learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/prerequisites (table de licence) |
| Poe / bots | **MASQUÉE** (`shown: false`, poe1 — données conservées) : création ✅ | [D] | creator.poe.com/docs/prompt-bots/how-to-create-a-prompt-bot |
| Perplexity / Projects | gratuit ✅ (création — secondaires concordants + silence des exclusions officielles) ; 🎓 Education Pro 10 $/mois SheerID ; Pro 20 $ ✅ ; renommés Spaces→Projects été 2026 (snapshots 03-06 vs 04-07) | [P]+[W]+[S] | article Projects (navigateur) · plans (W 21-08) · pricing (W 27-08) |

### SV3 — Nourrir l'agent (`services.feed`)

| Ligne | Valeur projetée | Méthode | Source |
|---|---|---|---|
| ChatGPT | **10-20 f ❓ (deux pages officielles se contredisent)** · 512 Mo/f · 2 M tokens (hors tableurs) ; gratuit 3 uploads/j ; instruction **❓ (8 000 c = folklore communautaire, absent des articles officiels)** | [W] | Creating GPTs (W 25-08 : « up to 20 files ») vs File Uploads FAQ (W 29-08 : « up to 10 files per GPT ») |
| Gemini | 10 f/prompt (« subject to availability ») · 100 Mo/f (vidéo 2 Go) ; instruction ❓ (non documentée) | [D] | support.google.com/gemini/answer/14903178 |
| Vibe | gratuit ⚠️ ; **volume ❓ — « 15 Go Pro » PÉRIMÉ** (pricing actuel : seul chiffre Team 30 Go/util.) ; instruction ❓ | [D] | mistral.ai/pricing |
| Claude | contexte ⚠️ ; RAG 💰 (×10, payant) ; instruction ❓ (non documentée) | [D] | support.claude.com/en/articles/11473015 |
| Copilot | **20 sources de connaissance** (fichiers embarqués = 💰) ; instruction **8 000 c CONFIRMÉ** (+ description 1 000, nom 30) | [D] | learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/copilot-studio-agent-builder-build |
| Poe | **MASQUÉE** (`shown: false`) : 5 Go / 30 M caractères | [D] | creator.poe.com (même page) |
| Perplexity | Pro 50 f/Project (Max 500, Ent. 5 000) 💰 ; gratuit ~3 f/jour [S] (aucun chiffre officiel par Project — rien d'affiché) ; **40 Mo/f** (File Uploads, maj 16-07 — la FAQ Projects dit 50 Mo payant, 40 = le plus récent) ; **instruction 8 000 c** [P] — 2e plateforme documentée avec Copilot ; audio/vidéo transcrits | [P]+[W]+[S] | File Uploads (W 22-07) · FAQ Projects (W 04-07) · article Projects (navigateur) |

### SV4 — La voix (`services.voice`)

| Ligne | Valeur projetée | Méthode | Source |
|---|---|---|---|
| ChatGPT Voice | temps réel ✅ gratuit (« GPT-Live-1 mini… default model for free users ») ; **full-duplex ✅ (System Card lue en direct)** ; caméra 💰 ❓ (abonnés, mobile, « pas encore en Live — soon », indexé) ; quotas gratuits ❓ (**« ~2 h/jour » SUPPRIMÉ : télescopage** — 2 h = durée max d'une session) | [D] System Card + [I] modes | deploymentsafety.openai.com/gpt-live · help.openai.com/…/8400625 (403) |
| Gemini Live | full-duplex ✅ ; caméra+écran ✅ gratuits (mobile ; **desktop via Gemini dans Chrome**, pas la web app) ; limites 5 h + plafond hebdo ; FR parmi 40+ | [D] | support.google.com/gemini/answer/15274899 · /16363185 · /16275805 · blog.google (I/O mai 2025) |
| Grok Voice | **tout ❓/⚠️ — x.ai intégralement en 403** ; voix + Live Camera corroborées par la fiche App Store (lue en direct) ; aucun chiffre de limite publié ; 13+/accord parental 13-17 (CGU via index ; App Store 16+) | [I] + App Store [D] | apps.apple.com/us/app/grok/id6670324846 · x.ai/grok (403) |
| Copilot Voice | ✅ gratuit « not limited » (priorité abonnés) ; interruption ✅ ; **Vision = Microsoft 365 Personal/Family/Premium** ; FR listé | [D] | support.microsoft.com (Voice · Vision · langues) |
| Claude Voice | ✅ tous plans (**mobile + desktop + web**, bêta ; Free = Haiku) ; interruption ✅ ; caméra ❌ ; FR (bêta, 11 langues) | [D] | support.claude.com/en/articles/11101966 · claude.com/blog (23-07-2026) |
| Mistral Vibe | dictée Voxtral seulement (❌ speech-to-speech ; astérisque : Voxtral TTS existe côté plateforme) ; tous plans ; FR listé | [D] | docs.mistral.ai/vibe/work/voice-mode |
| Meta AI | PAS DE LIGNE — vocal lancé US/CA/AU/NZ ; Europe = texte seul au lancement ; rien d'officiel pour le vocal FR au 03-09 | [D] | about.fb.com (avril 2025 · mars 2025 · avril 2026) |
| Perplexity | PAS DE LIGNE — temps réel via **GPT Realtime 1.5** (blog OpenAI, direct) ; full-duplex et quotas jamais énoncés | [D] OpenAI + [?] | developers.openai.com/blog/realtime-perplexity-computer |

### SV5 — Offres étudiantes (`services.students`)

| Ligne | Valeur projetée | Méthode | Source |
|---|---|---|---|
| Google | 🎓 12 mois AI Plus ; **puis 4,99 €/mois (page LUXEMBOURG lue en direct — l'ancien « ~8 € » était faux)** ; SheerID + email école + moyen de paiement ; re-vérif ~annuelle (≤4 ans) ; avant 31-12-2026 ; Luxembourg ✅ | [D] | gemini.google/lu/students/ · support.google.com/googleone/answer/17422238 · blog.google |
| Mistral | 🎓 **5,99 $/mois** (14,99 $ plein ; € non lu en direct) ; 12 mois ; email institutionnel OBLIGATOIRE ; **comptes existants acceptés** (« nouveaux comptes » = faux) ; **enseignants aussi** | [D] | mistral.ai/pricing · help.mistral.ai/en/articles/698530 |
| OpenAI | 🎓 US-only ❌ Luxembourg (« eligible U.S. degree-granting institutions », 4 mois de Plus, avant 31-10) | [W] 26-08 | chatgpt.com/students/2026/ (snapshot officiel) |
| Perplexity | 🎓 **Education Pro 10 $/mois SheerID — OFFICIEL par snapshot daté** (article plans maj 18-08-2026) + un mois Pro offert [S] ; **Learn Mode** (flashcards/quiz) gratuit pour étudiants VÉRIFIÉS (article officiel, W 31-07) ; promo parrainage-année-gratuite TERMINÉE le 31-05-2026 [S concordants] ; Luxembourg : aucune restriction publiée, SheerID accepte toute adresse ✅ ❓ | [W]+[S] | plans (W 21-08) · Learn Mode (W 31-07) · pricing (W 27-08) |
| Claude | ❌ individuel (« university-wide plan for institutions ») ; Pro 17 $ annuel / 20 $ mensuel | [D] | claude.com/solutions/education · /pricing |
| uni.lu / Copilot | **✅ CONFIRMÉ — le ❓ est tombé** : « The UL provides Microsoft Copilot as its official supported chatbot… guarantees the confidentiality of any data entered » (Guidelines GenAI sept. 2025, VRAE/Rectorat, **PDF lu en entier**) ; A1 gratuit n'inclut pas Copilot (add-on institutionnel, A1 = prérequis éligible) | [D] PDF + [D] MS | uni.lu/wp-content/uploads/sites/9/2025/09/22084834/guidelines-use-generative-ai-tools-for-learning-and-teaching-2025-09.pdf · learn.microsoft.com/…/microsoft-365-copilot-licensing |

### SV1 — Prix repères (cartes + infobulles)

| Valeur | Méthode | Source |
|---|---|---|
| Google AI Pro **20,99 €/mois** · AI Plus **4,99 €** (Luxembourg) — les anciens 21,99/8 € étaient faux | [D] | gemini.google/lu/subscriptions/ |
| Vibe Pro 14,99 $ (étudiant 5,99 $) | [D] | mistral.ai/pricing |
| Claude Pro 17 $ annuel / 20 $ mensuel | [D] | claude.com/pricing |
| ChatGPT Plus **20 $ + TVA locale** (montant € non vérifiable en direct) | [W]/[I] | pricing géolocalisé, live en 403 |
| Perplexity Pro ~20 $ ❓ | [I] | site en 403 |

### Leçon poe1 (2026-09-03)

- **Playwright passe certains murs** : le Help Center Perplexity rend au
  navigateur réel (l'article Projects s'y lit) quand curl/WebFetch prennent
  403 — mais Cloudflare tient sur le reste du domaine.
- **archive.org se tire par curl** quand WebFetch y est bloqué — et deux
  snapshots datés ENCADRENT un changement (renommage Spaces→Projects).

## Preuves d'archive conservées (scratchpads de session, 2026-09-03)

`gpt-create-wb.html`, `file-uploads-wb.html`, `gpts-faq-wb2.html`,
`unilu-guidelines.pdf`, `chatgpt-students-2026.html`, `pplx-students`,
`pplx-aug25.html`, `pplx-projects.txt` — les fichiers bruts des lectures datées des passes 2 et poe1.
