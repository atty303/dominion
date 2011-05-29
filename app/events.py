# -*- coding: utf-8; -*-


class Event(object):
    def resolv(self):
        pass


class ProduceCoin(Event):
    def __init__(self, value):
        self.value = value

    def resolv(self, game):
        game.current_player.coins += self.value
