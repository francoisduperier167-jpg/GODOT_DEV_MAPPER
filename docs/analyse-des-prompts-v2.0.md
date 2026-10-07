# Analyse et révision des deux prompts

7 octobre 2026 — Godot Visual Program & Execution Explorer

## Appréciation générale

Les deux prompts constituent une vision produit riche et déjà réfléchie. Leurs points les plus solides sont la séparation modèle/interface, la distinction définition/instance, la reconnaissance des limites de l’analyse statique, l’instrumentation progressive, les tranches verticales et les règles contre les APIs inventées. La révision conserve ces choix.

Le problème principal tient à l’écart entre cette prudence et certaines demandes très larges : carte « complète », MVP comportant de nombreuses vues, stabilisation précoce, dizaines de rubriques obligatoires et processus détaillé pour chaque tâche. Une IA peut satisfaire la forme en produisant un document volumineux sans résoudre les arbitrages décisifs.

La révision cherche donc à obtenir des décisions vérifiables : quelle information est réellement accessible, comment elle est acquise, ce que l’on peut en conclure et quelle expérience démontrera la prochaine capacité.

Les fichiers livrés restent des **prompts prêts à utiliser**. Ils ne constituent ni le plan directeur du plugin, ni sa méthodologie déjà exécutée, ni une implémentation.

## Changements prioritaires

Les références C et M désignent les sections des fichiers d’origine, respectivement conception et méthodologie.

| Point relevé | Pourquoi le préciser | Modification apportée |
| --- | --- | --- |
| « Modèle complet » et prudence sur l’extraction automatique coexistent (C2, C38) | Le lecteur peut confondre ambition globale et couverture garantie | Modèle global potentiellement partiel ; couverture, provenance et inconnues explicites |
| Architecture et temporalité se mélangent dans une seule descente hiérarchique (C5) | Un script peut servir plusieurs niveaux ; une rencontre mobilise plusieurs systèmes | Hiérarchies distinctes, reliées par des références ; occurrences séparées des définitions |
| Axe horizontal temporel imposé largement (C6) | Une disposition logique n’indique pas nécessairement une durée | Vue sémantique distincte de la timeline métrique, avec unité et agrégation explicites |
| Runtime très détaillé, acquisition inégalement précisée (C20, C39) | Un canal de communication ne capture pas spontanément tous les événements | Mécanisme de production exigé pour chaque type d’événement et capacité |
| Identités et liens source insuffisamment définis (C15, C19, M6–7) | Lignes, chemins, objets et sessions évoluent | Révision du code, ancrages source, identité de session et corrélations d’occurrences |
| Sampling et conservation de tous les événements importants (C22) | Une mémoire bornée peut déborder, même pour des événements prioritaires | Politique de saturation, pertes comptées, lacunes visibles et absence de garantie absolue |
| Diagnostic après absence d’événement (C23–25) | Filtrage, perte ou capture inactive peuvent expliquer cette absence | « Non observé » distinct de « non exécuté » ; diagnostic limité aux preuves disponibles |
| History/replay non défini (C42, M34) | Relire une trace et rejouer exactement le jeu n’ont pas le même coût | Relecture du journal au périmètre initial ; rejeu déterministe traité séparément |
| MVP très étendu malgré l’exigence de réalisme (C41) | Trop de chantiers avant une preuve utile | POC réduit, MVP utile sur petit projet réel, fonctions avancées explicitement reportées |
| « Tu disposes déjà » d’un prompt maître (M introduction) | Un prompt n’est pas un résultat validé, encore moins un dépôt existant | Entrée explicite : plan directeur, révision, décisions approuvées, état réellement fourni |
| Hiérarchie linéaire des documents (M3) | Les tests peuvent être faux et les contrats devoir évoluer | Autorité par domaine et procédure de résolution des contradictions |
| Gel précoce et neuf passes systématiques (M6, M13) | Coût excessif pour un petit projet et apprentissage ralenti | Invariants durables, contrats graduels, boucle proportionnée au risque |
| EXPERIMENTAL/INTERNAL/STABLE/PUBLIC sur un même axe (M40) | Maturité et visibilité sont deux propriétés différentes | Deux axes distincts : expérimental/stable et interne/public |
| Interdiction absolue des TODO et exigence de fichier complet (M14, M22) | Peut favoriser réécritures inutiles ou dissimulation des limites | Patch ciblé accepté ; aucun faux achèvement ; dette hors périmètre explicitement suivie |
| Vingt tâches entièrement détaillées dès le départ (M56) | Les résultats des premiers prototypes changeront probablement la suite | Vingt tâches ordonnées ; cinq détaillées ; reste conditionnel aux preuves |

