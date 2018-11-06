#!/usr/bin/env python3
"""
##########
Ship State
##########


"""

import hlt
from hlt import constants
from hlt.positionals import Direction, Position
import random
import logging
import math
from hlt.behaviors import Behavior

__author__ = "don4get"
__copyright__ = ""
__credits__ = ["don4get"]
__version__ = "1.0.0"
__maintainer__ = "don4get"
__status__ = "Production"


class ShipState:
    """
    Describes the state of a ship
    """

    def __init__(self, behavior):
        self.behavior = behavior
        self.position_goal = None
