# S14 — T08 Contrats C-03, C-04, C-06, C-07

> Fiche d'exécution du mode autonome. Chaque case se coche avec `python3 suivi/outil.py cocher S14 <sous-étape> --ia <n>`, juste après la sous-étape : la commande vérifie l'ordre et l'identité de l'IA, signe la case (IA, date, heure UTC), commite et pousse. Une sous-étape non cochée par cette commande est considérée comme non faite. Règles : `docs/construction/sequence.md`. Avancement : `SUIVI.md` et `suivi/tableau.html`.

| Champ | Valeur |
| --- | --- |
| Réalise | IA 1 (conception) |
| Vérifie | IA 3 (vérification), jamais un auteur de l'unité |
| Piste | 3.A Contrats : S13 → S14 (unité 2 sur 2) |
| Commence après | S10, S12, S13 (cochées dans `SUIVI.md`) |
| Indépendante de | aucune |
| Branche | `tache/S14-T08-contrats` |
| Fiche de conception | `docs/construction/etape-3.md`, section T08 |
| Estimation | 2 créneaux |

**Séquentiel ou indépendant.** Cette unité est la 2e de la piste 3.A « Contrats », dont les unités se font à la suite. Les autres pistes de la section (aucune) avancent en même temps, chacune de son côté. Elle attend S13, l'unité précédente de la piste. Elle attend aussi S10, S12, hors de la piste. Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Remplir les sept rubriques de C-03 (façades), C-04 (enveloppe et limites), C-06 (Event Store, lacunes, fin inconnue, chemin observé) et C-07 (API FlowTrace, table d'états du protocole de session, frontière de frame, bail, chemin désactivé).
- Écrire le schéma de l'enveloppe, ses fixtures, les sessions enregistrées, et les quatre tests de contrat avec leurs marqueurs (T09, T11, T12, T13a).

## Fichiers autorisés

- `docs/CONTRACTS.md`, sections C-03, C-04, C-06 et C-07 ;
- `contracts/schemas/envelope.v1.schema.json` ;
- `tests/contract/fixtures/envelope/`, `tests/contract/fixtures/sessions/` ;
- `tests/contract/test_c03_facades.gd`, `test_c04_envelope.gd`, `test_c06_store.gd`, `test_c07_flowtrace.gd` ;
- les marqueurs T09, T11, T12 et T13a de `tests/pending/`.

Toujours autorisés en plus : `rapports/S14*.md` et les cases de cette fiche (par `cocher`).

## Prompt de réalisation

