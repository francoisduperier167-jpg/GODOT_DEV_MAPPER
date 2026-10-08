# Étape 5 — Intégration

Tâches : file A : T14 · file B : T15 · Budget : 2 à 4 h humaines · Prérequis : étape 4 acceptée ; T04 accepté pour T15

## Objectif

Faire arriver dans l'Event Store de l'éditeur les événements d'un vrai jeu instrumenté. À la fin, le banc d'essai émet des événements avec les bonnes clés de sonde et deux instances distinctes ; l'éditeur les reçoit, les valide et les range.

## Obligations

- **Découpage testable.** La réception côté éditeur se divise en deux :
  - une passerelle mince (`editor/debugger_bridge.gd`), qui ne fait que relayer les messages de l'EditorDebuggerPlugin ;
  - un contrôleur de session en logique pure (`editor/session_controller.gd`), entièrement testé sans interface.
- **Protocole de C-07 côté éditeur.** Démarrage, bail toutes les 250 ms, arrêt avec attente d'une seconde au plus, « fin inconnue », messages du moteur ignorés.
- **Instrumentation hors du dépôt.** Elle vit dans une branche `gdm-instrumentation` de la copie de travail du jeu. Seul le graphe déclaré, `benches/<nom>/flow.json`, entre dans le dépôt : il ne contient aucun code du jeu.
- **Aucune clé orpheline.** Chaque clé de sonde du code instrumenté existe dans `flow.json`.

## Méthodologie

- **T14.** IA 2 réalise, IA 3 vérifie. Le contrôleur se teste avec les sessions enregistrées de `tests/contract/fixtures/sessions/` : normale, coupée, avec trous, mêlée de messages du moteur, avec commande en réentrance. La passerelle se vérifie en chargeant l'éditeur sans interface, puis sur ta machine dans l'éditeur réel.
- **T15.** IA 2 réalise, IA 3 vérifie. L'instrumentation suit les règles d'appel de C-07 : clés en StringName littéraux, et `if FlowTrace.enabled:` devant toute charge coûteuse.

## Points de contrôle

| ID | Contrôle | Commande ou preuve | Attendu |
| --- | --- | --- | --- |
| PC5.1 | Contrôleur de session | Runner | Tests du contrôleur verts sur toutes les sessions enregistrées |
| PC5.2 | Passerelle chargée | Contrôle PC1.2 étendu au marqueur `GDM_BRIDGE_READY` | Présent, aucune ligne d'erreur |
| PC5.3 | Banc d'essai sans débogueur | Jeu lancé sans `--remote-debug` | Aucune ligne d'erreur ; FlowTrace inerte |
| PC5.4 | Banc d'essai avec le banc de test | `tests/integration/run_bench.sh`, rejoué par `checks.d/55-bench.sh` | Clés attendues, deux instances distinctes, aucune destruction après réinsertion ; à la porte, OK et jamais IGNORÉ |
| PC5.5 | Clés orphelines | `python3 tools/check_probe_keys.py` | Code 0 |
| PC5.6 | Essai dans l'éditeur réel | Sur ta machine : une session du banc d'essai jusqu'au store | Compteurs cohérents avec le banc de test |

PC5.6 attend ta machine. Les autres contrôles passent sans elle.

## Cheminement d'amélioration

- **Le contrôleur grossit.** On sépare la machine à états et la gestion du bail.
- **L'éditeur réel diffère du banc de test.** On enregistre la session réelle comme nouvelle fixture, et le test du contrôleur la rejoue ensuite à chaque passage.
- **Instrumentation fastidieuse.** On note le temps passé par point instrumenté : c'est une donnée de la mesure de valeur (T19). Au-delà de cinq minutes par point, c'est un risque de valeur à porter en revue.

## T14 — Réception côté éditeur

IA 2 · A1 · file A · dépend de T09, T11, T12, T13a · vérification : IA 3 · pack de contexte EDITOR

Fichiers autorisés : `addons/godot_dev_mapper/editor/debugger_bridge.gd`, `addons/godot_dev_mapper/editor/session_controller.gd`, `addons/godot_dev_mapper/plugin.gd` (enregistrement de la passerelle uniquement), `tests/unit/test_session_controller.gd`, `tools/ci/checks.d/50-bridge.sh`.

