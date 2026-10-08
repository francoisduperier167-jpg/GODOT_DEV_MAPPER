# Étape 3 — Contrats

Tâches : T07, puis finalisation de T08, préparé en parallèle · Budget : 4 à 6 h humaines · Prérequis : étape 2 acceptée

## Objectif

Geler les sept contrats du POC assez précisément pour déléguer l'implémentation sans aucune décision de conception. Écrire, avant le code, les tests qui jugeront cette implémentation.

## Obligations

- **Gabarit complet.** Chaque contrat a sept rubriques : objet, format ou API, exemples valides, exemples invalides, comportement en erreur, version, tests de contrat.
- **Validation en deux niveaux.** Les formats JSON (graphe déclaré, enveloppe runtime) ont un schéma dans `contracts/schemas/`, au format JSON Schema 2020-12 : types, champs requis, variantes d'événements, nombre maximal d'éléments. Un validateur complémentaire vérifie ce qu'un schéma ne garantit pas : références résolues, unicité d'une clé entre éléments, ordre des séquences, taille sérialisée en octets. En JSON Schema, `uniqueItems` compare des éléments entiers et `maxLength` compte des caractères, pas des octets. Chaque règle a un code d'erreur, commun au validateur Python et à l'implémentation GDScript.
- **Motif de rejet vérifié.** Une fixture invalide se nomme `invalid_<CODE>__<description>.json` et doit être rejetée avec ce code, et lui seul. Rejetée pour un autre motif, elle ne prouve rien.
- **Tests écrits par l'auteur du contrat.** Opus les écrit, pas l'implémenteur. Ils vont dans `tests/contract/`, chacun avec un marqueur dans `tests/pending/` qui nomme la tâche qui l'activera.
- **Fidélité aux sources.** Les contrats reprennent le plan directeur en vigueur (PD-0.5) et les rapports de spike. Tout écart est signalé, jamais glissé.
- **Gel.** Tu valides avant le gel. Après, toute modification passe par une analyse d'impact et un changement de version.

## Méthodologie

1. **T07** : C-01 identités, C-02 ancrage, C-05 graphe déclaré, avec le schéma, les fixtures et les tests.
2. **T08** : préparé en parallèle, finalisé après la validation de T07, car il s'appuie sur les identités et les clés de sonde. Il couvre C-03 façades, C-04 enveloppe, C-06 Event Store et C-07 FlowTrace.
3. **Relecture** : Gemini relit chaque contrat et cherche contradictions avec le plan, cas non spécifiés et exemples incohérents. Tu tranches.
4. **Règle de travail** : chaque règle du contrat a au moins un exemple invalide et un test qui le rejette.
5. **Testabilité** : un comportement qui ne se teste pas sans interface est découpé en une passerelle mince, non testée, et une logique pure, testée. Le contrat porte sur la logique pure.

## Points de contrôle

| ID | Contrôle | Commande | Attendu |
| --- | --- | --- | --- |
| PC3.1 | Gabarit complet | `python3 tools/check_contracts.py` | Code 0 |
| PC3.2 | Fixtures | `python3 tools/validate_fixtures.py` | Code 0 : les valides passent ; chaque invalide est rejetée avec le code de son nom, et lui seul |
| PC3.3 | Exemples du plan conformes | `python3 tools/validate_fixtures.py --plan-examples`, après T08 | Code 0 ; T07 ne valide que l'exemple du graphe déclaré |
| PC3.4 | (CE) Schéma vigilant | Retirer `evidence` d'une fixture valide, relancer PC3.2 | Code 1 |
| PC3.4b | (CE) Règle sémantique vigilante | Dupliquer une clé de sonde dans une fixture valide, relancer PC3.2 | Code 1, avec le code de doublon |
| PC3.5 | Tests en attente | Runner | Code 0 et pending ≥ 6 ; chaque test de `tests/contract/` a son marqueur dans `tests/pending/` |
| PC3.6 | Couverture du protocole de session | Chaque transition de la table d'états de C-07 a un test | Liste croisée dans le rapport de T08 |
| PC3.7 | Relecture | Rapport de Gemini | Aucune contradiction ouverte |
| PC3.8 | Gel | En-tête de `docs/CONTRACTS.md` | « Statut : validé », avec la date |

Dès la fin de T07, deux scripts de `tools/ci/checks.d/` rejouent PC3.1 et PC3.2 à chaque passage.

## Cheminement d'amélioration

- **Questions pendant l'étape 4.** On compte les questions par contrat. Au-delà de deux, le contrat est ambigu : on ajoute un exemple, avec un changement de version mineur.
- **Test intestable sans interface.** On découpe le composant : passerelle mince et logique pure.
- **Contrats trop longs.** Si `docs/CONTRACTS.md` dépasse 400 lignes, on le sépare en DATA_MODEL, RUNTIME_PROTOCOL et GRAPH_MODEL (règle de la méthodologie).
- **Écart avec le plan.** Si un écart revient deux fois en relecture, on amende le plan plutôt que de laisser vivre deux vérités.

