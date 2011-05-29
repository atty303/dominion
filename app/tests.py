# -*- coding: utf-8; -*-

import unittest

import models


class CardClassTest(unittest.TestCase):
    def test1(self):
        card = models.CardClass('Cooper', models.Kind.Treasure, 0)
        self.assertEqual('Cooper', card.name)
        self.assertEqual(models.Kind.Treasure, card.kind)
        self.assertEqual(0, card.cost)

        card = models.CardClass('Province', models.Kind.Victory, 8)
        self.assertEqual('Province', card.name)
        self.assertEqual(models.Kind.Victory, card.kind)
        self.assertEqual(8, card.cost)

    def test_repr(self):
        card = models.CardClass('Cooper', models.Kind.Treasure, 0)
        self.assertEqual("<CardClass 'Cooper'>", repr(card))

    def test_action(self):
        cc = models.CardClass('Village', models.Kind.Action, 3)
        def action(obj):
            yield True
        cc.set_action(action)
        generator = cc.play()
        result = generator.next()
        self.assertEqual(True, result)
        self.assertRaises(StopIteration, lambda: generator.next())


class CardClassFactoryTest(unittest.TestCase):
    def test_raises_exception_if_card_is_not_exists(self):
        factory = models.CardClassFactory()
        self.assertRaises(KeyError, lambda: factory['NotExists'])

    def test_1(self):
        card = models.CardClass('Sample', models.Kind.Victory, 0)
        factory = models.CardClassFactory()
        factory.add_card_class(card)
        self.assertEqual(card, factory['Sample'])

    def test_factory_creation(self):
        factory = models.create_basic_factory()
        self.assertEqual('Cooper', factory['Cooper'].name)


class CardTest(unittest.TestCase):
    def setUp(self):
        factory = models.create_basic_factory()
        self.cooper_class = factory['Cooper']

    def test1(self):
        card = models.Card(self.cooper_class)
        self.assertEqual(self.cooper_class, card.card_class)

    def test_repr(self):
        card = models.Card(self.cooper_class)
        self.assertEqual("<Card 'Cooper' at 0x%x>" % id(card), repr(card))


class CardPileFuncTest(unittest.TestCase):
    def test(self):
        factory = models.create_basic_factory()
        cooper_class = factory['Cooper']
        cards = models.generate_cards(cooper_class, 2)
        self.assertEqual(cards[0].card_class, cooper_class)
        self.assertEqual(cards[1].card_class, cooper_class)
        self.assertTrue(cards[0] != cards[1])


class CardPileTest(unittest.TestCase):
    def setUp(self):
        factory = models.create_basic_factory()
        self.cooper_card = models.Card(factory['Cooper'])
        self.silver_card = models.Card(factory['Silver'])
        self.gold_card = models.Card(factory['Gold'])

    def test_init_with_empty(self):
        pile = models.CardPile()
        self.assertEqual(0, pile.count())

    def test_init_with_cards(self):
        cards = [self.cooper_card, self.silver_card]
        pile = models.CardPile(cards)
        self.assertEqual(2, pile.count())
        self.assertEqual(self.silver_card, pile[0])
        self.assertEqual(self.cooper_card, pile[1])

    def test_add_top_orderness(self):
        pile = models.CardPile()
        pile.add_top(self.cooper_card)
        pile.add_top(self.silver_card)
        self.assertEqual(2, pile.count())
        self.assertEqual(self.silver_card, pile[0])
        self.assertEqual(self.cooper_card, pile[1])
        self.assertEqual(self.cooper_card, pile[-1])
        self.assertEqual(self.silver_card, pile[-2])

    def test_add_card_list(self):
        cards = [self.cooper_card, self.silver_card, self.gold_card]

        pile = models.CardPile()
        pile.add_top(cards)

        self.assertEqual(self.cooper_card, pile[2])
        self.assertEqual(self.silver_card, pile[1])
        self.assertEqual(self.gold_card, pile[0])

    def test_remove_top(self):
        cards = [self.cooper_card, self.silver_card, self.gold_card]
        pile = models.CardPile()
        pile.add_top(cards)

        removed_card = pile.remove_top(1)
        self.assertEqual(2, pile.count())
        self.assertEqual([self.gold_card], removed_card)

        removed_card = pile.remove_top(2)
        self.assertEqual(0, pile.count())
        self.assertEqual([self.silver_card, self.cooper_card], removed_card)

    def test_card_pile_can_shuffle(self):
        pile = models.CardPile()
        pile.add_top(self.cooper_card)
        pile.add_top(self.silver_card)
        pile.add_top(self.gold_card)

        # 常に0を返す乱数生成器を使い山をシャッフルする。
        pile.shuffle(random_generator=lambda: 0)

        self.assertEqual(self.gold_card, pile[2])
        self.assertEqual(self.cooper_card, pile[1])
        self.assertEqual(self.silver_card, pile[0])


