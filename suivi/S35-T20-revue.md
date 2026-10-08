# S35 — T20 Revue de continuation et décision

> Fiche d'exécution du mode autonome. Chaque case se coche avec `python3 suivi/outil.py cocher S35 <sous-étape> --ia <n>`, juste après la sous-étape : la commande vérifie l'ordre et l'identité de l'IA, signe la case (IA, date, heure UTC), commite et pousse. Une sous-étape non cochée par cette commande est considérée comme non faite. Règles : `docs/construction/sequence.md`. Avancement : `SUIVI.md` et `suivi/tableau.html`.

| Champ | Valeur |
| --- | --- |
| Réalise | IA 1 (conception) |
| Vérifie | IA 3 (vérification), jamais un auteur de l'unité |
| Piste | Rendez-vous de l'étape 7 : S35 |
| Commence après | S34 (cochée dans `SUIVI.md`) |
| Indépendante de | aucune |
| Branche | `tache/S35-T20-revue` |
| Fiche de conception | `docs/construction/etape-7.md`, section T20 |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Cette unité appartient au rendez-vous de l'étape 7 : elle attend la fin des pistes 7.A. Concrètement, elle attend S34. Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Écrire `docs/revues/revue-poc.md` : budgets en créneaux, fiabilité par IA, signal d'utilité par substitution, risques, options, décisions à prendre, proposition d'amendement PD-0.6.
- Décider selon la règle : continuer si le signal est positif, si aucun arrêt n'est ouvert et si les créneaux consommés restent sous le double de l'estimation ; sinon écrire `rapports/ARRET.md`.
- Appliquer l'amendement PD-0.6 au statut « proposé ».

## Fichiers autorisés

`docs/revues/revue-poc.md`, `docs/plan-directeur.md` (amendement PD-0.6, statut « proposé »). À la fusion : la décision dans `docs/DECISIONS.md`.

Toujours autorisés en plus : `rapports/S35*.md` et les cases de cette fiche (par `cocher`).

## Prompt de réalisation

