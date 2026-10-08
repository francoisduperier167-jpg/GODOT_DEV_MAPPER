# S21 — T13b Banc sans éditeur et scénarios de coupure

> Fiche d'exécution du mode autonome. Chaque case se coche avec `python3 suivi/outil.py cocher S21 <sous-étape> --ia <n>`, juste après la sous-étape : la commande vérifie l'ordre et l'identité de l'IA, signe la case (IA, date, heure UTC), commite et pousse. Une sous-étape non cochée par cette commande est considérée comme non faite. Règles : `docs/construction/sequence.md`. Avancement : `SUIVI.md` et `suivi/tableau.html`.

| Champ | Valeur |
| --- | --- |
| Réalise | IA 2 (développement) |
| Vérifie | IA 1 (conception), jamais un auteur de l'unité |
| Piste | 4.B Façades, FlowTrace et mesures : S19 → S20 → S21 → S22 (unité 3 sur 4) |
| Commence après | S20 (cochée dans `SUIVI.md`) |
| Indépendante de | S17, S18, S24, S28 |
| Branche | `tache/S21-T13b-banc` |
| Fiche de conception | `docs/construction/etape-4.md`, section T13b |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Cette unité est la 3e de la piste 4.B « Façades, FlowTrace et mesures », dont les unités se font à la suite. Les autres pistes de la section (4.A) avancent en même temps, chacune de son côté. Elle attend S20, l'unité précédente de la piste. S22 l'attendra. Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- `tools/harness/fake_editor.gd` réécrit depuis le récepteur de SPIKE-01a (port configurable, scénarios).
- `tools/harness/demo_game/` : deux instances dont une enregistrée avant le démarrage, une décision.
- `tests/integration/run_session.sh` et `tools/ci/checks.d/40-integration.sh`.

## Fichiers autorisés

`tools/harness/fake_editor.gd`, `tools/harness/demo_game/`, `tests/integration/run_session.sh`, `tools/ci/checks.d/40-integration.sh`.

Toujours autorisés en plus : `rapports/S21*.md` et les cases de cette fiche (par `cocher`).

## Prompt de réalisation

