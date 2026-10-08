# S08 — T04 Préparation du banc d'essai

> Fiche d'exécution du mode autonome. Chaque case se coche avec `python3 suivi/outil.py cocher S08 <sous-étape> --ia <n>`, juste après la sous-étape : la commande vérifie l'ordre et l'identité de l'IA, signe la case (IA, date, heure UTC), commite et pousse. Une sous-étape non cochée par cette commande est considérée comme non faite. Règles : `docs/construction/sequence.md`. Avancement : `SUIVI.md` et `suivi/tableau.html`.

| Champ | Valeur |
| --- | --- |
| Réalise | IA 2 (développement) |
| Vérifie | IA 3 (vérification), jamais un auteur de l'unité |
| Piste | 1.B Banc d'essai : choix et copie : S07 → S08 (unité 2 sur 2) |
| Commence après | S04, S07 (cochées dans `SUIVI.md`) |
| Indépendante de | S05, S06, S10, S11 |
| Branche | `tache/S08-T04-preparation` |
| Fiche de conception | `docs/construction/etape-1.md`, section T04 |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Cette unité est la 2e de la piste 1.B « Banc d'essai : choix et copie », dont les unités se font à la suite. Les autres pistes de la section (1.A) avancent en même temps, chacune de son côté. Elle attend S07, l'unité précédente de la piste. Elle attend aussi S04, hors de la piste. Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Copier le jeu retenu, à sa révision épinglée, dans une branche orpheline `banc/<nom>-base` de ce dépôt (licences et fichiers LICENSE intacts), puis la pousser.
- L'importer avec Godot 4.7.2 et corriger seulement ce que la migration exige, une correction par commit, la raison dans le message.
- Sur la branche de la tâche : `benches/benches.json`, `tools/check_benches.py`, `docs/benches/<nom>.md`.

## Fichiers autorisés

Sur `tache/S08-T04-preparation` : `benches/benches.json`, `docs/benches/<nom>.md`, `tools/check_benches.py`. Hors de `main` : la branche orpheline `banc/<nom>-base`.

Toujours autorisés en plus : `rapports/S08*.md` et les cases de cette fiche (par `cocher`).

## Prompt de réalisation

