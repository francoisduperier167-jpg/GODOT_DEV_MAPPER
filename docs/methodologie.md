# Méthodologie de construction — Godot Visual Program & Execution Explorer

Révision MC-0.1 · statut : **proposé** · 7 octobre 2026 · entrées : `prompts/methodologie.txt` v2.2, `docs/plan-directeur.md` PD-0.1 (proposé)

La partie 9, les vingt premières tâches et le déroulé pas à pas, est dans `docs/orchestration.md`, qui sert de backlog vivant.

## 1. Hypothèses, entrées réelles et mode d'emploi

| Élément | État au 7 octobre 2026 |
| --- | --- |
| Prompt de méthodologie | v2.2, fourni |
| Plan directeur | PD-0.1, fourni, non validé |
| Estimation | `docs/estimation.md`, fournie |
| Dépôt GODOT_DEV_MAPPER | Documents seulement, aucun code |
| Décisions approuvées | Aucune, hors paramètres connus |
| Versions de Godot | 4.7.x pour le développement, préversion 4.8 suivie |
| Outils de test | Non choisis (D-05) ; aucune commande n'est encore vérifiée |

Mode d'emploi :

1. Valider le plan directeur, au minimum les décisions bloquantes D-01, D-02, D-05 et D-07.
2. Créer les documents de démarrage du §2, en squelette.
3. Exécuter les étapes de `docs/orchestration.md` dans l'ordre ; les tâches d'une même étape peuvent avancer en parallèle.
4. Tenir la revue de continuation à la fin du POC (tâche T20).

Tant que D-01 n'est pas tranchée, aucun code ne peut être déclaré compatible.

## 2. Sources de vérité et documentation

| Domaine | Référence |
| --- | --- |
| Besoin, périmètre, acceptation | `docs/SPEC.md` et décisions produit validées |
| Choix durables | ADR acceptés |
| Modules et dépendances | `docs/ARCHITECTURE.md`, aligné sur les ADR |
| Formats et interfaces | `docs/CONTRACTS.md` |
| Versions de Godot | `docs/COMPATIBILITY.md` et `compat/versions.json` |
| Comportements vérifiés | Tests, fixtures et résultats CI rattachés à une révision |
| Prochaine action et état | `docs/orchestration.md` et `PROJECT_STATE.md` |

Un test peut être faux, un contrat peut devoir évoluer : une contradiction ouvre une analyse d'impact, jamais une retouche discrète pour faire passer un test.

| Fichier, à créer | Contenu | Normatif | Mis à jour quand |
| --- | --- | --- | --- |
| `docs/SPEC.md` | Extrait des §1 à 3 du plan | Oui | Décision produit |
| `docs/ARCHITECTURE.md` | Modules, dépendances, couche de compatibilité | Oui | ADR accepté |
| `docs/CONTRACTS.md` | C-01 à C-07 | Oui | Changement de contrat |
| `docs/COMPATIBILITY.md` | Fenêtre de support, matrice générée par la CI, ruptures connues | Fenêtre oui, matrice non | Chaque version de Godot |
| `docs/TEST_PLAN.md` | Stratégie, commandes vérifiées | Oui | Nouvelle catégorie de test |
| `PROJECT_STATE.md` | État réel, budget consommé, mesures, dette | Non | Fin de tâche |
| `docs/adr/` | Décisions | Oui, une fois acceptées | Décision |
| `CLAUDE.md` | Règles courtes pour les agents, 200 lignes au plus | Oui | Correction répétée deux fois |

Au POC, SPEC, ARCHITECTURE et CONTRACTS peuvent tenir dans un même fichier. On extrait DATA_MODEL, RUNTIME_PROTOCOL ou GRAPH_MODEL quand un contrat devient stable ou que CONTRACTS dépasse environ 400 lignes. Une définition n'existe qu'à un seul endroit.

## 3. Invariants, décisions, contrats et dépendances

| Invariant | Règle |
| --- | --- |
| INV-01 | Modèle indépendant des widgets et de la vue |
| INV-02 | Définition, instance et occurrence distinctes |
| INV-03 | Provenance conservée : extraite, déclarée, observée, inférée |
| INV-04 | Non observé ne signifie pas non exécuté |
| INV-05 | Chronologie, causalité et intention distinctes |
| INV-06 | Runtime indépendant de l'éditeur |
| INV-07 | Collecte, stockage et affichage bornés ; pertes visibles |
| INV-08 | Traces et liens rattachés à une révision |
| INV-09 | API moteur sensibles uniquement via la couche de compatibilité ; versions supportées vérifiées en CI |

