# Déroulé séquentiel — mode autonome

Révision SQ-0.1 · statut : **proposé** · 8 octobre 2026 · fondé sur PD-0.5 (décision D-09), GC-0.4, OR-0.5 et MC-0.5

Ce document fixe l'ordre d'exécution quand trois IA construisent le projet à tour de rôle, sans humain jusqu'à la recette finale. Il dit qui réalise et qui vérifie chaque unité, comment un créneau passe la main au suivant, et ce qui change dans le guide quand personne n'est là pour trancher.

La fiche de chaque tâche reste celle du guide : objectif, fichiers autorisés, contrôles, contre-épreuves et prompts. En cas d'écart, ce document prime sur l'ordre et sur les rôles ; le guide prime sur le contenu d'une tâche.

## 1. Principes

- **Une seule file.** Une unité commence quand la précédente est acceptée et fusionnée. Aucune unité ne tourne en parallèle.
- **Trois rôles, trois IA.** L'auteur d'une unité ne la vérifie jamais.
- **Le dépôt distant est la mémoire commune.** Chaque IA arrive sans souvenir du créneau précédent. Elle lit `main`, les branches `tache/{ID}` et les rapports `rapports/{ID}*.md`.
- **Fichiers partagés.** `PROJECT_STATE.md` et `docs/DECISIONS.md` ne changent qu'à la fusion, sur `main`, par l'IA qui fusionne.
- **Décisions prises à ta place.** Chacune est écrite dans `docs/DECISIONS.md` avec le statut « adoptée par défaut » et sa date. Tu les confirmes ou tu les changes à la recette.
- **Personne ne t'attend**, sauf aux arrêts obligatoires (§6).

## 2. Les trois rôles

| Rôle | Réalise | Vérifie | Affectation proposée |
| --- | --- | --- | --- |
| Concepteur | Décisions, squelettes, spikes, contrats, portes d'étape, découpage des phases, revues | Façades, protocole, formats persistés, CI | Claude Opus 5.5 |
| Développeur | Implémentation, outillage, interface, essais sous écran virtuel | Rien | Deuxième IA : Sonnet dans le plan ; toute autre IA de code que tu utilises |
| Vérificateur | Choix du banc d'essai, injection des bugs de la mesure de valeur | Tout le reste, dont les contrats et les spikes du concepteur | Gemini |

Le plan prévoyait aussi Qwen3.8-27B en local. Son installation (T00) exige ta machine : en mode autonome, il n'est pas utilisé et ses tâches vont au développeur. Tu pourras l'ajouter entre deux phases.

Si la deuxième IA n'est pas Sonnet, rien ne change dans les fiches : « Sonnet » et « Qwen » y désignent le rôle de développeur.

## 3. Créneaux et passation

Chaque IA tient deux créneaux par jour, soit six créneaux par jour. L'ordre de passage n'importe pas : chaque créneau repart de l'état du dépôt.

**État d'une unité**, lu dans le dépôt :

| État | Comment le reconnaître |
| --- | --- |
| Acceptée | Ligne « Acceptée » dans le tableau de `PROJECT_STATE.md` sur `main` |
| À réaliser | Aucune branche `tache/{ID}`, ou dernier verdict « REFUSÉE » |
| À vérifier | `rapports/{ID}.md` au statut TERMINÉ sur `tache/{ID}`, sans verdict pour cette tentative |
| Bloquée | Statut QUESTION ou ESCALADE dans le rapport, ou `rapports/ARRET.md` sur `main` |

**Fusion**, par le vérificateur qui accepte :
1. `git switch main`, puis `git merge --no-ff tache/{ID}`.
2. `tools/ci/run_all_checks.sh` sur `main`, dès que T03 l'a créé.
3. Si les contrôles sont verts : un commit sur `main` met à jour `PROJECT_STATE.md`. Il note le statut, l'auteur, le vérificateur, les créneaux consommés et les tentatives. Puis `git push`.
4. Si les contrôles sont rouges : `git reset --hard ORIG_HEAD` avant tout envoi, puis verdict « REFUSÉE (fusion) » sur la branche.

## 4. Prompt de créneau

C'est le seul message que reçoit une IA au début de son créneau.

