# S10 — T05 SPIKE-01b, partie éditeur, sous écran virtuel

> Fiche d'exécution du mode autonome. Chaque case se coche avec `python3 suivi/outil.py cocher S10 <sous-étape> --ia <n>`, juste après la sous-étape : la commande vérifie l'ordre et l'identité de l'IA, signe la case (IA, date, heure UTC), commite et pousse. Une sous-étape non cochée par cette commande est considérée comme non faite. Règles : `docs/construction/sequence.md`. Avancement : `SUIVI.md` et `suivi/tableau.html`.

| Champ | Valeur |
| --- | --- |
| Réalise | IA 1 (conception) |
| Vérifie | IA 3 (vérification), jamais un auteur de l'unité |
| Piste | 2.A SPIKE-01b, éditeur sous écran virtuel : S10 (unité 1 sur 1) |
| Commence après | S02 (cochée dans `SUIVI.md`) |
| Indépendante de | S03, S04, S05, S06, S07, S08, S09, S11, S13 |
| Branche | `tache/S10-T05-spike01b` |
| Fiche de conception | `docs/construction/etape-2.md`, section T05 |
| Estimation | 2 créneaux |

**Séquentiel ou indépendant.** Cette unité est la 1re de la piste 2.A « SPIKE-01b, éditeur sous écran virtuel », dont les unités se font à la suite. Les autres pistes de la section (2.B) avancent en même temps, chacune de son côté. Elle attend S02, hors de la piste. Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Construire dans `spikes/spike01_debugger/editor/` un projet d'éditeur jetable dont le plugin déroule seul le scénario, sous écran virtuel avec rendu logiciel.
- Mesurer les six critères de la fiche T05, chacun déclenché par le plugin, et les afficher en lignes PASS ou FAIL par `spikes/spike01_debugger/editor/run.sh`.
- Compléter la section SPIKE-01b de `docs/spikes/SPIKE-01.md` et proposer KEEP, REWRITE ou DISCARD.

## Fichiers autorisés

`spikes/spike01_debugger/editor/`, `docs/spikes/SPIKE-01.md`. La décision KEEP, REWRITE ou DISCARD est reportée dans `docs/DECISIONS.md` à la fusion.

Toujours autorisés en plus : `rapports/S10*.md` et les cases de cette fiche (par `cocher`).

## Contrôles propres à cette fiche

- `S10-a` : `GODOT="$B" spikes/spike01_debugger/editor/run.sh` → cinq lignes PASS et une ligne MESURÉ
- `S10-b` : `grep -c "SPIKE-01b" docs/spikes/SPIKE-01.md` → au moins 1, section avec les six critères
- `T05-a` : Rapport et section SPIKE-01b : six critères, chacun avec déclenchement, observation, chiffre → complet
- `T05-b` : Le vérificateur rejoue le critère 3 seul avec run.sh → même observation
- `T05-c` : (CE) Retirer le plugin sans envoyer l'arrêt → le jeu arrête seul sa collecte en 2 s au plus
- (CE) Faire envoyer au jeu un lot après « stopped » : le critère 3 passe à FAIL ; annuler.
- (CE) Retirer le contrôle du bail côté jeu : le critère 4 passe à FAIL ; annuler.

## Prompt de réalisation

