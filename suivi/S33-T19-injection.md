# S33 — T19 Injection de trois bugs

> Fiche d'exécution du mode autonome. Chaque case se coche avec `python3 suivi/outil.py cocher S33 <sous-étape> --ia <n>`, juste après la sous-étape : la commande vérifie l'ordre et l'identité de l'IA, signe la case (IA, date, heure UTC), commite et pousse. Une sous-étape non cochée par cette commande est considérée comme non faite. Règles : `docs/construction/sequence.md`. Avancement : `SUIVI.md` et `suivi/tableau.html`.

| Champ | Valeur |
| --- | --- |
| Réalise | IA 3 (vérification) |
| Vérifie | IA 1 (conception), jamais un auteur de l'unité |
| Piste | 7.A Bugs injectés et mesure de valeur : S33 → S34 (unité 1 sur 2) |
| Commence après | S25 (cochée dans `SUIVI.md`) |
| Indépendante de | S17, S18, S22, S23, S24, S26, S27, S28, S29, S30, S31, S32 |
| Branche | `tache/S33-T19-injection` |
| Fiche de conception | `docs/construction/etape-7.md`, section T19 |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Cette unité est la 1re de la piste 7.A « Bugs injectés et mesure de valeur », dont les unités se font à la suite. Les autres pistes de la section (aucune) avancent en même temps, chacune de son côté. Elle attend S25, hors de la piste. S34 l'attendra. Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Créer trois branches `banc/<nom>-bug-1` à `-bug-3` depuis `banc/<nom>-instrumentation`, un seul bug par branche, de difficulté comparable, sans toucher aux appels FlowTrace ni au graphe déclaré ; les pousser.
- Écrire l'enveloppe scellée dans une branche orpheline `banc/<nom>-enveloppe`, et seulement les symptômes dans `rapports/S33.md`.

## Fichiers autorisés

`rapports/S33.md` (symptômes et déclenchement seulement). Hors de `main` : les branches `banc/<nom>-bug-1` à `-bug-3` et `banc/<nom>-enveloppe`.

Toujours autorisés en plus : `rapports/S33*.md` et les cases de cette fiche (par `cocher`).

## Contrôles propres à cette fiche

- `S33-a` : `git ls-remote origin "refs/heads/banc/*-bug-*" | wc -l` → 3
- `T19-a` : Chaque branche de bug reproduit son symptôme seule, vérifié par le vérificateur → trois symptômes reproduits
- `S33-b` : `grep -cE "\.gd:[0-9]+" rapports/S33.md` → 0 (aucune cause divulguée)
- (CE) Ajouter une ligne « fichier.gd:12 » dans `rapports/S33.md` : S33-b donne 1 ; annuler.

## Prompt de réalisation