```text
Tu réalises l'unité S35 « T20 Revue de continuation et décision » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.
Réalisation prévue : IA 1 (conception) ; vérification : IA 3 (vérification). Ton numéro d'IA est celui que te donne le prompt de créneau : tu le passes à --ia, et il signe chaque case que tu coches.

AVANT TOUT, depuis ton clone principal du dépôt
1. Lis REGLES_AGENTS.md s'il existe, puis cette fiche : suivi/S35-T20-revue.md.
2. python3 suivi/outil.py prendre S35 --ia <n>
   - « PRISE » ou « REPRISE » : tu es sur la branche tache/S35-T20-revue ; commence à la sous-étape affichée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
   - « REFUSÉ » : l'unité n'est pas pour toi maintenant (déjà prise par une autre IA, S34 non cochée, autre IA prévue) : reviens au prompt de créneau et choisis autre chose.

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
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status. Tu ne pousses jamais avec --force.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.
- Une décision réservée à l'humain (docs/construction/sequence.md §5) : arrêt obligatoire, rien d'autre.

TRACE OBLIGATOIRE, après CHAQUE sous-étape et avant la suivante
1. git add <les fichiers de la sous-étape> (jamais git add -A).
2. python3 suivi/outil.py cocher S35 <sous-étape> --ia <n>
   La commande vérifie l'ordre des cases et ton identité, coche la case dans suivi/S35-T20-revue.md, la signe (IA, date, heure UTC), commite et pousse sur tache/S35-T20-revue.
3. Une sous-étape faite mais non cochée par cette commande est considérée comme non faite : l'IA suivante la refera. Tu ne coches jamais une case à la main.
4. Tu ne modifies jamais SUIVI.md : il ne change qu'à la fusion, sous le verrou de main. Plusieurs IA le lisent en même temps ; aucune ne l'écrit hors de ce verrou.
5. Avant de cocher la dernière sous-étape R : « Statut : TERMINÉ » dans rapports/S35.md, puis git add.
6. Poussée refusée et non rattrapée par la commande : ne force jamais ; git pull --rebase origin tache/S35-T20-revue, puis relance la commande.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (docs/construction/etape-7.md, T20)
Tu prépares la revue de continuation du POC du projet GODOT_DEV_MAPPER. Tu ne décides pas : la décision est humaine.

ENTRÉES : PROJECT_STATE.md, docs/mesures/valeur-poc.md, docs/spikes/, les verdicts de vérification, docs/plan-directeur.md §9.

PRODUIS docs/revues/revue-poc.md avec :
1. Budgets : heures humaines et temps agent consommés par étape, contre le budget ; ratio global.
2. Fiabilité : taux de réussite au premier essai, escalades et refus du vérificateur, par IA.
3. Signal d'utilité : lecture qualitative de T19, avec ses limites (trois bugs, une seule personne, durées indicatives).
4. Risques : ceux du plan, mis à jour ; les nouveaux.
5. Options : continuer, réduire, réorienter ou arrêter. Pour chacune : conditions, conséquences, budget restant estimé avec le ratio observé.
6. Décisions à prendre :
   - SPIKE-03 (rendu) et SPIKE-04 (AST Flow ou extraction maison) au début du MVP ;
   - reprise d'AST Flow comme backend statique ;
   - répartition des tâches entre les trois IA pour le MVP ;
   - besoin, ou non, d'une mesure de valeur plus large au MVP.
7. Proposition d'amendement du plan (PD-0.6) : budgets recalibrés et décisions retenues. Le diff exact, sans l'appliquer.
TRAVAIL TECHNIQUE — fin de la copie exacte du guide

ADAPTATIONS DU MODE AUTONOME
- « Tu ne décides pas : la décision est humaine » : en mode autonome, tu appliques la règle de décision de la fiche, et la décision est inscrite « adoptée par défaut ».
- Budgets : en créneaux d'IA (estimation de `sequence.md` §8), et non en heures humaines.
- SPIKE-04 : si la reprise d'AST Flow est recommandée, c'est une nouvelle dépendance, à décider par l'humain ; le MVP continue avec l'extraction maison en attendant.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche ; après chacune, git add puis python3 suivi/outil.py cocher S35 R<k> --ia <n>.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Chaque sous-étape faite est cochée par `cocher`. Complète rapports/S35.md (sorties, « Passation » en cinq lignes au plus), git add, git commit, git push origin HEAD:tache/S35-T20-revue.
- git status ne montre aucune modification non commitée ; rien ne reste non poussé.

FORMAT DE rapports/S35.md (créé par prendre ; tu le complètes)
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

Après chaque sous-étape : `git add` de ses fichiers, puis `python3 suivi/outil.py cocher S35 R<k> --ia <n>` (coche, signe, commite, pousse).

- [ ] R0 Prise en charge : `python3 suivi/outil.py prendre S35 --ia <n>` (prérequis cochés dans `SUIVI.md` : S34 ; branche `tache/S35-T20-revue` créée ou reprise ; `rapports/S35.md` au statut EN COURS) ⟶ cochée par `prendre`
- [ ] R1 Rassembler `SUIVI.md`, `PROJECT_STATE.md`, les verdicts, `docs/mesures/valeur-poc-substitution.md`, `docs/spikes/`. ⟶ cocher S35 R1
- [ ] R2 Écrire les sections 1 à 6 de la revue. ⟶ cocher S35 R2
- [ ] R3 Appliquer la règle de décision et l'écrire dans la revue. ⟶ cocher S35 R3
- [ ] R4 Écrire et appliquer l'amendement PD-0.6, au statut « proposé ». ⟶ cocher S35 R4
- [ ] R5 Si la décision est de s'arrêter : écrire `rapports/ARRET.md`. ⟶ cocher S35 R5
- [ ] R6 Contrôles finaux : T20-a, T20-b, T20-c, T20-d exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » dans le rapport ⟶ cocher S35 R6

## Prompt de vérification

```text
Tu vérifies l'unité S35 « T20 Revue de continuation et décision » du projet GODOT_DEV_MAPPER. Vérification prévue : IA 3 (vérification). Ton numéro d'IA est celui du prompt de créneau. Tu n'es jamais un auteur de l'unité : la commande de prise le contrôle.

PRISE, depuis ton clone principal
python3 suivi/outil.py prendre S35 --ia <n> --verification
- « VÉRIFICATION PRISE » : copie neuve ../verif-S35-T20-revue créée sur origin/tache/S35-T20-revue, verdict EN COURS écrit, V1 cochée. cd ../verif-S35-T20-revue : toute la vérification se fait dans ce dossier.
- « REFUSÉ » : une autre IA vérifie déjà, tu es auteur, ou l'unité n'est pas terminée : reviens au prompt de créneau.
GODOT : même procédure que le prompt de réalisation.
Tu ne modifies aucun fichier de l'unité. Tu écris seulement ton verdict et tes cases V.

TRACE OBLIGATOIRE : après chaque sous-étape V, git add du fichier de verdict, puis python3 suivi/outil.py cocher S35 <V…> --ia <n>. Pour la dernière : --verdict ACCEPTÉE ou --verdict REFUSÉE, identique à la ligne « Verdict » du fichier. Une sous-étape non cochée par cette commande est considérée comme non faite.

