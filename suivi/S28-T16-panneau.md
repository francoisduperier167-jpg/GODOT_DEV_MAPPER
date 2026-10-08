# S28 — T16 Panneau du POC

> Fiche d'exécution du mode autonome. Chaque case se coche avec `python3 suivi/outil.py cocher S28 <sous-étape> --ia <n>`, juste après la sous-étape : la commande vérifie l'ordre et l'identité de l'IA, signe la case (IA, date, heure UTC), commite et pousse. Une sous-étape non cochée par cette commande est considérée comme non faite. Règles : `docs/construction/sequence.md`. Avancement : `SUIVI.md` et `suivi/tableau.html`.

| Champ | Valeur |
| --- | --- |
| Réalise | IA 2 (développement) |
| Vérifie | IA 3 (vérification), jamais un auteur de l'unité |
| Piste | 6.A Panneau et chemin observé : S28 → S29 → S31 (unité 1 sur 3) |
| Commence après | S17, S24 (cochées dans `SUIVI.md`) |
| Indépendante de | S21, S22, S23, S25, S26, S27, S30, S33 |
| Branche | `tache/S28-T16-panneau` |
| Fiche de conception | `docs/construction/etape-6.md`, section T16 |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Cette unité est la 1re de la piste 6.A « Panneau et chemin observé », dont les unités se font à la suite. Les autres pistes de la section (6.B) avancent en même temps, chacune de son côté. Elle attend S17, S24, hors de la piste. S29 l'attendra. Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- `projections/journal_projection.gd` en logique pure (filtre par instance, pagination, regroupement par invocation, liste des instances, graphe déclaré en liste).
- `ui/poc_panel.tscn` et `poc_panel.gd` : sélecteur d'instance, journal virtualisé, arbre du graphe déclaré, 30 Hz au plus, GDM_PANEL_READY.
- Mesures de latence (aller-retour, délai réception → affichage) dans une zone de diagnostic ; tests et `checks.d/60-panel.sh`.

## Fichiers autorisés

`addons/godot_dev_mapper/projections/journal_projection.gd`, `addons/godot_dev_mapper/ui/poc_panel.tscn`, `addons/godot_dev_mapper/ui/poc_panel.gd`, `addons/godot_dev_mapper/editor/debugger_bridge.gd` (horodatage de réception), `addons/godot_dev_mapper/editor/latency_probe.gd` (nouveau : aller-retour), `addons/godot_dev_mapper/plugin.gd` (ajout du panneau), `tests/unit/test_journal_projection.gd`, `tools/ci/checks.d/60-panel.sh`.

Toujours autorisés en plus : `rapports/S28*.md` et les cases de cette fiche (par `cocher`).

## Prompt de réalisation