**ADR.** Format : problème, contexte, options, décision, conséquences, périmètre, statut, date, preuves, liens, condition de réexamen. Les ADR sont réservés aux choix difficiles à inverser ou qui touchent plusieurs modules. Premiers candidats : ADR-001 modèle indépendant de l'interface ; ADR-002 définition, instance et occurrence ; ADR-003 buffer local et lots ; ADR-004 couche de compatibilité et fenêtre de support ; ADR-005 rendu, après SPIKE-03 ; ADR-006 backend statique, après SPIKE-04 ; ADR-007 helper runtime autonome.

**Contrats.** Chaque contrat de la tranche active précise : responsabilité, propriétaire, consommateurs, entrées, sorties, types, invariants, erreurs, dépendances autorisées et interdites, contexte d'exécution et contraintes de thread, version, comportement dégradé, exemples valides et invalides, tests de contrat. Deux axes distincts : maturité (expérimental, stable) et visibilité (interne, public). Une évolution additive compatible passe par la tâche qui la porte ; une rupture d'un format persisté exige analyse d'impact, migration et validation humaine.

**Dépendances.** La matrice du plan directeur (§4) est la règle. Un script `tools/check_deps` vérifie à chaque CI :

- les `preload`, `load`, `extends` et références de classes entre dossiers de modules ;
- la présence de noms d'API sensibles (EditorInterface, EditorPlugin, EditorDebuggerPlugin, EngineDebugger, GraphEdit, ClassDB, ProjectSettings, entre autres) hors de `compat/` et de `plugin.gd`.

Ce contrôle textuel ne voit pas les appels dynamiques ; la revue ciblée le complète.

## 4. Première tranche, prototypes et budgets

| Spike | Question | Mesure | Succès | Durée max |
| --- | --- | --- | --- | --- |
| SPIKE-01 | Un message du jeu atteint-il le plugin, et après un redémarrage ? | Débit, latence, pertes | 2 000 événements par seconde en lots sans perte ; redémarrage propre | 1 session |
| SPIKE-02 | Détection de capacités, UID et isolation de compilation tiennent-ils sur 4.7.x et 4.8 ? | Erreurs de compilation, comportement | Plugin actif sur les deux versions | 1 session |
| SPIKE-03 | Quel rendu tient 300 éléments visibles ? | Temps de frame, latence d'interaction | 16 ms au plus à 300 éléments | 1 à 2 sessions |
| SPIKE-04 | GDScript AST Flow ou extraction maison ? | Relations correctes, fausses, manquées ; coût d'intégration | 90 % des appels directs résolus, aucune relation certaine fausse | 1 à 2 sessions, au début du MVP |
| SPIKE-05 | Quel surcoût de capture ? | Temps de frame avec et sans | 5 % au plus à 1 000 événements par seconde | 1 session, dans T11 |
| SPIKE-06 | Le modèle local tient-il des tâches sous contrat ? | Réussite au premier essai, escalades, temps | 2 tâches sur 3 sans escalade | Mesuré pendant l'étape 4 |

Chaque spike vit dans `spikes/`, hors du plugin, et se conclut par KEEP, REWRITE ou DISCARD dans `docs/spikes/`. Sans exécution réelle, son résultat reste « à vérifier ».

La première tranche, les phases et leurs budgets sont ceux du plan directeur (§9). `PROJECT_STATE.md` suit la consommation réelle ; un dépassement de 50 % déclenche une revue de continuation sans attendre la fin de phase.

## 5. Tâches, contexte, autonomie et orchestration

**Fiche de tâche** : gabarit au §8. Une tâche a un objectif vérifiable, un périmètre réversible et un risque principal ; sa taille ne se mesure pas en nombre de fichiers.

**Autonomie**

| Niveau | Mandat |
| --- | --- |
| A0 | Exploration ou proposition, sans modification fusionnée |
| A1 | Modification réversible dans des contrats établis, avec vérifications |
| A2 | Capacité traversant plusieurs modules, quand interfaces et preuves sont solides |

Un mandat couvre les étapes mécaniques de son périmètre. Une validation humaine reste requise pour : changement de périmètre, rupture d'un format persisté, migration destructrice, nouvelle dépendance, élargissement de la fenêtre de support.

