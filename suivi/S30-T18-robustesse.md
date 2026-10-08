# S30 — T18 Robustesse et cycle de vie

> Fiche d'exécution du mode autonome. Chaque case se coche avec `python3 suivi/outil.py cocher S30 <sous-étape> --ia <n>`, juste après la sous-étape : la commande vérifie l'ordre et l'identité de l'IA, signe la case (IA, date, heure UTC), commite et pousse. Une sous-étape non cochée par cette commande est considérée comme non faite. Règles : `docs/construction/sequence.md`. Avancement : `SUIVI.md` et `suivi/tableau.html`.

| Champ | Valeur |
| --- | --- |
| Réalise | IA 2 (développement) |
| Vérifie | IA 1 (conception), jamais un auteur de l'unité |
| Piste | 6.B Robustesse : S30 (unité 1 sur 1) |
| Commence après | S21, S24 (cochées dans `SUIVI.md`) |
| Indépendante de | S22, S23, S25, S26, S27, S28, S29, S33 |
| Branche | `tache/S30-T18-robustesse` |
| Fiche de conception | `docs/construction/etape-6.md`, section T18 |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Cette unité est la 1re de la piste 6.B « Robustesse », dont les unités se font à la suite. Les autres pistes de la section (6.A) avancent en même temps, chacune de son côté. Elle attend S21, S24, hors de la piste. Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- `tests/integration/run_lifecycle.sh` : six scénarios (sans débogueur, cinq démarrages et arrêts, coupure du récepteur, jeu tué, désactivation simulée, redémarrage), et `checks.d/65-lifecycle.sh`.
- Corriger un défaut sans changer de contrat ; sinon QUESTION avec le diagnostic.

## Fichiers autorisés

`tests/integration/run_lifecycle.sh`, `tools/harness/` (nouveaux scénarios), `tests/unit/test_session_controller.gd` (nouveaux cas), `tools/ci/checks.d/65-lifecycle.sh`. Pour corriger un défaut sans changer de contrat : `addons/godot_dev_mapper_runtime/flow_trace.gd` et `addons/godot_dev_mapper/editor/session_controller.gd`. Les tests de contrat restent intouchables ; une correction qui exigerait de changer un contrat passe par QUESTION.

Toujours autorisés en plus : `rapports/S30*.md` et les cases de cette fiche (par `cocher`).

## Prompt de réalisation

