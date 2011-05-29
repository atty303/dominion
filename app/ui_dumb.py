import models


def format_card_class(cclass):
    return '%.16s/%1.1s' % (cclass.name, cclass.cost)

def dump_supply(supply):
    print '---- SUPPLY ----'
    for cclass, pile in supply.piles.items():
        print '(%2d) %-20s' % (pile.count(), format_card_class(cclass)),
    print

def dump_player(player):
    print u'---- PLAYER %s ----' % player.name
    print 'HANDS: %2d  DECK: %3d' % (player.hands.count(), player.deck.count())
    for i, card in enumerate(player.hands):
        print '%2d:[%s] ' % (i+1, format_card_class(card.card_class)),
    print


def main():
    factory = models.create_basic_factory()

    player = models.Player('atty303')

    supply = models.Supply()
    supply.add_pile(models.CardPile(models.generate_cards(factory['Cooper'], 60)))
    supply.add_pile(models.CardPile(models.generate_cards(factory['Silver'], 40)))
    supply.add_pile(models.CardPile(models.generate_cards(factory['Gold'], 30)))

    game = models.Game(players=[player], supply=supply)

    dump_supply(game.supply)

    player.deck.add_top(models.generate_cards(factory['Cooper'], 7))
    player.deck.add_top(models.generate_cards(factory['Estate'], 3))
    player.deck.shuffle()

    player.draw_card(5)

    dump_player(player)

if __name__ == '__main__':
    main()