**Boucle de travail**

1. Lire la tâche, l'état réel du dépôt et les contraintes.
2. Vérifier les API inconnues et les contrats touchés ; signaler les écarts.
3. Définir la preuve de réussite ; plan bref si la tâche n'est pas triviale.
4. Implémenter le seul périmètre autorisé.
5. Exécuter les vérifications ; corriger les erreurs observées.
6. Relire contre les invariants et les critères d'acceptation.
7. Mettre à jour les références et produire le rapport.

**Context packs**

| Pack | Contenu | Taille cible pour le modèle local |
| --- | --- | --- |
| CORE | C-01, C-02, C-05, extraits d'ARCHITECTURE | 12K tokens au plus |
| RUNTIME | C-04, C-07, ADR-003, extraits des ports runtime | 12K tokens au plus |
| EDITOR | C-03 côté éditeur, C-06, ADR-005 | 16K tokens au plus |
| COMPAT | C-03, `versions.json`, liste des API sensibles, extraits des guides de migration | 16K tokens au plus |
| ACQUISITION | C-05, ADR-006, fixtures statiques | 16K tokens au plus |

Chaque pack cite ses révisions ; un résumé ne remplace pas la lecture du dépôt quand elle est possible.

**Orchestration des modèles**

| Travail | Niveau | Lieu |
| --- | --- | --- |
| Cadrage, ADR, contrats, protocole, ports de compatibilité | Grand modèle (Claude Opus 5.5) et validation humaine | Distant |
| Spikes, interprétation des mesures | Grand modèle | Distant, Godot local |
| Implémentation sous contrat validé avec tests fournis | Modèle local (Qwen3.8-27B) | Local |
| Tests, fixtures, sérialisation, adaptateurs, documentation | Modèle local | Local |
| Interface éditeur | Modèle intermédiaire (Sonnet), retouches locales | Distant puis local |
| Débogage difficile, revue transverse | Grand modèle | Distant |
| Tri des échecs CI sur une préversion | Modèle local ; grand modèle si une sémantique d'API change | Local puis distant |
| Tests, lint, mesures | Outils sans IA | Local et CI |

Escalade : après deux échecs aux mêmes tests, ou dès qu'une API Godot hors du pack devient nécessaire, la tâche monte d'un niveau. Un diff local qui touche un format persisté, le protocole, un port de compatibilité ou une frontière de module est relu par le grand modèle avant fusion.

Capacité de relecture : deux files actives à 10 h par semaine, trois à 20 h, quatre à 35 h. Le nombre de files se règle sur la relecture humaine, pas sur la puissance de calcul.

Claude Code : `/clear` entre deux tâches ; `opusplan` pour les tâches de conception ; `CLAUDE.md` court. Modèle local : serveur local compatible et harnais d'agent avec appel d'outils, à choisir et vérifier en P2 ; packs autonomes uniquement.

## 6. Tests, fixtures, CI et preuves

| Type de test | POC | MVP | V1 |
| --- | --- | --- | --- |
| Unitaires du socle et du protocole | Oui | Oui | Oui |
| Contrats et sérialisation | Oui | Oui | Oui |
| Intégration runtime-éditeur | Manuel guidé et un scénario automatisé | Automatisé | Automatisé |
| Matrice de versions | 4.7.x bloquant, 4.8 non bloquant | Fenêtre complète | Deux stables et une préversion |
| Régression sur fixtures | Fixtures de base | Toutes | Toutes |
| Interface | Vérification manuelle ciblée | Scénarios manuels suivis | Scénarios manuels suivis |
| Performance | SPIKE-05 | Budgets mesurés | Suivi par version |

| Risque | Preuve attendue | Phase |
| --- | --- | --- |
| Mauvais rattachement | Deux instances restent distinctes ; une nouvelle session ne réutilise pas l'ancienne identité | POC |
| Fausse conclusion | Un événement perdu ou non capturé reste inconnu | POC |
| Transport incomplet | Capture réelle, redémarrage, debugger absent, lot invalide, version incompatible | POC et MVP |
| Buffer saturé | Mémoire bornée, pertes comptées et affichées | POC |
| Source obsolète | Un lien vers un fichier modifié est signalé périmé | POC |
| Rupture de version | Suite verte sur 4.7.x ; écarts 4.8 listés ; aucune correction hors de compat | POC |
| Analyse trompeuse | Un appel dynamique ne devient jamais une relation certaine | MVP |
| Temporalité incorrecte | Bloc interrompu et occurrence incomplète distingués | MVP |
| Plugin fragile | Activer, désactiver et réactiver nettoie tout | POC |

