# MVP — Phases P4a à P8

Budget : 43 à 74 h humaines (39 à 68 h si AST Flow sert de backend statique) · Prérequis : revue T20 qui décide de continuer

Le MVP est décrit phase par phase. Son découpage en tâches dépend des résultats du POC : le prompt de découpage, en fin de page, le produit au début de chaque phase, au format des fiches du POC. Chaque tâche suit ensuite les prompts universels de réalisation et de vérification.

## Ordre et files

| Phase | Dépend de | Heures humaines | File |
| --- | --- | --- | --- |
| P4a Évaluations | T20 | 6–12 | A |
| P4b Backend statique et inventaire | P4a | 8–14, ou 4–8 avec AST Flow | A |
| P5 Navigation | P4b | 8–13 | A |
| P6 Historique, persistance, protocole MVP | T20 | 10–16 | B |
| P7 Logique et Game Flow annoté | P6 | 5–9 | B |
| P8 Compatibilité MVP et stabilisation | P5, P7 | 6–10 | A et B |

Deux files à 10 h par semaine : l'acquisition et la navigation d'un côté, le runtime et la persistance de l'autre.

## P4a — Évaluations : rendu et backend statique

- **Objectif.** Décider avec des mesures :
  - SPIKE-03 : GraphEdit, canevas dessiné ou hybride, à 50, 300 et 1 000 éléments visibles ;
  - SPIKE-04 : GDScript AST Flow ou extraction maison, sur le banc d'essai.
- **Obligations.** Code jetable dans `spikes/`. Mesures avec version et machine. Pour AST Flow : licence, version épinglée, plan de sortie, et passage obligé par une façade de syntaxe.
- **Méthodologie.** IA 1 conduit les deux spikes. Pour SPIKE-04, un jeu de relations attendues, écrit à la main sur une partie du banc d'essai, sert d'étalon. On compte les relations justes, fausses et manquées.
- **Points de contrôle.**
  - Temps de frame et latence d'interaction mesurés pour chaque option de rendu (objectif : 16 ms à 300 éléments).
  - Pour chaque backend : relations justes, fausses et manquées sur l'étalon (objectif : 90 % des appels directs résolus, aucune relation certaine fausse) ; coût d'intégration estimé.
  - Décisions consignées.
- **Amélioration.** Si aucune option de rendu ne tient : agréger, n'afficher qu'un voisinage, ou passer par une vue en liste. Si aucun backend n'atteint l'objectif : réduire le périmètre aux appels directs, avec « non résolu » pour le reste.

## P4b — Backend statique et inventaire (CAP-08, CAP-09)

- **Objectif.** Inventorier un jeu réel de plus de 300 scripts sans l'instancier, et en extraire les relations d'appel avec leur provenance.
- **Obligations.**
  - Erreurs isolées par fichier : un script illisible ne bloque pas l'inventaire.
  - Appels dynamiques marqués « non résolus », jamais devinés.
  - Backend tiers uniquement derrière la façade de syntaxe.
- **Méthodologie.** Tests d'abord, sur des fixtures maison couvrant chaque construction GDScript ciblée. Puis tests de référence (« golden ») sur le banc d'essai : leur fichier de relations attendues est relu par toi.
- **Points de contrôle.**
  - Inventaire de 300 scripts en 15 s au plus (objectif à valider).
  - Aucune relation certaine fausse sur le fichier de référence.
  - Fixture de syntaxe inconnue : signalée, sans plantage.
  - (CE) Une relation fausse ajoutée au résultat fait échouer le test de référence.
- **Amélioration.** Si l'inventaire est trop lent : cache par révision de fichier, puis indexation incrémentale. Chaque faux positif découvert devient une fixture.

## P5 — Navigation et arborescence res:// (CAP-10)

- **Objectif.** Retrouver appelants et appelés, chercher une définition, et aller d'un fichier de res:// à son élément du graphe.
- **Obligations.** Expansion bornée : jamais de graphe complet affiché d'un coup. Toute relation affichée montre sa provenance.
- **Méthodologie.** Les requêtes vivent dans `projections/` et sont testées sans interface ; l'interface suit le rendu choisi en P4a.
- **Points de contrôle.**
  - Tests de requêtes verts.
  - Test de cartographie, chronométré avec et sans l'outil :
    - retrouver tous les appelants d'une fonction ;
    - expliquer un système inconnu du banc d'essai.
  - Le gain doit être réel, coût d'installation compris.
- **Amélioration.** Si le test de cartographie ne montre aucun gain, on revoit l'ergonomie de la recherche avant d'ajouter des vues.

## P6 — Historique, persistance, protocole MVP (CAP-11, CAP-07 complet)

- **Objectif.** Recharger et relire une session sans le jeu. Survivre à une connexion tardive et à une reconnexion. Marquer les lacunes explicitement.
- **Obligations.**
  - Formats persistés versionnés et sauvegarde atomique.
  - Refus explicite d'une version inconnue.
  - Négociation de capacités dans le protocole.
  - Frames et ticks physiques horodatés.
  - Toute rupture d'un format persisté exige ta validation.
