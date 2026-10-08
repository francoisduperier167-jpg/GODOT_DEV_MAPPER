# S38 — P5 Navigation et arborescence res:// (CAP-10) : découpage

> Fiche d'exécution du mode autonome. Chaque case se coche avec `python3 suivi/outil.py cocher S38 <sous-étape> --ia <n>`, juste après la sous-étape : la commande vérifie l'ordre et l'identité de l'IA, signe la case (IA, date, heure UTC), commite et pousse. Une sous-étape non cochée par cette commande est considérée comme non faite. Règles : `docs/construction/sequence.md`. Avancement : `SUIVI.md` et `suivi/tableau.html`.

| Champ | Valeur |
| --- | --- |
| Réalise | IA 1 (conception) |
| Vérifie | IA 3 (vérification), jamais un auteur de l'unité |
| Piste | M.A Phases P4a, P4b, P5 : S36 → S36.P → S37 → S37.P → S38 → S38.P (unité 5 sur 6) |
| Commence après | S37.P (cochée dans `SUIVI.md`) |
| Indépendante de | S39, S39.P, S40, S40.P |
| Branche | `tache/S38-P5-decoupage` |
| Fiche de conception | `docs/construction/mvp.md`, section P5 |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Cette unité est la 5e de la piste M.A « Phases P4a, P4b, P5 », dont les unités se font à la suite. Les autres pistes de la section (M.B) avancent en même temps, chacune de son côté. Elle attend S37.P, l'unité précédente de la piste. S38.P l'attendra. Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Découper la phase P5 en 4 à 12 tâches avec le prompt de découpage de `docs/construction/mvp.md`, en tenant compte des résultats du POC et des phases précédentes.
- Écrire `docs/construction/mvp-P5.md` (conception) et une fiche d'exécution par tâche, `suivi/S38.<k>-<nom>.md`, à partir de `suivi/_modele-tache.md`.
- Donner à chaque tâche ses prérequis réels : une tâche qui ne dépend que de la fin du découpage peut avancer en même temps que les autres. Les tâches qui s'enchaînent forment une sous-piste ; le tableau de bord les regroupe seul.
- Écrire dans le rapport les lignes à ajouter à `SUIVI.md`, entre **S38** et **S38.P**, dans la piste M.A, au format des autres lignes.

## Fichiers autorisés

`docs/construction/mvp-P5.md`, `suivi/S38.*-*.md` (sauf la porte S38.P), `rapports/S38*.md`.

## Prompt de réalisation