```text
Tu réalises l'unité S28 « T16 Panneau du POC » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.
Réalisation prévue : IA 2 (développement) ; vérification : IA 3 (vérification). Ton numéro d'IA est celui que te donne le prompt de créneau : tu le passes à --ia, et il signe chaque case que tu coches.

AVANT TOUT, depuis ton clone principal du dépôt
1. Lis REGLES_AGENTS.md s'il existe, puis cette fiche : suivi/S28-T16-panneau.md.
2. python3 suivi/outil.py prendre S28 --ia <n>
   - « PRISE » ou « REPRISE » : tu es sur la branche tache/S28-T16-panneau ; commence à la sous-étape affichée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
   - « REFUSÉ » : l'unité n'est pas pour toi maintenant (déjà prise par une autre IA, S17, S24 non cochées, autre IA prévue) : reviens au prompt de créneau et choisis autre chose.

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
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status. Tu ne pousses jamais avec --force.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.
- Une décision réservée à l'humain (docs/construction/sequence.md §5) : arrêt obligatoire, rien d'autre : python3 suivi/outil.py arreter --ia <n> --unite S28 --raison "<raison>", puis fin du créneau.

TRACE OBLIGATOIRE, après CHAQUE sous-étape et avant la suivante
1. git add <les fichiers de la sous-étape> (jamais git add -A).
2. python3 suivi/outil.py cocher S28 <sous-étape> --ia <n>
   La commande vérifie l'ordre des cases et ton identité, coche la case dans suivi/S28-T16-panneau.md, la signe (IA, date, heure UTC), commite et pousse sur tache/S28-T16-panneau.
3. Une sous-étape faite mais non cochée par cette commande est considérée comme non faite : l'IA suivante la refera. Tu ne coches jamais une case à la main.
4. Tu ne modifies jamais SUIVI.md : il ne change qu'à la fusion, sous le verrou de main. Plusieurs IA le lisent en même temps ; aucune ne l'écrit hors de ce verrou.
5. Avant de cocher la dernière sous-étape R : « Statut : TERMINÉ » dans rapports/S28.md, puis git add.
6. Poussée refusée et non rattrapée par la commande : ne force jamais ; git pull --rebase origin tache/S28-T16-panneau, puis relance la commande.

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

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche ; après chacune, git add puis python3 suivi/outil.py cocher S28 R<k> --ia <n>.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Chaque sous-étape faite est cochée par `cocher`. Complète rapports/S28.md (sorties, « Passation » en cinq lignes au plus), git add, git commit, git push origin HEAD:tache/S28-T16-panneau.
- git status ne montre aucune modification non commitée ; rien ne reste non poussé.

FORMAT DE rapports/S28.md (créé par prendre ; tu le complètes)
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

Après chaque sous-étape : `git add` de ses fichiers, puis `python3 suivi/outil.py cocher S28 R<k> --ia <n>` (coche, signe, commite, pousse).

- [ ] R0 Prise en charge : `python3 suivi/outil.py prendre S28 --ia <n>` (prérequis cochés dans `SUIVI.md` : S17, S24 ; branche `tache/S28-T16-panneau` créée ou reprise ; `rapports/S28.md` au statut EN COURS) ⟶ cochée par `prendre`
- [ ] R1 Écrire `projections/journal_projection.gd`. ⟶ cocher S28 R1
- [ ] R2 Écrire `ui/poc_panel.tscn` et `ui/poc_panel.gd`. ⟶ cocher S28 R2
- [ ] R3 Ajouter l'horodatage de réception dans `debugger_bridge.gd` et l'aller-retour dans `editor/latency_probe.gd`. ⟶ cocher S28 R3
- [ ] R4 Ajouter le panneau dans `plugin.gd`. ⟶ cocher S28 R4
- [ ] R5 Écrire `tests/unit/test_journal_projection.gd` (dont 10 000 événements sous 50 ms et l'horloge factice). ⟶ cocher S28 R5
- [ ] R6 Écrire `tools/ci/checks.d/60-panel.sh`. ⟶ cocher S28 R6
- [ ] R7 Écrire dans le rapport la procédure de captures et de mesure de latence, que S31 exécutera. ⟶ cocher S28 R7
- [ ] R8 Contrôles finaux : T16-a, T16-b, T16-c, T16-d, T16-e exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » dans le rapport ⟶ cocher S28 R8

## Prompt de vérification

```text
Tu vérifies l'unité S28 « T16 Panneau du POC » du projet GODOT_DEV_MAPPER. Vérification prévue : IA 3 (vérification). Ton numéro d'IA est celui du prompt de créneau. Tu n'es jamais un auteur de l'unité : la commande de prise le contrôle.

PRISE, depuis ton clone principal
python3 suivi/outil.py prendre S28 --ia <n> --verification
- « VÉRIFICATION PRISE » : copie neuve ../verif-S28-T16-panneau créée sur origin/tache/S28-T16-panneau, verdict EN COURS écrit, V1 cochée. cd ../verif-S28-T16-panneau : toute la vérification se fait dans ce dossier.
- « REFUSÉ » : une autre IA vérifie déjà, tu es auteur, ou l'unité n'est pas terminée : reviens au prompt de créneau.
- Créneau fini avant le verdict : au créneau suivant, etat te propose la même commande ; elle recrée la copie (« VÉRIFICATION REPRISE ») et tu reprends à la première case V ouverte.
GODOT : même procédure que le prompt de réalisation.
Tu ne modifies aucun fichier de l'unité. Tu écris seulement ton verdict et tes cases V.

TRACE OBLIGATOIRE : après chaque sous-étape V, git add du fichier de verdict, puis python3 suivi/outil.py cocher S28 <V…> --ia <n>. Pour la dernière : --verdict ACCEPTÉE ou --verdict REFUSÉE, identique à la ligne « Verdict » du fichier. Une sous-étape non cochée par cette commande est considérée comme non faite.

1. TRAÇABILITÉ. Chaque case R cochée est signée « — IA n · date » et a son commit sur la branche (git log --oneline origin/main..HEAD). Case cochée sans travail prouvé dans le rapport : refus.
2. PÉRIMÈTRE. git diff --name-only origin/main...HEAD. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S28*.md et suivi/S28-T16-panneau.md. Tout autre fichier : refus.
3. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : T16-a, T16-b, T16-c, T16-d, T16-e.
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
6. COHÉRENCE. C-05, C-06 ; plan §7 et §8 ; l'interface ne calcule rien.

