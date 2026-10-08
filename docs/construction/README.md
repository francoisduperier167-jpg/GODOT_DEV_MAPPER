# Guide de construction, étape par étape

Révision GC-0.4 · statut : **proposé** · 8 octobre 2026 · fondé sur PD-0.5, OR-0.5, MC-0.5 et SPIKE-01a

**Changements depuis GC-0.3** : déroulé séquentiel pour le mode autonome (`sequence.md`) ; T05 ne dépend plus de T01 ; PC2.1 compte six critères ; T05 exécutable sous écran virtuel.

**En mode autonome (D-09)**, l'ordre d'exécution, les rôles des trois IA, le prompt de créneau et les adaptations des étapes sont dans `sequence.md`. Ce guide reste la référence de chaque tâche : objectif, fichiers autorisés, contrôles, prompts.

**Changements depuis GC-0.2**, après une relecture externe :
- copies de travail isolées pour chaque tâche et pour son vérificateur ;
- plus aucun fichier partagé modifié par les agents : marqueurs de tests en attente, un script par contrôle ajouté, état du projet mis à jour à la fusion ;
- QUESTION réservée aux changements de contrat, de périmètre ou d'interface publique ;
- validation des formats en deux niveaux, avec motif de rejet vérifié ;
- T13 découpée en trois tâches ; latence mesurée en deux parties ; mesure de valeur exploratoire ;
- permissions et prérequis de T05, T06, T07, T17, T18 et P6 mis en cohérence.

**Pour savoir quoi faire maintenant**, ouvre la carte interactive `carte.html` : elle affiche une seule action à la fois, le modèle à lancer, le prompt à copier, et ce qui se passe selon le résultat. Ce guide en est la référence détaillée.

Ce guide décrit chaque étape de la construction du plugin, de l'étape 0 à la V1. Chaque étape a les mêmes six parties :
- objectif ;
- obligations ;
- méthodologie ;
- points de contrôle ;
- cheminement d'amélioration ;
- prompts : un pour qu'une IA réalise le travail, un pour qu'une autre IA le vérifie.

## Ce que « valider à coup sûr » veut dire ici

Aucun prompt ne garantit seul un résultat juste : un modèle peut se tromper tout en croyant réussir. La sûreté vient de quatre verrous, appliqués à chaque tâche.

1. **Des contrôles exécutables.** Chaque critère est une commande dont le résultat attendu est précis : un code de sortie, une ligne présente, une ligne absente. Jamais « le code semble correct ».
2. **Des contre-épreuves.** Pour chaque contrôle important, on casse volontairement le comportement et on vérifie que le contrôle échoue. Un contrôle qui ne peut pas échouer ne prouve rien. Dans les fiches, ces contrôles portent la marque **(CE)**.
3. **Un vérificateur indépendant.** Un autre modèle que l'auteur relance les contrôles, applique les contre-épreuves et cherche les contournements. Il ne modifie rien. Les tests de contrat sont écrits par l'auteur du contrat, et l'implémenteur n'a pas le droit d'y toucher.
4. **Une porte humaine.** À la fin de chaque étape, tu lis le rapport de vérification et tu décides.

## Commandes de contrôle vérifiées

Commandes exécutées le 8 octobre 2026 avec Godot 4.7.2 officiel sous Linux, et gdtoolkit 4.5.0.

| Commande | Comportement constaté |
| --- | --- |
| `godot --headless --path . --import` | Importe le projet ; code 0 |
| `godot --headless --editor --path . --quit-after 300` | Ouvre l'éditeur sans interface, charge les plugins activés, puis quitte |
| `godot --headless --path . -s res://tests/run_all.gd` | Exécute un script qui étend SceneTree ; `quit(n)` fixe le code de sortie |
| `godot --headless --path . --check-only -s res://chemin.gd` | Code 1 sur une erreur de syntaxe, 0 sinon |
| `gdlint <dossiers>` | Code 1 au moindre problème |
| `gdformat --check <dossiers>` | Code 1 si un fichier serait reformaté |
| `godot … --remote-debug tcp://127.0.0.1:6007` | Connecte le jeu à un récepteur de débogage : c'est la base du banc de test sans éditeur (SPIKE-01a) |

