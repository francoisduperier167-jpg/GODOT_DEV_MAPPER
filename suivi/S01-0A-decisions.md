# S01 — 0.A Dossier de décisions

> Fiche d'exécution du mode autonome. Chaque case se coche avec `python3 suivi/outil.py cocher S01 <sous-étape> --ia <n>`, juste après la sous-étape : la commande vérifie l'ordre et l'identité de l'IA, signe la case (IA, date, heure UTC), commite et pousse. Une sous-étape non cochée par cette commande est considérée comme non faite. Règles : `docs/construction/sequence.md`. Avancement : `SUIVI.md` et `suivi/tableau.html`.

| Champ | Valeur |
| --- | --- |
| Réalise | IA 1 (conception) |
| Vérifie | IA 3 (vérification), jamais un auteur de l'unité |
| Piste | 0.A Décisions et règles : S01 → S02 (unité 1 sur 2) |
| Commence après | rien : peut commencer tout de suite |
| Indépendante de | aucune |
| Branche | `tache/S01-0A-decisions` |
| Fiche de conception | `docs/construction/etape-0.md`, section 0.A |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Cette unité est la 1re de la piste 0.A « Décisions et règles », dont les unités se font à la suite. Les autres pistes de la section (aucune) avancent en même temps, chacune de son côté. S02 l'attendra. Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Créer `docs/DECISIONS.md` : une ligne d'en-tête « Statut : proposé · date », puis un tableau de D-01 à D-09.
- Colonnes : ID, question, options (deux ou trois), recommandation, conséquences de chaque option, échéance, statut, date.
- Recommandations : D-01 Godot 4.7.2 ; D-03 trois IA, deux créneaux chacune par jour ; D-05 runner maison minimal ; D-07 4.7.2 bloquant, préversion 4.8-dev7 dans un job non bloquant ; D-09 mode autonome (fiches `suivi/`, recette humaine finale).
- D-02 : critères de choix du banc d'essai (Godot 4.x en GDScript, au moins deux types d'ennemis qui décident, 30 à 500 scripts, licences du code et des assets qui permettent de redistribuer une copie modifiée). Le banc vivra dans des branches `banc/<nom>-*` de ce dépôt. Le choix se fait en S07.
- Statuts : « adoptée par défaut » pour D-01, D-03, D-05, D-07 et D-09 ; « critères adoptés par défaut, choix en S07 » pour D-02 ; « proposée » pour D-04, D-06 et D-08.

## Fichiers autorisés

`docs/DECISIONS.md`

Toujours autorisés en plus : `rapports/S01*.md` et les cases de cette fiche (par `cocher`).

## Contrôles propres à cette fiche

- `S01-a` : `for d in D-01 D-02 D-03 D-04 D-05 D-06 D-07 D-08 D-09; do c=$(grep -cE "^\| $d " docs/DECISIONS.md); [ "$c" = 1 ] || echo "$d : $c"; done` → aucune sortie
- `S01-b` : `for d in D-01 D-03 D-05 D-07 D-09; do grep -E "^\| $d " docs/DECISIONS.md | grep -q "adoptée par défaut" || echo "manque $d"; done` → aucune sortie
- `S01-c` : `grep -E "^\| D-0(4|6|8) " docs/DECISIONS.md | grep -c "proposée"` → 3
- (CE) Retirer « adoptée par défaut » de la ligne D-07, relancer S01-b : « manque D-07 » s'affiche ; annuler.

## Prompt de réalisation