```text
Tu réalises l'unité S33 « T19 Injection de trois bugs » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.
Réalisation prévue : IA 3 (vérification) ; vérification : IA 1 (conception). Ton numéro d'IA est celui que te donne le prompt de créneau : tu le passes à --ia, et il signe chaque case que tu coches.

AVANT TOUT, depuis ton clone principal du dépôt
1. Lis REGLES_AGENTS.md s'il existe, puis cette fiche : suivi/S33-T19-injection.md.
2. python3 suivi/outil.py prendre S33 --ia <n>
   - « PRISE » ou « REPRISE » : tu es sur la branche tache/S33-T19-injection ; commence à la sous-étape affichée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
   - « REFUSÉ » : l'unité n'est pas pour toi maintenant (déjà prise par une autre IA, S25 non cochée, autre IA prévue) : reviens au prompt de créneau et choisis autre chose.

GODOT
- Si tools/ci/fetch_godot.sh existe : B=$(tools/ci/fetch_godot.sh 4.7.2-stable)
- Sinon, hors du dépôt :
  D=$HOME/.cache/gdm-godot/4.7.2-stable ; mkdir -p "$D"
  test -x "$D/Godot_v4.7.2-stable_linux.x86_64" || { curl -sSL -o /tmp/godot-4.7.2.zip https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip && unzip -o -q /tmp/godot-4.7.2.zip -d "$D"; }
  B=$D/Godot_v4.7.2-stable_linux.x86_64
- « godot » dans les commandes désigne "$B". Contrôle : "$B" --version contient 4.7.2.stable.
- Éditeur avec rendu, quand la fiche le demande : xvfb-run -a -s "-screen 0 1600x900x24" "$B" --editor --path <projet> --rendering-driver opengl3

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S33.md et les cases de suivi/S33-T19-injection.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status. Tu ne pousses jamais avec --force.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.
- Une décision réservée à l'humain (docs/construction/sequence.md §5) : arrêt obligatoire, rien d'autre.

TRACE OBLIGATOIRE, après CHAQUE sous-étape et avant la suivante
1. git add <les fichiers de la sous-étape> (jamais git add -A).
2. python3 suivi/outil.py cocher S33 <sous-étape> --ia <n>
   La commande vérifie l'ordre des cases et ton identité, coche la case dans suivi/S33-T19-injection.md, la signe (IA, date, heure UTC), commite et pousse sur tache/S33-T19-injection.
3. Une sous-étape faite mais non cochée par cette commande est considérée comme non faite : l'IA suivante la refera. Tu ne coches jamais une case à la main.
4. Tu ne modifies jamais SUIVI.md : il ne change qu'à la fusion, sous le verrou de main. Plusieurs IA le lisent en même temps ; aucune ne l'écrit hors de ce verrou.
5. Avant de cocher la dernière sous-étape R : « Statut : TERMINÉ » dans rapports/S33.md, puis git add.
6. Poussée refusée et non rattrapée par la commande : ne force jamais ; git pull --rebase origin tache/S33-T19-injection, puis relance la commande.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (docs/construction/etape-7.md, T19)
Tu prépares la mesure de valeur, exploratoire, du POC du projet GODOT_DEV_MAPPER. Tu travailles dans la copie de travail ../benches/{nom}.
Crée trois branches à partir de gdm-instrumentation : gdm-bug-1, gdm-bug-2, gdm-bug-3. Chacune contient un seul bug, et seulement celui-là.
Règles des bugs :
- chacun est visible en jeu et lié à une décision instrumentée ou à l'état d'une instance ;
- chacun a une seule cause, à un ou deux appels du symptôme : les trois doivent être de difficulté comparable ;
- natures possibles : comparaison inversée dans une décision, état non réinitialisé après réinsertion dans l'arbre, mauvaise instance ciblée. N'en reprends pas un tel quel.
Ne touche ni aux appels FlowTrace, ni à benches/{nom}/flow.json.
Écris ../benches/{nom}/ENVELOPPE_SCELLEE.md, hors des trois branches : pour chaque bug, la branche, le symptôme visible, la cause, le fichier et la ligne, la manière de le déclencher, et pourquoi sa difficulté est comparable aux deux autres.
Dans ta réponse, donne-moi seulement, pour chaque bug : la branche, le symptôme et la manière de le déclencher en jeu. Rien d'autre.
TRAVAIL TECHNIQUE — fin de la copie exacte du guide

CONTRÔLES DE LA FICHE
S33-a  git ls-remote origin "refs/heads/banc/*-bug-*" | wc -l   → 3
T19-a  Chaque branche de bug reproduit son symptôme seule, vérifié par le vérificateur   → trois symptômes reproduits
S33-b  grep -cE "\.gd:[0-9]+" rapports/S33.md   → 0 (aucune cause divulguée)
(CE) Ajouter une ligne « fichier.gd:12 » dans `rapports/S33.md` : S33-b donne 1 ; annuler.

ADAPTATIONS DU MODE AUTONOME
- Les branches `gdm-bug-N` du guide deviennent `banc/<nom>-bug-N`, poussées sur le dépôt ; l'enveloppe vit dans la branche orpheline `banc/<nom>-enveloppe`.
- Règle pour toutes les IA : celle qui réalisera S34 ne récupère pas `banc/<nom>-enveloppe` avant d'avoir fini ses trois diagnostics.
- Contrôles du guide : T19-a (chaque branche reproduit son symptôme) est vérifié ici ; T19-b, T19-c et T19-d le sont en S34.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche ; après chacune, git add puis python3 suivi/outil.py cocher S33 R<k> --ia <n>.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Chaque sous-étape faite est cochée par `cocher`. Complète rapports/S33.md (sorties, « Passation » en cinq lignes au plus), git add, git commit, git push origin HEAD:tache/S33-T19-injection.
- git status ne montre aucune modification non commitée ; rien ne reste non poussé.

FORMAT DE rapports/S33.md (créé par prendre ; tu le complètes)
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

Après chaque sous-étape : `git add` de ses fichiers, puis `python3 suivi/outil.py cocher S33 R<k> --ia <n>` (coche, signe, commite, pousse).

- [ ] R0 Prise en charge : `python3 suivi/outil.py prendre S33 --ia <n>` (prérequis cochés dans `SUIVI.md` : S25 ; branche `tache/S33-T19-injection` créée ou reprise ; `rapports/S33.md` au statut EN COURS) ⟶ cochée par `prendre`
- [ ] R1 Copie de travail de `banc/<nom>-instrumentation`. ⟶ cocher S33 R1
- [ ] R2 Créer `banc/<nom>-bug-1` avec son bug ; vérifier que le symptôme se reproduit ; pousser. ⟶ cocher S33 R2
- [ ] R3 Créer `banc/<nom>-bug-2` ; vérifier ; pousser. ⟶ cocher S33 R3
- [ ] R4 Créer `banc/<nom>-bug-3` ; vérifier ; pousser. ⟶ cocher S33 R4
- [ ] R5 Écrire `ENVELOPPE_SCELLEE.md` dans la branche orpheline `banc/<nom>-enveloppe` ; pousser. ⟶ cocher S33 R5
- [ ] R6 Écrire dans `rapports/S33.md` seulement la branche, le symptôme et le déclenchement de chaque bug. ⟶ cocher S33 R6
- [ ] R7 Contrôles finaux : S33-a, T19-a, S33-b exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » dans le rapport ⟶ cocher S33 R7

## Prompt de vérification

```text
Tu vérifies l'unité S33 « T19 Injection de trois bugs » du projet GODOT_DEV_MAPPER. Vérification prévue : IA 1 (conception). Ton numéro d'IA est celui du prompt de créneau. Tu n'es jamais un auteur de l'unité : la commande de prise le contrôle.

