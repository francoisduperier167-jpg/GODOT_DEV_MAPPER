# S01 — 0.A Dossier de décisions

> Fiche d'exécution du mode autonome. Coche chaque case dès qu'elle est faite et prouvée, puis commite et pousse : une autre IA doit pouvoir reprendre à la première case non cochée. Règles : `docs/construction/sequence.md`. Avancement global : `SUIVI.md`.

| Champ | Valeur |
| --- | --- |
| Réalise | Concepteur |
| Vérifie | Vérificateur (jamais l'auteur) |
| Commence après | rien : peut commencer tout de suite |
| Indépendante de | aucune |
| Branche | `tache/S01-0A-decisions` |
| Fiche de conception | `docs/construction/etape-0.md`, section 0.A |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité elle-même peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Créer `docs/DECISIONS.md` : une ligne d'en-tête « Statut : proposé · date », puis un tableau de D-01 à D-09.
- Colonnes : ID, question, options (deux ou trois), recommandation, conséquences de chaque option, échéance, statut, date.
- Recommandations : D-01 Godot 4.7.2 ; D-03 trois IA, deux créneaux chacune par jour ; D-05 runner maison minimal ; D-07 4.7.2 bloquant, préversion 4.8-dev7 dans un job non bloquant ; D-09 mode autonome (fiches `suivi/`, recette humaine finale).
- D-02 : critères de choix du banc d'essai (Godot 4.x en GDScript, au moins deux types d'ennemis qui décident, 30 à 500 scripts, licences du code et des assets qui permettent de redistribuer une copie modifiée). Le banc vivra dans des branches `banc/<nom>-*` de ce dépôt. Le choix se fait en S07.
- Statuts : « adoptée par défaut » pour D-01, D-03, D-05, D-07 et D-09 ; « critères adoptés par défaut, choix en S07 » pour D-02 ; « proposée » pour D-04, D-06 et D-08.

## Fichiers autorisés

`docs/DECISIONS.md`

Toujours autorisés en plus : `rapports/S01*.md` et les cases de cette fiche.

## Contrôles propres à cette fiche

- `S01-a` : `for d in D-01 D-02 D-03 D-04 D-05 D-06 D-07 D-08 D-09; do c=$(grep -cE "^\| $d " docs/DECISIONS.md); [ "$c" = 1 ] || echo "$d : $c"; done` → aucune sortie
- `S01-b` : `for d in D-01 D-03 D-05 D-07 D-09; do grep -E "^\| $d " docs/DECISIONS.md | grep -q "adoptée par défaut" || echo "manque $d"; done` → aucune sortie
- `S01-c` : `grep -E "^\| D-0(4|6|8) " docs/DECISIONS.md | grep -c "proposée"` → 3
- (CE) Retirer « adoptée par défaut » de la ligne D-07, relancer S01-b : « manque D-07 » s'affiche ; annuler.

## Prompt de réalisation

