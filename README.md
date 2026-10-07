# GODOT_DEV_MAPPER

Préparation d'un plugin pour Godot : **Godot Visual Program & Execution Explorer**. Il doit cartographier un projet Godot (architecture, logique, données, déroulement du jeu) et superposer à cette carte ce qui s'est réellement exécuté.

**Statut au 7 octobre 2026 : cadrage.** Aucun code du plugin n'existe encore. Le plan directeur, la méthodologie et l'orchestration sont proposés, pas encore validés.

## Contenu

| Chemin | Rôle |
| --- | --- |
| `docs/plan-directeur.md` | Plan directeur PD-0.1 : capacités, architecture, couche de compatibilité, modèle de données, POC, MVP, roadmap, risques |
| `docs/methodologie.md` | Méthode de construction MC-0.1 : sources de vérité, contrats, tests, CI multi-version, veille de Godot, gabarits |
| `docs/orchestration.md` | Déroulé pas à pas, vingt premières tâches, routage entre modèles |
| `docs/estimation.md` | Pertinence, faisabilité et charge |
| `docs/feuille-de-route.svg` | Feuille de route en sessions cumulées |
| `docs/analyse-des-prompts-v2.0.md` | Analyse critique des prompts initiaux |
| `prompts/conception.txt` | Prompt de conception v2.2 |
| `prompts/methodologie.txt` | Prompt de méthodologie v2.2 |

## Démarrer

1. Relire `docs/plan-directeur.md` et trancher les décisions bloquantes D-01, D-02, D-05 et D-07 (§10).
2. Suivre `docs/orchestration.md` à partir de l'étape 0.

## Compatibilité avec les versions de Godot

Godot publie une version mineure tous les quelques mois, et une version mineure peut modifier certaines API. Le plugin isole donc tout appel sensible dans une couche de compatibilité : c'est l'invariant INV-09.

La CI teste la version de développement, 4.7.x, de façon bloquante, et la préversion suivante, 4.8, sans bloquer. Une veille hebdomadaire relance les tests sur chaque nouvelle préversion officielle.

## Orchestration des modèles

Claude Opus 5.5, via Claude Code, prend les contrats, le protocole, les ports de compatibilité, les spikes et le débogage difficile. Qwen3.8-27B, exécuté localement, prend les tâches sous contrat validé et couvertes par des tests. Les outils sans IA exécutent les tests, le lint et les mesures.

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
