# S25 — T15 Instrumentation du banc d'essai

> Fiche d'exécution du mode autonome. Coche chaque case dès qu'elle est faite et prouvée, puis commite et pousse : une autre IA doit pouvoir reprendre à la première case non cochée. Règles : `docs/construction/sequence.md`. Avancement global : `SUIVI.md`.

| Champ | Valeur |
| --- | --- |
| Réalise | Développeur |
| Vérifie | Vérificateur (jamais l'auteur) |
| Commence après | S08, S21 (cochées dans `SUIVI.md`) |
| Indépendante de | S17, S18, S22, S23, S24, S28, S30 |
| Branche | `tache/S25-T15-instrumentation` |
| Fiche de conception | `docs/construction/etape-5.md`, section T15 |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité elle-même peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Créer la branche `banc/<nom>-instrumentation` depuis `banc/<nom>-base` : copie de `addons/godot_dev_mapper_runtime/`, deux types d'ennemis instrumentés (register, enter, exit, decision), scène de retrait puis réinsertion d'un ennemi ; la pousser.
- Sur la branche de la tâche : `benches/<nom>/flow.json` (6 à 12 éléments), `tools/check_probe_keys.py`, `tests/integration/run_bench.sh`, `docs/benches/<nom>.md`, `tools/ci/checks.d/55-bench.sh`.

## Fichiers autorisés

Sur `tache/S25-T15-instrumentation` : `benches/<nom>/flow.json`, `tools/check_probe_keys.py`, `tests/integration/run_bench.sh`, `docs/benches/<nom>.md`, `tools/ci/checks.d/55-bench.sh`. Hors de `main` : la branche `banc/<nom>-instrumentation`.

Toujours autorisés en plus : `rapports/S25*.md` et les cases de cette fiche.

## Prompt de réalisation

```text
Tu es <ton nom d'IA>, au rôle Développeur. Tu réalises l'unité S25 « T15 Instrumentation du banc d'essai » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.

AVANT TOUT
1. git fetch origin. Lis REGLES_AGENTS.md s'il existe, puis la fiche suivi/S25-T15-instrumentation.md.
2. Si la branche origin/tache/S25-T15-instrumentation existe : reprends-la, relis rapports/S25.md et commence à la première sous-étape R non cochée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
3. Sinon : vérifie dans SUIVI.md, sur main, que S08, S21 sont cochées, puis crée tache/S25-T15-instrumentation depuis main.

GODOT
- Si tools/ci/fetch_godot.sh existe : B=$(tools/ci/fetch_godot.sh 4.7.2-stable)
- Sinon, hors du dépôt :
  D=$HOME/.cache/gdm-godot/4.7.2-stable ; mkdir -p "$D"
  test -x "$D/Godot_v4.7.2-stable_linux.x86_64" || { curl -sSL -o /tmp/godot-4.7.2.zip https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip && unzip -o -q /tmp/godot-4.7.2.zip -d "$D"; }
  B=$D/Godot_v4.7.2-stable_linux.x86_64
- « godot » dans les commandes désigne "$B". Contrôle : "$B" --version contient 4.7.2.stable.
- Éditeur avec rendu, quand la fiche le demande : xvfb-run -a -s "-screen 0 1600x900x24" "$B" --editor --path <projet> --rendering-driver opengl3

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S25.md et les cases de suivi/S25-T15-instrumentation.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu coches une case seulement quand elle est faite et prouvée. Tu commites et tu pousses après chaque case cochée.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (docs/construction/etape-5.md, T15)
Tu réalises la tâche T15 du projet GODOT_DEV_MAPPER. Applique les règles et le format de rapport du prompt universel de réalisation.
CONTEXTE : docs/benches/{nom}.md ; docs/CONTRACTS.md, sections C-01, C-05 et C-07 ; règles d'appel de C-07.

OBJECTIF
1. Dans la copie de travail ../benches/{nom}, branche gdm-instrumentation :
   - copie le dossier addons/godot_dev_mapper_runtime/ ;
   - instrumente deux types d'ennemis : register, enter et exit de la fonction de décision, decision sur la condition attaquer ou poursuivre ;
   - ajoute une scène de test qui retire un ennemi de l'arbre puis l'y remet.
2. benches/{nom}/flow.json : graphe déclaré de 6 à 12 éléments, conforme au schéma, avec des ancrages vers les fichiers et les lignes du jeu.
3. tools/check_probe_keys.py : relève les clés de sonde utilisées dans le code instrumenté et vérifie qu'elles existent toutes dans flow.json. Code 1 sinon.
4. tests/integration/run_bench.sh : lance le banc de test et le jeu instrumenté, puis vérifie les clés reçues, deux instances distinctes, et aucune destruction après réinsertion.
5. tools/ci/checks.d/55-bench.sh : exécute run_bench.sh si la copie de travail du banc d'essai est présente. Il affiche « CHECK bench OK », « CHECK bench KO », ou « CHECK bench IGNORÉ (copie absente) » : jamais un faux OK.

CONTRÔLES
T15-a  python3 tools/validate_fixtures.py --file benches/{nom}/flow.json ; echo $?   → 0
T15-b  python3 tools/check_probe_keys.py --bench ../benches/{nom} --graph benches/{nom}/flow.json ; echo $?   → 0
T15-c  godot --headless --path ../benches/{nom} --quit-after 600 2>&1 | grep -cE "^(ERROR|SCRIPT ERROR)"   → 0 (jeu sans débogueur, FlowTrace inerte)
T15-d  tests/integration/run_bench.sh ; echo $?   → 0
CONTRE-ÉPREUVES (CE)
- faute de frappe dans une clé de sonde du jeu → T15-b échoue ;
- envoyer une destruction à la sortie de l'arbre → T15-d échoue.
Note le temps passé par point instrumenté : la mesure de valeur (T19) s'en sert.
TRAVAIL TECHNIQUE — fin de la copie exacte du guide

ADAPTATIONS DU MODE AUTONOME
- Partout où le guide écrit `../benches/{nom}` et la branche `gdm-instrumentation`, lire la copie de travail de `banc/<nom>-instrumentation`, poussée sur le dépôt.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche, et coche chacune.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Coche dans suivi/S25-T15-instrumentation.md les sous-étapes faites et prouvées ; complète rapports/S25.md (sorties, section « Passation ») ; commite ; git push origin tache/S25-T15-instrumentation.
- Ne laisse aucune modification non poussée.

FORMAT DE rapports/S25.md
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

- [ ] R0 Prise en charge : `git fetch origin` ; S08, S21 sont cochées dans `SUIVI.md` ; branche `origin/tache/S25-T15-instrumentation` absente, ou sans commit depuis deux créneaux, ou dernier verdict REFUSÉE ; créer ou reprendre la branche ; `rapports/S25.md` avec « Statut : EN COURS » et « Auteur » ; commit ; push.
- [ ] R1 Copie de travail : `git fetch origin banc/<nom>-base && git worktree add ../benches/<nom> origin/banc/<nom>-base`, puis `git switch -c banc/<nom>-instrumentation` dans ce dossier.
- [ ] R2 Copier `addons/godot_dev_mapper_runtime/` dans le banc.
- [ ] R3 Instrumenter les deux types d'ennemis selon les règles d'appel de C-07 ; noter le temps passé par point instrumenté.
- [ ] R4 Ajouter la scène de retrait puis réinsertion ; pousser `banc/<nom>-instrumentation`.
- [ ] R5 Écrire `benches/<nom>/flow.json` avec les ancrages vers les fichiers et lignes du jeu.
- [ ] R6 Écrire `tools/check_probe_keys.py`.
- [ ] R7 Écrire `tests/integration/run_bench.sh` (récupère la branche du banc s'il le faut).
- [ ] R8 Écrire `tools/ci/checks.d/55-bench.sh` : OK, KO, ou IGNORÉ si la branche du banc est absente, jamais un faux OK.
- [ ] R9 Contrôles finaux : T15-a, T15-b, T15-c, T15-d exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » ; commit ; push.

## Prompt de vérification

```text
Tu es <ton nom d'IA>, au rôle Vérificateur, vérificateur indépendant de l'unité S25 « T15 Instrumentation du banc d'essai » du projet GODOT_DEV_MAPPER.
Tu n'en es pas l'auteur : lis la ligne « Auteur » de rapports/S25.md ; si c'est toi, arrête-toi.
Tu ne modifies aucun fichier de l'unité. Tu écris ton verdict et tu coches les sous-étapes V, sur la branche.

COPIE NEUVE : git fetch origin && git worktree add --detach ../verif-S25-T15-instrumentation origin/tache/S25-T15-instrumentation
GODOT : même procédure que le prompt de réalisation.

1. PÉRIMÈTRE. git diff --name-only origin/main...origin/tache/S25-T15-instrumentation. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S25*.md et suivi/S25-T15-instrumentation.md. Tout autre fichier : refus.
2. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : T15-a, T15-b, T15-c, T15-d.
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
5. COHÉRENCE. C-01, C-05, C-07 (règles d'appel) ; aucune clé orpheline.

VERDICT dans rapports/S25-verif-<tentative>.md :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte
Pousse le verdict sur la branche. Si ACCEPTÉE, fais les sous-étapes F de la fiche. Si REFUSÉE, arrête-toi : une IA au rôle de l'auteur reprendra.
```

## Sous-étapes de vérification

- [ ] V1 Prise en charge : pas l'auteur ; copie neuve `../verif-S25-T15-instrumentation` sur `origin/tache/S25-T15-instrumentation`.
- [ ] V2 Périmètre : `git diff --name-only origin/main...origin/tache/S25-T15-instrumentation` ⊂ fichiers autorisés.
- [ ] V3.1 Contrôle T15-a relancé, résultat conforme.
- [ ] V3.2 Contrôle T15-b relancé, résultat conforme.
- [ ] V3.3 Contrôle T15-c relancé, résultat conforme.
- [ ] V3.4 Contrôle T15-d relancé, résultat conforme.
- [ ] V4 Contre-épreuves (CE) appliquées et détectées, puis annulées.
- [ ] V5 Contournements cherchés.
- [ ] V6 Cohérence avec les contrats et les invariants.
- [ ] V7 Verdict écrit dans `rapports/S25-verif-<tentative>.md` et poussé.

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

- [ ] F1 `git switch main && git pull --ff-only && git merge --no-ff origin/tache/S25-T15-instrumentation -m "Fusion S25 : T15 Instrumentation du banc d'essai"`.
- [ ] F2 Sur `main` : `GODOT="$B" tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK. Sinon : `git reset --hard ORIG_HEAD`, verdict « REFUSÉE (fusion) » poussé sur la branche, et arrêt de la fusion.
- [ ] F3 Dans `SUIVI.md`, cocher la ligne **S25** et compléter « fait le <date> · auteur <IA> · vérifié par <IA> · <n> créneaux ».
- [ ] F4 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette.
- [ ] F5 Cocher les sous-étapes F de cette fiche ; `git commit` ; `git push origin main` (en cas de refus : `git pull --rebase`, puis push).

## Pour la recette

Rien de propre à cette unité.