```text
Tu réalises l'unité S01 « 0.A Dossier de décisions » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.
Réalisation prévue : IA 1 (conception) ; vérification : IA 3 (vérification). Ton numéro d'IA est celui que te donne le prompt de créneau : tu le passes à --ia, et il signe chaque case que tu coches.

AVANT TOUT, depuis ton clone principal du dépôt
1. Lis REGLES_AGENTS.md s'il existe, puis cette fiche : suivi/S01-0A-decisions.md.
2. python3 suivi/outil.py prendre S01 --ia <n>
   - « PRISE » ou « REPRISE » : tu es sur la branche tache/S01-0A-decisions ; commence à la sous-étape affichée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
   - « REFUSÉ » : l'unité n'est pas pour toi maintenant (déjà prise par une autre IA, autre IA prévue) : reviens au prompt de créneau et choisis autre chose.

GODOT
- Si tools/ci/fetch_godot.sh existe : B=$(tools/ci/fetch_godot.sh 4.7.2-stable)
- Sinon, hors du dépôt :
  D=$HOME/.cache/gdm-godot/4.7.2-stable ; mkdir -p "$D"
  test -x "$D/Godot_v4.7.2-stable_linux.x86_64" || { curl -sSL -o /tmp/godot-4.7.2.zip https://github.com/godotengine/godot-builds/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip && unzip -o -q /tmp/godot-4.7.2.zip -d "$D"; }
  B=$D/Godot_v4.7.2-stable_linux.x86_64
- « godot » dans les commandes désigne "$B". Contrôle : "$B" --version contient 4.7.2.stable.
- Éditeur avec rendu, quand la fiche le demande : xvfb-run -a -s "-screen 0 1600x900x24" "$B" --editor --path <projet> --rendering-driver opengl3

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S01.md et les cases de suivi/S01-0A-decisions.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status. Tu ne pousses jamais avec --force.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.
- Une décision réservée à l'humain (docs/construction/sequence.md §5) : arrêt obligatoire, rien d'autre : python3 suivi/outil.py arreter --ia <n> --unite S01 --raison "<raison>", puis fin du créneau.

TRACE OBLIGATOIRE, après CHAQUE sous-étape et avant la suivante
1. git add <les fichiers de la sous-étape> (jamais git add -A).
2. python3 suivi/outil.py cocher S01 <sous-étape> --ia <n>
   La commande vérifie l'ordre des cases et ton identité, coche la case dans suivi/S01-0A-decisions.md, la signe (IA, date, heure UTC), commite et pousse sur tache/S01-0A-decisions.
3. Une sous-étape faite mais non cochée par cette commande est considérée comme non faite : l'IA suivante la refera. Tu ne coches jamais une case à la main.
4. Tu ne modifies jamais SUIVI.md : il ne change qu'à la fusion, sous le verrou de main. Plusieurs IA le lisent en même temps ; aucune ne l'écrit hors de ce verrou.
5. Avant de cocher la dernière sous-étape R : « Statut : TERMINÉ » dans rapports/S01.md, puis git add.
6. Poussée refusée et non rattrapée par la commande : ne force jamais ; git pull --rebase origin tache/S01-0A-decisions, puis relance la commande.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (docs/construction/etape-0.md, 0.A)
Tu prépares les décisions de démarrage du projet GODOT_DEV_MAPPER. Tu ne décides rien.
Lis docs/plan-directeur.md (§0 et §10), docs/spikes/SPIKE-01.md et docs/construction/etape-0.md.
Crée docs/DECISIONS.md : un tableau avec ID, question, options (deux ou trois), recommandation, conséquences de chaque option, échéance, statut (« proposée »), date.
Couvre D-01 à D-08. Pour D-02, propose des critères de choix du banc d'essai, pas un jeu.
Avant de rendre, vérifie : chaque ID de D-01 à D-08 apparaît une seule fois ; chaque ligne a une recommandation ; aucune ligne n'est marquée « validée ».
Rapport : le chemin du fichier, puis les questions que je dois trancher, une par ligne, dans l'ordre de leur échéance.
TRAVAIL TECHNIQUE — fin de la copie exacte du guide

CONTRÔLES DE LA FICHE
S01-a  for d in D-01 D-02 D-03 D-04 D-05 D-06 D-07 D-08 D-09; do c=$(grep -cE "^\| $d " docs/DECISIONS.md); [ "$c" = 1 ] || echo "$d : $c"; done   → aucune sortie
S01-b  for d in D-01 D-03 D-05 D-07 D-09; do grep -E "^\| $d " docs/DECISIONS.md | grep -q "adoptée par défaut" || echo "manque $d"; done   → aucune sortie
S01-c  grep -E "^\| D-0(4|6|8) " docs/DECISIONS.md | grep -c "proposée"   → 3
(CE) Retirer « adoptée par défaut » de la ligne D-07, relancer S01-b : « manque D-07 » s'affiche ; annuler.

ADAPTATIONS DU MODE AUTONOME
- Le prompt du guide dit « Tu ne décides rien » et laisse toutes les lignes « proposée ». En mode autonome, tu inscris ensuite les statuts de la fiche : « adoptée par défaut » n'est pas « validée », la confirmation se fait à la recette.
- Ajoute D-09, absente du prompt du guide : mode d'exécution autonome, fiches `suivi/`, recette humaine finale.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche ; après chacune, git add puis python3 suivi/outil.py cocher S01 R<k> --ia <n>.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Chaque sous-étape faite est cochée par `cocher`. Complète rapports/S01.md (sorties, « Passation » en cinq lignes au plus), git add, git commit, git push origin HEAD:tache/S01-0A-decisions.
- git status ne montre aucune modification non commitée ; rien ne reste non poussé.

FORMAT DE rapports/S01.md (créé par prendre ; tu le complètes)
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

Après chaque sous-étape : `git add` de ses fichiers, puis `python3 suivi/outil.py cocher S01 R<k> --ia <n>` (coche, signe, commite, pousse).

- [ ] R0 Prise en charge : `python3 suivi/outil.py prendre S01 --ia <n>` (aucun prérequis ; branche `tache/S01-0A-decisions` créée ou reprise ; `rapports/S01.md` au statut EN COURS) ⟶ cochée par `prendre`
- [ ] R1 Lire `docs/plan-directeur.md` (§0 et §10), `docs/spikes/SPIKE-01.md`, `docs/construction/etape-0.md` (0.A) et `docs/construction/sequence.md`. ⟶ cocher S01 R1
- [ ] R2 Écrire `docs/DECISIONS.md` : en-tête de statut, puis le tableau D-01 à D-09 avec toutes ses colonnes. ⟶ cocher S01 R2
- [ ] R3 Appliquer les statuts de la section « Ce qu'il faut faire ». ⟶ cocher S01 R3
- [ ] R4 Écrire dans le rapport la liste « Pour la recette » : chaque décision adoptée par défaut, une par ligne. ⟶ cocher S01 R4
- [ ] R5 Contrôles finaux : S01-a, S01-b, S01-c exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » dans le rapport ⟶ cocher S01 R5

## Prompt de vérification

```text
Tu vérifies l'unité S01 « 0.A Dossier de décisions » du projet GODOT_DEV_MAPPER. Vérification prévue : IA 3 (vérification). Ton numéro d'IA est celui du prompt de créneau. Tu n'es jamais un auteur de l'unité : la commande de prise le contrôle.

