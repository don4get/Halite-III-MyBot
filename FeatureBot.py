#!/usr/bin/env python3
"""
###########
Feature bot
###########


"""

import hlt
from hlt import constants
from hlt.positionals import Direction, Position
import random
import logging
import math
from hlt.behaviors import Behavior, step_collect, step_deposit
from hlt.ship_state import ShipState

__author__ = "don4get"
__copyright__ = ""
__credits__ = ["SentDex", "don4get"]
__version__ = "1.0.0"
__maintainer__ = "don4get"
__status__ = "Production"


def main():
    game = hlt.Game()
    game.ready("FeatureBot")

    main_loop(game)


def main_loop(game):
    while True:
        game.update_frame()
        me = game.me

        game_map = game.game_map
        commands = []
        position_goals = []

        for ship in me.get_ships():
            # If a ship has no state (because it s bare born), make it collect.
            if ship.id not in me.ship_states:
                me.ship_states[ship.id] = ShipState(Behavior.COLLECT)

            if me.ship_states[ship.id].behavior is Behavior.COLLECT:

                step_collect(ship, game_map, position_goals, commands)

                if ship.halite_amount >= constants.MAX_HALITE:
                    me.ship_states[ship.id].behavior = Behavior.DEPOSIT

            elif me.ship_states[ship.id].behavior is Behavior.DEPOSIT:

                step_deposit(ship, game_map, me, position_goals, commands)

                if ship.position == me.shipyard.position:
                    me.ship_states[ship.id].behavior = Behavior.COLLECT

        # ship costs 1000, don t make a ship on a ship or they both sink
        if len(me.get_ships()) < math.ceil(game.turn_number / 25):
            if me.halite_amount >= 1000 and not game_map[me.shipyard].is_occupied:
                commands.append(me.shipyard.spawn())

        # Send your moves back to the game environment, ending this turn.
        game.end_turn(commands)


main()
