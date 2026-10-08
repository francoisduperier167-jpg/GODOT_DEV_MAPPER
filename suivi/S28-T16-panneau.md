# S28 — T16 Panneau du POC

> Fiche d'exécution du mode autonome. Coche chaque case dès qu'elle est faite et prouvée, puis commite et pousse : une autre IA doit pouvoir reprendre à la première case non cochée. Règles : `docs/construction/sequence.md`. Avancement global : `SUIVI.md`.

| Champ | Valeur |
| --- | --- |
| Réalise | Développeur |
| Vérifie | Vérificateur (jamais l'auteur) |
| Commence après | S17, S24 (cochées dans `SUIVI.md`) |
| Indépendante de | S21, S22, S23, S25, S26, S27, S30, S33 |
| Branche | `tache/S28-T16-panneau` |
| Fiche de conception | `docs/construction/etape-6.md`, section T16 |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité elle-même peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- `projections/journal_projection.gd` en logique pure (filtre par instance, pagination, regroupement par invocation, liste des instances, graphe déclaré en liste).
- `ui/poc_panel.tscn` et `poc_panel.gd` : sélecteur d'instance, journal virtualisé, arbre du graphe déclaré, 30 Hz au plus, GDM_PANEL_READY.
- Mesures de latence (aller-retour, délai réception → affichage) dans une zone de diagnostic ; tests et `checks.d/60-panel.sh`.

## Fichiers autorisés

`addons/godot_dev_mapper/projections/journal_projection.gd`, `addons/godot_dev_mapper/ui/poc_panel.tscn`, `addons/godot_dev_mapper/ui/poc_panel.gd`, `addons/godot_dev_mapper/editor/debugger_bridge.gd` (horodatage de réception), `addons/godot_dev_mapper/editor/latency_probe.gd` (nouveau : aller-retour), `addons/godot_dev_mapper/plugin.gd` (ajout du panneau), `tests/unit/test_journal_projection.gd`, `tools/ci/checks.d/60-panel.sh`.

Toujours autorisés en plus : `rapports/S28*.md` et les cases de cette fiche.

## Prompt de réalisation

```text
Tu es <ton nom d'IA>, au rôle Développeur. Tu réalises l'unité S28 « T16 Panneau du POC » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.

AVANT TOUT
1. git fetch origin. Lis REGLES_AGENTS.md s'il existe, puis la fiche suivi/S28-T16-panneau.md.
2. Si la branche origin/tache/S28-T16-panneau existe : reprends-la, relis rapports/S28.md et commence à la première sous-étape R non cochée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
3. Sinon : vérifie dans SUIVI.md, sur main, que S17, S24 sont cochées, puis crée tache/S28-T16-panneau depuis main.

GODOT
- Si tools/ci/fetch_godot.sh existe : B=$(tools/ci/fetch_godot.sh 4.7.2-stable)
- Sinon, hors du dépôt :
  D=$HOME/.cache/gdm-godot/4.7.2-stable ; mkdir -p "$D"
  test -x "$D/Godot_v4.7.2-stable_linux.x86_64" || { curl -sSL -o /tmp/godot-4.7.2.zip https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip && unzip -o -q /tmp/godot-4.7.2.zip -d "$D"; }
  B=$D/Godot_v4.7.2-stable_linux.x86_64
- « godot » dans les commandes désigne "$B". Contrôle : "$B" --version contient 4.7.2.stable.
- Éditeur avec rendu, quand la fiche le demande : xvfb-run -a -s "-screen 0 1600x900x24" "$B" --editor --path <projet> --rendering-driver opengl3

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S28.md et les cases de suivi/S28-T16-panneau.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu coches une case seulement quand elle est faite et prouvée. Tu commites et tu pousses après chaque case cochée.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (docs/construction/etape-6.md, T16)
Tu réalises la tâche T16 du projet GODOT_DEV_MAPPER. Applique les règles et le format de rapport du prompt universel de réalisation.
CONTEXTE : docs/CONTRACTS.md, sections C-05 et C-06 ; plan §7 (le POC n'a pas de graphe dessiné) ; plan §8 (budgets d'affichage).

OBJECTIF
1. projections/journal_projection.gd, en logique pure :
   - filtre par instance, pagination, regroupement par invocation ;
   - liste des instances d'une session ;
   - graphe déclaré présenté en liste arborescente.
2. ui/poc_panel.tscn et poc_panel.gd :
   - un sélecteur d'instance, un journal virtualisé, l'arbre du graphe déclaré ;
   - rafraîchissement à 30 Hz au plus ;
   - GDM_PANEL_READY affiché si GDM_TRACE_LIFECYCLE vaut 1.
3. Mesures de latence, affichées dans une zone de diagnostic du panneau :
   - aller-retour du transport : l'éditeur envoie un ping horodaté par sa propre horloge, le jeu le renvoie, l'éditeur calcule ;
   - délai réception → affichage : la passerelle horodate chaque lot à sa réception ; le panneau calcule l'écart quand il affiche ses événements ; 95e centile sur la session ;
   - latence estimée : moitié de l'aller-retour plus ce délai.
4. tests/unit/test_journal_projection.gd, avec un test de tenue en charge sur 10 000 événements (seuil : 50 ms) et un test du délai réception → affichage avec une horloge factice.
5. tools/ci/checks.d/60-panel.sh : rejoue le contrôle T16-b et affiche « CHECK panel OK » ou « CHECK panel KO ».

CONTRÔLES
T16-a  runner → 0
T16-b  GDM_TRACE_LIFECYCLE=1 godot --headless --editor --path . --quit-after 300 > /tmp/ed.out 2>&1 ; grep -c GDM_PANEL_READY /tmp/ed.out ; grep -cE "^(ERROR|SCRIPT ERROR)" /tmp/ed.out   → 1 et 0
T16-c  python3 tools/check_deps.py ; echo $?   → 0 ; ui/ ne lit jamais le store directement
T16-d  GODOT=<binaire> tools/ci/run_all_checks.sh ; echo $?   → 0
T16-e  Test du délai réception → affichage, avec une horloge factice → vert ; la zone de diagnostic affiche les deux mesures
CONTRE-ÉPREUVE (CE) pour le vérificateur : ignorer le filtre d'instance dans la projection → test_journal_projection échoue.
SUR MA MACHINE, plus tard (PC6.7) : la procédure pour les captures d'écran et la mesure de latence, écrite dans ton rapport.
TRAVAIL TECHNIQUE — fin de la copie exacte du guide

ADAPTATIONS DU MODE AUTONOME
- Les fichiers autorisés sont plus étroits que dans le guide : `editor/session_controller.gd` n'est pas modifié ici, pour que S30 puisse avancer en même temps. L'aller-retour passe par le nouveau fichier `editor/latency_probe.gd`.
- « SUR MA MACHINE, plus tard (PC6.7) » : exécuté en S31 sous écran virtuel ; la mesure sur GPU passe à la recette.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche, et coche chacune.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Coche dans suivi/S28-T16-panneau.md les sous-étapes faites et prouvées ; complète rapports/S28.md (sorties, section « Passation ») ; commite ; git push origin tache/S28-T16-panneau.
- Ne laisse aucune modification non poussée.

FORMAT DE rapports/S28.md
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

- [ ] R0 Prise en charge : `git fetch origin` ; S17, S24 sont cochées dans `SUIVI.md` ; branche `origin/tache/S28-T16-panneau` absente, ou sans commit depuis deux créneaux, ou dernier verdict REFUSÉE ; créer ou reprendre la branche ; `rapports/S28.md` avec « Statut : EN COURS » et « Auteur » ; commit ; push.
- [ ] R1 Écrire `projections/journal_projection.gd`.
- [ ] R2 Écrire `ui/poc_panel.tscn` et `ui/poc_panel.gd`.
- [ ] R3 Ajouter l'horodatage de réception dans `debugger_bridge.gd` et l'aller-retour dans `editor/latency_probe.gd`.
- [ ] R4 Ajouter le panneau dans `plugin.gd`.
- [ ] R5 Écrire `tests/unit/test_journal_projection.gd` (dont 10 000 événements sous 50 ms et l'horloge factice).
- [ ] R6 Écrire `tools/ci/checks.d/60-panel.sh`.
- [ ] R7 Écrire dans le rapport la procédure de captures et de mesure de latence, que S31 exécutera.
- [ ] R8 Contrôles finaux : T16-a, T16-b, T16-c, T16-d, T16-e exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » ; commit ; push.

## Prompt de vérification

```text
Tu es <ton nom d'IA>, au rôle Vérificateur, vérificateur indépendant de l'unité S28 « T16 Panneau du POC » du projet GODOT_DEV_MAPPER.
Tu n'en es pas l'auteur : lis la ligne « Auteur » de rapports/S28.md ; si c'est toi, arrête-toi.
Tu ne modifies aucun fichier de l'unité. Tu écris ton verdict et tu coches les sous-étapes V, sur la branche.

COPIE NEUVE : git fetch origin && git worktree add --detach ../verif-S28-T16-panneau origin/tache/S28-T16-panneau
GODOT : même procédure que le prompt de réalisation.

1. PÉRIMÈTRE. git diff --name-only origin/main...origin/tache/S28-T16-panneau. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S28*.md et suivi/S28-T16-panneau.md. Tout autre fichier : refus.
2. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : T16-a, T16-b, T16-c, T16-d, T16-e.
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
5. COHÉRENCE. C-05, C-06 ; plan §7 et §8 ; l'interface ne calcule rien.

VERDICT dans rapports/S28-verif-<tentative>.md :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte
Pousse le verdict sur la branche. Si ACCEPTÉE, fais les sous-étapes F de la fiche. Si REFUSÉE, arrête-toi : une IA au rôle de l'auteur reprendra.
```

## Sous-étapes de vérification

- [ ] V1 Prise en charge : pas l'auteur ; copie neuve `../verif-S28-T16-panneau` sur `origin/tache/S28-T16-panneau`.
- [ ] V2 Périmètre : `git diff --name-only origin/main...origin/tache/S28-T16-panneau` ⊂ fichiers autorisés.
- [ ] V3.1 Contrôle T16-a relancé, résultat conforme.
- [ ] V3.2 Contrôle T16-b relancé, résultat conforme.
- [ ] V3.3 Contrôle T16-c relancé, résultat conforme.
- [ ] V3.4 Contrôle T16-d relancé, résultat conforme.
- [ ] V3.5 Contrôle T16-e relancé, résultat conforme.
- [ ] V4 Contre-épreuves (CE) appliquées et détectées, puis annulées.
- [ ] V5 Contournements cherchés.
- [ ] V6 Cohérence avec les contrats et les invariants.
- [ ] V7 Verdict écrit dans `rapports/S28-verif-<tentative>.md` et poussé.

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

- [ ] F1 `git switch main && git pull --ff-only && git merge --no-ff origin/tache/S28-T16-panneau -m "Fusion S28 : T16 Panneau du POC"`.
- [ ] F2 Sur `main` : `GODOT="$B" tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK. Sinon : `git reset --hard ORIG_HEAD`, verdict « REFUSÉE (fusion) » poussé sur la branche, et arrêt de la fusion.
- [ ] F3 Dans `SUIVI.md`, cocher la ligne **S28** et compléter « fait le <date> · auteur <IA> · vérifié par <IA> · <n> créneaux ».
- [ ] F4 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette.
- [ ] F5 Cocher les sous-étapes F de cette fiche ; `git commit` ; `git push origin main` (en cas de refus : `git pull --rebase`, puis push).

## Pour la recette

Rien de propre à cette unité.