PRISE, depuis ton clone principal
python3 suivi/outil.py prendre S01 --ia <n> --verification
- « VÉRIFICATION PRISE » : copie neuve ../verif-S01-0A-decisions créée sur origin/tache/S01-0A-decisions, verdict EN COURS écrit, V1 cochée. cd ../verif-S01-0A-decisions : toute la vérification se fait dans ce dossier.
- « REFUSÉ » : une autre IA vérifie déjà, tu es auteur, ou l'unité n'est pas terminée : reviens au prompt de créneau.
- Créneau fini avant le verdict : au créneau suivant, etat te propose la même commande ; elle recrée la copie (« VÉRIFICATION REPRISE ») et tu reprends à la première case V ouverte.
GODOT : même procédure que le prompt de réalisation.
Tu ne modifies aucun fichier de l'unité. Tu écris seulement ton verdict et tes cases V.

TRACE OBLIGATOIRE : après chaque sous-étape V, git add du fichier de verdict, puis python3 suivi/outil.py cocher S01 <V…> --ia <n>. Pour la dernière : --verdict ACCEPTÉE ou --verdict REFUSÉE, identique à la ligne « Verdict » du fichier. Une sous-étape non cochée par cette commande est considérée comme non faite.

1. TRAÇABILITÉ. Chaque case R cochée est signée « — IA n · date » et a son commit sur la branche (git log --oneline origin/main..HEAD). Case cochée sans travail prouvé dans le rapport : refus.
2. PÉRIMÈTRE. git diff --name-only origin/main...HEAD. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S01*.md et suivi/S01-0A-decisions.md. Tout autre fichier : refus.
3. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : S01-a, S01-b, S01-c.
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
6. COHÉRENCE. Les recommandations reprennent le plan §0 et §10 et `docs/construction/etape-0.md` ; D-09 reprend `docs/construction/sequence.md`.

