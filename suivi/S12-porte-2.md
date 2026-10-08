# S12 — Porte de l'étape 2

> Fiche d'exécution du mode autonome. Coche chaque case dès qu'elle est faite et prouvée, puis commite et pousse : une autre IA doit pouvoir reprendre à la première case non cochée. Règles : `docs/construction/sequence.md`. Avancement global : `SUIVI.md`.

| Champ | Valeur |
| --- | --- |
| Réalise | Concepteur |
| Vérifie | Vérificateur (jamais l'auteur) |
| Commence après | S09, S10, S11 (cochées dans `SUIVI.md`) |
| Indépendante de | S13 |
| Branche | `tache/S12-porte-2` |
| Fiche de conception | `docs/construction/etape-2.md`, points de contrôle |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité elle-même peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Exécuter chaque point de contrôle de l'étape 2 sur `main` à jour, et noter commande, attendu, obtenu, OK ou KO.
- Décider selon la règle : **passer** si tout est OK (un point « sur ta machine » passe par son équivalent sous écran virtuel, l'humain le revoit à la recette) ; **corriger d'abord** si un point est KO.
- Si un point est KO : ne pas cocher la porte ; écrire dans le rapport la correction attendue et l'unité fautive ; à la fusion du verdict, le vérificateur ajoute sous la porte, dans `SUIVI.md`, une ligne « S12.c1 Correction : … » (réalise : rôle de l'unité fautive ; après : rien) et crée sa fiche depuis `suivi/_modele-correction.md`.

## Fichiers autorisés

`rapports/S12.md`.

## Points de contrôle de l'étape (copie du guide)

| ID | Contrôle | Commande ou preuve | Attendu | Adaptation |
| --- | --- | --- | --- | --- |
| PC2.1 | Partie éditeur du canal | Section SPIKE-01b de `docs/spikes/SPIKE-01.md` | Six critères marqués atteint ou non, chacun avec sa preuve | — |
| PC2.2 | Frontière de compatibilité | `docs/spikes/SPIKE-02.md` | Quatre questions, chacune avec commande et sortie sur les deux versions | — |
| PC2.3 | Reproductibilité | `spikes/spike02_compat/run.sh`, relancé par le vérificateur | Mêmes conclusions | — |
| PC2.4 | Décisions consignées | `docs/DECISIONS.md` | KEEP, REWRITE ou DISCARD pour chaque spike | Les décisions KEEP, REWRITE ou DISCARD ont été inscrites à la fusion de S10 et de S11, au statut « adoptée par défaut » : vérifier leur présence. |
| PC2.5 | Plan à jour | Diff proposé de `docs/plan-directeur.md` | Validé par toi, ou « aucun changement » justifié | Diff proposé du plan : appliqué au statut « proposé » si les spikes l'exigent, ou « aucun changement » justifié ; à confirmer à la recette. |
| PC2.6 | Isolation des spikes | `grep -rn "spikes/" addons` | Aucune ligne | — |

## Prompt de réalisation

```text
Tu es <ton nom d'IA>, au rôle Concepteur. Tu réalises l'unité S12 « Porte de l'étape 2 » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.

AVANT TOUT
1. git fetch origin. Lis REGLES_AGENTS.md s'il existe, puis la fiche suivi/S12-porte-2.md.
2. Si la branche origin/tache/S12-porte-2 existe : reprends-la, relis rapports/S12.md et commence à la première sous-étape R non cochée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
3. Sinon : vérifie dans SUIVI.md, sur main, que S09, S10, S11 sont cochées, puis crée tache/S12-porte-2 depuis main.

GODOT
- Si tools/ci/fetch_godot.sh existe : B=$(tools/ci/fetch_godot.sh 4.7.2-stable)
- Sinon, hors du dépôt :
  D=$HOME/.cache/gdm-godot/4.7.2-stable ; mkdir -p "$D"
  test -x "$D/Godot_v4.7.2-stable_linux.x86_64" || { curl -sSL -o /tmp/godot-4.7.2.zip https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip && unzip -o -q /tmp/godot-4.7.2.zip -d "$D"; }
  B=$D/Godot_v4.7.2-stable_linux.x86_64
- « godot » dans les commandes désigne "$B". Contrôle : "$B" --version contient 4.7.2.stable.
- Éditeur avec rendu, quand la fiche le demande : xvfb-run -a -s "-screen 0 1600x900x24" "$B" --editor --path <projet> --rendering-driver opengl3

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S12.md et les cases de suivi/S12-porte-2.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu coches une case seulement quand elle est faite et prouvée. Tu commites et tu pousses après chaque case cochée.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (docs/construction/README.md, prompt de porte d'étape)
Prépare la porte de sortie de l'étape 2 du projet GODOT_DEV_MAPPER. Entrées : docs/construction/etape-2.md, les verdicts de vérification de chaque tâche, PROJECT_STATE.md.
Pour les points de contrôle couverts par tools/ci/run_all_checks.sh, exécute ce script une fois sur main : son résultat fait foi. Exécute toi-même les autres points de contrôle de l'étape, puis produis une page :
- tableau : point de contrôle, commande, attendu, obtenu, OK ou KO ;
- heures humaines et temps agent consommés, contre le budget de l'étape ;
- problèmes ouverts et risques nouveaux ;
- recommandation : passer, corriger d'abord, ou revoir le plan.
Tu ne décides pas : la décision est humaine.
TRAVAIL TECHNIQUE — fin de la copie exacte du guide

ADAPTATIONS DU MODE AUTONOME
- « Tu ne décides pas » : en mode autonome, tu appliques la règle de décision de la fiche (passer ou corriger d'abord).
- Budget : en créneaux d'IA, comparés à l'estimation de docs/construction/sequence.md (§8). Au-delà de 50 % de dépassement, écris une revue courte dans docs/revues/ et continue, sauf arrêt obligatoire.
- PC2.4 : Les décisions KEEP, REWRITE ou DISCARD ont été inscrites à la fusion de S10 et de S11, au statut « adoptée par défaut » : vérifier leur présence.
- PC2.5 : Diff proposé du plan : appliqué au statut « proposé » si les spikes l'exigent, ou « aucun changement » justifié ; à confirmer à la recette.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche, et coche chacune.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Coche dans suivi/S12-porte-2.md les sous-étapes faites et prouvées ; complète rapports/S12.md (sorties, section « Passation ») ; commite ; git push origin tache/S12-porte-2.
- Ne laisse aucune modification non poussée.

FORMAT DE rapports/S12.md
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

- [ ] R0 Prise en charge : `git fetch origin` ; S09, S10, S11 sont cochées dans `SUIVI.md` ; branche `origin/tache/S12-porte-2` absente, ou sans commit depuis deux créneaux, ou dernier verdict REFUSÉE ; créer ou reprendre la branche ; `rapports/S12.md` avec « Statut : EN COURS » et « Auteur » ; commit ; push.
- [ ] R1 PC2.1 exécuté et noté (adaptation de la fiche s'il y en a une).
- [ ] R2 PC2.2 exécuté et noté (adaptation de la fiche s'il y en a une).
- [ ] R3 PC2.3 exécuté et noté (adaptation de la fiche s'il y en a une).
- [ ] R4 PC2.4 exécuté et noté (adaptation de la fiche s'il y en a une).
- [ ] R5 PC2.5 exécuté et noté (adaptation de la fiche s'il y en a une).
- [ ] R6 PC2.6 exécuté et noté (adaptation de la fiche s'il y en a une).
- [ ] R7 Décision écrite dans le rapport : passer, ou corriger d'abord avec l'unité fautive.
- [ ] R8 « Statut : TERMINÉ » ; commit ; push.

## Prompt de vérification

```text
Tu es <ton nom d'IA>, au rôle Vérificateur, vérificateur indépendant de l'unité S12 « Porte de l'étape 2 » du projet GODOT_DEV_MAPPER.
Tu n'en es pas l'auteur : lis la ligne « Auteur » de rapports/S12.md ; si c'est toi, arrête-toi.
Tu ne modifies aucun fichier de l'unité. Tu écris ton verdict et tu coches les sous-étapes V, sur la branche.

COPIE NEUVE : git fetch origin && git worktree add --detach ../verif-S12-porte-2 origin/tache/S12-porte-2
GODOT : même procédure que le prompt de réalisation.

1. PÉRIMÈTRE. git diff --name-only origin/main...origin/tache/S12-porte-2. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S12*.md et suivi/S12-porte-2.md. Tout autre fichier : refus.
2. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : PC2.1, PC2.2, PC2.3, PC2.4, PC2.5, PC2.6.
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
5. COHÉRENCE. Contrat et invariants concernés.
Relance chaque point automatisable toi-même ; pour les autres, vérifie la preuve citée. La décision suit-elle la règle ?

VERDICT dans rapports/S12-verif-<tentative>.md :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte
Pousse le verdict sur la branche. Si ACCEPTÉE, fais les sous-étapes F de la fiche. Si REFUSÉE, arrête-toi : une IA au rôle de l'auteur reprendra.
```

## Sous-étapes de vérification

- [ ] V1 Prise en charge : pas l'auteur ; copie neuve sur `origin/tache/S12-porte-2`.
- [ ] V2.1 PC2.1 relancé ou sa preuve vérifiée.
- [ ] V2.2 PC2.2 relancé ou sa preuve vérifiée.
- [ ] V2.3 PC2.3 relancé ou sa preuve vérifiée.
- [ ] V2.4 PC2.4 relancé ou sa preuve vérifiée.
- [ ] V2.5 PC2.5 relancé ou sa preuve vérifiée.
- [ ] V2.6 PC2.6 relancé ou sa preuve vérifiée.
- [ ] V3 Décision conforme à la règle.
- [ ] V4 Verdict écrit dans `rapports/S12-verif-<tentative>.md` et poussé.

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

- [ ] F1 `git switch main && git pull --ff-only && git merge --no-ff origin/tache/S12-porte-2 -m "Fusion S12 : Porte de l'étape 2"`.
- [ ] F2 Sur `main` : `GODOT="$B" tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK. Sinon : `git reset --hard ORIG_HEAD`, verdict « REFUSÉE (fusion) » poussé sur la branche, et arrêt de la fusion.
- [ ] F3 Dans `SUIVI.md`, cocher la ligne **S12** et compléter « fait le <date> · auteur <IA> · vérifié par <IA> · <n> créneaux ».
- [ ] F4 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette.
- [ ] F5 Cocher les sous-étapes F de cette fiche ; `git commit` ; `git push origin main` (en cas de refus : `git pull --rebase`, puis push).

## Pour la recette

Rien de propre à cette unité.
