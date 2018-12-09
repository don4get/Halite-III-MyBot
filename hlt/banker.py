#!/usr/bin/env python3
"""
######
Banker
######


"""

import math
from hlt import constants
from hlt.positionals import Position
from hlt.behaviors import Behavior
import logging

__author__ = "don4get"
__copyright__ = ""
__credits__ = ["SentDex", "don4get"]
__version__ = "1.0.0"
__maintainer__ = "don4get"
__status__ = "Production"


class Banker:
    def __init__(self):
        self._lastProductionCommands = []

    def build_ships(self, game):
        me = game.me
        production_commands = []
        # ship costs 1000, don t make a ship on a ship or they both sink
        if game.turn_number < constants.MAX_TURNS-100:
            if len(me.get_ships()) > (len(me.get_dropoffs()) + 1) * 16:
                if me.halite_amount >= constants.DROPOFF_COST:
                    self.order_ship_to_colonize(game)

            elif me.halite_amount >= constants.SHIP_COST and not game.game_map[
                    me.shipyard].is_occupied:
                    production_commands.append(me.shipyard.spawn())
        return production_commands

    @staticmethod
    def order_ship_to_colonize(game):
        me = game.me
        best_location = game.game_map.find_wealthiest_location()
        closest_ship_id = game.game_map.find_closest_entity(best_location, me.get_ships()).id
        me.get_ship(closest_ship_id).behavior = Behavior.COLONIZE
        me.get_ship(closest_ship_id).position_goal = best_location