**Piège de la deuxième commande** : l'éditeur sans interface sort avec le code 0, même quand un script du plugin ne compile pas. Les contrôles comptent donc aussi les lignes qui commencent par `ERROR` ou `SCRIPT ERROR`.

Dans les fiches, `godot` désigne le binaire de la version testée ; la CI le lit dans `versions.json`.

## Copies de travail et fichiers partagés

Chaque tâche se fait dans sa propre copie de travail Git, et sa vérification dans une autre. Deux tâches en parallèle ne se gênent donc jamais, et une contre-épreuve ne peut rien effacer d'autre.

| Moment | Commande, depuis le dossier principal du dépôt |
| --- | --- |
| Début de la tâche | `git worktree add ../gdm-{ID} -b tache/{ID} main` ; l'auteur travaille dans `../gdm-{ID}` |
| Vérification | `git worktree add --detach ../gdm-verif-{ID} tache/{ID}` ; le vérificateur travaille dans `../gdm-verif-{ID}` |
| Fin de la vérification | `git worktree remove --force ../gdm-verif-{ID}` |
| Fusion | `git switch main`, `git merge --no-ff tache/{ID}`, puis `tools/ci/run_all_checks.sh` sur main, puis `git worktree remove ../gdm-{ID}` |

Les agents ne modifient jamais un fichier que plusieurs tâches partagent :
- **`PROJECT_STATE.md` et `docs/DECISIONS.md`** : mis à jour seulement à l'étape de fusion, sur main, par toi ou à ta demande.
- **Tests en attente** : un marqueur par test, `tests/pending/<nom du test>.pending`, qui contient l'identifiant de la tâche. Une tâche supprime seulement ses propres marqueurs.
- **Contrôles ajoutés** : un script par contrôle, `tools/ci/checks.d/NN-nom.sh`. `run_all_checks.sh` les exécute dans l'ordre ; après T03, personne ne le modifie.

L'étape de fusion est aussi l'étape d'intégration : `run_all_checks.sh` y est relancé sur main. S'il échoue, la fusion est annulée avec `git reset --hard ORIG_HEAD`, avant tout envoi de main, et la tâche repart en correction sur sa branche. Un `git revert` ne convient pas ici : une nouvelle fusion de la même branche ne réappliquerait pas les changements annulés.

## Fichiers du guide

| Fichier | Contenu |
| --- | --- |
| `sequence.md` | Déroulé séquentiel du mode autonome : une unité après l'autre, trois IA en rotation, recette humaine finale |
| `etape-0.md` | Décisions, squelettes de documents, environnement de Qwen (T00) |
| `etape-1.md` | Fondations : projet, runner, contrôle de dépendances, CI, banc d'essai (T01 à T04) |
| `etape-2.md` | Spikes : partie éditeur du canal (T05), frontière de compatibilité (T06) |
| `etape-3.md` | Contrats C-01 à C-07, schémas et tests de contrat (T07, T08) |
| `etape-4.md` | Implémentation sous contrat (T09 à T13c) |
| `etape-5.md` | Intégration : réception côté éditeur, instrumentation du banc d'essai (T14, T15) |
| `etape-6.md` | Interface et robustesse (T16 à T18) |
| `etape-7.md` | Mesure de valeur et revue de continuation (T19, T20) |
| `mvp.md` | Phases P4a à P8, avec leur prompt de découpage |
| `v1.md` | Phases P9 à P16, avec leur prompt de découpage |

Le POC est détaillé tâche par tâche. Le MVP et la V1 sont décrits phase par phase : leur découpage en tâches dépend des résultats du POC, et un prompt dédié le produit au moment voulu.

## Statuts d'une tâche

À faire → En cours → À vérifier → Acceptée, ou Refusée.

