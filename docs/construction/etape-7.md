# Étape 7 — Valeur et revue

Tâches : T19, puis T20 · Budget : 2 à 3 h humaines · Prérequis : étape 6 acceptée, démonstration visuelle faite sur ta machine

## Objectif

Obtenir un premier signal d'utilité de l'outil, honnête sur ses limites, puis décider de la suite : continuer vers le MVP, réduire, réorienter ou arrêter.

## Ce que cette mesure peut dire, et ce qu'elle ne peut pas dire

Trois bugs et une personne suffisent pour :
- découvrir les problèmes d'usage ;
- chiffrer les coûts d'installation et d'instrumentation ;
- voir dans quels cas l'outil aide, et dans quels cas il gêne.

Ils ne suffisent pas pour chiffrer un gain de temps fiable : la difficulté de chaque bug se mêle à l'effet de l'outil. Les durées sont donc indicatives, et la conclusion est qualitative.

Le POC ne valide pas non plus l'expérience visuelle complète du produit. Il montre un journal, une liste arborescente du graphe déclaré et le chemin observé d'une invocation. La carte navigable arrive au MVP ; la timeline, les flux de données et l'export pour une IA arrivent en V1.

## Obligations

- **Coût complet.** La mesure compte le temps d'installation, de déclaration du graphe et d'instrumentation, pas seulement le diagnostic.
- **Bugs à l'aveugle.** Ils sont injectés par une IA. Tu ne connais que leurs symptômes jusqu'à la fin de la mesure.
- **Une variante isolée par bug.** Chaque bug vit sur sa propre branche du banc d'essai, reproductible seul, sans les deux autres.
- **Difficulté comparable.** Chaque bug a une seule cause, de même profondeur : une condition de décision ou un état d'instance, à un ou deux appels du symptôme.
- **Ordre contrebalancé si possible.** Si une deuxième personne participe, elle fait l'ordre inverse du tien.
- **Conclusion qualitative.** Le rapport décrit l'utilité observée, les coûts, les difficultés et les cas où l'outil aide. Les durées sont marquées « indicatives ».
- **Décision consignée.** Elle s'appuie sur ces constats, est écrite dans `docs/DECISIONS.md`, et le plan est amendé en conséquence.

## Méthodologie

1. **Injection.** IA 3 prépare trois variantes isolées du banc d'essai, une par bug. Elle te remet seulement leurs symptômes. La description complète va dans une enveloppe scellée : un fichier que tu n'ouvres qu'à la fin.
2. **Diagnostic chronométré.** Bug 1 avec l'outil, bug 2 sans, bug 3 avec. Une deuxième personne, si tu en as une, fait l'ordre inverse.
3. **Observation.** Pour chaque bug, tu notes : temps jusqu'à la cause, étapes suivies, confiance, ce qui a aidé, ce qui a gêné. Tu ouvres ensuite l'enveloppe et compares la cause trouvée à la cause réelle.
4. **Revue de continuation (T20).** IA 1 rassemble tout ; tu décides.

La valeur de la cartographie elle-même (retrouver un appelant, comprendre un système inconnu) se mesure à la porte du MVP, quand la carte statique existe.

## Points de contrôle

| ID | Contrôle | Preuve | Attendu |
| --- | --- | --- | --- |
| PC7.1 | Variantes isolées | Une branche par bug dans la copie de travail du banc d'essai | Chaque symptôme se reproduit seul |
| PC7.2 | Mesure complète | `docs/mesures/valeur-poc.md` | Durées indicatives, coûts, observations qualitatives, cause trouvée contre cause réelle |
| PC7.3 | Revue préparée | Synthèse d'IA 1 | Budgets consommés contre prévus, réussite par IA, signal d'utilité, risques |
| PC7.4 | Décision | `docs/DECISIONS.md` | Continuer, réduire, réorienter ou arrêter, avec sa justification |
| PC7.5 | Plan à jour | Amendement du plan (PD-0.6) | Budgets recalibrés ; décisions sur SPIKE-03, SPIKE-04 et la reprise d'AST Flow |

## Cheminement d'amélioration

- **Aucun signal d'utilité.** On regarde où part le temps. Si c'est l'instrumentation, on étudie l'instrumentation assistée avant toute nouvelle fonctionnalité. Si c'est la lecture du journal, on travaille l'affichage. Si c'est l'installation, on simplifie le plugin.
- **Signal réel mais faible.** On réduit le MVP à ce qui a servi pendant la mesure.
- **Besoin d'un chiffre fiable.** On prévoit au MVP une mesure plus large : plusieurs bugs par niveau de difficulté, plusieurs personnes, ordre contrebalancé.
- **Écart fort entre budget prévu et consommé.** On recalibre tous les budgets restants avec le ratio observé, et non au cas par cas.

