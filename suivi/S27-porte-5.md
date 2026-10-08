# S27 — Porte de l'étape 5

> Fiche d'exécution du mode autonome. Chaque case se coche avec `python3 suivi/outil.py cocher S27 <sous-étape> --ia <n>`, juste après la sous-étape : la commande vérifie l'ordre et l'identité de l'IA, signe la case (IA, date, heure UTC), commite et pousse. Une sous-étape non cochée par cette commande est considérée comme non faite. Règles : `docs/construction/sequence.md`. Avancement : `SUIVI.md` et `suivi/tableau.html`.

| Champ | Valeur |
| --- | --- |
| Réalise | IA 1 (conception) |
| Vérifie | IA 3 (vérification), jamais un auteur de l'unité |
| Piste | Rendez-vous de l'étape 5 : S27 |
| Commence après | S23, S26 (cochées dans `SUIVI.md`) |
| Indépendante de | S28, S29, S30, S31, S33 |
| Branche | `tache/S27-porte-5` |
| Fiche de conception | `docs/construction/etape-5.md`, points de contrôle |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Cette unité appartient au rendez-vous de l'étape 5 : elle attend la fin des pistes 5.A, 5.B. Concrètement, elle attend S23, S26. Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Exécuter chaque point de contrôle de l'étape 5 sur `main` à jour, et noter commande, attendu, obtenu, OK ou KO.
- Décider selon la règle : **passer** si tout est OK (un point « sur ta machine » passe par son équivalent sous écran virtuel, l'humain le revoit à la recette) ; **corriger d'abord** si un point est KO.
- Si un point est KO : la décision est « corriger d'abord », avec, dans le rapport, pour chaque point KO, l'unité fautive et la correction attendue. Le vérificateur fusionne alors avec `fusionner S27 --porte-ko` (la ligne **S27** reste ouverte) et crée une unité de correction par point KO avec `python3 suivi/outil.py correction S27 --fautive <Syy> --titre "<correction>" --realise <n> --verifie <m> --ia <n>`, placée juste avant la porte, dans sa piste. La porte se rejoue quand les corrections sont fusionnées : `prendre` remet ses cases à zéro.

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
Tu réalises l'unité S27 « Porte de l'étape 5 » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.
Réalisation prévue : IA 1 (conception) ; vérification : IA 3 (vérification). Ton numéro d'IA est celui que te donne le prompt de créneau : tu le passes à --ia, et il signe chaque case que tu coches.

AVANT TOUT, depuis ton clone principal du dépôt
1. Lis REGLES_AGENTS.md s'il existe, puis cette fiche : suivi/S27-porte-5.md.
2. python3 suivi/outil.py prendre S27 --ia <n>
   - « PRISE » ou « REPRISE » : tu es sur la branche tache/S27-porte-5 ; commence à la sous-étape affichée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
   - « REFUSÉ » : l'unité n'est pas pour toi maintenant (déjà prise par une autre IA, S23, S26 non cochées, autre IA prévue) : reviens au prompt de créneau et choisis autre chose.

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
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status. Tu ne pousses jamais avec --force.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.
- Une décision réservée à l'humain (docs/construction/sequence.md §5) : arrêt obligatoire, rien d'autre.

TRACE OBLIGATOIRE, après CHAQUE sous-étape et avant la suivante
1. git add <les fichiers de la sous-étape> (jamais git add -A).
2. python3 suivi/outil.py cocher S27 <sous-étape> --ia <n>
   La commande vérifie l'ordre des cases et ton identité, coche la case dans suivi/S27-porte-5.md, la signe (IA, date, heure UTC), commite et pousse sur tache/S27-porte-5.
3. Une sous-étape faite mais non cochée par cette commande est considérée comme non faite : l'IA suivante la refera. Tu ne coches jamais une case à la main.
4. Tu ne modifies jamais SUIVI.md : il ne change qu'à la fusion, sous le verrou de main. Plusieurs IA le lisent en même temps ; aucune ne l'écrit hors de ce verrou.
5. Avant de cocher la dernière sous-étape R : « Statut : TERMINÉ » dans rapports/S27.md, puis git add.
6. Poussée refusée et non rattrapée par la commande : ne force jamais ; git pull --rebase origin tache/S27-porte-5, puis relance la commande.

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

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche ; après chacune, git add puis python3 suivi/outil.py cocher S27 R<k> --ia <n>.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Chaque sous-étape faite est cochée par `cocher`. Complète rapports/S27.md (sorties, « Passation » en cinq lignes au plus), git add, git commit, git push origin HEAD:tache/S27-porte-5.
- git status ne montre aucune modification non commitée ; rien ne reste non poussé.

FORMAT DE rapports/S27.md (créé par prendre ; tu le complètes)
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

Après chaque sous-étape : `git add` de ses fichiers, puis `python3 suivi/outil.py cocher S27 R<k> --ia <n>` (coche, signe, commite, pousse).

- [ ] R0 Prise en charge : `python3 suivi/outil.py prendre S27 --ia <n>` (prérequis cochés dans `SUIVI.md` : S23, S26 ; branche `tache/S27-porte-5` créée ou reprise ; `rapports/S27.md` au statut EN COURS) ⟶ cochée par `prendre`
- [ ] R1 PC5.1 exécuté et noté (adaptation de la fiche s’il y en a une). ⟶ cocher S27 R1
- [ ] R2 PC5.2 exécuté et noté (adaptation de la fiche s’il y en a une). ⟶ cocher S27 R2
- [ ] R3 PC5.3 exécuté et noté (adaptation de la fiche s’il y en a une). ⟶ cocher S27 R3
- [ ] R4 PC5.4 exécuté et noté (adaptation de la fiche s’il y en a une). ⟶ cocher S27 R4
- [ ] R5 PC5.5 exécuté et noté (adaptation de la fiche s’il y en a une). ⟶ cocher S27 R5
- [ ] R6 PC5.6 exécuté et noté (adaptation de la fiche s’il y en a une). ⟶ cocher S27 R6
- [ ] R7 Décision écrite dans le rapport : passer, ou corriger d’abord avec, par point KO, l’unité fautive et la correction attendue. ⟶ cocher S27 R7
- [ ] R8 « Statut : TERMINÉ » dans le rapport ⟶ cocher S27 R8

## Prompt de vérification

```text
Tu vérifies l'unité S27 « Porte de l'étape 5 » du projet GODOT_DEV_MAPPER. Vérification prévue : IA 3 (vérification). Ton numéro d'IA est celui du prompt de créneau. Tu n'es jamais un auteur de l'unité : la commande de prise le contrôle.

PRISE, depuis ton clone principal
python3 suivi/outil.py prendre S27 --ia <n> --verification
- « VÉRIFICATION PRISE » : copie neuve ../verif-S27-porte-5 créée sur origin/tache/S27-porte-5, verdict EN COURS écrit, V1 cochée. cd ../verif-S27-porte-5 : toute la vérification se fait dans ce dossier.
- « REFUSÉ » : une autre IA vérifie déjà, tu es auteur, ou l'unité n'est pas terminée : reviens au prompt de créneau.
GODOT : même procédure que le prompt de réalisation.
Tu ne modifies aucun fichier de l'unité. Tu écris seulement ton verdict et tes cases V.

TRACE OBLIGATOIRE : après chaque sous-étape V, git add du fichier de verdict, puis python3 suivi/outil.py cocher S27 <V…> --ia <n>. Pour la dernière : --verdict ACCEPTÉE ou --verdict REFUSÉE, identique à la ligne « Verdict » du fichier. Une sous-étape non cochée par cette commande est considérée comme non faite.

1. TRAÇABILITÉ. Chaque case R cochée est signée « — IA n · date » et a son commit sur la branche (git log --oneline origin/main..HEAD). Case cochée sans travail prouvé dans le rapport : refus.
2. PÉRIMÈTRE. git diff --name-only origin/main...HEAD. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S27*.md et suivi/S27-porte-5.md. Tout autre fichier : refus.
3. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : PC5.1, PC5.2, PC5.3, PC5.4, PC5.5, PC5.6.
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

VERDICT dans rapports/S27-verif-<tentative>.md (créé par la prise) :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte

SI ACCEPTÉE — FUSION, depuis ton clone principal
1. python3 suivi/outil.py fusionner S27 --ia <n> --godot "$B" [--porte-ko si la décision est « corriger d'abord »]
   Elle prend le verrou de main (et attend s'il est pris), fusionne dans ../fusion-S27-porte-5, lance run_all_checks.sh, coche la ligne dans SUIVI.md et la case F1. Si les contrôles échouent : verdict passé à REFUSÉE, main inchangée, verrou rendu ; arrête-toi sur cette unité.
2. cd ../fusion-S27-porte-5 ; fais les sous-étapes F suivantes de la fiche, et coche chacune : python3 suivi/outil.py cocher S27 F<k> --ia <n> (commit local, sans poussée).
   Porte KO : dans ../fusion-S27-porte-5, pour chaque point KO : python3 suivi/outil.py correction S27 --fautive <Syy> --titre "<correction>" --realise <n> --verifie <m> --ia <n>.
3. python3 suivi/outil.py publier S27 --ia <n> : dernière case cochée, verifier relancé, main poussée, branche supprimée, verrou rendu.
SI REFUSÉE : arrête-toi sur cette unité ; son auteur la reprendra avec prendre.
```

## Sous-étapes de vérification

Dans `../verif-S27-porte-5`, après chaque sous-étape : `git add` du verdict, puis `python3 suivi/outil.py cocher S27 V<k> --ia <n>`.

- [ ] V1 Prise en charge : `python3 suivi/outil.py prendre S27 --ia <n> --verification` (pas un auteur ; copie neuve `../verif-S27-porte-5` sur `origin/tache/S27-porte-5` ; verdict EN COURS) ⟶ cochée par `prendre`
- [ ] V2 Traçabilité : chaque case R cochée porte une signature « — IA n · date » et un commit sur la branche (`git log --oneline origin/main..HEAD`) ⟶ cocher S27 V2
- [ ] V3.1 PC5.1 relancé ou sa preuve vérifiée. ⟶ cocher S27 V3.1
- [ ] V3.2 PC5.2 relancé ou sa preuve vérifiée. ⟶ cocher S27 V3.2
- [ ] V3.3 PC5.3 relancé ou sa preuve vérifiée. ⟶ cocher S27 V3.3
- [ ] V3.4 PC5.4 relancé ou sa preuve vérifiée. ⟶ cocher S27 V3.4
- [ ] V3.5 PC5.5 relancé ou sa preuve vérifiée. ⟶ cocher S27 V3.5
- [ ] V3.6 PC5.6 relancé ou sa preuve vérifiée. ⟶ cocher S27 V3.6
- [ ] V4 Décision conforme à la règle. ⟶ cocher S27 V4
- [ ] V5 Verdict écrit dans `rapports/S27-verif-<tentative>.md` ⟶ cocher S27 V5 --verdict ACCEPTÉE ou --verdict REFUSÉE

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

F1 et la dernière se cochent par `fusionner` et `publier` ; les autres, dans `../fusion-S27-porte-5`, par `python3 suivi/outil.py cocher S27 F<k> --ia <n>` (commit local).

- [ ] F1 Fusion : `python3 suivi/outil.py fusionner S27 --ia <n> --godot "$B"` (ajoute `--porte-ko` si la décision est « corriger d'abord » : la ligne reste ouverte) : verrou de `main`, fusion `--no-ff` dans `../fusion-S27-porte-5`, `tools/ci/run_all_checks.sh` sur `main` → ALL_CHECKS OK s'il existe (sinon fusion annulée et verdict passé à REFUSÉE), ligne **S27** cochée dans `SUIVI.md` ⟶ cochée par `fusionner`
- [ ] F2 Porte KO : une unité de correction par point KO, créée par `python3 suivi/outil.py correction S27 …` ; porte passée : « sans objet » dans le verdict. ⟶ cocher S27 F2
- [ ] F3 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette ⟶ cocher S27 F3
- [ ] F4 Publication : `python3 suivi/outil.py publier S27 --ia <n>` (verifier OK, `main` poussée, branche `tache/S27-porte-5` supprimée, verrou rendu) ⟶ cochée par `publier`

## Pour la recette

Rien de propre à cette unité.
