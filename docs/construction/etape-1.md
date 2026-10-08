# Étape 1 — Fondations

Tâches : file A : T01, puis T02, puis T03 · file B : T04 · Budget : 4 à 6 h humaines · Prérequis : étape 0 acceptée

## Objectif

Obtenir un dépôt où tout ce qui suivra se vérifie en une commande :
- le plugin se charge dans l'éditeur ;
- les tests tournent sans interface, avec un code de sortie fiable ;
- les règles de dépendance et le style sont contrôlés ;
- la CI rejoue tout sur 4.7.2 et sur la préversion.

En parallèle, le jeu de test est choisi et s'ouvre sur 4.7.2.

## Obligations

- Aucune fonctionnalité : squelette, outillage et CI seulement.
- `plugin.gd` est le seul script qui hérite d'EditorPlugin, et il ne fait que déléguer.
- Le dossier `addons/godot_dev_mapper_runtime/` ne référence jamais `addons/godot_dev_mapper/` (INV-06).
- Les versions de Godot ne sont écrites qu'à un endroit : `addons/godot_dev_mapper/compat/versions.json`.
- Chaque contrôle ajouté a sa contre-épreuve.
- Chaque tâche travaille dans sa propre copie de travail, et ne touche à aucun fichier partagé (guide, section « Copies de travail et fichiers partagés »).
- Aucun fichier du jeu de test n'entre dans le dépôt : on le référence par dépôt et révision.

## Méthodologie

- **File A, strictement séquentielle.** T01 crée le projet. T02 ajoute le runner et le contrôle de dépendances. T03 assemble tous les contrôles dans `tools/ci/run_all_checks.sh` et dans la CI. À la fin, une commande rejoue tout.
- **File B.** T04, toi et Gemini.
- **Modèles.** Qwen réalise, ou Sonnet si T00 a échoué. Gemini vérifie, sauf T03 que vérifie Opus (CI et versions).
- **Test d'abord.** Chaque tâche écrit sa contre-épreuve avant le code : on la voit échouer d'abord.

## Points de contrôle de l'étape

| ID | Contrôle | Commande | Attendu |
| --- | --- | --- | --- |
| PC1.1 | Import | `godot --headless --path . --import` | Code 0 |
| PC1.2 | Chargement du plugin | `GDM_TRACE_LIFECYCLE=1 godot --headless --editor --path . --quit-after 300 > /tmp/ed.out 2>&1`, puis compter `GDM_PLUGIN_ENTER`, `GDM_PLUGIN_EXIT` et les lignes `^(ERROR\|SCRIPT ERROR)` | 1, 1, 0 |
| PC1.3 | Tests | `godot --headless --path . -s res://tests/run_all.gd` | Code 0 et ligne `GDM_TESTS … failed=0` |
| PC1.4 | (CE) Échec détecté | Même commande avec `GDM_SELFTEST_FAIL=1` | Code non nul |
| PC1.5 | Dépendances | `python3 tools/check_deps.py`, puis le même script sur `tools/check_deps_fixtures` | Code 0, puis code 1 |
| PC1.6 | Style | `gdlint addons tests` et `gdformat --check addons tests` | Codes 0 |
| PC1.7 | Tout en une commande | `GODOT=<binaire> tools/ci/run_all_checks.sh` | Code 0 et `ALL_CHECKS OK` |
| PC1.8 | CI distante | Dernier passage sur GitHub après envoi | Job stable vert ; job préversion exécuté |
| PC1.9 | Banc d'essai | `python3 tools/check_benches.py`, puis import de la copie de travail sur 4.7.2 | Code 0 ; aucune ligne d'erreur nouvelle |
| PC1.10 | (CE) Contrôles ajoutés | Déposer dans `tools/ci/checks.d/` un script qui sort en 1, relancer PC1.7 | Code 1, puis 0 une fois le script retiré |

PC1.8 attend l'envoi sur GitHub. Tant que ta machine est indisponible, PC1.7 en est l'équivalent local.

## Cheminement d'amélioration