```text
Tu réalises l'unité S14 « T08 Contrats C-03, C-04, C-06, C-07 » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.
Réalisation prévue : IA 1 (conception) ; vérification : IA 3 (vérification). Ton numéro d'IA est celui que te donne le prompt de créneau : tu le passes à --ia, et il signe chaque case que tu coches.

AVANT TOUT, depuis ton clone principal du dépôt
1. Lis REGLES_AGENTS.md s'il existe, puis cette fiche : suivi/S14-T08-contrats.md.
2. python3 suivi/outil.py prendre S14 --ia <n>
   - « PRISE » ou « REPRISE » : tu es sur la branche tache/S14-T08-contrats ; commence à la sous-étape affichée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
   - « REFUSÉ » : l'unité n'est pas pour toi maintenant (déjà prise par une autre IA, S10, S12, S13 non cochées, autre IA prévue) : reviens au prompt de créneau et choisis autre chose.

GODOT
- Si tools/ci/fetch_godot.sh existe : B=$(tools/ci/fetch_godot.sh 4.7.2-stable)
- Sinon, hors du dépôt :
  D=$HOME/.cache/gdm-godot/4.7.2-stable ; mkdir -p "$D"
  test -x "$D/Godot_v4.7.2-stable_linux.x86_64" || { curl -sSL -o /tmp/godot-4.7.2.zip https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip && unzip -o -q /tmp/godot-4.7.2.zip -d "$D"; }
  B=$D/Godot_v4.7.2-stable_linux.x86_64
- « godot » dans les commandes désigne "$B". Contrôle : "$B" --version contient 4.7.2.stable.
- Éditeur avec rendu, quand la fiche le demande : xvfb-run -a -s "-screen 0 1600x900x24" "$B" --editor --path <projet> --rendering-driver opengl3

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S14.md et les cases de suivi/S14-T08-contrats.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status. Tu ne pousses jamais avec --force.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.
- Une décision réservée à l'humain (docs/construction/sequence.md §5) : arrêt obligatoire, rien d'autre.

TRACE OBLIGATOIRE, après CHAQUE sous-étape et avant la suivante
1. git add <les fichiers de la sous-étape> (jamais git add -A).
2. python3 suivi/outil.py cocher S14 <sous-étape> --ia <n>
   La commande vérifie l'ordre des cases et ton identité, coche la case dans suivi/S14-T08-contrats.md, la signe (IA, date, heure UTC), commite et pousse sur tache/S14-T08-contrats.
3. Une sous-étape faite mais non cochée par cette commande est considérée comme non faite : l'IA suivante la refera. Tu ne coches jamais une case à la main.
4. Tu ne modifies jamais SUIVI.md : il ne change qu'à la fusion, sous le verrou de main. Plusieurs IA le lisent en même temps ; aucune ne l'écrit hors de ce verrou.
5. Avant de cocher la dernière sous-étape R : « Statut : TERMINÉ » dans rapports/S14.md, puis git add.
6. Poussée refusée et non rattrapée par la commande : ne force jamais ; git pull --rebase origin tache/S14-T08-contrats, puis relance la commande.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (docs/construction/etape-3.md, T08)
Tu rédiges les contrats C-03, C-04, C-06 et C-07 du projet GODOT_DEV_MAPPER, et les tests qui les jugeront. Tu n'écris aucune implémentation. C-01 est validé : appuie-toi dessus sans le modifier.

SOURCES NORMATIVES
docs/plan-directeur.md §4 (façades), §6 (protocole de session, garanties, champs par type, chemin observé) et §8 (budgets, cycle de vie) ; docs/spikes/SPIKE-01.md, parties 01a et 01b ; docs/spikes/SPIKE-02.md.

DANS docs/CONTRACTS.md, les sept rubriques pour chaque contrat :
- C-03 Façades : pour chaque façade (runtime, débogueur, éditeur), la liste des opérations avec leur signature GDScript, leur comportement en erreur et la capacité qu'elles requièrent. La façade runtime accepte un transport de substitution pour les tests.
- C-04 Enveloppe : format des lots, champs communs et hérités, champs requis par type, limites (1 Ko par charge, 256 événements et 64 Ko par lot), réserve de contrôle de 64 places, identifiants 64 bits en chaîne, rejet d'une version inconnue.
- C-06 Event Store : sessions, lacunes déduites des séquences, rétention et marqueur « tronqué avant seq N », fin de session et « fin inconnue », requête « chemin observé » à trois états.
- C-07 FlowTrace : API statique (init, register, enter, exit, decision, enabled, shutdown) ; table d'états du protocole de session (inerte, prêt, collecte, arrêt demandé, arrêté, bail expiré, capture interrompue) avec toutes les transitions ; commandes appliquées à la frontière de frame ; bail de 2 s renouvelé toutes les 250 ms ; messages du moteur ignorés ; règles du chemin désactivé ; limite au périmètre synchrone.

À PRODUIRE AUSSI
- contracts/schemas/envelope.v1.schema.json et tests/contract/fixtures/envelope/ avec des fichiers valid_* et invalid_<CODE>__<description>. Au minimum : version de protocole inconnue, séquence non croissante dans un lot, décision sans payload.result, function_enter sans inv, lot de 257 événements, charge de plus de 1 Ko, identifiant 64 bits écrit comme nombre. La séquence non croissante et la charge de plus de 1 Ko, mesurée en octets, relèvent du niveau 2.
- tests/contract/fixtures/sessions/ : des sessions enregistrées au format de l'enveloppe. Au minimum : normale ; coupée sans fin ; avec trous ; mêlée de messages du moteur ; avec commande reçue en réentrance.
- Les quatre tests de contrat, chacun avec son marqueur dans tests/pending/ : C-04 → T09, C-06 → T11, C-03 → T12, C-07 → T13a.

RÈGLES
- Chaque transition de la table d'états de C-07 a au moins un test.
- Les constats de SPIKE-01a et 01b sont repris tels quels ; s'ils contredisent le plan, signale l'écart.
- Tout écart avec le plan est listé en tête de ton rapport.

CONTRÔLES
T08-a  python3 tools/check_contracts.py ; echo $?                            → 0 (sept contrats)
T08-b  python3 tools/validate_fixtures.py ; echo $?                          → 0
T08-b2 python3 tools/validate_fixtures.py --plan-examples ; echo $?   → 0 (tous les exemples du plan)
T08-c  (CE) remplace un identifiant chaîne par un nombre dans une fixture valide de l'enveloppe, relance T08-b   → 1 ; annule
T08-d  Tableau croisé dans le rapport : chaque transition de C-07 avec le test qui la couvre   → aucune transition sans test
T08-e  godot --headless --path . -s res://tests/run_all.gd ; echo $?         → 0, pending=6
TRAVAIL TECHNIQUE — fin de la copie exacte du guide

ADAPTATIONS DU MODE AUTONOME
- Aucune : suis le travail technique tel quel.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche ; après chacune, git add puis python3 suivi/outil.py cocher S14 R<k> --ia <n>.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Chaque sous-étape faite est cochée par `cocher`. Complète rapports/S14.md (sorties, « Passation » en cinq lignes au plus), git add, git commit, git push origin HEAD:tache/S14-T08-contrats.
- git status ne montre aucune modification non commitée ; rien ne reste non poussé.

FORMAT DE rapports/S14.md (créé par prendre ; tu le complètes)
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

Après chaque sous-étape : `git add` de ses fichiers, puis `python3 suivi/outil.py cocher S14 R<k> --ia <n>` (coche, signe, commite, pousse).

- [ ] R0 Prise en charge : `python3 suivi/outil.py prendre S14 --ia <n>` (prérequis cochés dans `SUIVI.md` : S10, S12, S13 ; branche `tache/S14-T08-contrats` créée ou reprise ; `rapports/S14.md` au statut EN COURS) ⟶ cochée par `prendre`
- [ ] R1 Lire le plan §4, §6 et §8, `docs/spikes/SPIKE-01.md` (01a et 01b), `docs/spikes/SPIKE-02.md` et C-01 validé. ⟶ cocher S14 R1
- [ ] R2 Rédiger C-03. ⟶ cocher S14 R2
- [ ] R3 Rédiger C-04. ⟶ cocher S14 R3
- [ ] R4 Rédiger C-06. ⟶ cocher S14 R4
- [ ] R5 Rédiger C-07, avec la table d'états complète et le constat de SPIKE-01b sur la file de commandes s'il existe. ⟶ cocher S14 R5
- [ ] R6 Écrire le schéma de l'enveloppe et ses fixtures (au moins les sept invalides de la fiche). ⟶ cocher S14 R6
- [ ] R7 Écrire les sessions enregistrées (au moins les cinq de la fiche). ⟶ cocher S14 R7
- [ ] R8 Écrire les quatre tests de contrat et leurs marqueurs. ⟶ cocher S14 R8
- [ ] R9 Écrire le tableau croisé transition → test de C-07 dans le rapport. ⟶ cocher S14 R9
- [ ] R10 Contrôles finaux : T08-a, T08-b, T08-b2, T08-c, T08-d, T08-e exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » dans le rapport ⟶ cocher S14 R10

## Prompt de vérification

```text
Tu vérifies l'unité S14 « T08 Contrats C-03, C-04, C-06, C-07 » du projet GODOT_DEV_MAPPER. Vérification prévue : IA 3 (vérification). Ton numéro d'IA est celui du prompt de créneau. Tu n'es jamais un auteur de l'unité : la commande de prise le contrôle.

