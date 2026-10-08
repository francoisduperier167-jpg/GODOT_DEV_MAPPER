# S21 — T13b Banc sans éditeur et scénarios de coupure

> Fiche d'exécution du mode autonome. Coche chaque case dès qu'elle est faite et prouvée, puis commite et pousse : une autre IA doit pouvoir reprendre à la première case non cochée. Règles : `docs/construction/sequence.md`. Avancement global : `SUIVI.md`.

| Champ | Valeur |
| --- | --- |
| Réalise | Développeur |
| Vérifie | Concepteur (jamais l'auteur) |
| Commence après | S20 (cochées dans `SUIVI.md`) |
| Indépendante de | S17, S18, S24, S28 |
| Branche | `tache/S21-T13b-banc` |
| Fiche de conception | `docs/construction/etape-4.md`, section T13b |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité elle-même peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- `tools/harness/fake_editor.gd` réécrit depuis le récepteur de SPIKE-01a (port configurable, scénarios).
- `tools/harness/demo_game/` : deux instances dont une enregistrée avant le démarrage, une décision.
- `tests/integration/run_session.sh` et `tools/ci/checks.d/40-integration.sh`.

## Fichiers autorisés

`tools/harness/fake_editor.gd`, `tools/harness/demo_game/`, `tests/integration/run_session.sh`, `tools/ci/checks.d/40-integration.sh`.

Toujours autorisés en plus : `rapports/S21*.md` et les cases de cette fiche.

## Prompt de réalisation

```text
Tu es <ton nom d'IA>, au rôle Développeur. Tu réalises l'unité S21 « T13b Banc sans éditeur et scénarios de coupure » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.

AVANT TOUT
1. git fetch origin. Lis REGLES_AGENTS.md s'il existe, puis la fiche suivi/S21-T13b-banc.md.
2. Si la branche origin/tache/S21-T13b-banc existe : reprends-la, relis rapports/S21.md et commence à la première sous-étape R non cochée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
3. Sinon : vérifie dans SUIVI.md, sur main, que S20 est cochée, puis crée tache/S21-T13b-banc depuis main.

GODOT
- Si tools/ci/fetch_godot.sh existe : B=$(tools/ci/fetch_godot.sh 4.7.2-stable)
- Sinon, hors du dépôt :
  D=$HOME/.cache/gdm-godot/4.7.2-stable ; mkdir -p "$D"
  test -x "$D/Godot_v4.7.2-stable_linux.x86_64" || { curl -sSL -o /tmp/godot-4.7.2.zip https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip && unzip -o -q /tmp/godot-4.7.2.zip -d "$D"; }
  B=$D/Godot_v4.7.2-stable_linux.x86_64
- « godot » dans les commandes désigne "$B". Contrôle : "$B" --version contient 4.7.2.stable.
- Éditeur avec rendu, quand la fiche le demande : xvfb-run -a -s "-screen 0 1600x900x24" "$B" --editor --path <projet> --rendering-driver opengl3

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S21.md et les cases de suivi/S21-T13b-banc.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu coches une case seulement quand elle est faite et prouvée. Tu commites et tu pousses après chaque case cochée.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (docs/construction/etape-4.md, T13b)
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
TRAVAIL TECHNIQUE — fin de la copie exacte du guide

ADAPTATIONS DU MODE AUTONOME
- Aucune : suis le travail technique tel quel.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche, et coche chacune.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Coche dans suivi/S21-T13b-banc.md les sous-étapes faites et prouvées ; complète rapports/S21.md (sorties, section « Passation ») ; commite ; git push origin tache/S21-T13b-banc.
- Ne laisse aucune modification non poussée.

FORMAT DE rapports/S21.md
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

- [ ] R0 Prise en charge : `git fetch origin` ; S20 est cochée dans `SUIVI.md` ; branche `origin/tache/S21-T13b-banc` absente, ou sans commit depuis deux créneaux, ou dernier verdict REFUSÉE ; créer ou reprendre la branche ; `rapports/S21.md` avec « Statut : EN COURS » et « Auteur » ; commit ; push.
- [ ] R1 Écrire `tools/harness/fake_editor.gd`.
- [ ] R2 Écrire `tools/harness/demo_game/`.
- [ ] R3 Écrire `tests/integration/run_session.sh` (cinq vérifications).
- [ ] R4 Écrire `tools/ci/checks.d/40-integration.sh`.
- [ ] R5 Si un scénario révèle un défaut de `flow_trace.gd` : ESCALADE avec le diagnostic (la correction revient à S20 rouverte).
- [ ] R6 Contrôles finaux : T13b-a, T13b-b exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » ; commit ; push.

## Prompt de vérification

```text
Tu es <ton nom d'IA>, au rôle Concepteur, vérificateur indépendant de l'unité S21 « T13b Banc sans éditeur et scénarios de coupure » du projet GODOT_DEV_MAPPER.
Tu n'en es pas l'auteur : lis la ligne « Auteur » de rapports/S21.md ; si c'est toi, arrête-toi.
Tu ne modifies aucun fichier de l'unité. Tu écris ton verdict et tu coches les sous-étapes V, sur la branche.

COPIE NEUVE : git fetch origin && git worktree add --detach ../verif-S21-T13b-banc origin/tache/S21-T13b-banc
GODOT : même procédure que le prompt de réalisation.

1. PÉRIMÈTRE. git diff --name-only origin/main...origin/tache/S21-T13b-banc. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S21*.md et suivi/S21-T13b-banc.md. Tout autre fichier : refus.
2. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : T13b-a, T13b-b.
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
5. COHÉRENCE. C-07 ; constats de SPIKE-01a ; aucun lot après « stopped ».

VERDICT dans rapports/S21-verif-<tentative>.md :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte
Pousse le verdict sur la branche. Si ACCEPTÉE, fais les sous-étapes F de la fiche. Si REFUSÉE, arrête-toi : une IA au rôle de l'auteur reprendra.
```

## Sous-étapes de vérification

- [ ] V1 Prise en charge : pas l'auteur ; copie neuve `../verif-S21-T13b-banc` sur `origin/tache/S21-T13b-banc`.
- [ ] V2 Périmètre : `git diff --name-only origin/main...origin/tache/S21-T13b-banc` ⊂ fichiers autorisés.
- [ ] V3.1 Contrôle T13b-a relancé, résultat conforme.
- [ ] V3.2 Contrôle T13b-b relancé, résultat conforme.
- [ ] V4 Contre-épreuves (CE) appliquées et détectées, puis annulées.
- [ ] V5 Contournements cherchés.
- [ ] V6 Cohérence avec les contrats et les invariants.
- [ ] V7 Verdict écrit dans `rapports/S21-verif-<tentative>.md` et poussé.

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

- [ ] F1 `git switch main && git pull --ff-only && git merge --no-ff origin/tache/S21-T13b-banc -m "Fusion S21 : T13b Banc sans éditeur et scénarios de coupure"`.
- [ ] F2 Sur `main` : `GODOT="$B" tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK. Sinon : `git reset --hard ORIG_HEAD`, verdict « REFUSÉE (fusion) » poussé sur la branche, et arrêt de la fusion.
- [ ] F3 Dans `SUIVI.md`, cocher la ligne **S21** et compléter « fait le <date> · auteur <IA> · vérifié par <IA> · <n> créneaux ».
- [ ] F4 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette.
- [ ] F5 Cocher les sous-étapes F de cette fiche ; `git commit` ; `git push origin main` (en cas de refus : `git pull --rebase`, puis push).

## Pour la recette

Rien de propre à cette unité.