```text
Tu réalises l'unité S21 « T13b Banc sans éditeur et scénarios de coupure » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.
Réalisation prévue : IA 2 (développement) ; vérification : IA 1 (conception). Ton numéro d'IA est celui que te donne le prompt de créneau : tu le passes à --ia, et il signe chaque case que tu coches.

AVANT TOUT, depuis ton clone principal du dépôt
1. Lis REGLES_AGENTS.md s'il existe, puis cette fiche : suivi/S21-T13b-banc.md.
2. python3 suivi/outil.py prendre S21 --ia <n>
   - « PRISE » ou « REPRISE » : tu es sur la branche tache/S21-T13b-banc ; commence à la sous-étape affichée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
   - « REFUSÉ » : l'unité n'est pas pour toi maintenant (déjà prise par une autre IA, S20 non cochée, autre IA prévue) : reviens au prompt de créneau et choisis autre chose.

GODOT
- Si tools/ci/fetch_godot.sh existe : B=$(tools/ci/fetch_godot.sh 4.7.2-stable)
- Sinon, hors du dépôt :
  D=$HOME/.cache/gdm-godot/4.7.2-stable ; mkdir -p "$D"
  test -x "$D/Godot_v4.7.2-stable_linux.x86_64" || { curl -sSL -o /tmp/godot-4.7.2.zip https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip && unzip -o -q /tmp/godot-4.7.2.zip -d "$D"; }
  B=$D/Godot_v4.7.2-stable_linux.x86_64
- « godot » dans les commandes désigne "$B". Contrôle : "$B" --version contient 4.7.2.stable.
- Éditeur avec rendu, quand la fiche le demande : xvfb-run -a -s "-screen 0 1600x900x24" "$B" --editor --path <projet> --rendering-driver opengl3

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S21.md et les cases de suivi/S21-T13b-banc.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status. Tu ne pousses jamais avec --force.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.
- Une décision réservée à l'humain (docs/construction/sequence.md §5) : arrêt obligatoire, rien d'autre : python3 suivi/outil.py arreter --ia <n> --unite S21 --raison "<raison>", puis fin du créneau.

TRACE OBLIGATOIRE, après CHAQUE sous-étape et avant la suivante
1. git add <les fichiers de la sous-étape> (jamais git add -A).
2. python3 suivi/outil.py cocher S21 <sous-étape> --ia <n>
   La commande vérifie l'ordre des cases et ton identité, coche la case dans suivi/S21-T13b-banc.md, la signe (IA, date, heure UTC), commite et pousse sur tache/S21-T13b-banc.
3. Une sous-étape faite mais non cochée par cette commande est considérée comme non faite : l'IA suivante la refera. Tu ne coches jamais une case à la main.
4. Tu ne modifies jamais SUIVI.md : il ne change qu'à la fusion, sous le verrou de main. Plusieurs IA le lisent en même temps ; aucune ne l'écrit hors de ce verrou.
5. Avant de cocher la dernière sous-étape R : « Statut : TERMINÉ » dans rapports/S21.md, puis git add.
6. Poussée refusée et non rattrapée par la commande : ne force jamais ; git pull --rebase origin tache/S21-T13b-banc, puis relance la commande.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (docs/construction/etape-4.md, T13b)
Tu réalises la tâche T13b du projet GODOT_DEV_MAPPER. Applique les règles et le format de rapport du prompt universel de réalisation.
CONTEXTE : docs/CONTRACTS.md, section C-07 ; docs/spikes/SPIKE-01.md ; spikes/spike01_debugger/receiver/, en exemple seulement.

OBJECTIF
1. tools/harness/fake_editor.gd : un récepteur qui joue l'éditeur sur le canal du débogueur. Réécris-le proprement à partir du récepteur de SPIKE-01a, avec un port configurable et des scénarios paramétrables : démarrage, arrêt, redémarrage, coupure.
2. tools/harness/demo_game/ : un mini-projet qui utilise FlowTrace, avec deux instances, dont une enregistrée avant le démarrage, et une décision.
3. tests/integration/run_session.sh : lance le banc et le mini-jeu, et vérifie :
   - aucun trou ;
   - aucun lot après « stopped » ;
   - état initial reçu au démarrage ;
   - bail déclenché après la coupure ;
   - jeu toujours actif.
   Code 0 si tout est vérifié, 1 sinon.
4. tools/ci/checks.d/40-integration.sh : exécute run_session.sh et affiche « CHECK integration OK » ou « CHECK integration KO ».
Si un scénario révèle un défaut de flow_trace.gd conforme au contrat, décris-le dans le rapport et passe en ESCALADE : la correction revient à la tâche T13a rouverte.

CONTRÔLES
T13b-a  tests/integration/run_session.sh avec GODOT=<4.7.2> ; echo $?   → 0
T13b-b  GODOT=<binaire> tools/ci/run_all_checks.sh ; echo $?   → 0, CHECK integration OK
CONTRE-ÉPREUVE (CE) pour le vérificateur : dans le mini-jeu, envoyer un lot après « stopped » → T13b-a échoue.
TRAVAIL TECHNIQUE — fin de la copie exacte du guide

ADAPTATIONS DU MODE AUTONOME
- Aucune : suis le travail technique tel quel.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche ; après chacune, git add puis python3 suivi/outil.py cocher S21 R<k> --ia <n>.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Chaque sous-étape faite est cochée par `cocher`. Complète rapports/S21.md (sorties, « Passation » en cinq lignes au plus), git add, git commit, git push origin HEAD:tache/S21-T13b-banc.
- git status ne montre aucune modification non commitée ; rien ne reste non poussé.

FORMAT DE rapports/S21.md (créé par prendre ; tu le complètes)
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

Après chaque sous-étape : `git add` de ses fichiers, puis `python3 suivi/outil.py cocher S21 R<k> --ia <n>` (coche, signe, commite, pousse).

- [ ] R0 Prise en charge : `python3 suivi/outil.py prendre S21 --ia <n>` (prérequis cochés dans `SUIVI.md` : S20 ; branche `tache/S21-T13b-banc` créée ou reprise ; `rapports/S21.md` au statut EN COURS) ⟶ cochée par `prendre`
- [ ] R1 Écrire `tools/harness/fake_editor.gd`. ⟶ cocher S21 R1
- [ ] R2 Écrire `tools/harness/demo_game/`. ⟶ cocher S21 R2
- [ ] R3 Écrire `tests/integration/run_session.sh` (cinq vérifications). ⟶ cocher S21 R3
- [ ] R4 Écrire `tools/ci/checks.d/40-integration.sh`. ⟶ cocher S21 R4
- [ ] R5 Si un scénario révèle un défaut de `flow_trace.gd` : ESCALADE avec le diagnostic (la correction revient à S20 rouverte). ⟶ cocher S21 R5
- [ ] R6 Contrôles finaux : T13b-a, T13b-b exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » dans le rapport ⟶ cocher S21 R6

## Prompt de vérification

```text
Tu vérifies l'unité S21 « T13b Banc sans éditeur et scénarios de coupure » du projet GODOT_DEV_MAPPER. Vérification prévue : IA 1 (conception). Ton numéro d'IA est celui du prompt de créneau. Tu n'es jamais un auteur de l'unité : la commande de prise le contrôle.

PRISE, depuis ton clone principal
python3 suivi/outil.py prendre S21 --ia <n> --verification
- « VÉRIFICATION PRISE » : copie neuve ../verif-S21-T13b-banc créée sur origin/tache/S21-T13b-banc, verdict EN COURS écrit, V1 cochée. cd ../verif-S21-T13b-banc : toute la vérification se fait dans ce dossier.
- « REFUSÉ » : une autre IA vérifie déjà, tu es auteur, ou l'unité n'est pas terminée : reviens au prompt de créneau.
- Créneau fini avant le verdict : au créneau suivant, etat te propose la même commande ; elle recrée la copie (« VÉRIFICATION REPRISE ») et tu reprends à la première case V ouverte.
GODOT : même procédure que le prompt de réalisation.
Tu ne modifies aucun fichier de l'unité. Tu écris seulement ton verdict et tes cases V.

