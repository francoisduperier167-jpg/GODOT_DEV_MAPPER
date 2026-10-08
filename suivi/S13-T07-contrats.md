# S13 — T07 Contrats C-01, C-02, C-05

> Fiche d'exécution du mode autonome. Chaque case se coche avec `python3 suivi/outil.py cocher S13 <sous-étape> --ia <n>`, juste après la sous-étape : la commande vérifie l'ordre et l'identité de l'IA, signe la case (IA, date, heure UTC), commite et pousse. Une sous-étape non cochée par cette commande est considérée comme non faite. Règles : `docs/construction/sequence.md`. Avancement : `SUIVI.md` et `suivi/tableau.html`.

| Champ | Valeur |
| --- | --- |
| Réalise | IA 1 (conception) |
| Vérifie | IA 3 (vérification), jamais un auteur de l'unité |
| Piste | 3.A Contrats : S13 → S14 (unité 1 sur 2) |
| Commence après | S09, S11 (cochées dans `SUIVI.md`) |
| Indépendante de | S10, S12 |
| Branche | `tache/S13-T07-contrats` |
| Fiche de conception | `docs/construction/etape-3.md`, section T07 |
| Estimation | 2 créneaux |

**Séquentiel ou indépendant.** Cette unité est la 1re de la piste 3.A « Contrats », dont les unités se font à la suite. Les autres pistes de la section (aucune) avancent en même temps, chacune de son côté. Elle attend S09, S11, hors de la piste. S14 l'attendra. Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Remplir dans `docs/CONTRACTS.md` les sept rubriques de C-01 (identités, cycle de vie, clés de sonde), C-02 (ancrage, révision, lien périmé) et C-05 (modèle minimal, `.flow.json` v1), avec leurs codes d'erreur.
- Écrire le schéma `contracts/schemas/declared_graph.v1.schema.json`, les fixtures valides et invalides, `tools/validate_fixtures.py`, `tools/check_contracts.py`, les deux tests de contrat avec leurs marqueurs T10, et les contrôles `checks.d/30-contracts.sh` et `31-fixtures.sh`.

## Fichiers autorisés

- `docs/CONTRACTS.md`, sections C-01, C-02 et C-05 ;
- `contracts/schemas/declared_graph.v1.schema.json` ;
- `tests/contract/fixtures/declared_graph/` ;
- `tests/contract/test_c01_identities.gd`, `tests/contract/test_c05_declared_graph.gd` ;
- les marqueurs T10 de `tests/pending/`, `tools/validate_fixtures.py`, `tools/check_contracts.py` ;
- `tools/ci/checks.d/30-contracts.sh`, `tools/ci/checks.d/31-fixtures.sh`.

Toujours autorisés en plus : `rapports/S13*.md` et les cases de cette fiche (par `cocher`).

## Prompt de réalisation