```text
Tu réalises l'unité S10 « T05 SPIKE-01b, partie éditeur, sous écran virtuel » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.
Réalisation prévue : IA 1 (conception) ; vérification : IA 3 (vérification). Ton numéro d'IA est celui que te donne le prompt de créneau : tu le passes à --ia, et il signe chaque case que tu coches.

AVANT TOUT, depuis ton clone principal du dépôt
1. Lis REGLES_AGENTS.md s'il existe, puis cette fiche : suivi/S10-T05-spike01b.md.
2. python3 suivi/outil.py prendre S10 --ia <n>
   - « PRISE » ou « REPRISE » : tu es sur la branche tache/S10-T05-spike01b ; commence à la sous-étape affichée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
   - « REFUSÉ » : l'unité n'est pas pour toi maintenant (déjà prise par une autre IA, S02 non cochée, autre IA prévue) : reviens au prompt de créneau et choisis autre chose.

GODOT
- Si tools/ci/fetch_godot.sh existe : B=$(tools/ci/fetch_godot.sh 4.7.2-stable)
- Sinon, hors du dépôt :
  D=$HOME/.cache/gdm-godot/4.7.2-stable ; mkdir -p "$D"
  test -x "$D/Godot_v4.7.2-stable_linux.x86_64" || { curl -sSL -o /tmp/godot-4.7.2.zip https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip && unzip -o -q /tmp/godot-4.7.2.zip -d "$D"; }
  B=$D/Godot_v4.7.2-stable_linux.x86_64
- « godot » dans les commandes désigne "$B". Contrôle : "$B" --version contient 4.7.2.stable.
- Éditeur avec rendu, quand la fiche le demande : xvfb-run -a -s "-screen 0 1600x900x24" "$B" --editor --path <projet> --rendering-driver opengl3

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S10.md et les cases de suivi/S10-T05-spike01b.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status. Tu ne pousses jamais avec --force.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.
- Une décision réservée à l'humain (docs/construction/sequence.md §5) : arrêt obligatoire, rien d'autre.

TRACE OBLIGATOIRE, après CHAQUE sous-étape et avant la suivante
1. git add <les fichiers de la sous-étape> (jamais git add -A).
2. python3 suivi/outil.py cocher S10 <sous-étape> --ia <n>
   La commande vérifie l'ordre des cases et ton identité, coche la case dans suivi/S10-T05-spike01b.md, la signe (IA, date, heure UTC), commite et pousse sur tache/S10-T05-spike01b.
3. Une sous-étape faite mais non cochée par cette commande est considérée comme non faite : l'IA suivante la refera. Tu ne coches jamais une case à la main.
4. Tu ne modifies jamais SUIVI.md : il ne change qu'à la fusion, sous le verrou de main. Plusieurs IA le lisent en même temps ; aucune ne l'écrit hors de ce verrou.
5. Avant de cocher la dernière sous-étape R : « Statut : TERMINÉ » dans rapports/S10.md, puis git add.
6. Poussée refusée et non rattrapée par la commande : ne force jamais ; git pull --rebase origin tache/S10-T05-spike01b, puis relance la commande.

TRAVAIL TECHNIQUE — début (rédigé pour le mode autonome)
Tu conduis SPIKE-01b du projet GODOT_DEV_MAPPER, la partie éditeur du canal du débogueur. La partie jeu est établie : lis docs/spikes/SPIKE-01.md et spikes/spike01_debugger/.

FAIT VÉRIFIÉ le 8 octobre 2026, dans un conteneur sans GPU :
- l'éditeur Godot 4.7.2 tourne sous xvfb-run avec --rendering-driver opengl3 et un rendu logiciel (llvmpipe) ;
- un plugin peut lancer le jeu avec EditorInterface.play_main_scene() ;
- un EditorDebuggerPlugin reçoit les messages « flowspike:* » et en envoie par EditorDebuggerSession.send_message ;
- le plugin ne reçoit pas les messages du moteur (set_pid, output).
Vérifie de nouveau chaque API avant de t'y fier : EditorDebuggerPlugin (_has_capture, _capture, _setup_session), EditorDebuggerSession.send_message, EditorInterface.play_main_scene, stop_playing_scene, set_plugin_enabled.

CONTRAINTES
- Code jetable dans spikes/spike01_debugger/editor/ uniquement ; rien dans addons/.
- Aucune manipulation humaine : le plugin déclenche chaque scénario.

LES SIX CRITÈRES
1. « prêt » reçu par le plugin.
2. « started » reçu avant tout lot.
3. Arrêt avant la désactivation du plugin : « stopped » reçu en une seconde au plus, et aucun lot ensuite.
4. Coupure : jeu arrêté sans « stopped » → l'éditeur conclut « fin inconnue » ; plugin retiré sans arrêt → le bail arrête la collecte côté jeu en 2 s au plus.
5. Cinq lancements successifs depuis l'éditeur, sans erreur ni fuite.
6. Débit et cadence à 1 200 et 10 000 événements par seconde, avec le rendu logiciel. Marque ces chiffres « non représentatifs d'un GPU ».
Le critère des instances enregistrées avant le démarrage relève du runtime : il est vérifié en T13a, pas ici.

À PRODUIRE
- spikes/spike01_debugger/editor/run.sh : une commande qui rejoue tout et affiche une ligne par critère (PASS, FAIL, ou MESURÉ avec les chiffres pour le critère 6).
- La section SPIKE-01b de docs/spikes/SPIKE-01.md : pour chaque critère, déclenchement, observation, chiffre, statut ; les limites (rendu logiciel, conteneur).
- Une proposition KEEP, REWRITE ou DISCARD ; si nécessaire, le changement exact à faire au plan §6, dans le rapport, sans l'appliquer.
TRAVAIL TECHNIQUE — fin

CONTRÔLES DE LA FICHE
S10-a  GODOT="$B" spikes/spike01_debugger/editor/run.sh   → cinq lignes PASS et une ligne MESURÉ
S10-b  grep -c "SPIKE-01b" docs/spikes/SPIKE-01.md   → au moins 1, section avec les six critères
T05-a  Rapport et section SPIKE-01b : six critères, chacun avec déclenchement, observation, chiffre   → complet
T05-b  Le vérificateur rejoue le critère 3 seul avec run.sh   → même observation
T05-c  (CE) Retirer le plugin sans envoyer l'arrêt   → le jeu arrête seul sa collecte en 2 s au plus
(CE) Faire envoyer au jeu un lot après « stopped » : le critère 3 passe à FAIL ; annuler.
(CE) Retirer le contrôle du bail côté jeu : le critère 4 passe à FAIL ; annuler.

ADAPTATIONS DU MODE AUTONOME
- Aucune : suis le travail technique tel quel.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche ; après chacune, git add puis python3 suivi/outil.py cocher S10 R<k> --ia <n>.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Chaque sous-étape faite est cochée par `cocher`. Complète rapports/S10.md (sorties, « Passation » en cinq lignes au plus), git add, git commit, git push origin HEAD:tache/S10-T05-spike01b.
- git status ne montre aucune modification non commitée ; rien ne reste non poussé.

FORMAT DE rapports/S10.md (créé par prendre ; tu le complètes)
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

Après chaque sous-étape : `git add` de ses fichiers, puis `python3 suivi/outil.py cocher S10 R<k> --ia <n>` (coche, signe, commite, pousse).

- [ ] R0 Prise en charge : `python3 suivi/outil.py prendre S10 --ia <n>` (prérequis cochés dans `SUIVI.md` : S02 ; branche `tache/S10-T05-spike01b` créée ou reprise ; `rapports/S10.md` au statut EN COURS) ⟶ cochée par `prendre`
- [ ] R1 Lire `docs/spikes/SPIKE-01.md` et `spikes/spike01_debugger/` (jeu et récepteur). ⟶ cocher S10 R1
- [ ] R2 Obtenir Godot 4.7.2 ; vérifier l'écran virtuel : lancer l'éditeur 15 s sous xvfb-run sur `spikes/spike01_debugger/game` et retrouver « OpenGL API » dans la sortie. ⟶ cocher S10 R2
- [ ] R3 Créer le projet d'éditeur jetable : copie du jeu du spike et plugin de pilotage (EditorDebuggerPlugin et EditorPlugin). ⟶ cocher S10 R3
- [ ] R4 Critères 1 et 2 : « prêt » reçu ; « started » avant tout lot. ⟶ cocher S10 R4
- [ ] R5 Critère 3 : stop, « stopped » en 1 s au plus, aucun lot ensuite, puis désactivation du plugin. ⟶ cocher S10 R5
- [ ] R6 Critère 4 : jeu arrêté sans « stopped » → « fin inconnue » ; plugin retiré sans arrêt → bail côté jeu en 2 s au plus. ⟶ cocher S10 R6
- [ ] R7 Critère 5 : cinq lancements successifs sans erreur. Si deux commandes arrivent dans la même frame, remplacer la commande unique de FlowSpike par une file, et le noter : c'est un constat pour C-07. ⟶ cocher S10 R7
- [ ] R8 Critère 6 : débit et cadence à 1 200 et 10 000 événements par seconde, marqués « rendu logiciel, non représentatif d'un GPU ». ⟶ cocher S10 R8
- [ ] R9 Écrire `run.sh` : télécharge Godot au besoin, lance tout sous écran virtuel, affiche une ligne PASS ou FAIL par critère (critère 6 : MESURÉ avec les chiffres). ⟶ cocher S10 R9
- [ ] R10 Compléter la section SPIKE-01b de `docs/spikes/SPIKE-01.md` (critère, déclenchement, observation, chiffre, statut, limites) ; proposer KEEP, REWRITE ou DISCARD ; écrire dans le rapport le changement exact à faire au plan §6, sans l'appliquer. ⟶ cocher S10 R10
- [ ] R11 Contrôles finaux : S10-a, S10-b, T05-a, T05-b, T05-c exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » dans le rapport ⟶ cocher S10 R11

## Prompt de vérification

```text
Tu vérifies l'unité S10 « T05 SPIKE-01b, partie éditeur, sous écran virtuel » du projet GODOT_DEV_MAPPER. Vérification prévue : IA 3 (vérification). Ton numéro d'IA est celui du prompt de créneau. Tu n'es jamais un auteur de l'unité : la commande de prise le contrôle.

