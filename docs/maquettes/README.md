# Maquettes du rendu

Simulations fictives du rendu de l'outil, appliquées à un roguelike imaginaire, « EMBER · Les Deux Portes ». Ce ne sont ni du code du plugin, ni des mesures de Godot.

| Fichier | Contenu |
| --- | --- |
| `ember-atlas-roguelike.html` | Version d'origine |
| `ember-atlas-roguelike-v2.html` | Version améliorée, le 8 octobre 2026 |

## Ce que la version améliorée change

**Lisibilité du graphe**, mesurée dans Chromium sur les cinq vues (68 relations) :

| Défaut | Avant | Après |
| --- | --- | --- |
| Relations qui traversent une autre carte | 19 | 0 |
| Étiquettes recouvertes par une carte | 39 | 0 |
| Étiquettes qui se chevauchent | 3 | 0 |
| Éléments de texte sous 11 px | 276 sur 416 | 56 sur 463, aucun sous 10,5 px |

- Relations orthogonales qui contournent les cartes, ports répartis le long de chaque côté.
- Étiquettes sur fond opaque, placées sans collision. Une étiquette sans place libre reste masquée et se lit au survol ou dans l'inspecteur.
- Zoom sémantique : dézoomée, la carte n'affiche que les noms, en plus grand.
- Groupe du niveau II lisible de gauche à droite ; cadre du groupe agrandi pour contenir « Passage accompli ».

**Fidélité au plan directeur (PD-0.4)**
- Pastilles « Calendrier du plan » (POC, MVP, V1, après V1, hors plan, illustration), désactivables.
- Provenance de chaque relation dans l'inspecteur : observée ×n, non observée, hors couverture de la trace.
- Chemin observé à trois états : cohérent, incohérent, indéterminé. Le sixième scénario, « Transition non déclarée », montre l'état incohérent, avec la transition tracée en rouge sur la carte.
- Vocabulaire : « non observé dans cette tentative », jamais « non parcouru ».

**Divers** : panneaux du bas repliables, rôle d'accessibilité du graphe corrigé, export téléchargeable aussi dans une page publiée.
