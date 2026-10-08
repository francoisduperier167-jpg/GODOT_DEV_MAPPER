# S34 — T19 Mesure de valeur par substitution

> Fiche d'exécution du mode autonome. Chaque case se coche avec `python3 suivi/outil.py cocher S34 <sous-étape> --ia <n>`, juste après la sous-étape : la commande vérifie l'ordre et l'identité de l'IA, signe la case (IA, date, heure UTC), commite et pousse. Une sous-étape non cochée par cette commande est considérée comme non faite. Règles : `docs/construction/sequence.md`. Avancement : `SUIVI.md` et `suivi/tableau.html`.

| Champ | Valeur |
| --- | --- |
| Réalise | IA 2 (développement) |
| Vérifie | IA 3 (vérification), jamais un auteur de l'unité |
| Piste | 7.A Bugs injectés et mesure de valeur : S33 → S34 (unité 2 sur 2) |
| Commence après | S32, S33 (cochées dans `SUIVI.md`) |
| Indépendante de | aucune |
| Branche | `tache/S34-T19-diagnostic` |
| Estimation | 2 créneaux |

**Séquentiel ou indépendant.** Cette unité est la 2e de la piste 7.A « Bugs injectés et mesure de valeur », dont les unités se font à la suite. Les autres pistes de la section (aucune) avancent en même temps, chacune de son côté. Elle attend S33, l'unité précédente de la piste. Elle attend aussi S32, hors de la piste. Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Préparer `fake_editor.gd --record` et `tools/gdm_query.gd`, puis diagnostiquer les trois bugs : 1 avec l'outil, 2 sans, 3 avec, sans avoir lu l'enveloppe.
- Compter pour chaque bug les exécutions, lectures, modifications temporaires et le temps ; proposer la cause ; ouvrir l'enveloppe seulement après ; écrire `docs/mesures/valeur-poc-substitution.md`.
- Appliquer le critère d'arrêt : si l'outil n'a aidé sur aucun des bugs 1 et 3, écrire `rapports/ARRET.md`.

## Fichiers autorisés

`tools/harness/fake_editor.gd` (option `--record`), `tools/gdm_query.gd`, `docs/mesures/valeur-poc-substitution.md`.

Toujours autorisés en plus : `rapports/S34*.md` et les cases de cette fiche (par `cocher`).

## Contrôles propres à cette fiche

- `S34-a` : `grep -c "pas pour une personne" docs/mesures/valeur-poc-substitution.md` → 1
- `T19-a` : Chaque branche de bug reproduit son symptôme seule → trois symptômes reproduits
- `T19-b` : Heure d'ouverture de l'enveloppe notée après le dernier diagnostic → présente
- `T19-c` : Tableau et conclusion complets, durées marquées indicatives → aucune case vide
- `T19-d` : Le vérificateur relit le tableau contre l'enveloppe → concordance des causes
- (CE) Le vérificateur relance `tools/gdm_query.gd` sur une session à trou : le chemin observé est « indéterminé ».

## Prompt de réalisation

