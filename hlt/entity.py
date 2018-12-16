import abc

from . import commands, constants
from .positionals import Direction, Position
from .common import read_input
from .mission import *


class Entity(abc.ABC):
    """
    Base Entity Class from whence Ships, Dropoffs and Shipyards inherit
    """
    def __init__(self, owner, id, position):
        self.owner = owner
        self.id = id
        self.position = position

    @staticmethod
    def _generate(player_id):
        """
        Method which creates an entity for a specific player given input from the engine.
        :param player_id: The player id for the player who owns this entity
        :return: An instance of Entity along with its id
        """
        ship_id, x_position, y_position = map(int, read_input().split())
        return ship_id, Entity(player_id, ship_id, Position(x_position, y_position))

    def __repr__(self):
        ret = f"{self.__class__.__name__}(id={self.id}, {self.position})"
        return ret


class Dropoff(Entity):
    """
    Dropoff class for housing dropoffs
    """
    pass


class Shipyard(Entity):
    """
    Shipyard class to house shipyards
    """
    def spawn(self):
        """Return a move to spawn a new ship."""
        return commands.GENERATE


class Ship(Entity):
    """
    Ship class to house ship entities
    """
    def __init__(self, owner, id, position, halite_amount):
        super().__init__(owner, id, position)
        self.halite_amount = halite_amount
        self.position_goal = Position(0, 0)
        self.behavior = None
        self.is_inspired = False
        self.distance_from_home = 0
        self.home_position = Position(0, 0)
        self.mission = Mission(Mission_types[HARVEST],  # Mission type
                               [],                      # Path
                               0,                       # Reward
                               0)                       # Remaining time

    @property
    def is_full(self):
        """Is this ship at max halite capacity?"""
        return self.halite_amount >= constants.MAX_HALITE

    def make_dropoff(self):
        """Return a move to transform this ship into a dropoff."""
        ret = f"{commands.CONSTRUCT} {self.id}"
        return ret

    def move(self, direction):
        """
        Return a move to move this ship in a direction without
        checking for collisions.
        """
        raw_direction = direction
        if not isinstance(direction, str) or direction not in "nsewo":
            raw_direction = Direction.convert(direction)

        ret = f"{commands.MOVE} {self.id} {raw_direction}"
        return ret

    def stay_still(self):
        """
        Don't move this ship.
        """
        ret = f"{commands.MOVE} {self.id} {commands.STAY_STILL}"
        return ret

    def update(self, position, halite_amount):
        self.position = position
        self.halite_amount = halite_amount
        return self

    @staticmethod
    def _get_info():
        """
        Gets the info about an instance of a ship.
        """
        ship_id, x_position, y_position, halite = map(int, read_input().split())
        position = Position(x_position, y_position)
        return ship_id, position, halite

    @staticmethod
    def _generate(player_id):
        """
        Creates an instance of a ship for a given player given the engine's input.
        :param player_id: The id of the player who owns this ship
        :return: The ship id and ship object
        """
        ship_id, x_position, y_position, halite = map(int, read_input().split())
        return ship_id, Ship(player_id, ship_id, Position(x_position, y_position), halite)

    def __repr__(self):
        ret = f"{self.__class__.__name__}(id={self.id}, {self.position}, " \
               f"cargo={self.halite_amount} halite)"
        return ret
