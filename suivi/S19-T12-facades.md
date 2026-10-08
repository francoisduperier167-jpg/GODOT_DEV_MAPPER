# S19 — T12 Façades de compatibilité et profil moteur

> Fiche d'exécution du mode autonome. Chaque case se coche avec `python3 suivi/outil.py cocher S19 <sous-étape> --ia <n>`, juste après la sous-étape : la commande vérifie l'ordre et l'identité de l'IA, signe la case (IA, date, heure UTC), commite et pousse. Une sous-étape non cochée par cette commande est considérée comme non faite. Règles : `docs/construction/sequence.md`. Avancement : `SUIVI.md` et `suivi/tableau.html`.

| Champ | Valeur |
| --- | --- |
| Réalise | IA 2 (développement) |
| Vérifie | IA 1 (conception), jamais un auteur de l'unité |
| Piste | 4.B Façades, FlowTrace et mesures : S19 → S20 → S21 → S22 (unité 1 sur 4) |
| Commence après | S15 (cochée dans `SUIVI.md`) |
| Indépendante de | S16, S17, S18 |
| Branche | `tache/S19-T12-facades` |
| Fiche de conception | `docs/construction/etape-4.md`, section T12 |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Cette unité est la 1re de la piste 4.B « Façades, FlowTrace et mesures », dont les unités se font à la suite. Les autres pistes de la section (4.A) avancent en même temps, chacune de son côté. Elle attend S15, hors de la piste. S20 l'attendra. Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Côté éditeur : façades débogueur et éditeur, profil moteur selon les règles de SPIKE-02.
- Côté runtime : `runtime_facade.gd`, avec un transport de substitution pour les tests, sans référence au plugin éditeur.
- Les API sensibles n'apparaissent que dans ces fichiers.

## Fichiers autorisés

`addons/godot_dev_mapper/compat/engine_facade.gd` et `engine_profile.gd`, `addons/godot_dev_mapper_runtime/runtime_facade.gd`, les marqueurs T12 de `tests/pending/` (suppression seulement).

Toujours autorisés en plus : `rapports/S19*.md` et les cases de cette fiche (par `cocher`).

## Prompt de réalisation