```text
Tu réalises l'unité S38 « P5 Navigation et arborescence res:// (CAP-10) : découpage » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.
Réalisation prévue : IA 1 (conception) ; vérification : IA 3 (vérification). Ton numéro d'IA est celui que te donne le prompt de créneau : tu le passes à --ia, et il signe chaque case que tu coches.

AVANT TOUT, depuis ton clone principal du dépôt
1. Lis REGLES_AGENTS.md s'il existe, puis cette fiche : suivi/S38-P5-decoupage.md.
2. python3 suivi/outil.py prendre S38 --ia <n>
   - « PRISE » ou « REPRISE » : tu es sur la branche tache/S38-P5-decoupage ; commence à la sous-étape affichée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
   - « REFUSÉ » : l'unité n'est pas pour toi maintenant (déjà prise par une autre IA, S37.P non cochée, autre IA prévue) : reviens au prompt de créneau et choisis autre chose.

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S38.md et les cases de suivi/S38-P5-decoupage.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status. Tu ne pousses jamais avec --force.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.
- Une décision réservée à l'humain (docs/construction/sequence.md §5) : arrêt obligatoire, rien d'autre.

TRACE OBLIGATOIRE, après CHAQUE sous-étape et avant la suivante
1. git add <les fichiers de la sous-étape> (jamais git add -A).
2. python3 suivi/outil.py cocher S38 <sous-étape> --ia <n>
   La commande vérifie l'ordre des cases et ton identité, coche la case dans suivi/S38-P5-decoupage.md, la signe (IA, date, heure UTC), commite et pousse sur tache/S38-P5-decoupage.
3. Une sous-étape faite mais non cochée par cette commande est considérée comme non faite : l'IA suivante la refera. Tu ne coches jamais une case à la main.
4. Tu ne modifies jamais SUIVI.md : il ne change qu'à la fusion, sous le verrou de main. Plusieurs IA le lisent en même temps ; aucune ne l'écrit hors de ce verrou.
5. Avant de cocher la dernière sous-étape R : « Statut : TERMINÉ » dans rapports/S38.md, puis git add.
6. Poussée refusée et non rattrapée par la commande : ne force jamais ; git pull --rebase origin tache/S38-P5-decoupage, puis relance la commande.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (docs/construction/mvp.md, prompt de découpage)
Tu découpes la phase P5 du projet GODOT_DEV_MAPPER en tâches exécutables, au format des fiches de docs/construction/etape-4.md.

ENTRÉES : docs/plan-directeur.md (§3, capacités {CAP} ; §9, porte de la phase) ; docs/construction/mvp.md, section P5 ; docs/DECISIONS.md ; docs/spikes/ ; PROJECT_STATE.md (budget consommé, taux de réussite par IA) ; docs/revues/revue-poc.md.

PRODUIS docs/construction/mvp-P5.md :
- objectif, obligations, méthodologie, points de contrôle et cheminement d'amélioration de la phase, précisés par les résultats du POC ;
- de 4 à 12 tâches. Chacune avec : modèle, autonomie, dépendances, fichiers autorisés, pack de contexte, contrôles exécutables dont au moins une contre-épreuve, et prompt de réalisation rempli à partir du prompt universel.

RÈGLES
- Une tâche tient en 1 à 3 h de travail agent et en 1 h de relecture humaine au plus.
- Une tâche qui touche un format persisté, le protocole ou une façade est vérifiée par IA 1.
- Les contrats et leurs tests précèdent l'implémentation, comme à l'étape 3. Une tâche qui révise un contrat liste explicitement `docs/CONTRACTS.md`, `contracts/` et `tests/contract/` dans ses fichiers autorisés ; IA 1 la réalise, IA 3 la vérifie, tu la valides.
- Chaque tâche précise les marqueurs de `tests/pending/` qu'elle crée ou supprime, et les scripts de `tools/ci/checks.d/` qu'elle ajoute. Aucune ne modifie `PROJECT_STATE.md` ni `docs/DECISIONS.md`.
- Le total reste dans le budget de la phase ({budget} h humaines). Sinon, tu signales le dépassement et proposes quoi retirer.
- Ne réalise aucune tâche.
TRAVAIL TECHNIQUE — fin de la copie exacte du guide

ADAPTATIONS DU MODE AUTONOME
- Budget : traduis les heures humaines de la phase en créneaux d'IA avec le ratio observé au POC (docs/revues/revue-poc.md).
- Pour chaque tâche, crée suivi/S38.<k>-<nom>.md en copiant suivi/_modele-tache.md et en remplissant toutes ses sections : prompt de réalisation complet (avec PRISE et TRACE OBLIGATOIRE), sous-étapes R, contrôles, prompt de vérification, sous-étapes V et F, chacune avec son « ⟶ cocher ».
- Prérequis : S38 pour toute tâche, plus les tâches de la phase dont elle dépend vraiment. Évite que deux tâches indépendantes modifient le même fichier.
- Répartition : réalisation par IA 2, sauf contrat, protocole, façade ou format persisté (IA 1) ; vérification par IA 3, sauf ces mêmes sujets (IA 1, ou IA 3 si IA 1 est l'auteur).
- Écris dans le rapport les lignes SUIVI.md à insérer ; le vérificateur les insère à la fusion, sous le verrou de main.
- Contrôle final : python3 suivi/outil.py verifier → OK, une fois les lignes insérées (le vérificateur le relance après insertion).

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche ; après chacune, git add puis python3 suivi/outil.py cocher S38 R<k> --ia <n>.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Chaque sous-étape faite est cochée par `cocher`. Complète rapports/S38.md (sorties, « Passation » en cinq lignes au plus), git add, git commit, git push origin HEAD:tache/S38-P5-decoupage.
- git status ne montre aucune modification non commitée ; rien ne reste non poussé.

FORMAT DE rapports/S38.md (créé par prendre ; tu le complètes)
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

Après chaque sous-étape : `git add` de ses fichiers, puis `python3 suivi/outil.py cocher S38 R<k> --ia <n>` (coche, signe, commite, pousse).

- [ ] R0 Prise en charge : `python3 suivi/outil.py prendre S38 --ia <n>` (prérequis cochés dans `SUIVI.md` : S37.P ; branche `tache/S38-P5-decoupage` créée ou reprise ; `rapports/S38.md` au statut EN COURS) ⟶ cochée par `prendre`
- [ ] R1 Lire la section de la phase, `docs/revues/revue-poc.md`, `PROJECT_STATE.md`, `SUIVI.md` et les rapports des phases précédentes. ⟶ cocher S38 R1
- [ ] R2 Écrire `docs/construction/mvp-P5.md`. ⟶ cocher S38 R2
- [ ] R3 Créer une fiche `suivi/S38.<k>-<nom>.md` par tâche, depuis `suivi/_modele-tache.md`, toutes sections remplies. ⟶ cocher S38 R3
- [ ] R4 Écrire dans le rapport les lignes à insérer dans `SUIVI.md`, avec leurs prérequis. ⟶ cocher S38 R4
- [ ] R5 Contrôles finaux : chaque fiche créée a toutes ses sections ; « Statut : TERMINÉ » dans le rapport ⟶ cocher S38 R5

## Prompt de vérification

```text
Tu vérifies l'unité S38 « P5 Navigation et arborescence res:// (CAP-10) : découpage » du projet GODOT_DEV_MAPPER. Vérification prévue : IA 3 (vérification). Ton numéro d'IA est celui du prompt de créneau. Tu n'es jamais un auteur de l'unité : la commande de prise le contrôle.

