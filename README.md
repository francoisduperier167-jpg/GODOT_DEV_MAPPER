# GODOT_DEV_MAPPER

Préparation d'un plugin pour Godot : **Godot Visual Program & Execution Explorer**. Il doit cartographier un projet Godot (architecture, logique, données, déroulement du jeu) et superposer à cette carte ce qui s'est réellement exécuté.

**Statut au 8 octobre 2026 : cadrage, premier spike fait.** Aucun code du plugin n'existe encore. SPIKE-01a a vérifié la partie jeu du canal du débogueur sur Godot 4.7.2 et 4.8-dev7. Le plan directeur, la méthodologie et l'orchestration sont proposés, pas encore validés.

## Contenu

| Chemin | Rôle |
| --- | --- |
| `docs/plan-directeur.md` | Plan directeur PD-0.3 : capacités, architecture, protocole de session, modèle de données, POC, MVP, budgets en heures, risques |
| `docs/methodologie.md` | Méthode de construction MC-0.3 : sources de vérité et leur hiérarchie, contrats, tests, CI, veille de Godot, gabarits |
| `docs/orchestration.md` | OR-0.3 : déroulé pas à pas, tâches T00 à T20, routage entre quatre modèles |
| `docs/construction/` | Guide de construction GC-0.1 : pour chaque étape, objectif, obligations, méthodologie, points de contrôle, amélioration et prompts de réalisation et de vérification |
| `docs/spikes/SPIKE-01.md` | Rapport de SPIKE-01a : canal du débogueur, partie jeu, mesuré sur 4.7.2 et 4.8-dev7 |
| `spikes/` | Prototypes jetables des spikes |
| `docs/estimation.md` | Historique : pertinence, faisabilité et raisonnement de charge initial, en sessions |
| `docs/feuille-de-route.svg` | Historique : feuille de route des prompts 2.1, en sessions cumulées |
| `docs/analyse-des-prompts-v2.0.md` | Historique : analyse critique des prompts initiaux |
| `prompts/conception.txt` | Historique : prompt de conception v2.2 |
| `prompts/methodologie.txt` | Historique : prompt de méthodologie v2.2 |

**En cas d'écart entre documents**, un fait mesuré dans un rapport de spike prime. Viennent ensuite le plan directeur (périmètre et budgets), l'orchestration (ordre des tâches) et la méthodologie (règles de travail). Les documents marqués « historique » expliquent d'où vient le plan ; ils ne le remplacent pas.

## Démarrer

1. Relire `docs/plan-directeur.md` et trancher les décisions bloquantes D-01, D-02, D-05 et D-07 (§10).
2. Suivre le guide `docs/construction/README.md` à partir de l'étape 0. Il donne, pour chaque tâche, le prompt de réalisation, les contrôles exécutables et le prompt de vérification.
3. La prochaine preuve qui exige ta machine est SPIKE-01b, la partie éditeur du canal (tâche T05). Beaucoup d'autres tâches peuvent avancer sans elle : le guide le précise étape par étape.

## Compatibilité avec les versions de Godot

Godot publie une version mineure tous les quelques mois, et une version mineure peut modifier certaines API. Le plugin isole donc tout appel sensible derrière une frontière de compatibilité : c'est l'invariant INV-09.

Avant la preuve de valeur, cette frontière reste légère : des façades, une CI bloquante sur Godot 4.7.2 et la préversion suivante testée à part. Les adaptateurs par version et la veille automatisée n'arrivent qu'au MVP, ou plus tôt si une rupture réelle apparaît.

## Orchestration des modèles

Claude Opus 5.5 prend les contrats, les façades de compatibilité, les spikes et le débogage difficile. Sonnet écrit le code de l'éditeur ; Gemini lit les jeux open source et relit les diffs de Sonnet. Qwen3.8-27B, exécuté localement, prend les tâches sous contrat validé et couvertes par des tests. Les outils sans IA exécutent les tests, le lint et les mesures.

Le parallélisme reste borné par la capacité de relecture humaine.

## Bancs d'essai

Les tests s'appuient sur des jeux Godot open source existants. Ne copier ni leur code ni leurs assets dans ce dépôt sans vérifier la compatibilité des licences. Les référencer par dépôt et révision, ou par sous-module Git.

## Versions des prompts

Chaque version est étiquetée :

- `prompts-v1` : prompts d'origine ;
- `prompts-v2.0` : révision et analyse critique ;
- `prompts-v2.1` : paramètres connus, analyse de l'existant, budget, contrat runtime phasé, bancs d'essai open source, orchestration multi-modèles ;
- `prompts-v2.2` : couche de compatibilité moteur et politique de versions (INV-09), avec le plan directeur, la méthodologie et l'orchestration.

La commande `git log --follow prompts/conception.txt` montre l'évolution d'un prompt.

## Licence

À définir avant la première ligne de code du plugin.
