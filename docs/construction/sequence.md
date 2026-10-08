# Déroulé du mode autonome

Révision SQ-0.2 · statut : **proposé** · 8 octobre 2026 · fondé sur PD-0.5 (décision D-09), GC-0.4, OR-0.5 et MC-0.5 · remplace SQ-0.1

**Changements depuis SQ-0.1** : la liste des unités et leurs dépendances passent dans `SUIVI.md` ; chaque unité a sa fiche d'exécution dans `suivi/`, avec ses prompts et ses sous-étapes à cocher ; les unités indépendantes peuvent avancer en même temps ; le banc d'essai vit dans des branches `banc/<nom>-*` de ce dépôt.

Ce document fixe les règles quand trois IA construisent le projet à tour de rôle, sans humain jusqu'à la recette finale.

| Fichier | Rôle |
| --- | --- |
| `SUIVI.md` | Liste de progression : une ligne par unité, cochée à la fusion ; dépendances ; vagues d'unités indépendantes ; recette finale |
| `suivi/Sxx-*.md` | Fiche d'exécution d'une unité : ce qu'il faut faire, fichiers autorisés, prompt de réalisation, prompt de vérification, sous-étapes à cocher |
| `suivi/outil.py` | `verifier` : cohérence de `SUIVI.md` et des fiches, conformité au guide ; `generer` : fiches régénérées depuis le guide, sans écraser une fiche entamée |
| `suivi/_modele-tache.md`, `suivi/_modele-correction.md` | Modèles des fiches créées en cours de route : tâches du MVP et de la V1, corrections demandées par une porte |
| `docs/construction/etape-*.md`, `mvp.md`, `v1.md` | Conception de chaque tâche. Les fiches en recopient le travail technique à l'identique ; `suivi/outil.py verifier` signale tout écart |

## 1. Principes

- **Prérequis, pas de file unique.** Une unité commence dès que les unités de sa colonne « après » sont cochées dans `SUIVI.md`. Les unités sans lien entre elles avancent en même temps, quel que soit leur ordre dans la liste.
- **Dans une unité, tout est séquentiel.** Les sous-étapes R (réalisation), V (vérification) et F (fusion) se font dans l'ordre.
- **Trois rôles, trois IA.** L'auteur d'une unité ne la vérifie jamais.
- **Reprise par n'importe quelle IA.** Une IA coche une sous-étape seulement quand elle est faite et prouvée, puis elle commite et pousse. Celle qui arrive ensuite reprend à la première case non cochée de la fiche, sur la branche de l'unité.
- **Fichiers partagés.** `SUIVI.md`, `PROJECT_STATE.md` et `docs/DECISIONS.md` ne changent qu'à la fusion, sur `main`, par l'IA qui fusionne.
- **Décisions prises à ta place.** Chacune est écrite dans `docs/DECISIONS.md` avec le statut « adoptée par défaut » et sa date. Tu les confirmes ou tu les changes à la recette.
- **Personne ne t'attend**, sauf aux arrêts obligatoires (§5).

## 2. Les trois rôles

| Rôle | Réalise | Vérifie | Affectation proposée |
| --- | --- | --- | --- |
| Concepteur | Décisions, squelettes, spikes, contrats, portes d'étape, découpage des phases, revues | Façades, protocole, formats persistés, CI, choix du banc d'essai, injection des bugs | Claude Opus 5.5 |
| Développeur | Implémentation, outillage, interface, essais sous écran virtuel | Rien | Deuxième IA : Sonnet dans le plan ; toute autre IA de code que tu utilises |
| Vérificateur | Choix du banc d'essai, injection des bugs de la mesure de valeur | Tout le reste, dont les contrats et les spikes du concepteur | Gemini |

Le plan prévoyait aussi Qwen3.8-27B en local. Son installation (T00) exige ta machine : en mode autonome, il n'est pas utilisé et ses tâches vont au développeur. Dans les fiches du guide, « Sonnet » et « Qwen » désignent le rôle de développeur.

## 3. États, prise en charge et fusion

| État d'une unité | Comment le reconnaître |
| --- | --- |
| Acceptée | Ligne cochée dans `SUIVI.md` sur `main` |
| Disponible | Prérequis cochés ; aucune branche `tache/<fiche>` sur le dépôt distant, ou aucun commit dessus depuis deux créneaux |
| En cours | Branche `tache/<fiche>` avec un commit récent, `rapports/Sxx.md` au statut EN COURS |
| À vérifier | `rapports/Sxx.md` au statut TERMINÉ, sans verdict pour cette tentative |
| Refusée | Dernier verdict `rapports/Sxx-verif-<n>.md` à REFUSÉE : elle redevient disponible pour le rôle de l'auteur |
| Bloquée | Statut QUESTION ou ESCALADE, ou `rapports/ARRET.md` sur `main` |

**Prise en charge.** Une IA prend une unité disponible en créant sa branche et en poussant `rapports/Sxx.md` au statut EN COURS. Si deux IA prennent la même unité, la première branche poussée l'emporte ; l'autre abandonne et choisit une autre unité.