PRISE, depuis ton clone principal
python3 suivi/outil.py prendre S38 --ia <n> --verification
- « VÉRIFICATION PRISE » : copie neuve ../verif-S38-P5-decoupage créée sur origin/tache/S38-P5-decoupage, verdict EN COURS écrit, V1 cochée. cd ../verif-S38-P5-decoupage : toute la vérification se fait dans ce dossier.
- « REFUSÉ » : une autre IA vérifie déjà, tu es auteur, ou l'unité n'est pas terminée : reviens au prompt de créneau.
GODOT : même procédure que le prompt de réalisation.
Tu ne modifies aucun fichier de l'unité. Tu écris seulement ton verdict et tes cases V.

TRACE OBLIGATOIRE : après chaque sous-étape V, git add du fichier de verdict, puis python3 suivi/outil.py cocher S38 <V…> --ia <n>. Pour la dernière : --verdict ACCEPTÉE ou --verdict REFUSÉE, identique à la ligne « Verdict » du fichier. Une sous-étape non cochée par cette commande est considérée comme non faite.

1. TRAÇABILITÉ. Chaque case R cochée est signée « — IA n · date » et a son commit sur la branche (git log --oneline origin/main..HEAD). Case cochée sans travail prouvé dans le rapport : refus.
2. PÉRIMÈTRE. git diff --name-only origin/main...HEAD. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S38*.md et suivi/S38-P5-decoupage.md. Tout autre fichier : refus.
3. CONTRÔLES. Relance chacun dans ta copie neuve et compare au rapport : ceux de la fiche.
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
6. COHÉRENCE. Contrat et invariants concernés.
Vérifie le découpage : budget de la phase respecté, chaque tâche avec au moins une contre-épreuve, prérequis réels et sans cycle, aucune paire de tâches indépendantes sur le même fichier, sous-étapes au format « ⟶ cocher ».

