# S24 — T14 Réception côté éditeur

> Fiche d'exécution du mode autonome. Chaque case se coche avec `python3 suivi/outil.py cocher S24 <sous-étape> --ia <n>`, juste après la sous-étape : la commande vérifie l'ordre et l'identité de l'IA, signe la case (IA, date, heure UTC), commite et pousse. Une sous-étape non cochée par cette commande est considérée comme non faite. Règles : `docs/construction/sequence.md`. Avancement : `SUIVI.md` et `suivi/tableau.html`.

| Champ | Valeur |
| --- | --- |
| Réalise | IA 2 (développement) |
| Vérifie | IA 3 (vérification), jamais un auteur de l'unité |
| Piste | 5.A Réception éditeur et essai : S24 → S26 (unité 1 sur 2) |
| Commence après | S18, S20 (cochées dans `SUIVI.md`) |
| Indépendante de | S21, S22, S23, S25, S33 |
| Branche | `tache/S24-T14-reception` |
| Fiche de conception | `docs/construction/etape-5.md`, section T14 |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Cette unité est la 1re de la piste 5.A « Réception éditeur et essai », dont les unités se font à la suite. Les autres pistes de la section (5.B) avancent en même temps, chacune de son côté. Elle attend S18, S20, hors de la piste. S26 l'attendra. Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- `editor/session_controller.gd` en logique pure : protocole de session côté éditeur, « fin inconnue », messages du moteur ignorés, lots validés puis rangés dans l'Event Store ; temps fourni de l'extérieur.
- `editor/debugger_bridge.gd`, passerelle mince ; `plugin.gd` : enregistrement et retrait de la passerelle seulement.
- `tests/unit/test_session_controller.gd` (rejoue chaque session enregistrée) et `tools/ci/checks.d/50-bridge.sh`.

## Fichiers autorisés

`addons/godot_dev_mapper/editor/debugger_bridge.gd`, `addons/godot_dev_mapper/editor/session_controller.gd`, `addons/godot_dev_mapper/plugin.gd` (enregistrement de la passerelle uniquement), `tests/unit/test_session_controller.gd`, `tools/ci/checks.d/50-bridge.sh`.

Toujours autorisés en plus : `rapports/S24*.md` et les cases de cette fiche (par `cocher`).

## Prompt de réalisation

