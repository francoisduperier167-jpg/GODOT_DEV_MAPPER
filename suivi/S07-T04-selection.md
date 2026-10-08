# S07 — T04 Sélection du banc d'essai

> Fiche d'exécution du mode autonome. Chaque case se coche avec `python3 suivi/outil.py cocher S07 <sous-étape> --ia <n>`, juste après la sous-étape : la commande vérifie l'ordre et l'identité de l'IA, signe la case (IA, date, heure UTC), commite et pousse. Une sous-étape non cochée par cette commande est considérée comme non faite. Règles : `docs/construction/sequence.md`. Avancement : `SUIVI.md` et `suivi/tableau.html`.

| Champ | Valeur |
| --- | --- |
| Réalise | IA 3 (vérification) |
| Vérifie | IA 1 (conception), jamais un auteur de l'unité |
| Piste | 1.B Banc d'essai : choix et copie : S07 → S08 (unité 1 sur 2) |
| Commence après | S01 (cochée dans `SUIVI.md`) |
| Indépendante de | S02, S03, S04, S05, S06, S10, S11 |
| Branche | `tache/S07-T04-selection` |
| Fiche de conception | `docs/construction/etape-1.md`, section T04 |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Cette unité est la 1re de la piste 1.B « Banc d'essai : choix et copie », dont les unités se font à la suite. Les autres pistes de la section (1.A) avancent en même temps, chacune de son côté. Elle attend S01, hors de la piste. S08 l'attendra. Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Trouver au plus trois jeux candidats qui remplissent tous les critères de D-02.
- Pour chacun, vérifier dans son dépôt, à une révision épinglée (SHA de 40 caractères) : licence du code et licence des assets (fichiers qui le disent), version de Godot d'origine (`project.godot`), nombre de scripts `.gd`, scripts qui contiennent les décisions ciblées, risques de migration.
- Écarter tout candidat dont une licence est incertaine ou ne permet pas de redistribuer une copie modifiée : le banc vivra dans des branches de ce dépôt.
- Écrire `docs/benches/selection.md` : tableau comparatif avec liens épinglés, recommandation, deux faiblesses principales.

## Fichiers autorisés

`docs/benches/selection.md`. À la fusion seulement, par l'IA qui fusionne : la ligne D-02 de `docs/DECISIONS.md`.

Toujours autorisés en plus : `rapports/S07*.md` et les cases de cette fiche (par `cocher`).

## Contrôles propres à cette fiche

- `S07-a` : `test -s docs/benches/selection.md; echo $?` → 0
- `S07-b` : `grep -Eo "[0-9a-f]{40}" docs/benches/selection.md | sort -u | wc -l` → au moins le nombre de candidats
- `S07-c` : `grep -i "licen" docs/benches/selection.md | grep -ci "non vérifié"` → 0
- (CE) Remplacer une licence par « non vérifié » dans le fichier : S07-c donne au moins 1 ; annuler.

## Prompt de réalisation

