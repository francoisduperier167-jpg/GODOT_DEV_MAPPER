# S49 — P16 Durcissement et documentation : revue du découpage

> Fiche d'exécution du mode autonome. Chaque case se coche avec `python3 suivi/outil.py cocher S49 <sous-étape> --ia <n>`, juste après la sous-étape : la commande vérifie l'ordre et l'identité de l'IA, signe la case (IA, date, heure UTC), commite et pousse. Une sous-étape non cochée par cette commande est considérée comme non faite. Règles : `docs/construction/sequence.md`. Avancement : `SUIVI.md` et `suivi/tableau.html`.

| Champ | Valeur |
| --- | --- |
| Réalise | IA 1 (conception) |
| Vérifie | IA 3 (vérification), jamais un auteur de l'unité |
| Piste | Rendez-vous de la V1 : S49 → S49.P |
| Commence après | S47.P, S48.P (cochées dans `SUIVI.md`) |
| Indépendante de | aucune |
| Branche | `tache/S49-P16-decoupage` |
| Fiche de conception | `docs/construction/v1.md`, section P16 |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Cette unité appartient au rendez-vous de la V1 : elle attend la fin des pistes V.A, V.B, V.C, V.D. Concrètement, elle attend S47.P, S48.P. S49.P l'attendra. Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Revoir le découpage provisoire de la phase P16 : 10 tâches (S49.1, S49.2, S49.3, S49.4, S49.5, S49.6, S49.7, S49.8, S49.9, S49.10), écrites avant le POC d'après `docs/construction/v1.md` et le plan directeur.
- Le confronter aux résultats du POC (`docs/revues/revue-poc.md`), aux décisions (`docs/DECISIONS.md`), aux spikes, aux mesures et aux rapports des phases précédentes.
- Pour chaque tâche : la garder, la préciser (fiche modifiée), la retirer, ou la remplacer ; ajouter les tâches manquantes depuis `suivi/_modele-tache.md`. Total dans le budget de la phase : 12 à 20 h humaines.
- Écrire `docs/construction/v1-P16.md` : objectif, obligations, méthodologie, points de contrôle et cheminement d'amélioration de la phase, précisés par les résultats ; tableau des tâches retenues, avec la raison de chaque changement.
- Écrire dans le rapport les changements à porter dans `SUIVI.md` : lignes ajoutées sous **S49**, lignes retirées, prérequis modifiés, rôles modifiés (réalise, vérifie) ; ou « aucun changement ». La fiche et sa ligne de `SUIVI.md` doivent dire la même chose : `verifier` compare rôles et prérequis.

## Fichiers autorisés

`docs/construction/v1-P16.md`, `suivi/S49.*-*.md` (fiches des tâches de la phase, sauf la porte S49.P), `rapports/S49*.md`.

## Tâches du découpage provisoire

- **S49.1** · Deux versions stables dans la CI · réalise IA 2 · vérifie IA 1 · après S49 · `suivi/S49.1-deux-stables.md`
- **S49.2** · Traitement de la dette · réalise IA 1 · vérifie IA 3 · après S49 · `suivi/S49.2-dette.md`
- **S49.3** · Documentation : installation et premiers pas · réalise IA 3 · vérifie IA 2 · après S49 · `suivi/S49.3-doc-installation.md`
- **S49.4** · Documentation des modes · réalise IA 3 · vérifie IA 2 · après S49.3 · `suivi/S49.4-doc-modes.md`
- **S49.5** · Guide d'instrumentation · réalise IA 3 · vérifie IA 2 · après S49.3 · `suivi/S49.5-doc-instrumentation.md`
- **S49.6** · Installation à froid par la documentation seule · réalise IA 1 · vérifie IA 2 · après S49.4, S49.5, S49.8, S49.9 · `suivi/S49.6-installation-froid.md`
- **S49.7** · Démonstrations de CAP-12 à CAP-18 rejouées · réalise IA 2 · vérifie IA 3 · après S49.1 · `suivi/S49.7-demos-v1.md`
- **S49.8** · Installation et désinstallation propres de la V1 · réalise IA 3 · vérifie IA 2 · après S49.3, S49.7 · `suivi/S49.8-desinstallation-v1.md`
- **S49.9** · Mesures finales et limites · réalise IA 1 · vérifie IA 3 · après S49.7 · `suivi/S49.9-mesures-v1.md`
- **S49.10** · Dossier de décision : licence et diffusion · réalise IA 1 · vérifie IA 3 · après S49 · `suivi/S49.10-dossier-licence.md`

