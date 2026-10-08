# S15 — Porte de l'étape 3 et gel des contrats

> Fiche d'exécution du mode autonome. Chaque case se coche avec `python3 suivi/outil.py cocher S15 <sous-étape> --ia <n>`, juste après la sous-étape : la commande vérifie l'ordre et l'identité de l'IA, signe la case (IA, date, heure UTC), commite et pousse. Une sous-étape non cochée par cette commande est considérée comme non faite. Règles : `docs/construction/sequence.md`. Avancement : `SUIVI.md` et `suivi/tableau.html`.

| Champ | Valeur |
| --- | --- |
| Réalise | IA 1 (conception) |
| Vérifie | IA 3 (vérification), jamais un auteur de l'unité |
| Piste | Rendez-vous de l'étape 3 : S15 |
| Commence après | S14 (cochée dans `SUIVI.md`) |
| Indépendante de | aucune |
| Branche | `tache/S15-porte-3-gel` |
| Fiche de conception | `docs/construction/etape-3.md`, points de contrôle |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Cette unité appartient au rendez-vous de l'étape 3 : elle attend la fin des pistes 3.A. Concrètement, elle attend S14. Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Exécuter chaque point de contrôle de l'étape 3 sur `main` à jour, et noter commande, attendu, obtenu, OK ou KO.
- Décider selon la règle : **passer** si tout est OK (un point « sur ta machine » passe par son équivalent sous écran virtuel, l'humain le revoit à la recette) ; **corriger d'abord** si un point est KO.
- Si un point est KO : la décision est « corriger d'abord », avec, dans le rapport, pour chaque point KO, l'unité fautive et la correction attendue. Le vérificateur fusionne alors avec `fusionner S15 --porte-ko` (la ligne **S15** reste ouverte) et crée une unité de correction par point KO avec `python3 suivi/outil.py correction S15 --fautive <Syy> --titre "<correction>" --realise <n> --verifie <m> --ia <n>`, placée juste avant la porte, dans sa piste. La porte se rejoue quand les corrections sont fusionnées : `prendre` remet ses cases à zéro.

## Fichiers autorisés

`rapports/S15.md`, `docs/CONTRACTS.md` (ligne de statut seulement).

## Points de contrôle de l'étape (copie du guide)

| ID | Contrôle | Commande ou preuve | Attendu | Adaptation |
| --- | --- | --- | --- | --- |
| PC3.1 | Gabarit complet | `python3 tools/check_contracts.py` | Code 0 | — |
| PC3.2 | Fixtures | `python3 tools/validate_fixtures.py` | Code 0 : les valides passent ; chaque invalide est rejetée avec le code de son nom, et lui seul | — |
| PC3.3 | Exemples du plan conformes | `python3 tools/validate_fixtures.py --plan-examples`, après T08 | Code 0 ; T07 ne valide que l'exemple du graphe déclaré | — |
| PC3.4 | (CE) Schéma vigilant | Retirer `evidence` d'une fixture valide, relancer PC3.2 | Code 1 | — |
| PC3.4b | (CE) Règle sémantique vigilante | Dupliquer une clé de sonde dans une fixture valide, relancer PC3.2 | Code 1, avec le code de doublon | — |
| PC3.5 | Tests en attente | Runner | Code 0 et pending ≥ 6 ; chaque test de `tests/contract/` a son marqueur dans `tests/pending/` | — |
| PC3.6 | Couverture du protocole de session | Chaque transition de la table d'états de C-07 a un test | Liste croisée dans le rapport de T08 | — |
| PC3.7 | Relecture | Rapport d'IA 3 | Aucune contradiction ouverte | — |
| PC3.8 | Gel | En-tête de `docs/CONTRACTS.md` | « Statut : validé », avec la date | Gel en mode autonome : la ligne de statut de `docs/CONTRACTS.md` devient « Statut : adopté par défaut · date ». Toute modification ultérieure passe par une analyse d'impact et un changement de version. |

## Prompt de réalisation

```text
Tu réalises l'unité S15 « Porte de l'étape 3 et gel des contrats » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.
Réalisation prévue : IA 1 (conception) ; vérification : IA 3 (vérification). Ton numéro d'IA est celui que te donne le prompt de créneau : tu le passes à --ia, et il signe chaque case que tu coches.

AVANT TOUT, depuis ton clone principal du dépôt
1. Lis REGLES_AGENTS.md s'il existe, puis cette fiche : suivi/S15-porte-3-gel.md.
2. python3 suivi/outil.py prendre S15 --ia <n>
   - « PRISE » ou « REPRISE » : tu es sur la branche tache/S15-porte-3-gel ; commence à la sous-étape affichée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
   - « REFUSÉ » : l'unité n'est pas pour toi maintenant (déjà prise par une autre IA, S14 non cochée, autre IA prévue) : reviens au prompt de créneau et choisis autre chose.

GODOT
- Si tools/ci/fetch_godot.sh existe : B=$(tools/ci/fetch_godot.sh 4.7.2-stable)
- Sinon, hors du dépôt :
  D=$HOME/.cache/gdm-godot/4.7.2-stable ; mkdir -p "$D"
  test -x "$D/Godot_v4.7.2-stable_linux.x86_64" || { curl -sSL -o /tmp/godot-4.7.2.zip https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip && unzip -o -q /tmp/godot-4.7.2.zip -d "$D"; }
  B=$D/Godot_v4.7.2-stable_linux.x86_64
- « godot » dans les commandes désigne "$B". Contrôle : "$B" --version contient 4.7.2.stable.
- Éditeur avec rendu, quand la fiche le demande : xvfb-run -a -s "-screen 0 1600x900x24" "$B" --editor --path <projet> --rendering-driver opengl3

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S15.md et les cases de suivi/S15-porte-3-gel.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status. Tu ne pousses jamais avec --force.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.
- Une décision réservée à l'humain (docs/construction/sequence.md §5) : arrêt obligatoire, rien d'autre.

TRACE OBLIGATOIRE, après CHAQUE sous-étape et avant la suivante
1. git add <les fichiers de la sous-étape> (jamais git add -A).
2. python3 suivi/outil.py cocher S15 <sous-étape> --ia <n>
   La commande vérifie l'ordre des cases et ton identité, coche la case dans suivi/S15-porte-3-gel.md, la signe (IA, date, heure UTC), commite et pousse sur tache/S15-porte-3-gel.
3. Une sous-étape faite mais non cochée par cette commande est considérée comme non faite : l'IA suivante la refera. Tu ne coches jamais une case à la main.
4. Tu ne modifies jamais SUIVI.md : il ne change qu'à la fusion, sous le verrou de main. Plusieurs IA le lisent en même temps ; aucune ne l'écrit hors de ce verrou.
5. Avant de cocher la dernière sous-étape R : « Statut : TERMINÉ » dans rapports/S15.md, puis git add.
6. Poussée refusée et non rattrapée par la commande : ne force jamais ; git pull --rebase origin tache/S15-porte-3-gel, puis relance la commande.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (docs/construction/README.md, prompt de porte d'étape)
Prépare la porte de sortie de l'étape 3 du projet GODOT_DEV_MAPPER. Entrées : docs/construction/etape-3.md, les verdicts de vérification de chaque tâche, PROJECT_STATE.md.
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
- PC3.8 : Gel en mode autonome : la ligne de statut de `docs/CONTRACTS.md` devient « Statut : adopté par défaut · date ». Toute modification ultérieure passe par une analyse d'impact et un changement de version.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche ; après chacune, git add puis python3 suivi/outil.py cocher S15 R<k> --ia <n>.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Chaque sous-étape faite est cochée par `cocher`. Complète rapports/S15.md (sorties, « Passation » en cinq lignes au plus), git add, git commit, git push origin HEAD:tache/S15-porte-3-gel.
- git status ne montre aucune modification non commitée ; rien ne reste non poussé.

FORMAT DE rapports/S15.md (créé par prendre ; tu le complètes)
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

Après chaque sous-étape : `git add` de ses fichiers, puis `python3 suivi/outil.py cocher S15 R<k> --ia <n>` (coche, signe, commite, pousse).

- [ ] R0 Prise en charge : `python3 suivi/outil.py prendre S15 --ia <n>` (prérequis cochés dans `SUIVI.md` : S14 ; branche `tache/S15-porte-3-gel` créée ou reprise ; `rapports/S15.md` au statut EN COURS) ⟶ cochée par `prendre`
- [ ] R1 PC3.1 exécuté et noté (adaptation de la fiche s’il y en a une). ⟶ cocher S15 R1
- [ ] R2 PC3.2 exécuté et noté (adaptation de la fiche s’il y en a une). ⟶ cocher S15 R2
- [ ] R3 PC3.3 exécuté et noté (adaptation de la fiche s’il y en a une). ⟶ cocher S15 R3
- [ ] R4 PC3.4 exécuté et noté (adaptation de la fiche s’il y en a une). ⟶ cocher S15 R4
- [ ] R5 PC3.4b exécuté et noté (adaptation de la fiche s’il y en a une). ⟶ cocher S15 R5
- [ ] R6 PC3.5 exécuté et noté (adaptation de la fiche s’il y en a une). ⟶ cocher S15 R6
- [ ] R7 PC3.6 exécuté et noté (adaptation de la fiche s’il y en a une). ⟶ cocher S15 R7
- [ ] R8 PC3.7 exécuté et noté (adaptation de la fiche s’il y en a une). ⟶ cocher S15 R8
- [ ] R9 PC3.8 exécuté et noté (adaptation de la fiche s’il y en a une). ⟶ cocher S15 R9
- [ ] R10 Décision écrite dans le rapport : passer, ou corriger d’abord avec, par point KO, l’unité fautive et la correction attendue. ⟶ cocher S15 R10
- [ ] R11 « Statut : TERMINÉ » dans le rapport ⟶ cocher S15 R11

## Prompt de vérification

```text
Tu vérifies l'unité S15 « Porte de l'étape 3 et gel des contrats » du projet GODOT_DEV_MAPPER. Vérification prévue : IA 3 (vérification). Ton numéro d'IA est celui du prompt de créneau. Tu n'es jamais un auteur de l'unité : la commande de prise le contrôle.

PRISE, depuis ton clone principal
python3 suivi/outil.py prendre S15 --ia <n> --verification
- « VÉRIFICATION PRISE » : copie neuve ../verif-S15-porte-3-gel créée sur origin/tache/S15-porte-3-gel, verdict EN COURS écrit, V1 cochée. cd ../verif-S15-porte-3-gel : toute la vérification se fait dans ce dossier.
- « REFUSÉ » : une autre IA vérifie déjà, tu es auteur, ou l'unité n'est pas terminée : reviens au prompt de créneau.
GODOT : même procédure que le prompt de réalisation.
Tu ne modifies aucun fichier de l'unité. Tu écris seulement ton verdict et tes cases V.

TRACE OBLIGATOIRE : après chaque sous-étape V, git add du fichier de verdict, puis python3 suivi/outil.py cocher S15 <V…> --ia <n>. Pour la dernière : --verdict ACCEPTÉE ou --verdict REFUSÉE, identique à la ligne « Verdict » du fichier. Une sous-étape non cochée par cette commande est considérée comme non faite.

1. TRAÇABILITÉ. Chaque case R cochée est signée « — IA n · date » et a son commit sur la branche (git log --oneline origin/main..HEAD). Case cochée sans travail prouvé dans le rapport : refus.
2. PÉRIMÈTRE. git diff --name-only origin/main...HEAD. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S15*.md et suivi/S15-porte-3-gel.md. Tout autre fichier : refus.
3. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : PC3.1, PC3.2, PC3.3, PC3.4, PC3.4b, PC3.5, PC3.6, PC3.7, PC3.8.
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
6. COHÉRENCE. Contrat et invariants concernés.
Relance chaque point automatisable toi-même ; pour les autres, vérifie la preuve citée. La décision suit-elle la règle ?

VERDICT dans rapports/S15-verif-<tentative>.md (créé par la prise) :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte

SI ACCEPTÉE — FUSION, depuis ton clone principal
1. python3 suivi/outil.py fusionner S15 --ia <n> --godot "$B" [--porte-ko si la décision est « corriger d'abord »]
   Elle prend le verrou de main (et attend s'il est pris), fusionne dans ../fusion-S15-porte-3-gel, lance run_all_checks.sh, coche la ligne dans SUIVI.md et la case F1. Si les contrôles échouent : verdict passé à REFUSÉE, main inchangée, verrou rendu ; arrête-toi sur cette unité.
2. cd ../fusion-S15-porte-3-gel ; fais les sous-étapes F suivantes de la fiche, et coche chacune : python3 suivi/outil.py cocher S15 F<k> --ia <n> (commit local, sans poussée).
   Porte KO : dans ../fusion-S15-porte-3-gel, pour chaque point KO : python3 suivi/outil.py correction S15 --fautive <Syy> --titre "<correction>" --realise <n> --verifie <m> --ia <n>.
3. python3 suivi/outil.py publier S15 --ia <n> : dernière case cochée, verifier relancé, main poussée, branche supprimée, verrou rendu.
SI REFUSÉE : arrête-toi sur cette unité ; son auteur la reprendra avec prendre.
```

## Sous-étapes de vérification

Dans `../verif-S15-porte-3-gel`, après chaque sous-étape : `git add` du verdict, puis `python3 suivi/outil.py cocher S15 V<k> --ia <n>`.

- [ ] V1 Prise en charge : `python3 suivi/outil.py prendre S15 --ia <n> --verification` (pas un auteur ; copie neuve `../verif-S15-porte-3-gel` sur `origin/tache/S15-porte-3-gel` ; verdict EN COURS) ⟶ cochée par `prendre`
- [ ] V2 Traçabilité : chaque case R cochée porte une signature « — IA n · date » et un commit sur la branche (`git log --oneline origin/main..HEAD`) ⟶ cocher S15 V2
- [ ] V3.1 PC3.1 relancé ou sa preuve vérifiée. ⟶ cocher S15 V3.1
- [ ] V3.2 PC3.2 relancé ou sa preuve vérifiée. ⟶ cocher S15 V3.2
- [ ] V3.3 PC3.3 relancé ou sa preuve vérifiée. ⟶ cocher S15 V3.3
- [ ] V3.4 PC3.4 relancé ou sa preuve vérifiée. ⟶ cocher S15 V3.4
- [ ] V3.5 PC3.4b relancé ou sa preuve vérifiée. ⟶ cocher S15 V3.5
- [ ] V3.6 PC3.5 relancé ou sa preuve vérifiée. ⟶ cocher S15 V3.6
- [ ] V3.7 PC3.6 relancé ou sa preuve vérifiée. ⟶ cocher S15 V3.7
- [ ] V3.8 PC3.7 relancé ou sa preuve vérifiée. ⟶ cocher S15 V3.8
- [ ] V3.9 PC3.8 relancé ou sa preuve vérifiée. ⟶ cocher S15 V3.9
- [ ] V4 Décision conforme à la règle. ⟶ cocher S15 V4
- [ ] V5 Verdict écrit dans `rapports/S15-verif-<tentative>.md` ⟶ cocher S15 V5 --verdict ACCEPTÉE ou --verdict REFUSÉE

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

F1 et la dernière se cochent par `fusionner` et `publier` ; les autres, dans `../fusion-S15-porte-3-gel`, par `python3 suivi/outil.py cocher S15 F<k> --ia <n>` (commit local).

- [ ] F1 Fusion : `python3 suivi/outil.py fusionner S15 --ia <n> --godot "$B"` (ajoute `--porte-ko` si la décision est « corriger d'abord » : la ligne reste ouverte) : verrou de `main`, fusion `--no-ff` dans `../fusion-S15-porte-3-gel`, `tools/ci/run_all_checks.sh` sur `main` → ALL_CHECKS OK s'il existe (sinon fusion annulée et verdict passé à REFUSÉE), ligne **S15** cochée dans `SUIVI.md` ⟶ cochée par `fusionner`
- [ ] F2 Porte KO : une unité de correction par point KO, créée par `python3 suivi/outil.py correction S15 …` ; porte passée : « sans objet » dans le verdict. ⟶ cocher S15 F2
- [ ] F3 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette ⟶ cocher S15 F3
- [ ] F4 Publication : `python3 suivi/outil.py publier S15 --ia <n>` (verifier OK, `main` poussée, branche `tache/S15-porte-3-gel` supprimée, verrou rendu) ⟶ cochée par `publier`

## Pour la recette

- Confirmer le gel des contrats C-01 à C-07.
