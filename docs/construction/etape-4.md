# Étape 4 — Implémentation sous contrat

Tâches : file A : T09, T10, T11 · file B : T12, T13a, T13b, T13c · Budget : 4 à 7 h humaines, objectif favorable · Prérequis : étape 3 acceptée, contrats gelés

## Objectif

Implémenter le socle (codec, modèle, Event Store) et le runtime (façades, FlowTrace) jusqu'à ce que tous les tests de contrat passent sur 4.7.2. Le résultat de la préversion est rapporté. À la fin, le runtime est éprouvé de bout en bout par un banc de test sans éditeur, et ses coûts sont mesurés.

## Obligations

- **Tests intouchables.** L'implémenteur active ses tests en supprimant ses marqueurs dans `tests/pending/`, et ne modifie jamais les tests ni les fixtures de contrat. S'il pense qu'un test contredit le contrat : statut QUESTION.
- **Pas d'interface publique hors contrat.** Les choix internes qui respectent le contrat, l'agent les tranche et les note dans son rapport. Une fonction publique non prévue au contrat : statut QUESTION.
- **Dépendances.** `check_deps` reste vert : le socle sans dépendance, le runtime autonome, les API sensibles derrière les façades.
- **Leçons de SPIKE-01a.** T13a applique les cinq constats :
  - commandes appliquées à la frontière de frame ;
  - bail ;
  - crochet de frame posé dès l'initialisation ;
  - désenregistrement explicite ;
  - messages du moteur ignorés.
- **Mesures réelles.** Les mesures de T13c sont faites, pas estimées.
- **Aucun fichier partagé.** Chaque contrôle ajouté est un script à part dans `tools/ci/checks.d/` ; `PROJECT_STATE.md` n'est mis à jour qu'à la fusion.

## Méthodologie

- **Rouge, vert, vérification.** On active les tests (ils échouent), on implémente, on les fait passer, puis le vérificateur intervient dans sa propre copie de travail.
- **Deux files en parallèle**, chacune dans ses copies de travail : file A pour le socle, file B pour le runtime. Qwen réalise. Opus vérifie T12, T13a et T13b (façades et protocole) ; Gemini vérifie T09, T10, T11 et T13c.
- **Banc de test sans éditeur.** T13b transforme le récepteur de SPIKE-01a en `tools/harness/fake_editor.gd`. Les tests d'intégration du runtime le réutilisent, en CI comme en local.
- **SPIKE-06.** Chaque tâche note tentatives, escalades et temps dans son rapport. À la fusion, tu les reportes dans `PROJECT_STATE.md`. À la fin de l'étape, on calcule le taux de réussite au premier essai par modèle.
- **Budget.** 4 à 7 h est un objectif favorable : il suppose des contrats clairs et peu de reprises. Le découpage de T13 et la règle QUESTION allégée servent à le tenir. Au-delà de 50 % de dépassement, revue de continuation.

## Points de contrôle

| ID | Contrôle | Commande ou preuve | Attendu |
| --- | --- | --- | --- |
| PC4.1 | Tout vert sur 4.7.2 | `GODOT=<4.7.2> tools/ci/run_all_checks.sh` sur main | Code 0 ; plus aucun marqueur de C-01 à C-07 dans `tests/pending/` |
| PC4.2 | Préversion | Même script avec le binaire de la préversion | Résultat consigné, sans exigence |
| PC4.3 | Session de bout en bout | Contrôle « integration » de `run_all_checks.sh` | Aucun trou, aucun lot après « stopped », bail déclenché à la coupure |
| PC4.4 | Coûts mesurés | `docs/spikes/SPIKE-05.md` | Coûts actif et désactivé, côté appelant compris, avec méthode et chiffres |
| PC4.5 | Contre-épreuves | Verdicts des vérificateurs | Toutes détectées |
| PC4.6 | Fiabilité des modèles | `PROJECT_STATE.md` | Taux de réussite au premier essai par modèle |

## Cheminement d'amélioration

- **Qwen sous 40 % de réussite après dix tâches.** Les tâches restantes passent à Sonnet, ou on les découpe plus finement.
- **Chemin désactivé mesurable dans le temps de frame.** On applique les règles d'appel : `if FlowTrace.enabled:` devant les charges, clés en StringName littéraux. Puis T13c mesure à nouveau.
- **Test d'intégration instable.** On compte en frames plutôt qu'en millisecondes, et on injecte une horloge factice dans les tests unitaires.
- **Questions répétées sur un contrat.** On le signale à la rétro : le contrat a besoin d'un exemple.

