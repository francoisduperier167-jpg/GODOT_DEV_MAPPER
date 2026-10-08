# S31 — Démonstration sous écran virtuel (PC6.7)

> Fiche d'exécution du mode autonome. Coche chaque case dès qu'elle est faite et prouvée, puis commite et pousse : une autre IA doit pouvoir reprendre à la première case non cochée. Règles : `docs/construction/sequence.md`. Avancement global : `SUIVI.md`.

| Champ | Valeur |
| --- | --- |
| Réalise | Développeur |
| Vérifie | Vérificateur (jamais l'auteur) |
| Commence après | S28, S29, S30 (cochées dans `SUIVI.md`) |
| Indépendante de | S22, S23, S26, S27, S33 |
| Branche | `tache/S31-demonstration` |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité elle-même peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Sous écran virtuel, ouvrir l'éditeur avec le plugin sur le banc instrumenté, jouer une session, et produire des captures du panneau : deux instances distinguées, trois états du chemin observé, ouverture du code à la bonne ligne.
- Mesurer l'aller-retour et le délai réception → affichage, marqués « rendu logiciel ».

## Fichiers autorisés

`tests/integration/run_demo.sh`, `tools/harness/editor_driver/` (scénario de démonstration), `rapports/S31/` (captures PNG), `docs/mesures/latence-poc.md`.

Toujours autorisés en plus : `rapports/S31*.md` et les cases de cette fiche.

## Contrôles propres à cette fiche

- `S31-a` : `tests/integration/run_demo.sh; echo $?` → 0 et une ligne OPEN avec la ligne de l'ancrage
- `S31-b` : `ls rapports/S31/*.png | wc -l` → au moins 4
- (CE) Ignorer le filtre d'instance dans la projection : le test de projection échoue et la capture ne distingue plus les instances ; annuler.

## Prompt de réalisation

```text
Tu es <ton nom d'IA>, au rôle Développeur. Tu réalises l'unité S31 « Démonstration sous écran virtuel (PC6.7) » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.

AVANT TOUT
1. git fetch origin. Lis REGLES_AGENTS.md s'il existe, puis la fiche suivi/S31-demonstration.md.
2. Si la branche origin/tache/S31-demonstration existe : reprends-la, relis rapports/S31.md et commence à la première sous-étape R non cochée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
3. Sinon : vérifie dans SUIVI.md, sur main, que S28, S29, S30 sont cochées, puis crée tache/S31-demonstration depuis main.

GODOT
- Si tools/ci/fetch_godot.sh existe : B=$(tools/ci/fetch_godot.sh 4.7.2-stable)
- Sinon, hors du dépôt :
  D=$HOME/.cache/gdm-godot/4.7.2-stable ; mkdir -p "$D"
  test -x "$D/Godot_v4.7.2-stable_linux.x86_64" || { curl -sSL -o /tmp/godot-4.7.2.zip https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip && unzip -o -q /tmp/godot-4.7.2.zip -d "$D"; }
  B=$D/Godot_v4.7.2-stable_linux.x86_64
- « godot » dans les commandes désigne "$B". Contrôle : "$B" --version contient 4.7.2.stable.
- Éditeur avec rendu, quand la fiche le demande : xvfb-run -a -s "-screen 0 1600x900x24" "$B" --editor --path <projet> --rendering-driver opengl3

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S31.md et les cases de suivi/S31-demonstration.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu coches une case seulement quand elle est faite et prouvée. Tu commites et tu pousses après chaque case cochée.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (rédigé pour le mode autonome)
Tu réalises la démonstration PC6.7 du projet GODOT_DEV_MAPPER, sans humain, sous écran virtuel.
CONTEXTE : docs/construction/etape-6.md (PC6.7, T16, T17), rapports de S28 et S29 (procédures), tools/harness/editor_driver/ (S26).
OBJECTIF
1. Étendre tools/harness/editor_driver/ : une fois la session reçue, sélectionner chaque instance, choisir une invocation, ouvrir le code par le panneau, et capturer le viewport de l'éditeur (get_viewport().get_texture().get_image().save_png) dans rapports/S31/.
2. tests/integration/run_demo.sh : lance tout sous xvfb-run, sur une copie temporaire de banc/<nom>-instrumentation, et affiche la ligne de script ouverte par l'éditeur (« OPEN res://…:ligne »).
3. Captures attendues : deux instances distinguées ; un chemin « cohérent », un « indéterminé — trace incomplète » (session à trou rejouée), un « incohérent » (fixture) ; le code ouvert à la ligne de l'ancrage.
4. docs/mesures/latence-poc.md : aller-retour et délai réception → affichage, 95e centile sur la session, latence estimée ; mention « rendu logiciel, non représentatif d'un GPU ».
CONTRÔLES
S31-a  tests/integration/run_demo.sh ; echo $?   → 0 et une ligne OPEN avec la ligne de l'ancrage
S31-b  ls rapports/S31/*.png | wc -l   → au moins 4
CONTRE-ÉPREUVE (CE) pour le vérificateur : faire ignorer le filtre d'instance au panneau → la capture des deux instances ne les distingue plus, et le test de projection échoue.
TRAVAIL TECHNIQUE — fin de la copie exacte du guide

CONTRÔLES DE LA FICHE
S31-a  tests/integration/run_demo.sh; echo $?   → 0 et une ligne OPEN avec la ligne de l'ancrage
S31-b  ls rapports/S31/*.png | wc -l   → au moins 4
(CE) Ignorer le filtre d'instance dans la projection : le test de projection échoue et la capture ne distingue plus les instances ; annuler.

ADAPTATIONS DU MODE AUTONOME
- Aucune : suis le travail technique tel quel.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche, et coche chacune.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Coche dans suivi/S31-demonstration.md les sous-étapes faites et prouvées ; complète rapports/S31.md (sorties, section « Passation ») ; commite ; git push origin tache/S31-demonstration.
- Ne laisse aucune modification non poussée.

FORMAT DE rapports/S31.md
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

- [ ] R0 Prise en charge : `git fetch origin` ; S28, S29, S30 sont cochées dans `SUIVI.md` ; branche `origin/tache/S31-demonstration` absente, ou sans commit depuis deux créneaux, ou dernier verdict REFUSÉE ; créer ou reprendre la branche ; `rapports/S31.md` avec « Statut : EN COURS » et « Auteur » ; commit ; push.
- [ ] R1 Étendre `tools/harness/editor_driver/` : sélection d'instance, choix d'une invocation, ouverture du code, capture du viewport de l'éditeur.
- [ ] R2 Écrire `tests/integration/run_demo.sh`.
- [ ] R3 Produire les captures dans `rapports/S31/` : deux instances, trois états (fixtures « cohérent », « trou », « incohérent »), code ouvert à la bonne ligne.
- [ ] R4 Écrire `docs/mesures/latence-poc.md` : aller-retour, délai réception → affichage, 95e centile, mention « rendu logiciel ».
- [ ] R5 Contrôles finaux : S31-a, S31-b exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » ; commit ; push.

## Prompt de vérification

```text
Tu es <ton nom d'IA>, au rôle Vérificateur, vérificateur indépendant de l'unité S31 « Démonstration sous écran virtuel (PC6.7) » du projet GODOT_DEV_MAPPER.
Tu n'en es pas l'auteur : lis la ligne « Auteur » de rapports/S31.md ; si c'est toi, arrête-toi.
Tu ne modifies aucun fichier de l'unité. Tu écris ton verdict et tu coches les sous-étapes V, sur la branche.

COPIE NEUVE : git fetch origin && git worktree add --detach ../verif-S31-demonstration origin/tache/S31-demonstration
GODOT : même procédure que le prompt de réalisation.

1. PÉRIMÈTRE. git diff --name-only origin/main...origin/tache/S31-demonstration. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S31*.md et suivi/S31-demonstration.md. Tout autre fichier : refus.
2. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : S31-a, S31-b.
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
5. COHÉRENCE. Plan §7 (pas de graphe dessiné au POC) ; états jamais portés par la seule couleur ; jamais « cause ».
Le vérificateur ouvre chaque capture et décrit ce qu'il voit dans son verdict.

VERDICT dans rapports/S31-verif-<tentative>.md :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte
Pousse le verdict sur la branche. Si ACCEPTÉE, fais les sous-étapes F de la fiche. Si REFUSÉE, arrête-toi : une IA au rôle de l'auteur reprendra.
```

## Sous-étapes de vérification

- [ ] V1 Prise en charge : pas l'auteur ; copie neuve `../verif-S31-demonstration` sur `origin/tache/S31-demonstration`.
- [ ] V2 Périmètre : `git diff --name-only origin/main...origin/tache/S31-demonstration` ⊂ fichiers autorisés.
- [ ] V3.1 Contrôle S31-a relancé, résultat conforme.
- [ ] V3.2 Contrôle S31-b relancé, résultat conforme.
- [ ] V4 Contre-épreuves (CE) appliquées et détectées, puis annulées.
- [ ] V5 Contournements cherchés.
- [ ] V6 Cohérence avec les contrats et les invariants.
- [ ] V7 Verdict écrit dans `rapports/S31-verif-<tentative>.md` et poussé.

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

- [ ] F1 `git switch main && git pull --ff-only && git merge --no-ff origin/tache/S31-demonstration -m "Fusion S31 : Démonstration sous écran virtuel (PC6.7)"`.
- [ ] F2 Sur `main` : `GODOT="$B" tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK. Sinon : `git reset --hard ORIG_HEAD`, verdict « REFUSÉE (fusion) » poussé sur la branche, et arrêt de la fusion.
- [ ] F3 Dans `SUIVI.md`, cocher la ligne **S31** et compléter « fait le <date> · auteur <IA> · vérifié par <IA> · <n> créneaux ».
- [ ] F4 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette.
- [ ] F5 Cocher les sous-étapes F de cette fiche ; `git commit` ; `git push origin main` (en cas de refus : `git pull --rebase`, puis push).

## Pour la recette

- Démonstration et latence sur ta machine, avec GPU ; jugement visuel du panneau.