PRISE, depuis ton clone principal
python3 suivi/outil.py prendre S10 --ia <n> --verification
- « VÉRIFICATION PRISE » : copie neuve ../verif-S10-T05-spike01b créée sur origin/tache/S10-T05-spike01b, verdict EN COURS écrit, V1 cochée. cd ../verif-S10-T05-spike01b : toute la vérification se fait dans ce dossier.
- « REFUSÉ » : une autre IA vérifie déjà, tu es auteur, ou l'unité n'est pas terminée : reviens au prompt de créneau.
GODOT : même procédure que le prompt de réalisation.
Tu ne modifies aucun fichier de l'unité. Tu écris seulement ton verdict et tes cases V.

TRACE OBLIGATOIRE : après chaque sous-étape V, git add du fichier de verdict, puis python3 suivi/outil.py cocher S10 <V…> --ia <n>. Pour la dernière : --verdict ACCEPTÉE ou --verdict REFUSÉE, identique à la ligne « Verdict » du fichier. Une sous-étape non cochée par cette commande est considérée comme non faite.

1. TRAÇABILITÉ. Chaque case R cochée est signée « — IA n · date » et a son commit sur la branche (git log --oneline origin/main..HEAD). Case cochée sans travail prouvé dans le rapport : refus.
2. PÉRIMÈTRE. git diff --name-only origin/main...HEAD. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S10*.md et suivi/S10-T05-spike01b.md. Tout autre fichier : refus.
3. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : S10-a, S10-b, T05-a, T05-b, T05-c.
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
6. COHÉRENCE. Constats de SPIKE-01a ; protocole de session du plan §6 ; critères de la fiche T05 de `docs/orchestration.md`.