Une tâche s'arrête en **QUESTION** seulement s'il faudrait changer un contrat, le périmètre ou une interface publique, ou modifier un fichier hors de sa liste. Les choix d'implémentation conformes au contrat, l'agent les tranche et les note dans son rapport. Une tâche passe en **ESCALADE** après deux échecs au même contrôle. Le statut vit dans `PROJECT_STATE.md`, mis à jour à l'étape de fusion.

## Qui vérifie qui

| Auteur | Vérificateur |
| --- | --- |
| Qwen | Opus pour le protocole, les façades et les formats ; Gemini sinon |
| Sonnet | Gemini |
| Gemini | Sonnet |
| Opus | Gemini |

Dans tous les cas, la porte d'étape revient à toi.

## Prompt universel de réalisation

`REGLES_AGENTS.md`, créé à l'étape 0, en reprend les règles : elles sont ainsi chargées par chaque agent. Les prompts des fiches le complètent avec l'objectif, les fichiers et les contrôles de la tâche.

```text
Tu réalises la tâche {ID} du projet GODOT_DEV_MAPPER, un plugin pour Godot 4.7.2 écrit en GDScript.

À LIRE AVANT TOUT, dans cet ordre :
1. docs/construction/{fichier d'étape}, section {ID} : objectif, fichiers, contrôles.
2. Les documents cités dans la ligne « Contexte » de la tâche.
3. PROJECT_STATE.md.

RÈGLES NON NÉGOCIABLES
- Tu travailles uniquement dans la copie de travail de la tâche, ../gdm-{ID}, sur la branche tache/{ID}.
- Tu ne modifies que les fichiers autorisés de la tâche. Si un autre fichier doit changer, tu t'arrêtes avec le statut QUESTION.
- Tu ne modifies jamais tests/contract/ (tests et fixtures de contrat), contracts/, docs/CONTRACTS.md, docs/construction/, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la tâche les liste dans ses fichiers autorisés. Dans tests/pending/, tu supprimes seulement les marqueurs de ta tâche.
- Tu tranches toi-même les choix d'implémentation qui respectent le contrat, et tu les notes dans ton rapport. Tu t'arrêtes avec le statut QUESTION seulement pour un changement de contrat, de périmètre ou d'interface publique.
- Avant d'utiliser une API Godot dont tu n'es pas certain qu'elle existe en 4.7.2, tu écris un script de trois lignes qui l'appelle et tu l'exécutes. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée ; tu colles sa sortie réelle.

DÉROULÉ
1. Reformule l'objectif en une phrase. Liste les fichiers que tu vas créer ou modifier, puis les contrôles que tu exécuteras.
2. Si la tâche a des tests en attente, supprime ses marqueurs dans tests/pending/ et montre que ces tests échouent.
3. Implémente le plus petit changement qui satisfait les contrôles.
4. Exécute tous les contrôles de la tâche, puis tools/ci/run_all_checks.sh s'il existe.
5. Si un contrôle échoue, corrige. Après deux tentatives infructueuses sur le même contrôle : statut ESCALADE.
6. Ne touche pas à PROJECT_STATE.md : ton rapport donne le statut, le temps passé et les écarts, et l'étape de fusion les reporte.

RAPPORT FINAL, dans ce format exact
- Statut : TERMINÉ | QUESTION | ESCALADE
- Fichiers modifiés : liste
- Contrôles : pour chacun, commande, code de sortie, 10 dernières lignes de sortie
- Contre-épreuves faites : liste, ou « aucune demandée »
- Écarts au contrat ou au guide : aucun, ou liste
- Hypothèses faites : aucune, ou liste
- Questions : aucune, ou liste
- Temps passé et nombre de tentatives : …
```

## Prompt universel de vérification