```text
Tu réalises l'unité S24 « T14 Réception côté éditeur » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.
Réalisation prévue : IA 2 (développement) ; vérification : IA 3 (vérification). Ton numéro d'IA est celui que te donne le prompt de créneau : tu le passes à --ia, et il signe chaque case que tu coches.

AVANT TOUT, depuis ton clone principal du dépôt
1. Lis REGLES_AGENTS.md s'il existe, puis cette fiche : suivi/S24-T14-reception.md.
2. python3 suivi/outil.py prendre S24 --ia <n>
   - « PRISE » ou « REPRISE » : tu es sur la branche tache/S24-T14-reception ; commence à la sous-étape affichée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
   - « REFUSÉ » : l'unité n'est pas pour toi maintenant (déjà prise par une autre IA, S18, S20 non cochées, autre IA prévue) : reviens au prompt de créneau et choisis autre chose.

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
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status. Tu ne pousses jamais avec --force.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.
- Une décision réservée à l'humain (docs/construction/sequence.md §5) : arrêt obligatoire, rien d'autre : python3 suivi/outil.py arreter --ia <n> --unite S24 --raison "<raison>", puis fin du créneau.

TRACE OBLIGATOIRE, après CHAQUE sous-étape et avant la suivante
1. git add <les fichiers de la sous-étape> (jamais git add -A).
2. python3 suivi/outil.py cocher S24 <sous-étape> --ia <n>
   La commande vérifie l'ordre des cases et ton identité, coche la case dans suivi/S24-T14-reception.md, la signe (IA, date, heure UTC), commite et pousse sur tache/S24-T14-reception.
3. Une sous-étape faite mais non cochée par cette commande est considérée comme non faite : l'IA suivante la refera. Tu ne coches jamais une case à la main.
4. Tu ne modifies jamais SUIVI.md : il ne change qu'à la fusion, sous le verrou de main. Plusieurs IA le lisent en même temps ; aucune ne l'écrit hors de ce verrou.
5. Avant de cocher la dernière sous-étape R : « Statut : TERMINÉ » dans rapports/S24.md, puis git add.
6. Poussée refusée et non rattrapée par la commande : ne force jamais ; git pull --rebase origin tache/S24-T14-reception, puis relance la commande.

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

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche ; après chacune, git add puis python3 suivi/outil.py cocher S24 R<k> --ia <n>.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Chaque sous-étape faite est cochée par `cocher`. Complète rapports/S24.md (sorties, « Passation » en cinq lignes au plus), git add, git commit, git push origin HEAD:tache/S24-T14-reception.
- git status ne montre aucune modification non commitée ; rien ne reste non poussé.

FORMAT DE rapports/S24.md (créé par prendre ; tu le complètes)
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

Après chaque sous-étape : `git add` de ses fichiers, puis `python3 suivi/outil.py cocher S24 R<k> --ia <n>` (coche, signe, commite, pousse).

- [ ] R0 Prise en charge : `python3 suivi/outil.py prendre S24 --ia <n>` (prérequis cochés dans `SUIVI.md` : S18, S20 ; branche `tache/S24-T14-reception` créée ou reprise ; `rapports/S24.md` au statut EN COURS) ⟶ cochée par `prendre`
- [ ] R1 Écrire `editor/session_controller.gd`. ⟶ cocher S24 R1
- [ ] R2 Écrire `editor/debugger_bridge.gd`. ⟶ cocher S24 R2
- [ ] R3 Modifier `plugin.gd` : enregistrement et retrait de la passerelle. ⟶ cocher S24 R3
- [ ] R4 Écrire `tests/unit/test_session_controller.gd`. ⟶ cocher S24 R4
- [ ] R5 Écrire `tools/ci/checks.d/50-bridge.sh`. ⟶ cocher S24 R5
- [ ] R6 Écrire dans le rapport la procédure de l'essai dans l'éditeur, que S26 exécutera sous écran virtuel. ⟶ cocher S24 R6
- [ ] R7 Contrôles finaux : T14-a, T14-b, T14-c, T14-d exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » dans le rapport ⟶ cocher S24 R7

## Prompt de vérification

```text
Tu vérifies l'unité S24 « T14 Réception côté éditeur » du projet GODOT_DEV_MAPPER. Vérification prévue : IA 3 (vérification). Ton numéro d'IA est celui du prompt de créneau. Tu n'es jamais un auteur de l'unité : la commande de prise le contrôle.

PRISE, depuis ton clone principal
python3 suivi/outil.py prendre S24 --ia <n> --verification
- « VÉRIFICATION PRISE » : copie neuve ../verif-S24-T14-reception créée sur origin/tache/S24-T14-reception, verdict EN COURS écrit, V1 cochée. cd ../verif-S24-T14-reception : toute la vérification se fait dans ce dossier.
- « REFUSÉ » : une autre IA vérifie déjà, tu es auteur, ou l'unité n'est pas terminée : reviens au prompt de créneau.
- Créneau fini avant le verdict : au créneau suivant, etat te propose la même commande ; elle recrée la copie (« VÉRIFICATION REPRISE ») et tu reprends à la première case V ouverte.
GODOT : même procédure que le prompt de réalisation.
Tu ne modifies aucun fichier de l'unité. Tu écris seulement ton verdict et tes cases V.

TRACE OBLIGATOIRE : après chaque sous-étape V, git add du fichier de verdict, puis python3 suivi/outil.py cocher S24 <V…> --ia <n>. Pour la dernière : --verdict ACCEPTÉE ou --verdict REFUSÉE, identique à la ligne « Verdict » du fichier. Une sous-étape non cochée par cette commande est considérée comme non faite.

1. TRAÇABILITÉ. Chaque case R cochée est signée « — IA n · date » et a son commit sur la branche (git log --oneline origin/main..HEAD). Case cochée sans travail prouvé dans le rapport : refus.
2. PÉRIMÈTRE. git diff --name-only origin/main...HEAD. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S24*.md et suivi/S24-T14-reception.md. Tout autre fichier : refus.
3. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : T14-a, T14-b, T14-c, T14-d.
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
6. COHÉRENCE. C-03 (façade débogueur), C-04, C-06, C-07 ; section 01b de SPIKE-01.

