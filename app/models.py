# -*- coding: utf-8; -*-

import itertools
import random


class CardType(object):
    Treasure = 'treasure'
    Victory = 'victory'
    Curse = 'curse'
    Action = 'action'


# ゲームで利用するカードの種類を表現するクラス
# カードの振る舞い(Behaviour)を定義する。
# インスタンスが1つのカード種類を表現する。
# TODO: canPlay?
class CardClass(object):
    def __init__(self, name, card_type, cost):
        self.name = name
        self._card_type = card_type
        self.cost = cost
        self.ability = None

    @property
    def card_type(self):
        return self._card_type

    def play_ability(self):
        """カードをプレイしたときの動作を実行する。"""
        return self.ability(self)

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

    def remove_card(self, card):
        self._list.remove(card)

    def move_card(self, card, to_pile):
        self.remove_card(card)
        to_pile.add_top(card)

    def shuffle(self, random_generator=random.random):
        random.shuffle(self._list, random=random_generator)


class Supply(object):
    def __init__(self):
        self.piles_dict = {}
        self._card_classes = set()

    def add_pile(self, pile):
        if len(frozenset([c.card_class for c in pile])) > 1:
            raise ValueError("Couldn't add variant pile; %r" % pile)
        card_class = pile[0].card_class
        if card_class in self._card_classes:
            raise KeyError("Couldn't add duplicated card class %r" % card_class)
        self.piles_dict[card_class] = pile
        self._card_classes.add(card_class)

    @property
    def piles(self):
        return self.piles_dict

    def card_classes(self):
        return self._card_classes


class Player(object):
    def __init__(self, name):
        self.name = name
        self.hands = CardPile()
        self.deck = CardPile()
        self.play_area = CardPile()
        self.discard_pile = CardPile()
        self.actions = 0
        self.buys = 0
        self.coins = 0

    def draw_card(self, count):
        dealed_cards = self.deck.remove_top(count)
        self.hands.add_top(dealed_cards)

    def __repr__(self):
        return "<Player '%s'>" % self.name


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


class CardClassTemplate(object):
    @classmethod
    def to_card_class(cls):
        cc = CardClass(cls.__name__, cls.card_type, cls.cost)
        if hasattr(cls, 'ability'):
            cc.ability = cls.ability
        return cc


def create_basic_factory():
    factory = CardClassFactory()

    import cards_basic
    cards_basic.setup_factory(factory)

    factory.add_card_class(CardClass('Estate', CardType.Victory, 2))
    factory.add_card_class(CardClass('Duchy', CardType.Victory, 5))
    factory.add_card_class(CardClass('Province', CardType.Victory, 8))

    return factory
