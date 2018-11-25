#!/usr/bin/env python3
"""
#########
Behaviors
#########


"""

import hlt
from hlt import constants
from hlt.positionals import Direction, Position
import random
import logging
import math
from hlt.game_map import GameMap
from hlt.autopilot import compute_position_goal

__author__ = "don4get"
__copyright__ = ""
__credits__ = ["don4get"]
__version__ = "1.0.0"
__maintainer__ = "don4get"
__status__ = "Production"


class Behavior:
    """
    Describes the behaviors that a ship can adopt during the game
    """

    COLLECT = 0
    DEPOSIT = 1
    ATTACK = 2
    COLONIZE = 3
    GOTO_HOME = 4


def step_deposit(ship, game_map, me, position_goals, commands):

    depots = me.get_dropoffs() + [me.shipyard]
    closest_depot = game_map.find_closest_entity(ship.position, depots)
    movement = game_map.naive_navigate(ship, closest_depot.position)
    upcoming_position = ship.position + Position(*movement)
    if upcoming_position not in position_goals:
        position_goals.append(upcoming_position)
        commands.append(ship.move(movement))

        # If current movement is still, ship is at shipyard and deposit is done. Make
        #  it collect again.
    else:
        # In this case, moving will cause two boats to sink, so wait until the other
        # boat to pass.
        position_goals.append(ship.position)
        movement = Direction.Still
        command = ship.move(movement)
        commands.append(command)


def step_collect(ship, game_map, position_goals, commands):
    position_goal = compute_position_goal(ship, game_map, position_goals)
    position_goals.append(position_goal)
    movement = game_map.naive_navigate(ship, position_goal)
    command = ship.move(movement)
    commands.append(command)


def step_colonize(ship, game_map, me, position_goals, commands):
    position_goal = me.ship_states[ship.id].position_goal
    position_goals.append(position_goal)

    if ship.position == position_goal:
        if not game_map[position_goal].has_structure:
            command = ship.make_dropoff()
        else:
            command = ship.move(Direction.Still)
            me.ship_states[ship.id].behavior = Behavior.COLLECT

    else:
        movement = game_map.naive_navigate(ship, position_goal)
        command = ship.move(movement)

    commands.append(command)


def step_goto_home(ship, game_map, me, position_goals, commands):
    depots = me.get_dropoffs() + [me.shipyard]
    closest_depot = game_map.find_closest_entity(ship.position, depots)
    movement = game_map.crush_depots_navigate(ship, closest_depot.position)
    upcoming_position = ship.position + Position(*movement)
    if upcoming_position not in position_goals:
        if upcoming_position is not me.shipyard.position:
            position_goals.append(upcoming_position)
        commands.append(ship.move(movement))

        # If current movement is still, ship is at shipyard and deposit is done. Make
        #  it collect again.
    else:
        # In this case, moving will cause two boats to sink, so wait until the other
        # boat to pass.
        position_goals.append(ship.position)
        movement = Direction.Still
        command = ship.move(movement)
        commands.append(command)

    if me.shipyard.position in position_goals:
        position_goals.remove(me.shipyard.position)
