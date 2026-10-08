# Maquettes du rendu

Simulations fictives du rendu de l'outil, appliquées à un roguelike imaginaire, « EMBER · Les Deux Portes ». Ce ne sont ni du code du plugin, ni des mesures de Godot.

| Fichier | Contenu |
| --- | --- |
| `ember-atlas-roguelike.html` | Version d'origine |
| `ember-atlas-roguelike-v2.html` | Version améliorée, le 8 octobre 2026 |
| `ember-atlas-roguelike-v3.html` | Version complète : personnages, monde et inventaire. C'est celle qui est publiée. |
| `ember-atlas-roguelike-v3.1.html` | v3 corrigée par GPT-6 : pas de physique fixe à 60 Hz, dégâts appliqués au pas suivant, inspecteur et journal stables pendant le survol, export figé à l'ouverture, bandeaux utilisables sur petit écran |
| `ember-en-direct.html` | Mode en direct : le jeu tourne, l'interface de l'outil se superpose à l'image et pilote les étapes |

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

## Ce que la version complète (v3) ajoute

La v2 couvrait le déroulé de la partie, les scripts, les chargements et la sauvegarde. Il lui manquait la caméra, la physique détaillée, la navigation, les machines à états des personnages, l'inventaire, les animations et les vagues d'ennemis. Ils sont ajoutés : le modèle passe de 38 à 68 définitions, et de 55 à 106 relations.

**Vue Personnages** (pastille « POC puis MVP »)
- Machines à états de la sentinelle, du joueur et des boss. Les deux boss partagent une même définition de phases : deux instances, une définition.
- La décision « À portée ? » de chaque sentinelle est le cas de démonstration du POC. Un sélecteur d'instance (`sentinel-01`, `sentinel-02`) montre l'état courant et le chemin observé de chacune ; ils diffèrent.
- L'inspecteur donne, pour chaque instance, ses passages dans l'état, son état actuel et sa dernière décision (vraie ou fausse, avec la distance).

**Vue Monde** (pastille « MVP »)
- Physique à pas fixe, 60 pas par seconde, figée pendant la pause. Corps du joueur, hitbox des ennemis, hurtbox du joueur, couches et masques de collision, flèches des archers.
- Un contact détecté au pas N est appliqué par CombatResolver au pas N + 1. Le journal affiche le pas de chaque événement : l'ordre des événements ne prouve pas la cause.
- Navigation (agent et maillage), directeur de vagues, caméra (suivi, limites de salle, tremblement, cadrage des boss), animations.

**Inventaire** (vue Scripts & données) : objet au sol, inventaire, catalogue d'objets. La Braise vive est ramassée au premier butin et utilisée contre le Forgeron sous 50 PV. La Frappe ardente et l'Écho de braise sont des reliques équipées.

**Deux scénarios de bug**
- « Masque de collision erroné » : sentinel-02 attaque sans jamais toucher. L'inspecteur de la hitbox montre « 2 attaques, 0 contact » et la surcharge de masque extraite de la scène.
- « Caméra bloquée » : après le choix de route, la caméra garde les limites d'une autre salle. L'inspecteur signale l'incohérence avec la dernière écriture connue des limites.

**Plan de réalisation d'EMBER** : 14 lots au lieu de 11 (P12 machines à états, P13 physique et monde, P14 inventaire).

**Mesures** : sur les sept vues, aucune relation ne traverse une carte et aucune étiquette n'est masquée par une carte ou une autre étiquette. La vue Personnages affiche 21 étiquettes de transition sur 24, dont les deux branches de la décision. Les 15 vérifications de la v2 passent toujours, et 13 vérifications nouvelles aussi, sans erreur JavaScript.

**Piste pour le plan** : relever les couches et masques de collision dans l'inventaire des scènes (MVP). Ce n'est pas encore au plan directeur.

## Ce que la version en direct ajoute

Les atlas montrent la carte hors exécution. `ember-en-direct.html` montre l'outil pendant que le jeu tourne dans l'onglet Jeu de l'éditeur, salle des sentinelles.

- **Superposition** : étiquettes d'instance, anneaux de portée de la décision « À portée ? », hitbox. Elles viennent des positions reçues : un léger retard en marche, exactes en pause.
- **Pilotage** : suspendre, avancer d'un pas de physique, aller jusqu'au prochain changement de décision, aller jusqu'à la fin d'une étape, vitesse. Les arrêts tombent toujours à la fin du pas.
- **Étapes** : bandeau du déroulé ; un clic sur une étape à venir arme un arrêt à son entrée. Les étapes passées avant la collecte restent « non observées ».
- **Arrêts** : conditions évaluées dans le jeu (fin du pas) ou dans l'éditeur (quelques pas plus tard, après l'aller-retour).
- **Scénarios** : parcours nominal, masque de collision erroné, événement perdu, jeu interrompu.

**Écart au plan** : la superposition et le pilotage ne sont pas au plan directeur. La page les marque « hors plan » et propose CAP-21 (pilotage, MVP), CAP-22 (superposition, V1) et SPIKE-07. Rien n'est vérifié sur Godot.
