# S31 — Démonstration sous écran virtuel (PC6.7)

> Fiche d'exécution du mode autonome. Chaque case se coche avec `python3 suivi/outil.py cocher S31 <sous-étape> --ia <n>`, juste après la sous-étape : la commande vérifie l'ordre et l'identité de l'IA, signe la case (IA, date, heure UTC), commite et pousse. Une sous-étape non cochée par cette commande est considérée comme non faite. Règles : `docs/construction/sequence.md`. Avancement : `SUIVI.md` et `suivi/tableau.html`.

| Champ | Valeur |
| --- | --- |
| Réalise | IA 2 (développement) |
| Vérifie | IA 3 (vérification), jamais un auteur de l'unité |
| Piste | 6.A Panneau et chemin observé : S28 → S29 → S31 (unité 3 sur 3) |
| Commence après | S28, S29, S30 (cochées dans `SUIVI.md`) |
| Indépendante de | S22, S23, S26, S27, S33 |
| Branche | `tache/S31-demonstration` |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Cette unité est la 3e de la piste 6.A « Panneau et chemin observé », dont les unités se font à la suite. Les autres pistes de la section (6.B) avancent en même temps, chacune de son côté. Elle attend S29, l'unité précédente de la piste. Elle attend aussi S30, hors de la piste. Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Sous écran virtuel, ouvrir l'éditeur avec le plugin sur le banc instrumenté, jouer une session, et produire des captures du panneau : deux instances distinguées, trois états du chemin observé, ouverture du code à la bonne ligne.
- Mesurer l'aller-retour et le délai réception → affichage, marqués « rendu logiciel ».

## Fichiers autorisés

`tests/integration/run_demo.sh`, `tools/harness/editor_driver/` (scénario de démonstration), `rapports/S31/` (captures PNG), `docs/mesures/latence-poc.md`.

Toujours autorisés en plus : `rapports/S31*.md` et les cases de cette fiche (par `cocher`).

## Contrôles propres à cette fiche

- `S31-a` : `tests/integration/run_demo.sh; echo $?` → 0 et une ligne OPEN avec la ligne de l'ancrage
- `S31-b` : `ls rapports/S31/*.png | wc -l` → au moins 4
- (CE) Ignorer le filtre d'instance dans la projection : le test de projection échoue et la capture ne distingue plus les instances ; annuler.

## Prompt de réalisation