```text
Tu réalises l'unité S07 « T04 Sélection du banc d'essai » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.
Réalisation prévue : IA 3 (vérification) ; vérification : IA 1 (conception). Ton numéro d'IA est celui que te donne le prompt de créneau : tu le passes à --ia, et il signe chaque case que tu coches.

AVANT TOUT, depuis ton clone principal du dépôt
1. Lis REGLES_AGENTS.md s'il existe, puis cette fiche : suivi/S07-T04-selection.md.
2. python3 suivi/outil.py prendre S07 --ia <n>
   - « PRISE » ou « REPRISE » : tu es sur la branche tache/S07-T04-selection ; commence à la sous-étape affichée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
   - « REFUSÉ » : l'unité n'est pas pour toi maintenant (déjà prise par une autre IA, S01 non cochée, autre IA prévue) : reviens au prompt de créneau et choisis autre chose.

GODOT
- Si tools/ci/fetch_godot.sh existe : B=$(tools/ci/fetch_godot.sh 4.7.2-stable)
- Sinon, hors du dépôt :
  D=$HOME/.cache/gdm-godot/4.7.2-stable ; mkdir -p "$D"
  test -x "$D/Godot_v4.7.2-stable_linux.x86_64" || { curl -sSL -o /tmp/godot-4.7.2.zip https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip && unzip -o -q /tmp/godot-4.7.2.zip -d "$D"; }
  B=$D/Godot_v4.7.2-stable_linux.x86_64
- « godot » dans les commandes désigne "$B". Contrôle : "$B" --version contient 4.7.2.stable.
- Éditeur avec rendu, quand la fiche le demande : xvfb-run -a -s "-screen 0 1600x900x24" "$B" --editor --path <projet> --rendering-driver opengl3

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S07.md et les cases de suivi/S07-T04-selection.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status. Tu ne pousses jamais avec --force.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.
- Une décision réservée à l'humain (docs/construction/sequence.md §5) : arrêt obligatoire, rien d'autre : python3 suivi/outil.py arreter --ia <n> --unite S07 --raison "<raison>", puis fin du créneau.

TRACE OBLIGATOIRE, après CHAQUE sous-étape et avant la suivante
1. git add <les fichiers de la sous-étape> (jamais git add -A).
2. python3 suivi/outil.py cocher S07 <sous-étape> --ia <n>
   La commande vérifie l'ordre des cases et ton identité, coche la case dans suivi/S07-T04-selection.md, la signe (IA, date, heure UTC), commite et pousse sur tache/S07-T04-selection.
3. Une sous-étape faite mais non cochée par cette commande est considérée comme non faite : l'IA suivante la refera. Tu ne coches jamais une case à la main.
4. Tu ne modifies jamais SUIVI.md : il ne change qu'à la fusion, sous le verrou de main. Plusieurs IA le lisent en même temps ; aucune ne l'écrit hors de ce verrou.
5. Avant de cocher la dernière sous-étape R : « Statut : TERMINÉ » dans rapports/S07.md, puis git add.
6. Poussée refusée et non rattrapée par la commande : ne force jamais ; git pull --rebase origin tache/S07-T04-selection, puis relance la commande.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (docs/construction/etape-1.md, T04)
Tu aides à choisir le banc d'essai du projet GODOT_DEV_MAPPER. Tu ne copies aucun fichier de jeu dans le dépôt.
Critères, tous requis :
- jeu Godot 4.x en GDScript ;
- au moins deux types d'ennemis ou d'agents qui prennent une décision observable : attaquer ou poursuivre, fuir, patrouiller ;
- licence du code qui permet une copie de travail locale modifiée ;
- licence des assets connue ;
- entre 30 et 500 scripts .gd.
Pour trois candidats au plus, donne : nom, dépôt, révision, licences du code et des assets (avec le fichier qui le dit), version de Godot d'origine, nombre de scripts .gd, scripts qui contiennent les décisions ciblées, risques de migration vers 4.7.2.
Vérifie chaque fait dans le dépôt lui-même (fichier LICENSE, project.godot). Écris « non vérifié » quand tu n'as pas pu vérifier.
Rapport : un tableau comparatif, puis ta recommandation et ses deux principales faiblesses.
TRAVAIL TECHNIQUE — fin de la copie exacte du guide

CONTRÔLES DE LA FICHE
S07-a  test -s docs/benches/selection.md; echo $?   → 0
S07-b  grep -Eo "[0-9a-f]{40}" docs/benches/selection.md | sort -u | wc -l   → au moins le nombre de candidats
S07-c  grep -i "licen" docs/benches/selection.md | grep -ci "non vérifié"   → 0
(CE) Remplacer une licence par « non vérifié » dans le fichier : S07-c donne au moins 1 ; annuler.

ADAPTATIONS DU MODE AUTONOME
- « Tu choisis » (dans le guide, l'humain) : en mode autonome, IA 1 vérifie ta recommandation contre les critères et l'inscrit en D-02 à la fusion.
- Critère ajouté : les licences doivent permettre de redistribuer une copie modifiée, car le banc vivra dans des branches `banc/<nom>-*` de ce dépôt. « Non vérifié » sur une licence écarte le candidat.
- Écris le résultat dans `docs/benches/selection.md`, en plus de ta réponse.
- Les contrôles T04-a, T04-b et T04-c du guide portent sur la préparation : ils s'exécutent en S08.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche ; après chacune, git add puis python3 suivi/outil.py cocher S07 R<k> --ia <n>.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Chaque sous-étape faite est cochée par `cocher`. Complète rapports/S07.md (sorties, « Passation » en cinq lignes au plus), git add, git commit, git push origin HEAD:tache/S07-T04-selection.
- git status ne montre aucune modification non commitée ; rien ne reste non poussé.

FORMAT DE rapports/S07.md (créé par prendre ; tu le complètes)
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

Après chaque sous-étape : `git add` de ses fichiers, puis `python3 suivi/outil.py cocher S07 R<k> --ia <n>` (coche, signe, commite, pousse).

- [ ] R0 Prise en charge : `python3 suivi/outil.py prendre S07 --ia <n>` (prérequis cochés dans `SUIVI.md` : S01 ; branche `tache/S07-T04-selection` créée ou reprise ; `rapports/S07.md` au statut EN COURS) ⟶ cochée par `prendre`
- [ ] R1 Relire D-02 dans `docs/DECISIONS.md`. ⟶ cocher S07 R1
- [ ] R2 Chercher des candidats (GitHub, bibliothèque d'assets de Godot) et en retenir au plus trois. ⟶ cocher S07 R2
- [ ] R3 Vérifier chaque fait dans le dépôt du candidat, à une révision épinglée ; noter le lien exact de chaque preuve. ⟶ cocher S07 R3
- [ ] R4 Écarter les candidats aux licences incertaines ou incompatibles avec une redistribution modifiée. ⟶ cocher S07 R4
- [ ] R5 Écrire `docs/benches/selection.md`. ⟶ cocher S07 R5
- [ ] R6 Écrire la recommandation et ses deux faiblesses. ⟶ cocher S07 R6
- [ ] R7 Contrôles finaux : S07-a, S07-b, S07-c exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » dans le rapport ⟶ cocher S07 R7

## Prompt de vérification

```text
Tu vérifies l'unité S07 « T04 Sélection du banc d'essai » du projet GODOT_DEV_MAPPER. Vérification prévue : IA 1 (conception). Ton numéro d'IA est celui du prompt de créneau. Tu n'es jamais un auteur de l'unité : la commande de prise le contrôle.

