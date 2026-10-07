# GODOT_DEV_MAPPER

Préparation d'un plugin pour Godot 4.7 : **Godot Visual Program & Execution Explorer**. Il doit cartographier un projet Godot (architecture, logique, données, déroulement du jeu) et superposer à cette carte ce qui s'est réellement exécuté.

**Statut au 7 octobre 2026 : cadrage.** Aucun code du plugin n'existe encore. Le dépôt contient les prompts qui produiront le plan directeur et la méthode de construction, ainsi qu'une estimation de charge.

## Contenu

| Chemin | Rôle |
| --- | --- |
| `prompts/conception.txt` | Prompt de conception v2.1 : produit le plan directeur |
| `prompts/methodologie.txt` | Prompt de méthodologie v2.1 : produit la méthode de construction, dont l'orchestration entre modèles |
| `docs/estimation.md` | Pertinence, faisabilité, réalisme et charge en sessions, heures et calendrier |
| `docs/feuille-de-route.svg` | Feuille de route en sessions cumulées, avec les jalons POC, MVP et V1 |
| `docs/analyse-des-prompts-v2.0.md` | Analyse critique des prompts initiaux, à l'origine de la v2.0 |

## Utilisation

1. Compléter les champs entre crochets de la section 2 de `prompts/conception.txt` : heures par semaine, système d'exploitation, jeux open source de test, matériel du modèle local.
2. Lancer le prompt de conception, relire le plan directeur et marquer les décisions acceptées.
3. Lancer le prompt de méthodologie avec le plan directeur et son dossier de passage.
4. Construire tâche par tâche en suivant la méthode produite et son plan d'orchestration.

## Orchestration des modèles

Le prompt de méthodologie répartit le travail entre trois niveaux. Claude Opus 5.5, via Claude Code, prend les contrats, le protocole, les spikes et le débogage difficile. Qwen3.8-27B, exécuté localement, prend les tâches sous contrat validé et couvertes par des tests. Les outils sans IA exécutent les tests, le lint et les mesures.

Le parallélisme reste borné par la capacité de relecture humaine.

## Bancs d'essai

Les tests s'appuient sur des jeux Godot open source existants. Ne copier ni leur code ni leurs assets dans ce dépôt sans vérifier la compatibilité des licences. Les référencer par dépôt et révision, ou par sous-module Git.

## Versions des prompts

Chaque version est étiquetée :

- `prompts-v1` : prompts d'origine ;
- `prompts-v2.0` : révision et analyse critique ;
- `prompts-v2.1` : paramètres connus, analyse de l'existant, budget et critère d'arrêt, contrat runtime phasé, bancs d'essai open source, orchestration multi-modèles.

La commande `git log --follow prompts/conception.txt` montre l'évolution d'un prompt.

## Licence

À définir avant la première ligne de code du plugin.
