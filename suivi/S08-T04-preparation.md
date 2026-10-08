# S08 — T04 Préparation du banc d'essai

> Fiche d'exécution du mode autonome. Coche chaque case dès qu'elle est faite et prouvée, puis commite et pousse : une autre IA doit pouvoir reprendre à la première case non cochée. Règles : `docs/construction/sequence.md`. Avancement global : `SUIVI.md`.

| Champ | Valeur |
| --- | --- |
| Réalise | Développeur |
| Vérifie | Vérificateur (jamais l'auteur) |
| Commence après | S04, S07 (cochées dans `SUIVI.md`) |
| Indépendante de | S05, S06, S10, S11 |
| Branche | `tache/S08-T04-preparation` |
| Fiche de conception | `docs/construction/etape-1.md`, section T04 |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité elle-même peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Copier le jeu retenu, à sa révision épinglée, dans une branche orpheline `banc/<nom>-base` de ce dépôt (licences et fichiers LICENSE intacts), puis la pousser.
- L'importer avec Godot 4.7.2 et corriger seulement ce que la migration exige, une correction par commit, la raison dans le message.
- Sur la branche de la tâche : `benches/benches.json`, `tools/check_benches.py`, `docs/benches/<nom>.md`.

## Fichiers autorisés

Sur `tache/S08-T04-preparation` : `benches/benches.json`, `docs/benches/<nom>.md`, `tools/check_benches.py`. Hors de `main` : la branche orpheline `banc/<nom>-base`.

Toujours autorisés en plus : `rapports/S08*.md` et les cases de cette fiche.

## Prompt de réalisation

```text
Tu es <ton nom d'IA>, au rôle Développeur. Tu réalises l'unité S08 « T04 Préparation du banc d'essai » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.

AVANT TOUT
1. git fetch origin. Lis REGLES_AGENTS.md s'il existe, puis la fiche suivi/S08-T04-preparation.md.
2. Si la branche origin/tache/S08-T04-preparation existe : reprends-la, relis rapports/S08.md et commence à la première sous-étape R non cochée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
3. Sinon : vérifie dans SUIVI.md, sur main, que S04, S07 sont cochées, puis crée tache/S08-T04-preparation depuis main.

GODOT
- Si tools/ci/fetch_godot.sh existe : B=$(tools/ci/fetch_godot.sh 4.7.2-stable)
- Sinon, hors du dépôt :
  D=$HOME/.cache/gdm-godot/4.7.2-stable ; mkdir -p "$D"
  test -x "$D/Godot_v4.7.2-stable_linux.x86_64" || { curl -sSL -o /tmp/godot-4.7.2.zip https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip && unzip -o -q /tmp/godot-4.7.2.zip -d "$D"; }
  B=$D/Godot_v4.7.2-stable_linux.x86_64
- « godot » dans les commandes désigne "$B". Contrôle : "$B" --version contient 4.7.2.stable.
- Éditeur avec rendu, quand la fiche le demande : xvfb-run -a -s "-screen 0 1600x900x24" "$B" --editor --path <projet> --rendering-driver opengl3

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S08.md et les cases de suivi/S08-T04-preparation.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu coches une case seulement quand elle est faite et prouvée. Tu commites et tu pousses après chaque case cochée.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (docs/construction/etape-1.md, T04)
Tu prépares le banc d'essai retenu pour le projet GODOT_DEV_MAPPER : {nom}, dépôt {url}, révision {sha}.
1. Clone-le hors du dépôt, dans ../benches/{nom}, puis crée la branche gdm-base.
2. Importe-le avec Godot 4.7.2 : godot --headless --path ../benches/{nom} --import > /tmp/bench.out 2>&1
   Corrige seulement ce que la migration exige. Chaque correction fait un commit séparé, avec la raison dans le message.
3. Écris benches/benches.json : nom, dépôt, révision d'origine, révision migrée, licences du code et des assets, version de Godot d'origine, scripts des décisions ciblées.
4. Écris tools/check_benches.py : il vérifie que benches.json est un JSON valide avec ces clés, et qu'aucun fichier .gd ni aucun asset du jeu n'est suivi par Git dans ce dépôt.
5. Écris docs/benches/{nom}.md : la fiche du jeu, les décisions observables, les corrections de migration.
CONTRÔLES
T04-a  python3 tools/check_benches.py ; echo $?                                          → 0
T04-b  grep -cE "^(ERROR|SCRIPT ERROR)" /tmp/bench.out après la migration                 → 0, ou erreurs listées et justifiées dans la fiche
T04-c  (CE) copie temporairement un .gd du jeu dans benches/ et ajoute-le à Git : T04-a → 1 ; annule
TRAVAIL TECHNIQUE — fin de la copie exacte du guide

ADAPTATIONS DU MODE AUTONOME
- Le guide clone le jeu hors du dépôt, branche `gdm-base`. En mode autonome, chaque IA arrive dans un environnement neuf : la copie vit dans la branche orpheline `banc/<nom>-base` de ce dépôt, jamais sur `main`. Pour la retrouver : `git fetch origin banc/<nom>-base && git worktree add ../benches/<nom> origin/banc/<nom>-base`.
- Partout où le guide écrit `../benches/{nom}` ou `gdm-base`, lire la copie de travail de `banc/<nom>-base`.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche, et coche chacune.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Coche dans suivi/S08-T04-preparation.md les sous-étapes faites et prouvées ; complète rapports/S08.md (sorties, section « Passation ») ; commite ; git push origin tache/S08-T04-preparation.
- Ne laisse aucune modification non poussée.

FORMAT DE rapports/S08.md
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

- [ ] R0 Prise en charge : `git fetch origin` ; S04, S07 sont cochées dans `SUIVI.md` ; branche `origin/tache/S08-T04-preparation` absente, ou sans commit depuis deux créneaux, ou dernier verdict REFUSÉE ; créer ou reprendre la branche ; `rapports/S08.md` avec « Statut : EN COURS » et « Auteur » ; commit ; push.
- [ ] R1 Relire D-02 et `docs/benches/selection.md` ; noter le nom court `<nom>`.
- [ ] R2 Obtenir Godot 4.7.2.
- [ ] R3 Créer la copie de travail du banc : `git worktree add --detach ../benches/<nom>`, puis dans ce dossier `git checkout --orphan banc/<nom>-base && git rm -rfq .` ; y copier le jeu à la révision épinglée (sans son `.git`) ; commit « Copie de <dépôt>@<SHA> » ; `git push origin banc/<nom>-base`.
- [ ] R4 Importer : `godot --headless --path ../benches/<nom> --import > /tmp/bench.out 2>&1` ; corriger la migration, un commit par correction ; pousser `banc/<nom>-base`.
- [ ] R5 Écrire `benches/benches.json` : nom, dépôt, révision d'origine, branche `banc/<nom>-base`, révision migrée, licences, version de Godot d'origine, scripts des décisions ciblées.
- [ ] R6 Écrire `tools/check_benches.py` (JSON valide avec ces clés ; aucun fichier du jeu suivi par Git sur la branche courante hors de `banc/*`).
- [ ] R7 Écrire `docs/benches/<nom>.md` : fiche du jeu, décisions observables, corrections de migration.
- [ ] R8 Faire la contre-épreuve T04-c, puis l'annuler.
- [ ] R9 Contrôles finaux : T04-a, T04-b, T04-c exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » ; commit ; push.

## Prompt de vérification

```text
Tu es <ton nom d'IA>, au rôle Vérificateur, vérificateur indépendant de l'unité S08 « T04 Préparation du banc d'essai » du projet GODOT_DEV_MAPPER.
Tu n'en es pas l'auteur : lis la ligne « Auteur » de rapports/S08.md ; si c'est toi, arrête-toi.
Tu ne modifies aucun fichier de l'unité. Tu écris ton verdict et tu coches les sous-étapes V, sur la branche.

COPIE NEUVE : git fetch origin && git worktree add --detach ../verif-S08-T04-preparation origin/tache/S08-T04-preparation
GODOT : même procédure que le prompt de réalisation.

1. PÉRIMÈTRE. git diff --name-only origin/main...origin/tache/S08-T04-preparation. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S08*.md et suivi/S08-T04-preparation.md. Tout autre fichier : refus.
2. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : T04-a, T04-b, T04-c.
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
5. COHÉRENCE. Aucun fichier du jeu sur `main` ; licences reprises de `docs/benches/selection.md`.

VERDICT dans rapports/S08-verif-<tentative>.md :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte
Pousse le verdict sur la branche. Si ACCEPTÉE, fais les sous-étapes F de la fiche. Si REFUSÉE, arrête-toi : une IA au rôle de l'auteur reprendra.
```

## Sous-étapes de vérification

- [ ] V1 Prise en charge : pas l'auteur ; copie neuve `../verif-S08-T04-preparation` sur `origin/tache/S08-T04-preparation`.
- [ ] V2 Périmètre : `git diff --name-only origin/main...origin/tache/S08-T04-preparation` ⊂ fichiers autorisés.
- [ ] V3.1 Contrôle T04-a relancé, résultat conforme.
- [ ] V3.2 Contrôle T04-b relancé, résultat conforme.
- [ ] V3.3 Contrôle T04-c relancé, résultat conforme.
- [ ] V4 Contre-épreuves (CE) appliquées et détectées, puis annulées.
- [ ] V5 Contournements cherchés.
- [ ] V6 Cohérence avec les contrats et les invariants.
- [ ] V7 Verdict écrit dans `rapports/S08-verif-<tentative>.md` et poussé.

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

- [ ] F1 `git switch main && git pull --ff-only && git merge --no-ff origin/tache/S08-T04-preparation -m "Fusion S08 : T04 Préparation du banc d'essai"`.
- [ ] F2 Sur `main` : `GODOT="$B" tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK. Sinon : `git reset --hard ORIG_HEAD`, verdict « REFUSÉE (fusion) » poussé sur la branche, et arrêt de la fusion.
- [ ] F3 Dans `SUIVI.md`, cocher la ligne **S08** et compléter « fait le <date> · auteur <IA> · vérifié par <IA> · <n> créneaux ».
- [ ] F4 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette.
- [ ] F5 Cocher les sous-étapes F de cette fiche ; `git commit` ; `git push origin main` (en cas de refus : `git pull --rebase`, puis push).

## Pour la recette

Rien de propre à cette unité.