- **Durée.** `run_all_checks.sh` doit tenir en moins de 3 minutes en local. Au-delà, on met en cache l'import et le binaire.
- **Lint.** Si `gdlint` impose une règle gênante, on la désactive une à une dans `gdlintrc`, chacune avec une raison écrite ; jamais en bloc.
- **Bruit du moteur.** Si l'éditeur sans interface affiche des lignes `ERROR` étrangères au plugin (pilotes, moteur), on les liste dans `tools/ci/known_engine_errors.txt`, avec la date et la version. On revoit cette liste à chaque version de Godot.
- **Banc d'essai introuvable.** Si T04 ne trouve aucun jeu avec deux ennemis qui décident, on élargit aux démos officielles de Godot. Créer un mini-jeu de test est le dernier recours (2 à 3 h).

## T01 — Squelette du dépôt et plugin activable

Qwen · A1 · file A · dépend de T00 et de l'étape 0 · vérification : Gemini · contexte : plan §4 (modules, arborescence)

Fichiers autorisés :
- `project.godot`, `.gitignore` ;
- `addons/godot_dev_mapper/plugin.cfg` et `plugin.gd` ;
- un `README.md` par module : core, protocol, store, projections, ui, editor, persistence, acquisition, compat ;
- `addons/godot_dev_mapper_runtime/README.md`.

```text
Tu réalises la tâche T01 du projet GODOT_DEV_MAPPER (plugin Godot 4.7.2, GDScript). Applique les règles et le format de rapport du prompt universel de réalisation (REGLES_AGENTS.md).

OBJECTIF
Créer le projet Godot de développement et un plugin éditeur qui se charge et se décharge sans erreur, sans aucune fonctionnalité.

À CRÉER
- project.godot : config_version=5 ; nom « GODOT_DEV_MAPPER (dev) » ; section [editor_plugins] qui active res://addons/godot_dev_mapper/plugin.cfg.
- addons/godot_dev_mapper/plugin.cfg : nom « Godot Dev Mapper », version 0.0.1, script plugin.gd.
- addons/godot_dev_mapper/plugin.gd : @tool, extends EditorPlugin. Seulement si la variable d'environnement GDM_TRACE_LIFECYCLE vaut « 1 » : afficher GDM_PLUGIN_ENTER dans _enter_tree et GDM_PLUGIN_EXIT dans _exit_tree. Rien d'autre.
- Un README.md d'une ligne qui décrit le rôle du module, dans chaque dossier : core, protocol, store, projections, ui, editor, persistence, acquisition, compat (sous addons/godot_dev_mapper/), et dans addons/godot_dev_mapper_runtime/.
- .gitignore : .godot/, .godot-bin/, *.out, sandbox/ (compléter le fichier existant). .godot-bin/ recevra les binaires de Godot téléchargés par T03.

CONTRÔLES (exécute-les tous et colle les sorties)
T01-a  godot --headless --path . --import ; echo $?                                → 0
T01-b  GDM_TRACE_LIFECYCLE=1 godot --headless --editor --path . --quit-after 300 > /tmp/ed.out 2>&1
       grep -c GDM_PLUGIN_ENTER /tmp/ed.out ; grep -c GDM_PLUGIN_EXIT /tmp/ed.out
       grep -cE "^(ERROR|SCRIPT ERROR)" /tmp/ed.out                                → 1, 1, 0
T01-c  grep -rl "extends EditorPlugin" addons | wc -l                              → 1
T01-d  grep -rn "godot_dev_mapper/" addons/godot_dev_mapper_runtime                → aucune ligne
T01-e  godot --headless --editor --path . --quit-after 300 2>&1 | grep -c "GDM_"   → 0 (sans la variable)
Attention : l'éditeur sans interface sort avec le code 0 même si plugin.gd ne compile pas. Seul le comptage des lignes d'erreur fait foi.

CONTRE-ÉPREUVE (CE), à exécuter puis annuler
Ajoute print(undefined_var) dans _enter_tree et relance T01-b : au moins une ligne SCRIPT ERROR doit apparaître. Annule, puis relance T01-b.
```