**CI, à créer en T02.** Le workflow `ci.yml`, à chaque push, exécute une matrice de versions. 4.7.x est bloquant. La dernière préversion 4.8 est non bloquante jusqu'à sa release candidate. Les binaires officiels sont téléchargés depuis les releases du projet godot-builds. Chaque job lance le runner en mode headless, le contrôle de dépendances et le lint. Le workflow `version-watch.yml` relance chaque semaine la suite sur la dernière préversion et ouvre une tâche en cas d'échec. Les commandes exactes sont vérifiées en T02 et T03 ; avant cela, elles restent « non vérifiées ».

Un test headless ne valide pas l'interface. Un import sans erreur ne prouve pas que tous les scripts fonctionnent.

**Fixtures**, petites et maison : appel simple, branche, signal, deux instances, bloc temporel, trace tronquée, source modifiée, syntaxe inconnue (construction absente de la grammaire connue). Les jeux open source servent aux tests d'intégration et de mesure, à une révision épinglée. Une golden fixture n'est jamais régénérée pour masquer une régression.

**Statuts de rapport** : exécuté et réussi, exécuté et échoué, non exécuté, non applicable. Une revue IA ne prouve pas qu'un test passe.

## 7. Versionnage, migrations, maintenance et veille de Godot

| Version | Règle |
| --- | --- |
| Plugin | SemVer, 0.x jusqu'à la V1 |
| Protocole | Entier, évolution additive préférée |
| Formats persistés | `schema_version` par format ; migration seulement après distribution |
| Programme analysé | Révision : empreinte des sources |
| Moteur | Profil moteur détecté ; fenêtre de support dans `compat/versions.json` |

**Veille des versions de Godot**

1. Chaque semaine, la CI teste la dernière préversion officielle.
2. À chaque nouvelle version mineure en préversion : lire le guide de migration (Editor, GDScript, Core), mettre à jour la liste des API sensibles, ouvrir une tâche par rupture.
3. À la release candidate, la version devient bloquante sur une branche dédiée.
4. À la sortie stable, bascule de la version de développement ; la plus ancienne stable sort de la fenêtre au cycle suivant.
5. La matrice de `docs/COMPATIBILITY.md` est regénérée.

Budget : 1 à 3 sessions par version mineure. Une rupture qui impose du code hors de `compat/` déclenche une revue d'architecture.

**Outils tiers réutilisés** : version épinglée, licence vérifiée, mode d'inclusion documenté, adaptateur unique, tests de contrat sur leurs sorties, plan de sortie.

**Git** : branches courtes ; une PR par capacité ; contrats, tests et code dans le même changement ; messages au format `feat(core): …`, `test(compat): …`, `docs(adr): …`. Les étiquettes marquent les versions du plugin et des prompts.

**Refactoring et dette** : refactorisations planifiées comme tâches dédiées, tests et contrats préservés. La dette figure dans `PROJECT_STATE.md` : raison, impact, contournement, déclencheur de réexamen.

## 8. Gabarits

**ADR**

```markdown
# ADR-NNN — Titre
Statut : proposé | accepté | remplacé par ADR-MMM · Date · Périmètre
Problème et contexte :
Options étudiées :
Décision :
Conséquences :
Preuves disponibles :
Condition de réexamen :
```

**Contrat**

```markdown
# C-NN — Nom · version · maturité (expérimental | stable) · visibilité (interne | public)
Responsabilité · propriétaire · consommateurs
Entrées / sorties / types
Invariants · erreurs · comportement dégradé
Dépendances autorisées / interdites · thread et ownership
Exemples valides / invalides
Tests de contrat
```

**Fiche de tâche**

```markdown
# TNN — Titre
Capacité et invariants : CAP-.. / INV-..
Objectif vérifiable :
Prérequis et révision de départ :
Fichiers autorisés (existants | à créer) / interdits :
Contrats : C-..
Critères d'acceptation :
Vérifications et commandes (vérifiées | non vérifiées) :
Risque principal · autonomie (A0 | A1 | A2) · niveau de modèle (grand | intermédiaire | local | sans IA) · file
Résultat attendu :
```

