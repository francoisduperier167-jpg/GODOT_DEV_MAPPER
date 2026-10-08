# S44 — P11 Data Flow : origine et usages d'un paramètre : revue du découpage

> Fiche d'exécution du mode autonome. Chaque case se coche avec `python3 suivi/outil.py cocher S44 <sous-étape> --ia <n>`, juste après la sous-étape : la commande vérifie l'ordre et l'identité de l'IA, signe la case (IA, date, heure UTC), commite et pousse. Une sous-étape non cochée par cette commande est considérée comme non faite. Règles : `docs/construction/sequence.md`. Avancement : `SUIVI.md` et `suivi/tableau.html`.

| Champ | Valeur |
| --- | --- |
| Réalise | IA 1 (conception) |
| Vérifie | IA 3 (vérification), jamais un auteur de l'unité |
| Piste | V.C Phase P11 : S44 → S44.P (unité 1 sur 2) |
| Commence après | S41.P (cochée dans `SUIVI.md`) |
| Indépendante de | S42, S42.P, S43, S43.P, S45, S45.P, S47, S42.1, S42.2, S42.3, S42.4, S42.5, S42.6, S42.7, et 13 autres (voir SUIVI.md) |
| Branche | `tache/S44-P11-decoupage` |
| Fiche de conception | `docs/construction/v1.md`, section P11 |
| Estimation | 1 créneau |

**Séquentiel ou indépendant.** Cette unité est la 1re de la piste V.C « Phase P11 », dont les unités se font à la suite. Les autres pistes de la section (V.A, V.B, V.D) avancent en même temps, chacune de son côté. Elle attend S41.P, hors de la piste. S44.P l'attendra. Les sous-étapes de cette fiche se font dans l'ordre, l'une après l'autre. L'unité peut avancer en même temps que toute unité de la ligne « Indépendante de » : aucune des deux n'attend l'autre, et elles ne modifient pas les mêmes fichiers.

## Ce qu'il faut faire

- Revoir le découpage provisoire de la phase P11 : 9 tâches (S44.1, S44.2, S44.3, S44.4, S44.5, S44.6, S44.7, S44.8, S44.9), écrites avant le POC d'après `docs/construction/v1.md` et le plan directeur.
- Le confronter aux résultats du POC (`docs/revues/revue-poc.md`), aux décisions (`docs/DECISIONS.md`), aux spikes, aux mesures et aux rapports des phases précédentes.
- Pour chaque tâche : la garder, la préciser (fiche modifiée), la retirer, ou la remplacer ; ajouter les tâches manquantes depuis `suivi/_modele-tache.md`. Total dans le budget de la phase : 12 à 20 h humaines.
- Écrire `docs/construction/v1-P11.md` : objectif, obligations, méthodologie, points de contrôle et cheminement d'amélioration de la phase, précisés par les résultats ; tableau des tâches retenues, avec la raison de chaque changement.
- Écrire dans le rapport les changements à porter dans `SUIVI.md` : lignes ajoutées sous **S44**, lignes retirées, prérequis modifiés, rôles modifiés (réalise, vérifie) ; ou « aucun changement ». La fiche et sa ligne de `SUIVI.md` doivent dire la même chose : `verifier` compare rôles et prérequis.

## Fichiers autorisés

`docs/construction/v1-P11.md`, `suivi/S44.*-*.md` (fiches des tâches de la phase, sauf la porte S44.P), `rapports/S44*.md`.

## Tâches du découpage provisoire

