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
        command_queue = []

        direction_order = [Direction.North, Direction.South, Direction.East, Direction.West,
                           Direction.Still]

        position_choices = []
        for ship in me.get_ships():
            # If a ship has no state (because it s bare born), make it collect.
            if ship.id not in me.ship_states:
                me.ship_states[ship.id] = "collecting"

            if me.ship_states[ship.id] == "collecting":
                position_options = ship.position.get_surrounding_cardinals() + [ship.position]
                position_dict = {}
                halite_dict = {}

                for n, direction in enumerate(direction_order):
                    position_dict[direction] = position_options[n]

                for direction in position_dict:
                    position = position_dict[direction]
                    halite_amount = game_map[position].halite_amount

                    # Consider a position as a potential ship goal if it is not already aimed by
                    # another one.
                    if position_dict[direction] not in position_choices:
                        # Make current ship position 4 times more interesting than the others
                        if direction == Direction.Still:
                            halite_amount *= 4
                        halite_dict[direction] = halite_amount

                directional_choice = max(halite_dict, key=halite_dict.get)
                position_choices.append(position_dict[directional_choice])

                movement = game_map.naive_navigate(ship,
                                                   ship.position + Position(*directional_choice))
                command = ship.move(movement)
                command_queue.append(command)

                if ship.halite_amount >= constants.MAX_HALITE:
                    me.ship_states[ship.id] = "depositing"

            elif me.ship_states[ship.id] == "depositing":
                movement = game_map.naive_navigate(ship, me.shipyard.position)
                upcoming_position = ship.position + Position(*movement)
                if upcoming_position not in position_choices:
                    position_choices.append(upcoming_position)
                    command_queue.append(ship.move(movement))

                    # If current movement is still, ship is at shipyard and deposit is done. Make
                    #  it collect again.
                    if movement == Direction.Still:
                        me.ship_states[ship.id] = "collecting"
                else:
                    # In this case, moving will cause two boats to sink, so wait until the other
                    # boat to pass.
                    position_choices.append(ship.position)
                    movement = game_map.naive_navigate(ship,
                                                       ship.position + Position(*Direction.Still))
                    command = ship.move(movement)
                    command_queue.append(command)

        # ship costs 1000, dont make a ship on a ship or they both sink
        if len(me.get_ships()) < math.ceil(game.turn_number / 25):
            if me.halite_amount >= 1000 and not game_map[me.shipyard].is_occupied:
                command_queue.append(me.shipyard.spawn())

        # Send your moves back to the game environment, ending this turn.
        game.end_turn(command_queue)


main()
