# S37 — P4b Backend statique et inventaire (CAP-08, CAP-09) : revue du découpage

> Fiche d'exécution du mode autonome. Chaque case se coche avec `python3 suivi/outil.py cocher S37 <sous-étape> --ia <n>`, juste après la sous-étape : la commande vérifie l'ordre et l'identité de l'IA, signe la case (IA, date, heure UTC), commite et pousse. Une sous-étape non cochée par cette commande est considérée comme non faite. Règles : `docs/construction/sequence.md`. Avancement : `SUIVI.md` et `suivi/tableau.html`.

| Champ | Valeur |
| --- | --- |
| Réalise | IA 1 (conception) |
| Vérifie | IA 3 (vérification), jamais un auteur de l'unité |
| Piste | M.A Phases P4a, P4b, P5 : S36 → S36.P → S37 → S37.P → S38 → S38.P (unité 3 sur 6) |
| Commence après | S36.P (cochée dans `SUIVI.md`) |
| Indépendante de | S39, S39.1, S39.2, S39.3, S39.4, S39.5, S39.6, S39.7, S39.10, S39.12 |
| Branche | `tache/S37-P4b-decoupage` |
| Fiche de conception | `docs/construction/mvp.md`, section P4b |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Cette unité est la 3e de la piste M.A « Phases P4a, P4b, P5 », dont les unités se font à la suite. Les autres pistes de la section (M.B) avancent en même temps, chacune de son côté. Elle attend S36.P, l'unité précédente de la piste. S37.P l'attendra. Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Revoir le découpage provisoire de la phase P4b : 11 tâches (S37.1, S37.2, S37.3, S37.4, S37.5, S37.6, S37.7, S37.8, S37.9, S37.10, S37.11), écrites avant le POC d'après `docs/construction/mvp.md` et le plan directeur.
- Le confronter aux résultats du POC (`docs/revues/revue-poc.md`), aux décisions (`docs/DECISIONS.md`), aux spikes, aux mesures et aux rapports des phases précédentes.
- Pour chaque tâche : la garder, la préciser (fiche modifiée), la retirer, ou la remplacer ; ajouter les tâches manquantes depuis `suivi/_modele-tache.md`. Total dans le budget de la phase : 8 à 14 h humaines.
- Écrire `docs/construction/mvp-P4b.md` : objectif, obligations, méthodologie, points de contrôle et cheminement d'amélioration de la phase, précisés par les résultats ; tableau des tâches retenues, avec la raison de chaque changement.
- Écrire dans le rapport les changements à porter dans `SUIVI.md` : lignes ajoutées sous **S37**, lignes retirées, prérequis modifiés, rôles modifiés (réalise, vérifie) ; ou « aucun changement ». La fiche et sa ligne de `SUIVI.md` doivent dire la même chose : `verifier` compare rôles et prérequis.

## Fichiers autorisés

`docs/construction/mvp-P4b.md`, `suivi/S37.*-*.md` (fiches des tâches de la phase, sauf la porte S37.P), `rapports/S37*.md`.

## Tâches du découpage provisoire

- **S37.1** · Contrat C-08 : inventaire du projet et relations d'appel · réalise IA 1 · vérifie IA 3 · après S37 · `suivi/S37.1-contrat-c08.md`
- **S37.2** · Façades d'introspection et de syntaxe · réalise IA 2 · vérifie IA 1 · après S37 · `suivi/S37.2-facades-introspection-syntaxe.md`
- **S37.3** · Fixtures de syntaxe GDScript et relations attendues · réalise IA 3 · vérifie IA 2 · après S37.1 · `suivi/S37.3-fixtures-syntaxe.md`
- **S37.4** · Lexeur GDScript · réalise IA 2 · vérifie IA 3 · après S37.2, S37.3 · `suivi/S37.4-lexeur-gdscript.md`
- **S37.5** · Extraction des déclarations et de leurs ancrages · réalise IA 2 · vérifie IA 3 · après S37.4 · `suivi/S37.5-declarations.md`
- **S37.6** · Extraction des relations d'appel et de signal · réalise IA 2 · vérifie IA 3 · après S37.5 · `suivi/S37.6-relations-appel.md`
- **S37.7** · Inventaire du projet sans instanciation · réalise IA 2 · vérifie IA 3 · après S37.2, S37.6 · `suivi/S37.7-inventaire.md`
- **S37.8** · Résolution entre scripts et fusion avec le graphe déclaré · réalise IA 2 · vérifie IA 1 · après S37.7 · `suivi/S37.8-resolution-provenance.md`
- **S37.9** · Cache d'index par révision de fichier · réalise IA 2 · vérifie IA 3 · après S37.7 · `suivi/S37.9-cache-index.md`
- **S37.10** · Grand projet de mesure : 300 scripts ou plus · réalise IA 3 · vérifie IA 1 · après S37 · `suivi/S37.10-grand-projet.md`
- **S37.11** · Tests de référence sur le banc d'essai et contrôle CI · réalise IA 3 · vérifie IA 2 · après S37.8, S37.9, S37.10 · `suivi/S37.11-golden-banc.md`