## T07 — Contrats C-01, C-02, C-05

Opus · A1 · file A · vérification : Gemini, puis toi · contexte : plan §5 et §10, `docs/spikes/SPIKE-02.md`, `docs/DECISIONS.md`

Fichiers autorisés :
- `docs/CONTRACTS.md`, sections C-01, C-02 et C-05 ;
- `contracts/schemas/declared_graph.v1.schema.json` ;
- `tests/contract/fixtures/declared_graph/` ;
- `tests/contract/test_c01_identities.gd`, `tests/contract/test_c05_declared_graph.gd` ;
- les marqueurs T10 de `tests/pending/`, `tools/validate_fixtures.py`, `tools/check_contracts.py` ;
- `tools/ci/checks.d/30-contracts.sh`, `tools/ci/checks.d/31-fixtures.sh`.

```text
Tu rédiges les contrats C-01, C-02 et C-05 du projet GODOT_DEV_MAPPER, et les tests qui les jugeront. Tu n'écris aucune implémentation.

SOURCES NORMATIVES
docs/plan-directeur.md §5 (modèle, identités, clés de sonde, cycle de vie des instances, exemples) et §10 ; docs/spikes/SPIKE-02.md (clé de correspondance, UID) ; docs/DECISIONS.md.

DANS docs/CONTRACTS.md
Pour chaque contrat, remplis les sept rubriques : objet ; format ou API ; exemples valides ; exemples invalides ; comportement en erreur ; version ; tests de contrat.
- C-01 : identités de définition, instance, invocation, occurrence et session ; règles de cycle de vie des instances (enregistrement, arbre, destruction connue ou constatée) ; clés de sonde.
- C-02 : ancrage source et révision du programme ; règle de lien périmé (range_hash).
- C-05 : modèle minimal et format .flow.json v1 ; références non résolues.
Pour C-01 et C-05, les API GDScript attendues s'écrivent sous forme de signatures, avec le comportement en erreur. Chaque contrat liste ses codes d'erreur, communs au validateur Python et à l'implémentation GDScript.

À PRODUIRE AUSSI
- contracts/schemas/declared_graph.v1.schema.json (JSON Schema 2020-12) : il accepte l'exemple du plan §5 et rejette chaque exemple invalide.
- tests/contract/fixtures/declared_graph/ : des fichiers valid_*.json et des fichiers invalid_<CODE>__<description>.json, un code d'erreur par fichier. Au minimum : evidence absent, ancrage sans revision, relation vers une définition inexistante sans objet unresolved, clé de sonde dupliquée, schema_version inconnue.
- tools/validate_fixtures.py : valide chaque fixture en deux niveaux. Niveau 1 : le schéma JSON. Niveau 2 : les règles sémantiques (références résolues, unicité des clés de sonde entre définitions, ordre des séquences, taille sérialisée en octets UTF-8), chacune avec son code d'erreur. Une fixture invalid_<CODE>__… doit être rejetée avec ce code, et lui seul ; sinon, code 1. Avec --plan-examples, il extrait les blocs JSON du plan et les valide ; --kinds declared_graph limite cette validation à un format. Avec --file <chemin>, il valide un seul fichier, contre le schéma choisi par son champ kind.
- tools/check_contracts.py : vérifie que chaque section C-0x de docs/CONTRACTS.md a les sept rubriques. Arguments facultatifs : les ID à vérifier. Code 1 si une rubrique manque.
- tests/contract/test_c01_identities.gd et tests/contract/test_c05_declared_graph.gd : tests GDScript qui chargent les fixtures et appellent l'API décrite au contrat, qui n'existe pas encore. Crée pour chacun un marqueur tests/pending/<nom du test>.pending qui contient « T10 ».
- tools/ci/checks.d/30-contracts.sh et 31-fixtures.sh : ils exécutent check_contracts et validate_fixtures, et affichent leur ligne CHECK.

RÈGLES
Chaque règle du contrat a au moins un exemple invalide et un test qui le rejette. Tout écart avec le plan est listé en tête de ton rapport, sans être tranché.

CONTRÔLES
T07-a  python3 tools/check_contracts.py C-01 C-02 C-05 ; echo $?            → 0
T07-b  python3 tools/validate_fixtures.py ; echo $?                          → 0
T07-c  python3 tools/validate_fixtures.py --plan-examples --kinds declared_graph ; echo $?   → 0 (l'enveloppe attend T08)
T07-d  (CE) retire « evidence » d'une fixture valide, relance T07-b          → 1 ; annule
T07-d2 (CE) duplique une clé de sonde dans une fixture valide, relance T07-b → 1, avec le code de doublon ; annule
T07-e  (CE) supprime la rubrique « Comportement en erreur » de C-05, relance T07-a   → 1 ; annule
T07-f  godot --headless --path . -s res://tests/run_all.gd ; echo $?         → 0, pending=2
T07-g  godot --headless --path . --check-only -s res://tests/contract/test_c05_declared_graph.gd   → 0 seulement si l'API appelée est déclarée ; sinon, explique dans le rapport comment le test sera activé en T10
```