## Prompt de réalisation

```text
Tu réalises l'unité S49 « P16 Durcissement et documentation : revue du découpage » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.
Réalisation prévue : IA 1 (conception) ; vérification : IA 3 (vérification). Ton numéro d'IA est celui que te donne le prompt de créneau : tu le passes à --ia, et il signe chaque case que tu coches.

AVANT TOUT, depuis ton clone principal du dépôt
1. Lis REGLES_AGENTS.md s'il existe, puis cette fiche : suivi/S49-P16-decoupage.md.
2. python3 suivi/outil.py prendre S49 --ia <n>
   - « PRISE » ou « REPRISE » : tu es sur la branche tache/S49-P16-decoupage ; commence à la sous-étape affichée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
   - « REFUSÉ » : l'unité n'est pas pour toi maintenant (déjà prise par une autre IA, S47.P, S48.P non cochées, autre IA prévue) : reviens au prompt de créneau et choisis autre chose.

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S49.md et les cases de suivi/S49-P16-decoupage.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status. Tu ne pousses jamais avec --force.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.
- Une décision réservée à l'humain (docs/construction/sequence.md §5) : arrêt obligatoire, rien d'autre : python3 suivi/outil.py arreter --ia <n> --unite S49 --raison "<raison>", puis fin du créneau.

TRACE OBLIGATOIRE, après CHAQUE sous-étape et avant la suivante
1. git add <les fichiers de la sous-étape> (jamais git add -A).
2. python3 suivi/outil.py cocher S49 <sous-étape> --ia <n>
   La commande vérifie l'ordre des cases et ton identité, coche la case dans suivi/S49-P16-decoupage.md, la signe (IA, date, heure UTC), commite et pousse sur tache/S49-P16-decoupage.
3. Une sous-étape faite mais non cochée par cette commande est considérée comme non faite : l'IA suivante la refera. Tu ne coches jamais une case à la main.
4. Tu ne modifies jamais SUIVI.md : il ne change qu'à la fusion, sous le verrou de main. Plusieurs IA le lisent en même temps ; aucune ne l'écrit hors de ce verrou.
5. Avant de cocher la dernière sous-étape R : « Statut : TERMINÉ » dans rapports/S49.md, puis git add.
6. Poussée refusée et non rattrapée par la commande : ne force jamais ; git pull --rebase origin tache/S49-P16-decoupage, puis relance la commande.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (docs/construction/v1.md, prompt de découpage)
Tu découpes la phase P16 du projet GODOT_DEV_MAPPER en tâches exécutables, au format des fiches de docs/construction/etape-4.md.

ENTRÉES : docs/plan-directeur.md (§3, capacités {CAP} ; §9, porte de la phase) ; docs/construction/v1.md, section P16 ; docs/DECISIONS.md ; docs/spikes/ ; PROJECT_STATE.md (budget consommé, taux de réussite par IA) ; docs/revues/revue-poc.md.

PRODUIS docs/construction/v1-P16.md :
- objectif, obligations, méthodologie, points de contrôle et cheminement d'amélioration de la phase, précisés par les résultats du POC ;
- de 4 à 12 tâches. Chacune avec : modèle, autonomie, dépendances, fichiers autorisés, pack de contexte, contrôles exécutables dont au moins une contre-épreuve, et prompt de réalisation rempli à partir du prompt universel.

RÈGLES
- Une tâche tient en 1 à 3 h de travail agent et en 1 h de relecture humaine au plus.
- Une tâche qui touche un format persisté, le protocole ou une façade est vérifiée par IA 1.
- Les contrats et leurs tests précèdent l'implémentation, comme à l'étape 3. Une tâche qui révise un contrat liste explicitement `docs/CONTRACTS.md`, `contracts/` et `tests/contract/` dans ses fichiers autorisés ; IA 1 la réalise, IA 3 la vérifie, tu la valides.
- Chaque tâche précise les marqueurs de `tests/pending/` qu'elle crée ou supprime, et les scripts de `tools/ci/checks.d/` qu'elle ajoute. Aucune ne modifie `PROJECT_STATE.md` ni `docs/DECISIONS.md`.
- Le total reste dans le budget de la phase ({budget} h humaines). Sinon, tu signales le dépassement et proposes quoi retirer.
- Ne réalise aucune tâche.
- Toute tâche qui produit une explication, une comparaison ou une suggestion inclut un contrôle qui vérifie que chaque affirmation affichée renvoie à une preuve.
TRAVAIL TECHNIQUE — fin de la copie exacte du guide

ADAPTATIONS DU MODE AUTONOME
- Le découpage existe déjà : les fiches suivi/S49.1-… à suivi/S49.10-…, listées dans cette fiche. Tu le revois au lieu de partir de zéro ; le document à produire reste celui du guide, docs/construction/v1-P16.md.
- Budget : traduis les heures humaines de la phase en créneaux d'IA avec le ratio observé au POC (docs/revues/revue-poc.md).
- Tu gardes une tâche telle quelle si rien ne la contredit. Tu la modifies si un résultat l'exige (décision de spike, contrat révisé, outil renommé, mesure), en le citant.
- Une tâche ajoutée : nouvelle fiche suivi/S49.<k>-<nom>.md depuis suivi/_modele-tache.md, toutes sections remplies, sous-étapes au format « ⟶ cocher ». Une tâche retirée : sa fiche reste, avec la raison en tête ; le vérificateur retire sa ligne de SUIVI.md à la fusion.
- Prérequis : S49 pour toute tâche, plus les tâches dont elle dépend vraiment, y compris d'une autre phase quand deux phases parallèles touchent le même fichier (contrat révisé, flow_trace.gd, envelope.gd et codec, tools/deps_rules.json, branche du banc). Deux tâches indépendantes ne modifient jamais le même fichier.
- Un nouveau contrat va dans son propre fichier docs/contracts/C-xx.md ; une révision de C-01 à C-07 reste dans docs/CONTRACTS.md, avec sa version cible écrite dans la fiche. Une nouvelle vue est un onglet ui/vues/<nom>/ (convention de S39.12), jamais une modification de plugin.gd ou du panneau principal.
- Répartition : réalisation par IA 2, sauf contrat, protocole, façade ou format persisté (IA 1) ; vérification par IA 3, sauf ces mêmes sujets (IA 1, ou IA 3 si IA 1 est l'auteur).
- Contrôle final : python3 suivi/outil.py verifier → OK, une fois SUIVI.md mis à jour à la fusion.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche ; après chacune, git add puis python3 suivi/outil.py cocher S49 R<k> --ia <n>.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Chaque sous-étape faite est cochée par `cocher`. Complète rapports/S49.md (sorties, « Passation » en cinq lignes au plus), git add, git commit, git push origin HEAD:tache/S49-P16-decoupage.
- git status ne montre aucune modification non commitée ; rien ne reste non poussé.

FORMAT DE rapports/S49.md (créé par prendre ; tu le complètes)
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

Après chaque sous-étape : `git add` de ses fichiers, puis `python3 suivi/outil.py cocher S49 R<k> --ia <n>` (coche, signe, commite, pousse).

- [ ] R0 Prise en charge : `python3 suivi/outil.py prendre S49 --ia <n>` (prérequis cochés dans `SUIVI.md` : S47.P, S48.P ; branche `tache/S49-P16-decoupage` créée ou reprise ; `rapports/S49.md` au statut EN COURS) ⟶ cochée par `prendre`
- [ ] R1 Lire `docs/revues/revue-poc.md`, `docs/DECISIONS.md`, `docs/spikes/`, `PROJECT_STATE.md` et les rapports des phases précédentes ; noter les faits qui touchent la phase. ⟶ cocher S49 R1
- [ ] R2 Relire chaque fiche du découpage provisoire (S49.1, S49.2, S49.3, S49.4, S49.5, S49.6, S49.7, S49.8, S49.9, S49.10) et décider : garder, préciser, retirer ou remplacer, avec la raison. ⟶ cocher S49 R2
- [ ] R3 Appliquer les décisions aux fiches ; créer les fiches des tâches ajoutées. ⟶ cocher S49 R3
- [ ] R4 Écrire `docs/construction/v1-P16.md`. ⟶ cocher S49 R4
- [ ] R5 Écrire dans le rapport les changements à porter dans `SUIVI.md` (lignes, prérequis, rôles), ou « aucun changement ». ⟶ cocher S49 R5
- [ ] R6 Contrôles finaux : chaque fiche gardée, modifiée ou ajoutée a toutes ses sections ; budget respecté ; « Statut : TERMINÉ » dans le rapport ⟶ cocher S49 R6

## Prompt de vérification

```text
Tu vérifies l'unité S49 « P16 Durcissement et documentation : revue du découpage » du projet GODOT_DEV_MAPPER. Vérification prévue : IA 3 (vérification). Ton numéro d'IA est celui du prompt de créneau. Tu n'es jamais un auteur de l'unité : la commande de prise le contrôle.