TRACE OBLIGATOIRE : après chaque sous-étape V, git add du fichier de verdict, puis python3 suivi/outil.py cocher S21 <V…> --ia <n>. Pour la dernière : --verdict ACCEPTÉE ou --verdict REFUSÉE, identique à la ligne « Verdict » du fichier. Une sous-étape non cochée par cette commande est considérée comme non faite.

1. TRAÇABILITÉ. Chaque case R cochée est signée « — IA n · date » et a son commit sur la branche (git log --oneline origin/main..HEAD). Case cochée sans travail prouvé dans le rapport : refus.
2. PÉRIMÈTRE. git diff --name-only origin/main...HEAD. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S21*.md et suivi/S21-T13b-banc.md. Tout autre fichier : refus.
3. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : T13b-a, T13b-b.
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
6. COHÉRENCE. C-07 ; constats de SPIKE-01a ; aucun lot après « stopped ».

VERDICT dans rapports/S21-verif-<tentative>.md (créé par la prise) :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte

SI ACCEPTÉE — FUSION, depuis ton clone principal (cd hors de ../verif-S21-T13b-banc)
1. python3 suivi/outil.py fusionner S21 --ia <n>
   Elle trouve Godot (--godot, $GODOT, cache du bloc GODOT ou tools/ci/fetch_godot.sh ; sans Godot : REFUSÉ, verdict inchangé), prend le verrou de main (et attend s'il est pris), revérifie l'unité, fusionne dans ../fusion-S21-T13b-banc, lance run_all_checks.sh, coche la ligne dans SUIVI.md et la case F1. Si les contrôles échouent : verdict passé à REFUSÉE, main inchangée, verrou rendu ; arrête-toi sur cette unité. La fusion te revient parce que tu as signé le verdict ; une autre IA ne la fait qu'après 12 h.
2. cd ../fusion-S21-T13b-banc ; fais les sous-étapes F suivantes de la fiche, et coche chacune : python3 suivi/outil.py cocher S21 F<k> --ia <n> (commit local, sans poussée).
3. python3 suivi/outil.py publier S21 --ia <n> : dernière case cochée, verifier relancé, main poussée, branche supprimée, verrou rendu.
SI REFUSÉE : arrête-toi sur cette unité ; son auteur la reprendra avec prendre.
```

## Sous-étapes de vérification

Dans `../verif-S21-T13b-banc`, après chaque sous-étape : `git add` du verdict, puis `python3 suivi/outil.py cocher S21 V<k> --ia <n>`.

- [ ] V1 Prise en charge : `python3 suivi/outil.py prendre S21 --ia <n> --verification` (pas un auteur ; copie neuve `../verif-S21-T13b-banc` sur `origin/tache/S21-T13b-banc` ; verdict EN COURS) ⟶ cochée par `prendre`
- [ ] V2 Traçabilité : chaque case R cochée porte une signature « — IA n · date » et un commit sur la branche (`git log --oneline origin/main..HEAD`) ⟶ cocher S21 V2
- [ ] V3 Périmètre : `git diff --name-only origin/main...HEAD` ⊂ fichiers autorisés. ⟶ cocher S21 V3
- [ ] V4.1 Contrôle T13b-a relancé, résultat conforme. ⟶ cocher S21 V4.1
- [ ] V4.2 Contrôle T13b-b relancé, résultat conforme. ⟶ cocher S21 V4.2
- [ ] V5 Contre-épreuves (CE) appliquées et détectées, puis annulées. ⟶ cocher S21 V5
- [ ] V6 Contournements cherchés. ⟶ cocher S21 V6
- [ ] V7 Cohérence avec les contrats et les invariants. ⟶ cocher S21 V7
- [ ] V8 Verdict écrit dans `rapports/S21-verif-<tentative>.md` ⟶ cocher S21 V8 --verdict ACCEPTÉE ou --verdict REFUSÉE

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

F1 et la dernière se cochent par `fusionner` et `publier` ; les autres, dans `../fusion-S21-T13b-banc`, par `python3 suivi/outil.py cocher S21 F<k> --ia <n>` (commit local).

- [ ] F1 Fusion, depuis le clone principal : `python3 suivi/outil.py fusionner S21 --ia <n>` : Godot trouvé seul (--godot, $GODOT, cache du bloc GODOT ou fetch_godot.sh), verrou de `main`, fusion `--no-ff` dans `../fusion-S21-T13b-banc`, `tools/ci/run_all_checks.sh` sur `main` → ALL_CHECKS OK s'il existe (sinon fusion annulée et verdict passé à REFUSÉE), ligne **S21** cochée dans `SUIVI.md` ⟶ cochée par `fusionner`
- [ ] F2 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette ⟶ cocher S21 F2
- [ ] F3 Publication : `python3 suivi/outil.py publier S21 --ia <n>` (verifier OK, `main` poussée, branche `tache/S21-T13b-banc` supprimée, verrou rendu) ⟶ cochée par `publier`

## Pour la recette

Rien de propre à cette unité.
