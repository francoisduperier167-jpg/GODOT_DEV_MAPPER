# S33 — T19 Injection de trois bugs

> Fiche d'exécution du mode autonome. Coche chaque case dès qu'elle est faite et prouvée, puis commite et pousse : une autre IA doit pouvoir reprendre à la première case non cochée. Règles : `docs/construction/sequence.md`. Avancement global : `SUIVI.md`.

| Champ | Valeur |
| --- | --- |
| Réalise | Vérificateur |
| Vérifie | Concepteur (jamais l'auteur) |
| Commence après | S25 (cochées dans `SUIVI.md`) |
| Indépendante de | S17, S18, S22, S23, S24, S26, S27, S28, S29, S30, S31, S32 |
| Branche | `tache/S33-T19-injection` |
| Fiche de conception | `docs/construction/etape-7.md`, section T19 |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité elle-même peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Créer trois branches `banc/<nom>-bug-1` à `-bug-3` depuis `banc/<nom>-instrumentation`, un seul bug par branche, de difficulté comparable, sans toucher aux appels FlowTrace ni au graphe déclaré ; les pousser.
- Écrire l'enveloppe scellée dans une branche orpheline `banc/<nom>-enveloppe`, et seulement les symptômes dans `rapports/S33.md`.

## Fichiers autorisés

`rapports/S33.md` (symptômes et déclenchement seulement). Hors de `main` : les branches `banc/<nom>-bug-1` à `-bug-3` et `banc/<nom>-enveloppe`.

Toujours autorisés en plus : `rapports/S33*.md` et les cases de cette fiche.

## Contrôles propres à cette fiche

- `S33-a` : `git ls-remote origin "refs/heads/banc/*-bug-*" | wc -l` → 3
- `T19-a` : Chaque branche de bug reproduit son symptôme seule, vérifié par le vérificateur → trois symptômes reproduits
- `S33-b` : `grep -cE "\.gd:[0-9]+" rapports/S33.md` → 0 (aucune cause divulguée)
- (CE) Ajouter une ligne « fichier.gd:12 » dans `rapports/S33.md` : S33-b donne 1 ; annuler.

## Prompt de réalisation

```text
Tu es <ton nom d'IA>, au rôle Vérificateur. Tu réalises l'unité S33 « T19 Injection de trois bugs » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.

AVANT TOUT
1. git fetch origin. Lis REGLES_AGENTS.md s'il existe, puis la fiche suivi/S33-T19-injection.md.
2. Si la branche origin/tache/S33-T19-injection existe : reprends-la, relis rapports/S33.md et commence à la première sous-étape R non cochée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
3. Sinon : vérifie dans SUIVI.md, sur main, que S25 est cochée, puis crée tache/S33-T19-injection depuis main.

GODOT
- Si tools/ci/fetch_godot.sh existe : B=$(tools/ci/fetch_godot.sh 4.7.2-stable)
- Sinon, hors du dépôt :
  D=$HOME/.cache/gdm-godot/4.7.2-stable ; mkdir -p "$D"
  test -x "$D/Godot_v4.7.2-stable_linux.x86_64" || { curl -sSL -o /tmp/godot-4.7.2.zip https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip && unzip -o -q /tmp/godot-4.7.2.zip -d "$D"; }
  B=$D/Godot_v4.7.2-stable_linux.x86_64
- « godot » dans les commandes désigne "$B". Contrôle : "$B" --version contient 4.7.2.stable.
- Éditeur avec rendu, quand la fiche le demande : xvfb-run -a -s "-screen 0 1600x900x24" "$B" --editor --path <projet> --rendering-driver opengl3

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S33.md et les cases de suivi/S33-T19-injection.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu coches une case seulement quand elle est faite et prouvée. Tu commites et tu pousses après chaque case cochée.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (docs/construction/etape-7.md, T19)
Tu prépares la mesure de valeur, exploratoire, du POC du projet GODOT_DEV_MAPPER. Tu travailles dans la copie de travail ../benches/{nom}.
Crée trois branches à partir de gdm-instrumentation : gdm-bug-1, gdm-bug-2, gdm-bug-3. Chacune contient un seul bug, et seulement celui-là.
Règles des bugs :
- chacun est visible en jeu et lié à une décision instrumentée ou à l'état d'une instance ;
- chacun a une seule cause, à un ou deux appels du symptôme : les trois doivent être de difficulté comparable ;
- natures possibles : comparaison inversée dans une décision, état non réinitialisé après réinsertion dans l'arbre, mauvaise instance ciblée. N'en reprends pas un tel quel.
Ne touche ni aux appels FlowTrace, ni à benches/{nom}/flow.json.
Écris ../benches/{nom}/ENVELOPPE_SCELLEE.md, hors des trois branches : pour chaque bug, la branche, le symptôme visible, la cause, le fichier et la ligne, la manière de le déclencher, et pourquoi sa difficulté est comparable aux deux autres.
Dans ta réponse, donne-moi seulement, pour chaque bug : la branche, le symptôme et la manière de le déclencher en jeu. Rien d'autre.
TRAVAIL TECHNIQUE — fin de la copie exacte du guide

CONTRÔLES DE LA FICHE
S33-a  git ls-remote origin "refs/heads/banc/*-bug-*" | wc -l   → 3
T19-a  Chaque branche de bug reproduit son symptôme seule, vérifié par le vérificateur   → trois symptômes reproduits
S33-b  grep -cE "\.gd:[0-9]+" rapports/S33.md   → 0 (aucune cause divulguée)
(CE) Ajouter une ligne « fichier.gd:12 » dans `rapports/S33.md` : S33-b donne 1 ; annuler.

ADAPTATIONS DU MODE AUTONOME
- Les branches `gdm-bug-N` du guide deviennent `banc/<nom>-bug-N`, poussées sur le dépôt ; l'enveloppe vit dans la branche orpheline `banc/<nom>-enveloppe`.
- Règle pour toutes les IA : celle qui réalisera S34 ne récupère pas `banc/<nom>-enveloppe` avant d'avoir fini ses trois diagnostics.
- Contrôles du guide : T19-a (chaque branche reproduit son symptôme) est vérifié ici ; T19-b, T19-c et T19-d le sont en S34.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche, et coche chacune.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Coche dans suivi/S33-T19-injection.md les sous-étapes faites et prouvées ; complète rapports/S33.md (sorties, section « Passation ») ; commite ; git push origin tache/S33-T19-injection.
- Ne laisse aucune modification non poussée.

FORMAT DE rapports/S33.md
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

- [ ] R0 Prise en charge : `git fetch origin` ; S25 est cochée dans `SUIVI.md` ; branche `origin/tache/S33-T19-injection` absente, ou sans commit depuis deux créneaux, ou dernier verdict REFUSÉE ; créer ou reprendre la branche ; `rapports/S33.md` avec « Statut : EN COURS » et « Auteur » ; commit ; push.
- [ ] R1 Copie de travail de `banc/<nom>-instrumentation`.
- [ ] R2 Créer `banc/<nom>-bug-1` avec son bug ; vérifier que le symptôme se reproduit ; pousser.
- [ ] R3 Créer `banc/<nom>-bug-2` ; vérifier ; pousser.
- [ ] R4 Créer `banc/<nom>-bug-3` ; vérifier ; pousser.
- [ ] R5 Écrire `ENVELOPPE_SCELLEE.md` dans la branche orpheline `banc/<nom>-enveloppe` ; pousser.
- [ ] R6 Écrire dans `rapports/S33.md` seulement la branche, le symptôme et le déclenchement de chaque bug.
- [ ] R7 Contrôles finaux : S33-a, T19-a, S33-b exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » ; commit ; push.

## Prompt de vérification

```text
Tu es <ton nom d'IA>, au rôle Concepteur, vérificateur indépendant de l'unité S33 « T19 Injection de trois bugs » du projet GODOT_DEV_MAPPER.
Tu n'en es pas l'auteur : lis la ligne « Auteur » de rapports/S33.md ; si c'est toi, arrête-toi.
Tu ne modifies aucun fichier de l'unité. Tu écris ton verdict et tu coches les sous-étapes V, sur la branche.

COPIE NEUVE : git fetch origin && git worktree add --detach ../verif-S33-T19-injection origin/tache/S33-T19-injection
GODOT : même procédure que le prompt de réalisation.

1. PÉRIMÈTRE. git diff --name-only origin/main...origin/tache/S33-T19-injection. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S33*.md et suivi/S33-T19-injection.md. Tout autre fichier : refus.
2. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : S33-a, T19-a, S33-b.
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
5. COHÉRENCE. Règles des bugs de la fiche T19 : une cause, difficulté comparable, natures variées.

VERDICT dans rapports/S33-verif-<tentative>.md :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte
Pousse le verdict sur la branche. Si ACCEPTÉE, fais les sous-étapes F de la fiche. Si REFUSÉE, arrête-toi : une IA au rôle de l'auteur reprendra.
```

## Sous-étapes de vérification

- [ ] V1 Prise en charge : pas l'auteur ; copie neuve `../verif-S33-T19-injection` sur `origin/tache/S33-T19-injection`.
- [ ] V2 Périmètre : `git diff --name-only origin/main...origin/tache/S33-T19-injection` ⊂ fichiers autorisés.
- [ ] V3.1 Contrôle S33-a relancé, résultat conforme.
- [ ] V3.2 Contrôle T19-a relancé, résultat conforme.
- [ ] V3.3 Contrôle S33-b relancé, résultat conforme.
- [ ] V4 Contre-épreuves (CE) appliquées et détectées, puis annulées.
- [ ] V5 Contournements cherchés.
- [ ] V6 Cohérence avec les contrats et les invariants.
- [ ] V7 Verdict écrit dans `rapports/S33-verif-<tentative>.md` et poussé.

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

- [ ] F1 `git switch main && git pull --ff-only && git merge --no-ff origin/tache/S33-T19-injection -m "Fusion S33 : T19 Injection de trois bugs"`.
- [ ] F2 Sur `main` : `GODOT="$B" tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK. Sinon : `git reset --hard ORIG_HEAD`, verdict « REFUSÉE (fusion) » poussé sur la branche, et arrêt de la fusion.
- [ ] F3 Dans `SUIVI.md`, cocher la ligne **S33** et compléter « fait le <date> · auteur <IA> · vérifié par <IA> · <n> créneaux ».
- [ ] F4 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette.
- [ ] F5 Cocher les sous-étapes F de cette fiche ; `git commit` ; `git push origin main` (en cas de refus : `git pull --rebase`, puis push).

## Pour la recette

Rien de propre à cette unité.
