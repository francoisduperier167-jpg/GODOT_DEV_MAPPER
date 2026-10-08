# S24 — T14 Réception côté éditeur

> Fiche d'exécution du mode autonome. Coche chaque case dès qu'elle est faite et prouvée, puis commite et pousse : une autre IA doit pouvoir reprendre à la première case non cochée. Règles : `docs/construction/sequence.md`. Avancement global : `SUIVI.md`.

| Champ | Valeur |
| --- | --- |
| Réalise | Développeur |
| Vérifie | Vérificateur (jamais l'auteur) |
| Commence après | S18, S20 (cochées dans `SUIVI.md`) |
| Indépendante de | S21, S22, S23, S25, S33 |
| Branche | `tache/S24-T14-reception` |
| Fiche de conception | `docs/construction/etape-5.md`, section T14 |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité elle-même peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- `editor/session_controller.gd` en logique pure : protocole de session côté éditeur, « fin inconnue », messages du moteur ignorés, lots validés puis rangés dans l'Event Store ; temps fourni de l'extérieur.
- `editor/debugger_bridge.gd`, passerelle mince ; `plugin.gd` : enregistrement et retrait de la passerelle seulement.
- `tests/unit/test_session_controller.gd` (rejoue chaque session enregistrée) et `tools/ci/checks.d/50-bridge.sh`.

## Fichiers autorisés

`addons/godot_dev_mapper/editor/debugger_bridge.gd`, `addons/godot_dev_mapper/editor/session_controller.gd`, `addons/godot_dev_mapper/plugin.gd` (enregistrement de la passerelle uniquement), `tests/unit/test_session_controller.gd`, `tools/ci/checks.d/50-bridge.sh`.

Toujours autorisés en plus : `rapports/S24*.md` et les cases de cette fiche.

## Prompt de réalisation

```text
Tu es <ton nom d'IA>, au rôle Développeur. Tu réalises l'unité S24 « T14 Réception côté éditeur » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.

AVANT TOUT
1. git fetch origin. Lis REGLES_AGENTS.md s'il existe, puis la fiche suivi/S24-T14-reception.md.
2. Si la branche origin/tache/S24-T14-reception existe : reprends-la, relis rapports/S24.md et commence à la première sous-étape R non cochée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
3. Sinon : vérifie dans SUIVI.md, sur main, que S18, S20 sont cochées, puis crée tache/S24-T14-reception depuis main.

GODOT
- Si tools/ci/fetch_godot.sh existe : B=$(tools/ci/fetch_godot.sh 4.7.2-stable)
- Sinon, hors du dépôt :
  D=$HOME/.cache/gdm-godot/4.7.2-stable ; mkdir -p "$D"
  test -x "$D/Godot_v4.7.2-stable_linux.x86_64" || { curl -sSL -o /tmp/godot-4.7.2.zip https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip && unzip -o -q /tmp/godot-4.7.2.zip -d "$D"; }
  B=$D/Godot_v4.7.2-stable_linux.x86_64
- « godot » dans les commandes désigne "$B". Contrôle : "$B" --version contient 4.7.2.stable.
- Éditeur avec rendu, quand la fiche le demande : xvfb-run -a -s "-screen 0 1600x900x24" "$B" --editor --path <projet> --rendering-driver opengl3

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S24.md et les cases de suivi/S24-T14-reception.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu coches une case seulement quand elle est faite et prouvée. Tu commites et tu pousses après chaque case cochée.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (docs/construction/etape-5.md, T14)
Tu réalises la tâche T14 du projet GODOT_DEV_MAPPER. Applique les règles et le format de rapport du prompt universel de réalisation.
CONTEXTE : docs/CONTRACTS.md, sections C-03 (façade débogueur), C-04, C-06 et C-07 ; docs/spikes/SPIKE-01.md, section 01b ; tests/contract/fixtures/sessions/.

OBJECTIF
1. editor/session_controller.gd, en logique pure, sans aucune API d'éditeur :
   - côté éditeur du protocole de session : prêt, démarrage, bail toutes les 250 ms, arrêt avec attente d'une seconde au plus ;
   - « fin inconnue » si le message de fin manque ;
   - messages du moteur ignorés ;
   - lots validés par le codec, puis rangés dans l'Event Store.
   Le temps lui est fourni de l'extérieur, pour être testable.
2. editor/debugger_bridge.gd : la passerelle mince. Elle relaie les messages de la façade débogueur vers le contrôleur, et ses ordres vers la session. Elle affiche GDM_BRIDGE_READY si GDM_TRACE_LIFECYCLE vaut 1.
3. plugin.gd : seulement l'enregistrement et le retrait de la passerelle.
4. tests/unit/test_session_controller.gd : rejoue chaque session de tests/contract/fixtures/sessions/ et vérifie l'état final attendu.
5. tools/ci/checks.d/50-bridge.sh : rejoue le contrôle T14-b et affiche « CHECK bridge OK » ou « CHECK bridge KO ».

CONTRÔLES
T14-a  runner → 0, tests du contrôleur verts
T14-b  GDM_TRACE_LIFECYCLE=1 godot --headless --editor --path . --quit-after 300 > /tmp/ed.out 2>&1 ; grep -c GDM_BRIDGE_READY /tmp/ed.out ; grep -cE "^(ERROR|SCRIPT ERROR)" /tmp/ed.out   → 1 et 0
T14-c  python3 tools/check_deps.py ; echo $?   → 0 ; session_controller.gd sans API sensible
T14-d  GODOT=<binaire> tools/ci/run_all_checks.sh ; echo $?   → 0
CONTRE-ÉPREUVES (CE) pour le vérificateur
- arrêter le bail dans le contrôleur → le test de la session coupée échoue ;
- traiter « set_pid » comme un lot → le test de la session mêlée échoue.
SUR MA MACHINE, plus tard (PC5.6) : la procédure exacte pour vérifier une vraie session, écrite dans ton rapport.
TRAVAIL TECHNIQUE — fin de la copie exacte du guide

ADAPTATIONS DU MODE AUTONOME
- « SUR MA MACHINE, plus tard (PC5.6) » : l'essai se fait en S26, sous écran virtuel. Écris la procédure pour S26.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche, et coche chacune.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Coche dans suivi/S24-T14-reception.md les sous-étapes faites et prouvées ; complète rapports/S24.md (sorties, section « Passation ») ; commite ; git push origin tache/S24-T14-reception.
- Ne laisse aucune modification non poussée.

FORMAT DE rapports/S24.md
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

- [ ] R0 Prise en charge : `git fetch origin` ; S18, S20 sont cochées dans `SUIVI.md` ; branche `origin/tache/S24-T14-reception` absente, ou sans commit depuis deux créneaux, ou dernier verdict REFUSÉE ; créer ou reprendre la branche ; `rapports/S24.md` avec « Statut : EN COURS » et « Auteur » ; commit ; push.
- [ ] R1 Écrire `editor/session_controller.gd`.
- [ ] R2 Écrire `editor/debugger_bridge.gd`.
- [ ] R3 Modifier `plugin.gd` : enregistrement et retrait de la passerelle.
- [ ] R4 Écrire `tests/unit/test_session_controller.gd`.
- [ ] R5 Écrire `tools/ci/checks.d/50-bridge.sh`.
- [ ] R6 Écrire dans le rapport la procédure de l'essai dans l'éditeur, que S26 exécutera sous écran virtuel.
- [ ] R7 Contrôles finaux : T14-a, T14-b, T14-c, T14-d exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » ; commit ; push.

## Prompt de vérification

```text
Tu es <ton nom d'IA>, au rôle Vérificateur, vérificateur indépendant de l'unité S24 « T14 Réception côté éditeur » du projet GODOT_DEV_MAPPER.
Tu n'en es pas l'auteur : lis la ligne « Auteur » de rapports/S24.md ; si c'est toi, arrête-toi.
Tu ne modifies aucun fichier de l'unité. Tu écris ton verdict et tu coches les sous-étapes V, sur la branche.

COPIE NEUVE : git fetch origin && git worktree add --detach ../verif-S24-T14-reception origin/tache/S24-T14-reception
GODOT : même procédure que le prompt de réalisation.

1. PÉRIMÈTRE. git diff --name-only origin/main...origin/tache/S24-T14-reception. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S24*.md et suivi/S24-T14-reception.md. Tout autre fichier : refus.
2. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : T14-a, T14-b, T14-c, T14-d.
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
5. COHÉRENCE. C-03 (façade débogueur), C-04, C-06, C-07 ; section 01b de SPIKE-01.

VERDICT dans rapports/S24-verif-<tentative>.md :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte
Pousse le verdict sur la branche. Si ACCEPTÉE, fais les sous-étapes F de la fiche. Si REFUSÉE, arrête-toi : une IA au rôle de l'auteur reprendra.
```

## Sous-étapes de vérification

- [ ] V1 Prise en charge : pas l'auteur ; copie neuve `../verif-S24-T14-reception` sur `origin/tache/S24-T14-reception`.
- [ ] V2 Périmètre : `git diff --name-only origin/main...origin/tache/S24-T14-reception` ⊂ fichiers autorisés.
- [ ] V3.1 Contrôle T14-a relancé, résultat conforme.
- [ ] V3.2 Contrôle T14-b relancé, résultat conforme.
- [ ] V3.3 Contrôle T14-c relancé, résultat conforme.
- [ ] V3.4 Contrôle T14-d relancé, résultat conforme.
- [ ] V4 Contre-épreuves (CE) appliquées et détectées, puis annulées.
- [ ] V5 Contournements cherchés.
- [ ] V6 Cohérence avec les contrats et les invariants.
- [ ] V7 Verdict écrit dans `rapports/S24-verif-<tentative>.md` et poussé.

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

- [ ] F1 `git switch main && git pull --ff-only && git merge --no-ff origin/tache/S24-T14-reception -m "Fusion S24 : T14 Réception côté éditeur"`.
- [ ] F2 Sur `main` : `GODOT="$B" tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK. Sinon : `git reset --hard ORIG_HEAD`, verdict « REFUSÉE (fusion) » poussé sur la branche, et arrêt de la fusion.
- [ ] F3 Dans `SUIVI.md`, cocher la ligne **S24** et compléter « fait le <date> · auteur <IA> · vérifié par <IA> · <n> créneaux ».
- [ ] F4 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette.
- [ ] F5 Cocher les sous-étapes F de cette fiche ; `git commit` ; `git push origin main` (en cas de refus : `git pull --rebase`, puis push).

## Pour la recette

Rien de propre à cette unité.