- **S44.1** · Contrat C-14 : origine et usages d'un paramètre · réalise IA 1 · vérifie IA 3 · après S44, S42.1 · `suivi/S44.1-contrat-c14-parametres.md`
- **S44.2** · Déclarations de paramètres et valeurs par défaut · réalise IA 2 · vérifie IA 3 · après S44.1 · `suivi/S44.2-declarations-parametres.md`
- **S44.3** · Valeurs des ressources .tres et .res · réalise IA 2 · vérifie IA 1 · après S44.1 · `suivi/S44.3-valeurs-ressources.md`
- **S44.4** · Surcharges de paramètres dans les scènes · réalise IA 2 · vérifie IA 3 · après S44.1 · `suivi/S44.4-surcharges-scenes.md`
- **S44.5** · Lecteurs et écrivains statiques d'un paramètre · réalise IA 2 · vérifie IA 3 · après S44.2 · `suivi/S44.5-lecteurs-ecrivains.md`
- **S44.6** · Valeur observée : écritures instrumentées · réalise IA 2 · vérifie IA 1 · après S44.1, S42.6 · `suivi/S44.6-valeur-observee.md`
- **S44.7** · Projection de l'origine d'un paramètre · réalise IA 2 · vérifie IA 3 · après S44.3, S44.4, S44.5, S44.6 · `suivi/S44.7-projection-origine.md`
- **S44.8** · Vue Data Flow (parcours J4) · réalise IA 2 · vérifie IA 3 · après S44.7 · `suivi/S44.8-vue-data-flow.md`
- **S44.9** · Paramètre du banc d'essai suivi de bout en bout · réalise IA 3 · vérifie IA 2 · après S44.7 · `suivi/S44.9-parametre-banc.md`

## Prompt de réalisation

