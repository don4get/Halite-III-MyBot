#!/usr/bin/env python3
"""
######
Banker
######


"""

import math

__author__ = "don4get"
__copyright__ = ""
__credits__ = ["SentDex", "don4get"]
__version__ = "1.0.0"
__maintainer__ = "don4get"
__status__ = "Production"


def build_ships(game, me, commands):
    # ship costs 1000, don t make a ship on a ship or they both sink
    if len(me.get_ships()) < math.ceil(game.turn_number / 25):
        if me.halite_amount >= 1000 and not game.game_map[me.shipyard].is_occupied:
            commands.append(me.shipyard.spawn())
