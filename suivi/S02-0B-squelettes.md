# S02 — 0.B Squelettes et règles des agents

> Fiche d'exécution du mode autonome. Chaque case se coche avec `python3 suivi/outil.py cocher S02 <sous-étape> --ia <n>`, juste après la sous-étape : la commande vérifie l'ordre et l'identité de l'IA, signe la case (IA, date, heure UTC), commite et pousse. Une sous-étape non cochée par cette commande est considérée comme non faite. Règles : `docs/construction/sequence.md`. Avancement : `SUIVI.md` et `suivi/tableau.html`.

| Champ | Valeur |
| --- | --- |
| Réalise | IA 1 (conception) |
| Vérifie | IA 3 (vérification), jamais un auteur de l'unité |
| Piste | 0.A Décisions et règles : S01 → S02 (unité 2 sur 2) |
| Commence après | S01 (cochée dans `SUIVI.md`) |
| Indépendante de | S07 |
| Branche | `tache/S02-0B-squelettes` |
| Fiche de conception | `docs/construction/etape-0.md`, section 0.B |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Cette unité est la 2e de la piste 0.A « Décisions et règles », dont les unités se font à la suite. Les autres pistes de la section (aucune) avancent en même temps, chacune de son côté. Elle attend S01, l'unité précédente de la piste. Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Créer `docs/SPEC.md`, `docs/ARCHITECTURE.md` (avec la liste des API sensibles), `docs/CONTRACTS.md` (sept sections C-01 à C-07, sept rubriques chacune, contenu « à rédiger en T07 » ou « en T08 »), `docs/COMPATIBILITY.md`, `docs/TEST_PLAN.md`. Chacun commence par « Statut : proposé · date ».
- Créer `PROJECT_STATE.md` : mis à jour seulement à la fusion ; sections Mesures, Dette, Versions de Godot testées, Liste de recette (reprise du §7 de `sequence.md`). L'avancement des unités est dans `SUIVI.md` : ne pas le recopier.
- Créer `REGLES_AGENTS.md`, 150 lignes au plus : règles non négociables, trace obligatoire et accès simultané (commandes `etat`, `prendre`, `cocher`, `fusionner`, `publier`, verrou de `main`), format de rapport, INV-01 à INV-09 en une ligne chacun, commandes de contrôle vérifiées, renvoi à `sequence.md` et à `SUIVI.md`.
- Créer `tools/sync_rules.sh` : copie `REGLES_AGENTS.md` vers chaque fichier de contexte de la liste écrite en tête du script (par défaut `AGENTS.md` ; l'humain y ajoute le fichier que lit chacune de ses IA) ; avec `--check`, compare sans écrire et sort en 1 si une copie diffère.

## Fichiers autorisés

`docs/SPEC.md`, `docs/ARCHITECTURE.md`, `docs/CONTRACTS.md`, `docs/COMPATIBILITY.md`, `docs/TEST_PLAN.md`, `PROJECT_STATE.md`, `REGLES_AGENTS.md`, `AGENTS.md` et les autres fichiers de contexte listés en tête de `tools/sync_rules.sh`, `tools/sync_rules.sh`.

Toujours autorisés en plus : `rapports/S02*.md` et les cases de cette fiche (par `cocher`).

## Contrôles propres à cette fiche

- `S02-a` : `for f in docs/SPEC.md docs/ARCHITECTURE.md docs/CONTRACTS.md docs/COMPATIBILITY.md docs/TEST_PLAN.md PROJECT_STATE.md REGLES_AGENTS.md; do test -s "$f" || echo "manque $f"; done` → aucune sortie
- `S02-b` : `grep -L "^Statut" docs/SPEC.md docs/ARCHITECTURE.md docs/CONTRACTS.md docs/COMPATIBILITY.md docs/TEST_PLAN.md` → aucune sortie
- `S02-c` : `tools/sync_rules.sh && tools/sync_rules.sh --check; echo $?` → 0
- `S02-d` : `wc -l < REGLES_AGENTS.md` → 150 au plus
- `S02-e` : `for c in C-01 C-02 C-03 C-04 C-05 C-06 C-07; do grep -c "^## $c" docs/CONTRACTS.md; done` → 1 pour chacun
- `S02-f` : `grep -c "SUIVI.md" REGLES_AGENTS.md PROJECT_STATE.md` → au moins 1 dans chaque fichier
- (CE) `echo x >> AGENTS.md; tools/sync_rules.sh --check; echo $?` → 1, puis `tools/sync_rules.sh` pour rétablir.

## Prompt de réalisation

```text
Tu réalises l'unité S02 « 0.B Squelettes et règles des agents » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.
Réalisation prévue : IA 1 (conception) ; vérification : IA 3 (vérification). Ton numéro d'IA est celui que te donne le prompt de créneau : tu le passes à --ia, et il signe chaque case que tu coches.

AVANT TOUT, depuis ton clone principal du dépôt
1. Lis REGLES_AGENTS.md s'il existe, puis cette fiche : suivi/S02-0B-squelettes.md.
2. python3 suivi/outil.py prendre S02 --ia <n>
   - « PRISE » ou « REPRISE » : tu es sur la branche tache/S02-0B-squelettes ; commence à la sous-étape affichée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
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
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S02.md et les cases de suivi/S02-0B-squelettes.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status. Tu ne pousses jamais avec --force.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.
- Une décision réservée à l'humain (docs/construction/sequence.md §5) : arrêt obligatoire, rien d'autre.

TRACE OBLIGATOIRE, après CHAQUE sous-étape et avant la suivante
1. git add <les fichiers de la sous-étape> (jamais git add -A).
2. python3 suivi/outil.py cocher S02 <sous-étape> --ia <n>
   La commande vérifie l'ordre des cases et ton identité, coche la case dans suivi/S02-0B-squelettes.md, la signe (IA, date, heure UTC), commite et pousse sur tache/S02-0B-squelettes.
3. Une sous-étape faite mais non cochée par cette commande est considérée comme non faite : l'IA suivante la refera. Tu ne coches jamais une case à la main.
4. Tu ne modifies jamais SUIVI.md : il ne change qu'à la fusion, sous le verrou de main. Plusieurs IA le lisent en même temps ; aucune ne l'écrit hors de ce verrou.
5. Avant de cocher la dernière sous-étape R : « Statut : TERMINÉ » dans rapports/S02.md, puis git add.
6. Poussée refusée et non rattrapée par la commande : ne force jamais ; git pull --rebase origin tache/S02-0B-squelettes, puis relance la commande.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (docs/construction/etape-0.md, 0.B)
Tu crées les squelettes de documents du projet GODOT_DEV_MAPPER. Tu n'écris aucun code du plugin.
Sources : docs/plan-directeur.md, docs/methodologie.md, docs/DECISIONS.md, docs/construction/README.md.

À CRÉER
- docs/SPEC.md : vision, scénarios et capacités, extraits des §1 à 3 du plan ; renvoie au plan pour le détail.
- docs/ARCHITECTURE.md : modules, dépendances autorisées et interdites, frontière de compatibilité, liste des API sensibles (plan §4).
- docs/CONTRACTS.md : une section par contrat C-01 à C-07, avec sept rubriques : objet, format ou API, exemples valides, exemples invalides, comportement en erreur, version, tests de contrat. Contenu : « à rédiger en T07 » ou « à rédiger en T08 ».
- docs/COMPATIBILITY.md : fenêtre de support issue de D-01 et D-07.
- docs/TEST_PLAN.md : types de tests, commandes de contrôle vérifiées (reprises du guide), principe des contre-épreuves.
- PROJECT_STATE.md : tableau des tâches T00 à T20, T13 découpée en T13a, T13b et T13c, au statut « À faire », avec en tête la mention « mis à jour seulement à l'étape de fusion » ; budget de chaque étape ; mesures à tenir (heures humaines, temps agent, capacités acceptées, réussite par IA).
- REGLES_AGENTS.md : 150 lignes au plus. Il contient les règles non négociables et le format de rapport du prompt universel de réalisation, les invariants INV-01 à INV-09 en une ligne chacun, et les commandes de contrôle.
- tools/sync_rules.sh : copie REGLES_AGENTS.md vers chaque fichier de contexte de la liste écrite en tête du script (par défaut AGENTS.md seul ; on y ajoute le fichier que lit chaque IA utilisée). Avec --check, il compare sans rien écrire et renvoie 1 si une copie diffère.

RÈGLES
Chaque document normatif commence par « Statut : proposé · 8 octobre 2026 » (ou la date du jour). Une définition n'existe qu'à un seul endroit ; ailleurs, on y renvoie.

CONTRÔLES (exécute-les et colle les sorties)
1. for f in docs/SPEC.md docs/ARCHITECTURE.md docs/CONTRACTS.md docs/COMPATIBILITY.md docs/TEST_PLAN.md PROJECT_STATE.md REGLES_AGENTS.md; do test -s "$f" || echo "manque $f"; done   → aucune sortie
2. grep -L "^Statut" docs/SPEC.md docs/ARCHITECTURE.md docs/CONTRACTS.md docs/COMPATIBILITY.md docs/TEST_PLAN.md   → aucune sortie
3. tools/sync_rules.sh && tools/sync_rules.sh --check; echo $?   → 0
4. (CE) echo x >> AGENTS.md; tools/sync_rules.sh --check; echo $?   → 1, puis tools/sync_rules.sh pour rétablir
5. wc -l < REGLES_AGENTS.md   → 150 au plus
6. for c in C-01 C-02 C-03 C-04 C-05 C-06 C-07; do grep -c "^## $c" docs/CONTRACTS.md; done   → 1 pour chacun

Rapport au format du prompt universel de réalisation.
TRAVAIL TECHNIQUE — fin de la copie exacte du guide

CONTRÔLES DE LA FICHE
S02-a  for f in docs/SPEC.md docs/ARCHITECTURE.md docs/CONTRACTS.md docs/COMPATIBILITY.md docs/TEST_PLAN.md PROJECT_STATE.md REGLES_AGENTS.md; do test -s "$f" || echo "manque $f"; done   → aucune sortie
S02-b  grep -L "^Statut" docs/SPEC.md docs/ARCHITECTURE.md docs/CONTRACTS.md docs/COMPATIBILITY.md docs/TEST_PLAN.md   → aucune sortie
S02-c  tools/sync_rules.sh && tools/sync_rules.sh --check; echo $?   → 0
S02-d  wc -l < REGLES_AGENTS.md   → 150 au plus
S02-e  for c in C-01 C-02 C-03 C-04 C-05 C-06 C-07; do grep -c "^## $c" docs/CONTRACTS.md; done   → 1 pour chacun
S02-f  grep -c "SUIVI.md" REGLES_AGENTS.md PROJECT_STATE.md   → au moins 1 dans chaque fichier
(CE) `echo x >> AGENTS.md; tools/sync_rules.sh --check; echo $?` → 1, puis `tools/sync_rules.sh` pour rétablir.

ADAPTATIONS DU MODE AUTONOME
- `PROJECT_STATE.md` ne contient pas le tableau des tâches T00 à T20 demandé par le guide : l'avancement vit dans `SUIVI.md`. Il contient les mesures, la dette, les versions testées et la liste de recette.
- `REGLES_AGENTS.md` ajoute les règles de trace et d'accès simultané de `docs/construction/sequence.md` §3 : une case se coche seulement par `python3 suivi/outil.py cocher`, juste après la sous-étape ; une unité se prend par `prendre` ; `SUIVI.md` ne change que sous le verrou de `main` ; jamais de `--force` ; reprise à la première case non cochée.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche ; après chacune, git add puis python3 suivi/outil.py cocher S02 R<k> --ia <n>.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Chaque sous-étape faite est cochée par `cocher`. Complète rapports/S02.md (sorties, « Passation » en cinq lignes au plus), git add, git commit, git push origin HEAD:tache/S02-0B-squelettes.
- git status ne montre aucune modification non commitée ; rien ne reste non poussé.

FORMAT DE rapports/S02.md (créé par prendre ; tu le complètes)
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

Après chaque sous-étape : `git add` de ses fichiers, puis `python3 suivi/outil.py cocher S02 R<k> --ia <n>` (coche, signe, commite, pousse).

- [ ] R0 Prise en charge : `python3 suivi/outil.py prendre S02 --ia <n>` (prérequis cochés dans `SUIVI.md` : S01 ; branche `tache/S02-0B-squelettes` créée ou reprise ; `rapports/S02.md` au statut EN COURS) ⟶ cochée par `prendre`
- [ ] R1 Lire le plan, la méthode, `docs/DECISIONS.md`, `docs/construction/README.md` et `docs/construction/sequence.md`. ⟶ cocher S02 R1
- [ ] R2 Créer les cinq documents normatifs, chacun avec sa ligne de statut. ⟶ cocher S02 R2
- [ ] R3 Créer `PROJECT_STATE.md` selon la fiche (pas de tableau des tâches : il renvoie à `SUIVI.md`). ⟶ cocher S02 R3
- [ ] R4 Créer `REGLES_AGENTS.md` (150 lignes au plus) avec les règles de cochage des fiches `suivi/`. ⟶ cocher S02 R4
- [ ] R5 Créer `tools/sync_rules.sh` (liste des copies en tête, `AGENTS.md` par défaut), le rendre exécutable, l'exécuter pour produire `AGENTS.md`. ⟶ cocher S02 R5
- [ ] R6 Contrôles finaux : S02-a, S02-b, S02-c, S02-d, S02-e, S02-f exécutés dans une copie propre, sorties collées dans le rapport ; `tools/ci/run_all_checks.sh` s'il existe → ALL_CHECKS OK ; « Statut : TERMINÉ » dans le rapport ⟶ cocher S02 R6

## Prompt de vérification

```text
Tu vérifies l'unité S02 « 0.B Squelettes et règles des agents » du projet GODOT_DEV_MAPPER. Vérification prévue : IA 3 (vérification). Ton numéro d'IA est celui du prompt de créneau. Tu n'es jamais un auteur de l'unité : la commande de prise le contrôle.

PRISE, depuis ton clone principal
python3 suivi/outil.py prendre S02 --ia <n> --verification
- « VÉRIFICATION PRISE » : copie neuve ../verif-S02-0B-squelettes créée sur origin/tache/S02-0B-squelettes, verdict EN COURS écrit, V1 cochée. cd ../verif-S02-0B-squelettes : toute la vérification se fait dans ce dossier.
- « REFUSÉ » : une autre IA vérifie déjà, tu es auteur, ou l'unité n'est pas terminée : reviens au prompt de créneau.
GODOT : même procédure que le prompt de réalisation.
Tu ne modifies aucun fichier de l'unité. Tu écris seulement ton verdict et tes cases V.

TRACE OBLIGATOIRE : après chaque sous-étape V, git add du fichier de verdict, puis python3 suivi/outil.py cocher S02 <V…> --ia <n>. Pour la dernière : --verdict ACCEPTÉE ou --verdict REFUSÉE, identique à la ligne « Verdict » du fichier. Une sous-étape non cochée par cette commande est considérée comme non faite.

1. TRAÇABILITÉ. Chaque case R cochée est signée « — IA n · date » et a son commit sur la branche (git log --oneline origin/main..HEAD). Case cochée sans travail prouvé dans le rapport : refus.
2. PÉRIMÈTRE. git diff --name-only origin/main...HEAD. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S02*.md et suivi/S02-0B-squelettes.md. Tout autre fichier : refus.
3. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : S02-a, S02-b, S02-c, S02-d, S02-e, S02-f.
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
6. COHÉRENCE. Aucune définition à deux endroits ; chaque règle du plan présente et non déformée ; INV-01 à INV-09 complets ; commandes identiques à celles du guide ; décisions de `docs/DECISIONS.md` reprises (prompt de relecture du guide, ci-dessous).
RELECTURE CROISÉE, prompt du guide :
Relis les squelettes créés à l'étape 0 du projet GODOT_DEV_MAPPER : docs/SPEC.md, docs/ARCHITECTURE.md, docs/CONTRACTS.md, docs/COMPATIBILITY.md, docs/TEST_PLAN.md, PROJECT_STATE.md, REGLES_AGENTS.md. Compare-les à docs/plan-directeur.md.
Cherche : une définition présente à deux endroits ; une règle du plan déformée ou absente ; un invariant manquant ; une commande de contrôle différente de celle du guide ; une décision de docs/DECISIONS.md non reprise.
Ne modifie rien. Rapport : liste numérotée avec fichier, passage, écart, correction proposée ; « aucun écart » sinon.

VERDICT dans rapports/S02-verif-<tentative>.md (créé par la prise) :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte

SI ACCEPTÉE — FUSION, depuis ton clone principal
1. python3 suivi/outil.py fusionner S02 --ia <n> --godot "$B"
   Elle prend le verrou de main (et attend s'il est pris), fusionne dans ../fusion-S02-0B-squelettes, lance run_all_checks.sh, coche la ligne dans SUIVI.md et la case F1. Si les contrôles échouent : verdict passé à REFUSÉE, main inchangée, verrou rendu ; arrête-toi sur cette unité.
2. cd ../fusion-S02-0B-squelettes ; fais les sous-étapes F suivantes de la fiche, et coche chacune : python3 suivi/outil.py cocher S02 F<k> --ia <n> (commit local, sans poussée).
3. python3 suivi/outil.py publier S02 --ia <n> : dernière case cochée, verifier relancé, main poussée, branche supprimée, verrou rendu.
SI REFUSÉE : arrête-toi sur cette unité ; son auteur la reprendra avec prendre.
```

## Sous-étapes de vérification

Dans `../verif-S02-0B-squelettes`, après chaque sous-étape : `git add` du verdict, puis `python3 suivi/outil.py cocher S02 V<k> --ia <n>`.

- [ ] V1 Prise en charge : `python3 suivi/outil.py prendre S02 --ia <n> --verification` (pas un auteur ; copie neuve `../verif-S02-0B-squelettes` sur `origin/tache/S02-0B-squelettes` ; verdict EN COURS) ⟶ cochée par `prendre`
- [ ] V2 Traçabilité : chaque case R cochée porte une signature « — IA n · date » et un commit sur la branche (`git log --oneline origin/main..HEAD`) ⟶ cocher S02 V2
- [ ] V3 Périmètre : `git diff --name-only origin/main...HEAD` ⊂ fichiers autorisés. ⟶ cocher S02 V3
- [ ] V4.1 Contrôle S02-a relancé, résultat conforme. ⟶ cocher S02 V4.1
- [ ] V4.2 Contrôle S02-b relancé, résultat conforme. ⟶ cocher S02 V4.2
- [ ] V4.3 Contrôle S02-c relancé, résultat conforme. ⟶ cocher S02 V4.3
- [ ] V4.4 Contrôle S02-d relancé, résultat conforme. ⟶ cocher S02 V4.4
- [ ] V4.5 Contrôle S02-e relancé, résultat conforme. ⟶ cocher S02 V4.5
- [ ] V4.6 Contrôle S02-f relancé, résultat conforme. ⟶ cocher S02 V4.6
- [ ] V5 Contre-épreuves (CE) appliquées et détectées, puis annulées. ⟶ cocher S02 V5
- [ ] V6 Contournements cherchés. ⟶ cocher S02 V6
- [ ] V7 Cohérence avec les contrats et les invariants. ⟶ cocher S02 V7
- [ ] V8 Verdict écrit dans `rapports/S02-verif-<tentative>.md` ⟶ cocher S02 V8 --verdict ACCEPTÉE ou --verdict REFUSÉE

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

F1 et la dernière se cochent par `fusionner` et `publier` ; les autres, dans `../fusion-S02-0B-squelettes`, par `python3 suivi/outil.py cocher S02 F<k> --ia <n>` (commit local).

- [ ] F1 Fusion : `python3 suivi/outil.py fusionner S02 --ia <n> --godot "$B"` : verrou de `main`, fusion `--no-ff` dans `../fusion-S02-0B-squelettes`, `tools/ci/run_all_checks.sh` sur `main` → ALL_CHECKS OK s'il existe (sinon fusion annulée et verdict passé à REFUSÉE), ligne **S02** cochée dans `SUIVI.md` ⟶ cochée par `fusionner`
- [ ] F2 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette ⟶ cocher S02 F2
- [ ] F3 Publication : `python3 suivi/outil.py publier S02 --ia <n>` (verifier OK, `main` poussée, branche `tache/S02-0B-squelettes` supprimée, verrou rendu) ⟶ cochée par `publier`

## Pour la recette

Rien de propre à cette unité.
