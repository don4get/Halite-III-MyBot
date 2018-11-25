#!/usr/bin/env python3
"""
###########
Feature bot
###########


"""

import hlt
from hlt.banker import Banker
from hlt.commander import Commander
import logging

__author__ = "don4get"
__copyright__ = ""
__credits__ = ["SentDex", "don4get"]
__version__ = "1.0.0"
__maintainer__ = "don4get"
__status__ = "Production"


class Bot:
    def __init__(self):
        self._game = hlt.Game()
        self._game.ready("FeatureBot")
        self._banker = Banker()
        self._commander = Commander()

    def play_game(self):
        while True:
            self.loop()

    def loop(self):
        self._game.update_frame()
        me = self._game.me

        commands = []
        commands += self._commander.control_ships(self._game)
        commands += self._banker.build_ships(self._game)

        self._game.end_turn(commands)


def main():
    my_bot = Bot()
    my_bot.play_game()


main()