PRISE, depuis ton clone principal
python3 suivi/outil.py prendre S14 --ia <n> --verification
- « VÉRIFICATION PRISE » : copie neuve ../verif-S14-T08-contrats créée sur origin/tache/S14-T08-contrats, verdict EN COURS écrit, V1 cochée. cd ../verif-S14-T08-contrats : toute la vérification se fait dans ce dossier.
- « REFUSÉ » : une autre IA vérifie déjà, tu es auteur, ou l'unité n'est pas terminée : reviens au prompt de créneau.
GODOT : même procédure que le prompt de réalisation.
Tu ne modifies aucun fichier de l'unité. Tu écris seulement ton verdict et tes cases V.

TRACE OBLIGATOIRE : après chaque sous-étape V, git add du fichier de verdict, puis python3 suivi/outil.py cocher S14 <V…> --ia <n>. Pour la dernière : --verdict ACCEPTÉE ou --verdict REFUSÉE, identique à la ligne « Verdict » du fichier. Une sous-étape non cochée par cette commande est considérée comme non faite.

1. TRAÇABILITÉ. Chaque case R cochée est signée « — IA n · date » et a son commit sur la branche (git log --oneline origin/main..HEAD). Case cochée sans travail prouvé dans le rapport : refus.
2. PÉRIMÈTRE. git diff --name-only origin/main...HEAD. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S14*.md et suivi/S14-T08-contrats.md. Tout autre fichier : refus.
3. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : T08-a, T08-b, T08-b2, T08-c, T08-d, T08-e.
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
6. COHÉRENCE. Plan §4, §6 et §8 ; constats de SPIKE-01a et 01b repris tels quels ; C-01 non modifié.

