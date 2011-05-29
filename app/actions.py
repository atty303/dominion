
PLAYER_SELF = 0
PLAYER_OTHERS = 1

def get_target_player_objects(target, game):
    if TARGET_PLAYER_SELF:
        return [game.current_player]
    else:
        return [p for p in game.players if p != game.current_player]

class ActionBase(object):
    pass


class ProduceResource(ActionBase):
    """リソース(ドロー、アクション、購入、コイン)を産み出すアクション"""
    def __init__(self, action=0, buy=0, coin=0):
        self.action = action
        self.buy = buy
        self.coin = coin


class ProduceAction(ActionBase):
    def __init__(self, target_player, value):
        self.target_player = target_player
        self.value = value

    def resolv(self, game):
        for player in get_target_player_objects(game):
            player.resource.add_action(self.value)


class DiscardDeck(ActionBase):
    """デッキを全て捨て札にするアクション"""
    def __init__(self, target_player):
        self.target_player = target_player

    def resolv(self, game):
        players = get_target_player_objects(game)
        for player in players:
            player.deck.discard()


class TrashCard(ActionBase):
    def __init__(self, card):
        self.card = card

    def resolv(self, game):
        card.remove_from_owner()
        game.trash.add(card)


class SelectCards(ActionBase):
    def __init__(self, target_player):
        self.target_player = target_player


# - あなたの手札からカード(任意or特定)をn枚選択する --> 選択したカード
# 誰を対象に？ 何を？
# - コスト(Range)のカードをサプライから獲得

# プレイ

#          |Player |場所     |Filter      |条件 |
# 改築     |あなた |手札     |全て        |1    |
# 改築     |あなた |サプライ |コストn以下 |0〜1 |
# 金貸し   |あなた |手札     |銅貨        |1    |
# 玉座の間 |あなた |手札     |全て        |1    |
# 鉱山     |あなた |手札     |財宝        |1    |
# 鉱山     |あなた |財宝     |コストn以下の財宝 |1    |
# 工房     |あなた |サプライ |コスト4以下 |1    |
# 宰相     |あなた |-        |-           |Bool |
# 祝宴     |あなた |サプライ |コスト5以下 |1    |
