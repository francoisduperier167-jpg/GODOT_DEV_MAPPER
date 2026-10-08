# Étape 6 — Interface et robustesse

Tâches : file A : T16, puis T17 · file B : T18 · Budget : 3 à 4 h humaines · Prérequis : étape 5 acceptée

## Objectif

Montrer la démonstration du POC dans l'éditeur :
- un journal où l'on choisit une instance ;
- le chemin observé de chaque invocation, dans l'un de ses trois états ;
- l'ouverture du code à la bonne ligne, avec un avertissement si le fichier a changé.

En parallèle, prouver que l'outil ne casse rien : jeu sans débogueur, redémarrages, plugin désactivé pendant une collecte, session tuée.

## Obligations

- **L'interface ne calcule rien.** Toute la logique d'affichage vit dans `projections/` et se teste sans interface. Les scènes de `ui/` ne font qu'afficher.
- **Affichage borné.** Rafraîchissement à 30 Hz au plus ; journal virtualisé, qui ne crée de lignes que pour la partie visible.
- **Aucune affirmation causale.** Le chemin observé affiche « cohérent », « incohérent » ou « indéterminé — trace incomplète », jamais « cause ».
- **Latence mesurée en deux parties.** D'abord l'aller-retour du transport, par un ping mesuré avec la seule horloge de l'éditeur. Ensuite le délai entre la réception d'un lot et son affichage, lui aussi mesuré avec l'horloge de l'éditeur : il couvre l'Event Store, la projection et le rafraîchissement du panneau. Jamais en soustrayant des horodatages du jeu.
- **Accessibilité.** Les états ne reposent jamais sur la seule couleur.

## Méthodologie

- **T16 et T17.** IA 2 réalise l'interface et les projections, IA 3 vérifie. Les projections se testent avec des fixtures. Le panneau se vérifie en chargeant l'éditeur sans interface, puis visuellement sur ta machine, avec des captures d'écran jointes au rapport.
- **T18.** IA 2 réalise, IA 1 vérifie, car le cycle de vie touche au protocole. Les scénarios passent par le banc de test sans éditeur ; la désactivation dans l'éditeur réel attend ta machine.

## Points de contrôle

| ID | Contrôle | Commande ou preuve | Attendu |
| --- | --- | --- | --- |
| PC6.1 | Projections | Runner | Tests du journal et du chemin observé verts |
| PC6.2 | Panneau chargé | Contrôle PC1.2 étendu au marqueur `GDM_PANEL_READY` | Présent, aucune ligne d'erreur |
| PC6.3 | Tenue en charge | Test de projection sur 10 000 événements | Sous le seuil fixé dans le test (objectif : 50 ms) |
| PC6.4 | Trois états du chemin observé | Fixtures « cohérent », « incohérent », « trou », « sortie manquante » | État attendu pour chacune |
| PC6.5 | Lien périmé | Fixture de source modifiée après la trace | Avertissement présent |
| PC6.6 | Robustesse | `tests/integration/run_lifecycle.sh`, rejoué par `checks.d/65-lifecycle.sh` | Tous les scénarios verts |
| PC6.7 | Démonstration visuelle | Sur ta machine : captures d'écran ; aller-retour du transport ; délai réception → affichage | Deux instances distinguées ; latence estimée (moitié de l'aller-retour plus délai d'affichage) sous 200 ms au 95e centile |

## Cheminement d'amélioration

- **Interface lente.** On mesure d'abord la projection, puis le rendu. On virtualise ou on agrège avant d'optimiser le dessin.
- **Trop d'« indéterminé ».** On regarde les causes (trous, sorties manquantes) avant de toucher à l'affichage. Un « indéterminé » fréquent signale un problème de collecte, pas d'interface.
- **Retour visuel de ta part.** Chaque remarque devient une fixture ou un test de projection quand c'est possible, pour ne pas régresser.

## T16 — Panneau du POC

IA 2 · A1 · file A · dépend de T10 et T14 · vérification : IA 3 · pack de contexte EDITOR

