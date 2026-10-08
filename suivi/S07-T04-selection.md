# S07 — T04 Sélection du banc d'essai

> Fiche d'exécution du mode autonome. Coche chaque case dès qu'elle est faite et prouvée, puis commite et pousse : une autre IA doit pouvoir reprendre à la première case non cochée. Règles : `docs/construction/sequence.md`. Avancement global : `SUIVI.md`.

| Champ | Valeur |
| --- | --- |
| Réalise | Vérificateur |
| Vérifie | Concepteur (jamais l'auteur) |
| Commence après | S01 (cochées dans `SUIVI.md`) |
| Indépendante de | S02, S03, S04, S05, S06, S10, S11 |
| Branche | `tache/S07-T04-selection` |
| Fiche de conception | `docs/construction/etape-1.md`, section T04 |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité elle-même peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Trouver au plus trois jeux candidats qui remplissent tous les critères de D-02.
- Pour chacun, vérifier dans son dépôt, à une révision épinglée (SHA de 40 caractères) : licence du code et licence des assets (fichiers qui le disent), version de Godot d'origine (`project.godot`), nombre de scripts `.gd`, scripts qui contiennent les décisions ciblées, risques de migration.
- Écarter tout candidat dont une licence est incertaine ou ne permet pas de redistribuer une copie modifiée : le banc vivra dans des branches de ce dépôt.
- Écrire `docs/benches/selection.md` : tableau comparatif avec liens épinglés, recommandation, deux faiblesses principales.

## Fichiers autorisés

`docs/benches/selection.md`. À la fusion seulement, par le concepteur : la ligne D-02 de `docs/DECISIONS.md`.

Toujours autorisés en plus : `rapports/S07*.md` et les cases de cette fiche.

## Contrôles propres à cette fiche

- `S07-a` : `test -s docs/benches/selection.md; echo $?` → 0
- `S07-b` : `grep -Eo "[0-9a-f]{40}" docs/benches/selection.md | sort -u | wc -l` → au moins le nombre de candidats
- `S07-c` : `grep -i "licen" docs/benches/selection.md | grep -ci "non vérifié"` → 0
- (CE) Remplacer une licence par « non vérifié » dans le fichier : S07-c donne au moins 1 ; annuler.

## Prompt de réalisation

```text
Tu es <ton nom d'IA>, au rôle Vérificateur. Tu réalises l'unité S07 « T04 Sélection du banc d'essai » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.

AVANT TOUT
1. git fetch origin. Lis REGLES_AGENTS.md s'il existe, puis la fiche suivi/S07-T04-selection.md.
2. Si la branche origin/tache/S07-T04-selection existe : reprends-la, relis rapports/S07.md et commence à la première sous-étape R non cochée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
3. Sinon : vérifie dans SUIVI.md, sur main, que S01 est cochée, puis crée tache/S07-T04-selection depuis main.

GODOT
- Si tools/ci/fetch_godot.sh existe : B=$(tools/ci/fetch_godot.sh 4.7.2-stable)
- Sinon, hors du dépôt :
  D=$HOME/.cache/gdm-godot/4.7.2-stable ; mkdir -p "$D"
  test -x "$D/Godot_v4.7.2-stable_linux.x86_64" || { curl -sSL -o /tmp/godot-4.7.2.zip https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip && unzip -o -q /tmp/godot-4.7.2.zip -d "$D"; }
  B=$D/Godot_v4.7.2-stable_linux.x86_64
- « godot » dans les commandes désigne "$B". Contrôle : "$B" --version contient 4.7.2.stable.
- Éditeur avec rendu, quand la fiche le demande : xvfb-run -a -s "-screen 0 1600x900x24" "$B" --editor --path <projet> --rendering-driver opengl3

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S07.md et les cases de suivi/S07-T04-selection.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu coches une case seulement quand elle est faite et prouvée. Tu commites et tu pousses après chaque case cochée.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (docs/construction/etape-1.md, T04)
Tu aides à choisir le banc d'essai du projet GODOT_DEV_MAPPER. Tu ne copies aucun fichier de jeu dans le dépôt.
Critères, tous requis :
- jeu Godot 4.x en GDScript ;
- au moins deux types d'ennemis ou d'agents qui prennent une décision observable : attaquer ou poursuivre, fuir, patrouiller ;
- licence du code qui permet une copie de travail locale modifiée ;
- licence des assets connue ;
- entre 30 et 500 scripts .gd.
Pour trois candidats au plus, donne : nom, dépôt, révision, licences du code et des assets (avec le fichier qui le dit), version de Godot d'origine, nombre de scripts .gd, scripts qui contiennent les décisions ciblées, risques de migration vers 4.7.2.
Vérifie chaque fait dans le dépôt lui-même (fichier LICENSE, project.godot). Écris « non vérifié » quand tu n'as pas pu vérifier.
Rapport : un tableau comparatif, puis ta recommandation et ses deux principales faiblesses.
TRAVAIL TECHNIQUE — fin de la copie exacte du guide

CONTRÔLES DE LA FICHE
S07-a  test -s docs/benches/selection.md; echo $?   → 0
S07-b  grep -Eo "[0-9a-f]{40}" docs/benches/selection.md | sort -u | wc -l   → au moins le nombre de candidats
S07-c  grep -i "licen" docs/benches/selection.md | grep -ci "non vérifié"   → 0
(CE) Remplacer une licence par « non vérifié » dans le fichier : S07-c donne au moins 1 ; annuler.

ADAPTATIONS DU MODE AUTONOME
- « Tu choisis » (dans le guide, l'humain) : en mode autonome, le concepteur vérifie ta recommandation contre les critères et l'inscrit en D-02 à la fusion.
- Critère ajouté : les licences doivent permettre de redistribuer une copie modifiée, car le banc vivra dans des branches `banc/<nom>-*` de ce dépôt. « Non vérifié » sur une licence écarte le candidat.
- Écris le résultat dans `docs/benches/selection.md`, en plus de ta réponse.
- Les contrôles T04-a, T04-b et T04-c du guide portent sur la préparation : ils s'exécutent en S08.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche, et coche chacune.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Coche dans suivi/S07-T04-selection.md les sous-étapes faites et prouvées ; complète rapports/S07.md (sorties, section « Passation ») ; commite ; git push origin tache/S07-T04-selection.
- Ne laisse aucune modification non poussée.

FORMAT DE rapports/S07.md
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

- [ ] R0 Prise en charge : `git fetch origin` ; S01 est cochée dans `SUIVI.md` ; branche `origin/tache/S07-T04-selection` absente, ou sans commit depuis deux créneaux, ou dernier verdict REFUSÉE ; créer ou reprendre la branche ; `rapports/S07.md` avec « Statut : EN COURS » et « Auteur » ; commit ; push.
- [ ] R1 Relire D-02 dans `docs/DECISIONS.md`.
- [ ] R2 Chercher des candidats (GitHub, bibliothèque d'assets de Godot) et en retenir au plus trois.
- [ ] R3 Vérifier chaque fait dans le dépôt du candidat, à une révision épinglée ; noter le lien exact de chaque preuve.
- [ ] R4 Écarter les candidats aux licences incertaines ou incompatibles avec une redistribution modifiée.
- [ ] R5 Écrire `docs/benches/selection.md`.
- [ ] R6 Écrire la recommandation et ses deux faiblesses.
- [ ] R7 Contrôles finaux : S07-a, S07-b, S07-c exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » ; commit ; push.

## Prompt de vérification

```text
Tu es <ton nom d'IA>, au rôle Concepteur, vérificateur indépendant de l'unité S07 « T04 Sélection du banc d'essai » du projet GODOT_DEV_MAPPER.
Tu n'en es pas l'auteur : lis la ligne « Auteur » de rapports/S07.md ; si c'est toi, arrête-toi.
Tu ne modifies aucun fichier de l'unité. Tu écris ton verdict et tu coches les sous-étapes V, sur la branche.

COPIE NEUVE : git fetch origin && git worktree add --detach ../verif-S07-T04-selection origin/tache/S07-T04-selection
GODOT : même procédure que le prompt de réalisation.

1. PÉRIMÈTRE. git diff --name-only origin/main...origin/tache/S07-T04-selection. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S07*.md et suivi/S07-T04-selection.md. Tout autre fichier : refus.
2. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : S07-a, S07-b, S07-c.
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
5. COHÉRENCE. Critères de D-02 et de la fiche T04 ; règle du README du dépôt sur les licences des bancs d'essai.

VERDICT dans rapports/S07-verif-<tentative>.md :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte
Pousse le verdict sur la branche. Si ACCEPTÉE, fais les sous-étapes F de la fiche. Si REFUSÉE, arrête-toi : une IA au rôle de l'auteur reprendra.
```

## Sous-étapes de vérification

- [ ] V1 Prise en charge : pas l'auteur ; copie neuve `../verif-S07-T04-selection` sur `origin/tache/S07-T04-selection`.
- [ ] V2 Périmètre : `git diff --name-only origin/main...origin/tache/S07-T04-selection` ⊂ fichiers autorisés.
- [ ] V3.1 Contrôle S07-a relancé, résultat conforme.
- [ ] V3.2 Contrôle S07-b relancé, résultat conforme.
- [ ] V3.3 Contrôle S07-c relancé, résultat conforme.
- [ ] V4 Contre-épreuves (CE) appliquées et détectées, puis annulées.
- [ ] V5 Contournements cherchés.
- [ ] V6 Cohérence avec les contrats et les invariants.
- [ ] V7 Verdict écrit dans `rapports/S07-verif-<tentative>.md` et poussé.

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

- [ ] F1 `git switch main && git pull --ff-only && git merge --no-ff origin/tache/S07-T04-selection -m "Fusion S07 : T04 Sélection du banc d'essai"`.
- [ ] F2 Sur `main` : `GODOT="$B" tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK. Sinon : `git reset --hard ORIG_HEAD`, verdict « REFUSÉE (fusion) » poussé sur la branche, et arrêt de la fusion.
- [ ] F3 Dans `SUIVI.md`, cocher la ligne **S07** et compléter « fait le <date> · auteur <IA> · vérifié par <IA> · <n> créneaux ».
- [ ] F4 Inscrire dans `docs/DECISIONS.md`, ligne D-02 : « adoptée par défaut : <nom>, <dépôt>@<SHA> », avec la date.
- [ ] F5 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette.
- [ ] F6 Cocher les sous-étapes F de cette fiche ; `git commit` ; `git push origin main` (en cas de refus : `git pull --rebase`, puis push).

## Pour la recette

- Confirmer le choix du banc d'essai (D-02).
