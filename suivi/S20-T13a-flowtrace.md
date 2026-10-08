# S20 — T13a FlowTrace, runtime et protocole de session

> Fiche d'exécution du mode autonome. Coche chaque case dès qu'elle est faite et prouvée, puis commite et pousse : une autre IA doit pouvoir reprendre à la première case non cochée. Règles : `docs/construction/sequence.md`. Avancement global : `SUIVI.md`.

| Champ | Valeur |
| --- | --- |
| Réalise | Développeur |
| Vérifie | Concepteur (jamais l'auteur) |
| Commence après | S16, S19 (cochées dans `SUIVI.md`) |
| Indépendante de | S17, S18 |
| Branche | `tache/S20-T13a-flowtrace` |
| Fiche de conception | `docs/construction/etape-4.md`, section T13a |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité elle-même peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- `addons/godot_dev_mapper_runtime/flow_trace.gd` : classe statique FlowTrace, sans autoload, par la façade runtime ; API de C-07, toute la table d'états, bail, réserve de contrôle, pile d'invocations, registre et état initial.
- Appliquer les constats de SPIKE-01a (et la file de commandes de SPIKE-01b si elle est au contrat).

## Fichiers autorisés

`addons/godot_dev_mapper_runtime/flow_trace.gd`, `tests/unit/test_flow_trace_internals.gd`, les marqueurs T13a de `tests/pending/` (suppression seulement).

Toujours autorisés en plus : `rapports/S20*.md` et les cases de cette fiche.

## Prompt de réalisation

```text
Tu es <ton nom d'IA>, au rôle Développeur. Tu réalises l'unité S20 « T13a FlowTrace, runtime et protocole de session » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.

AVANT TOUT
1. git fetch origin. Lis REGLES_AGENTS.md s'il existe, puis la fiche suivi/S20-T13a-flowtrace.md.
2. Si la branche origin/tache/S20-T13a-flowtrace existe : reprends-la, relis rapports/S20.md et commence à la première sous-étape R non cochée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
3. Sinon : vérifie dans SUIVI.md, sur main, que S16, S19 sont cochées, puis crée tache/S20-T13a-flowtrace depuis main.

GODOT
- Si tools/ci/fetch_godot.sh existe : B=$(tools/ci/fetch_godot.sh 4.7.2-stable)
- Sinon, hors du dépôt :
  D=$HOME/.cache/gdm-godot/4.7.2-stable ; mkdir -p "$D"
  test -x "$D/Godot_v4.7.2-stable_linux.x86_64" || { curl -sSL -o /tmp/godot-4.7.2.zip https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip && unzip -o -q /tmp/godot-4.7.2.zip -d "$D"; }
  B=$D/Godot_v4.7.2-stable_linux.x86_64
- « godot » dans les commandes désigne "$B". Contrôle : "$B" --version contient 4.7.2.stable.
- Éditeur avec rendu, quand la fiche le demande : xvfb-run -a -s "-screen 0 1600x900x24" "$B" --editor --path <projet> --rendering-driver opengl3

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S20.md et les cases de suivi/S20-T13a-flowtrace.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu coches une case seulement quand elle est faite et prouvée. Tu commites et tu pousses après chaque case cochée.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (docs/construction/etape-4.md, T13a)
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
TRAVAIL TECHNIQUE — fin de la copie exacte du guide

ADAPTATIONS DU MODE AUTONOME
- Aucune : suis le travail technique tel quel.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche, et coche chacune.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Coche dans suivi/S20-T13a-flowtrace.md les sous-étapes faites et prouvées ; complète rapports/S20.md (sorties, section « Passation ») ; commite ; git push origin tache/S20-T13a-flowtrace.
- Ne laisse aucune modification non poussée.

FORMAT DE rapports/S20.md
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

- [ ] R0 Prise en charge : `git fetch origin` ; S16, S19 sont cochées dans `SUIVI.md` ; branche `origin/tache/S20-T13a-flowtrace` absente, ou sans commit depuis deux créneaux, ou dernier verdict REFUSÉE ; créer ou reprendre la branche ; `rapports/S20.md` avec « Statut : EN COURS » et « Auteur » ; commit ; push.
- [ ] R1 Supprimer les marqueurs T13a ; coller l'échec.
- [ ] R2 Implémenter l'API statique et la table d'états.
- [ ] R3 Implémenter le bail et la réserve de contrôle.
- [ ] R4 Implémenter la pile d'invocations.
- [ ] R5 Implémenter le registre des instances et l'état initial.
- [ ] R6 Écrire `tests/unit/test_flow_trace_internals.gd` (transport de substitution, horloge factice).
- [ ] R7 Écrire dans le rapport le tableau transition → test (T13a-d).
- [ ] R8 Contrôles finaux : T13a-a, T13a-b, T13a-c, T13a-d exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » ; commit ; push.

## Prompt de vérification

```text
Tu es <ton nom d'IA>, au rôle Concepteur, vérificateur indépendant de l'unité S20 « T13a FlowTrace, runtime et protocole de session » du projet GODOT_DEV_MAPPER.
Tu n'en es pas l'auteur : lis la ligne « Auteur » de rapports/S20.md ; si c'est toi, arrête-toi.
Tu ne modifies aucun fichier de l'unité. Tu écris ton verdict et tu coches les sous-étapes V, sur la branche.

COPIE NEUVE : git fetch origin && git worktree add --detach ../verif-S20-T13a-flowtrace origin/tache/S20-T13a-flowtrace
GODOT : même procédure que le prompt de réalisation.

1. PÉRIMÈTRE. git diff --name-only origin/main...origin/tache/S20-T13a-flowtrace. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S20*.md et suivi/S20-T13a-flowtrace.md. Tout autre fichier : refus.
2. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : T13a-a, T13a-b, T13a-c, T13a-d.
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
5. COHÉRENCE. C-07, C-04 ; constats de SPIKE-01a ; INV-06.

VERDICT dans rapports/S20-verif-<tentative>.md :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte
Pousse le verdict sur la branche. Si ACCEPTÉE, fais les sous-étapes F de la fiche. Si REFUSÉE, arrête-toi : une IA au rôle de l'auteur reprendra.
```

## Sous-étapes de vérification

- [ ] V1 Prise en charge : pas l'auteur ; copie neuve `../verif-S20-T13a-flowtrace` sur `origin/tache/S20-T13a-flowtrace`.
- [ ] V2 Périmètre : `git diff --name-only origin/main...origin/tache/S20-T13a-flowtrace` ⊂ fichiers autorisés.
- [ ] V3.1 Contrôle T13a-a relancé, résultat conforme.
- [ ] V3.2 Contrôle T13a-b relancé, résultat conforme.
- [ ] V3.3 Contrôle T13a-c relancé, résultat conforme.
- [ ] V3.4 Contrôle T13a-d relancé, résultat conforme.
- [ ] V4 Contre-épreuves (CE) appliquées et détectées, puis annulées.
- [ ] V5 Contournements cherchés.
- [ ] V6 Cohérence avec les contrats et les invariants.
- [ ] V7 Verdict écrit dans `rapports/S20-verif-<tentative>.md` et poussé.

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

- [ ] F1 `git switch main && git pull --ff-only && git merge --no-ff origin/tache/S20-T13a-flowtrace -m "Fusion S20 : T13a FlowTrace, runtime et protocole de session"`.
- [ ] F2 Sur `main` : `GODOT="$B" tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK. Sinon : `git reset --hard ORIG_HEAD`, verdict « REFUSÉE (fusion) » poussé sur la branche, et arrêt de la fusion.
- [ ] F3 Dans `SUIVI.md`, cocher la ligne **S20** et compléter « fait le <date> · auteur <IA> · vérifié par <IA> · <n> créneaux ».
- [ ] F4 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette.
- [ ] F5 Cocher les sous-étapes F de cette fiche ; `git commit` ; `git push origin main` (en cas de refus : `git pull --rebase`, puis push).

## Pour la recette

Rien de propre à cette unité.