## T09 — Codec et validateur de l'enveloppe (C-04)

Qwen · A1 · file A · dépend de T08 · vérification : Gemini · pack de contexte RUNTIME

Fichiers autorisés : `addons/godot_dev_mapper_runtime/envelope.gd`, `addons/godot_dev_mapper/protocol/envelope_codec.gd`, les marqueurs T09 de `tests/pending/` (suppression seulement).

```text
Tu réalises la tâche T09 du projet GODOT_DEV_MAPPER. Applique les règles et le format de rapport du prompt universel de réalisation.
CONTEXTE : docs/CONTRACTS.md, section C-04, y compris sa table des codes d'erreur ; contracts/schemas/envelope.v1.schema.json ; tests/contract/test_c04_envelope.gd et ses fixtures.
OBJECTIF : implémenter le codec de l'enveloppe C-04 v1.
- L'encodage va dans addons/godot_dev_mapper_runtime/envelope.gd, qui ne dépend de rien hors du dossier runtime.
- Le décodage et la validation vont dans addons/godot_dev_mapper/protocol/envelope_codec.gd. Le validateur renvoie les codes d'erreur du contrat, y compris les règles sémantiques : ordre des séquences, taille en octets.
DÉROULÉ
1. Supprime les marqueurs T09 de tests/pending/ ; lance le runner et montre l'échec.
2. Implémente jusqu'à faire passer ces tests, sans les modifier.
CONTRÔLES
T09-a  godot --headless --path . -s res://tests/run_all.gd ; echo $?   → 0, aucun marqueur T09 restant
T09-b  GODOT=<binaire> tools/ci/run_all_checks.sh ; echo $?            → 0
T09-c  Dans le rapport : aller-retour de l'identifiant 9223372036854775807 sans perte, avec la sortie du test qui le prouve
CONTRE-ÉPREUVE (CE) pour le vérificateur : passer la limite d'événements par lot à 257 → test_c04_envelope échoue.
```

## T10 — Modèle minimal, graphe déclaré, clés de sonde (C-01, C-02, C-05)

Qwen · A1 · file A · dépend de T07 et T09 · vérification : Gemini · pack de contexte CORE

Fichiers autorisés : `addons/godot_dev_mapper/core/`, les marqueurs T10 de `tests/pending/` (suppression seulement).

```text
Tu réalises la tâche T10 du projet GODOT_DEV_MAPPER. Applique les règles et le format de rapport du prompt universel de réalisation.
CONTEXTE : docs/CONTRACTS.md, sections C-01, C-02 et C-05, avec leurs tables de codes d'erreur ; contracts/schemas/declared_graph.v1.schema.json ; tests/contract/test_c01_identities.gd et test_c05_declared_graph.gd, avec leurs fixtures.
OBJECTIF : dans addons/godot_dev_mapper/core/, le modèle minimal, le chargeur de .flow.json v1 et la table des clés de sonde.
- Le chargeur rejette chaque fixture invalide avec le code d'erreur attendu, et celui-là seulement.
- Il conserve les références non résolues.
- Une clé de sonde inconnue donne « définition non résolue ».
- core/ ne dépend d'aucun autre module.
DÉROULÉ : supprime les marqueurs T10 de tests/pending/, montre l'échec, puis implémente.
CONTRÔLES
T10-a  runner → 0, aucun marqueur T10 restant
T10-b  python3 tools/check_deps.py ; echo $?   → 0
T10-c  GODOT=<binaire> tools/ci/run_all_checks.sh ; echo $?   → 0
CONTRE-ÉPREUVE (CE) pour le vérificateur : faire accepter au chargeur une clé de sonde présente dans deux définitions → test_c05 échoue sur le code de doublon.
```

## T11 — Event Store minimal (C-06)

Qwen · A1 · file A · dépend de T08 et T10 · vérification : Gemini · pack de contexte EDITOR

Fichiers autorisés : `addons/godot_dev_mapper/store/`, les marqueurs T11 de `tests/pending/` (suppression seulement).