# - player can draw from deck
# - player can discards hands
# - player has playing area
# - player has discard pile
# - player references trash area
class PlayerTest(unittest.TestCase):
    def setUp(self):
        factory = models.create_basic_factory()
        self.cooper_card = models.Card(factory['Cooper'])
        self.silver_card = models.Card(factory['Silver'])
        self.gold_card = models.Card(factory['Gold'])

    def test_player_has_name(self):
        player = models.Player(name='homura')
        self.assertEqual('homura', player.name)

    def test_hands_empty(self):
        player = models.Player('name')
        self.assertEqual(0, player.hands.count())

    def test_hands(self):
        player = models.Player('name')
        player.hands.add_top(self.cooper_card)
        self.assertEqual(1, player.hands.count())

    def test_deck_empty(self):
        player = models.Player('name')
        self.assertEqual(0, player.deck.count())

    def test_draw_card(self):
        player = models.Player('name')
        player.deck.add_top([self.cooper_card, self.silver_card, self.gold_card])
        self.assertEqual(0, player.hands.count())

        player.draw_card(1)

        self.assertEqual(2, player.deck.count())
        self.assertEqual(1, player.hands.count())
        self.assertEqual(self.gold_card, player.hands[0])

        player.draw_card(2)

        self.assertEqual(0, player.deck.count())
        self.assertEqual(3, player.hands.count())
        self.assertEqual([self.cooper_card, self.silver_card, self.gold_card],
                         list(player.hands))

    def test_player_has_action_resource(self):
        player = models.Player('1')
        self.assertEqual(0, player.actions)
        player.actions = 1
        self.assertEqual(1, player.actions)

    def test_player_has_buy_resource(self):
        player = models.Player('1')
        self.assertEqual(0, player.buys)
        player.buys = 1
        self.assertEqual(1, player.buys)


class SupplyTest(unittest.TestCase):
    def setUp(self):
        factory = models.create_basic_factory()
        self.cooper_class = factory['Cooper']
        self.silver_class = factory['Silver']

    def test1(self):
        supply = models.Supply()
        cooper_pile = models.CardPile(models.generate_cards(self.cooper_class, 60))
        supply.add_pile(cooper_pile)

        self.assertTrue(self.cooper_class in supply)
        self.assertTrue(self.silver_class not in supply)
        self.assertEqual({self.cooper_class: cooper_pile}, supply.piles)

    def test_add_duplicated_pile(self):
        supply = models.Supply()
        def add_cooper_to_pile():
            copper_pile = models.CardPile(models.generate_cards(self.cooper_class, 60))
            supply.add_pile(copper_pile)
        # サプライに銅貨の山を追加する
        add_cooper_to_pile()
        # 既にサプライに存在するカードクラス"銅貨"の山をさらに追加することはできない
        self.assertRaises(KeyError, add_cooper_to_pile)

    # この制約はなくていいかも
    def test_add_variant_pile(self):
        variant_pile = models.CardPile()
        variant_pile.add_top(models.Card(self.cooper_class))
        variant_pile.add_top(models.Card(self.silver_class))

        supply = models.Supply()
        def add_variant_pile_to_supply():
            supply.add_pile(variant_pile)
        self.assertRaises(ValueError, add_variant_pile_to_supply)


class GameTest(unittest.TestCase):
    def test_game_has_player(self):
        player1 = models.Player('1')
        game = models.Game(players=[player1], supply=None)
        self.assertEqual(1, game.players_count())
        self.assertEqual([player1], game.players)

    def test_game_has_supply(self):
        empty_supply = models.Supply()
        game = models.Game(players=[models.Player('1')], supply=empty_supply)
        self.assertEqual(empty_supply, game.supply)

    def test_initial_game_has_no_current_player(self):
        player = models.Player('1')
        game = models.Game(players=[player], supply=None)

        self.assertEqual(None, game.current_player)

    def test_next_player(self):
        player1, player2 = models.Player('1'), models.Player('2')
        game = models.Game(players=[player1, player2], supply=None)

        next_player = game.next_player()
        self.assertEqual(player1, game.current_player)

        next_player = game.next_player()
        self.assertEqual(player2, game.current_player)

        next_player = game.next_player()
        self.assertEqual(player1, game.current_player)


if __name__ == '__main__':
    unittest.main()

