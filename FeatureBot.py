#!/usr/bin/env python3
"""
###########
Feature bot
###########


"""

import hlt
from hlt import logics
from hlt import banker
import logging

__author__ = "don4get"
__copyright__ = ""
__credits__ = ["SentDex", "don4get"]
__version__ = "1.0.0"
__maintainer__ = "don4get"
__status__ = "Production"


def main():
    game = hlt.Game()
    game.ready("FeatureBot")

    while True:
        loop(game)


def loop(game):

    game.update_frame()
    me = game.me

    commands = []
    position_goals = []

    for ship in me.get_ships():
        logics.choose_behavior(ship, game.game_map, me, position_goals, commands)

    banker.build_ships(game, me, commands)

    # Send your moves back to the game environment, ending this turn.
    game.end_turn(commands)


main()