```text
Tu es vérificateur indépendant pour la tâche {ID} du projet GODOT_DEV_MAPPER. Tu n'as pas écrit ce code. Tu travailles dans ta propre copie de travail, ../gdm-verif-{ID}, créée sur le commit à vérifier : tu n'y fais aucun commit, et tu ne touches à aucune autre copie.

ENTRÉES : la section {ID} de docs/construction/{fichier d'étape}, le rapport de l'auteur, la branche tache/{ID} et la branche main.

1. PÉRIMÈTRE. Exécute git diff --name-only main...tache/{ID}. Tout fichier hors de la liste autorisée est un motif de refus.
2. ÉTAT PROPRE. Ta copie est neuve : importe le projet, puis exécute chaque contrôle de la tâche et tools/ci/run_all_checks.sh. Note les codes de sortie et les lignes clés.
3. CONTRE-ÉPREUVES. Pour chaque contrôle marqué (CE), applique le sabotage décrit, vérifie que le contrôle échoue, puis annule avec git checkout -- . et git clean -fd, dans ta copie seulement. Un contrôle qui ne détecte pas son sabotage est un motif de refus.
4. CONTOURNEMENTS. Cherche :
   - test sans assertion, ou toujours vrai ;
   - test désactivé, renommé ou sorti du runner ;
   - valeur attendue recopiée depuis la sortie du code ;
   - marqueur supprimé de tests/pending/ sans test qui passe ;
   - fixture invalide rejetée pour un autre motif que celui de son nom ;
   - API Godot inventée ou non vérifiée ;
   - dépendance interdite entre modules ;
   - API sensible hors de la frontière de compatibilité ;
   - affirmation du rapport sans sortie qui la prouve.
5. COHÉRENCE. Compare le comportement au contrat cité et aux invariants INV-01 à INV-09 concernés.

VERDICT, dans ce format exact
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte
```

## Prompt d'escalade

```text
La tâche {ID} du projet GODOT_DEV_MAPPER a échoué deux fois au contrôle {contrôle}. Tu reçois la section de la tâche, le diff, les sorties des deux tentatives et le rapport de l'auteur.
1. Diagnostique la cause : erreur d'implémentation, API Godot absente ou différente, contrat ambigu ou faux, contrôle faux, environnement.
2. Si l'implémentation est en cause, fais la correction minimale et exécute tous les contrôles.
3. Si le contrat, le contrôle ou le guide est en cause, ne corrige rien : rédige une proposition de modification, avec son impact, pour validation humaine.
Rapport : cause, preuve, action faite ou proposée, statut.
```

## Prompt de porte d'étape

```text
Prépare la porte de sortie de l'étape {N} du projet GODOT_DEV_MAPPER. Entrées : docs/construction/etape-{N}.md, les verdicts de vérification de chaque tâche, PROJECT_STATE.md.
Pour les points de contrôle couverts par tools/ci/run_all_checks.sh, exécute ce script une fois sur main : son résultat fait foi. Exécute toi-même les autres points de contrôle de l'étape, puis produis une page :
- tableau : point de contrôle, commande, attendu, obtenu, OK ou KO ;
- heures humaines et temps agent consommés, contre le budget de l'étape ;
- problèmes ouverts et risques nouveaux ;
- recommandation : passer, corriger d'abord, ou revoir le plan.
Tu ne décides pas : la décision est humaine.
```

## Cheminement d'amélioration

Après chaque étape, une rétro de dix minutes compare ce qui s'est passé aux signaux ci-dessous. Si l'étape n'a connu ni refus, ni escalade, ni QUESTION, la rétro se réduit à noter les temps : pas de prompt.

| Signal | Lecture | Correction |
| --- | --- | --- |
| Une tâche demande plus de deux échanges de clarification | Le guide ou le contrat est ambigu | Ajouter un exemple ou une règle à la section concernée |
| Le vérificateur refuse pour un contournement | Le prompt laisse une porte ouverte | Ajouter l'interdit au prompt universel et à `REGLES_AGENTS.md` |
| Une contre-épreuve n'est pas détectée | Le contrôle est trop faible | Renforcer le contrôle avant de continuer |
| Deux escalades sur un même module | Le modèle ou le pack de contexte ne suffit pas | Changer de modèle, ou enrichir le pack |
| Budget d'étape dépassé de 50 % | Les tâches sont trop grosses | Scinder les tâches suivantes ; revue de continuation |
| Une API Godot diffère de l'attendu | Connaissance des modèles périmée | Ajouter le fait vérifié au guide et au pack COMPAT |
| Même erreur répétée deux fois par un agent | Règle manquante | Une ligne de plus dans `REGLES_AGENTS.md` |