VERDICT dans rapports/S10-verif-<tentative>.md (créé par la prise) :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte

SI ACCEPTÉE — FUSION, depuis ton clone principal
1. python3 suivi/outil.py fusionner S10 --ia <n> --godot "$B"
   Elle prend le verrou de main (et attend s'il est pris), fusionne dans ../fusion-S10-T05-spike01b, lance run_all_checks.sh, coche la ligne dans SUIVI.md et la case F1. Si les contrôles échouent : verdict passé à REFUSÉE, main inchangée, verrou rendu ; arrête-toi sur cette unité.
2. cd ../fusion-S10-T05-spike01b ; fais les sous-étapes F suivantes de la fiche, et coche chacune : python3 suivi/outil.py cocher S10 F<k> --ia <n> (commit local, sans poussée).
3. python3 suivi/outil.py publier S10 --ia <n> : dernière case cochée, verifier relancé, main poussée, branche supprimée, verrou rendu.
SI REFUSÉE : arrête-toi sur cette unité ; son auteur la reprendra avec prendre.
```

## Sous-étapes de vérification

Dans `../verif-S10-T05-spike01b`, après chaque sous-étape : `git add` du verdict, puis `python3 suivi/outil.py cocher S10 V<k> --ia <n>`.

- [ ] V1 Prise en charge : `python3 suivi/outil.py prendre S10 --ia <n> --verification` (pas un auteur ; copie neuve `../verif-S10-T05-spike01b` sur `origin/tache/S10-T05-spike01b` ; verdict EN COURS) ⟶ cochée par `prendre`
- [ ] V2 Traçabilité : chaque case R cochée porte une signature « — IA n · date » et un commit sur la branche (`git log --oneline origin/main..HEAD`) ⟶ cocher S10 V2
- [ ] V3 Périmètre : `git diff --name-only origin/main...HEAD` ⊂ fichiers autorisés. ⟶ cocher S10 V3
- [ ] V4.1 Contrôle S10-a relancé, résultat conforme. ⟶ cocher S10 V4.1
- [ ] V4.2 Contrôle S10-b relancé, résultat conforme. ⟶ cocher S10 V4.2
- [ ] V4.3 Contrôle T05-a relancé, résultat conforme. ⟶ cocher S10 V4.3
- [ ] V4.4 Contrôle T05-b relancé, résultat conforme. ⟶ cocher S10 V4.4
- [ ] V4.5 Contrôle T05-c relancé, résultat conforme. ⟶ cocher S10 V4.5
- [ ] V5 Contre-épreuves (CE) appliquées et détectées, puis annulées. ⟶ cocher S10 V5
- [ ] V6 Contournements cherchés. ⟶ cocher S10 V6
- [ ] V7 Cohérence avec les contrats et les invariants. ⟶ cocher S10 V7
- [ ] V8 Verdict écrit dans `rapports/S10-verif-<tentative>.md` ⟶ cocher S10 V8 --verdict ACCEPTÉE ou --verdict REFUSÉE

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

F1 et la dernière se cochent par `fusionner` et `publier` ; les autres, dans `../fusion-S10-T05-spike01b`, par `python3 suivi/outil.py cocher S10 F<k> --ia <n>` (commit local).

- [ ] F1 Fusion : `python3 suivi/outil.py fusionner S10 --ia <n> --godot "$B"` : verrou de `main`, fusion `--no-ff` dans `../fusion-S10-T05-spike01b`, `tools/ci/run_all_checks.sh` sur `main` → ALL_CHECKS OK s'il existe (sinon fusion annulée et verdict passé à REFUSÉE), ligne **S10** cochée dans `SUIVI.md` ⟶ cochée par `fusionner`
- [ ] F2 Inscrire dans `docs/DECISIONS.md` la décision KEEP, REWRITE ou DISCARD de SPIKE-01b, au statut « adoptée par défaut », avec la date. ⟶ cocher S10 F2
- [ ] F3 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette ⟶ cocher S10 F3
- [ ] F4 Publication : `python3 suivi/outil.py publier S10 --ia <n>` (verifier OK, `main` poussée, branche `tache/S10-T05-spike01b` supprimée, verrou rendu) ⟶ cochée par `publier`

## Pour la recette

- Critère 6 de SPIKE-01b sur ta machine, avec GPU.
