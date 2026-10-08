# S27 — Porte de l'étape 5

> Fiche d'exécution du mode autonome. Coche chaque case dès qu'elle est faite et prouvée, puis commite et pousse : une autre IA doit pouvoir reprendre à la première case non cochée. Règles : `docs/construction/sequence.md`. Avancement global : `SUIVI.md`.

| Champ | Valeur |
| --- | --- |
| Réalise | Concepteur |
| Vérifie | Vérificateur (jamais l'auteur) |
| Commence après | S23, S26 (cochées dans `SUIVI.md`) |
| Indépendante de | S28, S29, S30, S31, S33 |
| Branche | `tache/S27-porte-5` |
| Fiche de conception | `docs/construction/etape-5.md`, points de contrôle |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité elle-même peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Exécuter chaque point de contrôle de l'étape 5 sur `main` à jour, et noter commande, attendu, obtenu, OK ou KO.
- Décider selon la règle : **passer** si tout est OK (un point « sur ta machine » passe par son équivalent sous écran virtuel, l'humain le revoit à la recette) ; **corriger d'abord** si un point est KO.
- Si un point est KO : ne pas cocher la porte ; écrire dans le rapport la correction attendue et l'unité fautive ; à la fusion du verdict, le vérificateur ajoute sous la porte, dans `SUIVI.md`, une ligne « S27.c1 Correction : … » (réalise : rôle de l'unité fautive ; après : rien) et crée sa fiche depuis `suivi/_modele-correction.md`.

## Fichiers autorisés

`rapports/S27.md`.

## Points de contrôle de l'étape (copie du guide)

| ID | Contrôle | Commande ou preuve | Attendu | Adaptation |
| --- | --- | --- | --- | --- |
| PC5.1 | Contrôleur de session | Runner | Tests du contrôleur verts sur toutes les sessions enregistrées | — |
| PC5.2 | Passerelle chargée | Contrôle PC1.2 étendu au marqueur `GDM_BRIDGE_READY` | Présent, aucune ligne d'erreur | — |
| PC5.3 | Banc d'essai sans débogueur | Jeu lancé sans `--remote-debug` | Aucune ligne d'erreur ; FlowTrace inerte | — |
| PC5.4 | Banc d'essai avec le banc de test | `tests/integration/run_bench.sh`, rejoué par `checks.d/55-bench.sh` | Clés attendues, deux instances distinctes, aucune destruction après réinsertion ; à la porte, OK et jamais IGNORÉ | — |
| PC5.5 | Clés orphelines | `python3 tools/check_probe_keys.py` | Code 0 | — |
| PC5.6 | Essai dans l'éditeur réel | Sur ta machine : une session du banc d'essai jusqu'au store | Compteurs cohérents avec le banc de test | Preuve : le verdict ACCEPTÉE de S26, sous écran virtuel. L'essai sur ta machine passe à la recette. |

## Prompt de réalisation

```text
Tu es <ton nom d'IA>, au rôle Concepteur. Tu réalises l'unité S27 « Porte de l'étape 5 » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.

AVANT TOUT
1. git fetch origin. Lis REGLES_AGENTS.md s'il existe, puis la fiche suivi/S27-porte-5.md.
2. Si la branche origin/tache/S27-porte-5 existe : reprends-la, relis rapports/S27.md et commence à la première sous-étape R non cochée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
3. Sinon : vérifie dans SUIVI.md, sur main, que S23, S26 sont cochées, puis crée tache/S27-porte-5 depuis main.

GODOT
- Si tools/ci/fetch_godot.sh existe : B=$(tools/ci/fetch_godot.sh 4.7.2-stable)
- Sinon, hors du dépôt :
  D=$HOME/.cache/gdm-godot/4.7.2-stable ; mkdir -p "$D"
  test -x "$D/Godot_v4.7.2-stable_linux.x86_64" || { curl -sSL -o /tmp/godot-4.7.2.zip https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip && unzip -o -q /tmp/godot-4.7.2.zip -d "$D"; }
  B=$D/Godot_v4.7.2-stable_linux.x86_64
- « godot » dans les commandes désigne "$B". Contrôle : "$B" --version contient 4.7.2.stable.
- Éditeur avec rendu, quand la fiche le demande : xvfb-run -a -s "-screen 0 1600x900x24" "$B" --editor --path <projet> --rendering-driver opengl3

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S27.md et les cases de suivi/S27-porte-5.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu coches une case seulement quand elle est faite et prouvée. Tu commites et tu pousses après chaque case cochée.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (docs/construction/README.md, prompt de porte d'étape)
Prépare la porte de sortie de l'étape 5 du projet GODOT_DEV_MAPPER. Entrées : docs/construction/etape-5.md, les verdicts de vérification de chaque tâche, PROJECT_STATE.md.
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
- PC5.6 : Preuve : le verdict ACCEPTÉE de S26, sous écran virtuel. L'essai sur ta machine passe à la recette.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche, et coche chacune.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Coche dans suivi/S27-porte-5.md les sous-étapes faites et prouvées ; complète rapports/S27.md (sorties, section « Passation ») ; commite ; git push origin tache/S27-porte-5.
- Ne laisse aucune modification non poussée.

FORMAT DE rapports/S27.md
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

- [ ] R0 Prise en charge : `git fetch origin` ; S23, S26 sont cochées dans `SUIVI.md` ; branche `origin/tache/S27-porte-5` absente, ou sans commit depuis deux créneaux, ou dernier verdict REFUSÉE ; créer ou reprendre la branche ; `rapports/S27.md` avec « Statut : EN COURS » et « Auteur » ; commit ; push.
- [ ] R1 PC5.1 exécuté et noté (adaptation de la fiche s'il y en a une).
- [ ] R2 PC5.2 exécuté et noté (adaptation de la fiche s'il y en a une).
- [ ] R3 PC5.3 exécuté et noté (adaptation de la fiche s'il y en a une).
- [ ] R4 PC5.4 exécuté et noté (adaptation de la fiche s'il y en a une).
- [ ] R5 PC5.5 exécuté et noté (adaptation de la fiche s'il y en a une).
- [ ] R6 PC5.6 exécuté et noté (adaptation de la fiche s'il y en a une).
- [ ] R7 Décision écrite dans le rapport : passer, ou corriger d'abord avec l'unité fautive.
- [ ] R8 « Statut : TERMINÉ » ; commit ; push.

## Prompt de vérification

```text
Tu es <ton nom d'IA>, au rôle Vérificateur, vérificateur indépendant de l'unité S27 « Porte de l'étape 5 » du projet GODOT_DEV_MAPPER.
Tu n'en es pas l'auteur : lis la ligne « Auteur » de rapports/S27.md ; si c'est toi, arrête-toi.
Tu ne modifies aucun fichier de l'unité. Tu écris ton verdict et tu coches les sous-étapes V, sur la branche.

COPIE NEUVE : git fetch origin && git worktree add --detach ../verif-S27-porte-5 origin/tache/S27-porte-5
GODOT : même procédure que le prompt de réalisation.

1. PÉRIMÈTRE. git diff --name-only origin/main...origin/tache/S27-porte-5. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S27*.md et suivi/S27-porte-5.md. Tout autre fichier : refus.
2. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : PC5.1, PC5.2, PC5.3, PC5.4, PC5.5, PC5.6.
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

VERDICT dans rapports/S27-verif-<tentative>.md :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte
Pousse le verdict sur la branche. Si ACCEPTÉE, fais les sous-étapes F de la fiche. Si REFUSÉE, arrête-toi : une IA au rôle de l'auteur reprendra.
```

## Sous-étapes de vérification

- [ ] V1 Prise en charge : pas l'auteur ; copie neuve sur `origin/tache/S27-porte-5`.
- [ ] V2.1 PC5.1 relancé ou sa preuve vérifiée.
- [ ] V2.2 PC5.2 relancé ou sa preuve vérifiée.
- [ ] V2.3 PC5.3 relancé ou sa preuve vérifiée.
- [ ] V2.4 PC5.4 relancé ou sa preuve vérifiée.
- [ ] V2.5 PC5.5 relancé ou sa preuve vérifiée.
- [ ] V2.6 PC5.6 relancé ou sa preuve vérifiée.
- [ ] V3 Décision conforme à la règle.
- [ ] V4 Verdict écrit dans `rapports/S27-verif-<tentative>.md` et poussé.

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

- [ ] F1 `git switch main && git pull --ff-only && git merge --no-ff origin/tache/S27-porte-5 -m "Fusion S27 : Porte de l'étape 5"`.
- [ ] F2 Sur `main` : `GODOT="$B" tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK. Sinon : `git reset --hard ORIG_HEAD`, verdict « REFUSÉE (fusion) » poussé sur la branche, et arrêt de la fusion.
- [ ] F3 Dans `SUIVI.md`, cocher la ligne **S27** et compléter « fait le <date> · auteur <IA> · vérifié par <IA> · <n> créneaux ».
- [ ] F4 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette.
- [ ] F5 Cocher les sous-étapes F de cette fiche ; `git commit` ; `git push origin main` (en cas de refus : `git pull --rebase`, puis push).

## Pour la recette

Rien de propre à cette unité.