## Prompt de réalisation

```text
Tu réalises l'unité S37 « P4b Backend statique et inventaire (CAP-08, CAP-09) : revue du découpage » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.
Réalisation prévue : IA 1 (conception) ; vérification : IA 3 (vérification). Ton numéro d'IA est celui que te donne le prompt de créneau : tu le passes à --ia, et il signe chaque case que tu coches.

AVANT TOUT, depuis ton clone principal du dépôt
1. Lis REGLES_AGENTS.md s'il existe, puis cette fiche : suivi/S37-P4b-decoupage.md.
2. python3 suivi/outil.py prendre S37 --ia <n>
   - « PRISE » ou « REPRISE » : tu es sur la branche tache/S37-P4b-decoupage ; commence à la sous-étape affichée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
   - « REFUSÉ » : l'unité n'est pas pour toi maintenant (déjà prise par une autre IA, S36.P non cochée, autre IA prévue) : reviens au prompt de créneau et choisis autre chose.

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S37.md et les cases de suivi/S37-P4b-decoupage.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status. Tu ne pousses jamais avec --force.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.
- Une décision réservée à l'humain (docs/construction/sequence.md §5) : arrêt obligatoire, rien d'autre : python3 suivi/outil.py arreter --ia <n> --unite S37 --raison "<raison>", puis fin du créneau.

TRACE OBLIGATOIRE, après CHAQUE sous-étape et avant la suivante
1. git add <les fichiers de la sous-étape> (jamais git add -A).
2. python3 suivi/outil.py cocher S37 <sous-étape> --ia <n>
   La commande vérifie l'ordre des cases et ton identité, coche la case dans suivi/S37-P4b-decoupage.md, la signe (IA, date, heure UTC), commite et pousse sur tache/S37-P4b-decoupage.
3. Une sous-étape faite mais non cochée par cette commande est considérée comme non faite : l'IA suivante la refera. Tu ne coches jamais une case à la main.
4. Tu ne modifies jamais SUIVI.md : il ne change qu'à la fusion, sous le verrou de main. Plusieurs IA le lisent en même temps ; aucune ne l'écrit hors de ce verrou.
5. Avant de cocher la dernière sous-étape R : « Statut : TERMINÉ » dans rapports/S37.md, puis git add.
6. Poussée refusée et non rattrapée par la commande : ne force jamais ; git pull --rebase origin tache/S37-P4b-decoupage, puis relance la commande.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (docs/construction/mvp.md, prompt de découpage)
Tu découpes la phase P4b du projet GODOT_DEV_MAPPER en tâches exécutables, au format des fiches de docs/construction/etape-4.md.

ENTRÉES : docs/plan-directeur.md (§3, capacités {CAP} ; §9, porte de la phase) ; docs/construction/mvp.md, section P4b ; docs/DECISIONS.md ; docs/spikes/ ; PROJECT_STATE.md (budget consommé, taux de réussite par IA) ; docs/revues/revue-poc.md.

PRODUIS docs/construction/mvp-P4b.md :
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
- Le découpage existe déjà : les fiches suivi/S37.1-… à suivi/S37.11-…, listées dans cette fiche. Tu le revois au lieu de partir de zéro ; le document à produire reste celui du guide, docs/construction/mvp-P4b.md.
- Budget : traduis les heures humaines de la phase en créneaux d'IA avec le ratio observé au POC (docs/revues/revue-poc.md).
- Tu gardes une tâche telle quelle si rien ne la contredit. Tu la modifies si un résultat l'exige (décision de spike, contrat révisé, outil renommé, mesure), en le citant.
- Une tâche ajoutée : nouvelle fiche suivi/S37.<k>-<nom>.md depuis suivi/_modele-tache.md, toutes sections remplies, sous-étapes au format « ⟶ cocher ». Une tâche retirée : sa fiche reste, avec la raison en tête ; le vérificateur retire sa ligne de SUIVI.md à la fusion.
- Prérequis : S37 pour toute tâche, plus les tâches dont elle dépend vraiment, y compris d'une autre phase quand deux phases parallèles touchent le même fichier (contrat révisé, flow_trace.gd, envelope.gd et codec, tools/deps_rules.json, branche du banc). Deux tâches indépendantes ne modifient jamais le même fichier.
- Un nouveau contrat va dans son propre fichier docs/contracts/C-xx.md ; une révision de C-01 à C-07 reste dans docs/CONTRACTS.md, avec sa version cible écrite dans la fiche. Une nouvelle vue est un onglet ui/vues/<nom>/ (convention de S39.12), jamais une modification de plugin.gd ou du panneau principal.
- Répartition : réalisation par IA 2, sauf contrat, protocole, façade ou format persisté (IA 1) ; vérification par IA 3, sauf ces mêmes sujets (IA 1, ou IA 3 si IA 1 est l'auteur).
- Contrôle final : python3 suivi/outil.py verifier → OK, une fois SUIVI.md mis à jour à la fusion.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche ; après chacune, git add puis python3 suivi/outil.py cocher S37 R<k> --ia <n>.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Chaque sous-étape faite est cochée par `cocher`. Complète rapports/S37.md (sorties, « Passation » en cinq lignes au plus), git add, git commit, git push origin HEAD:tache/S37-P4b-decoupage.
- git status ne montre aucune modification non commitée ; rien ne reste non poussé.

FORMAT DE rapports/S37.md (créé par prendre ; tu le complètes)
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

Après chaque sous-étape : `git add` de ses fichiers, puis `python3 suivi/outil.py cocher S37 R<k> --ia <n>` (coche, signe, commite, pousse).

- [ ] R0 Prise en charge : `python3 suivi/outil.py prendre S37 --ia <n>` (prérequis cochés dans `SUIVI.md` : S36.P ; branche `tache/S37-P4b-decoupage` créée ou reprise ; `rapports/S37.md` au statut EN COURS) ⟶ cochée par `prendre`
- [ ] R1 Lire `docs/revues/revue-poc.md`, `docs/DECISIONS.md`, `docs/spikes/`, `PROJECT_STATE.md` et les rapports des phases précédentes ; noter les faits qui touchent la phase. ⟶ cocher S37 R1
- [ ] R2 Relire chaque fiche du découpage provisoire (S37.1, S37.2, S37.3, S37.4, S37.5, S37.6, S37.7, S37.8, S37.9, S37.10, S37.11) et décider : garder, préciser, retirer ou remplacer, avec la raison. ⟶ cocher S37 R2
- [ ] R3 Appliquer les décisions aux fiches ; créer les fiches des tâches ajoutées. ⟶ cocher S37 R3
- [ ] R4 Écrire `docs/construction/mvp-P4b.md`. ⟶ cocher S37 R4
- [ ] R5 Écrire dans le rapport les changements à porter dans `SUIVI.md` (lignes, prérequis, rôles), ou « aucun changement ». ⟶ cocher S37 R5
- [ ] R6 Contrôles finaux : chaque fiche gardée, modifiée ou ajoutée a toutes ses sections ; budget respecté ; « Statut : TERMINÉ » dans le rapport ⟶ cocher S37 R6

## Prompt de vérification

```text
Tu vérifies l'unité S37 « P4b Backend statique et inventaire (CAP-08, CAP-09) : revue du découpage » du projet GODOT_DEV_MAPPER. Vérification prévue : IA 3 (vérification). Ton numéro d'IA est celui du prompt de créneau. Tu n'es jamais un auteur de l'unité : la commande de prise le contrôle.

