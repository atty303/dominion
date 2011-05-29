# -*- coding: utf-8; -*-

import itertools
import random


class Kind(object):
    Treasure = 'treasure'
    Victory = 'victory'
    Curse = 'curse'
    Action = 'action'


# ゲームで利用するカードの種類を表現するクラス
# カードの振る舞い(Behaviour)を定義する。
# インスタンスが1つのカード種類を表現する。
# TODO: canPlay?
class CardClass(object):
    def __init__(self, name, kind, cost):
        self.name = name
        self._kind = kind
        self.cost = cost

    @property
    def kind(self):
        return self._kind

    def set_action(self, callback):
        self._action = callback

    def play(self):
        """カードをプレイしたときの動作を実行する。"""
        return self._action(self)

    def __repr__(self):
        return "<CardClass '%s'>" % self.name


class CardClassFactory(object):
    def __init__(self):
        self.card_classes = {}

    def add_card_class(self, card_class):
        self.card_classes[card_class.name] = card_class

    def __getitem__(self, name):
        return self.card_classes[name]


# カードそのものを表現するクラス
# インスタンスが1枚のカードを表現する。
class Card(object):
    def __init__(self, card_class):
        self.card_class = card_class

    def __repr__(self):
        return "<Card '%s' at 0x%x>" % (self.card_class.name, id(self))


def generate_cards(card_class, count):
    return [Card(card_class) for i in range(count)]


# カードの山を表現するクラス
class CardPile(object):
    def __init__(self, cards=[]):
        self._list = list(reversed(cards))

    def count(self):
        return len(self._list)

    def __getitem__(self, n):
        """山の上からn番目に位置するカードを返す。

        0 -- 山の上部、-1 -- 山の底部
        """
        # 山はリストで実装
        return self._list[n]

    def add_top(self, card):
        """山の上にカードを載せる。"""
        if isinstance(card, list) or isinstance(card, tuple):
            for c in card:
                self._list.insert(0, c)
        else:
            self._list.insert(0, card)

    def remove_top(self, count):
        removed = self._list[:count]
        del self._list[:count]
        return removed

    def shuffle(self, random_generator=random.random):
        random.shuffle(self._list, random=random_generator)


class Supply(object):
    def __init__(self):
        self.piles_dict = {}

    def add_pile(self, pile):
        if len(frozenset([c.card_class for c in pile])) > 1:
            raise ValueError("Couldn't add variant pile; %r" % pile)
        card_class = pile[0].card_class
        if card_class in self.piles_dict.keys():
            raise KeyError("Couldn't add duplicated card class %r" % card_class)
        self.piles_dict[card_class] = pile

    def __contains__(self, card_class):
        return card_class in self.piles_dict.keys()

    @property
    def piles(self):
        return self.piles_dict


class Player(object):
    def __init__(self, name):
        self.name = name
        self.hands = CardPile()
        self.deck = CardPile()
        self.actions = 0
        self.buys = 0

    def draw_card(self, count):
        dealed_cards = self.deck.remove_top(count)
        self.hands.add_top(dealed_cards)


class Game(object):
    def __init__(self, players, supply):
        """
        players -- ゲームに参加するプレイヤのリスト。
        リスト内でのプレイヤの順序がそのままターンの進行順となる。
        """
        self.players = players
        self.supply = supply

        self.current_player = None
        self.players_cycle = itertools.cycle(self.players)

    def players_count(self):
        return len(self.players)

    def next_player(self):
        self.current_player = self.players_cycle.next()
        return self.current_player


def create_basic_factory():
    factory = CardClassFactory()

    factory.add_card_class(CardClass('Cooper', Kind.Treasure, 0))
    factory.add_card_class(CardClass('Silver', Kind.Treasure, 3))
    factory.add_card_class(CardClass('Gold', Kind.Treasure, 6))

    factory.add_card_class(CardClass('Estate', Kind.Victory, 2))
    factory.add_card_class(CardClass('Duchy', Kind.Victory, 5))
    factory.add_card_class(CardClass('Province', Kind.Victory, 8))

    return factory