```text
Tu réalises l'unité S44 « P11 Data Flow : origine et usages d'un paramètre : revue du découpage » du projet GODOT_DEV_MAPPER (plugin pour Godot 4.7.2, GDScript), en mode autonome : aucun humain ne répondra pendant ton créneau.
Réalisation prévue : IA 1 (conception) ; vérification : IA 3 (vérification). Ton numéro d'IA est celui que te donne le prompt de créneau : tu le passes à --ia, et il signe chaque case que tu coches.

AVANT TOUT, depuis ton clone principal du dépôt
1. Lis REGLES_AGENTS.md s'il existe, puis cette fiche : suivi/S44-P11-decoupage.md.
2. python3 suivi/outil.py prendre S44 --ia <n>
   - « PRISE » ou « REPRISE » : tu es sur la branche tache/S44-P11-decoupage ; commence à la sous-étape affichée. Ne refais pas ce qui est coché, sauf si un contrôle prouve que c'est faux.
   - « REFUSÉ » : l'unité n'est pas pour toi maintenant (déjà prise par une autre IA, S41.P non cochée, autre IA prévue) : reviens au prompt de créneau et choisis autre chose.

RÈGLES NON NÉGOCIABLES
- Tu ne modifies que les fichiers autorisés de la fiche, plus rapports/S44.md et les cases de suivi/S44-P11-decoupage.md. Si un autre fichier doit changer : statut QUESTION, avec la raison.
- Tu ne modifies jamais tests/contract/, contracts/, docs/CONTRACTS.md, docs/construction/, SUIVI.md, PROJECT_STATE.md ni docs/DECISIONS.md, sauf si la fiche les autorise.
- Avant d'utiliser une API Godot dont tu n'es pas certain en 4.7.2, écris un script de trois lignes qui l'appelle et exécute-le. Une API non vérifiée n'entre pas dans le code.
- Tu n'affaiblis jamais un test ou un contrôle pour le faire passer.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée : tu colles sa sortie réelle dans le rapport.
- Tu n'ajoutes à Git que des fichiers nommés : jamais git add -A sans relire git status. Tu ne pousses jamais avec --force.
- Deux échecs au même contrôle : statut ESCALADE, avec ton diagnostic.
- Une décision réservée à l'humain (docs/construction/sequence.md §5) : arrêt obligatoire, rien d'autre : python3 suivi/outil.py arreter --ia <n> --unite S44 --raison "<raison>", puis fin du créneau.

TRACE OBLIGATOIRE, après CHAQUE sous-étape et avant la suivante
1. git add <les fichiers de la sous-étape> (jamais git add -A).
2. python3 suivi/outil.py cocher S44 <sous-étape> --ia <n>
   La commande vérifie l'ordre des cases et ton identité, coche la case dans suivi/S44-P11-decoupage.md, la signe (IA, date, heure UTC), commite et pousse sur tache/S44-P11-decoupage.
3. Une sous-étape faite mais non cochée par cette commande est considérée comme non faite : l'IA suivante la refera. Tu ne coches jamais une case à la main.
4. Tu ne modifies jamais SUIVI.md : il ne change qu'à la fusion, sous le verrou de main. Plusieurs IA le lisent en même temps ; aucune ne l'écrit hors de ce verrou.
5. Avant de cocher la dernière sous-étape R : « Statut : TERMINÉ » dans rapports/S44.md, puis git add.
6. Poussée refusée et non rattrapée par la commande : ne force jamais ; git pull --rebase origin tache/S44-P11-decoupage, puis relance la commande.

TRAVAIL TECHNIQUE — début de la copie exacte du guide (docs/construction/v1.md, prompt de découpage)
Tu découpes la phase P11 du projet GODOT_DEV_MAPPER en tâches exécutables, au format des fiches de docs/construction/etape-4.md.

ENTRÉES : docs/plan-directeur.md (§3, capacités {CAP} ; §9, porte de la phase) ; docs/construction/v1.md, section P11 ; docs/DECISIONS.md ; docs/spikes/ ; PROJECT_STATE.md (budget consommé, taux de réussite par IA) ; docs/revues/revue-poc.md.

PRODUIS docs/construction/v1-P11.md :
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
- Le découpage existe déjà : les fiches suivi/S44.1-… à suivi/S44.9-…, listées dans cette fiche. Tu le revois au lieu de partir de zéro ; le document à produire reste celui du guide, docs/construction/v1-P11.md.
- Budget : traduis les heures humaines de la phase en créneaux d'IA avec le ratio observé au POC (docs/revues/revue-poc.md).
- Tu gardes une tâche telle quelle si rien ne la contredit. Tu la modifies si un résultat l'exige (décision de spike, contrat révisé, outil renommé, mesure), en le citant.
- Une tâche ajoutée : nouvelle fiche suivi/S44.<k>-<nom>.md depuis suivi/_modele-tache.md, toutes sections remplies, sous-étapes au format « ⟶ cocher ». Une tâche retirée : sa fiche reste, avec la raison en tête ; le vérificateur retire sa ligne de SUIVI.md à la fusion.
- Prérequis : S44 pour toute tâche, plus les tâches dont elle dépend vraiment, y compris d'une autre phase quand deux phases parallèles touchent le même fichier (contrat révisé, flow_trace.gd, envelope.gd et codec, tools/deps_rules.json, branche du banc). Deux tâches indépendantes ne modifient jamais le même fichier.
- Un nouveau contrat va dans son propre fichier docs/contracts/C-xx.md ; une révision de C-01 à C-07 reste dans docs/CONTRACTS.md, avec sa version cible écrite dans la fiche. Une nouvelle vue est un onglet ui/vues/<nom>/ (convention de S39.12), jamais une modification de plugin.gd ou du panneau principal.
- Répartition : réalisation par IA 2, sauf contrat, protocole, façade ou format persisté (IA 1) ; vérification par IA 3, sauf ces mêmes sujets (IA 1, ou IA 3 si IA 1 est l'auteur).
- Contrôle final : python3 suivi/outil.py verifier → OK, une fois SUIVI.md mis à jour à la fusion.

SOUS-ÉTAPES : exécute dans l'ordre les sous-étapes R de la fiche ; après chacune, git add puis python3 suivi/outil.py cocher S44 R<k> --ia <n>.

FIN DE CRÉNEAU, même si l'unité n'est pas finie
- Chaque sous-étape faite est cochée par `cocher`. Complète rapports/S44.md (sorties, « Passation » en cinq lignes au plus), git add, git commit, git push origin HEAD:tache/S44-P11-decoupage.
- git status ne montre aucune modification non commitée ; rien ne reste non poussé.

FORMAT DE rapports/S44.md (créé par prendre ; tu le complètes)
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

Après chaque sous-étape : `git add` de ses fichiers, puis `python3 suivi/outil.py cocher S44 R<k> --ia <n>` (coche, signe, commite, pousse).

- [ ] R0 Prise en charge : `python3 suivi/outil.py prendre S44 --ia <n>` (prérequis cochés dans `SUIVI.md` : S41.P ; branche `tache/S44-P11-decoupage` créée ou reprise ; `rapports/S44.md` au statut EN COURS) ⟶ cochée par `prendre`
- [ ] R1 Lire `docs/revues/revue-poc.md`, `docs/DECISIONS.md`, `docs/spikes/`, `PROJECT_STATE.md` et les rapports des phases précédentes ; noter les faits qui touchent la phase. ⟶ cocher S44 R1
- [ ] R2 Relire chaque fiche du découpage provisoire (S44.1, S44.2, S44.3, S44.4, S44.5, S44.6, S44.7, S44.8, S44.9) et décider : garder, préciser, retirer ou remplacer, avec la raison. ⟶ cocher S44 R2
- [ ] R3 Appliquer les décisions aux fiches ; créer les fiches des tâches ajoutées. ⟶ cocher S44 R3
- [ ] R4 Écrire `docs/construction/v1-P11.md`. ⟶ cocher S44 R4
- [ ] R5 Écrire dans le rapport les changements à porter dans `SUIVI.md` (lignes, prérequis, rôles), ou « aucun changement ». ⟶ cocher S44 R5
- [ ] R6 Contrôles finaux : chaque fiche gardée, modifiée ou ajoutée a toutes ses sections ; budget respecté ; « Statut : TERMINÉ » dans le rapport ⟶ cocher S44 R6

## Prompt de vérification

```text
Tu vérifies l'unité S44 « P11 Data Flow : origine et usages d'un paramètre : revue du découpage » du projet GODOT_DEV_MAPPER. Vérification prévue : IA 3 (vérification). Ton numéro d'IA est celui du prompt de créneau. Tu n'es jamais un auteur de l'unité : la commande de prise le contrôle.

