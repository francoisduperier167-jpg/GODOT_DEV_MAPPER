# S10 — T05 SPIKE-01b, partie éditeur, sous écran virtuel

> Fiche d'exécution du mode autonome. Coche chaque case dès qu'elle est faite et prouvée, puis commite et pousse : une autre IA doit pouvoir reprendre à la première case non cochée. Règles : `docs/construction/sequence.md`. Avancement global : `SUIVI.md`.

| Champ | Valeur |
| --- | --- |
| Réalise | Concepteur |
| Vérifie | Vérificateur (jamais l'auteur) |
| Commence après | S02 (cochées dans `SUIVI.md`) |
| Indépendante de | S03, S04, S05, S06, S07, S08, S09, S11, S13 |
| Branche | `tache/S10-T05-spike01b` |
| Fiche de conception | `docs/construction/etape-2.md`, section T05 |
| Estimation | 2 créneaux |

**Séquentiel ou indépendant.** Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité elle-même peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Construire dans `spikes/spike01_debugger/editor/` un projet d'éditeur jetable dont le plugin déroule seul le scénario, sous écran virtuel avec rendu logiciel.
- Mesurer les six critères de la fiche T05, chacun déclenché par le plugin, et les afficher en lignes PASS ou FAIL par `spikes/spike01_debugger/editor/run.sh`.
- Compléter la section SPIKE-01b de `docs/spikes/SPIKE-01.md` et proposer KEEP, REWRITE ou DISCARD.

## Fichiers autorisés

`spikes/spike01_debugger/editor/`, `docs/spikes/SPIKE-01.md`. La décision KEEP, REWRITE ou DISCARD est reportée dans `docs/DECISIONS.md` à la fusion.

Toujours autorisés en plus : `rapports/S10*.md` et les cases de cette fiche.

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
Tu es <ton nom d'IA>, au rôle Concepteur. Tu réalises l'unité S10 « T05 SPIKE-01b, partie éditeur, sous écran virtuel » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.

AVANT TOUT
1. git fetch origin. Lis REGLES_AGENTS.md s'il existe, puis la fiche suivi/S10-T05-spike01b.md.
2. Si la branche origin/tache/S10-T05-spike01b existe : reprends-la, relis rapports/S10.md et commence à la première sous-étape R non cochée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
3. Sinon : vérifie dans SUIVI.md, sur main, que S02 est cochée, puis crée tache/S10-T05-spike01b depuis main.

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
- Tu coches une case seulement quand elle est faite et prouvée. Tu commites et tu pousses après chaque case cochée.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (rédigé pour le mode autonome)
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
TRAVAIL TECHNIQUE — fin de la copie exacte du guide

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

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche, et coche chacune.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Coche dans suivi/S10-T05-spike01b.md les sous-étapes faites et prouvées ; complète rapports/S10.md (sorties, section « Passation ») ; commite ; git push origin tache/S10-T05-spike01b.
- Ne laisse aucune modification non poussée.

FORMAT DE rapports/S10.md
- Statut : EN COURS | TERMINÉ | QUESTION | ESCALADE
- Auteur : <ton nom d'IA> · Tentative : n · Créneaux utilisés : n
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

- [ ] R0 Prise en charge : `git fetch origin` ; S02 est cochée dans `SUIVI.md` ; branche `origin/tache/S10-T05-spike01b` absente, ou sans commit depuis deux créneaux, ou dernier verdict REFUSÉE ; créer ou reprendre la branche ; `rapports/S10.md` avec « Statut : EN COURS » et « Auteur » ; commit ; push.
- [ ] R1 Lire `docs/spikes/SPIKE-01.md` et `spikes/spike01_debugger/` (jeu et récepteur).
- [ ] R2 Obtenir Godot 4.7.2 ; vérifier l'écran virtuel : lancer l'éditeur 15 s sous xvfb-run sur `spikes/spike01_debugger/game` et retrouver « OpenGL API » dans la sortie.
- [ ] R3 Créer le projet d'éditeur jetable : copie du jeu du spike et plugin de pilotage (EditorDebuggerPlugin et EditorPlugin).
- [ ] R4 Critères 1 et 2 : « prêt » reçu ; « started » avant tout lot.
- [ ] R5 Critère 3 : stop, « stopped » en 1 s au plus, aucun lot ensuite, puis désactivation du plugin.
- [ ] R6 Critère 4 : jeu arrêté sans « stopped » → « fin inconnue » ; plugin retiré sans arrêt → bail côté jeu en 2 s au plus.
- [ ] R7 Critère 5 : cinq lancements successifs sans erreur. Si deux commandes arrivent dans la même frame, remplacer la commande unique de FlowSpike par une file, et le noter : c'est un constat pour C-07.
- [ ] R8 Critère 6 : débit et cadence à 1 200 et 10 000 événements par seconde, marqués « rendu logiciel, non représentatif d'un GPU ».
- [ ] R9 Écrire `run.sh` : télécharge Godot au besoin, lance tout sous écran virtuel, affiche une ligne PASS ou FAIL par critère (critère 6 : MESURÉ avec les chiffres).
- [ ] R10 Compléter la section SPIKE-01b de `docs/spikes/SPIKE-01.md` (critère, déclenchement, observation, chiffre, statut, limites) ; proposer KEEP, REWRITE ou DISCARD ; écrire dans le rapport le changement exact à faire au plan §6, sans l'appliquer.
- [ ] R11 Contrôles finaux : S10-a, S10-b, T05-a, T05-b, T05-c exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » ; commit ; push.

## Prompt de vérification

```text
Tu es <ton nom d'IA>, au rôle Vérificateur, vérificateur indépendant de l'unité S10 « T05 SPIKE-01b, partie éditeur, sous écran virtuel » du projet GODOT_DEV_MAPPER.
Tu n'en es pas l'auteur : lis la ligne « Auteur » de rapports/S10.md ; si c'est toi, arrête-toi.
Tu ne modifies aucun fichier de l'unité. Tu écris ton verdict et tu coches les sous-étapes V, sur la branche.

COPIE NEUVE : git fetch origin && git worktree add --detach ../verif-S10-T05-spike01b origin/tache/S10-T05-spike01b
GODOT : même procédure que le prompt de réalisation.

1. PÉRIMÈTRE. git diff --name-only origin/main...origin/tache/S10-T05-spike01b. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S10*.md et suivi/S10-T05-spike01b.md. Tout autre fichier : refus.
2. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : S10-a, S10-b, T05-a, T05-b, T05-c.
3. CONTRE-ÉPREUVES. Applique chaque sabotage marqué (CE) dans la fiche et dans le travail technique ; vérifie que le contrôle échoue ; annule avec git checkout -- . && git clean -fd.
4. CONTOURNEMENTS. Cherche :
   - test sans assertion, ou toujours vrai ;
   - test désactivé, renommé ou sorti du runner ;
   - valeur attendue recopiée depuis la sortie du code ;
   - marqueur supprimé de tests/pending/ sans test qui passe ;
   - fixture invalide rejetée pour un autre motif que celui de son nom ;
   - API Godot inventée ou non vérifiée ;
   - dépendance interdite entre modules ; API sensible hors de la frontière de compatibilité ;
   - affirmation du rapport sans sortie qui la prouve.
5. COHÉRENCE. Constats de SPIKE-01a ; protocole de session du plan §6 ; critères de la fiche T05 de `docs/orchestration.md`.

VERDICT dans rapports/S10-verif-<tentative>.md :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte
Pousse le verdict sur la branche. Si ACCEPTÉE, fais les sous-étapes F de la fiche. Si REFUSÉE, arrête-toi : une IA au rôle de l'auteur reprendra.
```

## Sous-étapes de vérification

- [ ] V1 Prise en charge : pas l'auteur ; copie neuve `../verif-S10-T05-spike01b` sur `origin/tache/S10-T05-spike01b`.
- [ ] V2 Périmètre : `git diff --name-only origin/main...origin/tache/S10-T05-spike01b` ⊂ fichiers autorisés.
- [ ] V3.1 Contrôle S10-a relancé, résultat conforme.
- [ ] V3.2 Contrôle S10-b relancé, résultat conforme.
- [ ] V3.3 Contrôle T05-a relancé, résultat conforme.
- [ ] V3.4 Contrôle T05-b relancé, résultat conforme.
- [ ] V3.5 Contrôle T05-c relancé, résultat conforme.
- [ ] V4 Contre-épreuves (CE) appliquées et détectées, puis annulées.
- [ ] V5 Contournements cherchés.
- [ ] V6 Cohérence avec les contrats et les invariants.
- [ ] V7 Verdict écrit dans `rapports/S10-verif-<tentative>.md` et poussé.

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

- [ ] F1 `git switch main && git pull --ff-only && git merge --no-ff origin/tache/S10-T05-spike01b -m "Fusion S10 : T05 SPIKE-01b, partie éditeur, sous écran virtuel"`.
- [ ] F2 Sur `main` : `GODOT="$B" tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK. Sinon : `git reset --hard ORIG_HEAD`, verdict « REFUSÉE (fusion) » poussé sur la branche, et arrêt de la fusion.
- [ ] F3 Dans `SUIVI.md`, cocher la ligne **S10** et compléter « fait le <date> · auteur <IA> · vérifié par <IA> · <n> créneaux ».
- [ ] F4 Inscrire dans `docs/DECISIONS.md` la décision KEEP, REWRITE ou DISCARD de SPIKE-01b, au statut « adoptée par défaut », avec la date.
- [ ] F5 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette.
- [ ] F6 Cocher les sous-étapes F de cette fiche ; `git commit` ; `git push origin main` (en cas de refus : `git pull --rebase`, puis push).

## Pour la recette

- Critère 6 de SPIKE-01b sur ta machine, avec GPU.