PRISE, depuis ton clone principal
python3 suivi/outil.py prendre S37 --ia <n> --verification
- « VÉRIFICATION PRISE » : copie neuve ../verif-S37-P4b-decoupage créée sur origin/tache/S37-P4b-decoupage, verdict EN COURS écrit, V1 cochée. cd ../verif-S37-P4b-decoupage : toute la vérification se fait dans ce dossier.
- « REFUSÉ » : une autre IA vérifie déjà, tu es auteur, ou l'unité n'est pas terminée : reviens au prompt de créneau.
- Créneau fini avant le verdict : au créneau suivant, etat te propose la même commande ; elle recrée la copie (« VÉRIFICATION REPRISE ») et tu reprends à la première case V ouverte.
GODOT : même procédure que le prompt de réalisation.
Tu ne modifies aucun fichier de l'unité. Tu écris seulement ton verdict et tes cases V.

TRACE OBLIGATOIRE : après chaque sous-étape V, git add du fichier de verdict, puis python3 suivi/outil.py cocher S37 <V…> --ia <n>. Pour la dernière : --verdict ACCEPTÉE ou --verdict REFUSÉE, identique à la ligne « Verdict » du fichier. Une sous-étape non cochée par cette commande est considérée comme non faite.

1. TRAÇABILITÉ. Chaque case R cochée est signée « — IA n · date » et a son commit sur la branche (git log --oneline origin/main..HEAD). Case cochée sans travail prouvé dans le rapport : refus.
2. PÉRIMÈTRE. git diff --name-only origin/main...HEAD. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S37*.md et suivi/S37-P4b-decoupage.md. Tout autre fichier : refus.
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
Vérifie la revue : chaque changement cite le fait qui l'impose ; budget de la phase respecté ; chaque fiche gardée, modifiée ou ajoutée a toutes ses sections et au moins une contre-épreuve ; prérequis réels et sans cycle ; aucune paire de tâches indépendantes sur le même fichier.

