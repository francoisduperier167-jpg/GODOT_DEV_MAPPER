# S30 — T18 Robustesse et cycle de vie

> Fiche d'exécution du mode autonome. Coche chaque case dès qu'elle est faite et prouvée, puis commite et pousse : une autre IA doit pouvoir reprendre à la première case non cochée. Règles : `docs/construction/sequence.md`. Avancement global : `SUIVI.md`.

| Champ | Valeur |
| --- | --- |
| Réalise | Développeur |
| Vérifie | Concepteur (jamais l'auteur) |
| Commence après | S21, S24 (cochées dans `SUIVI.md`) |
| Indépendante de | S22, S23, S25, S26, S27, S28, S29, S33 |
| Branche | `tache/S30-T18-robustesse` |
| Fiche de conception | `docs/construction/etape-6.md`, section T18 |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité elle-même peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- `tests/integration/run_lifecycle.sh` : six scénarios (sans débogueur, cinq démarrages et arrêts, coupure du récepteur, jeu tué, désactivation simulée, redémarrage), et `checks.d/65-lifecycle.sh`.
- Corriger un défaut sans changer de contrat ; sinon QUESTION avec le diagnostic.

## Fichiers autorisés

`tests/integration/run_lifecycle.sh`, `tools/harness/` (nouveaux scénarios), `tests/unit/test_session_controller.gd` (nouveaux cas), `tools/ci/checks.d/65-lifecycle.sh`. Pour corriger un défaut sans changer de contrat : `addons/godot_dev_mapper_runtime/flow_trace.gd` et `addons/godot_dev_mapper/editor/session_controller.gd`. Les tests de contrat restent intouchables ; une correction qui exigerait de changer un contrat passe par QUESTION.

Toujours autorisés en plus : `rapports/S30*.md` et les cases de cette fiche.

## Prompt de réalisation

```text
Tu es <ton nom d'IA>, au rôle Développeur. Tu réalises l'unité S30 « T18 Robustesse et cycle de vie » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.

AVANT TOUT
1. git fetch origin. Lis REGLES_AGENTS.md s'il existe, puis la fiche suivi/S30-T18-robustesse.md.
2. Si la branche origin/tache/S30-T18-robustesse existe : reprends-la, relis rapports/S30.md et commence à la première sous-étape R non cochée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
3. Sinon : vérifie dans SUIVI.md, sur main, que S21, S24 sont cochées, puis crée tache/S30-T18-robustesse depuis main.

GODOT
- Si tools/ci/fetch_godot.sh existe : B=$(tools/ci/fetch_godot.sh 4.7.2-stable)
- Sinon, hors du dépôt :
  D=$HOME/.cache/gdm-godot/4.7.2-stable ; mkdir -p "$D"
  test -x "$D/Godot_v4.7.2-stable_linux.x86_64" || { curl -sSL -o /tmp/godot-4.7.2.zip https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip && unzip -o -q /tmp/godot-4.7.2.zip -d "$D"; }
  B=$D/Godot_v4.7.2-stable_linux.x86_64
- « godot » dans les commandes désigne "$B". Contrôle : "$B" --version contient 4.7.2.stable.
- Éditeur avec rendu, quand la fiche le demande : xvfb-run -a -s "-screen 0 1600x900x24" "$B" --editor --path <projet> --rendering-driver opengl3

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S30.md et les cases de suivi/S30-T18-robustesse.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu coches une case seulement quand elle est faite et prouvée. Tu commites et tu pousses après chaque case cochée.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (docs/construction/etape-6.md, T18)
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
TRAVAIL TECHNIQUE — fin de la copie exacte du guide

ADAPTATIONS DU MODE AUTONOME
- « SUR MA MACHINE, plus tard » : la désactivation du plugin pendant une vraie collecte passe à la recette.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche, et coche chacune.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Coche dans suivi/S30-T18-robustesse.md les sous-étapes faites et prouvées ; complète rapports/S30.md (sorties, section « Passation ») ; commite ; git push origin tache/S30-T18-robustesse.
- Ne laisse aucune modification non poussée.

FORMAT DE rapports/S30.md
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

- [ ] R0 Prise en charge : `git fetch origin` ; S21, S24 sont cochées dans `SUIVI.md` ; branche `origin/tache/S30-T18-robustesse` absente, ou sans commit depuis deux créneaux, ou dernier verdict REFUSÉE ; créer ou reprendre la branche ; `rapports/S30.md` avec « Statut : EN COURS » et « Auteur » ; commit ; push.
- [ ] R1 Scénario 1 : jeu sans débogueur.
- [ ] R2 Scénario 2 : cinq démarrages et arrêts.
- [ ] R3 Scénario 3 : coupure du récepteur.
- [ ] R4 Scénario 4 : jeu tué (kill -9).
- [ ] R5 Scénario 5 : désactivation du plugin simulée sur le contrôleur.
- [ ] R6 Scénario 6 : jeu redémarré, nouvelle session.
- [ ] R7 Écrire `tools/ci/checks.d/65-lifecycle.sh`.
- [ ] R8 Contrôles finaux : T18-a, T18-b exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » ; commit ; push.

## Prompt de vérification

```text
Tu es <ton nom d'IA>, au rôle Concepteur, vérificateur indépendant de l'unité S30 « T18 Robustesse et cycle de vie » du projet GODOT_DEV_MAPPER.
Tu n'en es pas l'auteur : lis la ligne « Auteur » de rapports/S30.md ; si c'est toi, arrête-toi.
Tu ne modifies aucun fichier de l'unité. Tu écris ton verdict et tu coches les sous-étapes V, sur la branche.

COPIE NEUVE : git fetch origin && git worktree add --detach ../verif-S30-T18-robustesse origin/tache/S30-T18-robustesse
GODOT : même procédure que le prompt de réalisation.

1. PÉRIMÈTRE. git diff --name-only origin/main...origin/tache/S30-T18-robustesse. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S30*.md et suivi/S30-T18-robustesse.md. Tout autre fichier : refus.
2. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : T18-a, T18-b.
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
5. COHÉRENCE. Plan §8 (trois opérations du cycle de vie) ; C-07.

VERDICT dans rapports/S30-verif-<tentative>.md :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte
Pousse le verdict sur la branche. Si ACCEPTÉE, fais les sous-étapes F de la fiche. Si REFUSÉE, arrête-toi : une IA au rôle de l'auteur reprendra.
```

## Sous-étapes de vérification

- [ ] V1 Prise en charge : pas l'auteur ; copie neuve `../verif-S30-T18-robustesse` sur `origin/tache/S30-T18-robustesse`.
- [ ] V2 Périmètre : `git diff --name-only origin/main...origin/tache/S30-T18-robustesse` ⊂ fichiers autorisés.
- [ ] V3.1 Contrôle T18-a relancé, résultat conforme.
- [ ] V3.2 Contrôle T18-b relancé, résultat conforme.
- [ ] V4 Contre-épreuves (CE) appliquées et détectées, puis annulées.
- [ ] V5 Contournements cherchés.
- [ ] V6 Cohérence avec les contrats et les invariants.
- [ ] V7 Verdict écrit dans `rapports/S30-verif-<tentative>.md` et poussé.

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

- [ ] F1 `git switch main && git pull --ff-only && git merge --no-ff origin/tache/S30-T18-robustesse -m "Fusion S30 : T18 Robustesse et cycle de vie"`.
- [ ] F2 Sur `main` : `GODOT="$B" tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK. Sinon : `git reset --hard ORIG_HEAD`, verdict « REFUSÉE (fusion) » poussé sur la branche, et arrêt de la fusion.
- [ ] F3 Dans `SUIVI.md`, cocher la ligne **S30** et compléter « fait le <date> · auteur <IA> · vérifié par <IA> · <n> créneaux ».
- [ ] F4 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette.
- [ ] F5 Cocher les sous-étapes F de cette fiche ; `git commit` ; `git push origin main` (en cas de refus : `git pull --rebase`, puis push).

## Pour la recette

- Désactiver le plugin pendant une vraie collecte, dans ton éditeur.
