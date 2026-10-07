# Étape 4 — Implémentation sous contrat

Tâches : file A : T09, T10, T11 · file B : T12, T13 · Budget : 4 à 7 h humaines · Prérequis : étape 3 acceptée, contrats gelés

## Objectif

Implémenter le socle (codec, modèle, Event Store) et le runtime (façades, FlowTrace) jusqu'à ce que tous les tests de contrat passent sur 4.7.2. Le résultat de la préversion est rapporté. À la fin, le runtime est éprouvé de bout en bout par un banc de test sans éditeur.

## Obligations

- **Tests intouchables.** L'implémenteur active ses tests en attente et ne les modifie jamais. Un test qui lui semble faux : statut QUESTION.
- **Pas d'API hors contrat.** Une fonction publique utile mais non prévue : statut QUESTION.
- **Dépendances.** `check_deps` reste vert : le socle sans dépendance, le runtime autonome, les API sensibles derrière les façades.
- **Leçons de SPIKE-01a.** T13 applique les cinq constats :
  - commandes appliquées à la frontière de frame ;
  - bail ;
  - crochet de frame posé dès l'initialisation ;
  - désenregistrement explicite ;
  - messages du moteur ignorés.
- **Mesures réelles.** Les mesures de SPIKE-05 sont faites, pas estimées.

## Méthodologie

- **Rouge, vert, vérification.** On active les tests (ils échouent), on implémente, on les fait passer, puis le vérificateur intervient.
- **Deux files en parallèle.** File A pour le socle, file B pour le runtime. Qwen réalise. Opus vérifie T12 et T13 (façades et protocole) ; Gemini vérifie T09 à T11.
- **Banc de test sans éditeur.** T13 transforme le récepteur de SPIKE-01a en `tools/harness/fake_editor.gd`. Les tests d'intégration du runtime le réutilisent, en CI comme en local.
- **SPIKE-06.** Chaque tâche note tentatives, escalades et temps. À la fin de l'étape, on calcule le taux de réussite au premier essai par modèle.

## Points de contrôle

| ID | Contrôle | Commande ou preuve | Attendu |
| --- | --- | --- | --- |
| PC4.1 | Tout vert sur 4.7.2 | `GODOT=<4.7.2> tools/ci/run_all_checks.sh` | Code 0 ; pending=0 pour les tests de C-01 à C-07 |
| PC4.2 | Préversion | Même script avec le binaire de la préversion | Résultat consigné, sans exigence |
| PC4.3 | Session de bout en bout | Étape « integration » de `run_all_checks.sh` | Aucun trou, aucun lot après « stopped », bail déclenché à la coupure |
| PC4.4 | Coûts mesurés | `docs/spikes/SPIKE-05.md` | Coûts actif et désactivé, côté appelant compris, avec méthode et chiffres |
| PC4.5 | Contre-épreuves | Verdicts des vérificateurs | Toutes détectées |
| PC4.6 | Fiabilité des modèles | `PROJECT_STATE.md` | Taux de réussite au premier essai par modèle |

## Cheminement d'amélioration

- **Qwen sous 40 % de réussite après dix tâches.** Les tâches restantes passent à Sonnet, ou on les découpe plus finement.
- **Chemin désactivé mesurable dans le temps de frame.** On applique les règles d'appel : `if FlowTrace.enabled:` devant les charges, clés en StringName littéraux. Puis on mesure à nouveau.
- **Test d'intégration instable.** On compte en frames plutôt qu'en millisecondes, et on injecte une horloge factice dans les tests unitaires.
- **Questions répétées sur un contrat.** On le signale à la rétro : le contrat a besoin d'un exemple.

## T09 — Codec et validateur de l'enveloppe (C-04)

Qwen · A1 · file A · dépend de T08 · vérification : Gemini · pack de contexte RUNTIME

Fichiers autorisés : `addons/godot_dev_mapper_runtime/envelope.gd`, `addons/godot_dev_mapper/protocol/envelope_codec.gd`, `tests/pending.json` (entrées T09), `PROJECT_STATE.md`.