```text
Tu réalises l'unité S13 « T07 Contrats C-01, C-02, C-05 » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.
Réalisation prévue : IA 1 (conception) ; vérification : IA 3 (vérification). Ton numéro d'IA est celui que te donne le prompt de créneau : tu le passes à --ia, et il signe chaque case que tu coches.

AVANT TOUT, depuis ton clone principal du dépôt
1. Lis REGLES_AGENTS.md s'il existe, puis cette fiche : suivi/S13-T07-contrats.md.
2. python3 suivi/outil.py prendre S13 --ia <n>
   - « PRISE » ou « REPRISE » : tu es sur la branche tache/S13-T07-contrats ; commence à la sous-étape affichée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
   - « REFUSÉ » : l'unité n'est pas pour toi maintenant (déjà prise par une autre IA, S09, S11 non cochées, autre IA prévue) : reviens au prompt de créneau et choisis autre chose.

GODOT
- Si tools/ci/fetch_godot.sh existe : B=$(tools/ci/fetch_godot.sh 4.7.2-stable)
- Sinon, hors du dépôt :
  D=$HOME/.cache/gdm-godot/4.7.2-stable ; mkdir -p "$D"
  test -x "$D/Godot_v4.7.2-stable_linux.x86_64" || { curl -sSL -o /tmp/godot-4.7.2.zip https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip && unzip -o -q /tmp/godot-4.7.2.zip -d "$D"; }
  B=$D/Godot_v4.7.2-stable_linux.x86_64
- « godot » dans les commandes désigne "$B". Contrôle : "$B" --version contient 4.7.2.stable.
- Éditeur avec rendu, quand la fiche le demande : xvfb-run -a -s "-screen 0 1600x900x24" "$B" --editor --path <projet> --rendering-driver opengl3

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S13.md et les cases de suivi/S13-T07-contrats.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status. Tu ne pousses jamais avec --force.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.
- Une décision réservée à l'humain (docs/construction/sequence.md §5) : arrêt obligatoire, rien d'autre : python3 suivi/outil.py arreter --ia <n> --unite S13 --raison "<raison>", puis fin du créneau.

TRACE OBLIGATOIRE, après CHAQUE sous-étape et avant la suivante
1. git add <les fichiers de la sous-étape> (jamais git add -A).
2. python3 suivi/outil.py cocher S13 <sous-étape> --ia <n>
   La commande vérifie l'ordre des cases et ton identité, coche la case dans suivi/S13-T07-contrats.md, la signe (IA, date, heure UTC), commite et pousse sur tache/S13-T07-contrats.
3. Une sous-étape faite mais non cochée par cette commande est considérée comme non faite : l'IA suivante la refera. Tu ne coches jamais une case à la main.
4. Tu ne modifies jamais SUIVI.md : il ne change qu'à la fusion, sous le verrou de main. Plusieurs IA le lisent en même temps ; aucune ne l'écrit hors de ce verrou.
5. Avant de cocher la dernière sous-étape R : « Statut : TERMINÉ » dans rapports/S13.md, puis git add.
6. Poussée refusée et non rattrapée par la commande : ne force jamais ; git pull --rebase origin tache/S13-T07-contrats, puis relance la commande.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (docs/construction/etape-3.md, T07)
Tu rédiges les contrats C-01, C-02 et C-05 du projet GODOT_DEV_MAPPER, et les tests qui les jugeront. Tu n'écris aucune implémentation.

SOURCES NORMATIVES
docs/plan-directeur.md §5 (modèle, identités, clés de sonde, cycle de vie des instances, exemples) et §10 ; docs/spikes/SPIKE-02.md (clé de correspondance, UID) ; docs/DECISIONS.md.

DANS docs/CONTRACTS.md
Pour chaque contrat, remplis les sept rubriques : objet ; format ou API ; exemples valides ; exemples invalides ; comportement en erreur ; version ; tests de contrat.
- C-01 : identités de définition, instance, invocation, occurrence et session ; règles de cycle de vie des instances (enregistrement, arbre, destruction connue ou constatée) ; clés de sonde.
- C-02 : ancrage source et révision du programme ; règle de lien périmé (range_hash).
- C-05 : modèle minimal et format .flow.json v1 ; références non résolues.
Pour C-01 et C-05, les API GDScript attendues s'écrivent sous forme de signatures, avec le comportement en erreur. Chaque contrat liste ses codes d'erreur, communs au validateur Python et à l'implémentation GDScript.

À PRODUIRE AUSSI
- contracts/schemas/declared_graph.v1.schema.json (JSON Schema 2020-12) : il accepte l'exemple du plan §5 et rejette chaque exemple invalide.
- tests/contract/fixtures/declared_graph/ : des fichiers valid_*.json et des fichiers invalid_<CODE>__<description>.json, un code d'erreur par fichier. Au minimum : evidence absent, ancrage sans revision, relation vers une définition inexistante sans objet unresolved, clé de sonde dupliquée, schema_version inconnue.
- tools/validate_fixtures.py : valide chaque fixture en deux niveaux. Niveau 1 : le schéma JSON. Niveau 2 : les règles sémantiques (références résolues, unicité des clés de sonde entre définitions, ordre des séquences, taille sérialisée en octets UTF-8), chacune avec son code d'erreur. Une fixture invalid_<CODE>__… doit être rejetée avec ce code, et lui seul ; sinon, code 1. Avec --plan-examples, il extrait les blocs JSON du plan et les valide ; --kinds declared_graph limite cette validation à un format. Avec --file <chemin>, il valide un seul fichier, contre le schéma choisi par son champ kind.
- tools/check_contracts.py : vérifie que chaque section C-0x de docs/CONTRACTS.md a les sept rubriques. Arguments facultatifs : les ID à vérifier. Code 1 si une rubrique manque.
- tests/contract/test_c01_identities.gd et tests/contract/test_c05_declared_graph.gd : tests GDScript qui chargent les fixtures et appellent l'API décrite au contrat, qui n'existe pas encore. Crée pour chacun un marqueur tests/pending/<nom du test>.pending qui contient « T10 ».
- tools/ci/checks.d/30-contracts.sh et 31-fixtures.sh : ils exécutent check_contracts et validate_fixtures, et affichent leur ligne CHECK.

RÈGLES
Chaque règle du contrat a au moins un exemple invalide et un test qui le rejette. Tout écart avec le plan est listé en tête de ton rapport, sans être tranché.

CONTRÔLES
T07-a  python3 tools/check_contracts.py C-01 C-02 C-05 ; echo $?            → 0
T07-b  python3 tools/validate_fixtures.py ; echo $?                          → 0
T07-c  python3 tools/validate_fixtures.py --plan-examples --kinds declared_graph ; echo $?   → 0 (l'enveloppe attend T08)
T07-d  (CE) retire « evidence » d'une fixture valide, relance T07-b          → 1 ; annule
T07-d2 (CE) duplique une clé de sonde dans une fixture valide, relance T07-b → 1, avec le code de doublon ; annule
T07-e  (CE) supprime la rubrique « Comportement en erreur » de C-05, relance T07-a   → 1 ; annule
T07-f  godot --headless --path . -s res://tests/run_all.gd ; echo $?         → 0, pending=2
T07-g  godot --headless --path . --check-only -s res://tests/contract/test_c05_declared_graph.gd   → 0 seulement si l'API appelée est déclarée ; sinon, explique dans le rapport comment le test sera activé en T10
TRAVAIL TECHNIQUE — fin de la copie exacte du guide

ADAPTATIONS DU MODE AUTONOME
- Aucune : suis le travail technique tel quel.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche ; après chacune, git add puis python3 suivi/outil.py cocher S13 R<k> --ia <n>.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Chaque sous-étape faite est cochée par `cocher`. Complète rapports/S13.md (sorties, « Passation » en cinq lignes au plus), git add, git commit, git push origin HEAD:tache/S13-T07-contrats.
- git status ne montre aucune modification non commitée ; rien ne reste non poussé.

FORMAT DE rapports/S13.md (créé par prendre ; tu le complètes)
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

Après chaque sous-étape : `git add` de ses fichiers, puis `python3 suivi/outil.py cocher S13 R<k> --ia <n>` (coche, signe, commite, pousse).

- [ ] R0 Prise en charge : `python3 suivi/outil.py prendre S13 --ia <n>` (prérequis cochés dans `SUIVI.md` : S09, S11 ; branche `tache/S13-T07-contrats` créée ou reprise ; `rapports/S13.md` au statut EN COURS) ⟶ cochée par `prendre`
- [ ] R1 Lire le plan §5 et §10, `docs/spikes/SPIKE-02.md`, `docs/DECISIONS.md`. ⟶ cocher S13 R1
- [ ] R2 Rédiger C-01 dans `docs/CONTRACTS.md` (sept rubriques, codes d'erreur). ⟶ cocher S13 R2
- [ ] R3 Rédiger C-02. ⟶ cocher S13 R3
- [ ] R4 Rédiger C-05. ⟶ cocher S13 R4
- [ ] R5 Écrire le schéma JSON du graphe déclaré. ⟶ cocher S13 R5
- [ ] R6 Écrire les fixtures `valid_*` et `invalid_<CODE>__*` (au moins les cinq invalides de la fiche). ⟶ cocher S13 R6
- [ ] R7 Écrire `tools/validate_fixtures.py` (deux niveaux, `--plan-examples`, `--kinds`, `--file`). ⟶ cocher S13 R7
- [ ] R8 Écrire `tools/check_contracts.py`. ⟶ cocher S13 R8
- [ ] R9 Écrire les deux tests de contrat et leurs marqueurs `tests/pending/` (« T10 »). ⟶ cocher S13 R9
- [ ] R10 Écrire `tools/ci/checks.d/30-contracts.sh` et `31-fixtures.sh`. ⟶ cocher S13 R10
- [ ] R11 Lister en tête du rapport tout écart avec le plan, sans le trancher. ⟶ cocher S13 R11
- [ ] R12 Contrôles finaux : T07-a, T07-b, T07-c, T07-d, T07-d2, T07-e, T07-f, T07-g exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » dans le rapport ⟶ cocher S13 R12

## Prompt de vérification

```text
Tu vérifies l'unité S13 « T07 Contrats C-01, C-02, C-05 » du projet GODOT_DEV_MAPPER. Vérification prévue : IA 3 (vérification). Ton numéro d'IA est celui du prompt de créneau. Tu n'es jamais un auteur de l'unité : la commande de prise le contrôle.

