#!/usr/bin/env python3
"""
######
Logics
######


"""

from hlt.positionals import Direction
from hlt.behaviors import *
from hlt.ship_state import ShipState
from hlt import constants
import logging

__author__ = "don4get"
__copyright__ = ""
__credits__ = ["SentDex", "don4get"]
__version__ = "1.0.0"
__maintainer__ = "don4get"
__status__ = "Production"


def choose_behavior(ship, game_map, me, turn_number, position_goals, commands):
    # If a ship has no state (because it s bare born), make it collect.
    if ship.id not in me.ship_states:
        me.ship_states[ship.id] = ShipState(Behavior.COLLECT)

    depots = me.get_dropoffs()+[me.shipyard]
    closest_depot = game_map.find_closest_entity(ship.position, depots)
    distance_to_home = game_map.calculate_distance(ship.position, closest_depot.position)
    if distance_to_home * 2 > 400 - turn_number:
        me.ship_states[ship.id].behavior = Behavior.GOTO_HOME

    if me.ship_states[ship.id].behavior is Behavior.COLLECT:

        step_collect(ship, game_map, position_goals, commands)

        if ship.halite_amount >= constants.MAX_HALITE * 0.95:
            me.ship_states[ship.id].behavior = Behavior.DEPOSIT

    elif me.ship_states[ship.id].behavior is Behavior.DEPOSIT:

        step_deposit(ship, game_map, me, position_goals, commands)

        depots = me.get_dropoffs()+[me.shipyard]
        for depot in depots:
            if ship.position == depot.position:
                me.ship_states[ship.id].behavior = Behavior.COLLECT

    elif me.ship_states[ship.id].behavior is Behavior.COLONIZE:
        step_colonize(ship, game_map, me, position_goals, commands)

    elif me.ship_states[ship.id].behavior is Behavior.GOTO_HOME:
        step_goto_home(ship, game_map, me, position_goals, commands)
