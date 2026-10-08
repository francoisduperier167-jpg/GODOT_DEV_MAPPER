# Déroulé du mode autonome

Révision SQ-0.3 · statut : **proposé** · 8 octobre 2026 · fondé sur PD-0.5 (décision D-09), GC-0.4, OR-0.5 et MC-0.5 · remplace SQ-0.2

**Changements depuis SQ-0.2** : les rôles s'appellent IA 1, IA 2 et IA 3, et tu choisis quelle IA tient chaque numéro ; chaque sous-étape se coche et se signe par une commande, qui commite et pousse ; l'accès simultané au suivi est réglé (prise atomique d'une unité, verrou de `main` pour toute écriture partagée) ; `SUIVI.md` s'organise en pistes autonomes et en rendez-vous ; un tableau de bord graphique, `suivi/tableau.html`, le dessine.

Ce document fixe les règles quand trois IA construisent le projet à tour de rôle, ou en même temps, sans humain jusqu'à la recette finale.

| Fichier | Rôle |
| --- | --- |
| `SUIVI.md` | Liste de progression : une ligne par unité, rangée dans sa piste autonome ou son rendez-vous, cochée à la fusion ; recette finale |
| `suivi/Sxx-*.md` | Fiche d'exécution d'une unité : ce qu'il faut faire, fichiers autorisés, prompts de réalisation et de vérification, sous-étapes R, V et F à cocher |
| `suivi/outil.py` | Commandes des IA (`etat`, `prendre`, `cocher`, `fusionner`, `publier`, `correction`, `verrou`) ; cohérence (`verifier`) ; génération (`generer`) ; tableau de bord (`tableau`) |
| `suivi/tableau.html` | Tableau de bord : cinq carrés par unité, du rouge au vert ; un carré de fond par piste ; bouton « Actualiser » qui relit `SUIVI.md` et les branches sur GitHub |
| `suivi/_modele-tache.md`, `suivi/_modele-correction.md` | Modèles des fiches créées en cours de route : tâches du MVP et de la V1, corrections demandées par une porte |
| `docs/construction/etape-*.md`, `mvp.md`, `v1.md` | Conception de chaque tâche. Les fiches en recopient le travail technique à l'identique ; `python3 suivi/outil.py verifier` signale tout écart |

## 1. Principes

- **Prérequis, pas de file unique.** Une unité commence dès que les unités de sa colonne « après » sont cochées dans `SUIVI.md`.
- **Pistes autonomes.** Dans chaque section de `SUIVI.md`, une piste regroupe des unités qui se font à la suite. Les pistes d'une même section avancent en même temps ; le rendez-vous de la section (une porte, en général) attend leur fin.
- **Dans une unité, tout est séquentiel.** Les sous-étapes R (réalisation), V (vérification) et F (fusion) se font dans l'ordre ; la commande `cocher` refuse une case tant que la précédente n'est pas cochée.
- **Trace obligatoire.** Une sous-étape n'est faite que lorsque `cocher` l'a cochée et signée (IA, date, heure UTC), puis commitée et poussée. Une sous-étape faite mais non cochée est refaite par l'IA suivante.
- **Reprise par n'importe quelle IA.** Celle qui arrive reprend à la première case non cochée de la fiche, sur la branche de l'unité.
- **L'auteur ne vérifie jamais.** Les commandes refusent qu'une IA vérifie ou fusionne une unité dont elle est auteur.
- **Décisions prises à ta place.** Chacune est écrite dans `docs/DECISIONS.md` avec le statut « adoptée par défaut » et sa date. Tu les confirmes ou tu les changes à la recette.
- **Personne ne t'attend**, sauf aux arrêts obligatoires (§5).

## 2. Les trois IA

Tu choisis quelle IA tient chaque numéro. Un numéro reste à la même IA pendant tout le projet : il signe ses cases, et c'est lui qui interdit à une IA de vérifier son propre travail.

| IA | Rôle | Réalise | Vérifie |
| --- | --- | --- | --- |
| IA 1 | Conception | Décisions, squelettes, spikes, contrats, portes, découpage des phases, revues | Façades, protocole, formats persistés, CI, choix du banc d'essai, injection des bugs |
| IA 2 | Développement | Implémentation, outillage, interface, essais sous écran virtuel | Rien, sauf relais |
| IA 3 | Vérification | Choix du banc d'essai, injection des bugs de la mesure de valeur | Tout le reste, dont les contrats et les spikes d'IA 1 |

La colonne « réalise » et la colonne « vérifie » de `SUIVI.md` donnent l'IA prévue pour chaque unité. Une autre IA peut prendre le relais quand l'IA prévue ne passe pas (§3), jamais pour vérifier une unité dont elle est auteur.

## 3. États, trace et accès simultané

### États d'une unité

| État | Comment le reconnaître (`python3 suivi/outil.py etat` le calcule) |
| --- | --- |
| En attente | Un prérequis n'est pas coché dans `SUIVI.md` |
| Prête | Prérequis cochés ; aucune branche `tache/<fiche>` sur le dépôt |
| En cours | Branche présente ; R0 cochée, dernière case R non cochée |
| Abandonnée | En cours, sans case signée depuis 6 heures |
| À vérifier | Dernière case R cochée (rapport « TERMINÉ »), V1 non cochée |
| En vérification | V1 cochée, dernière case V non cochée ; abandonnée après 6 heures sans case signée |
| Refusée | Dernière case V signée « REFUSÉE » |
| À fusionner | Dernière case V signée « ACCEPTÉE », ligne non cochée dans `SUIVI.md` |
| Bloquée | Rapport au statut QUESTION ou ESCALADE |
| Faite | Ligne cochée dans `SUIVI.md` sur `main` |

### Trace obligatoire

Après chaque sous-étape, l'IA ajoute les fichiers de la sous-étape (`git add`, fichiers nommés), puis lance `python3 suivi/outil.py cocher <unité> <sous-étape> --ia <n>`. La commande :

1. refuse une case déjà cochée, une case dont la précédente ne l'est pas, une IA qui n'est pas auteur (cases R) ou pas le vérificateur inscrit (cases V et F) ;
2. refuse la dernière case R si le rapport ne dit pas « Statut : TERMINÉ », et la dernière case V si le verdict passé à `--verdict` diffère de celui du fichier ;
3. coche la case et la signe : `— IA n · AAAA-MM-JJ HH:MM UTC`, plus le verdict pour la dernière case V ;
4. commite, puis pousse sur la branche de l'unité, en se rebasant si une autre poussée l'a précédée. Les cases F sont commitées sur la copie de fusion et poussées par `publier`.

R0 se coche par `prendre`, V1 par `prendre --verification`, F1 par `fusionner` et la dernière case F par `publier`. `python3 suivi/outil.py verifier` refuse une case cochée sans signature, une case cochée après une case ouverte, et une ligne cochée dans `SUIVI.md` dont la fiche a une case ouverte. Le vérificateur contrôle en V2 que chaque case R a son commit.

### Accès simultané

Toutes les IA peuvent lire `SUIVI.md`, les fiches et les branches en même temps, sur le dépôt distant. Chaque écriture passe par une poussée Git que le dépôt accepte ou refuse en entier : deux IA ne peuvent pas écrire la même chose au même moment.

| Ce qui est écrit | Par qui | Garantie |
| --- | --- | --- |
| Prise d'une unité | `prendre` : crée `tache/<fiche>` depuis `main`, rapport « EN COURS », R0 signée, puis poussée sans `--force` | Si deux IA prennent la même unité au même moment, le dépôt refuse la seconde poussée ; la commande nettoie et répond REFUSÉ |
| Fiche et rapport d'une unité | L'IA qui la tient, sur sa branche, par `cocher` | Une seule IA par branche ; une reprise ajoute un commit, et deux reprises simultanées se départagent comme une prise |
| Prise d'une vérification | `prendre --verification` : copie neuve `../verif-<fiche>`, `rapports/Sxx-verif-<t>.md` au verdict EN COURS, V1 signée, poussée sur la branche | Même garantie : la seconde IA est refusée |
| `main` : `SUIVI.md`, `PROJECT_STATE.md`, `docs/DECISIONS.md`, `rapports/ARRET.md` | Seulement sous le verrou de `main` : `fusionner` puis `publier`, `correction`, ou `verrou prendre` puis `verrou rendre` | Le verrou est la branche `verrou/main`, créée par une poussée qui échoue si elle existe déjà (`--force-with-lease=refs/heads/verrou/main:`). Une IA qui le trouve pris attend jusqu'à 30 minutes. Un verrou de plus de 45 minutes est périmé et supprimé. Seule l'IA qui le tient le rend |
| Branches `banc/<nom>-*` | L'unité qui les crée (S08, S25, S33) | Une seule unité par branche |

Aucune IA ne modifie `SUIVI.md` à la main. Les commandes ne poussent jamais avec `--force`, sauf pour créer et rendre le verrou, toujours avec la garantie `--force-with-lease`.

### Relais, abandon, questions

- **Abandon.** Une unité en cours ou en vérification sans case signée depuis 6 heures peut être reprise par une autre IA : `prendre` l'inscrit parmi les auteurs (ou comme vérificateur) et l'IA reprend à la première case ouverte.
- **Relais.** Une unité prête, ou à vérifier, depuis 12 heures sans que l'IA prévue l'ait prise, peut être prise par une autre IA, jamais par un auteur pour la vérifier.
- **Question ou escalade.** IA 1 répond dans le rapport et reprend l'unité ; si IA 1 en est l'auteur, c'est IA 3. Une question qui demande une décision réservée à l'humain est un arrêt obligatoire.
- **Refus.** L'auteur relance `prendre` : la commande ajoute une case « Rc » (problèmes du verdict corrigés), rouvre la dernière case R et les cases V, et passe à la tentative suivante.

### Fusion

Le vérificateur qui accepte lance `python3 suivi/outil.py fusionner Sxx --ia <n> --godot "$B"` depuis son clone principal. La commande prend le verrou de `main`, fusionne la branche avec `--no-ff` dans une copie `../fusion-<fiche>`, lance `tools/ci/run_all_checks.sh` (dès que S06 l'a créé), coche la ligne dans `SUIVI.md` avec la date, les auteurs et le vérificateur, et coche F1. Si les contrôles échouent, elle annule tout, passe le verdict à REFUSÉE sur la branche et rend le verrou. Le vérificateur fait ensuite les cases F suivantes dans la copie de fusion, puis `publier` : `verifier` relancé, `main` poussée, branche de l'unité supprimée, verrou rendu.

### Porte KO

Si une porte décide « corriger d'abord », le vérificateur fusionne son rapport avec `fusionner Sxx --porte-ko` (la ligne de la porte reste ouverte), puis crée une unité de correction par point KO : `python3 suivi/outil.py correction Sxx --fautive Syy --titre "…" --realise <n> --verifie <m> --ia <n>`. La correction se place juste avant la porte, dans sa piste, et la porte l'attend. Quand les corrections sont fusionnées, la porte redevient prête ; `prendre` remet ses cases à zéro pour la rejouer.

## 4. Prompt de créneau

C'est le seul message à donner à une IA au début de son créneau, avec son numéro à la place de {N}. Le tableau de bord le copie pour chaque IA (« Prompt de créneau »).

```text
Tu es IA {N} pour un créneau du projet GODOT_DEV_MAPPER. Ce numéro est le tien pour tout le projet : tu le passes à --ia dans chaque commande, et il signe chaque case que tu coches. Tu n'as aucune mémoire des créneaux précédents : le dépôt est ta seule source.

0. DÉPÔT. Clone le dépôt, ou, dans ton clone : git fetch origin, puis git switch --detach origin/main. Si rapports/ARRET.md existe sur origin/main : lis-le, ne fais rien d'autre, et termine en citant sa raison.

1. RÈGLES. Lis docs/construction/sequence.md, puis REGLES_AGENTS.md s'il existe.

2. CHOIX. python3 suivi/outil.py etat --ia {N}
   La commande lit SUIVI.md et les branches sur le dépôt, puis liste ce que tu peux faire, par ordre de priorité : questions à traiter, vérifications, fusions, tes unités à reprendre, unités prêtes pour toi, relais. Prends la première ligne et lance la commande qu'elle donne. Si elle répond REFUSÉ, une autre IA vient de la prendre : passe à la ligne suivante.

3. TRAVAIL. Ouvre la fiche suivi/<fiche>.md de l'unité et applique son prompt : de réalisation après prendre, de vérification après prendre --verification. Après chaque sous-étape : git add des fichiers de la sous-étape, puis python3 suivi/outil.py cocher <unité> <sous-étape> --ia {N}. Une sous-étape non cochée par cette commande est considérée comme non faite.

4. SUITE. Si ton créneau le permet, reviens au point 2.

5. FIN. Rien ne reste non commité ni non poussé. Si tu tiens le verrou de main (python3 suivi/outil.py verrou etat), termine la fusion avec publier, ou rends-le : python3 suivi/outil.py verrou rendre --ia {N}. Ta réponse finale liste les unités touchées et la dernière case cochée de chacune.

RÈGLES
- Tu ne vérifies jamais une unité dont tu es auteur ; les commandes le refusent.
- Tu ne modifies jamais SUIVI.md à la main, et tu ne pousses jamais avec --force.
- Arrêt obligatoire (§5 de sequence.md) : python3 suivi/outil.py verrou prendre --ia {N} --motif "Arrêt" ; git fetch origin ; git switch --detach origin/main ; écris rapports/ARRET.md (raison, unité, preuve, ce qu'il faut de l'humain) ; git add rapports/ARRET.md ; git commit ; git push origin HEAD:main ; python3 suivi/outil.py verrou rendre --ia {N} ; termine.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée.
```

## 5. Arrêts obligatoires

L'IA écrit `rapports/ARRET.md` sur `main`, sous le verrou (procédure du prompt de créneau), et s'arrête. Tous les créneaux suivants s'arrêtent aussi, et les commandes refusent de prendre ou de fusionner, jusqu'à ce que tu supprimes le fichier.

1. **Aucun signal d'utilité au POC** (S34) : c'est le critère d'arrêt du plan.
2. **File bloquée** : une unité refusée trois fois, ou passée deux fois en ESCALADE ; ou une unité dont les trois IA sont auteurs, que plus personne ne peut vérifier.
3. **Décision réservée à toi** :
   - licence du plugin (D-06) ;
   - nouvelle dépendance tierce (D-04), dont la reprise de GDScript AST Flow ;
   - retrait d'une capacité du périmètre ;
   - diffusion publique, dépense, identifiants ou droits d'accès.
4. **Format persisté** : une rupture après une diffusion.
5. **Contrôles impossibles** : pas de Godot, pas de réseau ou pas d'écran virtuel pendant deux créneaux de suite.
6. **Désaccord** : contradiction entre un fait mesuré et un contrat gelé, sans accord entre IA 1 et IA 3.

## 6. Ce qui change par rapport au guide

Chaque fiche porte ses propres adaptations, dans la section « ADAPTATIONS DU MODE AUTONOME » de son prompt. Les principales :

- **Décisions de démarrage (S01)** : adoptées par défaut, à confirmer à la recette ; D-09 ajoutée.
- **T00** : non exécutée ; pas d'IA locale en mode autonome.
- **Fichiers de contexte** : `tools/sync_rules.sh` copie `REGLES_AGENTS.md` vers `AGENTS.md` ; tu ajoutes à la liste en tête du script le fichier que lit chacune de tes IA.
- **Banc d'essai (S07, S08, S25, S33)** : licences qui permettent de redistribuer une copie modifiée ; copie dans des branches orphelines `banc/<nom>-base`, `-instrumentation`, `-bug-1` à `-bug-3` et `-enveloppe`, jamais sur `main`.
- **SPIKE-01b (S10)** : sous écran virtuel, avec rendu logiciel ; le débit sur GPU passe à la recette.
- **Essais « sur ta machine » (S26, S31)** : sous écran virtuel, avec captures d'écran lues par le vérificateur.
- **Mesure de valeur (S33, S34)** : par substitution, une IA cherche les bugs avec et sans l'outil ; ta mesure se fait à la recette.
- **Portes d'étape et revue (S03 à S35)** : règle de décision écrite ; un point KO crée une unité de correction (§3).
- **Gel des contrats (S15)** : statut « adopté par défaut » ; un changement ultérieur exige l'accord d'IA 1 et d'IA 3, une analyse d'impact et un changement de version.

## 7. Recette finale

C'est ta seule intervention prévue. Sa liste est en fin de `SUIVI.md`, complétée pendant la construction dans `PROJECT_STATE.md` :

1. **Décisions** : relire chaque « adoptée par défaut » dans `docs/DECISIONS.md`, puis confirmer ou changer.
2. **Sur ta machine, avec GPU** :
   - débit et cadence de SPIKE-01b (critère 6) ;
   - latence de PC6.7 ;
   - désactivation du plugin pendant une vraie collecte ;
   - jugement visuel du panneau.
3. **Mesure de valeur humaine** : T19 tel que le guide le décrit, sur trois nouveaux bugs, comparée à la mesure par substitution.
4. **Test de cartographie du MVP**, chronométré avec et sans l'outil.
5. **Installation à froid** en suivant la seule documentation, puis désinstallation.
6. **Licence (D-06)** et décision de diffusion.
7. **Carte des scripts superposée au jeu** : décider si la proposition des maquettes (CAP-21, CAP-22) entre au plan.

## 8. Calendrier et suivi

Un créneau vérifie une unité et en réalise une autre. Une unité consomme 1 à 1,5 créneau, reprises comprises. À six créneaux par jour :

| Bloc | Unités | Créneaux | Fin estimée |
| --- | --- | --- | --- |
| POC, S01 à S35 | 35 | 35 à 53 | Jour 6 à 9 |
| MVP, S36 à S41.P | 53 à 77, découpages et portes compris | 53 à 115 | Jour 15 à 28 |
| V1, S42 à S49.P | 81 à 126, découpages et portes compris | 81 à 189 | Jour 29 à 60 |

Les pistes autonomes ne raccourcissent pas ce calendrier quand les IA passent l'une après l'autre. Elles évitent les créneaux perdus : quand l'unité suivante d'une piste attend une autre IA, l'IA de service en prend une dans une autre piste. Si tu fais tourner deux ou trois IA en même temps, chacune peut tenir une piste différente ; le verrou de `main` n'est tenu que le temps d'une fusion.

Trente jours couvrent le POC et le MVP dans tous les cas, et la V1 seulement dans le cas le plus favorable. Deux limites ne dépendent pas des IA : la sortie de Godot 4.8 stable, nécessaire à la porte de la V1, et les quotas d'usage de chaque IA, à mesurer dès la première semaine.

**Pour suivre l'avancement**, ouvre `suivi/tableau.html` (depuis une copie du dépôt) et clique « Actualiser » : la page relit `SUIVI.md` et les branches sur GitHub. Chaque unité y a cinq carrés : prise en charge, réalisation, contrôles et rapport, vérification, fusion, qui passent du rouge au vert. `python3 suivi/outil.py tableau` régénère l'instantané embarqué dans la page.

À chaque fusion, `PROJECT_STATE.md` tient :
- par unité : auteurs, vérificateur, créneaux consommés, tentatives, verdicts ;
- par IA : taux d'acceptation au premier essai, refus, escalades ;
- par bloc : créneaux consommés contre l'estimation ;
- la liste de recette.

Le recalibrage se fait à S35, avec le ratio observé sur le POC.

## 9. Environnement de chaque IA

- Un clone du dépôt, avec le droit de pousser sur `main` et sur les branches `tache/*`, `banc/*` et `verrou/main`. Les copies `../verif-*` et `../fusion-*` se créent à côté du clone.
- git 2.42 ou plus (`worktree`, `--force-with-lease`), Python 3, `pip install -r requirements-dev.txt` (gdtoolkit 4.5.0, après S06).
- Un accès réseau à github.com, pour le dépôt et pour les binaires officiels de Godot (procédure dans chaque fiche).
- Pour S10, S26, S31 et les captures d'écran : Xvfb et Mesa. Un conteneur cloud avec ces paquets suffit ; c'est vérifié le 8 octobre 2026.
- Si le dépôt n'exécute pas les workflows GitHub, PC1.8 passe à la recette ; `run_all_checks.sh` en local fait foi en attendant.
