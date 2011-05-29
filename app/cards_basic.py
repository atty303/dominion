import events
from models import CardClassTemplate, CardType


class Cooper(CardClassTemplate):
    card_type = CardType.Treasure
    cost = 0

    @staticmethod
    def ability(self):
        yield events.ProduceCoin(1)


class Silver(CardClassTemplate):
    card_type = CardType.Treasure
    cost = 3

    @staticmethod
    def ability(self):
        yield events.ProduceCoin(2)


class Gold(CardClassTemplate):
    card_type = CardType.Treasure
    cost = 6

    @staticmethod
    def ability(self):
        yield events.ProduceCoin(3)


def setup_factory(factory):
    factory.add_card_class(Cooper.to_card_class())
    factory.add_card_class(Silver.to_card_class())
    factory.add_card_class(Gold.to_card_class())