PRISE, depuis ton clone principal
python3 suivi/outil.py prendre S07 --ia <n> --verification
- « VÉRIFICATION PRISE » : copie neuve ../verif-S07-T04-selection créée sur origin/tache/S07-T04-selection, verdict EN COURS écrit, V1 cochée. cd ../verif-S07-T04-selection : toute la vérification se fait dans ce dossier.
- « REFUSÉ » : une autre IA vérifie déjà, tu es auteur, ou l'unité n'est pas terminée : reviens au prompt de créneau.
- Créneau fini avant le verdict : au créneau suivant, etat te propose la même commande ; elle recrée la copie (« VÉRIFICATION REPRISE ») et tu reprends à la première case V ouverte.
GODOT : même procédure que le prompt de réalisation.
Tu ne modifies aucun fichier de l'unité. Tu écris seulement ton verdict et tes cases V.

TRACE OBLIGATOIRE : après chaque sous-étape V, git add du fichier de verdict, puis python3 suivi/outil.py cocher S07 <V…> --ia <n>. Pour la dernière : --verdict ACCEPTÉE ou --verdict REFUSÉE, identique à la ligne « Verdict » du fichier. Une sous-étape non cochée par cette commande est considérée comme non faite.

1. TRAÇABILITÉ. Chaque case R cochée est signée « — IA n · date » et a son commit sur la branche (git log --oneline origin/main..HEAD). Case cochée sans travail prouvé dans le rapport : refus.
2. PÉRIMÈTRE. git diff --name-only origin/main...HEAD. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S07*.md et suivi/S07-T04-selection.md. Tout autre fichier : refus.
3. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : S07-a, S07-b, S07-c.
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
6. COHÉRENCE. Critères de D-02 et de la fiche T04 ; règle du README du dépôt sur les licences des bancs d'essai.

VERDICT dans rapports/S07-verif-<tentative>.md (créé par la prise) :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte

SI ACCEPTÉE — FUSION, depuis ton clone principal (cd hors de ../verif-S07-T04-selection)
1. python3 suivi/outil.py fusionner S07 --ia <n>
   Elle trouve Godot (--godot, $GODOT, cache du bloc GODOT ou tools/ci/fetch_godot.sh ; sans Godot : REFUSÉ, verdict inchangé), prend le verrou de main (et attend s'il est pris), revérifie l'unité, fusionne dans ../fusion-S07-T04-selection, lance run_all_checks.sh, coche la ligne dans SUIVI.md et la case F1. Si les contrôles échouent : verdict passé à REFUSÉE, main inchangée, verrou rendu ; arrête-toi sur cette unité. La fusion te revient parce que tu as signé le verdict ; une autre IA ne la fait qu'après 12 h.
2. cd ../fusion-S07-T04-selection ; fais les sous-étapes F suivantes de la fiche, et coche chacune : python3 suivi/outil.py cocher S07 F<k> --ia <n> (commit local, sans poussée).
3. python3 suivi/outil.py publier S07 --ia <n> : dernière case cochée, verifier relancé, main poussée, branche supprimée, verrou rendu.
SI REFUSÉE : arrête-toi sur cette unité ; son auteur la reprendra avec prendre.
```

## Sous-étapes de vérification

Dans `../verif-S07-T04-selection`, après chaque sous-étape : `git add` du verdict, puis `python3 suivi/outil.py cocher S07 V<k> --ia <n>`.

- [ ] V1 Prise en charge : `python3 suivi/outil.py prendre S07 --ia <n> --verification` (pas un auteur ; copie neuve `../verif-S07-T04-selection` sur `origin/tache/S07-T04-selection` ; verdict EN COURS) ⟶ cochée par `prendre`
- [ ] V2 Traçabilité : chaque case R cochée porte une signature « — IA n · date » et un commit sur la branche (`git log --oneline origin/main..HEAD`) ⟶ cocher S07 V2
- [ ] V3 Périmètre : `git diff --name-only origin/main...HEAD` ⊂ fichiers autorisés. ⟶ cocher S07 V3
- [ ] V4.1 Contrôle S07-a relancé, résultat conforme. ⟶ cocher S07 V4.1
- [ ] V4.2 Contrôle S07-b relancé, résultat conforme. ⟶ cocher S07 V4.2
- [ ] V4.3 Contrôle S07-c relancé, résultat conforme. ⟶ cocher S07 V4.3
- [ ] V5 Contre-épreuves (CE) appliquées et détectées, puis annulées. ⟶ cocher S07 V5
- [ ] V6 Contournements cherchés. ⟶ cocher S07 V6
- [ ] V7 Cohérence avec les contrats et les invariants. ⟶ cocher S07 V7
- [ ] V8 Verdict écrit dans `rapports/S07-verif-<tentative>.md` ⟶ cocher S07 V8 --verdict ACCEPTÉE ou --verdict REFUSÉE

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

F1 et la dernière se cochent par `fusionner` et `publier` ; les autres, dans `../fusion-S07-T04-selection`, par `python3 suivi/outil.py cocher S07 F<k> --ia <n>` (commit local).

- [ ] F1 Fusion, depuis le clone principal : `python3 suivi/outil.py fusionner S07 --ia <n>` : Godot trouvé seul (--godot, $GODOT, cache du bloc GODOT ou fetch_godot.sh), verrou de `main`, fusion `--no-ff` dans `../fusion-S07-T04-selection`, `tools/ci/run_all_checks.sh` sur `main` → ALL_CHECKS OK s'il existe (sinon fusion annulée et verdict passé à REFUSÉE), ligne **S07** cochée dans `SUIVI.md` ⟶ cochée par `fusionner`
- [ ] F2 Inscrire dans `docs/DECISIONS.md`, ligne D-02 : « adoptée par défaut : <nom>, <dépôt>@<SHA> », avec la date. ⟶ cocher S07 F2
- [ ] F3 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette ⟶ cocher S07 F3
- [ ] F4 Publication : `python3 suivi/outil.py publier S07 --ia <n>` (verifier OK, `main` poussée, branche `tache/S07-T04-selection` supprimée, verrou rendu) ⟶ cochée par `publier`

## Pour la recette

- Confirmer le choix du banc d'essai (D-02).