```text
Tu es {NOM DE L'IA}, au rôle {Concepteur | Développeur | Vérificateur}, pour un créneau du projet GODOT_DEV_MAPPER. Tu n'as aucune mémoire des créneaux précédents : le dépôt est ta seule source.

0. ARRÊT. git fetch --all. Si rapports/ARRET.md existe sur main, lis-le, ne fais rien d'autre, et termine en citant sa raison.

1. ÉTAT. Lis REGLES_AGENTS.md (s'il existe), docs/construction/sequence.md, puis PROJECT_STATE.md sur main (s'il existe). L'unité courante est la première de la séquence (§5, puis §7) qui n'est pas « Acceptée ». Détermine son état avec le tableau du §3.

2. VÉRIFIER. Si l'unité courante est à vérifier, que tu n'en es pas l'auteur et que ton rôle est dans sa colonne « Vérifie » :
   - crée une copie de travail neuve sur tache/{ID} ;
   - applique le prompt universel de vérification de docs/construction/README.md et les adaptations du §5 pour cette unité ;
   - écris ton verdict dans rapports/{ID}-verif-{tentative}.md, sur la branche, et pousse-le.
   Si le rôle prévu n'est pas passé depuis deux créneaux, tout rôle autre que l'auteur peut vérifier.

3. FUSIONNER. Si ton verdict est ACCEPTÉE, fusionne selon le §3 de sequence.md.

4. RÉALISER. Prends l'unité courante si elle est à réaliser et que ton rôle est dans sa colonne « Réalise ». Une unité du développeur peut être prise par une autre IA si le développeur n'est pas passé depuis deux créneaux.
   - Pars de main, ou de la branche existante après un refus.
   - Applique le prompt universel de réalisation, la fiche de la tâche dans le guide, et les adaptations du §5.
   - Écris rapports/{ID}.md au format du rapport final, avec « Auteur : {NOM DE L'IA} ».
   - Pousse tache/{ID}.

5. PASSATION. Avant de finir, ajoute à ton rapport ou à ton verdict une section « Passation » de cinq lignes au plus : ce qui est fait, ce qui reste, le rôle attendu au créneau suivant. Ne laisse rien de non poussé.

RÈGLES
- Tu ne vérifies jamais ton propre travail.
- Tu ne modifies PROJECT_STATE.md et docs/DECISIONS.md qu'à l'étape 3, ou quand une adaptation du §5 le demande.
- Un arrêt obligatoire du §6 : écris rapports/ARRET.md sur main (raison, unité, preuve, ce qu'il faut de l'humain), pousse, et termine.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée.
```

## 5. Séquence du POC

C = concepteur, D = développeur, V = vérificateur. Chaque ligne commence quand la précédente est acceptée.

