# Étape 7 — Valeur et revue

Tâches : T19, puis T20 · Budget : 2 à 3 h humaines · Prérequis : étape 6 acceptée, démonstration visuelle faite sur ta machine

## Objectif

Savoir, mesures à l'appui, si l'outil fait gagner du temps, puis décider de la suite : continuer vers le MVP, réduire, réorienter ou arrêter.

## Obligations

- **Coût complet.** La mesure compte le temps d'installation, de déclaration du graphe et d'instrumentation, pas seulement le diagnostic.
- **Bugs à l'aveugle.** Ils sont injectés par une IA ; tu ne connais que leurs symptômes jusqu'à la fin de la mesure.
- **Comparaison équitable.** Chaque bug se diagnostique avec ou sans l'outil, en alternant l'ordre, pour limiter l'effet d'apprentissage.
- **Décision consignée.** Elle s'appuie sur les chiffres, est écrite dans `docs/DECISIONS.md`, et le plan est amendé en conséquence.

## Méthodologie

1. **Injection.** Gemini injecte trois bugs dans une branche du banc d'essai et te remet seulement leurs symptômes. La description complète va dans une enveloppe scellée : un fichier que tu n'ouvres qu'à la fin.
2. **Diagnostic chronométré.** Bug 1 avec l'outil, bug 2 sans, bug 3 avec. Si tu disposes d'une deuxième personne, elle fait l'ordre inverse.
3. **Comparaison.** Tu notes, pour chaque bug : temps jusqu'à la cause, étapes suivies, confiance dans la cause trouvée. Tu ouvres l'enveloppe et compares la cause trouvée à la cause réelle.
4. **Revue de continuation (T20).** Opus rassemble tout ; tu décides.

La valeur de la cartographie elle-même (retrouver un appelant, comprendre un système inconnu) se mesure à la porte du MVP, quand la carte statique existe.

## Points de contrôle

| ID | Contrôle | Preuve | Attendu |
| --- | --- | --- | --- |
| PC7.1 | Bugs reproductibles | Symptôme observé en jeu pour chacun | Trois symptômes visibles |
| PC7.2 | Mesure complète | `docs/mesures/valeur-poc.md` | Temps de diagnostic, coûts d'installation et d'instrumentation, cause trouvée contre cause réelle |
| PC7.3 | Revue préparée | Synthèse d'Opus | Budgets consommés contre prévus, réussite par modèle, mesure de valeur, risques |
| PC7.4 | Décision | `docs/DECISIONS.md` | Continuer, réduire, réorienter ou arrêter, avec sa justification |
| PC7.5 | Plan à jour | Amendement du plan (PD-0.4) | Budgets recalibrés ; décisions sur SPIKE-03, SPIKE-04 et la reprise d'AST Flow |

## Cheminement d'amélioration

- **Gain nul ou négatif.** On regarde où part le temps. Si c'est l'instrumentation, on étudie l'instrumentation assistée avant toute nouvelle fonctionnalité. Si c'est la lecture du journal, on travaille l'affichage. Si c'est l'installation, on simplifie le plugin.
- **Gain réel mais faible.** On réduit le MVP à ce qui a servi pendant la mesure.
- **Écart fort entre budget prévu et consommé.** On recalibre tous les budgets restants avec le ratio observé, et non au cas par cas.

## T19 — Mesure de valeur

Toi, avec Gemini pour l'injection · A0 · contexte : `docs/benches/<nom>.md`, plan §9

Prompt d'injection, pour Gemini :

```text
Tu prépares la mesure de valeur du POC du projet GODOT_DEV_MAPPER. Dans la copie de travail ../benches/{nom}, crée la branche gdm-bugs à partir de gdm-instrumentation.
Introduis trois bugs réalistes. Chacun doit être visible en jeu et lié à une décision instrumentée ou à une instance. Exemples de nature : comparaison inversée dans une décision ; état non réinitialisé après réinsertion dans l'arbre ; mauvaise instance ciblée. N'en reprends pas un tel quel.
Ne touche ni aux appels FlowTrace, ni à benches/{nom}/flow.json.
Écris ../benches/{nom}/ENVELOPPE_SCELLEE.md : pour chaque bug, le symptôme visible, la cause, le fichier et la ligne, la manière de le déclencher.
Dans ta réponse, donne-moi seulement les trois symptômes, un par ligne, et la manière de les déclencher en jeu. Rien d'autre.
```

Tu remplis ensuite `docs/mesures/valeur-poc.md` :

| Bug | Avec l'outil | Installation et instrumentation | Temps jusqu'à la cause | Étapes | Confiance | Cause exacte |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Oui | … min | … min | … | Faible, moyenne ou forte | Oui ou non |
| 2 | Non | — | … min | … | … | … |
| 3 | Oui | … min | … min | … | … | … |

**Contrôles**

| ID | Contrôle | Attendu |
| --- | --- | --- |
| T19-a | Enveloppe ouverte seulement après les trois diagnostics | Heure d'ouverture notée après le dernier diagnostic |
| T19-b | Tableau complet, coûts d'installation compris | Aucune case vide |
| T19-c | Gemini relit le tableau contre l'enveloppe | Concordance des causes vérifiée |

## T20 — Revue de continuation

Opus, puis toi · A0 · contexte : tous les rapports, `PROJECT_STATE.md`, `docs/mesures/valeur-poc.md`, plan §9

```text
Tu prépares la revue de continuation du POC du projet GODOT_DEV_MAPPER. Tu ne décides pas : la décision est humaine.

ENTRÉES : PROJECT_STATE.md, docs/mesures/valeur-poc.md, docs/spikes/, les verdicts de vérification, docs/plan-directeur.md §9.

PRODUIS docs/revues/revue-poc.md avec :
1. Budgets : heures humaines et temps agent consommés par étape, contre le budget ; ratio global.
2. Fiabilité : taux de réussite au premier essai, escalades et refus du vérificateur, par modèle.
3. Valeur : lecture du tableau de T19, avec ses limites (trois bugs, une seule personne).
4. Risques : ceux du plan, mis à jour ; les nouveaux.
5. Options : continuer, réduire, réorienter ou arrêter. Pour chacune : conditions, conséquences, budget restant estimé avec le ratio observé.
6. Décisions à prendre :
   - SPIKE-03 (rendu) et SPIKE-04 (AST Flow ou extraction maison) au début du MVP ;
   - reprise d'AST Flow comme backend statique ;
   - routage des modèles pour le MVP.
7. Proposition d'amendement du plan (PD-0.4) : budgets recalibrés et décisions retenues. Le diff exact, sans l'appliquer.
```

**Contrôles**

| ID | Contrôle | Attendu |
| --- | --- | --- |
| T20-a | Chiffres de la revue recalculés par Gemini depuis `PROJECT_STATE.md` | Mêmes totaux |
| T20-b | Décision consignée et datée dans `docs/DECISIONS.md` | Présente |
| T20-c | Amendement du plan appliqué après ta validation | PD-0.4 en tête du plan |
| T20-d | Si la décision est de continuer | Découpage de P4a lancé avec le prompt de `mvp.md` |
