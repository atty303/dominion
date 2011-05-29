import models


def format_card_class(cclass):
    return '%.12s/%1.1s' % (cclass.name, cclass.cost)

def dump_supply(supply):
    print '==== SUPPLY'
    for cclass, pile in supply.piles.items():
        print '(%2d) %-20s' % (pile.count(), format_card_class(cclass)),
    print

def dump_player(player):
    print u'==== PLAYER %s (A:%d B:%d C:%d)' % (player.name, player.actions, player.buys, player.coins)
    # print 'HANDS: %2d  DECK: %3d' % (player.hands.count(), player.deck.count())
    # for i, card in enumerate(player.hands):
    #     print '%2d:[%s] ' % (i+1, format_card_class(card.card_class)),
    # print
    print ' HAND: %2d [%s]' % (player.hands.count(), format_pile(player.hands))
    print ' DECK: %2d [%s]' % (player.deck.count(), format_pile(player.deck))
    print ' PLAY AREA: %2d [%s]' % (player.play_area.count(), format_pile(player.play_area))
    print ' DISCARDS: %2d [%s]' % (player.discard_pile.count(), format_pile(player.discard_pile))

def format_pile(pile):
    return ' '.join([format_card_class(card.card_class) for card in pile])

def select_player(player):
    dump_player(player)
    selected = None
    while selected is None:
        value = raw_input(">>> Select a card to play: ")
        try:
            n = int(value) - 1
            if n >= 0 and n < player.hands.count():
                selected = n
        except:
            pass
    return player.hands[selected]

def select_card_class_from_supply(supply, matcher=lambda card_class, pile_count: True):
    classes = [cc for cc, pile in supply.piles.items() if matcher(cc, pile.count())]

    selected = None
    while selected is None:
        for i, cc in enumerate(classes):
            print '%2d:[%s] ' % (i+1, format_card_class(cc)),
        print

        value = raw_input(">>> Select a card from supply: ")
        if value == '':
            return None
        try:
            n = int(value) - 1
            if n >= 0 and n < len(classes):
                selected = n
        except:
            pass

    return classes[selected]


def main():
    factory = models.create_basic_factory()

    players = [models.Player('atty303')]
    for player in players:
        player.deck.add_top(models.generate_cards(factory['Cooper'], 7))
        player.deck.add_top(models.generate_cards(factory['Estate'], 3))
        player.deck.shuffle()

        player.draw_card(5)

        dump_player(player)

    supply = models.Supply()
    supply.add_pile(models.CardPile(models.generate_cards(factory['Cooper'], 60)))
    supply.add_pile(models.CardPile(models.generate_cards(factory['Silver'], 40)))
    supply.add_pile(models.CardPile(models.generate_cards(factory['Gold'], 30)))

    game = models.Game(players=players, supply=supply)

    dump_supply(game.supply)

    # start game
    def turn():
        player = game.next_player()
        player.actions = 1
        player.buys = 1
        player.coins = 0

        print
        print "******** %r's turn ********" % player

        print "*** Action phase ***"
        dump_player(player)
        # Action phase
        # while player.actions > 0:
        #     select_player(player)

        # Buy phase
        print "*** Buy phase ***"
        # playing all treasure cards
        treasure_cards = [c for c in player.hands if c.card_class.card_type == models.CardType.Treasure]
        for card in treasure_cards:
            print "- playing %r" % card
            player.hands.move_card(card, player.play_area)
            for event in card.card_class.play_ability():
                event.resolv(game)
        dump_player(player)

        # buying
        while player.buys > 0:
            def buy_matcher(card_class, pile_count):
                return card_class.cost <= player.coins and pile_count > 0
            card_class = select_card_class_from_supply(game.supply,
                                                       matcher=buy_matcher)
            if not card_class:
                break
            print "- %r buying %r" % (player, card_class)
            player.coins -= card_class.cost
            player.buys -= 1

            pile = game.supply.piles[card_class]
            card = pile.remove_top(1)
            player.discard_pile.add_top(card)
            dump_player(player)

        # Cleanup phase
        print "*** Cleanup phase ***"
        player.play_area.move_all(player.discard_pile)
        player.hands.move_all(player.discard_pile)
        player.draw_card(5)
        dump_player(player)

    while True:
        turn()


if __name__ == '__main__':
    main()

