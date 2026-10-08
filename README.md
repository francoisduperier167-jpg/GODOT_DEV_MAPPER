# GODOT_DEV_MAPPER

Préparation d'un plugin pour Godot : **Godot Visual Program & Execution Explorer**. Il doit cartographier un projet Godot (architecture, logique, données, déroulement du jeu) et superposer à cette carte ce qui s'est réellement exécuté.

**Statut au 8 octobre 2026 : cadrage, premier spike fait.** Aucun code du plugin n'existe encore. SPIKE-01a a vérifié la partie jeu du canal du débogueur sur Godot 4.7.2 et 4.8-dev7. Le plan directeur, la méthodologie et l'orchestration sont proposés, pas encore validés. Mode d'exécution proposé : trois IA à tour de rôle, une unité après l'autre, recette humaine à la fin (D-09).

## Contenu

| Chemin | Rôle |
| --- | --- |
| `docs/plan-directeur.md` | Plan directeur PD-0.5 : capacités, architecture, protocole de session, modèle de données, POC, MVP, budgets, risques, mode d'exécution |
| `docs/methodologie.md` | Méthode de construction MC-0.5 : sources de vérité et leur hiérarchie, contrats, tests, CI, veille de Godot, gabarits |
| `docs/orchestration.md` | OR-0.5 : tâches T00 à T20, dépendances, répartition entre IA 1, IA 2 et IA 3 |
| `docs/construction/` | Guide de construction GC-0.4 et sa carte interactive `carte.html` : pour chaque étape, objectif, obligations, méthodologie, points de contrôle, amélioration et prompts de réalisation et de vérification |
| `SUIVI.md` | Liste de progression : une ligne par unité, rangée dans sa piste autonome ou son rendez-vous, cochée à la fusion ; recette finale |
| `suivi/` | Une fiche d'exécution par unité (prompts, sous-étapes à cocher et à signer) ; `suivi/outil.py` : commandes des IA, verrou de `main`, contrôle de cohérence ; `suivi/tableau.html` : tableau de bord graphique |
| `docs/construction/sequence.md` | Règles du mode autonome : IA 1, IA 2, IA 3, trace des sous-étapes, accès simultané, fusion, prompt de créneau, arrêts obligatoires, recette finale |
| `docs/maquettes/` | Maquettes fictives du rendu : atlas EMBER hors exécution, et mode en direct avec la carte des scripts superposée au jeu |
| `docs/spikes/SPIKE-01.md` | Rapport de SPIKE-01a : canal du débogueur, partie jeu, mesuré sur 4.7.2 et 4.8-dev7 |
| `spikes/` | Prototypes jetables des spikes |
| `docs/estimation.md` | Historique : pertinence, faisabilité et raisonnement de charge initial, en sessions |
| `docs/feuille-de-route.svg` | Historique : feuille de route des prompts 2.1, en sessions cumulées |
| `docs/analyse-des-prompts-v2.0.md` | Historique : analyse critique des prompts initiaux |
| `prompts/conception.txt` | Historique : prompt de conception v2.2 |
| `prompts/methodologie.txt` | Historique : prompt de méthodologie v2.2 |

**En cas d'écart entre documents**, un fait mesuré dans un rapport de spike prime. Viennent ensuite le plan directeur (périmètre et budgets), l'orchestration (ordre des tâches) et la méthodologie (règles de travail). Les documents marqués « historique » expliquent d'où vient le plan ; ils ne le remplacent pas.

## Démarrer

**En mode autonome**, le mode proposé (D-09) :
1. Choisis quelle IA tient chaque numéro : IA 1 (conception), IA 2 (développement), IA 3 (vérification). Le numéro ne change plus.
2. Donne à chaque IA, au début de chacun de ses créneaux, le prompt de créneau de `docs/construction/sequence.md` (§4) avec son numéro ; le bouton « Copier » du tableau de bord le prépare.
3. L'IA lance `python3 suivi/outil.py etat --ia N`, prend la première unité proposée, suit sa fiche dans `suivi/`, et coche puis signe chaque sous-étape avec `python3 suivi/outil.py cocher`. Une autre IA reprend à la première case non cochée. Deux IA qui travaillent en même temps ne se gênent pas : une unité ne se prend qu'une fois, et `main` ne s'écrit que sous verrou. La première unité est S01, le dossier de décisions, par IA 1.
4. Pour suivre l'avancement, ouvre `suivi/tableau.html` depuis une copie du dépôt et clique « Actualiser » : cinq carrés par unité, du rouge au vert, et un carré de fond par piste autonome.
5. Tu n'interviens qu'à la recette finale (fin de `SUIVI.md`), ou si un fichier `rapports/ARRET.md` apparaît sur `main` (§5 de `sequence.md`).

**En mode piloté**, le mode d'origine :
1. Relire `docs/plan-directeur.md` et trancher les décisions bloquantes D-01, D-02, D-05 et D-07 (§10).
2. Ouvrir la carte interactive `docs/construction/carte.html` : elle affiche la prochaine action, l'IA à lancer et le prompt à copier. Le guide `docs/construction/README.md` en est la référence détaillée.

SPIKE-01b, la partie éditeur du canal (tâche T05), peut s'exécuter sous écran virtuel avec un rendu logiciel : c'est vérifié sur Godot 4.7.2 le 8 octobre 2026. Seule la mesure de débit sur GPU attend ta machine.

## Compatibilité avec les versions de Godot

Godot publie une version mineure tous les quelques mois, et une version mineure peut modifier certaines API. Le plugin isole donc tout appel sensible derrière une frontière de compatibilité : c'est l'invariant INV-09.

Avant la preuve de valeur, cette frontière reste légère : des façades, une CI bloquante sur Godot 4.7.2 et la préversion suivante testée à part. Les adaptateurs par version et la veille automatisée n'arrivent qu'au MVP, ou plus tôt si une rupture réelle apparaît.

## Répartition entre les IA

Trois IA, que tu choisis, tiennent trois rôles. IA 1 prend les décisions, les contrats, les façades de compatibilité, les spikes, les portes et le débogage difficile. IA 2 écrit le code sous contrat validé et couvert par des tests, l'outillage et l'interface. IA 3 vérifie, lit les jeux open source et prépare la mesure de valeur. Les outils sans IA exécutent les tests, le lint et les mesures. L'auteur d'une unité ne la vérifie jamais (`docs/construction/sequence.md`, §2).

## Bancs d'essai

Les tests s'appuient sur des jeux Godot open source existants. Ne copier ni leur code ni leurs assets dans ce dépôt sans vérifier la compatibilité des licences. Les référencer par dépôt et révision, ou par sous-module Git.

## Versions des prompts

Chaque version correspond à un commit de l'historique. Les étiquettes ci-dessous sont prévues, mais pas encore créées sur le dépôt distant :

- `prompts-v1` : prompts d'origine ;
- `prompts-v2.0` : révision et analyse critique ;
- `prompts-v2.1` : paramètres connus, analyse de l'existant, budget, contrat runtime phasé, bancs d'essai open source, orchestration de plusieurs IA ;
- `prompts-v2.2` : couche de compatibilité moteur et politique de versions (INV-09), avec le plan directeur, la méthodologie et l'orchestration.

La commande `git log --follow prompts/conception.txt` montre l'évolution d'un prompt.

## Licence

À définir avant la première ligne de code du plugin.