```text
Tu réalises la tâche T11 du projet GODOT_DEV_MAPPER. Applique les règles et le format de rapport du prompt universel de réalisation.
CONTEXTE : docs/CONTRACTS.md, section C-06 (et C-04 pour le format reçu) ; tests/contract/test_c06_store.gd ; fixtures de tests/contract/fixtures/sessions/.
OBJECTIF : dans addons/godot_dev_mapper/store/, l'Event Store minimal du contrat :
- sessions et lacunes déduites des séquences ;
- rétention bornée, avec le marqueur « tronqué avant seq N » ;
- fin de session, et « fin inconnue » quand le message de fin manque ;
- requête « chemin observé » à trois états : cohérent, incohérent, indéterminé.
DÉROULÉ : supprime les marqueurs T11 de tests/pending/, montre l'échec, puis implémente.
CONTRÔLES
T11-a  runner → 0, aucun marqueur T11 restant
T11-b  GODOT=<binaire> tools/ci/run_all_checks.sh ; echo $?   → 0
T11-c  Dans le rapport : pour chaque fixture de session, l'état obtenu et l'état attendu par le contrat
CONTRE-ÉPREUVES (CE) pour le vérificateur
- supprimer le marqueur de troncature → test_c06 échoue ;
- classer « cohérent » une invocation touchée par un trou → test_c06 échoue.
```

## T12 — Façades de compatibilité et profil moteur (C-03)

Qwen · A1 · file B · dépend de T06 et T08 · vérification : Opus · pack de contexte COMPAT

Fichiers autorisés : `addons/godot_dev_mapper/compat/engine_facade.gd` et `engine_profile.gd`, `addons/godot_dev_mapper_runtime/runtime_facade.gd`, les marqueurs T12 de `tests/pending/` (suppression seulement).

```text
Tu réalises la tâche T12 du projet GODOT_DEV_MAPPER. Applique les règles et le format de rapport du prompt universel de réalisation.
CONTEXTE : docs/CONTRACTS.md, section C-03 ; docs/spikes/SPIKE-02.md (détection de capacités, isolation) ; docs/ARCHITECTURE.md (API sensibles) ; tests/contract/test_c03_facades.gd.
OBJECTIF
- Côté éditeur : les façades débogueur et éditeur, et le profil moteur (version affichée, capacités détectées selon les règles de SPIKE-02).
- Côté runtime : la façade du dossier autonome. Elle accepte un transport de substitution pour les tests et ne référence jamais le plugin éditeur.
- Les API sensibles n'apparaissent que dans ces fichiers.
DÉROULÉ : supprime les marqueurs T12 de tests/pending/, montre l'échec, puis implémente.
CONTRÔLES
T12-a  runner → 0 sur 4.7.2, aucun marqueur T12 restant
T12-b  python3 tools/check_deps.py ; echo $?   → 0
T12-c  Même runner avec le binaire de la préversion → résultat collé dans le rapport, sans exigence
T12-d  godot --headless --path . --check-only -s res://addons/godot_dev_mapper_runtime/runtime_facade.gd   → 0
CONTRE-ÉPREUVE (CE) pour le vérificateur : ajouter un appel à EngineDebugger dans store/ → check_deps échoue.
```

## T13a — FlowTrace : runtime et protocole de session (C-07)

Qwen · A1 · file B · dépend de T08, T09 et T12 · vérification : Opus · pack de contexte RUNTIME, plus `docs/spikes/SPIKE-01.md`

Fichiers autorisés : `addons/godot_dev_mapper_runtime/flow_trace.gd`, `tests/unit/test_flow_trace_internals.gd`, les marqueurs T13a de `tests/pending/` (suppression seulement).

```text
Tu réalises la tâche T13a du projet GODOT_DEV_MAPPER. Applique les règles et le format de rapport du prompt universel de réalisation.
CONTEXTE : docs/CONTRACTS.md, section C-07 (et C-04) ; docs/spikes/SPIKE-01.md, dont les constats sont obligatoires ; spikes/spike01_debugger/, en exemple seulement ; tests/contract/test_c07_flowtrace.gd.

OBJECTIF : addons/godot_dev_mapper_runtime/flow_trace.gd, classe à class_name FlowTrace, fonctions statiques, sans autoload. Elle passe par la façade runtime et couvre :
- l'API de C-07 et toute la table d'états du protocole de session ;
- le bail, la réserve de contrôle, la pile d'invocations ;
- le registre des instances et l'état initial envoyé au démarrage : une instance enregistrée avant le démarrage doit y figurer. Ce critère vient de SPIKE-01b, déplacé ici.
Constats de SPIKE-01a à respecter :
- le rappel de capture note la commande, appliquée à la frontière de frame suivante ;
- le crochet de frame est posé dès l'initialisation ;
- la capture est désenregistrée explicitement à la fin ;
- les messages du moteur sont ignorés.
Les tests unitaires utilisent le transport de substitution de la façade et une horloge factice.

DÉROULÉ : supprime les marqueurs T13a de tests/pending/, montre l'échec, puis implémente.

CONTRÔLES
T13a-a  runner → 0, aucun marqueur T13a restant
T13a-b  python3 tools/check_deps.py ; echo $?   → 0 ; le dossier runtime ne référence pas le plugin
T13a-c  GODOT=<binaire> tools/ci/run_all_checks.sh ; echo $?   → 0
T13a-d  Dans le rapport : chaque transition de la table d'états de C-07 avec le test qui la couvre
CONTRE-ÉPREUVES (CE) pour le vérificateur
- appliquer « stop » directement dans le rappel de capture → le test de réentrance échoue ;
- réserve de contrôle illimitée → le test « réserve pleine » échoue ;
- ne pas envoyer l'état initial → le test des instances antérieures échoue.
```