```text
Tu es <ton nom d'IA>, au rôle Concepteur. Tu réalises l'unité S01 « 0.A Dossier de décisions » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.

AVANT TOUT
1. git fetch origin. Lis REGLES_AGENTS.md s'il existe, puis la fiche suivi/S01-0A-decisions.md.
2. Si la branche origin/tache/S01-0A-decisions existe : reprends-la, relis rapports/S01.md et commence à la première sous-étape R non cochée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
3. Sinon : crée tache/S01-0A-decisions depuis main (aucun prérequis).

GODOT
- Si tools/ci/fetch_godot.sh existe : B=$(tools/ci/fetch_godot.sh 4.7.2-stable)
- Sinon, hors du dépôt :
  D=$HOME/.cache/gdm-godot/4.7.2-stable ; mkdir -p "$D"
  test -x "$D/Godot_v4.7.2-stable_linux.x86_64" || { curl -sSL -o /tmp/godot-4.7.2.zip https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip && unzip -o -q /tmp/godot-4.7.2.zip -d "$D"; }
  B=$D/Godot_v4.7.2-stable_linux.x86_64
- « godot » dans les commandes désigne "$B". Contrôle : "$B" --version contient 4.7.2.stable.
- Éditeur avec rendu, quand la fiche le demande : xvfb-run -a -s "-screen 0 1600x900x24" "$B" --editor --path <projet> --rendering-driver opengl3

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S01.md et les cases de suivi/S01-0A-decisions.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu coches une case seulement quand elle est faite et prouvée. Tu commites et tu pousses après chaque case cochée.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (docs/construction/etape-0.md, 0.A)
Tu prépares les décisions de démarrage du projet GODOT_DEV_MAPPER. Tu ne décides rien.
Lis docs/plan-directeur.md (§0 et §10), docs/spikes/SPIKE-01.md et docs/construction/etape-0.md.
Crée docs/DECISIONS.md : un tableau avec ID, question, options (deux ou trois), recommandation, conséquences de chaque option, échéance, statut (« proposée »), date.
Couvre D-01 à D-08. Pour D-02, propose des critères de choix du banc d'essai, pas un jeu.
Avant de rendre, vérifie : chaque ID de D-01 à D-08 apparaît une seule fois ; chaque ligne a une recommandation ; aucune ligne n'est marquée « validée ».
Rapport : le chemin du fichier, puis les questions que je dois trancher, une par ligne, dans l'ordre de leur échéance.
TRAVAIL TECHNIQUE — fin de la copie exacte du guide

CONTRÔLES DE LA FICHE
S01-a  for d in D-01 D-02 D-03 D-04 D-05 D-06 D-07 D-08 D-09; do c=$(grep -cE "^\| $d " docs/DECISIONS.md); [ "$c" = 1 ] || echo "$d : $c"; done   → aucune sortie
S01-b  for d in D-01 D-03 D-05 D-07 D-09; do grep -E "^\| $d " docs/DECISIONS.md | grep -q "adoptée par défaut" || echo "manque $d"; done   → aucune sortie
S01-c  grep -E "^\| D-0(4|6|8) " docs/DECISIONS.md | grep -c "proposée"   → 3
(CE) Retirer « adoptée par défaut » de la ligne D-07, relancer S01-b : « manque D-07 » s'affiche ; annuler.

ADAPTATIONS DU MODE AUTONOME
- Le prompt du guide dit « Tu ne décides rien » et laisse toutes les lignes « proposée ». En mode autonome, tu inscris ensuite les statuts de la fiche : « adoptée par défaut » n'est pas « validée », la confirmation se fait à la recette.
- Ajoute D-09, absente du prompt du guide : mode d'exécution autonome, fiches `suivi/`, recette humaine finale.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche, et coche chacune.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Coche dans suivi/S01-0A-decisions.md les sous-étapes faites et prouvées ; complète rapports/S01.md (sorties, section « Passation ») ; commite ; git push origin tache/S01-0A-decisions.
- Ne laisse aucune modification non poussée.

FORMAT DE rapports/S01.md
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

- [ ] R0 Prise en charge : `git fetch origin` ; aucun prérequis ; branche `origin/tache/S01-0A-decisions` absente, ou sans commit depuis deux créneaux, ou dernier verdict REFUSÉE ; créer ou reprendre la branche ; `rapports/S01.md` avec « Statut : EN COURS » et « Auteur » ; commit ; push.
- [ ] R1 Lire `docs/plan-directeur.md` (§0 et §10), `docs/spikes/SPIKE-01.md`, `docs/construction/etape-0.md` (0.A) et `docs/construction/sequence.md`.
- [ ] R2 Écrire `docs/DECISIONS.md` : en-tête de statut, puis le tableau D-01 à D-09 avec toutes ses colonnes.
- [ ] R3 Appliquer les statuts de la section « Ce qu'il faut faire ».
- [ ] R4 Écrire dans le rapport la liste « Pour la recette » : chaque décision adoptée par défaut, une par ligne.
- [ ] R5 Contrôles finaux : S01-a, S01-b, S01-c exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » ; commit ; push.

## Prompt de vérification

```text
Tu es <ton nom d'IA>, au rôle Vérificateur, vérificateur indépendant de l'unité S01 « 0.A Dossier de décisions » du projet GODOT_DEV_MAPPER.
Tu n'en es pas l'auteur : lis la ligne « Auteur » de rapports/S01.md ; si c'est toi, arrête-toi.
Tu ne modifies aucun fichier de l'unité. Tu écris ton verdict et tu coches les sous-étapes V, sur la branche.

COPIE NEUVE : git fetch origin && git worktree add --detach ../verif-S01-0A-decisions origin/tache/S01-0A-decisions
GODOT : même procédure que le prompt de réalisation.

1. PÉRIMÈTRE. git diff --name-only origin/main...origin/tache/S01-0A-decisions. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S01*.md et suivi/S01-0A-decisions.md. Tout autre fichier : refus.
2. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : S01-a, S01-b, S01-c.
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
5. COHÉRENCE. Les recommandations reprennent le plan §0 et §10 et `docs/construction/etape-0.md` ; D-09 reprend `docs/construction/sequence.md`.

VERDICT dans rapports/S01-verif-<tentative>.md :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte
Pousse le verdict sur la branche. Si ACCEPTÉE, fais les sous-étapes F de la fiche. Si REFUSÉE, arrête-toi : une IA au rôle de l'auteur reprendra.
```

## Sous-étapes de vérification

- [ ] V1 Prise en charge : pas l'auteur ; copie neuve `../verif-S01-0A-decisions` sur `origin/tache/S01-0A-decisions`.
- [ ] V2 Périmètre : `git diff --name-only origin/main...origin/tache/S01-0A-decisions` ⊂ fichiers autorisés.
- [ ] V3.1 Contrôle S01-a relancé, résultat conforme.
- [ ] V3.2 Contrôle S01-b relancé, résultat conforme.
- [ ] V3.3 Contrôle S01-c relancé, résultat conforme.
- [ ] V4 Contre-épreuves (CE) appliquées et détectées, puis annulées.
- [ ] V5 Contournements cherchés.
- [ ] V6 Cohérence avec les contrats et les invariants.
- [ ] V7 Verdict écrit dans `rapports/S01-verif-<tentative>.md` et poussé.

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

- [ ] F1 `git switch main && git pull --ff-only && git merge --no-ff origin/tache/S01-0A-decisions -m "Fusion S01 : 0.A Dossier de décisions"`.
- [ ] F2 Sur `main` : `GODOT="$B" tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK. Sinon : `git reset --hard ORIG_HEAD`, verdict « REFUSÉE (fusion) » poussé sur la branche, et arrêt de la fusion.
- [ ] F3 Dans `SUIVI.md`, cocher la ligne **S01** et compléter « fait le <date> · auteur <IA> · vérifié par <IA> · <n> créneaux ».
- [ ] F4 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette.
- [ ] F5 Cocher les sous-étapes F de cette fiche ; `git commit` ; `git push origin main` (en cas de refus : `git pull --rebase`, puis push).

## Pour la recette

- Confirmer ou changer chaque décision « adoptée par défaut ».