```text
Tu réalises l'unité S34 « T19 Mesure de valeur par substitution » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.
Réalisation prévue : IA 2 (développement) ; vérification : IA 3 (vérification). Ton numéro d'IA est celui que te donne le prompt de créneau : tu le passes à --ia, et il signe chaque case que tu coches.

AVANT TOUT, depuis ton clone principal du dépôt
1. Lis REGLES_AGENTS.md s'il existe, puis cette fiche : suivi/S34-T19-diagnostic.md.
2. python3 suivi/outil.py prendre S34 --ia <n>
   - « PRISE » ou « REPRISE » : tu es sur la branche tache/S34-T19-diagnostic ; commence à la sous-étape affichée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
   - « REFUSÉ » : l'unité n'est pas pour toi maintenant (déjà prise par une autre IA, S32, S33 non cochées, autre IA prévue) : reviens au prompt de créneau et choisis autre chose.

GODOT
- Si tools/ci/fetch_godot.sh existe : B=$(tools/ci/fetch_godot.sh 4.7.2-stable)
- Sinon, hors du dépôt :
  D=$HOME/.cache/gdm-godot/4.7.2-stable ; mkdir -p "$D"
  test -x "$D/Godot_v4.7.2-stable_linux.x86_64" || { curl -sSL -o /tmp/godot-4.7.2.zip https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip && unzip -o -q /tmp/godot-4.7.2.zip -d "$D"; }
  B=$D/Godot_v4.7.2-stable_linux.x86_64
- « godot » dans les commandes désigne "$B". Contrôle : "$B" --version contient 4.7.2.stable.
- Éditeur avec rendu, quand la fiche le demande : xvfb-run -a -s "-screen 0 1600x900x24" "$B" --editor --path <projet> --rendering-driver opengl3

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S34.md et les cases de suivi/S34-T19-diagnostic.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status. Tu ne pousses jamais avec --force.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.
- Une décision réservée à l'humain (docs/construction/sequence.md §5) : arrêt obligatoire, rien d'autre.

TRACE OBLIGATOIRE, après CHAQUE sous-étape et avant la suivante
1. git add <les fichiers de la sous-étape> (jamais git add -A).
2. python3 suivi/outil.py cocher S34 <sous-étape> --ia <n>
   La commande vérifie l'ordre des cases et ton identité, coche la case dans suivi/S34-T19-diagnostic.md, la signe (IA, date, heure UTC), commite et pousse sur tache/S34-T19-diagnostic.
3. Une sous-étape faite mais non cochée par cette commande est considérée comme non faite : l'IA suivante la refera. Tu ne coches jamais une case à la main.
4. Tu ne modifies jamais SUIVI.md : il ne change qu'à la fusion, sous le verrou de main. Plusieurs IA le lisent en même temps ; aucune ne l'écrit hors de ce verrou.
5. Avant de cocher la dernière sous-étape R : « Statut : TERMINÉ » dans rapports/S34.md, puis git add.
6. Poussée refusée et non rattrapée par la commande : ne force jamais ; git pull --rebase origin tache/S34-T19-diagnostic, puis relance la commande.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (rédigé pour le mode autonome)
Tu mesures, par substitution, l'utilité du POC du projet GODOT_DEV_MAPPER. Tu n'as pas lu ENVELOPPE_SCELLEE.md et tu ne récupères pas la branche banc/<nom>-enveloppe avant la fin des trois diagnostics.

PRÉPARE (fichiers autorisés : tools/harness/fake_editor.gd, tools/gdm_query.gd, docs/mesures/valeur-poc-substitution.md)
- --record enregistre la session reçue, lot par lot, dans un fichier JSONL.
- tools/gdm_query.gd relit ce fichier avec store/ et projections/, et affiche le journal d'une instance et le chemin observé de ses invocations.

MESURE, sur les branches banc/<nom>-bug-1 à -bug-3, dans cet ordre, avec les symptômes de rapports/S33.md :
- bug 1 avec l'outil : code du jeu, console du jeu, session enregistrée, sorties de gdm_query, captures du panneau sous écran virtuel si utile ;
- bug 2 sans l'outil : code du jeu et console du jeu seulement ; tu peux ajouter des print ;
- bug 3 avec l'outil.
Pour chaque bug, note : le nombre d'exécutions du jeu, de lectures de fichier et de modifications temporaires ; le temps écoulé ; la cause proposée, avec le fichier et la ligne ; ta confiance.
Ensuite seulement, récupère l'enveloppe, note l'heure, et note pour chaque bug si la cause est exacte.

RAPPORT dans docs/mesures/valeur-poc-substitution.md : le tableau de T19 adapté (colonnes : bug, branche, avec l'outil, préparation, exécutions, lectures, modifications, temps, cause proposée, confiance, cause exacte), puis une conclusion qualitative. Écris en tête : « Signal mesuré pour un agent, pas pour une personne ; la mesure humaine se fait à la recette. »

CRITÈRE D'ARRÊT : l'outil a aidé sur un bug s'il a permis de trouver la cause exacte avec moins d'exécutions qu'au bug 2, ou là où le bug 2 n'a pas été trouvé. S'il n'a aidé ni sur le bug 1 ni sur le bug 3, écris rapports/ARRET.md (raison, preuves, ce qu'il faut de l'humain), pousse-le sur main et arrête-toi.
TRAVAIL TECHNIQUE — fin de la copie exacte du guide

CONTRÔLES DE LA FICHE
S34-a  grep -c "pas pour une personne" docs/mesures/valeur-poc-substitution.md   → 1
T19-a  Chaque branche de bug reproduit son symptôme seule   → trois symptômes reproduits
T19-b  Heure d'ouverture de l'enveloppe notée après le dernier diagnostic   → présente
T19-c  Tableau et conclusion complets, durées marquées indicatives   → aucune case vide
T19-d  Le vérificateur relit le tableau contre l'enveloppe   → concordance des causes
(CE) Le vérificateur relance `tools/gdm_query.gd` sur une session à trou : le chemin observé est « indéterminé ».

ADAPTATIONS DU MODE AUTONOME
- Aucune : suis le travail technique tel quel.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche ; après chacune, git add puis python3 suivi/outil.py cocher S34 R<k> --ia <n>.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Chaque sous-étape faite est cochée par `cocher`. Complète rapports/S34.md (sorties, « Passation » en cinq lignes au plus), git add, git commit, git push origin HEAD:tache/S34-T19-diagnostic.
- git status ne montre aucune modification non commitée ; rien ne reste non poussé.

FORMAT DE rapports/S34.md (créé par prendre ; tu le complètes)
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

Après chaque sous-étape : `git add` de ses fichiers, puis `python3 suivi/outil.py cocher S34 R<k> --ia <n>` (coche, signe, commite, pousse).

- [ ] R0 Prise en charge : `python3 suivi/outil.py prendre S34 --ia <n>` (prérequis cochés dans `SUIVI.md` : S32, S33 ; branche `tache/S34-T19-diagnostic` créée ou reprise ; `rapports/S34.md` au statut EN COURS) ⟶ cochée par `prendre`
- [ ] R1 Ajouter l'option `--record` à `tools/harness/fake_editor.gd` (session en JSONL). ⟶ cocher S34 R1
- [ ] R2 Écrire `tools/gdm_query.gd` : relit la session avec `store/` et `projections/`, affiche le journal d'une instance et le chemin observé de ses invocations. ⟶ cocher S34 R2
- [ ] R3 Bug 1, avec l'outil : diagnostic et comptes. ⟶ cocher S34 R3
- [ ] R4 Bug 2, sans l'outil : diagnostic et comptes. ⟶ cocher S34 R4
- [ ] R5 Bug 3, avec l'outil : diagnostic et comptes. ⟶ cocher S34 R5
- [ ] R6 Ouvrir l'enveloppe (`git fetch origin banc/<nom>-enveloppe`) ; noter l'heure ; comparer les causes. ⟶ cocher S34 R6
- [ ] R7 Écrire `docs/mesures/valeur-poc-substitution.md` (signal pour un agent, pas pour une personne, écrit en tête). ⟶ cocher S34 R7
- [ ] R8 Appliquer le critère d'arrêt. ⟶ cocher S34 R8
- [ ] R9 Contrôles finaux : S34-a, T19-a, T19-b, T19-c, T19-d exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » dans le rapport ⟶ cocher S34 R9

## Prompt de vérification

```text
Tu vérifies l'unité S34 « T19 Mesure de valeur par substitution » du projet GODOT_DEV_MAPPER. Vérification prévue : IA 3 (vérification). Ton numéro d'IA est celui du prompt de créneau. Tu n'es jamais un auteur de l'unité : la commande de prise le contrôle.