Fichiers autorisés : `addons/godot_dev_mapper/projections/journal_projection.gd`, `addons/godot_dev_mapper/ui/poc_panel.tscn`, `addons/godot_dev_mapper/ui/poc_panel.gd`, `addons/godot_dev_mapper/editor/` (ajout du panneau, aller-retour, horodatage de réception), `addons/godot_dev_mapper/plugin.gd` (ajout du panneau uniquement), `tests/unit/test_journal_projection.gd`, `tools/ci/checks.d/60-panel.sh`.

```text
Tu réalises la tâche T16 du projet GODOT_DEV_MAPPER. Applique les règles et le format de rapport du prompt universel de réalisation.
CONTEXTE : docs/CONTRACTS.md, sections C-05 et C-06 ; plan §7 (le POC n'a pas de graphe dessiné) ; plan §8 (budgets d'affichage).

OBJECTIF
1. projections/journal_projection.gd, en logique pure :
   - filtre par instance, pagination, regroupement par invocation ;
   - liste des instances d'une session ;
   - graphe déclaré présenté en liste arborescente.
2. ui/poc_panel.tscn et poc_panel.gd :
   - un sélecteur d'instance, un journal virtualisé, l'arbre du graphe déclaré ;
   - rafraîchissement à 30 Hz au plus ;
   - GDM_PANEL_READY affiché si GDM_TRACE_LIFECYCLE vaut 1.
3. Mesures de latence, affichées dans une zone de diagnostic du panneau :
   - aller-retour du transport : l'éditeur envoie un ping horodaté par sa propre horloge, le jeu le renvoie, l'éditeur calcule ;
   - délai réception → affichage : la passerelle horodate chaque lot à sa réception ; le panneau calcule l'écart quand il affiche ses événements ; 95e centile sur la session ;
   - latence estimée : moitié de l'aller-retour plus ce délai.
4. tests/unit/test_journal_projection.gd, avec un test de tenue en charge sur 10 000 événements (seuil : 50 ms) et un test du délai réception → affichage avec une horloge factice.
5. tools/ci/checks.d/60-panel.sh : rejoue le contrôle T16-b et affiche « CHECK panel OK » ou « CHECK panel KO ».

CONTRÔLES
T16-a  runner → 0
T16-b  GDM_TRACE_LIFECYCLE=1 godot --headless --editor --path . --quit-after 300 > /tmp/ed.out 2>&1 ; grep -c GDM_PANEL_READY /tmp/ed.out ; grep -cE "^(ERROR|SCRIPT ERROR)" /tmp/ed.out   → 1 et 0
T16-c  python3 tools/check_deps.py ; echo $?   → 0 ; ui/ ne lit jamais le store directement
T16-d  GODOT=<binaire> tools/ci/run_all_checks.sh ; echo $?   → 0
T16-e  Test du délai réception → affichage, avec une horloge factice → vert ; la zone de diagnostic affiche les deux mesures
CONTRE-ÉPREUVE (CE) pour le vérificateur : ignorer le filtre d'instance dans la projection → test_journal_projection échoue.
SUR MA MACHINE, plus tard (PC6.7) : la procédure pour les captures d'écran et la mesure de latence, écrite dans ton rapport.
```

## T17 — Chemin observé et ouverture du code

IA 2 · A1 · file A · dépend de T15 et T16 · vérification : IA 3 · packs de contexte CORE et EDITOR

Fichiers autorisés : `addons/godot_dev_mapper/projections/observed_path.gd`, `addons/godot_dev_mapper/editor/source_opener.gd`, `addons/godot_dev_mapper/ui/poc_panel.gd` (affichage), `tests/unit/test_observed_path.gd`, `tests/unit/fixtures/observed_path/`.

