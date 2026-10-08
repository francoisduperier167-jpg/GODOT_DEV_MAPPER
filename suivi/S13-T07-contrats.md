# S13 — T07 Contrats C-01, C-02, C-05

> Fiche d'exécution du mode autonome. Coche chaque case dès qu'elle est faite et prouvée, puis commite et pousse : une autre IA doit pouvoir reprendre à la première case non cochée. Règles : `docs/construction/sequence.md`. Avancement global : `SUIVI.md`.

| Champ | Valeur |
| --- | --- |
| Réalise | Concepteur |
| Vérifie | Vérificateur (jamais l'auteur) |
| Commence après | S09, S11 (cochées dans `SUIVI.md`) |
| Indépendante de | S10, S12 |
| Branche | `tache/S13-T07-contrats` |
| Fiche de conception | `docs/construction/etape-3.md`, section T07 |
| Estimation | 2 créneaux |

**Séquentiel ou indépendant.** Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité elle-même peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Remplir dans `docs/CONTRACTS.md` les sept rubriques de C-01 (identités, cycle de vie, clés de sonde), C-02 (ancrage, révision, lien périmé) et C-05 (modèle minimal, `.flow.json` v1), avec leurs codes d'erreur.
- Écrire le schéma `contracts/schemas/declared_graph.v1.schema.json`, les fixtures valides et invalides, `tools/validate_fixtures.py`, `tools/check_contracts.py`, les deux tests de contrat avec leurs marqueurs T10, et les contrôles `checks.d/30-contracts.sh` et `31-fixtures.sh`.

## Fichiers autorisés

- `docs/CONTRACTS.md`, sections C-01, C-02 et C-05 ;
- `contracts/schemas/declared_graph.v1.schema.json` ;
- `tests/contract/fixtures/declared_graph/` ;
- `tests/contract/test_c01_identities.gd`, `tests/contract/test_c05_declared_graph.gd` ;
- les marqueurs T10 de `tests/pending/`, `tools/validate_fixtures.py`, `tools/check_contracts.py` ;
- `tools/ci/checks.d/30-contracts.sh`, `tools/ci/checks.d/31-fixtures.sh`.

Toujours autorisés en plus : `rapports/S13*.md` et les cases de cette fiche.

## Prompt de réalisation

```text
Tu es <ton nom d'IA>, au rôle Concepteur. Tu réalises l'unité S13 « T07 Contrats C-01, C-02, C-05 » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.

AVANT TOUT
1. git fetch origin. Lis REGLES_AGENTS.md s'il existe, puis la fiche suivi/S13-T07-contrats.md.
2. Si la branche origin/tache/S13-T07-contrats existe : reprends-la, relis rapports/S13.md et commence à la première sous-étape R non cochée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
3. Sinon : vérifie dans SUIVI.md, sur main, que S09, S11 sont cochées, puis crée tache/S13-T07-contrats depuis main.

GODOT
- Si tools/ci/fetch_godot.sh existe : B=$(tools/ci/fetch_godot.sh 4.7.2-stable)
- Sinon, hors du dépôt :
  D=$HOME/.cache/gdm-godot/4.7.2-stable ; mkdir -p "$D"
  test -x "$D/Godot_v4.7.2-stable_linux.x86_64" || { curl -sSL -o /tmp/godot-4.7.2.zip https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip && unzip -o -q /tmp/godot-4.7.2.zip -d "$D"; }
  B=$D/Godot_v4.7.2-stable_linux.x86_64
- « godot » dans les commandes désigne "$B". Contrôle : "$B" --version contient 4.7.2.stable.
- Éditeur avec rendu, quand la fiche le demande : xvfb-run -a -s "-screen 0 1600x900x24" "$B" --editor --path <projet> --rendering-driver opengl3

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S13.md et les cases de suivi/S13-T07-contrats.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu coches une case seulement quand elle est faite et prouvée. Tu commites et tu pousses après chaque case cochée.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (docs/construction/etape-3.md, T07)
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
TRAVAIL TECHNIQUE — fin de la copie exacte du guide

ADAPTATIONS DU MODE AUTONOME
- Aucune : suis le travail technique tel quel.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche, et coche chacune.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Coche dans suivi/S13-T07-contrats.md les sous-étapes faites et prouvées ; complète rapports/S13.md (sorties, section « Passation ») ; commite ; git push origin tache/S13-T07-contrats.
- Ne laisse aucune modification non poussée.

FORMAT DE rapports/S13.md
- Statut : EN COURS | TERMINÉ | QUESTION | ESCALADE
- Auteur : <ton nom d'IA> · Tentative : n · Créneaux utilisés : n
- Fichiers modifiés : liste
- Contrôles : pour chacun, commande, code de sortie, 10 dernières lignes de sortie
- Contre-épreuves faites : liste
- Écarts au contrat, au guide ou à la fiche : aucun, ou liste
- Hypothèses : aucune, ou liste
- Questions : aucune, ou liste
- Pour la recette : ce qu'un humain devra vérifier, ou « rien »
- Passation : cinq lignes au plus
```

## Sous-étapes de réalisation

- [ ] R0 Prise en charge : `git fetch origin` ; S09, S11 sont cochées dans `SUIVI.md` ; branche `origin/tache/S13-T07-contrats` absente, ou sans commit depuis deux créneaux, ou dernier verdict REFUSÉE ; créer ou reprendre la branche ; `rapports/S13.md` avec « Statut : EN COURS » et « Auteur » ; commit ; push.
- [ ] R1 Lire le plan §5 et §10, `docs/spikes/SPIKE-02.md`, `docs/DECISIONS.md`.
- [ ] R2 Rédiger C-01 dans `docs/CONTRACTS.md` (sept rubriques, codes d'erreur).
- [ ] R3 Rédiger C-02.
- [ ] R4 Rédiger C-05.
- [ ] R5 Écrire le schéma JSON du graphe déclaré.
- [ ] R6 Écrire les fixtures `valid_*` et `invalid_<CODE>__*` (au moins les cinq invalides de la fiche).
- [ ] R7 Écrire `tools/validate_fixtures.py` (deux niveaux, `--plan-examples`, `--kinds`, `--file`).
- [ ] R8 Écrire `tools/check_contracts.py`.
- [ ] R9 Écrire les deux tests de contrat et leurs marqueurs `tests/pending/` (« T10 »).
- [ ] R10 Écrire `tools/ci/checks.d/30-contracts.sh` et `31-fixtures.sh`.
- [ ] R11 Lister en tête du rapport tout écart avec le plan, sans le trancher.
- [ ] R12 Contrôles finaux : T07-a, T07-b, T07-c, T07-d, T07-d2, T07-e, T07-f, T07-g exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » ; commit ; push.

## Prompt de vérification

```text
Tu es <ton nom d'IA>, au rôle Vérificateur, vérificateur indépendant de l'unité S13 « T07 Contrats C-01, C-02, C-05 » du projet GODOT_DEV_MAPPER.
Tu n'en es pas l'auteur : lis la ligne « Auteur » de rapports/S13.md ; si c'est toi, arrête-toi.
Tu ne modifies aucun fichier de l'unité. Tu écris ton verdict et tu coches les sous-étapes V, sur la branche.

COPIE NEUVE : git fetch origin && git worktree add --detach ../verif-S13-T07-contrats origin/tache/S13-T07-contrats
GODOT : même procédure que le prompt de réalisation.

1. PÉRIMÈTRE. git diff --name-only origin/main...origin/tache/S13-T07-contrats. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S13*.md et suivi/S13-T07-contrats.md. Tout autre fichier : refus.
2. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : T07-a, T07-b, T07-c, T07-d, T07-d2, T07-e, T07-f, T07-g.
3. CONTRE-ÉPREUVES. Applique chaque sabotage marqué (CE) dans la fiche et dans le travail technique ; vérifie que le contrôle échoue ; annule avec git checkout -- . && git clean -fd.
4. CONTOURNEMENTS. Cherche :
   - test sans assertion, ou toujours vrai ;
   - test désactivé, renommé ou sorti du runner ;
   - valeur attendue recopiée depuis la sortie du code ;
   - marqueur supprimé de tests/pending/ sans test qui passe ;
   - fixture invalide rejetée pour un autre motif que celui de son nom ;
   - API Godot inventée ou non vérifiée ;
   - dépendance interdite entre modules ; API sensible hors de la frontière de compatibilité ;
   - affirmation du rapport sans sortie qui la prouve.
5. COHÉRENCE. Plan §5 et §10 ; SPIKE-02 ; règle « un exemple invalide et un test par règle du contrat ».

VERDICT dans rapports/S13-verif-<tentative>.md :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte
Pousse le verdict sur la branche. Si ACCEPTÉE, fais les sous-étapes F de la fiche. Si REFUSÉE, arrête-toi : une IA au rôle de l'auteur reprendra.
```

## Sous-étapes de vérification

- [ ] V1 Prise en charge : pas l'auteur ; copie neuve `../verif-S13-T07-contrats` sur `origin/tache/S13-T07-contrats`.
- [ ] V2 Périmètre : `git diff --name-only origin/main...origin/tache/S13-T07-contrats` ⊂ fichiers autorisés.
- [ ] V3.1 Contrôle T07-a relancé, résultat conforme.
- [ ] V3.2 Contrôle T07-b relancé, résultat conforme.
- [ ] V3.3 Contrôle T07-c relancé, résultat conforme.
- [ ] V3.4 Contrôle T07-d relancé, résultat conforme.
- [ ] V3.5 Contrôle T07-d2 relancé, résultat conforme.
- [ ] V3.6 Contrôle T07-e relancé, résultat conforme.
- [ ] V3.7 Contrôle T07-f relancé, résultat conforme.
- [ ] V3.8 Contrôle T07-g relancé, résultat conforme.
- [ ] V4 Contre-épreuves (CE) appliquées et détectées, puis annulées.
- [ ] V5 Contournements cherchés.
- [ ] V6 Cohérence avec les contrats et les invariants.
- [ ] V7 Verdict écrit dans `rapports/S13-verif-<tentative>.md` et poussé.

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

- [ ] F1 `git switch main && git pull --ff-only && git merge --no-ff origin/tache/S13-T07-contrats -m "Fusion S13 : T07 Contrats C-01, C-02, C-05"`.
- [ ] F2 Sur `main` : `GODOT="$B" tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK. Sinon : `git reset --hard ORIG_HEAD`, verdict « REFUSÉE (fusion) » poussé sur la branche, et arrêt de la fusion.
- [ ] F3 Dans `SUIVI.md`, cocher la ligne **S13** et compléter « fait le <date> · auteur <IA> · vérifié par <IA> · <n> créneaux ».
- [ ] F4 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette.
- [ ] F5 Cocher les sous-étapes F de cette fiche ; `git commit` ; `git push origin main` (en cas de refus : `git pull --rebase`, puis push).

## Pour la recette

Rien de propre à cette unité.
