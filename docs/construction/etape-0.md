# Étape 0 — Décisions et environnement

Tâches : 0.A dossier de décisions · 0.B squelettes et règles des agents · T00 environnement de Qwen · Budget : 2 à 4 h humaines · Prérequis : aucun

## Objectif

Partir sur des décisions écrites et des agents qui fonctionnent. À la fin de l'étape, chaque décision bloquante a une réponse datée. Chaque agent lit les mêmes règles, au même endroit. Le modèle local a prouvé qu'il sait lire, écrire et exécuter une commande dans le dépôt.

## Obligations

- Aucune ligne de code du plugin.
- Un modèle prépare les décisions, toi seul les tranches : D-01, D-05 et D-07, plus une liste courte pour D-02.
- Une seule source de règles pour les agents : `REGLES_AGENTS.md`. `CLAUDE.md` et `GEMINI.md` en sont des copies exactes, produites par un script ; le harnais de Qwen lit la même source.
- Chaque document normatif commence par une ligne « Statut : proposé · date » ou « Statut : validé · date ».
- Les squelettes extraient le plan sans le réécrire : une définition n'existe qu'à un seul endroit.

## Méthodologie

1. Opus prépare `docs/DECISIONS.md` (0.A). Tu tranches et tu dates.
2. Opus crée les squelettes et la source unique de règles (0.B). Gemini les relit pour y chercher contradictions et doublons avec le plan.
3. Tu installes l'environnement de Qwen : un serveur local du modèle et un harnais d'agent capable d'appeler des outils. Tu le fais passer par la tâche jouet T00.

| Décision | Recommandation | Raison |
| --- | --- | --- |
| D-01 Version de référence | Godot 4.7.2 | Dernière stable ; binaire officiel vérifié par SPIKE-01a |
| D-02 Banc d'essai | Liste courte de deux ou trois jeux ; choix final en T04 | Le choix demande une lecture des dépôts |
| D-05 Runner de tests | Runner maison minimal | Codes de sortie vérifiés ; aucune dépendance |
| D-07 Fenêtre de support | 4.7.2 bloquant ; dernière préversion 4.8 dans un job séparé | Alerte précoce sans blocage |
| D-04, D-06, D-08 | Non bloquantes : à trancher avant leur échéance | — |

## Points de contrôle

| ID | Contrôle | Commande ou preuve | Attendu |
| --- | --- | --- | --- |
| PC0.1 | Décisions bloquantes tranchées | `for d in D-01 D-05 D-07; do grep -E "^\| $d " docs/DECISIONS.md \| grep -q "validée" \|\| echo "manque $d"; done` | Aucune sortie |
| PC0.2 | Squelettes présents | `for f in docs/SPEC.md docs/ARCHITECTURE.md docs/CONTRACTS.md docs/COMPATIBILITY.md docs/TEST_PLAN.md PROJECT_STATE.md REGLES_AGENTS.md; do test -s "$f" \|\| echo "manque $f"; done` | Aucune sortie |
| PC0.3 | Statut en tête des documents normatifs | `grep -L "^Statut" docs/SPEC.md docs/ARCHITECTURE.md docs/CONTRACTS.md docs/COMPATIBILITY.md docs/TEST_PLAN.md` | Aucune sortie |
| PC0.4 | Copies des règles identiques | `tools/sync_rules.sh --check; echo $?` | 0 |
| PC0.5 | (CE) Copie divergente détectée | `echo x >> CLAUDE.md; tools/sync_rules.sh --check; echo $?`, puis `tools/sync_rules.sh` | 1, puis rétabli |
| PC0.6 | Règles courtes | `wc -l < REGLES_AGENTS.md` | 150 au plus |
| PC0.7 | Qwen opérationnel | Rapport de T00, commandes relancées par toi | Mêmes codes et mêmes sorties |
| PC0.8 | Relecture croisée | Rapport de Gemini sur les squelettes | Aucune contradiction ouverte |

Les barres verticales sont échappées dans le tableau ; dans le terminal, on tape `|` sans antislash.

## Cheminement d'amélioration

