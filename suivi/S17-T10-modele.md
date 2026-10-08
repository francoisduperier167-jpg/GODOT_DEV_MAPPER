# S17 — T10 Modèle minimal, graphe déclaré, clés de sonde

> Fiche d'exécution du mode autonome. Coche chaque case dès qu'elle est faite et prouvée, puis commite et pousse : une autre IA doit pouvoir reprendre à la première case non cochée. Règles : `docs/construction/sequence.md`. Avancement global : `SUIVI.md`.

| Champ | Valeur |
| --- | --- |
| Réalise | Développeur |
| Vérifie | Vérificateur (jamais l'auteur) |
| Commence après | S16 (cochées dans `SUIVI.md`) |
| Indépendante de | S19, S20, S21, S22, S25, S33 |
| Branche | `tache/S17-T10-modele` |
| Fiche de conception | `docs/construction/etape-4.md`, section T10 |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité elle-même peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Dans `addons/godot_dev_mapper/core/` : le modèle minimal, le chargeur de `.flow.json` v1 et la table des clés de sonde.
- Rejet de chaque fixture invalide avec son code ; références non résolues conservées ; clé inconnue « définition non résolue » ; `core/` sans dépendance.

## Fichiers autorisés

`addons/godot_dev_mapper/core/`, les marqueurs T10 de `tests/pending/` (suppression seulement).

Toujours autorisés en plus : `rapports/S17*.md` et les cases de cette fiche.

## Prompt de réalisation

```text
Tu es <ton nom d'IA>, au rôle Développeur. Tu réalises l'unité S17 « T10 Modèle minimal, graphe déclaré, clés de sonde » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.

AVANT TOUT
1. git fetch origin. Lis REGLES_AGENTS.md s'il existe, puis la fiche suivi/S17-T10-modele.md.
2. Si la branche origin/tache/S17-T10-modele existe : reprends-la, relis rapports/S17.md et commence à la première sous-étape R non cochée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
3. Sinon : vérifie dans SUIVI.md, sur main, que S16 est cochée, puis crée tache/S17-T10-modele depuis main.

GODOT
- Si tools/ci/fetch_godot.sh existe : B=$(tools/ci/fetch_godot.sh 4.7.2-stable)
- Sinon, hors du dépôt :
  D=$HOME/.cache/gdm-godot/4.7.2-stable ; mkdir -p "$D"
  test -x "$D/Godot_v4.7.2-stable_linux.x86_64" || { curl -sSL -o /tmp/godot-4.7.2.zip https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip && unzip -o -q /tmp/godot-4.7.2.zip -d "$D"; }
  B=$D/Godot_v4.7.2-stable_linux.x86_64
- « godot » dans les commandes désigne "$B". Contrôle : "$B" --version contient 4.7.2.stable.
- Éditeur avec rendu, quand la fiche le demande : xvfb-run -a -s "-screen 0 1600x900x24" "$B" --editor --path <projet> --rendering-driver opengl3

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S17.md et les cases de suivi/S17-T10-modele.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu coches une case seulement quand elle est faite et prouvée. Tu commites et tu pousses après chaque case cochée.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (docs/construction/etape-4.md, T10)
Tu réalises la tâche T10 du projet GODOT_DEV_MAPPER. Applique les règles et le format de rapport du prompt universel de réalisation.
CONTEXTE : docs/CONTRACTS.md, sections C-01, C-02 et C-05, avec leurs tables de codes d'erreur ; contracts/schemas/declared_graph.v1.schema.json ; tests/contract/test_c01_identities.gd et test_c05_declared_graph.gd, avec leurs fixtures.
OBJECTIF : dans addons/godot_dev_mapper/core/, le modèle minimal, le chargeur de .flow.json v1 et la table des clés de sonde.
- Le chargeur rejette chaque fixture invalide avec le code d'erreur attendu, et celui-là seulement.
- Il conserve les références non résolues.
- Une clé de sonde inconnue donne « définition non résolue ».
- core/ ne dépend d'aucun autre module.
DÉROULÉ : supprime les marqueurs T10 de tests/pending/, montre l'échec, puis implémente.
CONTRÔLES
T10-a  runner → 0, aucun marqueur T10 restant
T10-b  python3 tools/check_deps.py ; echo $?   → 0
T10-c  GODOT=<binaire> tools/ci/run_all_checks.sh ; echo $?   → 0
CONTRE-ÉPREUVE (CE) pour le vérificateur : faire accepter au chargeur une clé de sonde présente dans deux définitions → test_c05 échoue sur le code de doublon.
TRAVAIL TECHNIQUE — fin de la copie exacte du guide

ADAPTATIONS DU MODE AUTONOME
- Aucune : suis le travail technique tel quel.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche, et coche chacune.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Coche dans suivi/S17-T10-modele.md les sous-étapes faites et prouvées ; complète rapports/S17.md (sorties, section « Passation ») ; commite ; git push origin tache/S17-T10-modele.
- Ne laisse aucune modification non poussée.

FORMAT DE rapports/S17.md
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

- [ ] R0 Prise en charge : `git fetch origin` ; S16 est cochée dans `SUIVI.md` ; branche `origin/tache/S17-T10-modele` absente, ou sans commit depuis deux créneaux, ou dernier verdict REFUSÉE ; créer ou reprendre la branche ; `rapports/S17.md` avec « Statut : EN COURS » et « Auteur » ; commit ; push.
- [ ] R1 Supprimer les marqueurs T10 ; coller l'échec.
- [ ] R2 Implémenter le modèle minimal (C-01, C-02).
- [ ] R3 Implémenter le chargeur de `.flow.json` v1 et ses codes d'erreur (C-05).
- [ ] R4 Implémenter la table des clés de sonde.
- [ ] R5 Faire passer les tests sans les modifier.
- [ ] R6 Contrôles finaux : T10-a, T10-b, T10-c exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » ; commit ; push.

## Prompt de vérification

```text
Tu es <ton nom d'IA>, au rôle Vérificateur, vérificateur indépendant de l'unité S17 « T10 Modèle minimal, graphe déclaré, clés de sonde » du projet GODOT_DEV_MAPPER.
Tu n'en es pas l'auteur : lis la ligne « Auteur » de rapports/S17.md ; si c'est toi, arrête-toi.
Tu ne modifies aucun fichier de l'unité. Tu écris ton verdict et tu coches les sous-étapes V, sur la branche.

COPIE NEUVE : git fetch origin && git worktree add --detach ../verif-S17-T10-modele origin/tache/S17-T10-modele
GODOT : même procédure que le prompt de réalisation.

1. PÉRIMÈTRE. git diff --name-only origin/main...origin/tache/S17-T10-modele. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S17*.md et suivi/S17-T10-modele.md. Tout autre fichier : refus.
2. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : T10-a, T10-b, T10-c.
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
5. COHÉRENCE. C-01, C-02, C-05 ; `core/` ne dépend d'aucun autre module.

VERDICT dans rapports/S17-verif-<tentative>.md :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte
Pousse le verdict sur la branche. Si ACCEPTÉE, fais les sous-étapes F de la fiche. Si REFUSÉE, arrête-toi : une IA au rôle de l'auteur reprendra.
```

## Sous-étapes de vérification

- [ ] V1 Prise en charge : pas l'auteur ; copie neuve `../verif-S17-T10-modele` sur `origin/tache/S17-T10-modele`.
- [ ] V2 Périmètre : `git diff --name-only origin/main...origin/tache/S17-T10-modele` ⊂ fichiers autorisés.
- [ ] V3.1 Contrôle T10-a relancé, résultat conforme.
- [ ] V3.2 Contrôle T10-b relancé, résultat conforme.
- [ ] V3.3 Contrôle T10-c relancé, résultat conforme.
- [ ] V4 Contre-épreuves (CE) appliquées et détectées, puis annulées.
- [ ] V5 Contournements cherchés.
- [ ] V6 Cohérence avec les contrats et les invariants.
- [ ] V7 Verdict écrit dans `rapports/S17-verif-<tentative>.md` et poussé.

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

- [ ] F1 `git switch main && git pull --ff-only && git merge --no-ff origin/tache/S17-T10-modele -m "Fusion S17 : T10 Modèle minimal, graphe déclaré, clés de sonde"`.
- [ ] F2 Sur `main` : `GODOT="$B" tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK. Sinon : `git reset --hard ORIG_HEAD`, verdict « REFUSÉE (fusion) » poussé sur la branche, et arrêt de la fusion.
- [ ] F3 Dans `SUIVI.md`, cocher la ligne **S17** et compléter « fait le <date> · auteur <IA> · vérifié par <IA> · <n> créneaux ».
- [ ] F4 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette.
- [ ] F5 Cocher les sous-étapes F de cette fiche ; `git commit` ; `git push origin main` (en cas de refus : `git pull --rebase`, puis push).

## Pour la recette

Rien de propre à cette unité.