## T19 — Mesure de valeur, exploratoire

Toi, avec IA 3 pour l'injection · A0 · contexte : `docs/benches/<nom>.md`, plan §9

Prompt d'injection, pour IA 3 :

```text
Tu prépares la mesure de valeur, exploratoire, du POC du projet GODOT_DEV_MAPPER. Tu travailles dans la copie de travail ../benches/{nom}.
Crée trois branches à partir de gdm-instrumentation : gdm-bug-1, gdm-bug-2, gdm-bug-3. Chacune contient un seul bug, et seulement celui-là.
Règles des bugs :
- chacun est visible en jeu et lié à une décision instrumentée ou à l'état d'une instance ;
- chacun a une seule cause, à un ou deux appels du symptôme : les trois doivent être de difficulté comparable ;
- natures possibles : comparaison inversée dans une décision, état non réinitialisé après réinsertion dans l'arbre, mauvaise instance ciblée. N'en reprends pas un tel quel.
Ne touche ni aux appels FlowTrace, ni à benches/{nom}/flow.json.
Écris ../benches/{nom}/ENVELOPPE_SCELLEE.md, hors des trois branches : pour chaque bug, la branche, le symptôme visible, la cause, le fichier et la ligne, la manière de le déclencher, et pourquoi sa difficulté est comparable aux deux autres.
Dans ta réponse, donne-moi seulement, pour chaque bug : la branche, le symptôme et la manière de le déclencher en jeu. Rien d'autre.
```

Tu remplis ensuite `docs/mesures/valeur-poc.md` :

| Bug | Branche | Avec l'outil | Installation et instrumentation | Temps jusqu'à la cause (indicatif) | Ce qui a aidé | Ce qui a gêné | Confiance | Cause exacte |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | gdm-bug-1 | Oui | … min | … min | … | … | Faible, moyenne ou forte | Oui ou non |
| 2 | gdm-bug-2 | Non | — | … min | … | … | … | … |
| 3 | gdm-bug-3 | Oui | … min | … min | … | … | … | … |

Sous le tableau, quelques lignes de conclusion qualitative : utilité observée, coûts, difficultés, cas où l'outil aide ou n'aide pas.

**Contrôles**

| ID | Contrôle | Attendu |
| --- | --- | --- |
| T19-a | Chaque branche reproduit son symptôme seule | Trois symptômes reproduits |
| T19-b | Enveloppe ouverte seulement après les trois diagnostics | Heure d'ouverture notée après le dernier diagnostic |
| T19-c | Tableau et conclusion complets, coûts compris, durées marquées « indicatives » | Aucune case vide |
| T19-d | IA 3 relit le tableau contre l'enveloppe | Concordance des causes vérifiée |

## T20 — Revue de continuation

IA 1, puis toi · A0 · contexte : tous les rapports, `PROJECT_STATE.md`, `docs/mesures/valeur-poc.md`, plan §9

```text
Tu prépares la revue de continuation du POC du projet GODOT_DEV_MAPPER. Tu ne décides pas : la décision est humaine.

ENTRÉES : PROJECT_STATE.md, docs/mesures/valeur-poc.md, docs/spikes/, les verdicts de vérification, docs/plan-directeur.md §9.

PRODUIS docs/revues/revue-poc.md avec :
1. Budgets : heures humaines et temps agent consommés par étape, contre le budget ; ratio global.
2. Fiabilité : taux de réussite au premier essai, escalades et refus du vérificateur, par IA.
3. Signal d'utilité : lecture qualitative de T19, avec ses limites (trois bugs, une seule personne, durées indicatives).
4. Risques : ceux du plan, mis à jour ; les nouveaux.
5. Options : continuer, réduire, réorienter ou arrêter. Pour chacune : conditions, conséquences, budget restant estimé avec le ratio observé.
6. Décisions à prendre :
   - SPIKE-03 (rendu) et SPIKE-04 (AST Flow ou extraction maison) au début du MVP ;
   - reprise d'AST Flow comme backend statique ;
   - répartition des tâches entre les trois IA pour le MVP ;
   - besoin, ou non, d'une mesure de valeur plus large au MVP.
7. Proposition d'amendement du plan (PD-0.6) : budgets recalibrés et décisions retenues. Le diff exact, sans l'appliquer.
```

**Contrôles**

| ID | Contrôle | Attendu |
| --- | --- | --- |
| T20-a | Chiffres de la revue recalculés par IA 3 depuis `PROJECT_STATE.md` | Mêmes totaux |
| T20-b | Décision consignée et datée dans `docs/DECISIONS.md` | Présente |
| T20-c | Amendement du plan appliqué après ta validation | PD-0.6 en tête du plan |
| T20-d | Si la décision est de continuer | Découpage de P4a lancé avec le prompt de `mvp.md` |