```text
Tu réalises l'unité S19 « T12 Façades de compatibilité et profil moteur » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.
Réalisation prévue : IA 2 (développement) ; vérification : IA 1 (conception). Ton numéro d'IA est celui que te donne le prompt de créneau : tu le passes à --ia, et il signe chaque case que tu coches.

AVANT TOUT, depuis ton clone principal du dépôt
1. Lis REGLES_AGENTS.md s'il existe, puis cette fiche : suivi/S19-T12-facades.md.
2. python3 suivi/outil.py prendre S19 --ia <n>
   - « PRISE » ou « REPRISE » : tu es sur la branche tache/S19-T12-facades ; commence à la sous-étape affichée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
   - « REFUSÉ » : l'unité n'est pas pour toi maintenant (déjà prise par une autre IA, S15 non cochée, autre IA prévue) : reviens au prompt de créneau et choisis autre chose.

GODOT
- Si tools/ci/fetch_godot.sh existe : B=$(tools/ci/fetch_godot.sh 4.7.2-stable)
- Sinon, hors du dépôt :
  D=$HOME/.cache/gdm-godot/4.7.2-stable ; mkdir -p "$D"
  test -x "$D/Godot_v4.7.2-stable_linux.x86_64" || { curl -sSL -o /tmp/godot-4.7.2.zip https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip && unzip -o -q /tmp/godot-4.7.2.zip -d "$D"; }
  B=$D/Godot_v4.7.2-stable_linux.x86_64
- « godot » dans les commandes désigne "$B". Contrôle : "$B" --version contient 4.7.2.stable.
- Éditeur avec rendu, quand la fiche le demande : xvfb-run -a -s "-screen 0 1600x900x24" "$B" --editor --path <projet> --rendering-driver opengl3

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S19.md et les cases de suivi/S19-T12-facades.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status. Tu ne pousses jamais avec --force.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.
- Une décision réservée à l'humain (docs/construction/sequence.md §5) : arrêt obligatoire, rien d'autre.

TRACE OBLIGATOIRE, après CHAQUE sous-étape et avant la suivante
1. git add <les fichiers de la sous-étape> (jamais git add -A).
2. python3 suivi/outil.py cocher S19 <sous-étape> --ia <n>
   La commande vérifie l'ordre des cases et ton identité, coche la case dans suivi/S19-T12-facades.md, la signe (IA, date, heure UTC), commite et pousse sur tache/S19-T12-facades.
3. Une sous-étape faite mais non cochée par cette commande est considérée comme non faite : l'IA suivante la refera. Tu ne coches jamais une case à la main.
4. Tu ne modifies jamais SUIVI.md : il ne change qu'à la fusion, sous le verrou de main. Plusieurs IA le lisent en même temps ; aucune ne l'écrit hors de ce verrou.
5. Avant de cocher la dernière sous-étape R : « Statut : TERMINÉ » dans rapports/S19.md, puis git add.
6. Poussée refusée et non rattrapée par la commande : ne force jamais ; git pull --rebase origin tache/S19-T12-facades, puis relance la commande.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (docs/construction/etape-4.md, T12)
Tu réalises la tâche T12 du projet GODOT_DEV_MAPPER. Applique les règles et le format de rapport du prompt universel de réalisation.
CONTEXTE : docs/CONTRACTS.md, section C-03 ; docs/spikes/SPIKE-02.md (détection de capacités, isolation) ; docs/ARCHITECTURE.md (API sensibles) ; tests/contract/test_c03_facades.gd.
OBJECTIF
- Côté éditeur : les façades débogueur et éditeur, et le profil moteur (version affichée, capacités détectées selon les règles de SPIKE-02).
- Côté runtime : la façade du dossier autonome. Elle accepte un transport de substitution pour les tests et ne référence jamais le plugin éditeur.
- Les API sensibles n'apparaissent que dans ces fichiers.
DÉROULÉ : supprime les marqueurs T12 de tests/pending/, montre l'échec, puis implémente.
CONTRÔLES
T12-a  runner → 0 sur 4.7.2, aucun marqueur T12 restant
T12-b  python3 tools/check_deps.py ; echo $?   → 0
T12-c  Même runner avec le binaire de la préversion → résultat collé dans le rapport, sans exigence
T12-d  godot --headless --path . --check-only -s res://addons/godot_dev_mapper_runtime/runtime_facade.gd   → 0
CONTRE-ÉPREUVE (CE) pour le vérificateur : ajouter un appel à EngineDebugger dans store/ → check_deps échoue.
TRAVAIL TECHNIQUE — fin de la copie exacte du guide

ADAPTATIONS DU MODE AUTONOME
- Aucune : suis le travail technique tel quel.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche ; après chacune, git add puis python3 suivi/outil.py cocher S19 R<k> --ia <n>.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Chaque sous-étape faite est cochée par `cocher`. Complète rapports/S19.md (sorties, « Passation » en cinq lignes au plus), git add, git commit, git push origin HEAD:tache/S19-T12-facades.
- git status ne montre aucune modification non commitée ; rien ne reste non poussé.

FORMAT DE rapports/S19.md (créé par prendre ; tu le complètes)
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

Après chaque sous-étape : `git add` de ses fichiers, puis `python3 suivi/outil.py cocher S19 R<k> --ia <n>` (coche, signe, commite, pousse).

- [ ] R0 Prise en charge : `python3 suivi/outil.py prendre S19 --ia <n>` (prérequis cochés dans `SUIVI.md` : S15 ; branche `tache/S19-T12-facades` créée ou reprise ; `rapports/S19.md` au statut EN COURS) ⟶ cochée par `prendre`
- [ ] R1 Supprimer les marqueurs T12 ; coller l'échec. ⟶ cocher S19 R1
- [ ] R2 Implémenter `compat/engine_facade.gd`. ⟶ cocher S19 R2
- [ ] R3 Implémenter `compat/engine_profile.gd`. ⟶ cocher S19 R3
- [ ] R4 Implémenter `addons/godot_dev_mapper_runtime/runtime_facade.gd`. ⟶ cocher S19 R4
- [ ] R5 Lancer le runner avec la préversion et coller le résultat (T12-c). ⟶ cocher S19 R5
- [ ] R6 Contrôles finaux : T12-a, T12-b, T12-c, T12-d exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » dans le rapport ⟶ cocher S19 R6

## Prompt de vérification

```text
Tu vérifies l'unité S19 « T12 Façades de compatibilité et profil moteur » du projet GODOT_DEV_MAPPER. Vérification prévue : IA 1 (conception). Ton numéro d'IA est celui du prompt de créneau. Tu n'es jamais un auteur de l'unité : la commande de prise le contrôle.

PRISE, depuis ton clone principal
python3 suivi/outil.py prendre S19 --ia <n> --verification
- « VÉRIFICATION PRISE » : copie neuve ../verif-S19-T12-facades créée sur origin/tache/S19-T12-facades, verdict EN COURS écrit, V1 cochée. cd ../verif-S19-T12-facades : toute la vérification se fait dans ce dossier.
- « REFUSÉ » : une autre IA vérifie déjà, tu es auteur, ou l'unité n'est pas terminée : reviens au prompt de créneau.
GODOT : même procédure que le prompt de réalisation.
Tu ne modifies aucun fichier de l'unité. Tu écris seulement ton verdict et tes cases V.

