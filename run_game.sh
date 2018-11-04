#!/bin/sh

./halite --replay-directory replays/ -vvv --width 32 --height 32 "python3 MasterBot.py" "python3 FeatureBot.py"