| N° | Unité | Réalise | Vérifie | Acceptée quand | Fiche |
| --- | --- | --- | --- | --- | --- |
| S01 | 0.A Dossier de décisions | C | V | `docs/DECISIONS.md` couvre D-01 à D-09 ; adaptation A | étape 0 |
| S02 | 0.B Squelettes, `REGLES_AGENTS.md`, `tools/sync_rules.sh` | C | V | PC0.2 à PC0.6 et PC0.8 | étape 0 |
| S03 | Porte de l'étape 0 | C | V | Adaptation G ; T00 notée « non exécutée, mode autonome » | README, prompt de porte |
| S04 | T01 Squelette et plugin activable | D | V | T01-a à T01-e, contre-épreuve | étape 1 |
| S05 | T02 Runner et contrôle de dépendances | D | V | T02-a à T02-g | étape 1 |
| S06 | T03 Contrôle unique, lint et CI | D | C | T03-a à T03-i ; PC1.8 si le dépôt exécute les workflows | étape 1 |
| S07 | T04, sélection du banc d'essai | V | C | Adaptation C ; choix inscrit en D-02 | étape 1 |
| S08 | T04, préparation du banc d'essai | D | V | T04-a à T04-c | étape 1 |
| S09 | Porte de l'étape 1 | C | V | PC1.1 à PC1.10 | étape 1 |
| S10 | T05 SPIKE-01b sous écran virtuel | C | V | Adaptation D : six critères, chacun avec sa preuve | étape 2 |
| S11 | T06 SPIKE-02 | C | V | T06-a à T06-d | étape 2 |
| S12 | Porte de l'étape 2 | C | V | PC2.1 à PC2.6 | étape 2 |
| S13 | T07 Contrats C-01, C-02, C-05 | C | V | T07-a à T07-g | étape 3 |
| S14 | T08 Contrats C-03, C-04, C-06, C-07, puis gel | C | V | T08-a à T08-e ; adaptation H | étape 3 |
| S15 | Porte de l'étape 3 | C | V | PC3.1 à PC3.8 | étape 3 |
| S16 | T09 Codec de l'enveloppe | D | V | T09-a à T09-c | étape 4 |
| S17 | T10 Modèle, graphe déclaré, clés de sonde | D | V | T10-a à T10-c | étape 4 |
| S18 | T11 Event Store minimal | D | V | T11-a à T11-c | étape 4 |
| S19 | T12 Façades et profil moteur | D | C | T12-a à T12-d | étape 4 |
| S20 | T13a FlowTrace et protocole de session | D | C | T13a-a à T13a-d | étape 4 |
| S21 | T13b Banc sans éditeur et coupures | D | C | T13b-a, T13b-b | étape 4 |
| S22 | T13c Mesures de performance | D | V | T13c-a, T13c-b | étape 4 |
| S23 | Porte de l'étape 4 | C | V | PC4.1 à PC4.6 | étape 4 |
| S24 | T14 Réception côté éditeur | D | V | T14-a à T14-d | étape 5 |
| S25 | T15 Instrumentation du banc d'essai | D | V | T15-a à T15-d | étape 5 |
| S26 | Essai dans l'éditeur, sous écran virtuel (PC5.6) | D | C | Adaptation E | étape 5 |
| S27 | Porte de l'étape 5 | C | V | PC5.1 à PC5.6 | étape 5 |
| S28 | T16 Panneau du POC | D | V | T16-a à T16-e | étape 6 |
| S29 | T17 Chemin observé et ouverture du code | D | V | T17-a à T17-d | étape 6 |
| S30 | T18 Robustesse et cycle de vie | D | C | T18-a, T18-b | étape 6 |
| S31 | Démonstration sous écran virtuel (PC6.7) | D | V | Adaptation E | étape 6 |
| S32 | Porte de l'étape 6 | C | V | PC6.1 à PC6.7 | étape 6 |
| S33 | T19, injection de trois bugs | V | C | T19-a ; enveloppe scellée hors des branches de bug | étape 7 |
| S34 | T19, diagnostic par substitution | D | V | Adaptation F | étape 7 |
| S35 | T20 Revue de continuation et décision | C | V | Adaptation G et règle de décision du POC | étape 7 |

### Adaptations du guide

**A. Décisions (S01).** Le concepteur prépare `docs/DECISIONS.md` avec le prompt 0.A. Puis il inscrit la recommandation de D-01, D-05, D-07 et D-09 au statut « adoptée par défaut », daté. D-02 reçoit ses critères ; le choix se fait en S07. D-04, D-06 et D-08 restent « proposée » jusqu'à leur échéance. Le contrôle PC0.1 devient :

```bash
for d in D-01 D-05 D-07 D-09; do grep -E "^\| $d " docs/DECISIONS.md | grep -qE "validée|adoptée par défaut" || echo "manque $d"; done
```

**B. T00.** Non exécutée en mode autonome. Les tâches prévues pour Qwen vont au développeur.

**C. Choix du banc d'essai (S07).** Le vérificateur applique le prompt de sélection de T04. Le concepteur contrôle sa recommandation contre les critères, puis l'inscrit en D-02, au statut « adoptée par défaut ». Une licence non vérifiée écarte le candidat : on ne choisit jamais un jeu dont la licence reste incertaine.

**D. SPIKE-01b sous écran virtuel (S10).** Ce prompt remplace celui de T05, dont les manipulations à la main n'ont plus lieu d'être.