```text
Tu réalises l'unité S08 « T04 Préparation du banc d'essai » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.
Réalisation prévue : IA 2 (développement) ; vérification : IA 3 (vérification). Ton numéro d'IA est celui que te donne le prompt de créneau : tu le passes à --ia, et il signe chaque case que tu coches.

AVANT TOUT, depuis ton clone principal du dépôt
1. Lis REGLES_AGENTS.md s'il existe, puis cette fiche : suivi/S08-T04-preparation.md.
2. python3 suivi/outil.py prendre S08 --ia <n>
   - « PRISE » ou « REPRISE » : tu es sur la branche tache/S08-T04-preparation ; commence à la sous-étape affichée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
   - « REFUSÉ » : l'unité n'est pas pour toi maintenant (déjà prise par une autre IA, S04, S07 non cochées, autre IA prévue) : reviens au prompt de créneau et choisis autre chose.

GODOT
- Si tools/ci/fetch_godot.sh existe : B=$(tools/ci/fetch_godot.sh 4.7.2-stable)
- Sinon, hors du dépôt :
  D=$HOME/.cache/gdm-godot/4.7.2-stable ; mkdir -p "$D"
  test -x "$D/Godot_v4.7.2-stable_linux.x86_64" || { curl -sSL -o /tmp/godot-4.7.2.zip https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip && unzip -o -q /tmp/godot-4.7.2.zip -d "$D"; }
  B=$D/Godot_v4.7.2-stable_linux.x86_64
- « godot » dans les commandes désigne "$B". Contrôle : "$B" --version contient 4.7.2.stable.
- Éditeur avec rendu, quand la fiche le demande : xvfb-run -a -s "-screen 0 1600x900x24" "$B" --editor --path <projet> --rendering-driver opengl3

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S08.md et les cases de suivi/S08-T04-preparation.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status. Tu ne pousses jamais avec --force.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.
- Une décision réservée à l'humain (docs/construction/sequence.md §5) : arrêt obligatoire, rien d'autre : python3 suivi/outil.py arreter --ia <n> --unite S08 --raison "<raison>", puis fin du créneau.

TRACE OBLIGATOIRE, après CHAQUE sous-étape et avant la suivante
1. git add <les fichiers de la sous-étape> (jamais git add -A).
2. python3 suivi/outil.py cocher S08 <sous-étape> --ia <n>
   La commande vérifie l'ordre des cases et ton identité, coche la case dans suivi/S08-T04-preparation.md, la signe (IA, date, heure UTC), commite et pousse sur tache/S08-T04-preparation.
3. Une sous-étape faite mais non cochée par cette commande est considérée comme non faite : l'IA suivante la refera. Tu ne coches jamais une case à la main.
4. Tu ne modifies jamais SUIVI.md : il ne change qu'à la fusion, sous le verrou de main. Plusieurs IA le lisent en même temps ; aucune ne l'écrit hors de ce verrou.
5. Avant de cocher la dernière sous-étape R : « Statut : TERMINÉ » dans rapports/S08.md, puis git add.
6. Poussée refusée et non rattrapée par la commande : ne force jamais ; git pull --rebase origin tache/S08-T04-preparation, puis relance la commande.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (docs/construction/etape-1.md, T04)
Tu prépares le banc d'essai retenu pour le projet GODOT_DEV_MAPPER : {nom}, dépôt {url}, révision {sha}.
1. Clone-le hors du dépôt, dans ../benches/{nom}, puis crée la branche gdm-base.
2. Importe-le avec Godot 4.7.2 : godot --headless --path ../benches/{nom} --import > /tmp/bench.out 2>&1
   Corrige seulement ce que la migration exige. Chaque correction fait un commit séparé, avec la raison dans le message.
3. Écris benches/benches.json : nom, dépôt, révision d'origine, révision migrée, licences du code et des assets, version de Godot d'origine, scripts des décisions ciblées.
4. Écris tools/check_benches.py : il vérifie que benches.json est un JSON valide avec ces clés, et qu'aucun fichier .gd ni aucun asset du jeu n'est suivi par Git dans ce dépôt.
5. Écris docs/benches/{nom}.md : la fiche du jeu, les décisions observables, les corrections de migration.
CONTRÔLES
T04-a  python3 tools/check_benches.py ; echo $?                                          → 0
T04-b  grep -cE "^(ERROR|SCRIPT ERROR)" /tmp/bench.out après la migration                 → 0, ou erreurs listées et justifiées dans la fiche
T04-c  (CE) copie temporairement un .gd du jeu dans benches/ et ajoute-le à Git : T04-a → 1 ; annule
TRAVAIL TECHNIQUE — fin de la copie exacte du guide

ADAPTATIONS DU MODE AUTONOME
- Le guide clone le jeu hors du dépôt, branche `gdm-base`. En mode autonome, chaque IA arrive dans un environnement neuf : la copie vit dans la branche orpheline `banc/<nom>-base` de ce dépôt, jamais sur `main`. Pour la retrouver : `git fetch origin banc/<nom>-base && git worktree add ../benches/<nom> origin/banc/<nom>-base`.
- Partout où le guide écrit `../benches/{nom}` ou `gdm-base`, lire la copie de travail de `banc/<nom>-base`.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche ; après chacune, git add puis python3 suivi/outil.py cocher S08 R<k> --ia <n>.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Chaque sous-étape faite est cochée par `cocher`. Complète rapports/S08.md (sorties, « Passation » en cinq lignes au plus), git add, git commit, git push origin HEAD:tache/S08-T04-preparation.
- git status ne montre aucune modification non commitée ; rien ne reste non poussé.

FORMAT DE rapports/S08.md (créé par prendre ; tu le complètes)
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

Après chaque sous-étape : `git add` de ses fichiers, puis `python3 suivi/outil.py cocher S08 R<k> --ia <n>` (coche, signe, commite, pousse).

- [ ] R0 Prise en charge : `python3 suivi/outil.py prendre S08 --ia <n>` (prérequis cochés dans `SUIVI.md` : S04, S07 ; branche `tache/S08-T04-preparation` créée ou reprise ; `rapports/S08.md` au statut EN COURS) ⟶ cochée par `prendre`
- [ ] R1 Relire D-02 et `docs/benches/selection.md` ; noter le nom court `<nom>`. ⟶ cocher S08 R1
- [ ] R2 Obtenir Godot 4.7.2. ⟶ cocher S08 R2
- [ ] R3 Créer la copie de travail du banc : `git worktree add --detach ../benches/<nom>`, puis dans ce dossier `git checkout --orphan banc/<nom>-base && git rm -rfq .` ; y copier le jeu à la révision épinglée (sans son `.git`) ; commit « Copie de <dépôt>@<SHA> » ; `git push origin banc/<nom>-base`. ⟶ cocher S08 R3
- [ ] R4 Importer : `godot --headless --path ../benches/<nom> --import > /tmp/bench.out 2>&1` ; corriger la migration, un commit par correction ; pousser `banc/<nom>-base`. ⟶ cocher S08 R4
- [ ] R5 Écrire `benches/benches.json` : nom, dépôt, révision d'origine, branche `banc/<nom>-base`, révision migrée, licences, version de Godot d'origine, scripts des décisions ciblées. ⟶ cocher S08 R5
- [ ] R6 Écrire `tools/check_benches.py` (JSON valide avec ces clés ; aucun fichier du jeu suivi par Git sur la branche courante hors de `banc/*`). ⟶ cocher S08 R6
- [ ] R7 Écrire `docs/benches/<nom>.md` : fiche du jeu, décisions observables, corrections de migration. ⟶ cocher S08 R7
- [ ] R8 Faire la contre-épreuve T04-c, puis l'annuler. ⟶ cocher S08 R8
- [ ] R9 Contrôles finaux : T04-a, T04-b, T04-c exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » dans le rapport ⟶ cocher S08 R9

## Prompt de vérification

```text
Tu vérifies l'unité S08 « T04 Préparation du banc d'essai » du projet GODOT_DEV_MAPPER. Vérification prévue : IA 3 (vérification). Ton numéro d'IA est celui du prompt de créneau. Tu n'es jamais un auteur de l'unité : la commande de prise le contrôle.

PRISE, depuis ton clone principal
python3 suivi/outil.py prendre S08 --ia <n> --verification
- « VÉRIFICATION PRISE » : copie neuve ../verif-S08-T04-preparation créée sur origin/tache/S08-T04-preparation, verdict EN COURS écrit, V1 cochée. cd ../verif-S08-T04-preparation : toute la vérification se fait dans ce dossier.
- « REFUSÉ » : une autre IA vérifie déjà, tu es auteur, ou l'unité n'est pas terminée : reviens au prompt de créneau.
- Créneau fini avant le verdict : au créneau suivant, etat te propose la même commande ; elle recrée la copie (« VÉRIFICATION REPRISE ») et tu reprends à la première case V ouverte.
GODOT : même procédure que le prompt de réalisation.
Tu ne modifies aucun fichier de l'unité. Tu écris seulement ton verdict et tes cases V.

TRACE OBLIGATOIRE : après chaque sous-étape V, git add du fichier de verdict, puis python3 suivi/outil.py cocher S08 <V…> --ia <n>. Pour la dernière : --verdict ACCEPTÉE ou --verdict REFUSÉE, identique à la ligne « Verdict » du fichier. Une sous-étape non cochée par cette commande est considérée comme non faite.

1. TRAÇABILITÉ. Chaque case R cochée est signée « — IA n · date » et a son commit sur la branche (git log --oneline origin/main..HEAD). Case cochée sans travail prouvé dans le rapport : refus.
2. PÉRIMÈTRE. git diff --name-only origin/main...HEAD. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S08*.md et suivi/S08-T04-preparation.md. Tout autre fichier : refus.
3. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : T04-a, T04-b, T04-c.
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
6. COHÉRENCE. Aucun fichier du jeu sur `main` ; licences reprises de `docs/benches/selection.md`.

VERDICT dans rapports/S08-verif-<tentative>.md (créé par la prise) :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte

SI ACCEPTÉE — FUSION, depuis ton clone principal (cd hors de ../verif-S08-T04-preparation)
1. python3 suivi/outil.py fusionner S08 --ia <n>
   Elle trouve Godot (--godot, $GODOT, cache du bloc GODOT ou tools/ci/fetch_godot.sh ; sans Godot : REFUSÉ, verdict inchangé), prend le verrou de main (et attend s'il est pris), revérifie l'unité, fusionne dans ../fusion-S08-T04-preparation, lance run_all_checks.sh, coche la ligne dans SUIVI.md et la case F1. Si les contrôles échouent : verdict passé à REFUSÉE, main inchangée, verrou rendu ; arrête-toi sur cette unité. La fusion te revient parce que tu as signé le verdict ; une autre IA ne la fait qu'après 12 h.
2. cd ../fusion-S08-T04-preparation ; fais les sous-étapes F suivantes de la fiche, et coche chacune : python3 suivi/outil.py cocher S08 F<k> --ia <n> (commit local, sans poussée).
3. python3 suivi/outil.py publier S08 --ia <n> : dernière case cochée, verifier relancé, main poussée, branche supprimée, verrou rendu.
SI REFUSÉE : arrête-toi sur cette unité ; son auteur la reprendra avec prendre.
```

## Sous-étapes de vérification

Dans `../verif-S08-T04-preparation`, après chaque sous-étape : `git add` du verdict, puis `python3 suivi/outil.py cocher S08 V<k> --ia <n>`.

- [ ] V1 Prise en charge : `python3 suivi/outil.py prendre S08 --ia <n> --verification` (pas un auteur ; copie neuve `../verif-S08-T04-preparation` sur `origin/tache/S08-T04-preparation` ; verdict EN COURS) ⟶ cochée par `prendre`
- [ ] V2 Traçabilité : chaque case R cochée porte une signature « — IA n · date » et un commit sur la branche (`git log --oneline origin/main..HEAD`) ⟶ cocher S08 V2
- [ ] V3 Périmètre : `git diff --name-only origin/main...HEAD` ⊂ fichiers autorisés. ⟶ cocher S08 V3
- [ ] V4.1 Contrôle T04-a relancé, résultat conforme. ⟶ cocher S08 V4.1
- [ ] V4.2 Contrôle T04-b relancé, résultat conforme. ⟶ cocher S08 V4.2
- [ ] V4.3 Contrôle T04-c relancé, résultat conforme. ⟶ cocher S08 V4.3
- [ ] V5 Contre-épreuves (CE) appliquées et détectées, puis annulées. ⟶ cocher S08 V5
- [ ] V6 Contournements cherchés. ⟶ cocher S08 V6
- [ ] V7 Cohérence avec les contrats et les invariants. ⟶ cocher S08 V7
- [ ] V8 Verdict écrit dans `rapports/S08-verif-<tentative>.md` ⟶ cocher S08 V8 --verdict ACCEPTÉE ou --verdict REFUSÉE

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

F1 et la dernière se cochent par `fusionner` et `publier` ; les autres, dans `../fusion-S08-T04-preparation`, par `python3 suivi/outil.py cocher S08 F<k> --ia <n>` (commit local).

- [ ] F1 Fusion, depuis le clone principal : `python3 suivi/outil.py fusionner S08 --ia <n>` : Godot trouvé seul (--godot, $GODOT, cache du bloc GODOT ou fetch_godot.sh), verrou de `main`, fusion `--no-ff` dans `../fusion-S08-T04-preparation`, `tools/ci/run_all_checks.sh` sur `main` → ALL_CHECKS OK s'il existe (sinon fusion annulée et verdict passé à REFUSÉE), ligne **S08** cochée dans `SUIVI.md` ⟶ cochée par `fusionner`
- [ ] F2 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette ⟶ cocher S08 F2
- [ ] F3 Publication : `python3 suivi/outil.py publier S08 --ia <n>` (verifier OK, `main` poussée, branche `tache/S08-T04-preparation` supprimée, verrou rendu) ⟶ cochée par `publier`

## Pour la recette

Rien de propre à cette unité.