VERDICT dans rapports/S01-verif-<tentative>.md (créé par la prise) :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte

SI ACCEPTÉE — FUSION, depuis ton clone principal (cd hors de ../verif-S01-0A-decisions)
1. python3 suivi/outil.py fusionner S01 --ia <n>
   Elle trouve Godot (--godot, $GODOT, cache du bloc GODOT ou tools/ci/fetch_godot.sh ; sans Godot : REFUSÉ, verdict inchangé), prend le verrou de main (et attend s'il est pris), revérifie l'unité, fusionne dans ../fusion-S01-0A-decisions, lance run_all_checks.sh, coche la ligne dans SUIVI.md et la case F1. Si les contrôles échouent : verdict passé à REFUSÉE, main inchangée, verrou rendu ; arrête-toi sur cette unité. La fusion te revient parce que tu as signé le verdict ; une autre IA ne la fait qu'après 12 h.
2. cd ../fusion-S01-0A-decisions ; fais les sous-étapes F suivantes de la fiche, et coche chacune : python3 suivi/outil.py cocher S01 F<k> --ia <n> (commit local, sans poussée).
3. python3 suivi/outil.py publier S01 --ia <n> : dernière case cochée, verifier relancé, main poussée, branche supprimée, verrou rendu.
SI REFUSÉE : arrête-toi sur cette unité ; son auteur la reprendra avec prendre.
```

## Sous-étapes de vérification

Dans `../verif-S01-0A-decisions`, après chaque sous-étape : `git add` du verdict, puis `python3 suivi/outil.py cocher S01 V<k> --ia <n>`.

- [ ] V1 Prise en charge : `python3 suivi/outil.py prendre S01 --ia <n> --verification` (pas un auteur ; copie neuve `../verif-S01-0A-decisions` sur `origin/tache/S01-0A-decisions` ; verdict EN COURS) ⟶ cochée par `prendre`
- [ ] V2 Traçabilité : chaque case R cochée porte une signature « — IA n · date » et un commit sur la branche (`git log --oneline origin/main..HEAD`) ⟶ cocher S01 V2
- [ ] V3 Périmètre : `git diff --name-only origin/main...HEAD` ⊂ fichiers autorisés. ⟶ cocher S01 V3
- [ ] V4.1 Contrôle S01-a relancé, résultat conforme. ⟶ cocher S01 V4.1
- [ ] V4.2 Contrôle S01-b relancé, résultat conforme. ⟶ cocher S01 V4.2
- [ ] V4.3 Contrôle S01-c relancé, résultat conforme. ⟶ cocher S01 V4.3
- [ ] V5 Contre-épreuves (CE) appliquées et détectées, puis annulées. ⟶ cocher S01 V5
- [ ] V6 Contournements cherchés. ⟶ cocher S01 V6
- [ ] V7 Cohérence avec les contrats et les invariants. ⟶ cocher S01 V7
- [ ] V8 Verdict écrit dans `rapports/S01-verif-<tentative>.md` ⟶ cocher S01 V8 --verdict ACCEPTÉE ou --verdict REFUSÉE

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

F1 et la dernière se cochent par `fusionner` et `publier` ; les autres, dans `../fusion-S01-0A-decisions`, par `python3 suivi/outil.py cocher S01 F<k> --ia <n>` (commit local).

- [ ] F1 Fusion, depuis le clone principal : `python3 suivi/outil.py fusionner S01 --ia <n>` : Godot trouvé seul (--godot, $GODOT, cache du bloc GODOT ou fetch_godot.sh), verrou de `main`, fusion `--no-ff` dans `../fusion-S01-0A-decisions`, `tools/ci/run_all_checks.sh` sur `main` → ALL_CHECKS OK s'il existe (sinon fusion annulée et verdict passé à REFUSÉE), ligne **S01** cochée dans `SUIVI.md` ⟶ cochée par `fusionner`
- [ ] F2 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette ⟶ cocher S01 F2
- [ ] F3 Publication : `python3 suivi/outil.py publier S01 --ia <n>` (verifier OK, `main` poussée, branche `tache/S01-0A-decisions` supprimée, verrou rendu) ⟶ cochée par `publier`

## Pour la recette

- Confirmer ou changer chaque décision « adoptée par défaut ».