PRISE, depuis ton clone principal
python3 suivi/outil.py prendre S13 --ia <n> --verification
- « VÉRIFICATION PRISE » : copie neuve ../verif-S13-T07-contrats créée sur origin/tache/S13-T07-contrats, verdict EN COURS écrit, V1 cochée. cd ../verif-S13-T07-contrats : toute la vérification se fait dans ce dossier.
- « REFUSÉ » : une autre IA vérifie déjà, tu es auteur, ou l'unité n'est pas terminée : reviens au prompt de créneau.
- Créneau fini avant le verdict : au créneau suivant, etat te propose la même commande ; elle recrée la copie (« VÉRIFICATION REPRISE ») et tu reprends à la première case V ouverte.
GODOT : même procédure que le prompt de réalisation.
Tu ne modifies aucun fichier de l'unité. Tu écris seulement ton verdict et tes cases V.

TRACE OBLIGATOIRE : après chaque sous-étape V, git add du fichier de verdict, puis python3 suivi/outil.py cocher S13 <V…> --ia <n>. Pour la dernière : --verdict ACCEPTÉE ou --verdict REFUSÉE, identique à la ligne « Verdict » du fichier. Une sous-étape non cochée par cette commande est considérée comme non faite.

1. TRAÇABILITÉ. Chaque case R cochée est signée « — IA n · date » et a son commit sur la branche (git log --oneline origin/main..HEAD). Case cochée sans travail prouvé dans le rapport : refus.
2. PÉRIMÈTRE. git diff --name-only origin/main...HEAD. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S13*.md et suivi/S13-T07-contrats.md. Tout autre fichier : refus.
3. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : T07-a, T07-b, T07-c, T07-d, T07-d2, T07-e, T07-f, T07-g.
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
6. COHÉRENCE. Plan §5 et §10 ; SPIKE-02 ; règle « un exemple invalide et un test par règle du contrat ».