## Ce qui est ajouté

Les ajouts répondent aux risques propres à cet outil, sans ajouter de nouvelles ambitions produit majeures :

- **Provenance et fraîcheur** : distinguer origine des données, résolution, observation et validité après changement du code.
- **Causalité** : conserver les liens effectivement connus ; des timestamps proches ne prouvent pas qu’un événement en a provoqué un autre.
- **Durées** : séparer temps écoulé, temps actif et CPU ; une fonction suspendue n’occupe pas nécessairement le processeur pendant toute sa durée.
- **Contrat runtime** : session, producteur, séquence, horloge, corrélations, messages incomplets, versions et capacités.
- **Fiabilité opérationnelle** : absence de debugger, réactivation du plugin, arrêt brutal, références périmées et fichiers invalides pendant l’édition.
- **Données et exports** : représentation des identifiants sans perte, validation des imports, distinction caches/déclarations/traces, contrôle des champs partagés dans un snapshot IA.
- **Maintenabilité** : ne pas écraser les annotations humaines lors de la réindexation ; séparer les dépendances du runtime de celles de l’éditeur.
- **Validation** : distinguer tests proposés, réellement exécutés et réussis ; préciser ce qu’un test headless ne couvre pas.

Le vocabulaire commun INV-01 à INV-08 et le dossier de passage rendent les deux prompts compatibles. La méthodologie reprend le résultat de conception au lieu de reconstruire sa propre vision.

## Vérifications techniques Godot

Ces vérifications documentaires soutiennent la révision. Elles ne constituent pas des tests du plugin. Les pages officielles `/stable` ont été consultées le 7 octobre 2026 ; leur URL évolutive ne remplace pas le choix d’une version exacte du moteur. Les prompts demandent donc une vérification sur la branche retenue avant l’implémentation.

