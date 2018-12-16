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
from hlt.player import Player

__author__ = "don4get"
__copyright__ = ""
__credits__ = ["SentDex", "don4get"]
__version__ = "1.0.0"
__maintainer__ = "don4get"
__status__ = "Production"


class Banker:
    def __init__(self):
        self._lastProductionCommands = []
        self.dropoff_count = 0

    def manage_money(self, game):
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
    def find_best_position_to_colonize(game):
        sorted_list_by_halite_amount = game.game_map.sort_cells_by_halite_amount()
        enemy_list = [player for player_id, player in game.players.items() if player_id is not \
                      game.my_id]
        enemy_structures = []
        for enemy in enemy_list:
            enemy_structures.append(enemy.shipyard)
            enemy_structures.extend(enemy.get_dropoffs())

        max_score = 0
        best_position = game.me.shipyard.position
        for cell in sorted_list_by_halite_amount:
            closest_structure = game.game_map.find_closest_entity(cell.position,
                                                                            enemy_structures)

            smallest_distance = game.game_map.calculate_distance(
                    closest_structure.position, cell.position)

            score = cell.halite_amount * smallest_distance
            if (score > max_score):
                max_score = score
                best_position = cell.position

        return best_position

    @staticmethod
    def order_ship_to_colonize(game):
        me = game.me
        best_location = Banker.find_best_position_to_colonize(game)
        closest_ship_id = game.game_map.find_closest_entity(best_location, me.get_ships()).id
        me.get_ship(closest_ship_id).behavior = Behavior.COLONIZE
        me.get_ship(closest_ship_id).position_goal = best_location