VERDICT dans rapports/S37-verif-<tentative>.md (créé par la prise) :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte

SI ACCEPTÉE — FUSION, depuis ton clone principal (cd hors de ../verif-S37-P4b-decoupage)
1. python3 suivi/outil.py fusionner S37 --ia <n>
   Elle trouve Godot (--godot, $GODOT, cache du bloc GODOT ou tools/ci/fetch_godot.sh ; sans Godot : REFUSÉ, verdict inchangé), prend le verrou de main (et attend s'il est pris), revérifie l'unité, fusionne dans ../fusion-S37-P4b-decoupage, lance run_all_checks.sh, coche la ligne dans SUIVI.md et la case F1. Si les contrôles échouent : verdict passé à REFUSÉE, main inchangée, verrou rendu ; arrête-toi sur cette unité. La fusion te revient parce que tu as signé le verdict ; une autre IA ne la fait qu'après 12 h.
2. cd ../fusion-S37-P4b-decoupage ; fais les sous-étapes F suivantes de la fiche, et coche chacune : python3 suivi/outil.py cocher S37 F<k> --ia <n> (commit local, sans poussée).
   Dans ../fusion-S37-P4b-decoupage : porte dans SUIVI.md les changements du rapport (lignes ajoutées sous S37, retirées, prérequis, rôles réalise et vérifie) ; python3 suivi/outil.py verifier → OK (il compare rôles et prérequis de chaque fiche à sa ligne) ; git add SUIVI.md ; puis coche F2.
3. python3 suivi/outil.py publier S37 --ia <n> : dernière case cochée, verifier relancé, main poussée, branche supprimée, verrou rendu.
SI REFUSÉE : arrête-toi sur cette unité ; son auteur la reprendra avec prendre.
```

## Sous-étapes de vérification

Dans `../verif-S37-P4b-decoupage`, après chaque sous-étape : `git add` du verdict, puis `python3 suivi/outil.py cocher S37 V<k> --ia <n>`.

- [ ] V1 Prise en charge : `python3 suivi/outil.py prendre S37 --ia <n> --verification` (pas un auteur ; copie neuve `../verif-S37-P4b-decoupage` sur `origin/tache/S37-P4b-decoupage` ; verdict EN COURS) ⟶ cochée par `prendre`
- [ ] V2 Traçabilité : chaque case R cochée porte une signature « — IA n · date » et un commit sur la branche (`git log --oneline origin/main..HEAD`) ⟶ cocher S37 V2
- [ ] V3 Chaque changement cite le fait du POC ou d'une phase précédente qui l'impose. ⟶ cocher S37 V3
- [ ] V4 Budget de la phase respecté, ou dépassement signalé avec une proposition de retrait. ⟶ cocher S37 V4
- [ ] V5 Chaque fiche gardée, modifiée ou ajoutée : toutes les sections, au moins une contre-épreuve, fichiers autorisés précis, sous-étapes au format « ⟶ cocher ». ⟶ cocher S37 V5
- [ ] V6 Prérequis réels, sans cycle ; tâches indépendantes sans fichier commun. ⟶ cocher S37 V6
- [ ] V7 Verdict écrit dans `rapports/S37-verif-<tentative>.md` ⟶ cocher S37 V7 --verdict ACCEPTÉE ou --verdict REFUSÉE

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

F1 et la dernière se cochent par `fusionner` et `publier` ; les autres, dans `../fusion-S37-P4b-decoupage`, par `python3 suivi/outil.py cocher S37 F<k> --ia <n>` (commit local).

- [ ] F1 Fusion, depuis le clone principal : `python3 suivi/outil.py fusionner S37 --ia <n>` : Godot trouvé seul (--godot, $GODOT, cache du bloc GODOT ou fetch_godot.sh), verrou de `main`, fusion `--no-ff` dans `../fusion-S37-P4b-decoupage`, `tools/ci/run_all_checks.sh` sur `main` → ALL_CHECKS OK s'il existe (sinon fusion annulée et verdict passé à REFUSÉE), ligne **S37** cochée dans `SUIVI.md` ⟶ cochée par `fusionner`
- [ ] F2 Changements du rapport portés dans `SUIVI.md` (lignes ajoutées sous **S37**, retirées, prérequis, rôles) ; `python3 suivi/outil.py verifier` → OK ⟶ cocher S37 F2
- [ ] F3 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette ⟶ cocher S37 F3
- [ ] F4 Publication : `python3 suivi/outil.py publier S37 --ia <n>` (verifier OK, `main` poussée, branche `tache/S37-P4b-decoupage` supprimée, verrou rendu) ⟶ cochée par `publier`

## Pour la recette

Rien de propre à cette unité.