PRISE, depuis ton clone principal
python3 suivi/outil.py prendre S33 --ia <n> --verification
- « VÉRIFICATION PRISE » : copie neuve ../verif-S33-T19-injection créée sur origin/tache/S33-T19-injection, verdict EN COURS écrit, V1 cochée. cd ../verif-S33-T19-injection : toute la vérification se fait dans ce dossier.
- « REFUSÉ » : une autre IA vérifie déjà, tu es auteur, ou l'unité n'est pas terminée : reviens au prompt de créneau.
GODOT : même procédure que le prompt de réalisation.
Tu ne modifies aucun fichier de l'unité. Tu écris seulement ton verdict et tes cases V.

TRACE OBLIGATOIRE : après chaque sous-étape V, git add du fichier de verdict, puis python3 suivi/outil.py cocher S33 <V…> --ia <n>. Pour la dernière : --verdict ACCEPTÉE ou --verdict REFUSÉE, identique à la ligne « Verdict » du fichier. Une sous-étape non cochée par cette commande est considérée comme non faite.

1. TRAÇABILITÉ. Chaque case R cochée est signée « — IA n · date » et a son commit sur la branche (git log --oneline origin/main..HEAD). Case cochée sans travail prouvé dans le rapport : refus.
2. PÉRIMÈTRE. git diff --name-only origin/main...HEAD. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S33*.md et suivi/S33-T19-injection.md. Tout autre fichier : refus.
3. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : S33-a, T19-a, S33-b.
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
6. COHÉRENCE. Règles des bugs de la fiche T19 : une cause, difficulté comparable, natures variées.

