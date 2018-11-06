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