1. TRAÇABILITÉ. Chaque case R cochée est signée « — IA n · date » et a son commit sur la branche (git log --oneline origin/main..HEAD). Case cochée sans travail prouvé dans le rapport : refus.
2. PÉRIMÈTRE. git diff --name-only origin/main...HEAD. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S35*.md et suivi/S35-T20-revue.md. Tout autre fichier : refus.
3. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : T20-a, T20-b, T20-c, T20-d.
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
6. COHÉRENCE. Plan §9 (portes, critères d'arrêt) ; `sequence.md` §5 et §8.

VERDICT dans rapports/S35-verif-<tentative>.md (créé par la prise) :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte

SI ACCEPTÉE — FUSION, depuis ton clone principal
1. python3 suivi/outil.py fusionner S35 --ia <n> --godot "$B"
   Elle prend le verrou de main (et attend s'il est pris), fusionne dans ../fusion-S35-T20-revue, lance run_all_checks.sh, coche la ligne dans SUIVI.md et la case F1. Si les contrôles échouent : verdict passé à REFUSÉE, main inchangée, verrou rendu ; arrête-toi sur cette unité.
2. cd ../fusion-S35-T20-revue ; fais les sous-étapes F suivantes de la fiche, et coche chacune : python3 suivi/outil.py cocher S35 F<k> --ia <n> (commit local, sans poussée).
3. python3 suivi/outil.py publier S35 --ia <n> : dernière case cochée, verifier relancé, main poussée, branche supprimée, verrou rendu.
SI REFUSÉE : arrête-toi sur cette unité ; son auteur la reprendra avec prendre.
```

## Sous-étapes de vérification

Dans `../verif-S35-T20-revue`, après chaque sous-étape : `git add` du verdict, puis `python3 suivi/outil.py cocher S35 V<k> --ia <n>`.

- [ ] V1 Prise en charge : `python3 suivi/outil.py prendre S35 --ia <n> --verification` (pas un auteur ; copie neuve `../verif-S35-T20-revue` sur `origin/tache/S35-T20-revue` ; verdict EN COURS) ⟶ cochée par `prendre`
- [ ] V2 Traçabilité : chaque case R cochée porte une signature « — IA n · date » et un commit sur la branche (`git log --oneline origin/main..HEAD`) ⟶ cocher S35 V2
- [ ] V3 Périmètre : `git diff --name-only origin/main...HEAD` ⊂ fichiers autorisés. ⟶ cocher S35 V3
- [ ] V4.1 Contrôle T20-a relancé, résultat conforme. ⟶ cocher S35 V4.1
- [ ] V4.2 Contrôle T20-b relancé, résultat conforme. ⟶ cocher S35 V4.2
- [ ] V4.3 Contrôle T20-c relancé, résultat conforme. ⟶ cocher S35 V4.3
- [ ] V4.4 Contrôle T20-d relancé, résultat conforme. ⟶ cocher S35 V4.4
- [ ] V5 Contre-épreuves (CE) appliquées et détectées, puis annulées. ⟶ cocher S35 V5
- [ ] V6 Contournements cherchés. ⟶ cocher S35 V6
- [ ] V7 Cohérence avec les contrats et les invariants. ⟶ cocher S35 V7
- [ ] V8 Verdict écrit dans `rapports/S35-verif-<tentative>.md` ⟶ cocher S35 V8 --verdict ACCEPTÉE ou --verdict REFUSÉE

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

F1 et la dernière se cochent par `fusionner` et `publier` ; les autres, dans `../fusion-S35-T20-revue`, par `python3 suivi/outil.py cocher S35 F<k> --ia <n>` (commit local).

- [ ] F1 Fusion : `python3 suivi/outil.py fusionner S35 --ia <n> --godot "$B"` : verrou de `main`, fusion `--no-ff` dans `../fusion-S35-T20-revue`, `tools/ci/run_all_checks.sh` sur `main` → ALL_CHECKS OK s'il existe (sinon fusion annulée et verdict passé à REFUSÉE), ligne **S35** cochée dans `SUIVI.md` ⟶ cochée par `fusionner`
- [ ] F2 Inscrire la décision du POC dans `docs/DECISIONS.md`, au statut « adoptée par défaut ». ⟶ cocher S35 F2
- [ ] F3 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette ⟶ cocher S35 F3
- [ ] F4 Publication : `python3 suivi/outil.py publier S35 --ia <n>` (verifier OK, `main` poussée, branche `tache/S35-T20-revue` supprimée, verrou rendu) ⟶ cochée par `publier`

## Pour la recette

- Confirmer la décision de continuer, et l'amendement PD-0.6.
