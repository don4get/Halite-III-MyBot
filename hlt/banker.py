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


def build_ships(game, me, commands):
    # ship costs 1000, don t make a ship on a ship or they both sink
    #if len(me.get_ships()) < math.ceil(game.turn_number / 25):
    if game.turn_number < constants.MAX_TURNS-100:
        if len(me.get_ships()) > (len(me.get_dropoffs()) + 1) * 16:
            if me.halite_amount >= constants.DROPOFF_COST:
                order_ship_to_colonize(game, me)

        elif me.halite_amount >= constants.SHIP_COST and not game.game_map[me.shipyard].is_occupied:
            commands.append(me.shipyard.spawn())


def order_ship_to_colonize(game, me):
    best_location = find_best_drop_off_location(game, me)
    closest_ship_id = game.game_map.find_closest_entity(best_location, me.get_ships()).id
    me.ship_states[closest_ship_id].behavior = Behavior.COLONIZE
    me.ship_states[closest_ship_id].position_goal = best_location
    #me.get_ship(closest_ship_id).set_behavior(Behavior.COLONIZE)



def find_best_drop_off_location(game, me):
    halite_amount_max = 0
    best_cell = None
    logging.info(f"{game.game_map.get_cells()}")
    for row in game.game_map.get_cells():
        for cell in row:
            if cell.halite_amount > halite_amount_max:
                halite_amount_max = cell.halite_amount
                best_cell = cell

    return best_cell.position