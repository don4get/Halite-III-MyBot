from hlt import logics


class Commander:
    def __init__(self):
        self._position_goals = []
        self._last_movement_commands = []

    def control_ships(self, game):
        me = game.me
        movement_commands = []
        self._position_goals = []
        for ship in me.get_ships():
            logics.choose_behavior(ship, game.game_map, me, game.turn_number,
                                   self._position_goals,
                                   movement_commands)
        return movement_commands
