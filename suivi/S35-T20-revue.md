# S35 — T20 Revue de continuation et décision

> Fiche d'exécution du mode autonome. Coche chaque case dès qu'elle est faite et prouvée, puis commite et pousse : une autre IA doit pouvoir reprendre à la première case non cochée. Règles : `docs/construction/sequence.md`. Avancement global : `SUIVI.md`.

| Champ | Valeur |
| --- | --- |
| Réalise | Concepteur |
| Vérifie | Vérificateur (jamais l'auteur) |
| Commence après | S34 (cochées dans `SUIVI.md`) |
| Indépendante de | aucune |
| Branche | `tache/S35-T20-revue` |
| Fiche de conception | `docs/construction/etape-7.md`, section T20 |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité elle-même peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Écrire `docs/revues/revue-poc.md` : budgets en créneaux, fiabilité par IA, signal d'utilité par substitution, risques, options, décisions à prendre, proposition d'amendement PD-0.6.
- Décider selon la règle : continuer si le signal est positif, si aucun arrêt n'est ouvert et si les créneaux consommés restent sous le double de l'estimation ; sinon écrire `rapports/ARRET.md`.
- Appliquer l'amendement PD-0.6 au statut « proposé ».

## Fichiers autorisés

`docs/revues/revue-poc.md`, `docs/plan-directeur.md` (amendement PD-0.6, statut « proposé »). À la fusion : la décision dans `docs/DECISIONS.md`.

Toujours autorisés en plus : `rapports/S35*.md` et les cases de cette fiche.

## Prompt de réalisation

```text
Tu es <ton nom d'IA>, au rôle Concepteur. Tu réalises l'unité S35 « T20 Revue de continuation et décision » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.

AVANT TOUT
1. git fetch origin. Lis REGLES_AGENTS.md s'il existe, puis la fiche suivi/S35-T20-revue.md.
2. Si la branche origin/tache/S35-T20-revue existe : reprends-la, relis rapports/S35.md et commence à la première sous-étape R non cochée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
3. Sinon : vérifie dans SUIVI.md, sur main, que S34 est cochée, puis crée tache/S35-T20-revue depuis main.

GODOT
- Si tools/ci/fetch_godot.sh existe : B=$(tools/ci/fetch_godot.sh 4.7.2-stable)
- Sinon, hors du dépôt :
  D=$HOME/.cache/gdm-godot/4.7.2-stable ; mkdir -p "$D"
  test -x "$D/Godot_v4.7.2-stable_linux.x86_64" || { curl -sSL -o /tmp/godot-4.7.2.zip https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip && unzip -o -q /tmp/godot-4.7.2.zip -d "$D"; }
  B=$D/Godot_v4.7.2-stable_linux.x86_64
- « godot » dans les commandes désigne "$B". Contrôle : "$B" --version contient 4.7.2.stable.
- Éditeur avec rendu, quand la fiche le demande : xvfb-run -a -s "-screen 0 1600x900x24" "$B" --editor --path <projet> --rendering-driver opengl3

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S35.md et les cases de suivi/S35-T20-revue.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu coches une case seulement quand elle est faite et prouvée. Tu commites et tu pousses après chaque case cochée.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (docs/construction/etape-7.md, T20)
Tu prépares la revue de continuation du POC du projet GODOT_DEV_MAPPER. Tu ne décides pas : la décision est humaine.

ENTRÉES : PROJECT_STATE.md, docs/mesures/valeur-poc.md, docs/spikes/, les verdicts de vérification, docs/plan-directeur.md §9.

PRODUIS docs/revues/revue-poc.md avec :
1. Budgets : heures humaines et temps agent consommés par étape, contre le budget ; ratio global.
2. Fiabilité : taux de réussite au premier essai, escalades et refus du vérificateur, par modèle.
3. Signal d'utilité : lecture qualitative de T19, avec ses limites (trois bugs, une seule personne, durées indicatives).
4. Risques : ceux du plan, mis à jour ; les nouveaux.
5. Options : continuer, réduire, réorienter ou arrêter. Pour chacune : conditions, conséquences, budget restant estimé avec le ratio observé.
6. Décisions à prendre :
   - SPIKE-03 (rendu) et SPIKE-04 (AST Flow ou extraction maison) au début du MVP ;
   - reprise d'AST Flow comme backend statique ;
   - routage des modèles pour le MVP ;
   - besoin, ou non, d'une mesure de valeur plus large au MVP.
7. Proposition d'amendement du plan (PD-0.6) : budgets recalibrés et décisions retenues. Le diff exact, sans l'appliquer.
TRAVAIL TECHNIQUE — fin de la copie exacte du guide

ADAPTATIONS DU MODE AUTONOME
- « Tu ne décides pas : la décision est humaine » : en mode autonome, tu appliques la règle de décision de la fiche, et la décision est inscrite « adoptée par défaut ».
- Budgets : en créneaux d'IA (estimation de `sequence.md` §8), et non en heures humaines.
- SPIKE-04 : si la reprise d'AST Flow est recommandée, c'est une nouvelle dépendance, à décider par l'humain ; le MVP continue avec l'extraction maison en attendant.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche, et coche chacune.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Coche dans suivi/S35-T20-revue.md les sous-étapes faites et prouvées ; complète rapports/S35.md (sorties, section « Passation ») ; commite ; git push origin tache/S35-T20-revue.
- Ne laisse aucune modification non poussée.

FORMAT DE rapports/S35.md
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

- [ ] R0 Prise en charge : `git fetch origin` ; S34 est cochée dans `SUIVI.md` ; branche `origin/tache/S35-T20-revue` absente, ou sans commit depuis deux créneaux, ou dernier verdict REFUSÉE ; créer ou reprendre la branche ; `rapports/S35.md` avec « Statut : EN COURS » et « Auteur » ; commit ; push.
- [ ] R1 Rassembler `SUIVI.md`, `PROJECT_STATE.md`, les verdicts, `docs/mesures/valeur-poc-substitution.md`, `docs/spikes/`.
- [ ] R2 Écrire les sections 1 à 6 de la revue.
- [ ] R3 Appliquer la règle de décision et l'écrire dans la revue.
- [ ] R4 Écrire et appliquer l'amendement PD-0.6, au statut « proposé ».
- [ ] R5 Si la décision est de s'arrêter : écrire `rapports/ARRET.md`.
- [ ] R6 Contrôles finaux : T20-a, T20-b, T20-c, T20-d exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » ; commit ; push.

## Prompt de vérification

```text
Tu es <ton nom d'IA>, au rôle Vérificateur, vérificateur indépendant de l'unité S35 « T20 Revue de continuation et décision » du projet GODOT_DEV_MAPPER.
Tu n'en es pas l'auteur : lis la ligne « Auteur » de rapports/S35.md ; si c'est toi, arrête-toi.
Tu ne modifies aucun fichier de l'unité. Tu écris ton verdict et tu coches les sous-étapes V, sur la branche.

COPIE NEUVE : git fetch origin && git worktree add --detach ../verif-S35-T20-revue origin/tache/S35-T20-revue
GODOT : même procédure que le prompt de réalisation.

1. PÉRIMÈTRE. git diff --name-only origin/main...origin/tache/S35-T20-revue. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S35*.md et suivi/S35-T20-revue.md. Tout autre fichier : refus.
2. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : T20-a, T20-b, T20-c, T20-d.
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
5. COHÉRENCE. Plan §9 (portes, critères d'arrêt) ; `sequence.md` §5 et §8.

VERDICT dans rapports/S35-verif-<tentative>.md :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte
Pousse le verdict sur la branche. Si ACCEPTÉE, fais les sous-étapes F de la fiche. Si REFUSÉE, arrête-toi : une IA au rôle de l'auteur reprendra.
```

## Sous-étapes de vérification

- [ ] V1 Prise en charge : pas l'auteur ; copie neuve `../verif-S35-T20-revue` sur `origin/tache/S35-T20-revue`.
- [ ] V2 Périmètre : `git diff --name-only origin/main...origin/tache/S35-T20-revue` ⊂ fichiers autorisés.
- [ ] V3.1 Contrôle T20-a relancé, résultat conforme.
- [ ] V3.2 Contrôle T20-b relancé, résultat conforme.
- [ ] V3.3 Contrôle T20-c relancé, résultat conforme.
- [ ] V3.4 Contrôle T20-d relancé, résultat conforme.
- [ ] V4 Contre-épreuves (CE) appliquées et détectées, puis annulées.
- [ ] V5 Contournements cherchés.
- [ ] V6 Cohérence avec les contrats et les invariants.
- [ ] V7 Verdict écrit dans `rapports/S35-verif-<tentative>.md` et poussé.

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

- [ ] F1 `git switch main && git pull --ff-only && git merge --no-ff origin/tache/S35-T20-revue -m "Fusion S35 : T20 Revue de continuation et décision"`.
- [ ] F2 Sur `main` : `GODOT="$B" tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK. Sinon : `git reset --hard ORIG_HEAD`, verdict « REFUSÉE (fusion) » poussé sur la branche, et arrêt de la fusion.
- [ ] F3 Dans `SUIVI.md`, cocher la ligne **S35** et compléter « fait le <date> · auteur <IA> · vérifié par <IA> · <n> créneaux ».
- [ ] F4 Inscrire la décision du POC dans `docs/DECISIONS.md`, au statut « adoptée par défaut ».
- [ ] F5 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette.
- [ ] F6 Cocher les sous-étapes F de cette fiche ; `git commit` ; `git push origin main` (en cas de refus : `git pull --rebase`, puis push).

## Pour la recette

- Confirmer la décision de continuer, et l'amendement PD-0.6.