```text
Tu réalises la tâche T17 du projet GODOT_DEV_MAPPER. Applique les règles et le format de rapport du prompt universel de réalisation.
CONTEXTE : docs/CONTRACTS.md, sections C-02 (ancrage, range_hash) et C-06 (requête « chemin observé ») ; plan §6.

OBJECTIF
1. projections/observed_path.gd : pour une invocation, rassemble ses événements et ses invocations enfants, puis renvoie l'un des trois états :
   - « cohérent avec la branche déclarée » ;
   - « incohérent » ;
   - « indéterminé — trace incomplète », quand un trou touche l'invocation, qu'une sortie manque ou que la corrélation n'est pas garantie.
   Chaque état est accompagné de ses preuves.
2. editor/source_opener.gd, passerelle mince : ouvre le script à la ligne de l'ancrage, par la façade éditeur. Avant d'ouvrir, compare le range_hash actuel et celui de l'ancrage ; en cas d'écart, affiche « lien périmé ».
3. tests/unit/test_observed_path.gd et ses fixtures : cohérent, incohérent, trou, sortie manquante, réentrance non garantie, source modifiée.

CONTRÔLES
T17-a  runner → 0
T17-b  Dans le rapport : pour chaque fixture, l'état attendu et l'état obtenu
T17-c  python3 tools/check_deps.py ; echo $?   → 0
T17-d  GODOT=<binaire> tools/ci/run_all_checks.sh ; echo $?   → 0
CONTRE-ÉPREUVES (CE) pour le vérificateur
- ignorer les trous → la fixture « trou » donne « cohérent » et le test échoue ;
- ne pas comparer le range_hash → le test « source modifiée » échoue.
SUR MA MACHINE, plus tard : un clic ouvre le bon fichier à la bonne ligne.
```

## T18 — Robustesse et cycle de vie

IA 2 · A1 · file B · dépend de T13b et T14 · vérification : IA 1 · pack de contexte RUNTIME

Fichiers autorisés : `tests/integration/run_lifecycle.sh`, `tools/harness/` (nouveaux scénarios), `tests/unit/test_session_controller.gd` (nouveaux cas), `tools/ci/checks.d/65-lifecycle.sh`. Pour corriger un défaut sans changer de contrat : `addons/godot_dev_mapper_runtime/flow_trace.gd` et `addons/godot_dev_mapper/editor/session_controller.gd`. Les tests de contrat restent intouchables ; une correction qui exigerait de changer un contrat passe par QUESTION.

```text
Tu réalises la tâche T18 du projet GODOT_DEV_MAPPER. Applique les règles et le format de rapport du prompt universel de réalisation.
CONTEXTE : plan §8 (cycle de vie : trois opérations) ; docs/CONTRACTS.md, section C-07 ; docs/spikes/SPIKE-01.md.

OBJECTIF : prouver par des scénarios automatiques que l'outil ne casse pas le jeu. tests/integration/run_lifecycle.sh enchaîne :
1. le jeu du banc de test lancé sans débogueur : aucune ligne d'erreur, FlowTrace inerte ;
2. cinq démarrages et arrêts de collecte de suite : aucun lot après « stopped », séquences continues ;
3. coupure du récepteur pendant la collecte : arrêt par le bail en 2 s au plus, jeu toujours actif ;
4. jeu tué pendant la collecte (kill -9) : le contrôleur de session conclut « fin inconnue » ;
5. désactivation du plugin pendant une collecte, simulée sur le contrôleur : arrêt envoyé, attente d'une seconde au plus, puis retrait ;
6. jeu redémarré après un arrêt : nouvelle session, aucun mélange avec l'ancienne.
Si un scénario échoue à cause du runtime ou du contrôleur, corrige le défaut s'il se corrige sans changer de contrat, et décris-le dans le rapport. S'il faut changer un contrat : statut QUESTION, avec le diagnostic.
Ajoute tools/ci/checks.d/65-lifecycle.sh, qui exécute run_lifecycle.sh et affiche « CHECK lifecycle OK » ou « CHECK lifecycle KO ».

CONTRÔLES
T18-a  tests/integration/run_lifecycle.sh ; echo $?   → 0, un OK par scénario
T18-b  GODOT=<binaire> tools/ci/run_all_checks.sh ; echo $?   → 0
CONTRE-ÉPREUVE (CE) pour le vérificateur : envoyer un lot après « stopped » dans le mini-jeu → le scénario 2 échoue.
SUR MA MACHINE, plus tard : désactiver le plugin pendant une vraie collecte, procédure écrite dans ton rapport.
```