VERDICT dans rapports/S14-verif-<tentative>.md (créé par la prise) :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte

SI ACCEPTÉE — FUSION, depuis ton clone principal
1. python3 suivi/outil.py fusionner S14 --ia <n> --godot "$B"
   Elle prend le verrou de main (et attend s'il est pris), fusionne dans ../fusion-S14-T08-contrats, lance run_all_checks.sh, coche la ligne dans SUIVI.md et la case F1. Si les contrôles échouent : verdict passé à REFUSÉE, main inchangée, verrou rendu ; arrête-toi sur cette unité.
2. cd ../fusion-S14-T08-contrats ; fais les sous-étapes F suivantes de la fiche, et coche chacune : python3 suivi/outil.py cocher S14 F<k> --ia <n> (commit local, sans poussée).
3. python3 suivi/outil.py publier S14 --ia <n> : dernière case cochée, verifier relancé, main poussée, branche supprimée, verrou rendu.
SI REFUSÉE : arrête-toi sur cette unité ; son auteur la reprendra avec prendre.
```

## Sous-étapes de vérification

Dans `../verif-S14-T08-contrats`, après chaque sous-étape : `git add` du verdict, puis `python3 suivi/outil.py cocher S14 V<k> --ia <n>`.

- [ ] V1 Prise en charge : `python3 suivi/outil.py prendre S14 --ia <n> --verification` (pas un auteur ; copie neuve `../verif-S14-T08-contrats` sur `origin/tache/S14-T08-contrats` ; verdict EN COURS) ⟶ cochée par `prendre`
- [ ] V2 Traçabilité : chaque case R cochée porte une signature « — IA n · date » et un commit sur la branche (`git log --oneline origin/main..HEAD`) ⟶ cocher S14 V2
- [ ] V3 Périmètre : `git diff --name-only origin/main...HEAD` ⊂ fichiers autorisés. ⟶ cocher S14 V3
- [ ] V4.1 Contrôle T08-a relancé, résultat conforme. ⟶ cocher S14 V4.1
- [ ] V4.2 Contrôle T08-b relancé, résultat conforme. ⟶ cocher S14 V4.2
- [ ] V4.3 Contrôle T08-b2 relancé, résultat conforme. ⟶ cocher S14 V4.3
- [ ] V4.4 Contrôle T08-c relancé, résultat conforme. ⟶ cocher S14 V4.4
- [ ] V4.5 Contrôle T08-d relancé, résultat conforme. ⟶ cocher S14 V4.5
- [ ] V4.6 Contrôle T08-e relancé, résultat conforme. ⟶ cocher S14 V4.6
- [ ] V5 Contre-épreuves (CE) appliquées et détectées, puis annulées. ⟶ cocher S14 V5
- [ ] V6 Contournements cherchés. ⟶ cocher S14 V6
- [ ] V7 Cohérence avec les contrats et les invariants. ⟶ cocher S14 V7
- [ ] V8 Verdict écrit dans `rapports/S14-verif-<tentative>.md` ⟶ cocher S14 V8 --verdict ACCEPTÉE ou --verdict REFUSÉE

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

F1 et la dernière se cochent par `fusionner` et `publier` ; les autres, dans `../fusion-S14-T08-contrats`, par `python3 suivi/outil.py cocher S14 F<k> --ia <n>` (commit local).

- [ ] F1 Fusion : `python3 suivi/outil.py fusionner S14 --ia <n> --godot "$B"` : verrou de `main`, fusion `--no-ff` dans `../fusion-S14-T08-contrats`, `tools/ci/run_all_checks.sh` sur `main` → ALL_CHECKS OK s'il existe (sinon fusion annulée et verdict passé à REFUSÉE), ligne **S14** cochée dans `SUIVI.md` ⟶ cochée par `fusionner`
- [ ] F2 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette ⟶ cocher S14 F2
- [ ] F3 Publication : `python3 suivi/outil.py publier S14 --ia <n>` (verifier OK, `main` poussée, branche `tache/S14-T08-contrats` supprimée, verrou rendu) ⟶ cochée par `publier`

## Pour la recette

Rien de propre à cette unité.