## T08 — Contrats C-03, C-04, C-06, C-07

Opus · A1 · file B · préparé en parallèle de T07, finalisé après sa validation · vérification : Gemini, puis toi · contexte : plan §4, §6 et §8, `docs/spikes/SPIKE-01.md` (01a et 01b), `docs/spikes/SPIKE-02.md`, C-01 validé

Fichiers autorisés :
- `docs/CONTRACTS.md`, sections C-03, C-04, C-06 et C-07 ;
- `contracts/schemas/envelope.v1.schema.json` ;
- `tests/contract/fixtures/envelope/`, `tests/contract/fixtures/sessions/` ;
- `tests/contract/test_c03_facades.gd`, `test_c04_envelope.gd`, `test_c06_store.gd`, `test_c07_flowtrace.gd` ;
- les marqueurs T09, T11, T12 et T13a de `tests/pending/`.

```text
Tu rédiges les contrats C-03, C-04, C-06 et C-07 du projet GODOT_DEV_MAPPER, et les tests qui les jugeront. Tu n'écris aucune implémentation. C-01 est validé : appuie-toi dessus sans le modifier.

SOURCES NORMATIVES
docs/plan-directeur.md §4 (façades), §6 (protocole de session, garanties, champs par type, chemin observé) et §8 (budgets, cycle de vie) ; docs/spikes/SPIKE-01.md, parties 01a et 01b ; docs/spikes/SPIKE-02.md.

DANS docs/CONTRACTS.md, les sept rubriques pour chaque contrat :
- C-03 Façades : pour chaque façade (runtime, débogueur, éditeur), la liste des opérations avec leur signature GDScript, leur comportement en erreur et la capacité qu'elles requièrent. La façade runtime accepte un transport de substitution pour les tests.
- C-04 Enveloppe : format des lots, champs communs et hérités, champs requis par type, limites (1 Ko par charge, 256 événements et 64 Ko par lot), réserve de contrôle de 64 places, identifiants 64 bits en chaîne, rejet d'une version inconnue.
- C-06 Event Store : sessions, lacunes déduites des séquences, rétention et marqueur « tronqué avant seq N », fin de session et « fin inconnue », requête « chemin observé » à trois états.
- C-07 FlowTrace : API statique (init, register, enter, exit, decision, enabled, shutdown) ; table d'états du protocole de session (inerte, prêt, collecte, arrêt demandé, arrêté, bail expiré, capture interrompue) avec toutes les transitions ; commandes appliquées à la frontière de frame ; bail de 2 s renouvelé toutes les 250 ms ; messages du moteur ignorés ; règles du chemin désactivé ; limite au périmètre synchrone.

À PRODUIRE AUSSI
- contracts/schemas/envelope.v1.schema.json et tests/contract/fixtures/envelope/ avec des fichiers valid_* et invalid_<CODE>__<description>. Au minimum : version de protocole inconnue, séquence non croissante dans un lot, décision sans payload.result, function_enter sans inv, lot de 257 événements, charge de plus de 1 Ko, identifiant 64 bits écrit comme nombre. La séquence non croissante et la charge de plus de 1 Ko, mesurée en octets, relèvent du niveau 2.
- tests/contract/fixtures/sessions/ : des sessions enregistrées au format de l'enveloppe. Au minimum : normale ; coupée sans fin ; avec trous ; mêlée de messages du moteur ; avec commande reçue en réentrance.
- Les quatre tests de contrat, chacun avec son marqueur dans tests/pending/ : C-04 → T09, C-06 → T11, C-03 → T12, C-07 → T13a.

RÈGLES
- Chaque transition de la table d'états de C-07 a au moins un test.
- Les constats de SPIKE-01a et 01b sont repris tels quels ; s'ils contredisent le plan, signale l'écart.
- Tout écart avec le plan est listé en tête de ton rapport.

CONTRÔLES
T08-a  python3 tools/check_contracts.py ; echo $?                            → 0 (sept contrats)
T08-b  python3 tools/validate_fixtures.py ; echo $?                          → 0
T08-b2 python3 tools/validate_fixtures.py --plan-examples ; echo $?   → 0 (tous les exemples du plan)
T08-c  (CE) remplace un identifiant chaîne par un nombre dans une fixture valide de l'enveloppe, relance T08-b   → 1 ; annule
T08-d  Tableau croisé dans le rapport : chaque transition de C-07 avec le test qui la couvre   → aucune transition sans test
T08-e  godot --headless --path . -s res://tests/run_all.gd ; echo $?         → 0, pending=6
```

Une fois T07 et T08 relus par Gemini, tu passes l'en-tête de `docs/CONTRACTS.md` à « Statut : validé », avec la date. Les contrats sont gelés.
