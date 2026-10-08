# S09 — Porte de l'étape 1

> Fiche d'exécution du mode autonome. Chaque case se coche avec `python3 suivi/outil.py cocher S09 <sous-étape> --ia <n>`, juste après la sous-étape : la commande vérifie l'ordre et l'identité de l'IA, signe la case (IA, date, heure UTC), commite et pousse. Une sous-étape non cochée par cette commande est considérée comme non faite. Règles : `docs/construction/sequence.md`. Avancement : `SUIVI.md` et `suivi/tableau.html`.

| Champ | Valeur |
| --- | --- |
| Réalise | IA 1 (conception) |
| Vérifie | IA 3 (vérification), jamais un auteur de l'unité |
| Piste | Rendez-vous de l'étape 1 : S09 |
| Commence après | S06, S08 (cochées dans `SUIVI.md`) |
| Indépendante de | S10, S11 |
| Branche | `tache/S09-porte-1` |
| Fiche de conception | `docs/construction/etape-1.md`, points de contrôle |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Cette unité appartient au rendez-vous de l'étape 1 : elle attend la fin des pistes 1.A, 1.B. Concrètement, elle attend S06, S08. Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Exécuter chaque point de contrôle de l'étape 1 sur `main` à jour, et noter commande, attendu, obtenu, OK ou KO.
- Décider selon la règle : **passer** si tout est OK (un point « sur ta machine » passe par son équivalent sous écran virtuel, l'humain le revoit à la recette) ; **corriger d'abord** si un point est KO.
- Si un point est KO : la décision est « corriger d'abord », avec, dans le rapport, pour chaque point KO, l'unité fautive et la correction attendue. La ligne « - Décision : CORRIGER D'ABORD » du rapport (« - Décision : PASSER » sinon) commande la fusion : `fusionner S09 --ia <n>` laisse alors la ligne **S09** ouverte, et le vérificateur crée une unité de correction par point KO avec `python3 suivi/outil.py correction S09 --fautive <Syy> --titre "<correction>" --realise <n> --verifie <m> --ia <n>`, placée juste avant la porte, dans sa piste. La porte se rejoue quand les corrections sont fusionnées : `prendre` remet ses cases à zéro.

## Fichiers autorisés

`rapports/S09.md`.

## Points de contrôle de l'étape (copie du guide)

| ID | Contrôle | Commande ou preuve | Attendu | Adaptation |
| --- | --- | --- | --- | --- |
| PC1.1 | Import | `godot --headless --path . --import` | Code 0 | — |
| PC1.2 | Chargement du plugin | `GDM_TRACE_LIFECYCLE=1 godot --headless --editor --path . --quit-after 300 > /tmp/ed.out 2>&1`, puis compter `GDM_PLUGIN_ENTER`, `GDM_PLUGIN_EXIT` et les lignes `^(ERROR\|SCRIPT ERROR)` | 1, 1, 0 | — |
| PC1.3 | Tests | `godot --headless --path . -s res://tests/run_all.gd` | Code 0 et ligne `GDM_TESTS … failed=0` | — |
| PC1.4 | (CE) Échec détecté | Même commande avec `GDM_SELFTEST_FAIL=1` | Code non nul | — |
| PC1.5 | Dépendances | `python3 tools/check_deps.py`, puis le même script sur `tools/check_deps_fixtures` | Code 0, puis code 1 | — |
| PC1.6 | Style | `gdlint addons tests` et `gdformat --check addons tests` | Codes 0 | — |
| PC1.7 | Tout en une commande | `GODOT=<binaire> tools/ci/run_all_checks.sh` | Code 0 et `ALL_CHECKS OK` | — |
| PC1.8 | CI distante | Dernier passage sur GitHub après envoi | Job stable vert ; job préversion exécuté | Si GitHub Actions ne s'exécute pas sur le dépôt : noter PC1.8 dans la liste de recette ; PC1.7 en local fait foi. |
| PC1.9 | Banc d'essai | `python3 tools/check_benches.py`, puis import de la copie de travail sur 4.7.2 | Code 0 ; aucune ligne d'erreur nouvelle | — |
| PC1.10 | (CE) Contrôles ajoutés | Déposer dans `tools/ci/checks.d/` un script qui sort en 1, relancer PC1.7 | Code 1, puis 0 une fois le script retiré | — |

## Prompt de réalisation

```text
Tu réalises l'unité S09 « Porte de l'étape 1 » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.
Réalisation prévue : IA 1 (conception) ; vérification : IA 3 (vérification). Ton numéro d'IA est celui que te donne le prompt de créneau : tu le passes à --ia, et il signe chaque case que tu coches.

AVANT TOUT, depuis ton clone principal du dépôt
1. Lis REGLES_AGENTS.md s'il existe, puis cette fiche : suivi/S09-porte-1.md.
2. python3 suivi/outil.py prendre S09 --ia <n>
   - « PRISE » ou « REPRISE » : tu es sur la branche tache/S09-porte-1 ; commence à la sous-étape affichée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
   - « REFUSÉ » : l'unité n'est pas pour toi maintenant (déjà prise par une autre IA, S06, S08 non cochées, autre IA prévue) : reviens au prompt de créneau et choisis autre chose.

GODOT
- Si tools/ci/fetch_godot.sh existe : B=$(tools/ci/fetch_godot.sh 4.7.2-stable)
- Sinon, hors du dépôt :
  D=$HOME/.cache/gdm-godot/4.7.2-stable ; mkdir -p "$D"
  test -x "$D/Godot_v4.7.2-stable_linux.x86_64" || { curl -sSL -o /tmp/godot-4.7.2.zip https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip && unzip -o -q /tmp/godot-4.7.2.zip -d "$D"; }
  B=$D/Godot_v4.7.2-stable_linux.x86_64
- « godot » dans les commandes désigne "$B". Contrôle : "$B" --version contient 4.7.2.stable.
- Éditeur avec rendu, quand la fiche le demande : xvfb-run -a -s "-screen 0 1600x900x24" "$B" --editor --path <projet> --rendering-driver opengl3

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S09.md et les cases de suivi/S09-porte-1.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status. Tu ne pousses jamais avec --force.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.
- Une décision réservée à l'humain (docs/construction/sequence.md §5) : arrêt obligatoire, rien d'autre : python3 suivi/outil.py arreter --ia <n> --unite S09 --raison "<raison>", puis fin du créneau.

TRACE OBLIGATOIRE, après CHAQUE sous-étape et avant la suivante
1. git add <les fichiers de la sous-étape> (jamais git add -A).
2. python3 suivi/outil.py cocher S09 <sous-étape> --ia <n>
   La commande vérifie l'ordre des cases et ton identité, coche la case dans suivi/S09-porte-1.md, la signe (IA, date, heure UTC), commite et pousse sur tache/S09-porte-1.
3. Une sous-étape faite mais non cochée par cette commande est considérée comme non faite : l'IA suivante la refera. Tu ne coches jamais une case à la main.
4. Tu ne modifies jamais SUIVI.md : il ne change qu'à la fusion, sous le verrou de main. Plusieurs IA le lisent en même temps ; aucune ne l'écrit hors de ce verrou.
5. Avant de cocher la dernière sous-étape R : « Statut : TERMINÉ » dans rapports/S09.md, puis git add.
6. Poussée refusée et non rattrapée par la commande : ne force jamais ; git pull --rebase origin tache/S09-porte-1, puis relance la commande.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (docs/construction/README.md, prompt de porte d'étape)
Prépare la porte de sortie de l'étape 1 du projet GODOT_DEV_MAPPER. Entrées : docs/construction/etape-1.md, les verdicts de vérification de chaque tâche, PROJECT_STATE.md.
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
- PC1.8 : Si GitHub Actions ne s'exécute pas sur le dépôt : noter PC1.8 dans la liste de recette ; PC1.7 en local fait foi.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche ; après chacune, git add puis python3 suivi/outil.py cocher S09 R<k> --ia <n>.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Chaque sous-étape faite est cochée par `cocher`. Complète rapports/S09.md (sorties, « Passation » en cinq lignes au plus), git add, git commit, git push origin HEAD:tache/S09-porte-1.
- git status ne montre aucune modification non commitée ; rien ne reste non poussé.

FORMAT DE rapports/S09.md (créé par prendre ; tu le complètes)
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

Après chaque sous-étape : `git add` de ses fichiers, puis `python3 suivi/outil.py cocher S09 R<k> --ia <n>` (coche, signe, commite, pousse).

- [ ] R0 Prise en charge : `python3 suivi/outil.py prendre S09 --ia <n>` (prérequis cochés dans `SUIVI.md` : S06, S08 ; branche `tache/S09-porte-1` créée ou reprise ; `rapports/S09.md` au statut EN COURS) ⟶ cochée par `prendre`
- [ ] R1 PC1.1 exécuté et noté (adaptation de la fiche s’il y en a une). ⟶ cocher S09 R1
- [ ] R2 PC1.2 exécuté et noté (adaptation de la fiche s’il y en a une). ⟶ cocher S09 R2
- [ ] R3 PC1.3 exécuté et noté (adaptation de la fiche s’il y en a une). ⟶ cocher S09 R3
- [ ] R4 PC1.4 exécuté et noté (adaptation de la fiche s’il y en a une). ⟶ cocher S09 R4
- [ ] R5 PC1.5 exécuté et noté (adaptation de la fiche s’il y en a une). ⟶ cocher S09 R5
- [ ] R6 PC1.6 exécuté et noté (adaptation de la fiche s’il y en a une). ⟶ cocher S09 R6
- [ ] R7 PC1.7 exécuté et noté (adaptation de la fiche s’il y en a une). ⟶ cocher S09 R7
- [ ] R8 PC1.8 exécuté et noté (adaptation de la fiche s’il y en a une). ⟶ cocher S09 R8
- [ ] R9 PC1.9 exécuté et noté (adaptation de la fiche s’il y en a une). ⟶ cocher S09 R9
- [ ] R10 PC1.10 exécuté et noté (adaptation de la fiche s’il y en a une). ⟶ cocher S09 R10
- [ ] R11 Décision écrite dans le rapport, sur la ligne « - Décision : PASSER » ou « - Décision : CORRIGER D'ABORD » (la commande `cocher` de la dernière case R la contrôle) ; si corriger d’abord : par point KO, l’unité fautive et la correction attendue. ⟶ cocher S09 R11
- [ ] R12 « Statut : TERMINÉ » dans le rapport ⟶ cocher S09 R12

## Prompt de vérification

```text
Tu vérifies l'unité S09 « Porte de l'étape 1 » du projet GODOT_DEV_MAPPER. Vérification prévue : IA 3 (vérification). Ton numéro d'IA est celui du prompt de créneau. Tu n'es jamais un auteur de l'unité : la commande de prise le contrôle.

PRISE, depuis ton clone principal
python3 suivi/outil.py prendre S09 --ia <n> --verification
- « VÉRIFICATION PRISE » : copie neuve ../verif-S09-porte-1 créée sur origin/tache/S09-porte-1, verdict EN COURS écrit, V1 cochée. cd ../verif-S09-porte-1 : toute la vérification se fait dans ce dossier.
- « REFUSÉ » : une autre IA vérifie déjà, tu es auteur, ou l'unité n'est pas terminée : reviens au prompt de créneau.
- Créneau fini avant le verdict : au créneau suivant, etat te propose la même commande ; elle recrée la copie (« VÉRIFICATION REPRISE ») et tu reprends à la première case V ouverte.
GODOT : même procédure que le prompt de réalisation.
Tu ne modifies aucun fichier de l'unité. Tu écris seulement ton verdict et tes cases V.

TRACE OBLIGATOIRE : après chaque sous-étape V, git add du fichier de verdict, puis python3 suivi/outil.py cocher S09 <V…> --ia <n>. Pour la dernière : --verdict ACCEPTÉE ou --verdict REFUSÉE, identique à la ligne « Verdict » du fichier. Une sous-étape non cochée par cette commande est considérée comme non faite.

1. TRAÇABILITÉ. Chaque case R cochée est signée « — IA n · date » et a son commit sur la branche (git log --oneline origin/main..HEAD). Case cochée sans travail prouvé dans le rapport : refus.
2. PÉRIMÈTRE. git diff --name-only origin/main...HEAD. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S09*.md et suivi/S09-porte-1.md. Tout autre fichier : refus.
3. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : PC1.1, PC1.2, PC1.3, PC1.4, PC1.5, PC1.6, PC1.7, PC1.8, PC1.9, PC1.10.
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

VERDICT dans rapports/S09-verif-<tentative>.md (créé par la prise) :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte

SI ACCEPTÉE — FUSION, depuis ton clone principal (cd hors de ../verif-S09-porte-1)
1. python3 suivi/outil.py fusionner S09 --ia <n>   (la ligne « Décision » du rapport fait foi : CORRIGER D'ABORD laisse la ligne de la porte ouverte)
   Elle trouve Godot (--godot, $GODOT, cache du bloc GODOT ou tools/ci/fetch_godot.sh ; sans Godot : REFUSÉ, verdict inchangé), prend le verrou de main (et attend s'il est pris), revérifie l'unité, fusionne dans ../fusion-S09-porte-1, lance run_all_checks.sh, coche la ligne dans SUIVI.md et la case F1. Si les contrôles échouent : verdict passé à REFUSÉE, main inchangée, verrou rendu ; arrête-toi sur cette unité. La fusion te revient parce que tu as signé le verdict ; une autre IA ne la fait qu'après 12 h.
2. cd ../fusion-S09-porte-1 ; fais les sous-étapes F suivantes de la fiche, et coche chacune : python3 suivi/outil.py cocher S09 F<k> --ia <n> (commit local, sans poussée).
   Porte KO : dans ../fusion-S09-porte-1, pour chaque point KO : python3 suivi/outil.py correction S09 --fautive <Syy> --titre "<correction>" --realise <n> --verifie <m> --ia <n>.
3. python3 suivi/outil.py publier S09 --ia <n> : dernière case cochée, verifier relancé, main poussée, branche supprimée, verrou rendu.
SI REFUSÉE : arrête-toi sur cette unité ; son auteur la reprendra avec prendre.
```

## Sous-étapes de vérification

Dans `../verif-S09-porte-1`, après chaque sous-étape : `git add` du verdict, puis `python3 suivi/outil.py cocher S09 V<k> --ia <n>`.

- [ ] V1 Prise en charge : `python3 suivi/outil.py prendre S09 --ia <n> --verification` (pas un auteur ; copie neuve `../verif-S09-porte-1` sur `origin/tache/S09-porte-1` ; verdict EN COURS) ⟶ cochée par `prendre`
- [ ] V2 Traçabilité : chaque case R cochée porte une signature « — IA n · date » et un commit sur la branche (`git log --oneline origin/main..HEAD`) ⟶ cocher S09 V2
- [ ] V3.1 PC1.1 relancé ou sa preuve vérifiée. ⟶ cocher S09 V3.1
- [ ] V3.2 PC1.2 relancé ou sa preuve vérifiée. ⟶ cocher S09 V3.2
- [ ] V3.3 PC1.3 relancé ou sa preuve vérifiée. ⟶ cocher S09 V3.3
- [ ] V3.4 PC1.4 relancé ou sa preuve vérifiée. ⟶ cocher S09 V3.4
- [ ] V3.5 PC1.5 relancé ou sa preuve vérifiée. ⟶ cocher S09 V3.5
- [ ] V3.6 PC1.6 relancé ou sa preuve vérifiée. ⟶ cocher S09 V3.6
- [ ] V3.7 PC1.7 relancé ou sa preuve vérifiée. ⟶ cocher S09 V3.7
- [ ] V3.8 PC1.8 relancé ou sa preuve vérifiée. ⟶ cocher S09 V3.8
- [ ] V3.9 PC1.9 relancé ou sa preuve vérifiée. ⟶ cocher S09 V3.9
- [ ] V3.10 PC1.10 relancé ou sa preuve vérifiée. ⟶ cocher S09 V3.10
- [ ] V4 Décision conforme à la règle. ⟶ cocher S09 V4
- [ ] V5 Verdict écrit dans `rapports/S09-verif-<tentative>.md` ⟶ cocher S09 V5 --verdict ACCEPTÉE ou --verdict REFUSÉE

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

F1 et la dernière se cochent par `fusionner` et `publier` ; les autres, dans `../fusion-S09-porte-1`, par `python3 suivi/outil.py cocher S09 F<k> --ia <n>` (commit local).

- [ ] F1 Fusion, depuis le clone principal : `python3 suivi/outil.py fusionner S09 --ia <n>` (la décision du rapport fait foi : « CORRIGER D'ABORD » laisse la ligne ouverte) : Godot trouvé seul (--godot, $GODOT, cache du bloc GODOT ou fetch_godot.sh), verrou de `main`, fusion `--no-ff` dans `../fusion-S09-porte-1`, `tools/ci/run_all_checks.sh` sur `main` → ALL_CHECKS OK s'il existe (sinon fusion annulée et verdict passé à REFUSÉE), ligne **S09** cochée dans `SUIVI.md` ⟶ cochée par `fusionner`
- [ ] F2 Porte KO : une unité de correction par point KO, créée par `python3 suivi/outil.py correction S09 …` ; porte passée : « sans objet » dans le verdict. ⟶ cocher S09 F2
- [ ] F3 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette ⟶ cocher S09 F3
- [ ] F4 Publication : `python3 suivi/outil.py publier S09 --ia <n>` (verifier OK, `main` poussée, branche `tache/S09-porte-1` supprimée, verrou rendu) ⟶ cochée par `publier`

## Pour la recette

Rien de propre à cette unité.