PRISE, depuis ton clone principal
python3 suivi/outil.py prendre S49 --ia <n> --verification
- « VÉRIFICATION PRISE » : copie neuve ../verif-S49-P16-decoupage créée sur origin/tache/S49-P16-decoupage, verdict EN COURS écrit, V1 cochée. cd ../verif-S49-P16-decoupage : toute la vérification se fait dans ce dossier.
- « REFUSÉ » : une autre IA vérifie déjà, tu es auteur, ou l'unité n'est pas terminée : reviens au prompt de créneau.
- Créneau fini avant le verdict : au créneau suivant, etat te propose la même commande ; elle recrée la copie (« VÉRIFICATION REPRISE ») et tu reprends à la première case V ouverte.
GODOT : même procédure que le prompt de réalisation.
Tu ne modifies aucun fichier de l'unité. Tu écris seulement ton verdict et tes cases V.

TRACE OBLIGATOIRE : après chaque sous-étape V, git add du fichier de verdict, puis python3 suivi/outil.py cocher S49 <V…> --ia <n>. Pour la dernière : --verdict ACCEPTÉE ou --verdict REFUSÉE, identique à la ligne « Verdict » du fichier. Une sous-étape non cochée par cette commande est considérée comme non faite.

1. TRAÇABILITÉ. Chaque case R cochée est signée « — IA n · date » et a son commit sur la branche (git log --oneline origin/main..HEAD). Case cochée sans travail prouvé dans le rapport : refus.
2. PÉRIMÈTRE. git diff --name-only origin/main...HEAD. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S49*.md et suivi/S49-P16-decoupage.md. Tout autre fichier : refus.
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