PRISE, depuis ton clone principal
python3 suivi/outil.py prendre S44 --ia <n> --verification
- « VÉRIFICATION PRISE » : copie neuve ../verif-S44-P11-decoupage créée sur origin/tache/S44-P11-decoupage, verdict EN COURS écrit, V1 cochée. cd ../verif-S44-P11-decoupage : toute la vérification se fait dans ce dossier.
- « REFUSÉ » : une autre IA vérifie déjà, tu es auteur, ou l'unité n'est pas terminée : reviens au prompt de créneau.
- Créneau fini avant le verdict : au créneau suivant, etat te propose la même commande ; elle recrée la copie (« VÉRIFICATION REPRISE ») et tu reprends à la première case V ouverte.
GODOT : même procédure que le prompt de réalisation.
Tu ne modifies aucun fichier de l'unité. Tu écris seulement ton verdict et tes cases V.

TRACE OBLIGATOIRE : après chaque sous-étape V, git add du fichier de verdict, puis python3 suivi/outil.py cocher S44 <V…> --ia <n>. Pour la dernière : --verdict ACCEPTÉE ou --verdict REFUSÉE, identique à la ligne « Verdict » du fichier. Une sous-étape non cochée par cette commande est considérée comme non faite.

1. TRAÇABILITÉ. Chaque case R cochée est signée « — IA n · date » et a son commit sur la branche (git log --oneline origin/main..HEAD). Case cochée sans travail prouvé dans le rapport : refus.
2. PÉRIMÈTRE. git diff --name-only origin/main...HEAD. Autorisés : les « Fichiers autorisés » de la fiche, rapports/S44*.md et suivi/S44-P11-decoupage.md. Tout autre fichier : refus.
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

VERDICT dans rapports/S44-verif-<tentative>.md (créé par la prise) :
- Verdict : ACCEPTÉE | REFUSÉE
- Contrôles relancés : commande, code, attendu, obtenu
- Contre-épreuves : sabotage, contrôle, détecté oui ou non
- Problèmes : numérotés, avec fichier, ligne et preuve ; « aucun » sinon
- Doutes non bloquants : liste courte