| Constat documentaire | Conséquence dans les prompts |
| --- | --- |
| [EngineDebugger](https://docs.godotengine.org/en/stable/classes/class_enginedebugger.html) expose notamment l’activité du debugger, l’envoi de messages et leur capture | Une voie de transport est plausible ; son activation et son comportement dégradé doivent être vérifiés |
| [EditorDebuggerPlugin](https://docs.godotengine.org/en/stable/classes/class_editordebuggerplugin.html) reçoit les messages et gère des sessions, potentiellement inactives | Distinguer session créée, session active et capture en cours ; vérifier le cycle de vie |
| [Script](https://docs.godotengine.org/en/stable/classes/class_script.html) documente l’accès à des métadonnées de méthodes, propriétés, signaux et au texte source lorsqu’il existe | Ces informations ne constituent pas, à elles seules, un graphe d’appels résolu ; l’extraction et la résolution demandent une stratégie distincte |
| [GraphEdit](https://docs.godotengine.org/en/stable/classes/class_graphedit.html) fournit un conteneur graphique et des interactions dont la logique est à implémenter | Choisir son usage après un prototype de rendu ; garder le modèle métier indépendant |
| [Thread-safe APIs](https://docs.godotengine.org/en/stable/tutorials/performance/thread_safe_apis.html) indique notamment que l’interaction avec l’arbre de scène actif n’est pas thread-safe | Ne pas déplacer arbitrairement collecte, indexation et interface sur des threads secondaires |
| [Time](https://docs.godotengine.org/en/stable/classes/class_time.html) distingue les horloges système des ticks monotones | Spécifier les domaines d’horloge et mesurer les durées avec un mécanisme approprié |
| [The Profiler](https://docs.godotengine.org/en/stable/tutorials/scripting/debug/the_profiler.html) explique le coût du profiling et les mesures inclusive/self | Mesurer le coût de l’observation et définir précisément la métrique affichée |
| [Running code in the editor](https://docs.godotengine.org/en/stable/tutorials/plugins/running_code_in_the_editor.html) décrit l’exécution des scripts @tool dans l’éditeur | Évaluer les effets du chargement et de l’instanciation lors de l’indexation |

Les recommandations sur les identités, les lacunes de trace et le découpage du MVP sont des choix d’architecture proposés dans cette analyse. Elles ne sont pas présentées comme des contraintes imposées par Godot.

## Couverture conservée

La révision regroupe les rubriques ; elle n’élimine pas les modes avancés de la vision. Le report après le MVP est explicite.

| Sections originales de conception | Sections révisées | Traitement |
| --- | --- | --- |
| 1–3 | 1, 3–5 | Vision et invariants conservés ; Data Flow devient une dimension explicite |
| 4–7 | 4, 8 | Temporalité, hiérarchies, granularité et lanes clarifiées |
| 8–14, 29 | 5, 7, 11 | Groupes, appels, branches, navigation et arborescence conservés |
| 15–18 | 5–7, 10 | Explications, descriptions et origine des valeurs conservées |
| 19–22 | 7–9 | Instances, événements, illumination et buffers précisés |
| 23–28 | 5, 10 | Expected/Actual, comparaison, Diagnostic, Explain, Tune et InterventionPoints conservés |
| 30–31 | 4, 8 | Game Flow et blocs temporels avec occurrences distinctes |
| 32–34 | 5, 12 | Performance, contexte IA et toutes les vues conservés |
| 35–37 | 7, 11 | Modèle, architecture et rendu regroupés |
| 38–39 | 6, 9 | Acquisition et instrumentation reliées aux preuves |
| 40–42 | 13 | Roguelike conservé ; POC et MVP resserrés |
| 43–45 | 6, 12, 14 | Risques, performance, formats et persistance regroupés |
| 46–50 | 1, 3, 13–14 | Ambition, priorisation, réalisme et livrable conservés |

| Sections originales de méthodologie | Sections révisées | Traitement |
| --- | --- | --- |
| 1–4 | 1–4 | Constitution, documentation, autorité et ADR clarifiés |
| 5–8 | 4–5 | Contrats, données, protocole et dépendances conservés |
| 9–12 | 6–7, 13 | Tranches, capacités, tâches et micro-prompts reliés |
| 13–17 | 8–9, 11 | Boucle simplifiée ; code, version, typage et tests préservés |
| 18–23 | 9, 12 | Tests, fixtures, roguelike, DoD et jalons conservés |
| 24–28 | 4, 8, 11 | Changements, migrations, revue et correction proportionnés |
| 29–33 | 7, 13 | État, context packs et rappels d’invariants regroupés |
| 34–37 | 6, 12 | Roadmap, preuve de valeur et prototypes rapprochés |
| 38–40 | 4, 10 | Budgets et observabilité conservés ; stabilité/visibilité séparées |
| 41–44 | 11 | Git, commits, refactoring et dette regroupés |
| 45–47 | 1, 8–9, 11 | Vérification des APIs et discipline Godot conservées |
| 48–53 | 7–8, 12–14 | Validation, autonomie, checklists et continuité proportionnées |
| 54–60 | 12–14 | Livrables et vingt tâches conservés avec détail progressif |

## Taille et compromis éditoriaux

Comptage indicatif par éléments séparés par des espaces ; les nombres, symboles et éléments de tableau peuvent être comptés comme des mots.

| Prompt | Original | Révision | Réduction | Grandes sections |
| --- | ---: | ---: | ---: | --- |
| conception.txt | 4 341 | 3 121 | 28,1 % | 50 → 14 |
| methodologie.txt | 4 286 | 3 074 | 28,3 % | 60 → 14 |

Les nombreuses lignes vides ont également été supprimées. La réduction du nombre de lignes ne doit pas être confondue avec une réduction équivalente du contenu.

Les versions restent substantielles pour préserver la vision. Les exemples répétitifs et les longues listes de titres ont été comprimés ; l’espace récupéré précise surtout les garanties techniques et les décisions attendues. Les nomenclatures de classes et l’arborescence restent à proposer, plutôt que d’être imposées avant validation.

## Utilisation recommandée

1. Utiliser **conception.txt** pour produire le plan directeur, en ajoutant les contraintes déjà connues : version Godot, projet cible, équipe et disponibilité.
2. Examiner en priorité les hypothèses, le POC, le MVP, les risques et les décisions à confirmer. Marquer explicitement les décisions acceptées.
3. Fournir ce résultat et son dossier de passage avec **methodologie.txt**. Ajouter l’état réel du dépôt s’il existe.
4. Utiliser ensuite les tâches et micro-prompts produits par la méthodologie pour construire progressivement le plugin.

Il n’est pas nécessaire de remplir artificiellement tous les paramètres avant de lancer la conception : les versions révisées autorisent des hypothèses réversibles, tout en signalant ce qui bloque réellement un prototype exécutable.

## Vérifications effectuées sur cette révision

Lecture intégrale des deux sources, comparaison de leur couverture fonctionnelle, harmonisation des huit invariants, contrôle des références entre les prompts et consultation des huit pages officielles ci-dessus. Aucun code Godot ni test de performance n’a été exécuté : la tâche portait sur l’analyse et la réécriture des prompts.