- **Méthodologie.** Une tâche de révision de contrat, confiée à IA 1, étend C-04 et C-06 avec un changement de version : elle liste `docs/CONTRACTS.md`, `contracts/` et `tests/contract/` dans ses fichiers autorisés, et passe par ta validation. IA 2 implémente ensuite sous contrat. Les sessions enregistrées du POC deviennent des fixtures de compatibilité ascendante.
- **Points de contrôle.**
  - Une session du POC rechargée par le MVP.
  - Reconnexion testée sur le banc sans éditeur.
  - (CE) Un fichier tronqué est refusé, avec un message clair.
- **Amélioration.** Chaque bug de persistance devient une fixture permanente.

## P7 — Logique et Game Flow annoté (CAP-12 annoté)

- **Objectif.** Afficher les décisions et les états, ainsi que les blocs temporels déclarés et leurs occurrences.
- **Obligations.** Seuls les blocs déclarés s'affichent, pas les blocs inférés. Un bloc interrompu s'affiche « incomplet ». Le cycle de vie des blocs suit le plan §6.
- **Méthodologie.** Contrat d'abord (événements block_begin et block_end, déjà prévus au MVP), puis projections testées, puis interface.
- **Points de contrôle.**
  - Bloc interrompu affiché « incomplet » sur une fixture.
  - Blocs imbriqués corrects.
  - (CE) Un bloc sans fin marqué « terminé » fait échouer le test.
- **Amélioration.** Si déclarer des blocs coûte trop cher, on mesure ce coût, puis on étudie des modèles de déclaration réutilisables.

## P8 — Compatibilité MVP et stabilisation (CAP-13)

- **Objectif.** Publier la matrice de compatibilité générée par la CI. Basculer vers 4.8 stable quand elle sort. Installer et désinstaller le plugin proprement.
- **Obligations.**
  - L'outil de désinstallation liste les appels FlowTrace et refuse de retirer le dossier runtime s'il en reste.
  - Les adaptateurs par version n'apparaissent que si une rupture est constatée.
  - Toute rupture se corrige dans la frontière de compatibilité.
- **Méthodologie.** IA 2 trie les échecs de la préversion ; IA 1 intervient si une API change de sens. Tu fais une installation propre de bout en bout.
- **Points de contrôle.**
  - CI verte sur la fenêtre de support.
  - Matrice publiée.
  - Installation, puis désinstallation, sans résidu.
  - Porte MVP du plan §9 franchie.
- **Amélioration.** Si 4.8 stable casse des choses, chaque rupture devient un test de compatibilité ; la veille automatisée s'active.

## Porte du MVP

C'est la porte du plan §9 :
- un jeu réel de 300 scripts ou plus indexé sans l'instancier ;
- test de cartographie gagnant ;
- session rechargée ;
- installation et désinstallation propres ;
- CI verte sur la fenêtre de support.

Le prompt de porte d'étape du `README.md` s'applique, avec ces critères.

## Prompt de découpage d'une phase

```text
Tu découpes la phase {Px} du projet GODOT_DEV_MAPPER en tâches exécutables, au format des fiches de docs/construction/etape-4.md.

ENTRÉES : docs/plan-directeur.md (§3, capacités {CAP} ; §9, porte de la phase) ; docs/construction/mvp.md, section {Px} ; docs/DECISIONS.md ; docs/spikes/ ; PROJECT_STATE.md (budget consommé, taux de réussite par IAdèle) ; docs/revues/revue-poc.md.

PRODUIS docs/construction/mvp-{Px}.md :
- objectif, obligations, méthodologie, points de contrôle et cheminement d'amélioration de la phase, précisés par les résultats du POC ;
- de 4 à 12 tâches. Chacune avec : modèle, autonomie, dépendances, fichiers autorisés, pack de contexte, contrôles exécutables dont au moins une contre-épreuve, et prompt de réalisation rempli à partir du prompt universel.

RÈGLES
- Une tâche tient en 1 à 3 h de travail agent et en 1 h de relecture humaine au plus.
- Une tâche qui touche un format persisté, le protocole ou une façade est vérifiée par IA 1.
- Les contrats et leurs tests précèdent l'implémentation, comme à l'étape 3. Une tâche qui révise un contrat liste explicitement `docs/CONTRACTS.md`, `contracts/` et `tests/contract/` dans ses fichiers autorisés ; IA 1 la réalise, IA 3 la vérifie, tu la valides.
- Chaque tâche précise les marqueurs de `tests/pending/` qu'elle crée ou supprime, et les scripts de `tools/ci/checks.d/` qu'elle ajoute. Aucune ne modifie `PROJECT_STATE.md` ni `docs/DECISIONS.md`.
- Le total reste dans le budget de la phase ({budget} h humaines). Sinon, tu signales le dépassement et proposes quoi retirer.
- Ne réalise aucune tâche.
```