TRACE OBLIGATOIRE : après chaque sous-étape V, git add du fichier de verdict, puis python3 suivi/outil.py cocher S19 <V…> --ia <n>. Pour la dernière : --verdict ACCEPTÉE ou --verdict REFUSÉE, identique à la ligne « Verdict » du fichier. Une sous-étape non cochée par cette commande est considérée comme non faite.

1. TRAÇABILITÉ. Chaque case R cochée est signée « — IA n · date » et a son commit sur la branche (git log --oneline origin/main..HEAD). Case cochée sans travail prouvé dans le rapport : refus.
2. PÉRIMÈTRE. git diff --name-only origin/main...HEAD. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S19*.md et suivi/S19-T12-facades.md. Tout autre fichier : refus.
3. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : T12-a, T12-b, T12-c, T12-d.
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
6. COHÉRENCE. C-03 ; INV-09 ; règles de SPIKE-02.

VERDICT dans rapports/S19-verif-<tentative>.md (créé par la prise) :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte

SI ACCEPTÉE — FUSION, depuis ton clone principal
1. python3 suivi/outil.py fusionner S19 --ia <n> --godot "$B"
   Elle prend le verrou de main (et attend s'il est pris), fusionne dans ../fusion-S19-T12-facades, lance run_all_checks.sh, coche la ligne dans SUIVI.md et la case F1. Si les contrôles échouent : verdict passé à REFUSÉE, main inchangée, verrou rendu ; arrête-toi sur cette unité.
2. cd ../fusion-S19-T12-facades ; fais les sous-étapes F suivantes de la fiche, et coche chacune : python3 suivi/outil.py cocher S19 F<k> --ia <n> (commit local, sans poussée).
3. python3 suivi/outil.py publier S19 --ia <n> : dernière case cochée, verifier relancé, main poussée, branche supprimée, verrou rendu.
SI REFUSÉE : arrête-toi sur cette unité ; son auteur la reprendra avec prendre.
```

## Sous-étapes de vérification

Dans `../verif-S19-T12-facades`, après chaque sous-étape : `git add` du verdict, puis `python3 suivi/outil.py cocher S19 V<k> --ia <n>`.

- [ ] V1 Prise en charge : `python3 suivi/outil.py prendre S19 --ia <n> --verification` (pas un auteur ; copie neuve `../verif-S19-T12-facades` sur `origin/tache/S19-T12-facades` ; verdict EN COURS) ⟶ cochée par `prendre`
- [ ] V2 Traçabilité : chaque case R cochée porte une signature « — IA n · date » et un commit sur la branche (`git log --oneline origin/main..HEAD`) ⟶ cocher S19 V2
- [ ] V3 Périmètre : `git diff --name-only origin/main...HEAD` ⊂ fichiers autorisés. ⟶ cocher S19 V3
- [ ] V4.1 Contrôle T12-a relancé, résultat conforme. ⟶ cocher S19 V4.1
- [ ] V4.2 Contrôle T12-b relancé, résultat conforme. ⟶ cocher S19 V4.2
- [ ] V4.3 Contrôle T12-c relancé, résultat conforme. ⟶ cocher S19 V4.3
- [ ] V4.4 Contrôle T12-d relancé, résultat conforme. ⟶ cocher S19 V4.4
- [ ] V5 Contre-épreuves (CE) appliquées et détectées, puis annulées. ⟶ cocher S19 V5
- [ ] V6 Contournements cherchés. ⟶ cocher S19 V6
- [ ] V7 Cohérence avec les contrats et les invariants. ⟶ cocher S19 V7
- [ ] V8 Verdict écrit dans `rapports/S19-verif-<tentative>.md` ⟶ cocher S19 V8 --verdict ACCEPTÉE ou --verdict REFUSÉE

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

F1 et la dernière se cochent par `fusionner` et `publier` ; les autres, dans `../fusion-S19-T12-facades`, par `python3 suivi/outil.py cocher S19 F<k> --ia <n>` (commit local).

- [ ] F1 Fusion : `python3 suivi/outil.py fusionner S19 --ia <n> --godot "$B"` : verrou de `main`, fusion `--no-ff` dans `../fusion-S19-T12-facades`, `tools/ci/run_all_checks.sh` sur `main` → ALL_CHECKS OK s'il existe (sinon fusion annulée et verdict passé à REFUSÉE), ligne **S19** cochée dans `SUIVI.md` ⟶ cochée par `fusionner`
- [ ] F2 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette ⟶ cocher S19 F2
- [ ] F3 Publication : `python3 suivi/outil.py publier S19 --ia <n>` (verifier OK, `main` poussée, branche `tache/S19-T12-facades` supprimée, verrou rendu) ⟶ cochée par `publier`

## Pour la recette

Rien de propre à cette unité.