## T13b — Banc sans éditeur et scénarios de coupure

Qwen · A1 · file B · dépend de T13a · vérification : Opus · pack de contexte RUNTIME

Fichiers autorisés : `tools/harness/fake_editor.gd`, `tools/harness/demo_game/`, `tests/integration/run_session.sh`, `tools/ci/checks.d/40-integration.sh`.

```text
Tu réalises la tâche T13b du projet GODOT_DEV_MAPPER. Applique les règles et le format de rapport du prompt universel de réalisation.
CONTEXTE : docs/CONTRACTS.md, section C-07 ; docs/spikes/SPIKE-01.md ; spikes/spike01_debugger/receiver/, en exemple seulement.

OBJECTIF
1. tools/harness/fake_editor.gd : un récepteur qui joue l'éditeur sur le canal du débogueur. Réécris-le proprement à partir du récepteur de SPIKE-01a, avec un port configurable et des scénarios paramétrables : démarrage, arrêt, redémarrage, coupure.
2. tools/harness/demo_game/ : un mini-projet qui utilise FlowTrace, avec deux instances, dont une enregistrée avant le démarrage, et une décision.
3. tests/integration/run_session.sh : lance le banc et le mini-jeu, et vérifie :
   - aucun trou ;
   - aucun lot après « stopped » ;
   - état initial reçu au démarrage ;
   - bail déclenché après la coupure ;
   - jeu toujours actif.
   Code 0 si tout est vérifié, 1 sinon.
4. tools/ci/checks.d/40-integration.sh : exécute run_session.sh et affiche « CHECK integration OK » ou « CHECK integration KO ».
Si un scénario révèle un défaut de flow_trace.gd conforme au contrat, décris-le dans le rapport et passe en ESCALADE : la correction revient à la tâche T13a rouverte.

CONTRÔLES
T13b-a  tests/integration/run_session.sh avec GODOT=<4.7.2> ; echo $?   → 0
T13b-b  GODOT=<binaire> tools/ci/run_all_checks.sh ; echo $?   → 0, CHECK integration OK
CONTRE-ÉPREUVE (CE) pour le vérificateur : dans le mini-jeu, envoyer un lot après « stopped » → T13b-a échoue.
```

## T13c — Mesures de performance (SPIKE-05)

Qwen · A1 · file B · dépend de T13b · vérification : Gemini, qui relance la mesure · pack de contexte RUNTIME

Fichiers autorisés : `tools/bench/flow_trace_cost/`, `docs/spikes/SPIKE-05.md`.

```text
Tu réalises la tâche T13c du projet GODOT_DEV_MAPPER. Applique les règles et le format de rapport du prompt universel de réalisation.
CONTEXTE : plan §6 (coût du chemin désactivé) et §8 (budgets) ; docs/CONTRACTS.md, section C-07 (règles d'appel).

OBJECTIF
1. tools/bench/flow_trace_cost/ : un projet de mesure reproductible, lancé par une seule commande, qui mesure :
   - le coût d'un appel désactivé, côté appelant compris (arguments évalués) ;
   - le coût de la collecte active à 1 000 événements par seconde, en temps de frame, avec et sans collecte.
2. docs/spikes/SPIKE-05.md : méthode, machine, version de Godot, nombre de répétitions, chiffres, écart entre répétitions, conclusion au regard des objectifs du plan §8.

CONTRÔLES
T13c-a  La commande de mesure du rapport, relancée → chiffres du même ordre que ceux du rapport
T13c-b  SPIKE-05.md contient la commande, la machine, la version et au moins cinq répétitions
CONTRE-ÉPREUVE (CE) pour le vérificateur : ajouter une construction de chaîne coûteuse au point d'appel désactivé → le coût mesuré augmente nettement.
```
