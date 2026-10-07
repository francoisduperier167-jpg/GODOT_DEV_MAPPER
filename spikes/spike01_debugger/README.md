# SPIKE-01a — prototype jetable

Canal du débogueur distant, partie jeu. Code de mesure, pas de production : rien ici ne doit être copié dans `addons/`.

- `game/` : scène de test et classe `FlowSpike`, statique et sans autoload.
- `receiver/` : récepteur GDScript qui joue le rôle de l'éditeur sur le port 6007. Ce n'est pas l'éditeur.
- `run.sh` : `GODOT=/chemin/vers/godot ./run.sh --rate=400 --seconds=10` (Linux ; chemins temporaires dans `/tmp`).

Résultats et décision : `docs/spikes/SPIKE-01.md`.
