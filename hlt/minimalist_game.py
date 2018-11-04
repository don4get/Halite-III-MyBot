import sys


class Ship:
    def __init__(self, id, x, y, halite):
        self.id = id
        self.position = Position(x, y)
        self.halite = halite


class Directions:
    NORTH = (0, -1)
    SOUTH = (0, 1)
    EAST = (1, 0)
    WEST = (-1, 0)
    NONE = (0, 0)
    ALL = ((0, 1), (1, 0), (0, -1), (-1, 0), (0, 0))


direction_strings = {Directions.NORTH: 'n',
                     Directions.EAST: 'e',
                     Directions.SOUTH: 's',
                     Directions.WEST: 'w',
                     Directions.NONE: 'o'}


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return self.x * 1000 +  self.y

    def distance(self, other):
        x_diff = min(abs(self.x - other.x), Game.WIDTH - abs(self.x - other.x))
        y_diff = min(abs(self.y - other.y), Game.HEIGHT - abs(self.y - other.y))
        return x_diff + y_diff

    def move(self, direction):
        return Position((self.x + direction[0]) % Game.WIDTH, (self.y + direction[1]) % Game.HEIGHT)

    def around(self):
        return [self.move(x) for x in Directions.ALL if x != Directions.NONE]

    def __str__(self):
        return str((self.x, self.y))

    def __repr__(self):
        return str(self)


class Player:
    def __init__(self, id, spawn_x, spawn_y):
        self.spawn = Position(spawn_x, spawn_y)
        self.id = id
        self.dropoffs = set()
        self.ships = set()
        self.halite = 0

    def reset(self):
        self.dropoffs = set()
        self.ships = set()

    def add_ship(self, ship):
        self.ships.add(ship)

    def add_dropoff(self, pos):
        self.dropoffs.add(pos)

    def set_halite(self, halite):
        self.halite = halite


class Game:
    WIDTH = 0
    HEIGHT = 0

    def __init__(self):
        self.players = {}
        self.commands = []
        self.constants = input()
        self.num_players, self.my_id = map(int, input().split())
        for player in range(self.num_players):
            player_id, spawn_x, spawn_y = map(int, input().split())
            self.players[player_id] = Player(player_id, spawn_x, spawn_y)
        Game.WIDTH, Game.HEIGHT = map(int, input().split())
        # NOTE this is self.halite[y][x] NOT [x][y]
        self.halite = [list(map(int, input().split())) for y in range(Game.HEIGHT)]
        self.turn = 0
        print("Hjax")
        sys.stdout.flush()

    def tiles(self):
        for x in range(Game.WIDTH):
            for y in range(Game.HEIGHT):
                yield Position(x, y)

    def max_turn(self):
        return 400 + ((Game.WIDTH - 32) / 8) * 25

    def turns_left(self):
        return self.max_turn() - self.turn

    def start_frame(self):
        self.turn = int(input())
        self.commands = []
        for player in range(self.num_players):
            player_id, num_ships, num_dropoffs, halite = map(int, input().split())
            self.players[player_id].reset()
            self.players[player_id].set_halite(halite)
            for ship in range(num_ships):
                ship_id, ship_x, ship_y, ship_halite = map(int, input().split())
                self.players[player_id].add_ship(Ship(ship_id, ship_x, ship_y, ship_halite))
            for dropoff in range(num_dropoffs):
                _, drop_x, drop_y = map(int, input().split())
                self.players[player_id].add_dropoff(Position(drop_x, drop_y))
        updates = int(input())
        for update in range(updates):
            hal_x, hal_y, hal_val = map(int, input().split())
            self.halite[hal_y][hal_x] = hal_val

    def move(self, ship, direction):
        self.commands.append("m %d %s" % (ship.id, direction_strings[direction]))

    def build_dropoff(self, ship):
        self.players[self.my_id].halite -= 4000
        self.commands.append("c %d" % ship.id)

    def build_ship(self):
        self.players[self.my_id].halite -= 1000
        self.commands.append('g')

    def halite_at(self, pos):
        return self.halite[pos.y][pos.x]

    def end_frame(self):
        print(" ".join(self.commands))
        sys.stdout.flush()