- **Décisions trop longues.** Si elles prennent plus d'une heure, c'est qu'on refait le plan. Adopte les recommandations et note les doutes pour la revue T20.
- **Règles trop longues.** Si `REGLES_AGENTS.md` dépasse 150 lignes, déplace le détail dans le guide. Les règles ne contiennent que ce que les agents ratent vraiment.
- **Qwen trop lent ou peu fiable.** Note le débit en tokens par seconde, la durée de la tâche jouet et les appels d'outil ratés. Au-delà de dix minutes, ou au premier appel d'outil inventé, confie T01 à T03 à Sonnet et réessaie Qwen sur une tâche de l'étape 4.
- **Après coup.** À chaque erreur répétée deux fois par un agent, ajoute une ligne à `REGLES_AGENTS.md`, puis relance `tools/sync_rules.sh`.

## 0.A — Dossier de décisions

Opus · A0 · contexte : plan §0 et §10, `docs/spikes/SPIKE-01.md`

```text
Tu prépares les décisions de démarrage du projet GODOT_DEV_MAPPER. Tu ne décides rien.
Lis docs/plan-directeur.md (§0 et §10), docs/spikes/SPIKE-01.md et docs/construction/etape-0.md.
Crée docs/DECISIONS.md : un tableau avec ID, question, options (deux ou trois), recommandation, conséquences de chaque option, échéance, statut (« proposée »), date.
Couvre D-01 à D-08. Pour D-02, propose des critères de choix du banc d'essai, pas un jeu.
Avant de rendre, vérifie : chaque ID de D-01 à D-08 apparaît une seule fois ; chaque ligne a une recommandation ; aucune ligne n'est marquée « validée ».
Rapport : le chemin du fichier, puis les questions que je dois trancher, une par ligne, dans l'ordre de leur échéance.
```

Ensuite, tu remplaces « proposée » par « validée » et la date, ligne par ligne.

## 0.B — Squelettes et source unique de règles

Opus · A1 · vérification : Gemini · contexte : plan, méthodologie, `docs/DECISIONS.md`, `docs/construction/README.md`

Fichiers autorisés : `docs/SPEC.md`, `docs/ARCHITECTURE.md`, `docs/CONTRACTS.md`, `docs/COMPATIBILITY.md`, `docs/TEST_PLAN.md`, `PROJECT_STATE.md`, `REGLES_AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `tools/sync_rules.sh`.

```text
Tu crées les squelettes de documents du projet GODOT_DEV_MAPPER. Tu n'écris aucun code du plugin.
Sources : docs/plan-directeur.md, docs/methodologie.md, docs/DECISIONS.md, docs/construction/README.md.

À CRÉER
- docs/SPEC.md : vision, scénarios et capacités, extraits des §1 à 3 du plan ; renvoie au plan pour le détail.
- docs/ARCHITECTURE.md : modules, dépendances autorisées et interdites, frontière de compatibilité, liste des API sensibles (plan §4).
- docs/CONTRACTS.md : une section par contrat C-01 à C-07, avec sept rubriques : objet, format ou API, exemples valides, exemples invalides, comportement en erreur, version, tests de contrat. Contenu : « à rédiger en T07 » ou « à rédiger en T08 ».
- docs/COMPATIBILITY.md : fenêtre de support issue de D-01 et D-07.
- docs/TEST_PLAN.md : types de tests, commandes de contrôle vérifiées (reprises du guide), principe des contre-épreuves.
- PROJECT_STATE.md : tableau des tâches T00 à T20 avec statut « À faire » ; budget de chaque étape ; mesures à tenir (heures humaines, temps agent, capacités acceptées, réussite par modèle).
- REGLES_AGENTS.md : 150 lignes au plus. Il contient les règles non négociables et le format de rapport du prompt universel de réalisation, les invariants INV-01 à INV-09 en une ligne chacun, et les commandes de contrôle.
- tools/sync_rules.sh : copie REGLES_AGENTS.md vers CLAUDE.md et GEMINI.md. Avec --check, il compare sans rien écrire et renvoie 1 si une copie diffère.