```text
Tu réalises la tâche T09 du projet GODOT_DEV_MAPPER. Applique les règles et le format de rapport du prompt universel de réalisation.
CONTEXTE : docs/CONTRACTS.md section C-04 ; contracts/schemas/envelope.v1.schema.json ; tests/contract/test_c04_envelope.gd et ses fixtures.
OBJECTIF : implémenter le codec de l'enveloppe C-04 v1. L'encodage va dans addons/godot_dev_mapper_runtime/envelope.gd, qui ne dépend de rien hors du dossier runtime. Le décodage et la validation vont dans addons/godot_dev_mapper/protocol/envelope_codec.gd.
DÉROULÉ
1. Retire de tests/pending.json l'entrée de test_c04_envelope.gd ; lance le runner et montre l'échec.
2. Implémente jusqu'à faire passer ce test, sans le modifier.
CONTRÔLES
T09-a  godot --headless --path . -s res://tests/run_all.gd ; echo $?   → 0, aucun test de C-04 en attente
T09-b  GODOT=<binaire> tools/ci/run_all_checks.sh ; echo $?            → 0
T09-c  Dans le rapport : aller-retour de l'identifiant 9223372036854775807 sans perte, avec la sortie du test qui le prouve
CONTRE-ÉPREUVE (CE) pour le vérificateur : passer la limite d'événements par lot à 257 → test_c04_envelope échoue.
```

## T10 — Modèle minimal, graphe déclaré, clés de sonde (C-01, C-02, C-05)

Qwen · A1 · file A · dépend de T07 et T09 · vérification : Gemini · pack de contexte CORE

Fichiers autorisés : `addons/godot_dev_mapper/core/`, `tests/pending.json` (entrées T10), `PROJECT_STATE.md`.

```text
Tu réalises la tâche T10 du projet GODOT_DEV_MAPPER. Applique les règles et le format de rapport du prompt universel de réalisation.
CONTEXTE : docs/CONTRACTS.md, sections C-01, C-02 et C-05 ; contracts/schemas/declared_graph.v1.schema.json ; tests/contract/test_c01_identities.gd et test_c05_declared_graph.gd, avec leurs fixtures.
OBJECTIF : dans addons/godot_dev_mapper/core/, le modèle minimal, le chargeur de .flow.json v1 et la table des clés de sonde.
- Le chargeur rejette chaque fixture invalide pour le motif attendu.
- Il conserve les références non résolues.
- Une clé de sonde inconnue donne « définition non résolue ».
- core/ ne dépend d'aucun autre module.
DÉROULÉ : retire de tests/pending.json les entrées T10, montre l'échec, puis implémente.
CONTRÔLES
T10-a  runner → 0, aucun test T10 en attente
T10-b  python3 tools/check_deps.py ; echo $?   → 0
T10-c  GODOT=<binaire> tools/ci/run_all_checks.sh ; echo $?   → 0
CONTRE-ÉPREUVE (CE) pour le vérificateur : faire accepter au chargeur une définition sans « evidence » → test_c05 échoue.
```

## T11 — Event Store minimal (C-06)

Qwen · A1 · file A · dépend de T08 et T10 · vérification : Gemini · pack de contexte EDITOR

Fichiers autorisés : `addons/godot_dev_mapper/store/`, `tests/pending.json` (entrées T11), `PROJECT_STATE.md`.

```text
Tu réalises la tâche T11 du projet GODOT_DEV_MAPPER. Applique les règles et le format de rapport du prompt universel de réalisation.
CONTEXTE : docs/CONTRACTS.md, section C-06 (et C-04 pour le format reçu) ; tests/contract/test_c06_store.gd ; fixtures de tests/contract/fixtures/sessions/.
OBJECTIF : dans addons/godot_dev_mapper/store/, l'Event Store minimal du contrat :
- sessions et lacunes déduites des séquences ;
- rétention bornée, avec le marqueur « tronqué avant seq N » ;
- fin de session, et « fin inconnue » quand le message de fin manque ;
- requête « chemin observé » à trois états : cohérent, incohérent, indéterminé.
DÉROULÉ : retire les entrées T11 de tests/pending.json, montre l'échec, puis implémente.
CONTRÔLES
T11-a  runner → 0, aucun test T11 en attente
T11-b  GODOT=<binaire> tools/ci/run_all_checks.sh ; echo $?   → 0
T11-c  Dans le rapport : pour chaque fixture de session, l'état obtenu et l'état attendu par le contrat
CONTRE-ÉPREUVES (CE) pour le vérificateur :
- supprimer le marqueur de troncature → test_c06 échoue ;
- classer « cohérent » une invocation touchée par un trou → test_c06 échoue.
```

## T12 — Façades de compatibilité et profil moteur (C-03)

Qwen · A1 · file B · dépend de T06 et T08 · vérification : Opus · pack de contexte COMPAT

Fichiers autorisés : `addons/godot_dev_mapper/compat/engine_facade.gd` et `engine_profile.gd`, `addons/godot_dev_mapper_runtime/runtime_facade.gd`, `tests/pending.json` (entrées T12), `PROJECT_STATE.md`.