SI ACCEPTÉE — FUSION, depuis ton clone principal (cd hors de ../verif-S44-P11-decoupage)
1. python3 suivi/outil.py fusionner S44 --ia <n>
   Elle trouve Godot (--godot, $GODOT, cache du bloc GODOT ou tools/ci/fetch_godot.sh ; sans Godot : REFUSÉ, verdict inchangé), prend le verrou de main (et attend s'il est pris), revérifie l'unité, fusionne dans ../fusion-S44-P11-decoupage, lance run_all_checks.sh, coche la ligne dans SUIVI.md et la case F1. Si les contrôles échouent : verdict passé à REFUSÉE, main inchangée, verrou rendu ; arrête-toi sur cette unité. La fusion te revient parce que tu as signé le verdict ; une autre IA ne la fait qu'après 12 h.
2. cd ../fusion-S44-P11-decoupage ; fais les sous-étapes F suivantes de la fiche, et coche chacune : python3 suivi/outil.py cocher S44 F<k> --ia <n> (commit local, sans poussée).
   Dans ../fusion-S44-P11-decoupage : porte dans SUIVI.md les changements du rapport (lignes ajoutées sous S44, retirées, prérequis, rôles réalise et vérifie) ; python3 suivi/outil.py verifier → OK (il compare rôles et prérequis de chaque fiche à sa ligne) ; git add SUIVI.md ; puis coche F2.
3. python3 suivi/outil.py publier S44 --ia <n> : dernière case cochée, verifier relancé, main poussée, branche supprimée, verrou rendu.
SI REFUSÉE : arrête-toi sur cette unité ; son auteur la reprendra avec prendre.
```

## Sous-étapes de vérification

Dans `../verif-S44-P11-decoupage`, après chaque sous-étape : `git add` du verdict, puis `python3 suivi/outil.py cocher S44 V<k> --ia <n>`.

- [ ] V1 Prise en charge : `python3 suivi/outil.py prendre S44 --ia <n> --verification` (pas un auteur ; copie neuve `../verif-S44-P11-decoupage` sur `origin/tache/S44-P11-decoupage` ; verdict EN COURS) ⟶ cochée par `prendre`
- [ ] V2 Traçabilité : chaque case R cochée porte une signature « — IA n · date » et un commit sur la branche (`git log --oneline origin/main..HEAD`) ⟶ cocher S44 V2
- [ ] V3 Chaque changement cite le fait du POC ou d'une phase précédente qui l'impose. ⟶ cocher S44 V3
- [ ] V4 Budget de la phase respecté, ou dépassement signalé avec une proposition de retrait. ⟶ cocher S44 V4
- [ ] V5 Chaque fiche gardée, modifiée ou ajoutée : toutes les sections, au moins une contre-épreuve, fichiers autorisés précis, sous-étapes au format « ⟶ cocher ». ⟶ cocher S44 V5
- [ ] V6 Prérequis réels, sans cycle ; tâches indépendantes sans fichier commun. ⟶ cocher S44 V6
- [ ] V7 Verdict écrit dans `rapports/S44-verif-<tentative>.md` ⟶ cocher S44 V7 --verdict ACCEPTÉE ou --verdict REFUSÉE

## Sous-étapes de fusion (vérificateur, si ACCEPTÉE)

F1 et la dernière se cochent par `fusionner` et `publier` ; les autres, dans `../fusion-S44-P11-decoupage`, par `python3 suivi/outil.py cocher S44 F<k> --ia <n>` (commit local).

- [ ] F1 Fusion, depuis le clone principal : `python3 suivi/outil.py fusionner S44 --ia <n>` : Godot trouvé seul (--godot, $GODOT, cache du bloc GODOT ou fetch_godot.sh), verrou de `main`, fusion `--no-ff` dans `../fusion-S44-P11-decoupage`, `tools/ci/run_all_checks.sh` sur `main` → ALL_CHECKS OK s'il existe (sinon fusion annulée et verdict passé à REFUSÉE), ligne **S44** cochée dans `SUIVI.md` ⟶ cochée par `fusionner`
- [ ] F2 Changements du rapport portés dans `SUIVI.md` (lignes ajoutées sous **S44**, retirées, prérequis, rôles) ; `python3 suivi/outil.py verifier` → OK ⟶ cocher S44 F2
- [ ] F3 `PROJECT_STATE.md` (s'il existe) : mesures de l'unité ; éléments « Pour la recette » du rapport ajoutés à la liste de recette ⟶ cocher S44 F3
- [ ] F4 Publication : `python3 suivi/outil.py publier S44 --ia <n>` (verifier OK, `main` poussée, branche `tache/S44-P11-decoupage` supprimée, verrou rendu) ⟶ cochée par `publier`

## Pour la recette

Rien de propre à cette unité.