RÈGLES
Chaque document normatif commence par « Statut : proposé · 8 octobre 2026 » (ou la date du jour). Une définition n'existe qu'à un seul endroit ; ailleurs, on y renvoie.

CONTRÔLES (exécute-les et colle les sorties)
1. for f in docs/SPEC.md docs/ARCHITECTURE.md docs/CONTRACTS.md docs/COMPATIBILITY.md docs/TEST_PLAN.md PROJECT_STATE.md REGLES_AGENTS.md; do test -s "$f" || echo "manque $f"; done   → aucune sortie
2. grep -L "^Statut" docs/SPEC.md docs/ARCHITECTURE.md docs/CONTRACTS.md docs/COMPATIBILITY.md docs/TEST_PLAN.md   → aucune sortie
3. tools/sync_rules.sh && tools/sync_rules.sh --check; echo $?   → 0
4. (CE) echo x >> CLAUDE.md; tools/sync_rules.sh --check; echo $?   → 1, puis tools/sync_rules.sh pour rétablir
5. wc -l < REGLES_AGENTS.md   → 150 au plus
6. for c in C-01 C-02 C-03 C-04 C-05 C-06 C-07; do grep -c "^## $c" docs/CONTRACTS.md; done   → 1 pour chacun

Rapport au format du prompt universel de réalisation.
```

Prompt de relecture pour Gemini :

```text
Relis les squelettes créés à l'étape 0 du projet GODOT_DEV_MAPPER : docs/SPEC.md, docs/ARCHITECTURE.md, docs/CONTRACTS.md, docs/COMPATIBILITY.md, docs/TEST_PLAN.md, PROJECT_STATE.md, REGLES_AGENTS.md. Compare-les à docs/plan-directeur.md.
Cherche : une définition présente à deux endroits ; une règle du plan déformée ou absente ; un invariant manquant ; une commande de contrôle différente de celle du guide ; une décision de docs/DECISIONS.md non reprise.
Ne modifie rien. Rapport : liste numérotée avec fichier, passage, écart, correction proposée ; « aucun écart » sinon.
```

## T00 — Environnement de Qwen

Toi, puis Qwen · contexte : ce fichier

**Ce que tu fais.** Installe un serveur local pour Qwen3.8-27B et un harnais d'agent qui sait lire, écrire et exécuter des commandes. Fais lire `REGLES_AGENTS.md` au harnais, au démarrage ou comme fichier de contexte, puis donne-lui la tâche jouet.

```text
Tâche jouet T00. Tu vérifies ton environnement dans le dépôt GODOT_DEV_MAPPER.
1. Crée sandbox/t00/project.godot, qui contient config_version=5, puis une section [application] avec config/name="t00".
2. Crée sandbox/t00/hello.gd : un script qui étend SceneTree, affiche T00_OK dans _initialize, puis quitte avec le code 0.
3. Exécute :
   godot --headless --path sandbox/t00 --check-only -s res://hello.gd ; echo $?
   godot --headless --path sandbox/t00 -s res://hello.gd ; echo $?
4. Crée sandbox/t00/RAPPORT.md : les deux commandes, leur code de sortie, leurs cinq dernières lignes de sortie, et le temps total de la tâche.
N'invente aucune sortie. Si une commande échoue, recopie l'erreur telle quelle et arrête-toi.
```

**Contrôles**

| ID | Contrôle | Attendu |
| --- | --- | --- |
| T00-a | Tu relances les deux commandes du rapport | Codes 0, `T00_OK` visible, sorties identiques au rapport |
| T00-b | (CE) Tu demandes à Qwen d'ajouter une faute de syntaxe dans `hello.gd`, puis de relancer la première commande | Il rapporte le code 1 et l'erreur réelle, sans la masquer |
| T00-c | Mesures notées dans `PROJECT_STATE.md` | Débit en tokens par seconde, durée, appels d'outil ratés |

Le dossier `sandbox/` n'est pas versionné : T01 l'ajoute au `.gitignore`.

**Si T00 échoue**, T01 à T03 passent à Sonnet. La mise au point de Qwen reprend en parallèle de l'étape 1, sans retarder le projet.
