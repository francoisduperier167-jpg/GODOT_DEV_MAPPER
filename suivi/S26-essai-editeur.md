# S26 — Essai dans l'éditeur sous écran virtuel (PC5.6)

> Fiche d'exécution du mode autonome. Coche chaque case dès qu'elle est faite et prouvée, puis commite et pousse : une autre IA doit pouvoir reprendre à la première case non cochée. Règles : `docs/construction/sequence.md`. Avancement global : `SUIVI.md`.

| Champ | Valeur |
| --- | --- |
| Réalise | Développeur |
| Vérifie | Concepteur (jamais l'auteur) |
| Commence après | S24, S25 (cochées dans `SUIVI.md`) |
| Indépendante de | S22, S23, S28, S29, S30, S31, S33 |
| Branche | `tache/S26-essai-editeur` |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité elle-même peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Lancer, sous écran virtuel, l'éditeur avec le plugin sur une copie temporaire du banc instrumenté, jouer une session complète jusqu'à l'Event Store, et comparer les compteurs à ceux du banc sans éditeur.
- Enregistrer la session réelle comme fixture de régression (hors des fixtures de contrat).

## Fichiers autorisés

`tests/integration/run_editor_session.sh`, `tools/harness/editor_driver/`, `tests/fixtures/sessions_reelles/`, `tools/ci/checks.d/57-editor.sh`, `docs/benches/<nom>.md` (section « Essai dans l'éditeur »).

Toujours autorisés en plus : `rapports/S26*.md` et les cases de cette fiche.

## Contrôles propres à cette fiche

- `S26-a` : `tests/integration/run_editor_session.sh; echo $?` → 0
- `S26-b` : `GODOT="$B" tools/ci/run_all_checks.sh; echo $?` → 0, CHECK editor OK ou IGNORÉ
- (CE) Faire ignorer les lots par `debugger_bridge.gd` : S26-a échoue ; annuler.

## Prompt de réalisation

```text
Tu es <ton nom d'IA>, au rôle Développeur. Tu réalises l'unité S26 « Essai dans l'éditeur sous écran virtuel (PC5.6) » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.

AVANT TOUT
1. git fetch origin. Lis REGLES_AGENTS.md s'il existe, puis la fiche suivi/S26-essai-editeur.md.
2. Si la branche origin/tache/S26-essai-editeur existe : reprends-la, relis rapports/S26.md et commence à la première sous-étape R non cochée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
3. Sinon : vérifie dans SUIVI.md, sur main, que S24, S25 sont cochées, puis crée tache/S26-essai-editeur depuis main.

GODOT
- Si tools/ci/fetch_godot.sh existe : B=$(tools/ci/fetch_godot.sh 4.7.2-stable)
- Sinon, hors du dépôt :
  D=$HOME/.cache/gdm-godot/4.7.2-stable ; mkdir -p "$D"
  test -x "$D/Godot_v4.7.2-stable_linux.x86_64" || { curl -sSL -o /tmp/godot-4.7.2.zip https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip && unzip -o -q /tmp/godot-4.7.2.zip -d "$D"; }
  B=$D/Godot_v4.7.2-stable_linux.x86_64
- « godot » dans les commandes désigne "$B". Contrôle : "$B" --version contient 4.7.2.stable.
- Éditeur avec rendu, quand la fiche le demande : xvfb-run -a -s "-screen 0 1600x900x24" "$B" --editor --path <projet> --rendering-driver opengl3

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S26.md et les cases de suivi/S26-essai-editeur.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu coches une case seulement quand elle est faite et prouvée. Tu commites et tu pousses après chaque case cochée.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (rédigé pour le mode autonome)
Tu réalises l'essai PC5.6 du projet GODOT_DEV_MAPPER, sans humain : une session du banc d'essai jusqu'au store de l'éditeur réel, sous écran virtuel.
CONTEXTE : docs/construction/etape-5.md (T14, PC5.6), rapport de S24 (procédure), docs/benches/<nom>.md, branche banc/<nom>-instrumentation.
OBJECTIF
1. tools/harness/editor_driver/ : plugin de pilotage, chargé avec le plugin du projet. Il lance la scène principale, attend la fin de la session, l'arrête, puis écrit dans un fichier les compteurs lus par l'API publique du contrôleur de session (C-06) : événements, trous, instances, fin.
2. tests/integration/run_editor_session.sh : prépare une copie temporaire du banc instrumenté, y ajoute addons/godot_dev_mapper/ et le pilote, lance l'éditeur sous xvfb-run, puis compare ces compteurs à ceux de tests/integration/run_bench.sh. Code 0 si les clés et les instances concordent et qu'aucune ligne ERROR n'apparaît.
3. La session reçue est enregistrée dans tests/fixtures/sessions_reelles/ ; elle ne remplace aucune fixture de contrat.
4. tools/ci/checks.d/57-editor.sh : « CHECK editor OK », « KO », ou « IGNORÉ (xvfb-run absent) ».
CONTRÔLES
S26-a  tests/integration/run_editor_session.sh ; echo $?   → 0
S26-b  GODOT="$B" tools/ci/run_all_checks.sh ; echo $?   → 0, CHECK editor OK ou IGNORÉ
CONTRE-ÉPREUVE (CE) pour le vérificateur : faire ignorer les lots par la passerelle → S26-a échoue.
TRAVAIL TECHNIQUE — fin de la copie exacte du guide

CONTRÔLES DE LA FICHE
S26-a  tests/integration/run_editor_session.sh; echo $?   → 0
S26-b  GODOT="$B" tools/ci/run_all_checks.sh; echo $?   → 0, CHECK editor OK ou IGNORÉ
(CE) Faire ignorer les lots par `debugger_bridge.gd` : S26-a échoue ; annuler.

ADAPTATIONS DU MODE AUTONOME
- Aucune : suis le travail technique tel quel.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche, et coche chacune.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Coche dans suivi/S26-essai-editeur.md les sous-étapes faites et prouvées ; complète rapports/S26.md (sorties, section « Passation ») ; commite ; git push origin tache/S26-essai-editeur.
- Ne laisse aucune modification non poussée.

FORMAT DE rapports/S26.md
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

- [ ] R0 Prise en charge : `git fetch origin` ; S24, S25 sont cochées dans `SUIVI.md` ; branche `origin/tache/S26-essai-editeur` absente, ou sans commit depuis deux créneaux, ou dernier verdict REFUSÉE ; créer ou reprendre la branche ; `rapports/S26.md` avec « Statut : EN COURS » et « Auteur » ; commit ; push.
- [ ] R1 Écrire `tools/harness/editor_driver/` : un plugin de pilotage qui lance la scène principale, attend la session, l'arrête, puis écrit les compteurs du contrôleur de session (C-06) dans un fichier.
- [ ] R2 Écrire `tests/integration/run_editor_session.sh` : copie temporaire de `banc/<nom>-instrumentation`, ajout du plugin et du pilote, éditeur sous xvfb-run, comparaison avec les compteurs de `run_bench.sh`.
- [ ] R3 Enregistrer la session dans `tests/fixtures/sessions_reelles/`.
- [ ] R4 Écrire `tools/ci/checks.d/57-editor.sh` : OK, KO, ou IGNORÉ si xvfb-run est absent, jamais un faux OK.
- [ ] R5 Compléter `docs/benches/<nom>.md`, section « Essai dans l'éditeur ».
- [ ] R6 Contrôles finaux : S26-a, S26-b exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » ; commit ; push.

## Prompt de vérification

```text
Tu es <ton nom d'IA>, au rôle Concepteur, vérificateur indépendant de l'unité S26 « Essai dans l'éditeur sous écran virtuel (PC5.6) » du projet GODOT_DEV_MAPPER.
Tu n'en es pas l'auteur : lis la ligne « Auteur » de rapports/S26.md ; si c'est toi, arrête-toi.
Tu ne modifies aucun fichier de l'unité. Tu écris ton verdict et tu coches les sous-étapes V, sur la branche.

COPIE NEUVE : git fetch origin && git worktree add --detach ../verif-S26-essai-editeur origin/tache/S26-essai-editeur
GODOT : même procédure que le prompt de réalisation.

1. PÉRIMÈTRE. git diff --name-only origin/main...origin/tache/S26-essai-editeur. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S26*.md et suivi/S26-essai-editeur.md. Tout autre fichier : refus.
2. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : S26-a, S26-b.
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
5. COHÉRENCE. Protocole de C-07 côté éditeur ; compteurs cohérents avec le banc sans éditeur.

VERDICT dans rapports/S26-verif-<tentative>.md :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte
Pousse le verdict sur la branche. Si ACCEPTÉE, fais les sous-étapes F de la fiche. Si REFUSÉE, arrête-toi : une IA au rôle de l'auteur reprendra.
```

## Sous-étapes de vérification

- [ ] V1 Prise en charge : pas l'auteur ; copie neuve `../verif-S26-essai-editeur` sur `origin/tache/S26-essai-editeur`.
- [ ] V2 Périmètre : `git diff --name-only origin/main...origin/tache/S26-essai-editeur` ⊂ fichiers autorisés.
- [ ] V3.1 Contrôle S26-a relancé, résultat conforme.
- [ ] V3.2 Contrôle S26-b relancé, résultat conforme.
- [ ] V4 Contre-épreuves (CE) appliquées et détectées, puis annulées.
- [ ] V5 Contournements cherchés.
- [ ] V6 Cohérence avec les contrats et les invariants.
- [ ] V7 Verdict écrit dans `rapports/S26-verif-<tentative>.md` et poussé.

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

- [ ] F1 `git switch main && git pull --ff-only && git merge --no-ff origin/tache/S26-essai-editeur -m "Fusion S26 : Essai dans l'éditeur sous écran virtuel (PC5.6)"`.
- [ ] F2 Sur `main` : `GODOT="$B" tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK. Sinon : `git reset --hard ORIG_HEAD`, verdict « REFUSÉE (fusion) » poussé sur la branche, et arrêt de la fusion.
- [ ] F3 Dans `SUIVI.md`, cocher la ligne **S26** et compléter « fait le <date> · auteur <IA> · vérifié par <IA> · <n> créneaux ».
- [ ] F4 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette.
- [ ] F5 Cocher les sous-étapes F de cette fiche ; `git commit` ; `git push origin main` (en cas de refus : `git pull --rebase`, puis push).

## Pour la recette

- Une session réelle dans ton éditeur, sur ta machine.
