#!/bin/bash
# SPIKE-01a, prototype jetable : lance le récepteur (éditeur simulé), puis le jeu
# connecté au débogueur distant. Les arguments sont transmis au jeu.
# Usage : GODOT=/chemin/vers/godot ./run.sh --rate=400 --seconds=10 [--lazy]
set -u
GODOT="${GODOT:-godot}"
cd "$(dirname "$0")"
rm -f /tmp/spike01_game_status.txt /tmp/spike01_receiver.log
"$GODOT" --headless --path receiver --import > /dev/null 2>&1
"$GODOT" --headless --path game --import > /dev/null 2>&1
timeout 40 "$GODOT" --headless --path receiver -s receiver.gd > recv.out 2>&1 &
RPID=$!
sleep 1.5
timeout 40 "$GODOT" --headless --path game --remote-debug tcp://127.0.0.1:6007 -- "$@" > game.out 2>&1
wait $RPID
cat /tmp/spike01_receiver.log
echo "--- état final du jeu ---"
cat /tmp/spike01_game_status.txt
grep -E "ERROR|WARNING" game.out || true