**Fusion.** Elle est faite par le vérificateur qui accepte, selon les sous-étapes F de la fiche : fusion `--no-ff` dans `main`, puis `tools/ci/run_all_checks.sh` sur `main` (dès que S06 l'a créé). Si les contrôles sont verts : la ligne est cochée dans `SUIVI.md`, `PROJECT_STATE.md` est mis à jour, puis push. Sinon : `git reset --hard ORIG_HEAD` avant tout envoi, puis verdict « REFUSÉE (fusion) ».

## 4. Prompt de créneau

C'est le seul message à donner à une IA au début de son créneau. Elle choisit seule son travail dans `SUIVI.md` et suit la fiche de l'unité.

```text
Tu es {NOM DE L'IA}, au rôle {Concepteur | Développeur | Vérificateur}, pour un créneau du projet GODOT_DEV_MAPPER. Tu n'as aucune mémoire des créneaux précédents : le dépôt est ta seule source.

0. ARRÊT. git fetch --all. Si rapports/ARRET.md existe sur main, lis-le, ne fais rien d'autre, et termine en citant sa raison.

1. ÉTAT. Lis docs/construction/sequence.md, REGLES_AGENTS.md s'il existe, puis SUIVI.md sur main. Lance python3 suivi/outil.py verifier et note le résultat.

2. CHOIX, dans cet ordre de priorité :
   a. Une unité à vérifier dont tu n'es pas l'auteur et dont la colonne « vérifie » est ton rôle. Si le rôle prévu n'est pas passé depuis deux créneaux, tout rôle autre que l'auteur peut vérifier.
   b. Une unité en cours abandonnée (aucun commit depuis deux créneaux) ou refusée, dont la colonne « réalise » est ton rôle : tu la reprends à la première case non cochée.
   c. La première unité disponible de SUIVI.md dont la colonne « réalise » est ton rôle. Une unité du développeur peut être prise par une autre IA si le développeur n'est pas passé depuis deux créneaux.
   Rien ne correspond à ton rôle : écris-le dans ta réponse et termine.

3. TRAVAIL. Ouvre la fiche suivi/<fiche>.md de l'unité choisie et applique son prompt de réalisation ou de vérification, en cochant les sous-étapes au fur et à mesure. Si ton créneau le permet, prends ensuite une autre unité selon le point 2.

4. FIN. Rien ne reste non poussé. Ta réponse finale liste les unités touchées et la dernière case cochée de chacune.

RÈGLES
- Tu ne vérifies jamais ton propre travail.
- Un arrêt obligatoire du §5 de sequence.md : écris rapports/ARRET.md sur main (raison, unité, preuve, ce qu'il faut de l'humain), pousse, et termine.
- Tu n'écris jamais qu'une commande a réussi sans l'avoir exécutée.
```

## 5. Arrêts obligatoires

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

## 6. Ce qui change par rapport au guide

Chaque fiche porte ses propres adaptations, dans la section « ADAPTATIONS DU MODE AUTONOME » de son prompt. Les principales :

- **Décisions de démarrage (S01)** : adoptées par défaut, à confirmer à la recette ; D-09 ajoutée.
- **T00** : non exécutée ; Qwen n'est pas utilisé.
- **Banc d'essai (S07, S08, S25, S33)** : licences qui permettent de redistribuer une copie modifiée ; copie dans des branches orphelines `banc/<nom>-base`, `-instrumentation`, `-bug-1` à `-bug-3` et `-enveloppe`, jamais sur `main`.
- **SPIKE-01b (S10)** : sous écran virtuel, avec rendu logiciel ; le débit sur GPU passe à la recette.
- **Essais « sur ta machine » (S26, S31)** : sous écran virtuel, avec captures d'écran lues par le vérificateur.
- **Mesure de valeur (S33, S34)** : par substitution, une IA cherche les bugs avec et sans l'outil ; ta mesure se fait à la recette.
- **Portes d'étape et revue (S03 à S35)** : règle de décision écrite ; un point KO crée une unité de correction `Sxx.c1` depuis `suivi/_modele-correction.md`.
- **Gel des contrats (S15)** : statut « adopté par défaut » ; un changement ultérieur exige l'accord du concepteur et du vérificateur, une analyse d'impact et un changement de version.

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

Les unités indépendantes ne raccourcissent pas ce calendrier quand les IA passent l'une après l'autre. Elles évitent les créneaux perdus : quand l'unité suivante attend un autre rôle, l'IA de service en prend une indépendante. Si tu fais tourner deux ou trois IA en même temps, les vagues de `SUIVI.md` montrent ce qui peut avancer ensemble.

Trente jours couvrent le POC et le MVP dans tous les cas, et la V1 seulement dans le cas le plus favorable. Deux limites ne dépendent pas des IA : la sortie de Godot 4.8 stable, nécessaire à la porte de la V1, et les quotas d'usage de chaque IA, à mesurer dès la première semaine.

À chaque fusion, `PROJECT_STATE.md` tient :
- par unité : auteur, vérificateur, créneaux consommés, tentatives, verdicts ;
- par IA : taux d'acceptation au premier essai, refus, escalades ;
- par bloc : créneaux consommés contre l'estimation ;
- la liste de recette.

Le recalibrage se fait à S35, avec le ratio observé sur le POC.

## 9. Environnement de chaque IA

- Un clone du dépôt, avec le droit de pousser sur `main` et sur les branches `tache/*` et `banc/*`.
- git 2.42 ou plus, Python 3, `pip install -r requirements-dev.txt` (gdtoolkit 4.5.0, après S06).
- Un accès réseau à github.com, pour les binaires officiels de Godot (procédure dans chaque fiche).
- Pour S10, S26, S31 et les captures d'écran : Xvfb et Mesa. Le conteneur cloud de Claude Code les fournit, ce qui a été vérifié le 8 octobre 2026.
- Si le dépôt n'exécute pas les workflows GitHub, PC1.8 passe à la recette ; `run_all_checks.sh` en local fait foi en attendant.