Sabotage pour le vérificateur : `print(undefined_var)` dans `_enter_tree` ; T01-b doit compter au moins une erreur.

## T02 — Runner de tests et contrôle de dépendances

Qwen · A1 · file A · dépend de T01 · vérification : Gemini · contexte : plan §4 (table des modules, API sensibles), méthodologie §3

Fichiers autorisés :
- `tests/run_all.gd`, `tests/gdm_test.gd`, `tests/pending/README.md`, `tests/README.md` ;
- `tests/unit/test_smoke.gd`, `tests/unit/test_selftest.gd` ;
- `tools/check_deps.py`, `tools/deps_rules.json`, `tools/check_deps_fixtures/`.

```text
Tu réalises la tâche T02 du projet GODOT_DEV_MAPPER. Applique les règles et le format de rapport du prompt universel de réalisation.

OBJECTIF
Un runner de tests sans interface dont le code de sortie est fiable, et un contrôle automatique des dépendances entre modules.

RUNNER
- tests/gdm_test.gd : classe de base (extends RefCounted) avec assert_true(cond, msg), assert_eq(attendu, obtenu, msg) et fail(msg). Elle compte les assertions et les échecs de chaque test.
- tests/run_all.gd : extends SceneTree. Il trouve récursivement les fichiers res://tests/**/test_*.gd et ignore ceux qui ont un marqueur dans tests/pending/ (un fichier <nom du test>.pending qui contient l'identifiant de la tâche) et les compte comme « pending ». Il exécute chaque méthode dont le nom commence par test_. Un test sans aucune assertion compte comme échoué. Il affiche PASS ou FAIL suivi de chemin::méthode, puis la ligne finale « GDM_TESTS passed=N failed=M pending=K ». Il quitte avec le code 0 si M = 0, et 1 sinon.
- tests/unit/test_smoke.gd : un test trivial, avec une assertion.
- tests/unit/test_selftest.gd : si GDM_SELFTEST_FAIL vaut « 1 », un test échoue ; si GDM_SELFTEST_NOASSERT vaut « 1 », un test ne fait aucune assertion ; sinon, les deux passent.
- tests/pending/README.md : la convention des marqueurs ; aucun marqueur pour l'instant.
Une erreur d'exécution GDScript ne remonte pas toujours au runner. T03 fera donc échouer la vérification à toute ligne « SCRIPT ERROR » dans la sortie du runner. Dis-le dans tests/README.md.

CONTRÔLE DE DÉPENDANCES
- tools/deps_rules.json : pour chaque module (dossiers sous addons/godot_dev_mapper/, plus « runtime » pour addons/godot_dev_mapper_runtime/), la liste des modules dont il peut dépendre (plan §4) ; la liste des API sensibles (docs/ARCHITECTURE.md) ; les fichiers où ces API sont permises : compat/, plugin.gd, addons/godot_dev_mapper_runtime/runtime_facade.gd.
- tools/check_deps.py (Python 3, bibliothèque standard seulement, option --root, par défaut la racine du dépôt) détecte :
  1. les preload ou load de « res://addons/godot_dev_mapper/<module>/ » interdits par les règles ;
  2. l'usage, dans un autre module, d'un class_name déclaré par un module interdit (lignes de commentaire ignorées) ;
  3. une API sensible hors des fichiers permis ;
  4. toute référence du dossier runtime à « res://addons/godot_dev_mapper/ ».
  Une ligne par violation, au format « fichier:ligne règle détail ». Code 1 s'il y en a au moins une.
- tools/check_deps_fixtures/ : une fausse arborescence qui contient exactement trois violations, une de chaque sorte parmi 1, 3 et 4.

CONTRÔLES
T02-a  godot --headless --path . -s res://tests/run_all.gd ; echo $?        → 0, ligne GDM_TESTS passed=3 failed=0 pending=0
T02-b  (CE) GDM_SELFTEST_FAIL=1 godot --headless --path . -s res://tests/run_all.gd ; echo $?   → 1, failed=1
T02-c  (CE) GDM_SELFTEST_NOASSERT=1 godot --headless --path . -s res://tests/run_all.gd ; echo $?   → 1, failed=1
T02-d  python3 tools/check_deps.py ; echo $?                                 → 0
T02-e  (CE) python3 tools/check_deps.py --root tools/check_deps_fixtures ; echo $?   → 1, trois lignes de violation
T02-f  godot --headless --path . --check-only -s res://tests/run_all.gd ; echo $?   → 0
T02-g  (CE) ajoute temporairement un test test_pending_demo.gd en échec et son marqueur tests/pending/test_pending_demo.gd.pending : T02-a reste à 0 avec pending=1 ; supprime le marqueur : code 1 ; puis supprime les deux fichiers.
```

