from .entity import Shipyard, Ship, Dropoff
from .positionals import Position
from .common import read_input


class Player:
    """
    Player object containing all items/metadata pertinent to the player.
    """
    def __init__(self, player_id, shipyard, halite=0):
        self.id = player_id
        self.shipyard = shipyard
        self.halite_amount = halite
        self._ships = {}
        self._old_ship_ids = []
        self._dropoffs = {}
        self.ship_states = {}

    def get_ship(self, ship_id):
        """
        Returns a singular ship mapped by the ship id
        :param ship_id: The ship id of the ship you wish to return
        :return: the ship object.
        """
        return self._ships[ship_id]

    def get_ships(self):
        """
        :return: Returns all ship objects in a list
        """
        return list(self._ships.values())

    def get_dropoff(self, dropoff_id):
        """
        Returns a singular dropoff mapped by its id
        :param dropoff_id: The dropoff id to return
        :return: The dropoff object
        """
        return self._dropoffs[dropoff_id]

    def get_dropoffs(self):
        """
        :return: Returns all dropoff objects in a list
        """
        return list(self._dropoffs.values())

    def has_ship(self, ship_id):
        """
        Check whether the player has a ship with a given ID.

        Useful if you track ships via IDs elsewhere and want to make
        sure the ship still exists.

        :param ship_id: The ID to check.
        :return: True if and only if the ship exists.
        """
        return ship_id in self._ships



    @staticmethod
    def _generate():
        """
        Creates a player object from the input given by the game engine
        :return: The player object
        """
        player, shipyard_x, shipyard_y = map(int, read_input().split())
        return Player(player, Shipyard(player, -1, Position(shipyard_x, shipyard_y)))

    def _update(self, num_ships, num_dropoffs, halite):
        """
        Updates this player object considering the input from the game engine for the current specific turn.
        :param num_ships: The number of ships this player has this turn
        :param num_dropoffs: The number of dropoffs this player has this turn
        :param halite: How much halite the player has in total
        :return: nothing.
        """
        self.halite_amount = halite

        ### Update ships ###
        ships_info = [[ship_id, ship_position, ship_halite] for (ship_id, ship_position, ship_halite) in
            [Ship._get_info() for _ in range(num_ships)]]
        ships_alive = []
        for line in ships_info:
            ship_id = line[0]
            ship_position = line[1]
            ship_halite = line[2]
            ships_alive.append(ship_id)
            if ship_id in self.old_ship_ids:
                self.get_ship(ship_id).update(ship_position, ship_halite)
            else:
                ship = Ship(self.id, ship_id, ship_position, ship_halite)
                self._ships[ship_id] = ship
        dead_ships = set(self._ships.keys()) - set(ships_alive)
        for dead_ship  in dead_ships:
            self._ships.pop(dead_ship)
        self.old_ship_ids = self._ships.keys()

        ### Update dropoffs ###
        self._dropoffs = {id: dropoff for (id, dropoff) in [Dropoff._generate(self.id) for _ in range(num_dropoffs)]}
