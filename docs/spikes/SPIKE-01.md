# SPIKE-01a — Canal du débogueur, partie jeu

Statut : **terminé** · décision : **KEEP, avec modifications** · 8 octobre 2026 · prototype jetable : `spikes/spike01_debugger/`

La partie éditeur reste à faire : c'est SPIKE-01b, tâche T05 de l'orchestration.

## Question

Un runtime sans autoload peut-il ouvrir, arrêter et rouvrir une collecte sur le canal du débogueur distant, sans perte, pendant que le jeu tourne ? Que se passe-t-il quand la connexion disparaît ?

## Méthode

- **Moteurs** : Godot 4.7.2 stable officiel (ed1daf0bf) et 4.8-dev7 officiel (c971f93e7), téléchargés depuis l'archive godot-builds. Linux x86_64, conteneur sans GPU, mode headless, jeu limité à 60 images par seconde.
- **Côté jeu** : classe `FlowSpike` à `class_name` et fonctions statiques, sans autoload. Elle enregistre une capture de messages, se branche sur le signal de frame de l'arbre de scènes et envoie un lot par frame.
- **Côté éditeur** : un récepteur GDScript qui parle le protocole du débogueur distant sur le port 6007. Ce n'est pas l'éditeur.
- **Scénario** : démarrage, 2,5 s de collecte, arrêt, pause, redémarrage, 1,5 s, arrêt, pause, redémarrage, puis coupure brutale de la connexion. Un ping toutes les 250 ms pendant la collecte.
- **Débits** : 20, 170 et 400 événements par frame, soit environ 1 200, 10 200 et 24 000 événements par seconde.

## Résultats, après correction

| Mesure | 20 par frame | 170 par frame | 400 par frame |
| --- | --- | --- | --- |
| Événements reçus pendant les phases de collecte | 5 700 | 48 450 | 114 000 à 114 800 |
| Trous de séquence, pertes annoncées | 0 | 0 | 0 |
| Lots reçus après la confirmation d'arrêt | 0 | 0 | 0 |
| Cadence du jeu | 60 images/s | 60 images/s | 60 images/s |
| Aller-retour ping, médiane | 48 à 55 ms | 49 ms | 49 ms |
| Aller-retour ping, maximum | 70 à 90 ms | 62 ms | 69 à 97 ms |

Sept essais après correction : cinq sur 4.7.2, deux sur 4.8-dev7. Les deux versions donnent les mêmes résultats.

## Constats

1. **La classe statique sans autoload fonctionne.** Une capture enregistrée par un Callable sur la classe reçoit les messages. Le branchement sur la frontière de frame fonctionne depuis du code statique. L'initialisation paresseuse, au premier appel, fonctionne aussi.
2. **Les messages entrants peuvent arriver en réentrance.** Quand un débogueur est attaché, Godot traite les messages entrants pendant l'exécution du GDScript, sur le thread principal. À 400 événements par frame, cela s'est produit 6 à 12 fois par essai.

   Dans la première version, l'arrêt modifiait l'état directement. Un événement s'enregistrait alors entre le vidage final et la confirmation, puis partait dans un lot tardif, à chaque essai. Correction : le rappel note seulement la commande, appliquée à la frontière de frame suivante. Depuis, aucun lot ne suit la confirmation d'arrêt.
3. **Une coupure ne se voit pas côté jeu.** `EngineDebugger.is_active()` reste vrai après la coupure. Sans autre mécanisme, le jeu continue à envoyer dans le vide. Avec un bail de 2 s renouvelé par les pings, la collecte s'arrête seule, et le jeu continue à 60 images par seconde.
4. **L'arrêt du moteur demande un désenregistrement.** Sans désenregistrement explicite de la capture, une erreur « Capture not registered » apparaît à la sortie. Avec, elle disparaît.
5. **Le moteur envoie ses propres messages** : set_pid, output, window:title, et environ un performance:profile_frame par seconde. La capture de l'outil doit les ignorer.
6. **Débit** : jusqu'à environ 24 000 événements par seconde, sans perte ni baisse de cadence dans ce contexte sans rendu.

## Limites

- Pas de rendu, pas d'éditeur, réseau local du conteneur. Les chiffres ne valent pas performance de l'outil.
- Le coût de la capture dans le temps de frame n'est pas mesuré ici : c'est SPIKE-05, en T13.
- La latence est un aller-retour mesuré avec la seule horloge du récepteur. Elle inclut l'attente de la frontière de frame côté jeu. Aucun horodatage du jeu n'est soustrait d'un horodatage du récepteur.

## Décision

KEEP. Le plan PD-0.3 reprend ces modifications :
- commandes appliquées à la frontière de frame ;
- bail renouvelé par l'éditeur ;
- crochet de frame posé dès l'initialisation ;
- désenregistrement explicite à la fin ;
- messages du moteur ignorés.

## Reste à vérifier : SPIKE-01b, sur la machine du développeur

Avec l'éditeur réel et le rendu actif :
- capture côté plugin et envoi de commandes par la session de débogage ;
- lancements répétés depuis l'éditeur ;
- désactivation du plugin pendant une collecte ;
- débit et cadence.

Les critères détaillés sont dans la fiche T05 de `docs/orchestration.md`. Les instances enregistrées avant le démarrage relèvent du runtime : elles sont vérifiées en T13a.