```text
Tu réalises l'unité S30 « T18 Robustesse et cycle de vie » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.
Réalisation prévue : IA 2 (développement) ; vérification : IA 1 (conception). Ton numéro d'IA est celui que te donne le prompt de créneau : tu le passes à --ia, et il signe chaque case que tu coches.

AVANT TOUT, depuis ton clone principal du dépôt
1. Lis REGLES_AGENTS.md s'il existe, puis cette fiche : suivi/S30-T18-robustesse.md.
2. python3 suivi/outil.py prendre S30 --ia <n>
   - « PRISE » ou « REPRISE » : tu es sur la branche tache/S30-T18-robustesse ; commence à la sous-étape affichée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
   - « REFUSÉ » : l'unité n'est pas pour toi maintenant (déjà prise par une autre IA, S21, S24 non cochées, autre IA prévue) : reviens au prompt de créneau et choisis autre chose.

GODOT
- Si tools/ci/fetch_godot.sh existe : B=$(tools/ci/fetch_godot.sh 4.7.2-stable)
- Sinon, hors du dépôt :
  D=$HOME/.cache/gdm-godot/4.7.2-stable ; mkdir -p "$D"
  test -x "$D/Godot_v4.7.2-stable_linux.x86_64" || { curl -sSL -o /tmp/godot-4.7.2.zip https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip && unzip -o -q /tmp/godot-4.7.2.zip -d "$D"; }
  B=$D/Godot_v4.7.2-stable_linux.x86_64
- « godot » dans les commandes désigne "$B". Contrôle : "$B" --version contient 4.7.2.stable.
- Éditeur avec rendu, quand la fiche le demande : xvfb-run -a -s "-screen 0 1600x900x24" "$B" --editor --path <projet> --rendering-driver opengl3

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S30.md et les cases de suivi/S30-T18-robustesse.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status. Tu ne pousses jamais avec --force.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.
- Une décision réservée à l'humain (docs/construction/sequence.md §5) : arrêt obligatoire, rien d'autre.

TRACE OBLIGATOIRE, après CHAQUE sous-étape et avant la suivante
1. git add <les fichiers de la sous-étape> (jamais git add -A).
2. python3 suivi/outil.py cocher S30 <sous-étape> --ia <n>
   La commande vérifie l'ordre des cases et ton identité, coche la case dans suivi/S30-T18-robustesse.md, la signe (IA, date, heure UTC), commite et pousse sur tache/S30-T18-robustesse.
3. Une sous-étape faite mais non cochée par cette commande est considérée comme non faite : l'IA suivante la refera. Tu ne coches jamais une case à la main.
4. Tu ne modifies jamais SUIVI.md : il ne change qu'à la fusion, sous le verrou de main. Plusieurs IA le lisent en même temps ; aucune ne l'écrit hors de ce verrou.
5. Avant de cocher la dernière sous-étape R : « Statut : TERMINÉ » dans rapports/S30.md, puis git add.
6. Poussée refusée et non rattrapée par la commande : ne force jamais ; git pull --rebase origin tache/S30-T18-robustesse, puis relance la commande.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (docs/construction/etape-6.md, T18)
Tu réalises la tâche T18 du projet GODOT_DEV_MAPPER. Applique les règles et le format de rapport du prompt universel de réalisation.
CONTEXTE : plan §8 (cycle de vie : trois opérations) ; docs/CONTRACTS.md, section C-07 ; docs/spikes/SPIKE-01.md.

OBJECTIF : prouver par des scénarios automatiques que l'outil ne casse pas le jeu. tests/integration/run_lifecycle.sh enchaîne :
1. le jeu du banc de test lancé sans débogueur : aucune ligne d'erreur, FlowTrace inerte ;
2. cinq démarrages et arrêts de collecte de suite : aucun lot après « stopped », séquences continues ;
3. coupure du récepteur pendant la collecte : arrêt par le bail en 2 s au plus, jeu toujours actif ;
4. jeu tué pendant la collecte (kill -9) : le contrôleur de session conclut « fin inconnue » ;
5. désactivation du plugin pendant une collecte, simulée sur le contrôleur : arrêt envoyé, attente d'une seconde au plus, puis retrait ;
6. jeu redémarré après un arrêt : nouvelle session, aucun mélange avec l'ancienne.
Si un scénario échoue à cause du runtime ou du contrôleur, corrige le défaut s'il se corrige sans changer de contrat, et décris-le dans le rapport. S'il faut changer un contrat : statut QUESTION, avec le diagnostic.
Ajoute tools/ci/checks.d/65-lifecycle.sh, qui exécute run_lifecycle.sh et affiche « CHECK lifecycle OK » ou « CHECK lifecycle KO ».

CONTRÔLES
T18-a  tests/integration/run_lifecycle.sh ; echo $?   → 0, un OK par scénario
T18-b  GODOT=<binaire> tools/ci/run_all_checks.sh ; echo $?   → 0
CONTRE-ÉPREUVE (CE) pour le vérificateur : envoyer un lot après « stopped » dans le mini-jeu → le scénario 2 échoue.
SUR MA MACHINE, plus tard : désactiver le plugin pendant une vraie collecte, procédure écrite dans ton rapport.
TRAVAIL TECHNIQUE — fin de la copie exacte du guide

ADAPTATIONS DU MODE AUTONOME
- « SUR MA MACHINE, plus tard » : la désactivation du plugin pendant une vraie collecte passe à la recette.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche ; après chacune, git add puis python3 suivi/outil.py cocher S30 R<k> --ia <n>.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Chaque sous-étape faite est cochée par `cocher`. Complète rapports/S30.md (sorties, « Passation » en cinq lignes au plus), git add, git commit, git push origin HEAD:tache/S30-T18-robustesse.
- git status ne montre aucune modification non commitée ; rien ne reste non poussé.

FORMAT DE rapports/S30.md (créé par prendre ; tu le complètes)
- Statut : EN COURS | TERMINÉ | QUESTION | ESCALADE
- Auteurs : IA n (écrit par `prendre`) · Tentative : n · Créneaux utilisés : n
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

Après chaque sous-étape : `git add` de ses fichiers, puis `python3 suivi/outil.py cocher S30 R<k> --ia <n>` (coche, signe, commite, pousse).

- [ ] R0 Prise en charge : `python3 suivi/outil.py prendre S30 --ia <n>` (prérequis cochés dans `SUIVI.md` : S21, S24 ; branche `tache/S30-T18-robustesse` créée ou reprise ; `rapports/S30.md` au statut EN COURS) ⟶ cochée par `prendre`
- [ ] R1 Scénario 1 : jeu sans débogueur. ⟶ cocher S30 R1
- [ ] R2 Scénario 2 : cinq démarrages et arrêts. ⟶ cocher S30 R2
- [ ] R3 Scénario 3 : coupure du récepteur. ⟶ cocher S30 R3
- [ ] R4 Scénario 4 : jeu tué (kill -9). ⟶ cocher S30 R4
- [ ] R5 Scénario 5 : désactivation du plugin simulée sur le contrôleur. ⟶ cocher S30 R5
- [ ] R6 Scénario 6 : jeu redémarré, nouvelle session. ⟶ cocher S30 R6
- [ ] R7 Écrire `tools/ci/checks.d/65-lifecycle.sh`. ⟶ cocher S30 R7
- [ ] R8 Contrôles finaux : T18-a, T18-b exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » dans le rapport ⟶ cocher S30 R8

## Prompt de vérification

```text
Tu vérifies l'unité S30 « T18 Robustesse et cycle de vie » du projet GODOT_DEV_MAPPER. Vérification prévue : IA 1 (conception). Ton numéro d'IA est celui du prompt de créneau. Tu n'es jamais un auteur de l'unité : la commande de prise le contrôle.