```text
Tu conduis SPIKE-01b du projet GODOT_DEV_MAPPER, sans humain. La partie jeu est établie : lis docs/spikes/SPIKE-01.md et spikes/spike01_debugger/.

FAIT VÉRIFIÉ le 8 octobre 2026, dans un conteneur sans GPU :
- l'éditeur Godot 4.7.2 tourne sous xvfb-run avec --rendering-driver opengl3 et un rendu logiciel (llvmpipe) ;
- un plugin peut lancer le jeu avec EditorInterface.play_main_scene() ;
- un EditorDebuggerPlugin reçoit les messages « flowspike:* » et en envoie par EditorDebuggerSession.send_message ;
- le plugin ne reçoit pas les messages du moteur (set_pid, output).
Vérifie de nouveau chaque API avant de t'y fier.

CONSTRUIS, dans spikes/spike01_debugger/editor/ seulement :
- un projet d'éditeur jetable, dont le plugin déroule seul le scénario ;
- un script run.sh qui télécharge Godot si besoin, lance l'éditeur sous écran virtuel, et affiche une ligne PASS ou FAIL par critère.

LES SIX CRITÈRES, chacun déclenché par le plugin lui-même :
1. « prêt » reçu par le plugin.
2. « started » reçu avant tout lot.
3. Arrêt avant la désactivation du plugin (EditorInterface.set_plugin_enabled) : « stopped » en une seconde au plus, aucun lot ensuite.
4. Coupure : jeu arrêté par stop_playing_scene, puis plugin retiré sans arrêt. Côté éditeur, « fin inconnue » ; côté jeu, collecte arrêtée par le bail en 2 s au plus.
5. Cinq lancements successifs, sans erreur ni fuite.
6. Débit et cadence à 1 200 et 10 000 événements par seconde, avec le rendu logiciel. Marque ces chiffres « non représentatifs d'un GPU » : la mesure sur ta machine passe à la recette.

À LA FIN : complète la section SPIKE-01b de docs/spikes/SPIKE-01.md (critère, déclenchement, observation, chiffre, statut, limites) et propose KEEP, REWRITE ou DISCARD.
```

Le vérificateur relance `run.sh` et compare les six lignes. Contre-épreuve : il retire l'envoi du bail dans le plugin, puis vérifie que le critère 4 reste vert grâce au bail côté jeu, et que le critère 3 détecte un lot tardif injecté exprès.

**E. Essais dans l'éditeur (S26, S31).** Les contrôles « sur ta machine » se font sous écran virtuel, avec le banc d'essai instrumenté lancé depuis l'éditeur :
- S26 : une session complète jusqu'au store ; compteurs comparés à ceux du banc sans éditeur.
- S31 : captures d'écran du panneau, jointes au rapport et lues par le vérificateur ; deux instances distinguées, trois états du chemin observé, ouverture du code à la bonne ligne. Aller-retour et délai réception → affichage mesurés et marqués « rendu logiciel ».
La désactivation du plugin pendant une vraie collecte, la latence sur GPU et le jugement visuel passent à la recette.

**F. Mesure de valeur par substitution (S33, S34).** La mesure du plan exige une personne. En son absence, une IA tient le rôle du développeur qui cherche un bug ; la mesure humaine est refaite à la recette.

```text
Tu mesures, par substitution, l'utilité du POC du projet GODOT_DEV_MAPPER. Tu n'as pas lu ../benches/{nom}/ENVELOPPE_SCELLEE.md et tu ne l'ouvres pas avant la fin.

PRÉPARE, fichiers autorisés : tools/harness/fake_editor.gd (option --record), tools/gdm_query.gd, docs/mesures/valeur-poc-substitution.md.
- --record enregistre la session reçue, lot par lot, dans un fichier JSONL.
- tools/gdm_query.gd relit ce fichier avec store/ et projections/, et affiche le journal d'une instance et le chemin observé de ses invocations.

MESURE, sur les trois branches gdm-bug-1 à gdm-bug-3, dans cet ordre :
- bug 1 avec l'outil : code du jeu, console du jeu, session enregistrée, sorties de gdm_query, captures du panneau sous écran virtuel ;
- bug 2 sans l'outil : code du jeu et console du jeu seulement ; tu peux ajouter des print ;
- bug 3 avec l'outil.
Pour chaque bug, note : le nombre d'exécutions du jeu, de lectures de fichier et de modifications temporaires ; le temps écoulé ; la cause que tu proposes, avec le fichier et la ligne ; ta confiance.
Ensuite seulement, ouvre l'enveloppe et note pour chaque bug si la cause est exacte.

RAPPORT dans docs/mesures/valeur-poc-substitution.md : le tableau de T19 adapté, puis une conclusion qualitative. Ce signal vaut pour un agent, pas pour une personne : écris-le en tête.
```