PRISE, depuis ton clone principal
python3 suivi/outil.py prendre S34 --ia <n> --verification
- « VÉRIFICATION PRISE » : copie neuve ../verif-S34-T19-diagnostic créée sur origin/tache/S34-T19-diagnostic, verdict EN COURS écrit, V1 cochée. cd ../verif-S34-T19-diagnostic : toute la vérification se fait dans ce dossier.
- « REFUSÉ » : une autre IA vérifie déjà, tu es auteur, ou l'unité n'est pas terminée : reviens au prompt de créneau.
GODOT : même procédure que le prompt de réalisation.
Tu ne modifies aucun fichier de l'unité. Tu écris seulement ton verdict et tes cases V.

TRACE OBLIGATOIRE : après chaque sous-étape V, git add du fichier de verdict, puis python3 suivi/outil.py cocher S34 <V…> --ia <n>. Pour la dernière : --verdict ACCEPTÉE ou --verdict REFUSÉE, identique à la ligne « Verdict » du fichier. Une sous-étape non cochée par cette commande est considérée comme non faite.

1. TRAÇABILITÉ. Chaque case R cochée est signée « — IA n · date » et a son commit sur la branche (git log --oneline origin/main..HEAD). Case cochée sans travail prouvé dans le rapport : refus.
2. PÉRIMÈTRE. git diff --name-only origin/main...HEAD. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S34*.md et suivi/S34-T19-diagnostic.md. Tout autre fichier : refus.
3. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : S34-a, T19-a, T19-b, T19-c, T19-d.
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
6. COHÉRENCE. Fiche T19 ; plan §9 (mesure exploratoire, critère d'arrêt).

VERDICT dans rapports/S34-verif-<tentative>.md (créé par la prise) :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte

SI ACCEPTÉE — FUSION, depuis ton clone principal
1. python3 suivi/outil.py fusionner S34 --ia <n> --godot "$B"
   Elle prend le verrou de main (et attend s'il est pris), fusionne dans ../fusion-S34-T19-diagnostic, lance run_all_checks.sh, coche la ligne dans SUIVI.md et la case F1. Si les contrôles échouent : verdict passé à REFUSÉE, main inchangée, verrou rendu ; arrête-toi sur cette unité.
2. cd ../fusion-S34-T19-diagnostic ; fais les sous-étapes F suivantes de la fiche, et coche chacune : python3 suivi/outil.py cocher S34 F<k> --ia <n> (commit local, sans poussée).
3. python3 suivi/outil.py publier S34 --ia <n> : dernière case cochée, verifier relancé, main poussée, branche supprimée, verrou rendu.
SI REFUSÉE : arrête-toi sur cette unité ; son auteur la reprendra avec prendre.
```

## Sous-étapes de vérification

Dans `../verif-S34-T19-diagnostic`, après chaque sous-étape : `git add` du verdict, puis `python3 suivi/outil.py cocher S34 V<k> --ia <n>`.

- [ ] V1 Prise en charge : `python3 suivi/outil.py prendre S34 --ia <n> --verification` (pas un auteur ; copie neuve `../verif-S34-T19-diagnostic` sur `origin/tache/S34-T19-diagnostic` ; verdict EN COURS) ⟶ cochée par `prendre`
- [ ] V2 Traçabilité : chaque case R cochée porte une signature « — IA n · date » et un commit sur la branche (`git log --oneline origin/main..HEAD`) ⟶ cocher S34 V2
- [ ] V3 Périmètre : `git diff --name-only origin/main...HEAD` ⊂ fichiers autorisés. ⟶ cocher S34 V3
- [ ] V4.1 Contrôle S34-a relancé, résultat conforme. ⟶ cocher S34 V4.1
- [ ] V4.2 Contrôle T19-a relancé, résultat conforme. ⟶ cocher S34 V4.2
- [ ] V4.3 Contrôle T19-b relancé, résultat conforme. ⟶ cocher S34 V4.3
- [ ] V4.4 Contrôle T19-c relancé, résultat conforme. ⟶ cocher S34 V4.4
- [ ] V4.5 Contrôle T19-d relancé, résultat conforme. ⟶ cocher S34 V4.5
- [ ] V5 Contre-épreuves (CE) appliquées et détectées, puis annulées. ⟶ cocher S34 V5
- [ ] V6 Contournements cherchés. ⟶ cocher S34 V6
- [ ] V7 Cohérence avec les contrats et les invariants. ⟶ cocher S34 V7
- [ ] V8 Verdict écrit dans `rapports/S34-verif-<tentative>.md` ⟶ cocher S34 V8 --verdict ACCEPTÉE ou --verdict REFUSÉE

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

F1 et la dernière se cochent par `fusionner` et `publier` ; les autres, dans `../fusion-S34-T19-diagnostic`, par `python3 suivi/outil.py cocher S34 F<k> --ia <n>` (commit local).

- [ ] F1 Fusion : `python3 suivi/outil.py fusionner S34 --ia <n> --godot "$B"` : verrou de `main`, fusion `--no-ff` dans `../fusion-S34-T19-diagnostic`, `tools/ci/run_all_checks.sh` sur `main` → ALL_CHECKS OK s'il existe (sinon fusion annulée et verdict passé à REFUSÉE), ligne **S34** cochée dans `SUIVI.md` ⟶ cochée par `fusionner`
- [ ] F2 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette ⟶ cocher S34 F2
- [ ] F3 Publication : `python3 suivi/outil.py publier S34 --ia <n>` (verifier OK, `main` poussée, branche `tache/S34-T19-diagnostic` supprimée, verrou rendu) ⟶ cochée par `publier`

## Pour la recette

- Mesure de valeur humaine (T19 du guide), sur trois nouveaux bugs.