VERDICT dans rapports/S49-verif-<tentative>.md (créé par la prise) :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte

SI ACCEPTÉE — FUSION, depuis ton clone principal (cd hors de ../verif-S49-P16-decoupage)
1. python3 suivi/outil.py fusionner S49 --ia <n>
   Elle trouve Godot (--godot, $GODOT, cache du bloc GODOT ou tools/ci/fetch_godot.sh ; sans Godot : REFUSÉ, verdict inchangé), prend le verrou de main (et attend s'il est pris), revérifie l'unité, fusionne dans ../fusion-S49-P16-decoupage, lance run_all_checks.sh, coche la ligne dans SUIVI.md et la case F1. Si les contrôles échouent : verdict passé à REFUSÉE, main inchangée, verrou rendu ; arrête-toi sur cette unité. La fusion te revient parce que tu as signé le verdict ; une autre IA ne la fait qu'après 12 h.
2. cd ../fusion-S49-P16-decoupage ; fais les sous-étapes F suivantes de la fiche, et coche chacune : python3 suivi/outil.py cocher S49 F<k> --ia <n> (commit local, sans poussée).
   Dans ../fusion-S49-P16-decoupage : porte dans SUIVI.md les changements du rapport (lignes ajoutées sous S49, retirées, prérequis, rôles réalise et vérifie) ; python3 suivi/outil.py verifier → OK (il compare rôles et prérequis de chaque fiche à sa ligne) ; git add SUIVI.md ; puis coche F2.
3. python3 suivi/outil.py publier S49 --ia <n> : dernière case cochée, verifier relancé, main poussée, branche supprimée, verrou rendu.
SI REFUSÉE : arrête-toi sur cette unité ; son auteur la reprendra avec prendre.
```

## Sous-étapes de vérification

Dans `../verif-S49-P16-decoupage`, après chaque sous-étape : `git add` du verdict, puis `python3 suivi/outil.py cocher S49 V<k> --ia <n>`.

- [ ] V1 Prise en charge : `python3 suivi/outil.py prendre S49 --ia <n> --verification` (pas un auteur ; copie neuve `../verif-S49-P16-decoupage` sur `origin/tache/S49-P16-decoupage` ; verdict EN COURS) ⟶ cochée par `prendre`
- [ ] V2 Traçabilité : chaque case R cochée porte une signature « — IA n · date » et un commit sur la branche (`git log --oneline origin/main..HEAD`) ⟶ cocher S49 V2
- [ ] V3 Chaque changement cite le fait du POC ou d'une phase précédente qui l'impose. ⟶ cocher S49 V3
- [ ] V4 Budget de la phase respecté, ou dépassement signalé avec une proposition de retrait. ⟶ cocher S49 V4
- [ ] V5 Chaque fiche gardée, modifiée ou ajoutée : toutes les sections, au moins une contre-épreuve, fichiers autorisés précis, sous-étapes au format « ⟶ cocher ». ⟶ cocher S49 V5
- [ ] V6 Prérequis réels, sans cycle ; tâches indépendantes sans fichier commun. ⟶ cocher S49 V6
- [ ] V7 Verdict écrit dans `rapports/S49-verif-<tentative>.md` ⟶ cocher S49 V7 --verdict ACCEPTÉE ou --verdict REFUSÉE

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

F1 et la dernière se cochent par `fusionner` et `publier` ; les autres, dans `../fusion-S49-P16-decoupage`, par `python3 suivi/outil.py cocher S49 F<k> --ia <n>` (commit local).

- [ ] F1 Fusion, depuis le clone principal : `python3 suivi/outil.py fusionner S49 --ia <n>` : Godot trouvé seul (--godot, $GODOT, cache du bloc GODOT ou fetch_godot.sh), verrou de `main`, fusion `--no-ff` dans `../fusion-S49-P16-decoupage`, `tools/ci/run_all_checks.sh` sur `main` → ALL_CHECKS OK s'il existe (sinon fusion annulée et verdict passé à REFUSÉE), ligne **S49** cochée dans `SUIVI.md` ⟶ cochée par `fusionner`
- [ ] F2 Changements du rapport portés dans `SUIVI.md` (lignes ajoutées sous **S49**, retirées, prérequis, rôles) ; `python3 suivi/outil.py verifier` → OK ⟶ cocher S49 F2
- [ ] F3 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette ⟶ cocher S49 F3
- [ ] F4 Publication : `python3 suivi/outil.py publier S49 --ia <n>` (verifier OK, `main` poussée, branche `tache/S49-P16-decoupage` supprimée, verrou rendu) ⟶ cochée par `publier`

## Pour la recette

Rien de propre à cette unité.
