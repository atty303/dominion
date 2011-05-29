from models import CardClass, Kind




class Villeage(CardClassTemplate):
    kind = Kind.Action
    cost = 3

    @staticmethod
    def action(self):
        yield actions.ProduceAction(actions.PLAYER_SELF, 2)

class Cellar(CardClassTemplate):
    kind = kind.Action
    cost = 2

    @staticmethod
    def action(self, player):
        selected_cards = yield SelectOnHandsAction()
        player.discard(selected_cards)
        player.draw(len(selected_cards))

class Militia(CardClassTemplate):
    kind = kind.Action
    cost = 2

    @staticmethod
    def action(self, player):
        yield actions.ProduceCoin(actions.PLAYER_SELF, 2)
        selected_cards = yield actions.SelectCards(actions.PLAYER_OTHERS, 2)

class Smithy(CardClassTemplate):
    kind = kind.Action
    cost = 3

    @staticmethod
    def action(self, player):
        yield action.DrawCard(actions.PLAYER_SELF, 3)


# Feast
# yield TrashCard(self)


def setup_factory(factory):
    factory.add_card_class(CardClass('Cooper', Kind.Treasure, 0))
    factory.add_card_class(CardClass('Silver', Kind.Treasure, 3))
    factory.add_card_class(CardClass('Gold', Kind.Treasure, 6))

    factory.add_card_class(CardClass('Estate', Kind.Victory, 2))
    factory.add_card_class(CardClass('Duchy', Kind.Victory, 5))
    factory.add_card_class(CardClass('Province', Kind.Victory, 8))

    factory.add_card_class(CardClass('Curse', Kind.Curse, 0))

    card = CardClass('Village', Kind.Action, 3)
    def action(self):
        yield Resource(action=2)
    card.set_action(action)
    factory.add_card_class(card)