```text
Tu réalises la tâche T14 du projet GODOT_DEV_MAPPER. Applique les règles et le format de rapport du prompt universel de réalisation.
CONTEXTE : docs/CONTRACTS.md, sections C-03 (façade débogueur), C-04, C-06 et C-07 ; docs/spikes/SPIKE-01.md, section 01b ; tests/contract/fixtures/sessions/.

OBJECTIF
1. editor/session_controller.gd, en logique pure, sans aucune API d'éditeur :
   - côté éditeur du protocole de session : prêt, démarrage, bail toutes les 250 ms, arrêt avec attente d'une seconde au plus ;
   - « fin inconnue » si le message de fin manque ;
   - messages du moteur ignorés ;
   - lots validés par le codec, puis rangés dans l'Event Store.
   Le temps lui est fourni de l'extérieur, pour être testable.
2. editor/debugger_bridge.gd : la passerelle mince. Elle relaie les messages de la façade débogueur vers le contrôleur, et ses ordres vers la session. Elle affiche GDM_BRIDGE_READY si GDM_TRACE_LIFECYCLE vaut 1.
3. plugin.gd : seulement l'enregistrement et le retrait de la passerelle.
4. tests/unit/test_session_controller.gd : rejoue chaque session de tests/contract/fixtures/sessions/ et vérifie l'état final attendu.
5. tools/ci/checks.d/50-bridge.sh : rejoue le contrôle T14-b et affiche « CHECK bridge OK » ou « CHECK bridge KO ».

CONTRÔLES
T14-a  runner → 0, tests du contrôleur verts
T14-b  GDM_TRACE_LIFECYCLE=1 godot --headless --editor --path . --quit-after 300 > /tmp/ed.out 2>&1 ; grep -c GDM_BRIDGE_READY /tmp/ed.out ; grep -cE "^(ERROR|SCRIPT ERROR)" /tmp/ed.out   → 1 et 0
T14-c  python3 tools/check_deps.py ; echo $?   → 0 ; session_controller.gd sans API sensible
T14-d  GODOT=<binaire> tools/ci/run_all_checks.sh ; echo $?   → 0
CONTRE-ÉPREUVES (CE) pour le vérificateur
- arrêter le bail dans le contrôleur → le test de la session coupée échoue ;
- traiter « set_pid » comme un lot → le test de la session mêlée échoue.
SUR MA MACHINE, plus tard (PC5.6) : la procédure exacte pour vérifier une vraie session, écrite dans ton rapport.
```

## T15 — Instrumentation du banc d'essai

IA 2 · A1 · file B · dépend de T04 et T13b · vérification : IA 3 · contexte : `docs/benches/<nom>.md`, C-01, C-05, C-07

Fichiers autorisés dans le dépôt : `benches/<nom>/flow.json`, `tools/check_probe_keys.py`, `tests/integration/run_bench.sh`, `docs/benches/<nom>.md`, `tools/ci/checks.d/55-bench.sh`. Dans la copie de travail du jeu : la branche `gdm-instrumentation` uniquement.

```text
Tu réalises la tâche T15 du projet GODOT_DEV_MAPPER. Applique les règles et le format de rapport du prompt universel de réalisation.
CONTEXTE : docs/benches/{nom}.md ; docs/CONTRACTS.md, sections C-01, C-05 et C-07 ; règles d'appel de C-07.

OBJECTIF
1. Dans la copie de travail ../benches/{nom}, branche gdm-instrumentation :
   - copie le dossier addons/godot_dev_mapper_runtime/ ;
   - instrumente deux types d'ennemis : register, enter et exit de la fonction de décision, decision sur la condition attaquer ou poursuivre ;
   - ajoute une scène de test qui retire un ennemi de l'arbre puis l'y remet.
2. benches/{nom}/flow.json : graphe déclaré de 6 à 12 éléments, conforme au schéma, avec des ancrages vers les fichiers et les lignes du jeu.
3. tools/check_probe_keys.py : relève les clés de sonde utilisées dans le code instrumenté et vérifie qu'elles existent toutes dans flow.json. Code 1 sinon.
4. tests/integration/run_bench.sh : lance le banc de test et le jeu instrumenté, puis vérifie les clés reçues, deux instances distinctes, et aucune destruction après réinsertion.
5. tools/ci/checks.d/55-bench.sh : exécute run_bench.sh si la copie de travail du banc d'essai est présente. Il affiche « CHECK bench OK », « CHECK bench KO », ou « CHECK bench IGNORÉ (copie absente) » : jamais un faux OK.

CONTRÔLES
T15-a  python3 tools/validate_fixtures.py --file benches/{nom}/flow.json ; echo $?   → 0
T15-b  python3 tools/check_probe_keys.py --bench ../benches/{nom} --graph benches/{nom}/flow.json ; echo $?   → 0
T15-c  godot --headless --path ../benches/{nom} --quit-after 600 2>&1 | grep -cE "^(ERROR|SCRIPT ERROR)"   → 0 (jeu sans débogueur, FlowTrace inerte)
T15-d  tests/integration/run_bench.sh ; echo $?   → 0
CONTRE-ÉPREUVES (CE)
- faute de frappe dans une clé de sonde du jeu → T15-b échoue ;
- envoyer une destruction à la sortie de l'arbre → T15-d échoue.
Note le temps passé par point instrumenté : la mesure de valeur (T19) s'en sert.
```
