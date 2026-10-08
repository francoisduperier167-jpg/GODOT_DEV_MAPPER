# GODOT_DEV_MAPPER

Préparation d'un plugin pour Godot : **Godot Visual Program & Execution Explorer**. Il doit cartographier un projet Godot (architecture, logique, données, déroulement du jeu) et superposer à cette carte ce qui s'est réellement exécuté.

**Statut au 8 octobre 2026 : cadrage, premier spike fait.** Aucun code du plugin n'existe encore. SPIKE-01a a vérifié la partie jeu du canal du débogueur sur Godot 4.7.2 et 4.8-dev7. Le plan directeur, la méthodologie et l'orchestration sont proposés, pas encore validés. Mode d'exécution proposé : trois IA à tour de rôle, une unité après l'autre, recette humaine à la fin (D-09).

## Contenu

| Chemin | Rôle |
| --- | --- |
| `docs/plan-directeur.md` | Plan directeur PD-0.5 : capacités, architecture, protocole de session, modèle de données, POC, MVP, budgets, risques, mode d'exécution |
| `docs/methodologie.md` | Méthode de construction MC-0.5 : sources de vérité et leur hiérarchie, contrats, tests, CI, veille de Godot, gabarits |
| `docs/orchestration.md` | OR-0.5 : tâches T00 à T20, dépendances, routage entre les modèles |
| `docs/construction/` | Guide de construction GC-0.4 et sa carte interactive `carte.html` : pour chaque étape, objectif, obligations, méthodologie, points de contrôle, amélioration et prompts de réalisation et de vérification |
| `docs/construction/sequence.md` | Déroulé séquentiel du mode autonome : ordre des 35 unités du POC puis des phases, rôles des trois IA, prompt de créneau, arrêts obligatoires, recette finale |
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
1. Donne à chaque IA, au début de chacun de ses créneaux, le prompt de créneau de `docs/construction/sequence.md` (§4), avec son nom et son rôle.
2. La première IA au rôle de concepteur commence par l'unité S01, le dossier de décisions. Les suivantes enchaînent seules, une unité après l'autre.
3. Tu n'interviens qu'à la recette finale (§8), ou si un fichier `rapports/ARRET.md` apparaît sur `main` (§6).

**En mode piloté**, le mode d'origine :
1. Relire `docs/plan-directeur.md` et trancher les décisions bloquantes D-01, D-02, D-05 et D-07 (§10).
2. Ouvrir la carte interactive `docs/construction/carte.html` : elle affiche la prochaine action, le modèle à lancer et le prompt à copier. Le guide `docs/construction/README.md` en est la référence détaillée.

SPIKE-01b, la partie éditeur du canal (tâche T05), peut s'exécuter sous écran virtuel avec un rendu logiciel : c'est vérifié sur Godot 4.7.2 le 8 octobre 2026. Seule la mesure de débit sur GPU attend ta machine.

## Compatibilité avec les versions de Godot

Godot publie une version mineure tous les quelques mois, et une version mineure peut modifier certaines API. Le plugin isole donc tout appel sensible derrière une frontière de compatibilité : c'est l'invariant INV-09.

Avant la preuve de valeur, cette frontière reste légère : des façades, une CI bloquante sur Godot 4.7.2 et la préversion suivante testée à part. Les adaptateurs par version et la veille automatisée n'arrivent qu'au MVP, ou plus tôt si une rupture réelle apparaît.

## Orchestration des modèles

Claude Opus 5.5 prend les contrats, les façades de compatibilité, les spikes et le débogage difficile. Sonnet écrit le code de l'éditeur ; Gemini lit les jeux open source et relit les diffs de Sonnet. Qwen3.8-27B, exécuté localement, prend les tâches sous contrat validé et couvertes par des tests. Les outils sans IA exécutent les tests, le lint et les mesures.

En mode autonome, trois IA tiennent trois rôles : concepteur, développeur, vérificateur (`docs/construction/sequence.md`, §2). L'auteur d'une unité ne la vérifie jamais.

## Bancs d'essai

Les tests s'appuient sur des jeux Godot open source existants. Ne copier ni leur code ni leurs assets dans ce dépôt sans vérifier la compatibilité des licences. Les référencer par dépôt et révision, ou par sous-module Git.

## Versions des prompts

Chaque version correspond à un commit de l'historique. Les étiquettes ci-dessous sont prévues, mais pas encore créées sur le dépôt distant :

- `prompts-v1` : prompts d'origine ;
- `prompts-v2.0` : révision et analyse critique ;
- `prompts-v2.1` : paramètres connus, analyse de l'existant, budget, contrat runtime phasé, bancs d'essai open source, orchestration multi-modèles ;
- `prompts-v2.2` : couche de compatibilité moteur et politique de versions (INV-09), avec le plan directeur, la méthodologie et l'orchestration.

La commande `git log --follow prompts/conception.txt` montre l'évolution d'un prompt.

## Licence

À définir avant la première ligne de code du plugin.