VERDICT dans rapports/S28-verif-<tentative>.md (créé par la prise) :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte

SI ACCEPTÉE — FUSION, depuis ton clone principal (cd hors de ../verif-S28-T16-panneau)
1. python3 suivi/outil.py fusionner S28 --ia <n>
   Elle trouve Godot (--godot, $GODOT, cache du bloc GODOT ou tools/ci/fetch_godot.sh ; sans Godot : REFUSÉ, verdict inchangé), prend le verrou de main (et attend s'il est pris), revérifie l'unité, fusionne dans ../fusion-S28-T16-panneau, lance run_all_checks.sh, coche la ligne dans SUIVI.md et la case F1. Si les contrôles échouent : verdict passé à REFUSÉE, main inchangée, verrou rendu ; arrête-toi sur cette unité. La fusion te revient parce que tu as signé le verdict ; une autre IA ne la fait qu'après 12 h.
2. cd ../fusion-S28-T16-panneau ; fais les sous-étapes F suivantes de la fiche, et coche chacune : python3 suivi/outil.py cocher S28 F<k> --ia <n> (commit local, sans poussée).
3. python3 suivi/outil.py publier S28 --ia <n> : dernière case cochée, verifier relancé, main poussée, branche supprimée, verrou rendu.
SI REFUSÉE : arrête-toi sur cette unité ; son auteur la reprendra avec prendre.
```

## Sous-étapes de vérification

Dans `../verif-S28-T16-panneau`, après chaque sous-étape : `git add` du verdict, puis `python3 suivi/outil.py cocher S28 V<k> --ia <n>`.

- [ ] V1 Prise en charge : `python3 suivi/outil.py prendre S28 --ia <n> --verification` (pas un auteur ; copie neuve `../verif-S28-T16-panneau` sur `origin/tache/S28-T16-panneau` ; verdict EN COURS) ⟶ cochée par `prendre`
- [ ] V2 Traçabilité : chaque case R cochée porte une signature « — IA n · date » et un commit sur la branche (`git log --oneline origin/main..HEAD`) ⟶ cocher S28 V2
- [ ] V3 Périmètre : `git diff --name-only origin/main...HEAD` ⊂ fichiers autorisés. ⟶ cocher S28 V3
- [ ] V4.1 Contrôle T16-a relancé, résultat conforme. ⟶ cocher S28 V4.1
- [ ] V4.2 Contrôle T16-b relancé, résultat conforme. ⟶ cocher S28 V4.2
- [ ] V4.3 Contrôle T16-c relancé, résultat conforme. ⟶ cocher S28 V4.3
- [ ] V4.4 Contrôle T16-d relancé, résultat conforme. ⟶ cocher S28 V4.4
- [ ] V4.5 Contrôle T16-e relancé, résultat conforme. ⟶ cocher S28 V4.5
- [ ] V5 Contre-épreuves (CE) appliquées et détectées, puis annulées. ⟶ cocher S28 V5
- [ ] V6 Contournements cherchés. ⟶ cocher S28 V6
- [ ] V7 Cohérence avec les contrats et les invariants. ⟶ cocher S28 V7
- [ ] V8 Verdict écrit dans `rapports/S28-verif-<tentative>.md` ⟶ cocher S28 V8 --verdict ACCEPTÉE ou --verdict REFUSÉE

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

F1 et la dernière se cochent par `fusionner` et `publier` ; les autres, dans `../fusion-S28-T16-panneau`, par `python3 suivi/outil.py cocher S28 F<k> --ia <n>` (commit local).

- [ ] F1 Fusion, depuis le clone principal : `python3 suivi/outil.py fusionner S28 --ia <n>` : Godot trouvé seul (--godot, $GODOT, cache du bloc GODOT ou fetch_godot.sh), verrou de `main`, fusion `--no-ff` dans `../fusion-S28-T16-panneau`, `tools/ci/run_all_checks.sh` sur `main` → ALL_CHECKS OK s'il existe (sinon fusion annulée et verdict passé à REFUSÉE), ligne **S28** cochée dans `SUIVI.md` ⟶ cochée par `fusionner`
- [ ] F2 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette ⟶ cocher S28 F2
- [ ] F3 Publication : `python3 suivi/outil.py publier S28 --ia <n>` (verifier OK, `main` poussée, branche `tache/S28-T16-panneau` supprimée, verrou rendu) ⟶ cochée par `publier`

## Pour la recette

Rien de propre à cette unité.