```text
Rétro de l'étape {N} du projet GODOT_DEV_MAPPER. Entrées : verdicts, rapports, PROJECT_STATE.md, temps consommés.
Produis au plus trois améliorations. Pour chacune : signal observé, cause probable, modification exacte (fichier, section, texte avant, texte après).
Dis aussi s'il faut garder ou changer le routage des modèles, avec la mesure qui le justifie.
Ne modifie rien : la décision est humaine.
```

Chaque amélioration acceptée est appliquée au guide, dont la révision augmente (GC-0.4, GC-0.5…).

## Carte des étapes

| Étape | Tâches | Heures humaines | Possible sans ta machine |
| --- | --- | --- | --- |
| 0 Décisions et environnement | Décisions, squelettes, T00 | 2–4 | Squelettes : oui. Décisions : non, elles sont à toi. T00 : non, Qwen est local |
| 1 Fondations | T01 à T04 | 4–6 | T01 à T03 : oui, sauf l'envoi sur GitHub. T04 : en partie |
| 2 Spikes | T05, T06 | 4–6 | T06 : oui. T05 : oui sous écran virtuel avec rendu logiciel (vérifié le 8 octobre 2026) ; la mesure sur GPU reste à faire sur ta machine |
| 3 Contrats | T07, T08 | 4–6 | T07 : oui. T08 : non, il attend SPIKE-01b (T05). La validation reste à toi |
| 4 Implémentation | T09 à T13c | 4–7, objectif favorable | Godot sans interface suffit, mais tout dépend de T08, donc de T05 |
| 5 Intégration | T14, T15 | 2–4 | Après T08 : T15 et la logique de T14. Essai dans l'éditeur : non |
| 6 Interface et robustesse | T16 à T18 | 3–4 | Après T08 : logique et tests. Vérification visuelle : non |
| 7 Valeur et revue | T19, T20 | 2–3 | Non : mesure et décision humaines |
| **POC** | | **25–40** | |
| MVP | P4a à P8 | 43–74 | Voir `mvp.md` |
| V1 | P9 à P16 | 75–120 | Voir `v1.md` |

Sans ta machine, le projet avance jusqu'à T07 : décisions, squelettes, T01 à T04, T06 et T07. T08 attend SPIKE-01b (T05), qui demande l'éditeur avec rendu : un écran virtuel avec rendu logiciel suffit, ce qui a été vérifié le 8 octobre 2026 dans un conteneur, sur Godot 4.7.2. La carte interactive applique ces dépendances d'elle-même.

## Outillage créé au fil des étapes

| Fichier | Créé en | Rôle |
| --- | --- | --- |
| `REGLES_AGENTS.md`, `tools/sync_rules.sh` | Étape 0 | Source unique des règles, copiée vers `CLAUDE.md` et `GEMINI.md` |
| `tests/run_all.gd`, `tests/gdm_test.gd`, `tests/pending/` | T02 | Runner, assertions, un marqueur par test pas encore activé |
| `tools/check_deps.py`, `tools/deps_rules.json` | T02 | Règles de dépendance entre modules et API sensibles |
| `tools/ci/run_all_checks.sh`, `tools/ci/checks.d/`, `tools/ci/fetch_godot.sh` | T03 | Tous les contrôles en une commande, un script par contrôle ajouté ; binaires officiels |
| `contracts/schemas/`, `tools/validate_fixtures.py`, `tools/check_contracts.py` | T07, T08 | Schémas JSON, règles sémantiques à codes d'erreur, contrôle des contrats |
| `tools/harness/fake_editor.gd` | T13b | Banc de test du runtime sans éditeur, issu de SPIKE-01a |