**Micro-prompt, grand modèle ou modèle intermédiaire**

```markdown
Objectif unique : …
Références : SPEC rév. …, ARCHITECTURE rév. …, C-.. v…, ADR-..
État vérifié du dépôt : fichiers concernés, révision …
Invariants à respecter : INV-..
Fichiers autorisés : … · interdits : …
API Godot vérifiées (version, source) : … · inconnues : à signaler, jamais devinées
Critères d'acceptation : …
Commandes de validation disponibles : …
Autonomie : A1 · Résultat attendu : patch ciblé + rapport de tâche
```

**Micro-prompt, variante pour le modèle local** : identique, mais autonome. Il contient le texte intégral des contrats et des extraits d'API vérifiés, les tests d'acceptation à faire passer et les commandes exactes, et ne renvoie à aucune conversation antérieure. Règle ajoutée : « Si une information manque, réponds BLOQUÉ avec la liste de ce qui manque. »

**Changement incompatible**

```markdown
Changement demandé · raison
Modules, API, formats persistés touchés
Migration nécessaire ? · compatibilité ascendante ?
Tests impactés · ADR nécessaire ?
Décision humaine : …
```

**Rapport de tâche**

```markdown
Objectif atteint : oui | non | partiellement
Révision / diff · fichiers modifiés
Contrats touchés
Vérifications exactes et statut (exécuté-réussi | exécuté-échoué | non exécuté)
Versions de Godot testées
Limites · dette · décisions nécessaires · prochaine dépendance
Mesures : temps, escalades, quota consommé
```

**Exemples de micro-prompts, conditionnels**

1. T10, modèle local : « Implémente le codec et le validateur de l'enveloppe C-04 v1 dans `protocol/`. Contrat complet ci-dessous. Fais passer `tests/contract/test_envelope.gd` : identifiants 64 bits encodés en chaîne sans perte, lot invalide rejeté avec un code d'erreur, champ inconnu ignoré. N'utilise aucune API hors des types fondamentaux. Si une API te manque, réponds BLOQUÉ. »
2. T12, modèle intermédiaire : « Ajoute la preuve runtime vers éditeur. Le DebuggerPort (C-03) reçoit les lots du helper runtime ; valide-les avec le codec existant ; range-les dans l'Event Store (C-06). Le critère est le scénario `tests/integration/two_instances` : séquences continues, pertes comptées, deux instances distinctes. Signale toute API non couverte par l'adaptateur 4.7. »
3. Régression sur la préversion 4.8, modèle local puis escalade : « La CI non bloquante 4.8 échoue. Log, diff de la dernière fusion et port concerné ci-dessous. Diagnostique, puis propose une correction limitée à `compat/adapters/`. Si la cause est un changement de sémantique d'API, réponds ESCALADE avec ton analyse. »

## 9. Vingt premières tâches

Voir `docs/orchestration.md`.

## 10. Cohérence, décisions de démarrage et checklists

Contrôle de cohérence :

- Chaque tâche de l'orchestration a une preuve de réussite.
- Chaque contrat critique a un propriétaire : le développeur, assisté du grand modèle.
- Aucune API incertaine n'est présentée comme vérifiée : les commandes et signatures restent « non vérifiées » jusqu'à T02, T03 et aux spikes.
- Chaque mécanisme répond à un risque nommé dans le plan.
- Chaque phase a un budget et une revue de continuation.
- Aucune tâche n'est confiée au modèle local sans tests d'acceptation ni règle d'escalade.
- Aucune API moteur sensible n'est appelée hors de la couche de compatibilité.

Décisions nécessaires au démarrage : D-01, D-02, D-05 et D-07. Les autres peuvent attendre leur phase.

**Avant une tâche** : objectif vérifiable ? contrat existant ? fichiers autorisés connus ? API vérifiées sur les versions de la fenêtre ? tests d'acceptation présents ? niveau de modèle et file attribués ? tâche assez petite ? Si une réponse est non, ne pas coder.

**Après une tâche** : tests exécutés sur 4.7.x et la préversion ? contrat respecté ? aucune dépendance interdite ? aucune API sensible hors de compat ? aucune API inventée ? documentation et `PROJECT_STATE.md` à jour ? ADR nécessaire ? rapport rédigé avec ses mesures ?