PRISE, depuis ton clone principal
python3 suivi/outil.py prendre S30 --ia <n> --verification
- « VÉRIFICATION PRISE » : copie neuve ../verif-S30-T18-robustesse créée sur origin/tache/S30-T18-robustesse, verdict EN COURS écrit, V1 cochée. cd ../verif-S30-T18-robustesse : toute la vérification se fait dans ce dossier.
- « REFUSÉ » : une autre IA vérifie déjà, tu es auteur, ou l'unité n'est pas terminée : reviens au prompt de créneau.
GODOT : même procédure que le prompt de réalisation.
Tu ne modifies aucun fichier de l'unité. Tu écris seulement ton verdict et tes cases V.

TRACE OBLIGATOIRE : après chaque sous-étape V, git add du fichier de verdict, puis python3 suivi/outil.py cocher S30 <V…> --ia <n>. Pour la dernière : --verdict ACCEPTÉE ou --verdict REFUSÉE, identique à la ligne « Verdict » du fichier. Une sous-étape non cochée par cette commande est considérée comme non faite.

1. TRAÇABILITÉ. Chaque case R cochée est signée « — IA n · date » et a son commit sur la branche (git log --oneline origin/main..HEAD). Case cochée sans travail prouvé dans le rapport : refus.
2. PÉRIMÈTRE. git diff --name-only origin/main...HEAD. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S30*.md et suivi/S30-T18-robustesse.md. Tout autre fichier : refus.
3. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : T18-a, T18-b.
4. CONTRE-ÉPREUVES. Applique chaque sabotage marqué (CE) dans la fiche et dans le travail technique ; vérifie que le contrôle échoue ; annule avec git checkout -- . && git clean -fd (jamais sur rapports/).
5. CONTOURNEMENTS. Cherche :
   - test sans assertion, ou toujours vrai ;
   - test désactivé, renommé ou sorti du runner ;
   - valeur attendue recopiée depuis la sortie du code ;
   - marqueur supprimé de tests/pending/ sans test qui passe ;
   - fixture invalide rejetée pour un autre motif que celui de son nom ;
   - API Godot inventée ou non vérifiée ;
   - dépendance interdite entre modules ; API sensible hors de la frontière de compatibilité ;
   - affirmation du rapport sans sortie qui la prouve.
