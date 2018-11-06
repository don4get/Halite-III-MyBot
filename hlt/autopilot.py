#!/usr/bin/env python3
"""
#########
Autopilot
#########


"""

from hlt.positionals import Direction

__author__ = "don4get"
__copyright__ = ""
__credits__ = ["SentDex", "don4get"]
__version__ = "1.0.0"
__maintainer__ = "don4get"
__status__ = "Production"


def compute_position_goal(ship, game_map, position_goals):
    position_options = ship.position.get_surrounding_cardinals()
    position_dict = {}
    halite_dict = {}
    for n, direction in enumerate(Direction.get_all_cardinals()):
        position_dict[direction] = position_options[n]
    for direction in position_dict:
        position = position_dict[direction]
        halite_amount = game_map[position].halite_amount

        # Consider a position as a potential ship goal if it is not already aimed by
        # another one.
        if position_dict[direction] not in position_goals:
            # Make current ship position 4 times more interesting than the others
            if direction == Direction.Still:
                halite_amount *= 4
            halite_dict[direction] = halite_amount
    directional_choice = max(halite_dict, key=halite_dict.get)
    position_goal = position_dict[directional_choice]
    return position_goal