## T03 — Contrôle unique, lint et CI

Qwen · A1 · file A · dépend de T01 et T02 · vérification : Opus · contexte : plan §4 (frontière de compatibilité), `docs/COMPATIBILITY.md`

Fichiers autorisés :
- `addons/godot_dev_mapper/compat/versions.json` ;
- `tools/ci/fetch_godot.sh`, `tools/ci/run_all_checks.sh`, `tools/ci/known_engine_errors.txt` ;
- `tools/ci/checks.d/README.md` ;
- `.github/workflows/ci.yml`, `requirements-dev.txt`, `gdlintrc` (seulement si nécessaire).

```text
Tu réalises la tâche T03 du projet GODOT_DEV_MAPPER. Applique les règles et le format de rapport du prompt universel de réalisation.

OBJECTIF
Une seule commande rejoue tous les contrôles ; la CI l'exécute sur 4.7.2 de façon bloquante, et sur la préversion sans bloquer.

À CRÉER
- addons/godot_dev_mapper/compat/versions.json : {"stable": "4.7.2-stable", "preview": "4.8-dev7"}. C'est la seule source des numéros de version.
- requirements-dev.txt : gdtoolkit==4.5.0 et jsonschema, version figée.
- tools/ci/fetch_godot.sh <version> : télécharge https://github.com/godotengine/godot-builds/releases/download/<version>/Godot_v<version>_linux.x86_64.zip. Cette adresse est vérifiée pour 4.7.2-stable et 4.8-dev7. Le script décompresse dans .godot-bin/<version>/, réutilise le binaire s'il est déjà présent, affiche son chemin et quitte avec un code non nul en cas d'échec. Si une empreinte SHA-512 est publiée avec la version, il la vérifie.
- tools/ci/run_all_checks.sh : exige la variable GODOT. Il exécute dans l'ordre :
  1. import ;
  2. chargement du plugin (comptages de PC1.2, en ignorant les lignes listées dans tools/ci/known_engine_errors.txt) ;
  3. runner (code 0, et aucune ligne SCRIPT ERROR dans sa sortie) ;
  4. check_deps ;
  5. gdlint addons tests ;
  6. gdformat --check addons tests ;
  7. chaque script de tools/ci/checks.d/, dans l'ordre de leur nom.
  Chaque étape affiche « CHECK <nom> OK » ou « CHECK <nom> KO ». À la fin : « ALL_CHECKS OK » et code 0, ou code 1. Après T03, on ajoute un contrôle en déposant un script dans checks.d/, jamais en modifiant run_all_checks.sh.
- tools/ci/checks.d/README.md : la convention de nommage NN-nom.sh et le format de sortie CHECK.
- .github/workflows/ci.yml : déclenché par push et pull_request ; deux jobs sur ubuntu-latest. Job « stable » : bloquant. Job « preview » : continue-on-error: true. Étapes : checkout, Python, pip install -r requirements-dev.txt, version lue dans versions.json, fetch_godot.sh, run_all_checks.sh.
- tools/ci/known_engine_errors.txt : vide, avec un commentaire qui explique son usage.

CONTRÔLES
T03-a  B=$(tools/ci/fetch_godot.sh 4.7.2-stable) && "$B" --version        → contient 4.7.2.stable
T03-b  GODOT="$B" tools/ci/run_all_checks.sh ; echo $?                       → 0 et ALL_CHECKS OK
T03-c  (CE) GDM_SELFTEST_FAIL=1 GODOT="$B" tools/ci/run_all_checks.sh ; echo $?   → 1 et CHECK tests KO
T03-d  (CE) ajoute une ligne de plus de 100 caractères dans test_smoke.gd : CHECK lint KO ; annule
T03-e  (CE) ajoute print(undefined_var) dans plugin.gd : CHECK plugin KO ; annule
T03-f  P=$(tools/ci/fetch_godot.sh 4.8-dev7) && GODOT="$P" tools/ci/run_all_checks.sh ; echo $?   → résultat consigné, sans exigence
T03-g  grep -c "continue-on-error: true" .github/workflows/ci.yml          → 1
T03-h  grep -rn "4\.7\.2\|4\.8-dev" --include=*.sh --include=*.yml --include=*.gd . | grep -v versions.json   → aucune ligne
T03-i  (CE) dépose tools/ci/checks.d/99-demo.sh, qui affiche « CHECK demo KO » et sort en 1 : run_all_checks.sh → 1 ; supprime-le
```