VERDICT dans rapports/S38-verif-<tentative>.md (créé par la prise) :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte

SI ACCEPTÉE — FUSION, depuis ton clone principal
1. python3 suivi/outil.py fusionner S38 --ia <n> --godot "$B"
   Elle prend le verrou de main (et attend s'il est pris), fusionne dans ../fusion-S38-P5-decoupage, lance run_all_checks.sh, coche la ligne dans SUIVI.md et la case F1. Si les contrôles échouent : verdict passé à REFUSÉE, main inchangée, verrou rendu ; arrête-toi sur cette unité.
2. cd ../fusion-S38-P5-decoupage ; fais les sous-étapes F suivantes de la fiche, et coche chacune : python3 suivi/outil.py cocher S38 F<k> --ia <n> (commit local, sans poussée).
   Dans ../fusion-S38-P5-decoupage : insère dans SUIVI.md, entre S38 et S38.P, les lignes données par le rapport ; python3 suivi/outil.py verifier → OK ; git add SUIVI.md ; puis coche F2.
3. python3 suivi/outil.py publier S38 --ia <n> : dernière case cochée, verifier relancé, main poussée, branche supprimée, verrou rendu.
SI REFUSÉE : arrête-toi sur cette unité ; son auteur la reprendra avec prendre.
```

## Sous-étapes de vérification

Dans `../verif-S38-P5-decoupage`, après chaque sous-étape : `git add` du verdict, puis `python3 suivi/outil.py cocher S38 V<k> --ia <n>`.

- [ ] V1 Prise en charge : `python3 suivi/outil.py prendre S38 --ia <n> --verification` (pas un auteur ; copie neuve `../verif-S38-P5-decoupage` sur `origin/tache/S38-P5-decoupage` ; verdict EN COURS) ⟶ cochée par `prendre`
- [ ] V2 Traçabilité : chaque case R cochée porte une signature « — IA n · date » et un commit sur la branche (`git log --oneline origin/main..HEAD`) ⟶ cocher S38 V2
- [ ] V3 Budget de la phase respecté, ou dépassement signalé avec une proposition de retrait. ⟶ cocher S38 V3
- [ ] V4 Chaque fiche créée : toutes les sections, au moins une contre-épreuve, fichiers autorisés précis, sous-étapes au format « ⟶ cocher ». ⟶ cocher S38 V4
- [ ] V5 Prérequis réels, sans cycle ; tâches indépendantes sans fichier commun. ⟶ cocher S38 V5
- [ ] V6 Verdict écrit dans `rapports/S38-verif-<tentative>.md` ⟶ cocher S38 V6 --verdict ACCEPTÉE ou --verdict REFUSÉE

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

F1 et la dernière se cochent par `fusionner` et `publier` ; les autres, dans `../fusion-S38-P5-decoupage`, par `python3 suivi/outil.py cocher S38 F<k> --ia <n>` (commit local).

- [ ] F1 Fusion : `python3 suivi/outil.py fusionner S38 --ia <n> --godot "$B"` : verrou de `main`, fusion `--no-ff` dans `../fusion-S38-P5-decoupage`, `tools/ci/run_all_checks.sh` sur `main` → ALL_CHECKS OK s'il existe (sinon fusion annulée et verdict passé à REFUSÉE), ligne **S38** cochée dans `SUIVI.md` ⟶ cochée par `fusionner`
- [ ] F2 Lignes des tâches insérées dans `SUIVI.md`, entre **S38** et **S38.P**, dans la même piste ; `python3 suivi/outil.py verifier` → OK ⟶ cocher S38 F2
- [ ] F3 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette ⟶ cocher S38 F3
- [ ] F4 Publication : `python3 suivi/outil.py publier S38 --ia <n>` (verifier OK, `main` poussée, branche `tache/S38-P5-decoupage` supprimée, verrou rendu) ⟶ cochée par `publier`

## Pour la recette

Rien de propre à cette unité.