VERDICT dans rapports/S33-verif-<tentative>.md (créé par la prise) :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte

SI ACCEPTÉE — FUSION, depuis ton clone principal
1. python3 suivi/outil.py fusionner S33 --ia <n> --godot "$B"
   Elle prend le verrou de main (et attend s'il est pris), fusionne dans ../fusion-S33-T19-injection, lance run_all_checks.sh, coche la ligne dans SUIVI.md et la case F1. Si les contrôles échouent : verdict passé à REFUSÉE, main inchangée, verrou rendu ; arrête-toi sur cette unité.
2. cd ../fusion-S33-T19-injection ; fais les sous-étapes F suivantes de la fiche, et coche chacune : python3 suivi/outil.py cocher S33 F<k> --ia <n> (commit local, sans poussée).
3. python3 suivi/outil.py publier S33 --ia <n> : dernière case cochée, verifier relancé, main poussée, branche supprimée, verrou rendu.
SI REFUSÉE : arrête-toi sur cette unité ; son auteur la reprendra avec prendre.
```

## Sous-étapes de vérification

Dans `../verif-S33-T19-injection`, après chaque sous-étape : `git add` du verdict, puis `python3 suivi/outil.py cocher S33 V<k> --ia <n>`.

- [ ] V1 Prise en charge : `python3 suivi/outil.py prendre S33 --ia <n> --verification` (pas un auteur ; copie neuve `../verif-S33-T19-injection` sur `origin/tache/S33-T19-injection` ; verdict EN COURS) ⟶ cochée par `prendre`
- [ ] V2 Traçabilité : chaque case R cochée porte une signature « — IA n · date » et un commit sur la branche (`git log --oneline origin/main..HEAD`) ⟶ cocher S33 V2
- [ ] V3 Périmètre : `git diff --name-only origin/main...HEAD` ⊂ fichiers autorisés. ⟶ cocher S33 V3
- [ ] V4.1 Contrôle S33-a relancé, résultat conforme. ⟶ cocher S33 V4.1
- [ ] V4.2 Contrôle T19-a relancé, résultat conforme. ⟶ cocher S33 V4.2
- [ ] V4.3 Contrôle S33-b relancé, résultat conforme. ⟶ cocher S33 V4.3
- [ ] V5 Contre-épreuves (CE) appliquées et détectées, puis annulées. ⟶ cocher S33 V5
- [ ] V6 Contournements cherchés. ⟶ cocher S33 V6
- [ ] V7 Cohérence avec les contrats et les invariants. ⟶ cocher S33 V7
- [ ] V8 Verdict écrit dans `rapports/S33-verif-<tentative>.md` ⟶ cocher S33 V8 --verdict ACCEPTÉE ou --verdict REFUSÉE

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

F1 et la dernière se cochent par `fusionner` et `publier` ; les autres, dans `../fusion-S33-T19-injection`, par `python3 suivi/outil.py cocher S33 F<k> --ia <n>` (commit local).

- [ ] F1 Fusion : `python3 suivi/outil.py fusionner S33 --ia <n> --godot "$B"` : verrou de `main`, fusion `--no-ff` dans `../fusion-S33-T19-injection`, `tools/ci/run_all_checks.sh` sur `main` → ALL_CHECKS OK s'il existe (sinon fusion annulée et verdict passé à REFUSÉE), ligne **S33** cochée dans `SUIVI.md` ⟶ cochée par `fusionner`
- [ ] F2 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette ⟶ cocher S33 F2
- [ ] F3 Publication : `python3 suivi/outil.py publier S33 --ia <n>` (verifier OK, `main` poussée, branche `tache/S33-T19-injection` supprimée, verrou rendu) ⟶ cochée par `publier`

## Pour la recette

Rien de propre à cette unité.