L'envoi sur GitHub et PC1.8 viendront quand le dépôt sera poussé.

## T04 — Banc d'essai

Toi et Gemini · A0, puis A1 pour la migration · file B · vérification : toi · contexte : plan §0 et §9, `docs/DECISIONS.md` (D-02)

Fichiers autorisés : `benches/benches.json`, `docs/benches/<nom>.md`, `tools/check_benches.py`. La copie de travail du jeu vit hors du dépôt, par exemple dans `../benches/<nom>`.

Prompt de sélection, pour Gemini :

```text
Tu aides à choisir le banc d'essai du projet GODOT_DEV_MAPPER. Tu ne copies aucun fichier de jeu dans le dépôt.
Critères, tous requis :
- jeu Godot 4.x en GDScript ;
- au moins deux types d'ennemis ou d'agents qui prennent une décision observable : attaquer ou poursuivre, fuir, patrouiller ;
- licence du code qui permet une copie de travail locale modifiée ;
- licence des assets connue ;
- entre 30 et 500 scripts .gd.
Pour trois candidats au plus, donne : nom, dépôt, révision, licences du code et des assets (avec le fichier qui le dit), version de Godot d'origine, nombre de scripts .gd, scripts qui contiennent les décisions ciblées, risques de migration vers 4.7.2.
Vérifie chaque fait dans le dépôt lui-même (fichier LICENSE, project.godot). Écris « non vérifié » quand tu n'as pas pu vérifier.
Rapport : un tableau comparatif, puis ta recommandation et ses deux principales faiblesses.
```

Tu choisis. Ensuite, prompt de préparation pour Qwen ou Sonnet :

```text
Tu prépares le banc d'essai retenu pour le projet GODOT_DEV_MAPPER : {nom}, dépôt {url}, révision {sha}.
1. Clone-le hors du dépôt, dans ../benches/{nom}, puis crée la branche gdm-base.
2. Importe-le avec Godot 4.7.2 : godot --headless --path ../benches/{nom} --import > /tmp/bench.out 2>&1
   Corrige seulement ce que la migration exige. Chaque correction fait un commit séparé, avec la raison dans le message.
3. Écris benches/benches.json : nom, dépôt, révision d'origine, révision migrée, licences du code et des assets, version de Godot d'origine, scripts des décisions ciblées.
4. Écris tools/check_benches.py : il vérifie que benches.json est un JSON valide avec ces clés, et qu'aucun fichier .gd ni aucun asset du jeu n'est suivi par Git dans ce dépôt.
5. Écris docs/benches/{nom}.md : la fiche du jeu, les décisions observables, les corrections de migration.
CONTRÔLES
T04-a  python3 tools/check_benches.py ; echo $?                                          → 0
T04-b  grep -cE "^(ERROR|SCRIPT ERROR)" /tmp/bench.out après la migration                 → 0, ou erreurs listées et justifiées dans la fiche
T04-c  (CE) copie temporairement un .gd du jeu dans benches/ et ajoute-le à Git : T04-a → 1 ; annule
```