```text
Tu réalises l'unité S31 « Démonstration sous écran virtuel (PC6.7) » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.
Réalisation prévue : IA 2 (développement) ; vérification : IA 3 (vérification). Ton numéro d'IA est celui que te donne le prompt de créneau : tu le passes à --ia, et il signe chaque case que tu coches.

AVANT TOUT, depuis ton clone principal du dépôt
1. Lis REGLES_AGENTS.md s'il existe, puis cette fiche : suivi/S31-demonstration.md.
2. python3 suivi/outil.py prendre S31 --ia <n>
   - « PRISE » ou « REPRISE » : tu es sur la branche tache/S31-demonstration ; commence à la sous-étape affichée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
   - « REFUSÉ » : l'unité n'est pas pour toi maintenant (déjà prise par une autre IA, S28, S29, S30 non cochées, autre IA prévue) : reviens au prompt de créneau et choisis autre chose.

GODOT
- Si tools/ci/fetch_godot.sh existe : B=$(tools/ci/fetch_godot.sh 4.7.2-stable)
- Sinon, hors du dépôt :
  D=$HOME/.cache/gdm-godot/4.7.2-stable ; mkdir -p "$D"
  test -x "$D/Godot_v4.7.2-stable_linux.x86_64" || { curl -sSL -o /tmp/godot-4.7.2.zip https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip && unzip -o -q /tmp/godot-4.7.2.zip -d "$D"; }
  B=$D/Godot_v4.7.2-stable_linux.x86_64
- « godot » dans les commandes désigne "$B". Contrôle : "$B" --version contient 4.7.2.stable.
- Éditeur avec rendu, quand la fiche le demande : xvfb-run -a -s "-screen 0 1600x900x24" "$B" --editor --path <projet> --rendering-driver opengl3

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S31.md et les cases de suivi/S31-demonstration.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status. Tu ne pousses jamais avec --force.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.
- Une décision réservée à l'humain (docs/construction/sequence.md §5) : arrêt obligatoire, rien d'autre : python3 suivi/outil.py arreter --ia <n> --unite S31 --raison "<raison>", puis fin du créneau.

TRACE OBLIGATOIRE, après CHAQUE sous-étape et avant la suivante
1. git add <les fichiers de la sous-étape> (jamais git add -A).
2. python3 suivi/outil.py cocher S31 <sous-étape> --ia <n>
   La commande vérifie l'ordre des cases et ton identité, coche la case dans suivi/S31-demonstration.md, la signe (IA, date, heure UTC), commite et pousse sur tache/S31-demonstration.
3. Une sous-étape faite mais non cochée par cette commande est considérée comme non faite : l'IA suivante la refera. Tu ne coches jamais une case à la main.
4. Tu ne modifies jamais SUIVI.md : il ne change qu'à la fusion, sous le verrou de main. Plusieurs IA le lisent en même temps ; aucune ne l'écrit hors de ce verrou.
5. Avant de cocher la dernière sous-étape R : « Statut : TERMINÉ » dans rapports/S31.md, puis git add.
6. Poussée refusée et non rattrapée par la commande : ne force jamais ; git pull --rebase origin tache/S31-demonstration, puis relance la commande.

TRAVAIL TECHNIQUE — début (rédigé pour le mode autonome)
Tu réalises la démonstration PC6.7 du projet GODOT_DEV_MAPPER, sans humain, sous écran virtuel.
CONTEXTE : docs/construction/etape-6.md (PC6.7, T16, T17), rapports de S28 et S29 (procédures), tools/harness/editor_driver/ (S26).
OBJECTIF
1. Étendre tools/harness/editor_driver/ : une fois la session reçue, sélectionner chaque instance, choisir une invocation, ouvrir le code par le panneau, et capturer le viewport de l'éditeur (get_viewport().get_texture().get_image().save_png) dans rapports/S31/.
2. tests/integration/run_demo.sh : lance tout sous xvfb-run, sur une copie temporaire de banc/<nom>-instrumentation, et affiche la ligne de script ouverte par l'éditeur (« OPEN res://…:ligne »).
3. Captures attendues : deux instances distinguées ; un chemin « cohérent », un « indéterminé — trace incomplète » (session à trou rejouée), un « incohérent » (fixture) ; le code ouvert à la ligne de l'ancrage.
4. docs/mesures/latence-poc.md : aller-retour et délai réception → affichage, 95e centile sur la session, latence estimée ; mention « rendu logiciel, non représentatif d'un GPU ».
CONTRÔLES
S31-a  tests/integration/run_demo.sh ; echo $?   → 0 et une ligne OPEN avec la ligne de l'ancrage
S31-b  ls rapports/S31/*.png | wc -l   → au moins 4
CONTRE-ÉPREUVE (CE) pour le vérificateur : faire ignorer le filtre d'instance au panneau → la capture des deux instances ne les distingue plus, et le test de projection échoue.
TRAVAIL TECHNIQUE — fin

CONTRÔLES DE LA FICHE
S31-a  tests/integration/run_demo.sh; echo $?   → 0 et une ligne OPEN avec la ligne de l'ancrage
S31-b  ls rapports/S31/*.png | wc -l   → au moins 4
(CE) Ignorer le filtre d'instance dans la projection : le test de projection échoue et la capture ne distingue plus les instances ; annuler.

ADAPTATIONS DU MODE AUTONOME
- Aucune : suis le travail technique tel quel.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche ; après chacune, git add puis python3 suivi/outil.py cocher S31 R<k> --ia <n>.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Chaque sous-étape faite est cochée par `cocher`. Complète rapports/S31.md (sorties, « Passation » en cinq lignes au plus), git add, git commit, git push origin HEAD:tache/S31-demonstration.
- git status ne montre aucune modification non commitée ; rien ne reste non poussé.

FORMAT DE rapports/S31.md (créé par prendre ; tu le complètes)
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

Après chaque sous-étape : `git add` de ses fichiers, puis `python3 suivi/outil.py cocher S31 R<k> --ia <n>` (coche, signe, commite, pousse).

- [ ] R0 Prise en charge : `python3 suivi/outil.py prendre S31 --ia <n>` (prérequis cochés dans `SUIVI.md` : S28, S29, S30 ; branche `tache/S31-demonstration` créée ou reprise ; `rapports/S31.md` au statut EN COURS) ⟶ cochée par `prendre`
- [ ] R1 Étendre `tools/harness/editor_driver/` : sélection d'instance, choix d'une invocation, ouverture du code, capture du viewport de l'éditeur. ⟶ cocher S31 R1
- [ ] R2 Écrire `tests/integration/run_demo.sh`. ⟶ cocher S31 R2
- [ ] R3 Produire les captures dans `rapports/S31/` : deux instances, trois états (fixtures « cohérent », « trou », « incohérent »), code ouvert à la bonne ligne. ⟶ cocher S31 R3
- [ ] R4 Écrire `docs/mesures/latence-poc.md` : aller-retour, délai réception → affichage, 95e centile, mention « rendu logiciel ». ⟶ cocher S31 R4
- [ ] R5 Contrôles finaux : S31-a, S31-b exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » dans le rapport ⟶ cocher S31 R5

## Prompt de vérification

```text
Tu vérifies l'unité S31 « Démonstration sous écran virtuel (PC6.7) » du projet GODOT_DEV_MAPPER. Vérification prévue : IA 3 (vérification). Ton numéro d'IA est celui du prompt de créneau. Tu n'es jamais un auteur de l'unité : la commande de prise le contrôle.