VERDICT dans rapports/S24-verif-<tentative>.md (créé par la prise) :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte

SI ACCEPTÉE — FUSION, depuis ton clone principal (cd hors de ../verif-S24-T14-reception)
1. python3 suivi/outil.py fusionner S24 --ia <n>
   Elle trouve Godot (--godot, $GODOT, cache du bloc GODOT ou tools/ci/fetch_godot.sh ; sans Godot : REFUSÉ, verdict inchangé), prend le verrou de main (et attend s'il est pris), revérifie l'unité, fusionne dans ../fusion-S24-T14-reception, lance run_all_checks.sh, coche la ligne dans SUIVI.md et la case F1. Si les contrôles échouent : verdict passé à REFUSÉE, main inchangée, verrou rendu ; arrête-toi sur cette unité. La fusion te revient parce que tu as signé le verdict ; une autre IA ne la fait qu'après 12 h.
2. cd ../fusion-S24-T14-reception ; fais les sous-étapes F suivantes de la fiche, et coche chacune : python3 suivi/outil.py cocher S24 F<k> --ia <n> (commit local, sans poussée).
3. python3 suivi/outil.py publier S24 --ia <n> : dernière case cochée, verifier relancé, main poussée, branche supprimée, verrou rendu.
SI REFUSÉE : arrête-toi sur cette unité ; son auteur la reprendra avec prendre.
```

## Sous-étapes de vérification

Dans `../verif-S24-T14-reception`, après chaque sous-étape : `git add` du verdict, puis `python3 suivi/outil.py cocher S24 V<k> --ia <n>`.

- [ ] V1 Prise en charge : `python3 suivi/outil.py prendre S24 --ia <n> --verification` (pas un auteur ; copie neuve `../verif-S24-T14-reception` sur `origin/tache/S24-T14-reception` ; verdict EN COURS) ⟶ cochée par `prendre`
- [ ] V2 Traçabilité : chaque case R cochée porte une signature « — IA n · date » et un commit sur la branche (`git log --oneline origin/main..HEAD`) ⟶ cocher S24 V2
- [ ] V3 Périmètre : `git diff --name-only origin/main...HEAD` ⊂ fichiers autorisés. ⟶ cocher S24 V3
- [ ] V4.1 Contrôle T14-a relancé, résultat conforme. ⟶ cocher S24 V4.1
- [ ] V4.2 Contrôle T14-b relancé, résultat conforme. ⟶ cocher S24 V4.2
- [ ] V4.3 Contrôle T14-c relancé, résultat conforme. ⟶ cocher S24 V4.3
- [ ] V4.4 Contrôle T14-d relancé, résultat conforme. ⟶ cocher S24 V4.4
- [ ] V5 Contre-épreuves (CE) appliquées et détectées, puis annulées. ⟶ cocher S24 V5
- [ ] V6 Contournements cherchés. ⟶ cocher S24 V6
- [ ] V7 Cohérence avec les contrats et les invariants. ⟶ cocher S24 V7
- [ ] V8 Verdict écrit dans `rapports/S24-verif-<tentative>.md` ⟶ cocher S24 V8 --verdict ACCEPTÉE ou --verdict REFUSÉE

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

F1 et la dernière se cochent par `fusionner` et `publier` ; les autres, dans `../fusion-S24-T14-reception`, par `python3 suivi/outil.py cocher S24 F<k> --ia <n>` (commit local).

- [ ] F1 Fusion, depuis le clone principal : `python3 suivi/outil.py fusionner S24 --ia <n>` : Godot trouvé seul (--godot, $GODOT, cache du bloc GODOT ou fetch_godot.sh), verrou de `main`, fusion `--no-ff` dans `../fusion-S24-T14-reception`, `tools/ci/run_all_checks.sh` sur `main` → ALL_CHECKS OK s'il existe (sinon fusion annulée et verdict passé à REFUSÉE), ligne **S24** cochée dans `SUIVI.md` ⟶ cochée par `fusionner`
- [ ] F2 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette ⟶ cocher S24 F2
- [ ] F3 Publication : `python3 suivi/outil.py publier S24 --ia <n>` (verifier OK, `main` poussée, branche `tache/S24-T14-reception` supprimée, verrou rendu) ⟶ cochée par `publier`

## Pour la recette

Rien de propre à cette unité.