Si l'outil n'a aidé sur aucun des deux bugs où il servait, c'est l'arrêt obligatoire n° 1 du §6. Aider veut dire : cause exacte trouvée avec moins d'exécutions qu'au bug 2, ou trouvée là où le bug 2 ne l'a pas été.

**G. Portes d'étape et revue.** Le concepteur applique le prompt de porte d'étape du guide, puis décide seul selon cette règle :
- **Passer** : tous les points de contrôle exécutables sont OK, et chaque point « sur ta machine » a son équivalent sous écran virtuel. Ce qui exige un humain passe à la liste de recette, dans `PROJECT_STATE.md`.
- **Corriger d'abord** : un point est KO. L'unité suivante devient une correction, numérotée `S{n}.c` et réalisée par le rôle de la tâche fautive. Puis la porte est rejouée.
- **Budget** : au-delà de 50 % de créneaux en plus de l'estimation de l'étape, le concepteur écrit une revue courte dans `docs/revues/`, puis continue, sauf si un arrêt du §6 s'applique.

À S35, la décision du POC suit cette règle :
- **continuer** si la mesure par substitution montre un signal d'utilité, si aucun arrêt n'est ouvert et si les créneaux consommés restent sous le double de l'estimation ;
- **s'arrêter et t'attendre** dans les autres cas.

La décision est inscrite en « adoptée par défaut ». L'amendement du plan (PD-0.6) est appliqué au statut « proposé ».

**H. Gel des contrats (S14).** Après le verdict ACCEPTÉE du vérificateur, le concepteur passe `docs/CONTRACTS.md` au statut « adopté par défaut · date ». Une question qui changerait un contrat gelé se tranche par l'accord du concepteur et du vérificateur, avec analyse d'impact et changement de version, et passe à la liste de recette. Sans accord, c'est l'arrêt n° 6.

## 6. Arrêts obligatoires

L'IA écrit `rapports/ARRET.md` sur `main` et s'arrête. Tous les créneaux suivants s'arrêtent aussi, jusqu'à ce que tu supprimes le fichier.

1. **Aucun signal d'utilité au POC** (S34) : c'est le critère d'arrêt du plan.
2. **File bloquée** : une unité refusée trois fois, ou passée deux fois en ESCALADE.
3. **Décision réservée à toi** :
   - licence du plugin (D-06) ;
   - nouvelle dépendance tierce (D-04), dont la reprise de GDScript AST Flow ;
   - retrait d'une capacité du périmètre ;
   - diffusion publique, dépense, identifiants ou droits d'accès.
4. **Format persisté** : une rupture après une diffusion.
5. **Contrôles impossibles** : pas de Godot, pas de réseau ou pas d'écran virtuel pendant deux créneaux de suite.
6. **Désaccord** : contradiction entre un fait mesuré et un contrat gelé, sans accord entre le concepteur et le vérificateur.

## 7. Après le POC : MVP et V1

Chaque phase suit le même motif :
1. **Découpage.** Le concepteur applique le prompt de découpage de `mvp.md` ou de `v1.md` ; le vérificateur vérifie. Les tâches produites s'insèrent ici, dans leur ordre, au format des lignes du §5.
2. **Tâches.** Rôles fixés par le découpage. Toute tâche qui touche un contrat, le protocole, une façade ou un format persisté est vérifiée par le concepteur.
3. **Porte de phase.** Réalisée par le concepteur, vérifiée par le vérificateur ; adaptation G.