VERDICT dans rapports/S13-verif-<tentative>.md (créé par la prise) :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte

SI ACCEPTÉE — FUSION, depuis ton clone principal (cd hors de ../verif-S13-T07-contrats)
1. python3 suivi/outil.py fusionner S13 --ia <n>
   Elle trouve Godot (--godot, $GODOT, cache du bloc GODOT ou tools/ci/fetch_godot.sh ; sans Godot : REFUSÉ, verdict inchangé), prend le verrou de main (et attend s'il est pris), revérifie l'unité, fusionne dans ../fusion-S13-T07-contrats, lance run_all_checks.sh, coche la ligne dans SUIVI.md et la case F1. Si les contrôles échouent : verdict passé à REFUSÉE, main inchangée, verrou rendu ; arrête-toi sur cette unité. La fusion te revient parce que tu as signé le verdict ; une autre IA ne la fait qu'après 12 h.
2. cd ../fusion-S13-T07-contrats ; fais les sous-étapes F suivantes de la fiche, et coche chacune : python3 suivi/outil.py cocher S13 F<k> --ia <n> (commit local, sans poussée).
3. python3 suivi/outil.py publier S13 --ia <n> : dernière case cochée, verifier relancé, main poussée, branche supprimée, verrou rendu.
SI REFUSÉE : arrête-toi sur cette unité ; son auteur la reprendra avec prendre.
```

## Sous-étapes de vérification

Dans `../verif-S13-T07-contrats`, après chaque sous-étape : `git add` du verdict, puis `python3 suivi/outil.py cocher S13 V<k> --ia <n>`.

- [ ] V1 Prise en charge : `python3 suivi/outil.py prendre S13 --ia <n> --verification` (pas un auteur ; copie neuve `../verif-S13-T07-contrats` sur `origin/tache/S13-T07-contrats` ; verdict EN COURS) ⟶ cochée par `prendre`
- [ ] V2 Traçabilité : chaque case R cochée porte une signature « — IA n · date » et un commit sur la branche (`git log --oneline origin/main..HEAD`) ⟶ cocher S13 V2
- [ ] V3 Périmètre : `git diff --name-only origin/main...HEAD` ⊂ fichiers autorisés. ⟶ cocher S13 V3
- [ ] V4.1 Contrôle T07-a relancé, résultat conforme. ⟶ cocher S13 V4.1
- [ ] V4.2 Contrôle T07-b relancé, résultat conforme. ⟶ cocher S13 V4.2
- [ ] V4.3 Contrôle T07-c relancé, résultat conforme. ⟶ cocher S13 V4.3
- [ ] V4.4 Contrôle T07-d relancé, résultat conforme. ⟶ cocher S13 V4.4
- [ ] V4.5 Contrôle T07-d2 relancé, résultat conforme. ⟶ cocher S13 V4.5
- [ ] V4.6 Contrôle T07-e relancé, résultat conforme. ⟶ cocher S13 V4.6
- [ ] V4.7 Contrôle T07-f relancé, résultat conforme. ⟶ cocher S13 V4.7
- [ ] V4.8 Contrôle T07-g relancé, résultat conforme. ⟶ cocher S13 V4.8
- [ ] V5 Contre-épreuves (CE) appliquées et détectées, puis annulées. ⟶ cocher S13 V5
- [ ] V6 Contournements cherchés. ⟶ cocher S13 V6
- [ ] V7 Cohérence avec les contrats et les invariants. ⟶ cocher S13 V7
- [ ] V8 Verdict écrit dans `rapports/S13-verif-<tentative>.md` ⟶ cocher S13 V8 --verdict ACCEPTÉE ou --verdict REFUSÉE

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

F1 et la dernière se cochent par `fusionner` et `publier` ; les autres, dans `../fusion-S13-T07-contrats`, par `python3 suivi/outil.py cocher S13 F<k> --ia <n>` (commit local).

- [ ] F1 Fusion, depuis le clone principal : `python3 suivi/outil.py fusionner S13 --ia <n>` : Godot trouvé seul (--godot, $GODOT, cache du bloc GODOT ou fetch_godot.sh), verrou de `main`, fusion `--no-ff` dans `../fusion-S13-T07-contrats`, `tools/ci/run_all_checks.sh` sur `main` → ALL_CHECKS OK s'il existe (sinon fusion annulée et verdict passé à REFUSÉE), ligne **S13** cochée dans `SUIVI.md` ⟶ cochée par `fusionner`
- [ ] F2 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette ⟶ cocher S13 F2
- [ ] F3 Publication : `python3 suivi/outil.py publier S13 --ia <n>` (verifier OK, `main` poussée, branche `tache/S13-T07-contrats` supprimée, verrou rendu) ⟶ cochée par `publier`

## Pour la recette

Rien de propre à cette unité.
