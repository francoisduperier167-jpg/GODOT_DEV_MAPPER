# S34 — T19 Mesure de valeur par substitution

> Fiche d'exécution du mode autonome. Coche chaque case dès qu'elle est faite et prouvée, puis commite et pousse : une autre IA doit pouvoir reprendre à la première case non cochée. Règles : `docs/construction/sequence.md`. Avancement global : `SUIVI.md`.

| Champ | Valeur |
| --- | --- |
| Réalise | Développeur |
| Vérifie | Vérificateur (jamais l'auteur) |
| Commence après | S32, S33 (cochées dans `SUIVI.md`) |
| Indépendante de | aucune |
| Branche | `tache/S34-T19-diagnostic` |
| Estimation | 2 créneaux |

**Séquentiel ou indépendant.** Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité elle-même peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Préparer `fake_editor.gd --record` et `tools/gdm_query.gd`, puis diagnostiquer les trois bugs : 1 avec l'outil, 2 sans, 3 avec, sans avoir lu l'enveloppe.
- Compter pour chaque bug les exécutions, lectures, modifications temporaires et le temps ; proposer la cause ; ouvrir l'enveloppe seulement après ; écrire `docs/mesures/valeur-poc-substitution.md`.
- Appliquer le critère d'arrêt : si l'outil n'a aidé sur aucun des bugs 1 et 3, écrire `rapports/ARRET.md`.

## Fichiers autorisés

`tools/harness/fake_editor.gd` (option `--record`), `tools/gdm_query.gd`, `docs/mesures/valeur-poc-substitution.md`.

Toujours autorisés en plus : `rapports/S34*.md` et les cases de cette fiche.

## Contrôles propres à cette fiche

- `S34-a` : `grep -c "pas pour une personne" docs/mesures/valeur-poc-substitution.md` → 1
- `T19-a` : Chaque branche de bug reproduit son symptôme seule → trois symptômes reproduits
- `T19-b` : Heure d'ouverture de l'enveloppe notée après le dernier diagnostic → présente
- `T19-c` : Tableau et conclusion complets, durées marquées indicatives → aucune case vide
- `T19-d` : Le vérificateur relit le tableau contre l'enveloppe → concordance des causes
- (CE) Le vérificateur relance `tools/gdm_query.gd` sur une session à trou : le chemin observé est « indéterminé ».

## Prompt de réalisation

```text
Tu es <ton nom d'IA>, au rôle Développeur. Tu réalises l'unité S34 « T19 Mesure de valeur par substitution » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.

AVANT TOUT
1. git fetch origin. Lis REGLES_AGENTS.md s'il existe, puis la fiche suivi/S34-T19-diagnostic.md.
2. Si la branche origin/tache/S34-T19-diagnostic existe : reprends-la, relis rapports/S34.md et commence à la première sous-étape R non cochée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
3. Sinon : vérifie dans SUIVI.md, sur main, que S32, S33 sont cochées, puis crée tache/S34-T19-diagnostic depuis main.

GODOT
- Si tools/ci/fetch_godot.sh existe : B=$(tools/ci/fetch_godot.sh 4.7.2-stable)
- Sinon, hors du dépôt :
  D=$HOME/.cache/gdm-godot/4.7.2-stable ; mkdir -p "$D"
  test -x "$D/Godot_v4.7.2-stable_linux.x86_64" || { curl -sSL -o /tmp/godot-4.7.2.zip https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip && unzip -o -q /tmp/godot-4.7.2.zip -d "$D"; }
  B=$D/Godot_v4.7.2-stable_linux.x86_64
- « godot » dans les commandes désigne "$B". Contrôle : "$B" --version contient 4.7.2.stable.
- Éditeur avec rendu, quand la fiche le demande : xvfb-run -a -s "-screen 0 1600x900x24" "$B" --editor --path <projet> --rendering-driver opengl3

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S34.md et les cases de suivi/S34-T19-diagnostic.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu coches une case seulement quand elle est faite et prouvée. Tu commites et tu pousses après chaque case cochée.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (rédigé pour le mode autonome)
Tu mesures, par substitution, l'utilité du POC du projet GODOT_DEV_MAPPER. Tu n'as pas lu ENVELOPPE_SCELLEE.md et tu ne récupères pas la branche banc/<nom>-enveloppe avant la fin des trois diagnostics.

PRÉPARE (fichiers autorisés : tools/harness/fake_editor.gd, tools/gdm_query.gd, docs/mesures/valeur-poc-substitution.md)
- --record enregistre la session reçue, lot par lot, dans un fichier JSONL.
- tools/gdm_query.gd relit ce fichier avec store/ et projections/, et affiche le journal d'une instance et le chemin observé de ses invocations.

MESURE, sur les branches banc/<nom>-bug-1 à -bug-3, dans cet ordre, avec les symptômes de rapports/S33.md :
- bug 1 avec l'outil : code du jeu, console du jeu, session enregistrée, sorties de gdm_query, captures du panneau sous écran virtuel si utile ;
- bug 2 sans l'outil : code du jeu et console du jeu seulement ; tu peux ajouter des print ;
- bug 3 avec l'outil.
Pour chaque bug, note : le nombre d'exécutions du jeu, de lectures de fichier et de modifications temporaires ; le temps écoulé ; la cause proposée, avec le fichier et la ligne ; ta confiance.
Ensuite seulement, récupère l'enveloppe, note l'heure, et note pour chaque bug si la cause est exacte.

RAPPORT dans docs/mesures/valeur-poc-substitution.md : le tableau de T19 adapté (colonnes : bug, branche, avec l'outil, préparation, exécutions, lectures, modifications, temps, cause proposée, confiance, cause exacte), puis une conclusion qualitative. Écris en tête : « Signal mesuré pour un agent, pas pour une personne ; la mesure humaine se fait à la recette. »

CRITÈRE D'ARRÊT : l'outil a aidé sur un bug s'il a permis de trouver la cause exacte avec moins d'exécutions qu'au bug 2, ou là où le bug 2 n'a pas été trouvé. S'il n'a aidé ni sur le bug 1 ni sur le bug 3, écris rapports/ARRET.md (raison, preuves, ce qu'il faut de l'humain), pousse-le sur main et arrête-toi.
TRAVAIL TECHNIQUE — fin de la copie exacte du guide

CONTRÔLES DE LA FICHE
S34-a  grep -c "pas pour une personne" docs/mesures/valeur-poc-substitution.md   → 1
T19-a  Chaque branche de bug reproduit son symptôme seule   → trois symptômes reproduits
T19-b  Heure d'ouverture de l'enveloppe notée après le dernier diagnostic   → présente
T19-c  Tableau et conclusion complets, durées marquées indicatives   → aucune case vide
T19-d  Le vérificateur relit le tableau contre l'enveloppe   → concordance des causes
(CE) Le vérificateur relance `tools/gdm_query.gd` sur une session à trou : le chemin observé est « indéterminé ».

ADAPTATIONS DU MODE AUTONOME
- Aucune : suis le travail technique tel quel.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche, et coche chacune.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Coche dans suivi/S34-T19-diagnostic.md les sous-étapes faites et prouvées ; complète rapports/S34.md (sorties, section « Passation ») ; commite ; git push origin tache/S34-T19-diagnostic.
- Ne laisse aucune modification non poussée.

FORMAT DE rapports/S34.md
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

- [ ] R0 Prise en charge : `git fetch origin` ; S32, S33 sont cochées dans `SUIVI.md` ; branche `origin/tache/S34-T19-diagnostic` absente, ou sans commit depuis deux créneaux, ou dernier verdict REFUSÉE ; créer ou reprendre la branche ; `rapports/S34.md` avec « Statut : EN COURS » et « Auteur » ; commit ; push.
- [ ] R1 Ajouter l'option `--record` à `tools/harness/fake_editor.gd` (session en JSONL).
- [ ] R2 Écrire `tools/gdm_query.gd` : relit la session avec `store/` et `projections/`, affiche le journal d'une instance et le chemin observé de ses invocations.
- [ ] R3 Bug 1, avec l'outil : diagnostic et comptes.
- [ ] R4 Bug 2, sans l'outil : diagnostic et comptes.
- [ ] R5 Bug 3, avec l'outil : diagnostic et comptes.
- [ ] R6 Ouvrir l'enveloppe (`git fetch origin banc/<nom>-enveloppe`) ; noter l'heure ; comparer les causes.
- [ ] R7 Écrire `docs/mesures/valeur-poc-substitution.md` (signal pour un agent, pas pour une personne, écrit en tête).
- [ ] R8 Appliquer le critère d'arrêt.
- [ ] R9 Contrôles finaux : S34-a, T19-a, T19-b, T19-c, T19-d exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » ; commit ; push.

## Prompt de vérification

```text
Tu es <ton nom d'IA>, au rôle Vérificateur, vérificateur indépendant de l'unité S34 « T19 Mesure de valeur par substitution » du projet GODOT_DEV_MAPPER.
Tu n'en es pas l'auteur : lis la ligne « Auteur » de rapports/S34.md ; si c'est toi, arrête-toi.
Tu ne modifies aucun fichier de l'unité. Tu écris ton verdict et tu coches les sous-étapes V, sur la branche.

COPIE NEUVE : git fetch origin && git worktree add --detach ../verif-S34-T19-diagnostic origin/tache/S34-T19-diagnostic
GODOT : même procédure que le prompt de réalisation.

1. PÉRIMÈTRE. git diff --name-only origin/main...origin/tache/S34-T19-diagnostic. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S34*.md et suivi/S34-T19-diagnostic.md. Tout autre fichier : refus.
2. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : S34-a, T19-a, T19-b, T19-c, T19-d.
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
5. COHÉRENCE. Fiche T19 ; plan §9 (mesure exploratoire, critère d'arrêt).

VERDICT dans rapports/S34-verif-<tentative>.md :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte
Pousse le verdict sur la branche. Si ACCEPTÉE, fais les sous-étapes F de la fiche. Si REFUSÉE, arrête-toi : une IA au rôle de l'auteur reprendra.
```

## Sous-étapes de vérification

- [ ] V1 Prise en charge : pas l'auteur ; copie neuve `../verif-S34-T19-diagnostic` sur `origin/tache/S34-T19-diagnostic`.
- [ ] V2 Périmètre : `git diff --name-only origin/main...origin/tache/S34-T19-diagnostic` ⊂ fichiers autorisés.
- [ ] V3.1 Contrôle S34-a relancé, résultat conforme.
- [ ] V3.2 Contrôle T19-a relancé, résultat conforme.
- [ ] V3.3 Contrôle T19-b relancé, résultat conforme.
- [ ] V3.4 Contrôle T19-c relancé, résultat conforme.
- [ ] V3.5 Contrôle T19-d relancé, résultat conforme.
- [ ] V4 Contre-épreuves (CE) appliquées et détectées, puis annulées.
- [ ] V5 Contournements cherchés.
- [ ] V6 Cohérence avec les contrats et les invariants.
- [ ] V7 Verdict écrit dans `rapports/S34-verif-<tentative>.md` et poussé.

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

- [ ] F1 `git switch main && git pull --ff-only && git merge --no-ff origin/tache/S34-T19-diagnostic -m "Fusion S34 : T19 Mesure de valeur par substitution"`.
- [ ] F2 Sur `main` : `GODOT="$B" tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK. Sinon : `git reset --hard ORIG_HEAD`, verdict « REFUSÉE (fusion) » poussé sur la branche, et arrêt de la fusion.
- [ ] F3 Dans `SUIVI.md`, cocher la ligne **S34** et compléter « fait le <date> · auteur <IA> · vérifié par <IA> · <n> créneaux ».
- [ ] F4 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette.
- [ ] F5 Cocher les sous-étapes F de cette fiche ; `git commit` ; `git push origin main` (en cas de refus : `git pull --rebase`, puis push).

## Pour la recette

- Mesure de valeur humaine (T19 du guide), sur trois nouveaux bugs.