PRISE, depuis ton clone principal
python3 suivi/outil.py prendre S31 --ia <n> --verification
- « VÉRIFICATION PRISE » : copie neuve ../verif-S31-demonstration créée sur origin/tache/S31-demonstration, verdict EN COURS écrit, V1 cochée. cd ../verif-S31-demonstration : toute la vérification se fait dans ce dossier.
- « REFUSÉ » : une autre IA vérifie déjà, tu es auteur, ou l'unité n'est pas terminée : reviens au prompt de créneau.
- Créneau fini avant le verdict : au créneau suivant, etat te propose la même commande ; elle recrée la copie (« VÉRIFICATION REPRISE ») et tu reprends à la première case V ouverte.
GODOT : même procédure que le prompt de réalisation.
Tu ne modifies aucun fichier de l'unité. Tu écris seulement ton verdict et tes cases V.

TRACE OBLIGATOIRE : après chaque sous-étape V, git add du fichier de verdict, puis python3 suivi/outil.py cocher S31 <V…> --ia <n>. Pour la dernière : --verdict ACCEPTÉE ou --verdict REFUSÉE, identique à la ligne « Verdict » du fichier. Une sous-étape non cochée par cette commande est considérée comme non faite.

1. TRAÇABILITÉ. Chaque case R cochée est signée « — IA n · date » et a son commit sur la branche (git log --oneline origin/main..HEAD). Case cochée sans travail prouvé dans le rapport : refus.
2. PÉRIMÈTRE. git diff --name-only origin/main...HEAD. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S31*.md et suivi/S31-demonstration.md. Tout autre fichier : refus.
3. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : S31-a, S31-b.
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
6. COHÉRENCE. Plan §7 (pas de graphe dessiné au POC) ; états jamais portés par la seule couleur ; jamais « cause ».
Le vérificateur ouvre chaque capture et décrit ce qu'il voit dans son verdict.

VERDICT dans rapports/S31-verif-<tentative>.md (créé par la prise) :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte

SI ACCEPTÉE — FUSION, depuis ton clone principal (cd hors de ../verif-S31-demonstration)
1. python3 suivi/outil.py fusionner S31 --ia <n>
   Elle trouve Godot (--godot, $GODOT, cache du bloc GODOT ou tools/ci/fetch_godot.sh ; sans Godot : REFUSÉ, verdict inchangé), prend le verrou de main (et attend s'il est pris), revérifie l'unité, fusionne dans ../fusion-S31-demonstration, lance run_all_checks.sh, coche la ligne dans SUIVI.md et la case F1. Si les contrôles échouent : verdict passé à REFUSÉE, main inchangée, verrou rendu ; arrête-toi sur cette unité. La fusion te revient parce que tu as signé le verdict ; une autre IA ne la fait qu'après 12 h.
2. cd ../fusion-S31-demonstration ; fais les sous-étapes F suivantes de la fiche, et coche chacune : python3 suivi/outil.py cocher S31 F<k> --ia <n> (commit local, sans poussée).
3. python3 suivi/outil.py publier S31 --ia <n> : dernière case cochée, verifier relancé, main poussée, branche supprimée, verrou rendu.
SI REFUSÉE : arrête-toi sur cette unité ; son auteur la reprendra avec prendre.
```

## Sous-étapes de vérification

Dans `../verif-S31-demonstration`, après chaque sous-étape : `git add` du verdict, puis `python3 suivi/outil.py cocher S31 V<k> --ia <n>`.

- [ ] V1 Prise en charge : `python3 suivi/outil.py prendre S31 --ia <n> --verification` (pas un auteur ; copie neuve `../verif-S31-demonstration` sur `origin/tache/S31-demonstration` ; verdict EN COURS) ⟶ cochée par `prendre`
- [ ] V2 Traçabilité : chaque case R cochée porte une signature « — IA n · date » et un commit sur la branche (`git log --oneline origin/main..HEAD`) ⟶ cocher S31 V2
- [ ] V3 Périmètre : `git diff --name-only origin/main...HEAD` ⊂ fichiers autorisés. ⟶ cocher S31 V3
- [ ] V4.1 Contrôle S31-a relancé, résultat conforme. ⟶ cocher S31 V4.1
- [ ] V4.2 Contrôle S31-b relancé, résultat conforme. ⟶ cocher S31 V4.2
- [ ] V5 Contre-épreuves (CE) appliquées et détectées, puis annulées. ⟶ cocher S31 V5
- [ ] V6 Contournements cherchés. ⟶ cocher S31 V6
- [ ] V7 Cohérence avec les contrats et les invariants. ⟶ cocher S31 V7
- [ ] V8 Verdict écrit dans `rapports/S31-verif-<tentative>.md` ⟶ cocher S31 V8 --verdict ACCEPTÉE ou --verdict REFUSÉE

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

F1 et la dernière se cochent par `fusionner` et `publier` ; les autres, dans `../fusion-S31-demonstration`, par `python3 suivi/outil.py cocher S31 F<k> --ia <n>` (commit local).

- [ ] F1 Fusion, depuis le clone principal : `python3 suivi/outil.py fusionner S31 --ia <n>` : Godot trouvé seul (--godot, $GODOT, cache du bloc GODOT ou fetch_godot.sh), verrou de `main`, fusion `--no-ff` dans `../fusion-S31-demonstration`, `tools/ci/run_all_checks.sh` sur `main` → ALL_CHECKS OK s'il existe (sinon fusion annulée et verdict passé à REFUSÉE), ligne **S31** cochée dans `SUIVI.md` ⟶ cochée par `fusionner`
- [ ] F2 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette ⟶ cocher S31 F2
- [ ] F3 Publication : `python3 suivi/outil.py publier S31 --ia <n>` (verifier OK, `main` poussée, branche `tache/S31-demonstration` supprimée, verrou rendu) ⟶ cochée par `publier`

## Pour la recette

- Démonstration et latence sur ta machine, avec GPU ; jugement visuel du panneau.