6. COHÉRENCE. Plan §8 (trois opérations du cycle de vie) ; C-07.

VERDICT dans rapports/S30-verif-<tentative>.md (créé par la prise) :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte

SI ACCEPTÉE — FUSION, depuis ton clone principal
1. python3 suivi/outil.py fusionner S30 --ia <n> --godot "$B"
   Elle prend le verrou de main (et attend s'il est pris), fusionne dans ../fusion-S30-T18-robustesse, lance run_all_checks.sh, coche la ligne dans SUIVI.md et la case F1. Si les contrôles échouent : verdict passé à REFUSÉE, main inchangée, verrou rendu ; arrête-toi sur cette unité.
2. cd ../fusion-S30-T18-robustesse ; fais les sous-étapes F suivantes de la fiche, et coche chacune : python3 suivi/outil.py cocher S30 F<k> --ia <n> (commit local, sans poussée).
3. python3 suivi/outil.py publier S30 --ia <n> : dernière case cochée, verifier relancé, main poussée, branche supprimée, verrou rendu.
SI REFUSÉE : arrête-toi sur cette unité ; son auteur la reprendra avec prendre.
```

## Sous-étapes de vérification

Dans `../verif-S30-T18-robustesse`, après chaque sous-étape : `git add` du verdict, puis `python3 suivi/outil.py cocher S30 V<k> --ia <n>`.

- [ ] V1 Prise en charge : `python3 suivi/outil.py prendre S30 --ia <n> --verification` (pas un auteur ; copie neuve `../verif-S30-T18-robustesse` sur `origin/tache/S30-T18-robustesse` ; verdict EN COURS) ⟶ cochée par `prendre`
- [ ] V2 Traçabilité : chaque case R cochée porte une signature « — IA n · date » et un commit sur la branche (`git log --oneline origin/main..HEAD`) ⟶ cocher S30 V2
- [ ] V3 Périmètre : `git diff --name-only origin/main...HEAD` ⊂ fichiers autorisés. ⟶ cocher S30 V3
- [ ] V4.1 Contrôle T18-a relancé, résultat conforme. ⟶ cocher S30 V4.1
- [ ] V4.2 Contrôle T18-b relancé, résultat conforme. ⟶ cocher S30 V4.2
- [ ] V5 Contre-épreuves (CE) appliquées et détectées, puis annulées. ⟶ cocher S30 V5
- [ ] V6 Contournements cherchés. ⟶ cocher S30 V6
- [ ] V7 Cohérence avec les contrats et les invariants. ⟶ cocher S30 V7
- [ ] V8 Verdict écrit dans `rapports/S30-verif-<tentative>.md` ⟶ cocher S30 V8 --verdict ACCEPTÉE ou --verdict REFUSÉE

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

F1 et la dernière se cochent par `fusionner` et `publier` ; les autres, dans `../fusion-S30-T18-robustesse`, par `python3 suivi/outil.py cocher S30 F<k> --ia <n>` (commit local).

- [ ] F1 Fusion : `python3 suivi/outil.py fusionner S30 --ia <n> --godot "$B"` : verrou de `main`, fusion `--no-ff` dans `../fusion-S30-T18-robustesse`, `tools/ci/run_all_checks.sh` sur `main` → ALL_CHECKS OK s'il existe (sinon fusion annulée et verdict passé à REFUSÉE), ligne **S30** cochée dans `SUIVI.md` ⟶ cochée par `fusionner`
- [ ] F2 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette ⟶ cocher S30 F2
- [ ] F3 Publication : `python3 suivi/outil.py publier S30 --ia <n>` (verifier OK, `main` poussée, branche `tache/S30-T18-robustesse` supprimée, verrou rendu) ⟶ cochée par `publier`

## Pour la recette

- Désactiver le plugin pendant une vraie collecte, dans ton éditeur.