| N° | Phase | Après | Tâches prévues par le plan |
| --- | --- | --- | --- |
| S36 | P4a Évaluations : SPIKE-03 rendu, SPIKE-04 backend statique | S35 | 3 à 5 |
| S37 | P4b Backend statique et inventaire | S36 | 9 à 13 |
| S38 | P5 Navigation et arborescence res:// | S37 | 8 à 12 |
| S39 | P6 Historique, persistance, protocole MVP | S38 | 10 à 16 |
| S40 | P7 Logique et Game Flow annoté | S39 | 5 à 9 |
| S41 | P8 Compatibilité MVP et stabilisation, porte du MVP | S40 | 6 à 10 |
| S42 | P9 Timeline du Game Flow | S41 | 65 à 110 pour toute la V1 |
| S43 | P10 Instances et comparaison | S42 | |
| S44 | P11 Data Flow | S43 | |
| S45 | P12 Attendu contre observé | S44 | |
| S46 | P13 Diagnostic, Explain, Tune | S45 | |
| S47 | P14 Performance corrélée | S46 | |
| S48 | P15 AI Snapshot | S47 | |
| S49 | P16 Durcissement et documentation, porte de la V1 | S48 | |

Cet ordre linéaire respecte les dépendances de `mvp.md` et de `v1.md`.

Deux points restent hors de portée des IA :
- **Reprise d'AST Flow (SPIKE-04).** C'est une nouvelle dépendance : si le spike la recommande, c'est l'arrêt n° 3. Sinon, l'extraction maison continue.
- **Porte de la V1.** Elle demande deux versions stables de Godot. Si 4.8 stable n'est pas sortie, P16 s'arrête sur ce seul point et le note pour la recette.

## 8. Recette finale

C'est ta seule intervention prévue. `PROJECT_STATE.md` en tient la liste à jour pendant la construction ; elle contient au moins :

1. **Décisions** : relire chaque « adoptée par défaut » dans `docs/DECISIONS.md`, puis confirmer ou changer.
2. **Sur ta machine, avec GPU** :
   - débit et cadence de SPIKE-01b (critère 6) ;
   - latence de PC6.7 ;
   - désactivation du plugin pendant une vraie collecte ;
   - jugement visuel du panneau.
3. **Mesure de valeur humaine** : T19 tel que le guide le décrit, sur trois nouveaux bugs, puis comparaison avec la mesure par substitution.
4. **Test de cartographie du MVP**, chronométré avec et sans l'outil.
5. **Installation à froid** en suivant la seule documentation, puis désinstallation.
6. **Licence (D-06)** et décision de diffusion.
7. **Carte des scripts superposée au jeu** : décider si la proposition des maquettes (CAP-21, CAP-22) entre au plan.

## 9. Calendrier et suivi

Un créneau réalise une unité et en vérifie une autre ; une unité consomme 1 à 1,5 créneau, reprises comprises. À six créneaux par jour :

| Bloc | Unités | Créneaux | Fin estimée |
| --- | --- | --- | --- |
| POC, S01 à S35 | 35 | 35 à 53 | Jour 6 à 9 |
| MVP, P4a à P8 | 53 à 77, découpages et portes compris | 53 à 115 | Jour 15 à 28 |
| V1, P9 à P16 | 81 à 126, découpages et portes compris | 81 à 189 | Jour 29 à 60 |

Trente jours couvrent le POC et le MVP dans tous les cas, et la V1 seulement dans le cas le plus favorable. Deux limites ne dépendent pas des IA : la sortie de Godot 4.8 stable, et les quotas d'usage de chaque IA. Les quotas se mesurent dès la première semaine.

`PROJECT_STATE.md` tient, à chaque fusion :
- par unité : auteur, vérificateur, créneaux consommés, tentatives, verdicts ;
- par IA : taux d'acceptation au premier essai, refus, escalades ;
- par bloc : créneaux consommés contre l'estimation ;
- la liste de recette.

Le recalibrage se fait à S35, avec le ratio observé sur le POC.

## 10. Environnement de chaque IA

- Un clone du dépôt, avec le droit de pousser sur `main` et sur les branches `tache/*`.
- git, Python 3, `pip install -r requirements-dev.txt` (gdtoolkit 4.5.0, après T03).
- Un accès réseau à github.com, pour les binaires officiels de Godot (`tools/ci/fetch_godot.sh`, après T03).
- Pour S10, S26, S31 et les captures d'écran : Xvfb et Mesa. Le conteneur cloud de Claude Code les fournit (vérifié le 8 octobre 2026).
- Si le dépôt n'exécute pas les workflows GitHub, PC1.8 passe à la recette ; `run_all_checks.sh` en local fait foi en attendant.