```text
Tu réalises la tâche T12 du projet GODOT_DEV_MAPPER. Applique les règles et le format de rapport du prompt universel de réalisation.
CONTEXTE : docs/CONTRACTS.md, section C-03 ; docs/spikes/SPIKE-02.md (détection de capacités, isolation) ; docs/ARCHITECTURE.md (API sensibles) ; tests/contract/test_c03_facades.gd.
OBJECTIF
- Côté éditeur : les façades débogueur et éditeur, et le profil moteur (version affichée, capacités détectées selon les règles de SPIKE-02).
- Côté runtime : la façade du dossier autonome. Elle accepte un transport de substitution pour les tests et ne référence jamais le plugin éditeur.
- Les API sensibles n'apparaissent que dans ces fichiers.
DÉROULÉ : retire les entrées T12 de tests/pending.json, montre l'échec, puis implémente.
CONTRÔLES
T12-a  runner → 0 sur 4.7.2, aucun test T12 en attente
T12-b  python3 tools/check_deps.py ; echo $?   → 0
T12-c  Même runner avec le binaire de la préversion → résultat collé dans le rapport, sans exigence
T12-d  godot --headless --path . --check-only -s res://addons/godot_dev_mapper_runtime/runtime_facade.gd   → 0
CONTRE-ÉPREUVE (CE) pour le vérificateur : ajouter un appel à EngineDebugger dans store/ → check_deps échoue.
```

## T13 — FlowTrace, banc sans éditeur et SPIKE-05 (C-07)

Qwen · A1 · file B · dépend de T08, T09 et T12 · vérification : Opus · pack de contexte RUNTIME, plus `docs/spikes/SPIKE-01.md`

Fichiers autorisés :
- `addons/godot_dev_mapper_runtime/flow_trace.gd` ;
- `tools/harness/fake_editor.gd`, `tools/harness/demo_game/` ;
- `tests/integration/run_session.sh`, `tools/ci/run_all_checks.sh` (ajout de l'étape « integration ») ;
- `docs/spikes/SPIKE-05.md`, `tests/pending.json` (entrées T13), `PROJECT_STATE.md`.

```text
Tu réalises la tâche T13 du projet GODOT_DEV_MAPPER. Applique les règles et le format de rapport du prompt universel de réalisation.
CONTEXTE : docs/CONTRACTS.md, section C-07 (et C-04) ; docs/spikes/SPIKE-01.md, dont les constats sont obligatoires ; spikes/spike01_debugger/, en exemple seulement ; tests/contract/test_c07_flowtrace.gd.

OBJECTIF
1. addons/godot_dev_mapper_runtime/flow_trace.gd : classe à class_name FlowTrace, fonctions statiques, sans autoload. Elle couvre l'API de C-07, la table d'états du protocole de session, le bail, la réserve de contrôle, le registre des instances et l'état initial, et la pile d'invocations. Elle passe par la façade runtime.
   Constats de SPIKE-01a à respecter :
   - le rappel de capture note la commande, appliquée à la frontière de frame suivante ;
   - le crochet de frame est posé dès l'initialisation ;
   - la capture est désenregistrée explicitement à la fin ;
   - les messages du moteur sont ignorés.
2. tools/harness/fake_editor.gd : un récepteur qui joue l'éditeur sur le canal du débogueur. Réécris-le proprement à partir de spikes/spike01_debugger/receiver/, avec un port configurable et des scénarios paramétrables : démarrage, arrêt, redémarrage, coupure.
3. tools/harness/demo_game/ : un mini-projet qui utilise FlowTrace, avec deux instances et une décision.
4. tests/integration/run_session.sh : lance le banc et le mini-jeu, et vérifie : aucun trou ; aucun lot après « stopped » ; bail déclenché après la coupure ; jeu toujours actif. Ajoute l'étape « integration » à run_all_checks.sh.
5. docs/spikes/SPIKE-05.md : coût d'un appel désactivé, côté appelant compris, et coût de la collecte active à 1 000 événements par seconde, avec la méthode, la machine, la version et les chiffres.

DÉROULÉ : retire les entrées T13 de tests/pending.json, montre l'échec, puis implémente.

CONTRÔLES
T13-a  runner → 0, aucun test T13 en attente
T13-b  tests/integration/run_session.sh avec GODOT=<4.7.2> ; echo $?   → 0
T13-c  GODOT=<binaire> tools/ci/run_all_checks.sh ; echo $?            → 0, CHECK integration OK
T13-d  python3 tools/check_deps.py ; echo $?                           → 0 ; le dossier runtime ne référence pas le plugin
T13-e  docs/spikes/SPIKE-05.md contient des chiffres mesurés et la commande qui les reproduit

CONTRE-ÉPREUVES (CE) pour le vérificateur
- appliquer « stop » directement dans le rappel de capture → le test de réentrance de test_c07 ou T13-b échoue ;
- bail infini → T13-b échoue sur la coupure ;
- réserve de contrôle illimitée → le test « réserve pleine » échoue.
```
